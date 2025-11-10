"""
Prompt templates for memory operations

This module provides prompt templates for different memory operations.
"""

import logging
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class PromptTemplates:
    """
    Base class for prompt templates.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize prompt templates.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load prompt templates."""
        # Base templates
        self.templates = {
            "system": {
                "memory_assistant": """You are a memory assistant that helps users manage and retrieve information. 
                Your role is to:
                1. Extract important facts from user input
                2. Store memories in an organized way
                3. Retrieve relevant memories when needed
                4. Provide context-aware responses
                
                Always be helpful, accurate, and respectful of user privacy.""",
                
                "fact_extractor": """You are a fact extraction specialist. Your task is to identify and extract 
                important facts, preferences, and information from user input. Focus on:
                - Personal preferences and opinions
                - Important facts and data
                - Relationships and connections
                - Goals and intentions
                - Contextual information
                
                Extract only factual, verifiable information.""",
                
                "memory_processor": """You are a memory processing specialist. Your task is to:
                1. Analyze and categorize memories
                2. Determine importance and relevance
                3. Suggest memory organization strategies
                4. Identify patterns and connections
                
                Always prioritize user privacy and data security."""
            },
            
            "user": {
                "extract_facts": """Extract important facts and information from the following text:
                
                Text: {text}
                
                Please identify:
                1. Key facts and information
                2. Personal preferences or opinions
                3. Important relationships or connections
                4. Goals or intentions
                5. Contextual information
                
                Return the extracted information in a structured format.""",
                
                "process_memory": """Process the following memory for storage:
                
                Memory: {memory}
                Context: {context}
                
                Please:
                1. Determine the importance level (low, medium, high)
                2. Suggest appropriate categorization
                3. Identify key topics or themes
                4. Recommend storage duration
                
                Return your analysis in a structured format.""",
                
                "search_memories": """Search for memories related to the following query:
                
                Query: {query}
                Context: {context}
                
                Please:
                1. Identify relevant memory categories
                2. Suggest search strategies
                3. Recommend filtering criteria
                4. Provide search optimization tips
                
                Return your recommendations in a structured format."""
            }
        }
    
    def get_template(self, category: str, template_name: str) -> str:
        """
        Get a specific template.
        
        Args:
            category: Template category (system, user, etc.)
            template_name: Name of the template
            
        Returns:
            Template string
        """
        return self.templates.get(category, {}).get(template_name, "")
    
    def format_template(self, category: str, template_name: str, **kwargs) -> str:
        """
        Format a template with provided variables.
        
        Args:
            category: Template category
            template_name: Name of the template
            **kwargs: Variables to format the template
            
        Returns:
            Formatted template string
        """
        template = self.get_template(category, template_name)
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing template variable: {e}")
            return template
    
    def add_template(self, category: str, template_name: str, template: str) -> None:
        """
        Add a new template.
        
        Args:
            category: Template category
            template_name: Name of the template
            template: Template string
        """
        if category not in self.templates:
            self.templates[category] = {}
        
        self.templates[category][template_name] = template
    
    def get_all_templates(self) -> Dict[str, Dict[str, str]]:
        """
        Get all templates.
        
        Returns:
            Dictionary of all templates
        """
        return self.templates
    
    def export_templates(self, file_path: str) -> None:
        """
        Export templates to a file.
        
        Args:
            file_path: Path to export file
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
            logger.info(f"Templates exported to {file_path}")
        except Exception as e:
            logger.error(f"Failed to export templates: {e}")
    
    def import_templates(self, file_path: str) -> None:
        """
        Import templates from a file.
        
        Args:
            file_path: Path to import file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_templates = json.load(f)
            
            # Merge with existing templates
            for category, templates in imported_templates.items():
                if category not in self.templates:
                    self.templates[category] = {}
                self.templates[category].update(templates)
            
            logger.info(f"Templates imported from {file_path}")
        except Exception as e:
            logger.error(f"Failed to import templates: {e}")
