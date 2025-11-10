"""
Abstract base class for agent collaboration managers.

This module defines the interface for managing collaboration and coordination
between agents in the memory system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from powermem.agent.types import CollaborationType, CollaborationStatus


class AgentCollaborationManagerBase(ABC):
    """
    Abstract base class for agent collaboration managers.
    
    This class defines the interface for managing collaboration and coordination
    between agents in the memory system.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the collaboration manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the collaboration manager.
        """
        pass
    
    @abstractmethod
    def initiate_collaboration(
        self,
        initiator_id: str,
        participant_ids: List[str],
        collaboration_type: CollaborationType,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Initiate a collaboration between agents.
        
        Args:
            initiator_id: ID of the agent initiating the collaboration
            participant_ids: List of agent IDs participating in the collaboration
            collaboration_type: Type of collaboration
            context: Optional context information
            
        Returns:
            Dictionary containing the collaboration initiation result
        """
        pass
    
    @abstractmethod
    def join_collaboration(
        self,
        collaboration_id: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        Join an existing collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            agent_id: ID of the agent joining
            
        Returns:
            Dictionary containing the join result
        """
        pass
    
    @abstractmethod
    def leave_collaboration(
        self,
        collaboration_id: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        Leave a collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            agent_id: ID of the agent leaving
            
        Returns:
            Dictionary containing the leave result
        """
        pass
    
    @abstractmethod
    def get_collaboration_status(
        self,
        collaboration_id: str
    ) -> CollaborationStatus:
        """
        Get the status of a collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            
        Returns:
            CollaborationStatus enum value
        """
        pass
    
    @abstractmethod
    def update_collaboration_status(
        self,
        collaboration_id: str,
        status: CollaborationStatus,
        updated_by: str
    ) -> Dict[str, Any]:
        """
        Update the status of a collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            status: New status
            updated_by: ID of the agent updating the status
            
        Returns:
            Dictionary containing the update result
        """
        pass
    
    @abstractmethod
    def get_collaboration_participants(
        self,
        collaboration_id: str
    ) -> List[str]:
        """
        Get list of participants in a collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            
        Returns:
            List of agent IDs participating in the collaboration
        """
        pass
    
    @abstractmethod
    def share_memory_in_collaboration(
        self,
        collaboration_id: str,
        memory_id: str,
        shared_by: str
    ) -> Dict[str, Any]:
        """
        Share a memory within a collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            memory_id: ID of the memory to share
            shared_by: ID of the agent sharing the memory
            
        Returns:
            Dictionary containing the share result
        """
        pass
    
    @abstractmethod
    def get_collaboration_memories(
        self,
        collaboration_id: str,
        agent_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get memories shared in a collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            agent_id: Optional ID of the agent requesting
            
        Returns:
            List of memory dictionaries
        """
        pass
    
    @abstractmethod
    def resolve_collaboration_conflict(
        self,
        collaboration_id: str,
        conflict_data: Dict[str, Any],
        resolver_id: str
    ) -> Dict[str, Any]:
        """
        Resolve a conflict in a collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            conflict_data: Data about the conflict
            resolver_id: ID of the agent resolving the conflict
            
        Returns:
            Dictionary containing the resolution result
        """
        pass
    
    @abstractmethod
    def get_collaboration_history(
        self,
        collaboration_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get history of a collaboration.
        
        Args:
            collaboration_id: ID of the collaboration
            limit: Optional limit on number of entries
            
        Returns:
            List of collaboration history entries
        """
        pass
    
    @abstractmethod
    def get_agent_collaborations(
        self,
        agent_id: str,
        status: Optional[CollaborationStatus] = None
    ) -> List[Dict[str, Any]]:
        """
        Get collaborations for an agent.
        
        Args:
            agent_id: ID of the agent
            status: Optional status filter
            
        Returns:
            List of collaboration dictionaries
        """
        pass
    
    def is_initialized(self) -> bool:
        """
        Check if the collaboration manager is initialized.
        
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
