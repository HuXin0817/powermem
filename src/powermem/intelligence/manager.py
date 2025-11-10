"""
Intelligence manager

This module provides the main intelligence management interface.
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from .intelligent_memory_manager import IntelligentMemoryManager

logger = logging.getLogger(__name__)


class IntelligenceManager:
    """
    Main intelligence manager for memory processing.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize intelligence manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        # Check if intelligent memory is enabled
        intelligent_config = self.config.get("intelligent_memory", {})
        self.enabled = intelligent_config.get("enabled", False)  # Default to False for backward compatibility
        
        if self.enabled:
            self.intelligent_memory_manager = IntelligentMemoryManager(self.config)
        else:
            self.intelligent_memory_manager = None
            
        logger.info(f"IntelligenceManager initialized (enabled: {self.enabled})")
    
    def process_metadata(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process metadata with intelligence.
        
        Args:
            content: Content to analyze
            metadata: Additional metadata
            context: Additional context
            
        Returns:
            Enhanced metadata with intelligence analysis
        """
        if not self.enabled or not self.intelligent_memory_manager:
            return metadata or {}
            
        return self.intelligent_memory_manager.process_metadata(content, metadata, context)
    
    async def process_metadata_async(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process metadata with intelligence asynchronously.
        
        Args:
            content: Content to analyze
            metadata: Additional metadata
            context: Additional context
            
        Returns:
            Enhanced metadata with intelligence analysis
        """
        if not self.enabled or not self.intelligent_memory_manager:
            return metadata or {}
            
        return await self.intelligent_memory_manager.process_metadata_async(content, metadata, context)
    
    def process_search_results(
        self,
        results: List[Dict[str, Any]],
        query: str
    ) -> List[Dict[str, Any]]:
        """
        Process search results with intelligence.
        
        Args:
            results: Search results
            query: Original query
            
        Returns:
            Processed and ranked results
        """
        if not self.enabled or not self.intelligent_memory_manager:
            # Return original results if intelligence is disabled
            return results
            
        return self.intelligent_memory_manager.process_search_results(results, query)
    
    async def process_search_results_async(
        self,
        results: List[Dict[str, Any]],
        query: str
    ) -> List[Dict[str, Any]]:
        """
        Process search results with intelligence asynchronously.
        
        Args:
            results: Search results
            query: Original query
            
        Returns:
            Processed and ranked results
        """
        if not self.enabled or not self.intelligent_memory_manager:
            # Return original results if intelligence is disabled
            return results
            
        return await self.intelligent_memory_manager.process_search_results_async(results, query)
    
    def optimize_memories(self) -> Dict[str, Any]:
        """
        Optimize memory storage.
        
        Returns:
            Optimization results
        """
        if not self.enabled or not self.intelligent_memory_manager:
            return {"optimized": False, "reason": "intelligence disabled"}
            
        return self.intelligent_memory_manager.optimize_memories()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Memory statistics
        """
        if not self.enabled or not self.intelligent_memory_manager:
            return {"stats": "intelligence disabled"}
            
        return self.intelligent_memory_manager.get_memory_stats()
