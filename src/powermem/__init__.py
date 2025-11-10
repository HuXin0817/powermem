"""
powermem - Intelligent Memory System

An AI-powered intelligent memory management system that provides a persistent memory layer for LLM applications.
"""

import importlib.metadata
from typing import Any

__version__ = importlib.metadata.version("powermem")

# Import core classes
from .core.memory import Memory, _auto_convert_config
from .core.async_memory import AsyncMemory
from .core.base import MemoryBase

# Import configuration loader
from .config_loader import load_config_from_env, create_config, validate_config, auto_config


def create_memory(
    config: Any = None,
    **kwargs
):
    """
    Create a Memory instance with automatic configuration loading.
    
    This is the simplest way to create a Memory instance. It automatically:
    1. Loads configuration from .env file if no config is provided
    2. Falls back to defaults if .env is not available
    3. Uses mock providers if API keys are not provided
    
    Args:
        config: Optional configuration dictionary. If None, loads from .env
        **kwargs: Additional parameters to pass to Memory
    
    Returns:
        Memory instance
        
    Example:
        ```python
        from powermem import create_memory
        
        # Simplest usage - auto loads from .env
        # No API keys needed - will use mock providers
        memory = create_memory()
        
        # With custom config
        memory = create_memory(config=my_config)
        
        # With parameters
        memory = create_memory(agent_id="my_agent")
        ```
    """
    if config is None:
        config = auto_config()
    
    return Memory(config=config, **kwargs)


def from_config(config: Any = None, **kwargs):
    """
    Create Memory instance from configuration
    
    Args:
        config: Configuration dictionary
        **kwargs: Additional parameters
    
    Returns:
        Memory instance
        
    Example:
        ```python
        from powermem import from_config
        
        memory = from_config({
            "llm": {"provider": "openai", "config": {"api_key": "..."}},
            "embedder": {"provider": "openai", "config": {"api_key": "..."}},
            "vector_store": {"provider": "chroma", "config": {...}},
        })
        
        # Or auto-load from .env
        memory = from_config()
        ```
    """
    from .core.setup import from_config as _from_config
    return _from_config(config=config, **kwargs)


Memory.from_config = classmethod(lambda cls, config=None, **kwargs: create_memory(config, **kwargs))


__all__ = [
    "Memory",
    "AsyncMemory", 
    "MemoryBase",
    "load_config_from_env",
    "create_config",
    "validate_config",
    "create_memory",
    "from_config",
    "auto_config",
]
