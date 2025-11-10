"""
Abstract base class for agent permission managers.

This module defines the interface for managing permissions and access control
in the agent memory system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from powermem.agent.types import AccessPermission


class AgentPermissionManagerBase(ABC):
    """
    Abstract base class for agent permission managers.
    
    This class defines the interface for managing permissions and access control
    in the agent memory system.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the permission manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the permission manager.
        """
        pass
    
    @abstractmethod
    def check_permission(
        self,
        agent_id: str,
        memory_id: str,
        permission: AccessPermission
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
    
    @abstractmethod
    def grant_permission(
        self,
        memory_id: str,
        agent_id: str,
        permission: AccessPermission,
        granted_by: str
    ) -> Dict[str, Any]:
        """
        Grant a permission to an agent/user for a memory.
        
        Args:
            memory_id: ID of the memory
            agent_id: ID of the agent/user to grant permission to
            permission: Permission to grant
            granted_by: ID of the agent/user granting the permission
            
        Returns:
            Dictionary containing the grant result
        """
        pass
    
    @abstractmethod
    def revoke_permission(
        self,
        memory_id: str,
        agent_id: str,
        permission: AccessPermission,
        revoked_by: str
    ) -> Dict[str, Any]:
        """
        Revoke a permission from an agent/user for a memory.
        
        Args:
            memory_id: ID of the memory
            agent_id: ID of the agent/user to revoke permission from
            permission: Permission to revoke
            revoked_by: ID of the agent/user revoking the permission
            
        Returns:
            Dictionary containing the revoke result
        """
        pass
    
    @abstractmethod
    def get_permissions(
        self,
        memory_id: str,
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get permissions for a memory or agent/user.
        
        Args:
            memory_id: ID of the memory
            agent_id: Optional ID of the agent/user
            
        Returns:
            Dictionary containing permission information
        """
        pass
    
    @abstractmethod
    def set_default_permissions(
        self,
        memory_id: str,
        permissions: Dict[str, List[AccessPermission]],
        set_by: str
    ) -> Dict[str, Any]:
        """
        Set default permissions for a memory.
        
        Args:
            memory_id: ID of the memory
            permissions: Dictionary of default permissions
            set_by: ID of the agent/user setting the permissions
            
        Returns:
            Dictionary containing the set result
        """
        pass
    
    @abstractmethod
    def inherit_permissions(
        self,
        target_memory_id: str,
        source_memory_id: str,
        inherited_by: str
    ) -> Dict[str, Any]:
        """
        Inherit permissions from another memory.
        
        Args:
            target_memory_id: ID of the target memory
            source_memory_id: ID of the source memory
            inherited_by: ID of the agent/user inheriting the permissions
            
        Returns:
            Dictionary containing the inherit result
        """
        pass
    
    @abstractmethod
    def get_permission_history(
        self,
        memory_id: str,
        agent_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get permission history for a memory or agent/user.
        
        Args:
            memory_id: ID of the memory
            agent_id: Optional ID of the agent/user
            limit: Optional limit on number of entries
            
        Returns:
            List of permission history entries
        """
        pass
    
    @abstractmethod
    def validate_permission_chain(
        self,
        agent_id: str,
        memory_id: str,
        permission: AccessPermission
    ) -> Dict[str, Any]:
        """
        Validate the permission chain for an agent/user and memory.
        
        Args:
            agent_id: ID of the agent/user
            memory_id: ID of the memory
            permission: Permission to validate
            
        Returns:
            Dictionary containing validation results
        """
        pass
    
    def is_initialized(self) -> bool:
        """
        Check if the permission manager is initialized.
        
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
