"""
Abstract base class for agent memory managers.

This module defines the core interface that all agent memory managers must implement,
providing a unified API for memory operations across different scenarios.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from typing import Any, Dict


class AgentMemoryManagerBase(ABC):
    """
    Abstract base class for agent memory managers.
    
    This class defines the core interface that all agent memory managers must implement,
    providing a unified API for memory operations across different scenarios.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the agent memory manager.
        
        Args:
            config: Memory configuration object
        """
        self.config = config
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the memory manager.
        
        This method should be called after instantiation to set up
        any required resources or connections.
        """
        pass
    
    @abstractmethod
    def process_memory(
        self,
        content: str,
        agent_id: str,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process and store a new memory.
        
        Args:
            content: The memory content to store
            agent_id: ID of the agent/user creating the memory
            context: Additional context information
            metadata: Additional metadata for the memory
            
        Returns:
            Dictionary containing the processed memory information
        """
        pass
    
    @abstractmethod
    def get_memories(
        self,
        agent_id: str,
        query: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve memories for a specific agent/user.
        
        Args:
            agent_id: ID of the agent/user
            query: Optional query string for filtering
            filters: Optional additional filters
            
        Returns:
            List of memory dictionaries
        """
        pass
    
    @abstractmethod
    def update_memory(
        self,
        memory_id: str,
        agent_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing memory.
        
        Args:
            memory_id: ID of the memory to update
            agent_id: ID of the agent/user making the update
            updates: Dictionary of updates to apply
            
        Returns:
            Dictionary containing the updated memory information
        """
        pass
    
    @abstractmethod
    def delete_memory(
        self,
        memory_id: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        Delete a memory.
        
        Args:
            memory_id: ID of the memory to delete
            agent_id: ID of the agent/user making the deletion
            
        Returns:
            Dictionary containing the deletion result
        """
        pass
    
    @abstractmethod
    def share_memory(
        self,
        memory_id: str,
        from_agent: str,
        to_agents: List[str],
        permissions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Share a memory with other agents/users.
        
        Args:
            memory_id: ID of the memory to share
            from_agent: ID of the agent/user sharing the memory
            to_agents: List of agent/user IDs to share with
            permissions: Optional list of permissions to grant
            
        Returns:
            Dictionary containing the sharing result
        """
        pass
    
    @abstractmethod
    def get_context_info(self, agent_id: str) -> Dict[str, Any]:
        """
        Get context information for an agent/user.
        
        Args:
            agent_id: ID of the agent/user
            
        Returns:
            Dictionary containing context information
        """
        pass
    
    @abstractmethod
    def update_memory_decay(self) -> Dict[str, Any]:
        """
        Update memory decay based on Ebbinghaus forgetting curve.
        
        Returns:
            Dictionary containing the decay update results
        """
        pass
    
    @abstractmethod
    def cleanup_forgotten_memories(self) -> Dict[str, Any]:
        """
        Clean up memories that have been forgotten.
        
        Returns:
            Dictionary containing the cleanup results
        """
        pass
    
    @abstractmethod
    def get_memory_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the memory system.
        
        Returns:
            Dictionary containing memory statistics
        """
        pass
    
    @abstractmethod
    def check_permission(
        self,
        agent_id: str,
        memory_id: str,
        permission: str
    ) -> bool:
        """
        Check if an agent/user has a specific permission for a memory.
        
        Args:
            agent_id: ID of the agent/user
            memory_id: ID of the memory
            permission: Permission to check
            
        Returns:
            True if the agent/user has the permission, False otherwise
        """
        pass
    
    def get_manager_type(self) -> str:
        """
        Get the type of this memory manager.
        
        Returns:
            String representing the manager type
        """
        return self.__class__.__name__
    
    def is_initialized(self) -> bool:
        """
        Check if the memory manager is initialized.
        
        Returns:
            True if initialized, False otherwise
        """
        return self.initialized
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the configuration object.
        
        Returns:
            Memory configuration object
        """
        return self.config
