"""
Wrapper classes for agent memory management system.

This module provides wrapper classes that provide unified interfaces
and compatibility layers for the agent memory management system.
"""

from .agent_memory_wrapper import AgentMemoryWrapper
from .compatibility_wrapper import CompatibilityWrapper

__all__ = [
    "AgentMemoryWrapper",
    "CompatibilityWrapper"
]
