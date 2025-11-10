"""
Abstract base classes for agent memory management system.

This module defines the core interfaces and abstract classes that all
agent memory managers must implement.
"""

from .manager import AgentMemoryManagerBase
from .context import AgentContextManagerBase
from .scope import AgentScopeManagerBase
from .permission import AgentPermissionManagerBase
from .collaboration import AgentCollaborationManagerBase
from .privacy import AgentPrivacyManagerBase

__all__ = [
    "AgentMemoryManagerBase",
    "AgentContextManagerBase", 
    "AgentScopeManagerBase",
    "AgentPermissionManagerBase",
    "AgentCollaborationManagerBase",
    "AgentPrivacyManagerBase"
]
