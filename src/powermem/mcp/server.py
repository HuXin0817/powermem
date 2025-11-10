"""
MCP Server implementation for powermem

This module implements a Model Context Protocol (MCP) server that exposes
powermem's memory management capabilities as MCP tools and resources.
"""

import json
import sys
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime, date

from ..core.memory import Memory
from ..config_loader import auto_config
from ..core.setup import get_user_id

# Import create_memory from main module (it's defined in __init__.py)
def create_memory(config=None, **kwargs):
    """
    Create a Memory instance with automatic configuration loading.
    This is a local implementation to avoid circular imports.
    """
    if config is None:
        config = auto_config()
    return Memory(config=config, **kwargs)

logger = logging.getLogger(__name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def sanitize_for_json(data, _visited=None):
    """
    Recursively convert datetime objects and other non-serializable objects to JSON-compatible types.
    
    Args:
        data: Data structure that may contain datetime objects or other non-serializable objects
        _visited: Set to track visited objects and prevent infinite recursion
        
    Returns:
        Sanitized data structure with all datetime objects converted to ISO format strings
    """
    if _visited is None:
        _visited = set()
    
    # Prevent infinite recursion
    obj_id = id(data)
    if obj_id in _visited:
        return data
    _visited.add(obj_id)
    
    try:
        # First check for datetime/date (before other type checks)
        if isinstance(data, (datetime, date)):
            return data.isoformat()
        
        # Check for datetime-like objects that might have isoformat method
        if hasattr(data, 'isoformat') and callable(getattr(data, 'isoformat', None)):
            try:
                # Try to call isoformat if it exists (handles datetime subclasses)
                if isinstance(data, (datetime, date)):
                    return data.isoformat()
            except Exception:
                pass
        
        # Handle Pydantic models
        if hasattr(data, 'model_dump'):
            try:
                data = data.model_dump(mode='json')  # Use mode='json' to auto-serialize dates
                # Recursively sanitize the result to catch any datetime objects that might have been missed
                # This is important because mode='json' might not always serialize nested datetime objects
                if isinstance(data, dict):
                    data = {k: sanitize_for_json(v, _visited) for k, v in data.items()}
                elif isinstance(data, list):
                    data = [sanitize_for_json(item, _visited) for item in data]
            except Exception:
                try:
                    dumped = data.model_dump()
                    # Recursively sanitize the dumped result
                    if isinstance(dumped, dict):
                        data = {k: sanitize_for_json(v, _visited) for k, v in dumped.items()}
                    elif isinstance(dumped, list):
                        data = [sanitize_for_json(item, _visited) for item in dumped]
                    else:
                        data = dumped
                except Exception:
                    if hasattr(data, '__dict__'):
                        data = data.__dict__
        
        # Handle objects with dict() method or __dict__ attribute
        if not isinstance(data, (dict, list, str, int, float, bool, type(None))):
            if hasattr(data, '__dict__'):
                try:
                    data = {k: v for k, v in data.__dict__.items() if not k.startswith('_')}
                except Exception:
                    pass
            elif hasattr(data, 'dict'):
                try:
                    data = data.dict()
                except Exception:
                    pass
        
        # Recursively process collections
        if isinstance(data, dict):
            result = {}
            for k, v in data.items():
                # Recursively sanitize values (use same visited set)
                sanitized_v = sanitize_for_json(v, _visited)
                result[k] = sanitized_v
            return result
        elif isinstance(data, list):
            result = []
            for item in data:
                # Recursively sanitize items (use same visited set)
                sanitized_item = sanitize_for_json(item, _visited)
                result.append(sanitized_item)
            return result
        elif isinstance(data, tuple):
            result = tuple(sanitize_for_json(item, _visited) for item in data)
            return result
        elif isinstance(data, (datetime, date)):
            # Double-check (shouldn't reach here but just in case)
            return data.isoformat()
        else:
            return data
    finally:
        _visited.discard(obj_id)


def safe_json_dumps(obj: Any, **kwargs) -> str:
    """
    Safely serialize object to JSON, handling datetime and other non-serializable types.
    
    Args:
        obj: Object to serialize
        **kwargs: Additional arguments to pass to json.dumps
        
    Returns:
        JSON string
    """
    # Sanitize the object multiple times to catch all nested datetime objects
    sanitized = sanitize_for_json(obj)
    sanitized = sanitize_for_json(sanitized)  # Second pass to catch any missed objects
    
    # Enhanced json_serial that also handles any remaining edge cases
    def enhanced_json_serial(obj):
        """Enhanced JSON serializer with fallbacks"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        # Handle datetime-like objects with isoformat method
        if hasattr(obj, 'isoformat') and callable(getattr(obj, 'isoformat', None)):
            try:
                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()
            except Exception:
                pass
        # Handle other common non-serializable types
        if hasattr(obj, '__dict__'):
            try:
                return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
            except Exception:
                pass
        # Try to convert unknown objects to string
        try:
            return str(obj)
        except Exception:
            return None
    
    # Use enhanced serializer as fallback
    try:
        return json.dumps(sanitized, default=enhanced_json_serial, **kwargs)
    except TypeError as e:
        # Last resort: try one more deep sanitization
        logger.warning(f"JSON serialization failed, attempting one more sanitization pass: {e}")
        final_sanitized = sanitize_for_json(sanitized)
        return json.dumps(final_sanitized, default=enhanced_json_serial, **kwargs)


class MCPServer:
    """
    MCP Server for powermem that exposes memory operations as tools.
    
    The server communicates via STDIO using JSON-RPC 2.0 protocol.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MCP server.
        
        Args:
            config: Optional powermem configuration dictionary.
                   If None, will attempt to load from environment.
        """
        self.config = config
        self.memory: Optional[Memory] = None
        self.request_id: Optional[str] = None
        
    def initialize_memory(self):
        """Initialize the memory instance."""
        if self.memory is None:
            if self.config is None:
                self.config = auto_config()
            self.memory = create_memory(config=self.config)
            logger.info("Memory instance initialized")
    
    def get_default_user_id(self) -> str:
        """
        Get or generate a default user_id for MCP operations.
        
        Returns:
            User ID string
        """
        try:
            return get_user_id()
        except Exception as e:
            logger.warning(f"Failed to get user_id from config: {e}, using default")
            # Fallback to a default user ID for MCP sessions
            return "mcp_user"
    
    def get_user_id_from_args(self, arguments: Dict[str, Any]) -> Optional[str]:
        """
        Get user_id from arguments, or use default if not provided.
        
        Args:
            arguments: Tool call arguments
            
        Returns:
            User ID (never None, always returns a valid user_id)
        """
        user_id = arguments.get("user_id")
        if not user_id:
            user_id = self.get_default_user_id()
            logger.debug(f"Using default user_id: {user_id}")
        return user_id
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Return the list of available MCP tools.
        
        Returns:
            List of tool definitions following MCP schema
        """
        return [
            {
                "name": "add_memory",
                "description": "Add a new memory to the memory store. Can accept text, a message dict, or a list of messages.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "messages": {
                            "type": ["string", "object", "array"],
                            "description": "The content to store. Can be a string, a message dict with 'role' and 'content', or a list of message dicts."
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Optional user identifier for the memory"
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "Optional agent identifier for multi-agent scenarios"
                        },
                        "run_id": {
                            "type": "string",
                            "description": "Optional run/thread identifier for grouping related memories"
                        },
                        "metadata": {
                            "type": "object",
                            "description": "Optional metadata dictionary to attach to the memory"
                        },
                        "scope": {
                            "type": "string",
                            "description": "Optional scope for the memory (e.g., 'user', 'agent', 'session')"
                        },
                        "memory_type": {
                            "type": "string",
                            "description": "Optional memory type classification"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters dictionary for advanced filtering"
                        }
                    },
                    "required": ["messages"]
                }
            },
            {
                "name": "search_memories",
                "description": "Search for memories using semantic similarity and keyword matching",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query text"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Optional user identifier to filter memories"
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "Optional agent identifier to filter memories"
                        },
                        "run_id": {
                            "type": "string",
                            "description": "Optional run/thread identifier to filter memories"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 10)",
                            "default": 10
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional metadata filters for advanced search"
                        },
                        "threshold": {
                            "type": "number",
                            "description": "Optional similarity threshold (0.0-1.0) for filtering results"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_memory",
                "description": "Retrieve a specific memory by its ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "memory_id": {
                            "type": "integer",
                            "description": "The unique identifier of the memory to retrieve"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Optional user identifier for permission check"
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "Optional agent identifier for permission check"
                        }
                    },
                    "required": ["memory_id"]
                }
            },
            {
                "name": "update_memory",
                "description": "Update an existing memory's content and/or metadata",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "memory_id": {
                            "type": "integer",
                            "description": "The unique identifier of the memory to update"
                        },
                        "content": {
                            "type": "string",
                            "description": "The new content for the memory"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Optional user identifier for permission check"
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "Optional agent identifier for permission check"
                        },
                        "metadata": {
                            "type": "object",
                            "description": "Optional metadata dictionary to update"
                        }
                    },
                    "required": ["memory_id", "content"]
                }
            },
            {
                "name": "delete_memory",
                "description": "Delete a memory by its ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "memory_id": {
                            "type": "integer",
                            "description": "The unique identifier of the memory to delete"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Optional user identifier for permission check"
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "Optional agent identifier for permission check"
                        }
                    },
                    "required": ["memory_id"]
                }
            },
            {
                "name": "delete_all_memories",
                "description": "Delete all memories for a user and/or agent",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Optional user identifier to filter memories for deletion"
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "Optional agent identifier to filter memories for deletion"
                        },
                        "run_id": {
                            "type": "string",
                            "description": "Optional run/thread identifier to filter memories for deletion"
                        }
                    }
                }
            },
            {
                "name": "list_memories",
                "description": "List all memories with optional filters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Optional user identifier to filter memories"
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "Optional agent identifier to filter memories"
                        },
                        "run_id": {
                            "type": "string",
                            "description": "Optional run/thread identifier to filter memories"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 100)",
                            "default": 100
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Offset for pagination (default: 0)",
                            "default": 0
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional metadata filters for advanced filtering"
                        }
                    }
                }
            }
        ]
    
    def get_resources(self) -> List[Dict[str, Any]]:
        """
        Return the list of available MCP resources.
        
        Returns:
            List of resource definitions following MCP schema
        """
        return [
            {
                "uri": "powermem://memory",
                "name": "Memory Store",
                "description": "Access to the powermem memory store",
                "mimeType": "application/json"
            }
        ]
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the initialize request from MCP client.
        
        Args:
            params: Initialize parameters from client
            
        Returns:
            Server capabilities
        """
        self.initialize_memory()
        
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {}
            },
            "serverInfo": {
                "name": "powermem-mcp",
                "version": "0.1.0"
            }
        }
    
    def handle_tools_list(self) -> Dict[str, Any]:
        """
        Handle tools/list request.
        
        Returns:
            List of available tools
        """
        return {
            "tools": self.get_tools()
        }
    
    def handle_resources_list(self) -> Dict[str, Any]:
        """
        Handle resources/list request.
        
        Returns:
            List of available resources
        """
        return {
            "resources": self.get_resources()
        }
    
    def handle_resources_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle resources/read request.
        
        Args:
            params: Resource read parameters with 'uri'
            
        Returns:
            Resource content
        """
        uri = params.get("uri")
        
        if uri == "powermem://memory":
            self.initialize_memory()
            # Return summary of memory store
            try:
                stats = {
                    "total_memories": 0,
                    "description": "powermem memory store"
                }
                
                # Try to get some stats (if supported)
                try:
                    all_mems = self.memory.get_all(limit=1)
                    if isinstance(all_mems, dict) and "results" in all_mems:
                        # Get total count (this might require storage-specific implementation)
                        stats["total_memories"] = "Unknown (check with list_memories tool)"
                except Exception:
                    pass
                
                return {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": safe_json_dumps(stats, indent=2)
                        }
                    ]
                }
            except Exception as e:
                return {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": safe_json_dumps({
                                "error": str(e)
                            }, indent=2)
                        }
                    ],
                    "isError": True
                }
        else:
            return {
                "contents": [],
                "isError": True
            }
    
    def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tools/call request.
        
        Args:
            params: Tool call parameters with 'name' and 'arguments'
            
        Returns:
            Tool execution result
        """
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        self.initialize_memory()
        
        try:
            if tool_name == "add_memory":
                # Auto-provide user_id if not specified
                user_id = self.get_user_id_from_args(arguments)
                result = self.memory.add(
                    messages=arguments.get("messages"),
                    user_id=user_id,
                    agent_id=arguments.get("agent_id"),
                    run_id=arguments.get("run_id"),
                    metadata=arguments.get("metadata"),
                    filters=arguments.get("filters"),
                    scope=arguments.get("scope"),
                    memory_type=arguments.get("memory_type")
                )
                # Sanitize result to handle datetime objects
                sanitized_result = sanitize_for_json(result)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": safe_json_dumps({
                                "success": True,
                                "memory_id": sanitized_result.get("id") if isinstance(sanitized_result, dict) else result.get("id"),
                                "message": "Memory added successfully",
                                "data": sanitized_result
                            }, indent=2)
                        }
                    ]
                }
            
            elif tool_name == "search_memories":
                query = arguments.get("query")
                if not query:
                    raise ValueError("query parameter is required")
                
                # Auto-provide user_id if not specified
                user_id = self.get_user_id_from_args(arguments)
                result = self.memory.search(
                    query=query,
                    user_id=user_id,
                    agent_id=arguments.get("agent_id"),
                    run_id=arguments.get("run_id"),
                    filters=arguments.get("filters"),
                    limit=arguments.get("limit", 10),
                    threshold=arguments.get("threshold")
                )
                
                # Ensure all datetime objects and other non-serializable objects are serialized correctly
                # Deep sanitize multiple times to catch all nested datetime objects
                # First pass: sanitize the entire structure
                sanitized_result = sanitize_for_json(result)
                
                # Second pass: extract and deep sanitize results array
                sanitized_results = sanitized_result.get("results", [])
                sanitized_relations = sanitized_result.get("relations", [])
                
                # Deep sanitize each result item multiple times (defensive programming)
                final_results = []
                for item in sanitized_results:
                    # Multiple passes to ensure all nested datetime objects are caught
                    cleaned_item = sanitize_for_json(item)
                    cleaned_item = sanitize_for_json(cleaned_item)  # Second pass
                    # Final check for datetime objects
                    cleaned_item = sanitize_for_json(cleaned_item)  # Third pass
                    final_results.append(cleaned_item)
                
                final_relations = []
                if sanitized_relations:
                    for item in sanitized_relations:
                        cleaned_item = sanitize_for_json(item)
                        cleaned_item = sanitize_for_json(cleaned_item)  # Second pass
                        cleaned_item = sanitize_for_json(cleaned_item)  # Third pass
                        final_relations.append(cleaned_item)
                
                # Final structure to return
                response_data = {
                    "success": True,
                    "count": len(final_results),
                    "results": final_results,
                    "relations": final_relations
                }
                
                # Multiple final sanitization passes to ensure all datetime objects are converted
                final_response = sanitize_for_json(response_data)
                final_response = sanitize_for_json(final_response)  # Second pass
                final_response = sanitize_for_json(final_response)  # Third pass for safety
                
                # One more final check: manually walk through and convert any remaining datetime
                # Use a more robust approach with visited set to prevent infinite recursion
                def final_datetime_check(obj, path="", visited=None):
                    """Final check for any datetime objects that might have been missed"""
                    if visited is None:
                        visited = set()
                    
                    obj_id = id(obj)
                    if obj_id in visited:
                        return obj
                    visited.add(obj_id)
                    
                    try:
                        if isinstance(obj, (datetime, date)):
                            logger.warning(f"Found datetime object at path {path}: {obj}, converting to ISO")
                            return obj.isoformat()
                        elif isinstance(obj, dict):
                            return {k: final_datetime_check(v, f"{path}.{k}", visited) for k, v in obj.items()}
                        elif isinstance(obj, list):
                            return [final_datetime_check(item, f"{path}[{i}]", visited) for i, item in enumerate(obj)]
                        elif isinstance(obj, tuple):
                            return tuple(final_datetime_check(item, f"{path}[{i}]", visited) for i, item in enumerate(obj))
                        else:
                            # Check if it's a datetime-like object that might have been missed
                            if hasattr(obj, 'isoformat') and callable(getattr(obj, 'isoformat', None)):
                                try:
                                    return obj.isoformat()
                                except Exception:
                                    pass
                            return obj
                    finally:
                        visited.discard(obj_id)
                
                final_response = final_datetime_check(final_response)
                
                # Final sanitization pass before JSON serialization
                final_response = sanitize_for_json(final_response)
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": safe_json_dumps(final_response, indent=2)
                        }
                    ]
                }
            
            elif tool_name == "get_memory":
                memory_id = arguments.get("memory_id")
                if not memory_id:
                    raise ValueError("memory_id parameter is required")
                
                # Convert to int to ensure type compatibility
                try:
                    memory_id = int(memory_id)
                except (ValueError, TypeError):
                    raise ValueError(f"memory_id must be a valid integer, got: {memory_id}")
                
                # Auto-provide user_id if not specified
                user_id = self.get_user_id_from_args(arguments)
                result = self.memory.get(
                    memory_id=memory_id,
                    user_id=user_id,
                    agent_id=arguments.get("agent_id")
                )
                
                if result is None:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": safe_json_dumps({
                                    "success": False,
                                    "message": "Memory not found"
                                }, indent=2)
                            }
                        ],
                        "isError": True
                    }
                
                # Sanitize result to handle datetime objects
                sanitized_result = sanitize_for_json(result)
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": safe_json_dumps({
                                "success": True,
                                "data": sanitized_result
                            }, indent=2)
                        }
                    ]
                }
            
            elif tool_name == "update_memory":
                memory_id = arguments.get("memory_id")
                content = arguments.get("content")
                
                if not memory_id or not content:
                    raise ValueError("memory_id and content parameters are required")
                
                # Convert to int to ensure type compatibility
                try:
                    memory_id = int(memory_id)
                except (ValueError, TypeError):
                    raise ValueError(f"memory_id must be a valid integer, got: {memory_id}")
                
                # Auto-provide user_id if not specified
                user_id = self.get_user_id_from_args(arguments)
                result = self.memory.update(
                    memory_id=memory_id,
                    content=content,
                    user_id=user_id,
                    agent_id=arguments.get("agent_id"),
                    metadata=arguments.get("metadata")
                )
                
                # Sanitize result to handle datetime objects
                sanitized_result = sanitize_for_json(result)
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": safe_json_dumps({
                                "success": True,
                                "message": "Memory updated successfully",
                                "data": sanitized_result
                            }, indent=2)
                        }
                    ]
                }
            
            elif tool_name == "delete_memory":
                memory_id = arguments.get("memory_id")
                if not memory_id:
                    raise ValueError("memory_id parameter is required")
                
                # Convert to int to ensure type compatibility
                try:
                    memory_id = int(memory_id)
                except (ValueError, TypeError):
                    raise ValueError(f"memory_id must be a valid integer, got: {memory_id}")
                
                # Auto-provide user_id if not specified
                user_id = self.get_user_id_from_args(arguments)
                result = self.memory.delete(
                    memory_id=memory_id,
                    user_id=user_id,
                    agent_id=arguments.get("agent_id")
                )
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": safe_json_dumps({
                                "success": True,
                                "message": "Memory deleted successfully",
                                "deleted_id": memory_id
                            }, indent=2)
                        }
                    ]
                }
            
            elif tool_name == "delete_all_memories":
                # Auto-provide user_id if not specified
                user_id = self.get_user_id_from_args(arguments)
                self.memory.delete_all(
                    user_id=user_id,
                    agent_id=arguments.get("agent_id"),
                    run_id=arguments.get("run_id")
                )
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": safe_json_dumps({
                                "success": True,
                                "message": "All memories deleted successfully"
                            }, indent=2)
                        }
                    ]
                }
            
            elif tool_name == "list_memories":
                # Auto-provide user_id if not specified
                user_id = self.get_user_id_from_args(arguments)
                result = self.memory.get_all(
                    user_id=user_id,
                    agent_id=arguments.get("agent_id"),
                    run_id=arguments.get("run_id"),
                    limit=arguments.get("limit", 100),
                    offset=arguments.get("offset", 0),
                    filters=arguments.get("filters")
                )
                
                # Sanitize result to handle datetime objects
                sanitized_result = sanitize_for_json(result)
                
                # get_all returns a dict with 'results' key
                memories = sanitized_result.get("results", []) if isinstance(sanitized_result, dict) else sanitized_result
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": safe_json_dumps({
                                "success": True,
                                "count": len(memories),
                                "memories": memories
                            }, indent=2)
                        }
                    ]
                }
            
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}", exc_info=True)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": safe_json_dumps({
                            "success": False,
                            "error": str(e),
                            "error_type": type(e).__name__
                        }, indent=2)
                    }
                ],
                "isError": True
            }
    
    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process an incoming JSON-RPC request.
        
        Args:
            request: JSON-RPC request dictionary
            
        Returns:
            Response dictionary or None if no response needed
        """
        method = request.get("method")
        params = request.get("params", {})
        self.request_id = request.get("id")
        
        try:
            if method == "initialize":
                response = self.handle_initialize(params)
            elif method == "tools/list":
                response = self.handle_tools_list()
            elif method == "resources/list":
                response = self.handle_resources_list()
            elif method == "resources/read":
                response = self.handle_resources_read(params)
            elif method == "tools/call":
                response = self.handle_tools_call(params)
            elif method == "notifications/initialized":
                # No response needed for notifications
                return None
            else:
                response = {
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            # Build JSON-RPC response
            result = {
                "jsonrpc": "2.0",
                "id": self.request_id
            }
            
            if "error" in response:
                result["error"] = response["error"]
            else:
                result["result"] = response
            
            return result
        
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def run(self):
        """
        Run the MCP server, reading from stdin and writing to stdout.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            stream=sys.stderr  # Log to stderr so stdout is reserved for JSON-RPC
        )
        
        logger.info("Starting powermem MCP server...")
        
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = self.process_request(request)
                    
                    if response is not None:
                        print(safe_json_dumps(response))
                        sys.stdout.flush()
                
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(safe_json_dumps(error_response))
                    sys.stdout.flush()
        
        except KeyboardInterrupt:
            logger.info("Server shutting down...")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            sys.exit(1)


def main():
    """Entry point for the MCP server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="powermem MCP Server")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration JSON file"
    )
    parser.add_argument(
        "--env",
        type=str,
        help="Path to .env file for configuration"
    )
    
    args = parser.parse_args()
    
    config = None
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    elif args.env:
        from dotenv import load_dotenv
        load_dotenv(args.env)
    
    server = MCPServer(config=config)
    server.run()


if __name__ == "__main__":
    main()
