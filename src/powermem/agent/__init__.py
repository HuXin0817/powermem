"""
Agent Memory Management System

This module provides a unified architecture for managing memories across different
agent and user scenarios, including multi-agent collaboration, multi-user isolation,
and hybrid modes.

Key Components:
- MemoryFactory: Factory for creating different memory managers
- ManagerType: Enumeration of available manager types
- AgentMemoryManagerBase: Base class for all memory managers
"""

from .factories.memory_factory import MemoryFactory
from .abstract.manager import AgentMemoryManagerBase
from .implementations.multi_agent import MultiAgentMemoryManager
from .implementations.multi_user import MultiUserMemoryManager
from .implementations.hybrid import HybridMemoryManager
from .agent import AgentMemory

# Manager types for factory
class ManagerType:
    MULTI_AGENT = "multi_agent"
    MULTI_USER = "multi_user"
    HYBRID = "hybrid"

__all__ = [
    "MemoryFactory",
    "ManagerType", 
    "AgentMemoryManagerBase",
    "MultiAgentMemoryManager",
    "MultiUserMemoryManager", 
    "HybridMemoryManager",
    "AgentMemory"
]
