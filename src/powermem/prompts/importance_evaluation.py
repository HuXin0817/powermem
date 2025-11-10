"""
Importance evaluation prompts

This module provides prompts for importance evaluation operations.
"""

import logging
from typing import Dict, Any, Optional
from .templates import PromptTemplates

logger = logging.getLogger(__name__)


class ImportanceEvaluationPrompts(PromptTemplates):
    """
    Prompts for importance evaluation operations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize importance evaluation prompts.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self._load_importance_evaluation_templates()
    
    def _load_importance_evaluation_templates(self) -> None:
        """Load importance evaluation specific templates."""
        # Check for custom prompt in config
        custom_prompt = self.config.get("custom_importance_evaluation_prompt")
        
        # Use custom prompt if provided, otherwise use default
        if custom_prompt:
            default_system_prompt = custom_prompt
            logger.info("Using custom importance evaluation prompt from config")
        else:
            default_system_prompt = """You are an AI assistant that evaluates the importance of memory content on a scale from 0.0 to 1.0.

Your task is to analyze memory content and assess its importance based on multiple criteria:
- Relevance: How relevant is this information to the user's needs and interests?
- Novelty: How new or unique is this information?
- Emotional Impact: How emotionally significant is this content?
- Actionability: How actionable or useful is this information?
- Factual Value: How factual and reliable is this information?
- Personal Significance: How personally important is this to the user?

Always provide detailed reasoning for your evaluation and return results in structured JSON format."""
        
        importance_templates = {
            "system": {
                "importance_evaluator": default_system_prompt
            },
            
            "user": {
                "evaluate_importance": """You are an AI assistant that evaluates the importance of memory content on a scale from 0.0 to 1.0.

Content to evaluate: "{content}"

{metadata_section}
{context_section}
Please evaluate the importance of this content based on the following criteria:
- Relevance: How relevant is this information to the user's needs and interests?
- Novelty: How new or unique is this information?
- Emotional Impact: How emotionally significant is this content?
- Actionability: How actionable or useful is this information?
- Factual Value: How factual and reliable is this information?
- Personal Significance: How personally important is this to the user?

Respond with a JSON object containing:
{{
    "importance_score": <float between 0.0 and 1.0>,
    "reasoning": "<brief explanation of the score>",
    "criteria_scores": {{
        "relevance": <float>,
        "novelty": <float>,
        "emotional_impact": <float>,
        "actionable": <float>,
        "factual": <float>,
        "personal": <float>
    }}
}}""",
                
                "evaluate_importance_with_metadata": """Metadata: {metadata}

""",
                
                "evaluate_importance_with_context": """Context: {context}

""",
                
                "detailed_importance_breakdown": """Provide a detailed breakdown of importance evaluation for the following content:

Content: "{content}"

{metadata_section}
{context_section}

For each criterion, provide:
1. A score from 0.0 to 1.0
2. Brief reasoning for the score
3. Key factors that influenced the evaluation

Criteria to evaluate:
- Relevance: How relevant is this information to the user's needs and interests?
- Novelty: How new or unique is this information?
- Emotional Impact: How emotionally significant is this content?
- Actionability: How actionable or useful is this information?
- Factual Value: How factual and reliable is this information?
- Personal Significance: How personally important is this to the user?

Respond with a JSON object containing:
{{
    "overall_score": <float between 0.0 and 1.0>,
    "reasoning": "<overall explanation>",
    "criteria_scores": {{
        "relevance": {{
            "score": <float>,
            "reasoning": "<explanation>"
        }},
        "novelty": {{
            "score": <float>,
            "reasoning": "<explanation>"
        }},
        "emotional_impact": {{
            "score": <float>,
            "reasoning": "<explanation>"
        }},
        "actionable": {{
            "score": <float>,
            "reasoning": "<explanation>"
        }},
        "factual": {{
            "score": <float>,
            "reasoning": "<explanation>"
        }},
        "personal": {{
            "score": <float>,
            "reasoning": "<explanation>"
        }}
    }}
}}"""
            }
        }
        
        # Add importance evaluation templates to existing templates
        for category, templates in importance_templates.items():
            if category not in self.templates:
                self.templates[category] = {}
            self.templates[category].update(templates)
    
    def get_importance_evaluation_prompt(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get importance evaluation prompt.
        
        Args:
            content: Content to evaluate
            metadata: Additional metadata
            context: Additional context
            
        Returns:
            Formatted prompt
        """
        # Build metadata section if provided
        metadata_section = ""
        if metadata:
            metadata_section = self.format_template(
                "user", 
                "evaluate_importance_with_metadata", 
                metadata=metadata
            )
        
        # Build context section if provided
        context_section = ""
        if context:
            context_section = self.format_template(
                "user", 
                "evaluate_importance_with_context", 
                context=context
            )
        
        return self.format_template(
            "user", 
            "evaluate_importance", 
            content=content,
            metadata_section=metadata_section,
            context_section=context_section
        )
    
    def get_detailed_importance_breakdown_prompt(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get detailed importance breakdown prompt.
        
        Args:
            content: Content to evaluate
            metadata: Additional metadata
            context: Additional context
            
        Returns:
            Formatted prompt
        """
        # Build metadata section if provided
        metadata_section = ""
        if metadata:
            metadata_section = self.format_template(
                "user", 
                "evaluate_importance_with_metadata", 
                metadata=metadata
            )
        
        # Build context section if provided
        context_section = ""
        if context:
            context_section = self.format_template(
                "user", 
                "evaluate_importance_with_context", 
                context=context
            )
        
        return self.format_template(
            "user", 
            "detailed_importance_breakdown", 
            content=content,
            metadata_section=metadata_section,
            context_section=context_section
        )
    
    def get_system_prompt(self) -> str:
        """
        Get system prompt for importance evaluation.
        
        Returns:
            System prompt
        """
        return self.get_template("system", "importance_evaluator")
