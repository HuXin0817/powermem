"""
Abstract base class for agent context managers.

This module defines the interface for managing agent/user context information
in the memory system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AgentContextManagerBase(ABC):
    """
    Abstract base class for agent context managers.
    
    This class defines the interface for managing context information
    for agents and users in the memory system.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the context manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the context manager.
        """
        pass
    
    @abstractmethod
    def get_context(
        self,
        agent_id: str,
        context_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get context information for an agent/user.
        
        Args:
            agent_id: ID of the agent/user
            context_type: Optional context type filter
            
        Returns:
            Dictionary containing context information
        """
        pass
    
    @abstractmethod
    def update_context(
        self,
        agent_id: str,
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update context information for an agent/user.
        
        Args:
            agent_id: ID of the agent/user
            context_data: Context data to update
            
        Returns:
            Dictionary containing the update result
        """
        pass
    
    @abstractmethod
    def add_context_entry(
        self,
        agent_id: str,
        context_type: str,
        context_value: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a new context entry for an agent/user.
        
        Args:
            agent_id: ID of the agent/user
            context_type: Type of context entry
            context_value: Value of the context entry
            metadata: Optional metadata for the context entry
            
        Returns:
            Dictionary containing the add result
        """
        pass
    
    @abstractmethod
    def remove_context_entry(
        self,
        agent_id: str,
        context_type: str,
        context_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Remove a context entry for an agent/user.
        
        Args:
            agent_id: ID of the agent/user
            context_type: Type of context entry to remove
            context_id: Optional specific context entry ID
            
        Returns:
            Dictionary containing the removal result
        """
        pass
    
    @abstractmethod
    def get_shared_context(
        self,
        agent_ids: List[str],
        context_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get shared context information for multiple agents/users.
        
        Args:
            agent_ids: List of agent/user IDs
            context_type: Optional context type filter
            
        Returns:
            Dictionary containing shared context information
        """
        pass
    
    @abstractmethod
    def clear_context(
        self,
        agent_id: str,
        context_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Clear context information for an agent/user.
        
        Args:
            agent_id: ID of the agent/user
            context_type: Optional context type to clear
            
        Returns:
            Dictionary containing the clear result
        """
        pass
    
    @abstractmethod
    def get_context_history(
        self,
        agent_id: str,
        context_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get context history for an agent/user.
        
        Args:
            agent_id: ID of the agent/user
            context_type: Optional context type filter
            limit: Optional limit on number of entries
            
        Returns:
            List of context history entries
        """
        pass
    
    def is_initialized(self) -> bool:
        """
        Check if the context manager is initialized.
        
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
