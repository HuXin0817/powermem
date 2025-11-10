"""
Component classes for agent memory management system.

This module provides concrete implementations of the agent memory management
components, migrated from the original multi_agent directory.
"""

from .scope_controller import ScopeController
from .permission_controller import PermissionController
from .collaboration_coordinator import CollaborationCoordinator
from .privacy_protector import PrivacyProtector

__all__ = [
    "ScopeController",
    "PermissionController", 
    "CollaborationCoordinator",
    "PrivacyProtector"
]
