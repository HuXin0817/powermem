"""
Abstract base class for agent scope managers.

This module defines the interface for managing memory scopes and access control
in the agent memory system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from powermem.agent.types import MemoryScope


class AgentScopeManagerBase(ABC):
    """
    Abstract base class for agent scope managers.
    
    This class defines the interface for managing memory scopes and access control
    in the agent memory system.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the scope manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the scope manager.
        """
        pass
    
    @abstractmethod
    def determine_scope(
        self,
        agent_id: str,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryScope:
        """
        Determine the appropriate scope for a memory.
        
        Args:
            agent_id: ID of the agent/user creating the memory
            context: Optional context information
            metadata: Optional metadata information
            
        Returns:
            MemoryScope enum value
        """
        pass
    
    @abstractmethod
    def get_accessible_memories(
        self,
        agent_id: str,
        scope: Optional[MemoryScope] = None
    ) -> List[str]:
        """
        Get list of memory IDs accessible to an agent/user.
        
        Args:
            agent_id: ID of the agent/user
            scope: Optional scope filter
            
        Returns:
            List of accessible memory IDs
        """
        pass
    
    @abstractmethod
    def check_scope_access(
        self,
        agent_id: str,
        memory_id: str
    ) -> bool:
        """
        Check if an agent/user has access to a memory based on scope.
        
        Args:
            agent_id: ID of the agent/user
            memory_id: ID of the memory
            
        Returns:
            True if access is allowed, False otherwise
        """
        pass
    
    @abstractmethod
    def update_memory_scope(
        self,
        memory_id: str,
        new_scope: MemoryScope,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        Update the scope of a memory.
        
        Args:
            memory_id: ID of the memory
            new_scope: New scope for the memory
            agent_id: ID of the agent/user making the change
            
        Returns:
            Dictionary containing the update result
        """
        pass
    
    @abstractmethod
    def get_scope_members(
        self,
        scope: MemoryScope,
        memory_id: Optional[str] = None
    ) -> List[str]:
        """
        Get list of agents/users with access to a scope.
        
        Args:
            scope: Memory scope
            memory_id: Optional specific memory ID
            
        Returns:
            List of agent/user IDs with access
        """
        pass
    
    @abstractmethod
    def add_scope_member(
        self,
        scope: MemoryScope,
        agent_id: str,
        memory_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add an agent/user to a scope.
        
        Args:
            scope: Memory scope
            agent_id: ID of the agent/user to add
            memory_id: Optional specific memory ID
            
        Returns:
            Dictionary containing the add result
        """
        pass
    
    @abstractmethod
    def remove_scope_member(
        self,
        scope: MemoryScope,
        agent_id: str,
        memory_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Remove an agent/user from a scope.
        
        Args:
            scope: Memory scope
            agent_id: ID of the agent/user to remove
            memory_id: Optional specific memory ID
            
        Returns:
            Dictionary containing the removal result
        """
        pass
    
    @abstractmethod
    def get_scope_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about scope usage.
        
        Returns:
            Dictionary containing scope statistics
        """
        pass
    
    def is_initialized(self) -> bool:
        """
        Check if the scope manager is initialized.
        
        Returns:
            True if initialized, False otherwise
        """
        return self.initialized
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the configuration object.
        
        Returns:
            Configuration dictionary
        """
        return self.config
