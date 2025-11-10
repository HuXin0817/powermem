"""
Abstract base class for agent privacy managers.

This module defines the interface for managing privacy and data protection
in the agent memory system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from powermem.agent.types import PrivacyLevel


class AgentPrivacyManagerBase(ABC):
    """
    Abstract base class for agent privacy managers.
    
    This class defines the interface for managing privacy and data protection
    in the agent memory system.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the privacy manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the privacy manager.
        """
        pass
    
    @abstractmethod
    def set_privacy_level(
        self,
        memory_id: str,
        privacy_level: PrivacyLevel,
        set_by: str
    ) -> Dict[str, Any]:
        """
        Set the privacy level for a memory.
        
        Args:
            memory_id: ID of the memory
            privacy_level: Privacy level to set
            set_by: ID of the agent/user setting the privacy level
            
        Returns:
            Dictionary containing the set result
        """
        pass
    
    @abstractmethod
    def get_privacy_level(
        self,
        memory_id: str
    ) -> PrivacyLevel:
        """
        Get the privacy level for a memory.
        
        Args:
            memory_id: ID of the memory
            
        Returns:
            PrivacyLevel enum value
        """
        pass
    
    @abstractmethod
    def encrypt_memory(
        self,
        memory_id: str,
        encryption_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Encrypt a memory.
        
        Args:
            memory_id: ID of the memory
            encryption_key: Optional encryption key
            
        Returns:
            Dictionary containing the encryption result
        """
        pass
    
    @abstractmethod
    def decrypt_memory(
        self,
        memory_id: str,
        decryption_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Decrypt a memory.
        
        Args:
            memory_id: ID of the memory
            decryption_key: Optional decryption key
            
        Returns:
            Dictionary containing the decryption result
        """
        pass
    
    @abstractmethod
    def anonymize_memory(
        self,
        memory_id: str,
        anonymization_rules: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Anonymize a memory.
        
        Args:
            memory_id: ID of the memory
            anonymization_rules: Optional anonymization rules
            
        Returns:
            Dictionary containing the anonymization result
        """
        pass
    
    @abstractmethod
    def log_access(
        self,
        memory_id: str,
        agent_id: str,
        access_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Log access to a memory.
        
        Args:
            memory_id: ID of the memory
            agent_id: ID of the agent/user accessing
            access_type: Type of access
            metadata: Optional metadata about the access
            
        Returns:
            Dictionary containing the log result
        """
        pass
    
    @abstractmethod
    def get_access_logs(
        self,
        memory_id: str,
        agent_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get access logs for a memory.
        
        Args:
            memory_id: ID of the memory
            agent_id: Optional ID of the agent/user
            limit: Optional limit on number of entries
            
        Returns:
            List of access log entries
        """
        pass
    
    @abstractmethod
    def apply_retention_policy(
        self,
        memory_id: str,
        retention_policy: str
    ) -> Dict[str, Any]:
        """
        Apply a retention policy to a memory.
        
        Args:
            memory_id: ID of the memory
            retention_policy: Retention policy to apply
            
        Returns:
            Dictionary containing the policy application result
        """
        pass
    
    @abstractmethod
    def check_gdpr_compliance(
        self,
        memory_id: str
    ) -> Dict[str, Any]:
        """
        Check GDPR compliance for a memory.
        
        Args:
            memory_id: ID of the memory
            
        Returns:
            Dictionary containing compliance check results
        """
        pass
    
    @abstractmethod
    def export_user_data(
        self,
        agent_id: str,
        export_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Export user data for GDPR compliance.
        
        Args:
            agent_id: ID of the agent/user
            export_format: Format for the export
            
        Returns:
            Dictionary containing the export result
        """
        pass
    
    @abstractmethod
    def delete_user_data(
        self,
        agent_id: str,
        confirmation_token: str
    ) -> Dict[str, Any]:
        """
        Delete user data for GDPR compliance.
        
        Args:
            agent_id: ID of the agent/user
            confirmation_token: Confirmation token for deletion
            
        Returns:
            Dictionary containing the deletion result
        """
        pass
    
    @abstractmethod
    def get_privacy_statistics(self) -> Dict[str, Any]:
        """
        Get privacy statistics.
        
        Returns:
            Dictionary containing privacy statistics
        """
        pass
    
    def is_initialized(self) -> bool:
        """
        Check if the privacy manager is initialized.
        
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
