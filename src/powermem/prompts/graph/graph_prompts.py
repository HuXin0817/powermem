"""
Graph prompts for memory operations

This module provides prompts for graph-based memory operations.
"""

import logging
from typing import Dict, Any, Optional
from ..templates import PromptTemplates

logger = logging.getLogger(__name__)

# Graph prompts constants
UPDATE_GRAPH_PROMPT = """
You are an AI expert specializing in graph memory management and optimization. Your task is to analyze existing graph memories alongside new information, and update the relationships in the memory list to ensure the most accurate, current, and coherent representation of knowledge.

Input:
1. Existing Graph Memories: A list of current graph memories, each containing source, target, and relationship information.
2. New Graph Memory: Fresh information to be integrated into the existing graph structure.

Guidelines:
1. Identification: Use the source and target as primary identifiers when matching existing memories with new information.
2. Conflict Resolution:
   - If new information contradicts an existing memory:
     a) For matching source and target but differing content, update the relationship of the existing memory.
     b) If the new memory provides more recent or accurate information, update the existing memory accordingly.
3. Comprehensive Review: Thoroughly examine each existing graph memory against the new information, updating relationships as necessary. Multiple updates may be required.
4. Consistency: Maintain a uniform and clear style across all memories. Each entry should be concise yet comprehensive.
5. Semantic Coherence: Ensure that updates maintain or improve the overall semantic structure of the graph.
6. Temporal Awareness: If timestamps are available, consider the recency of information when making updates.
7. Relationship Refinement: Look for opportunities to refine relationship descriptions for greater precision or clarity.
8. Redundancy Elimination: Identify and merge any redundant or highly similar relationships that may result from the update.

Memory Format:
source -- RELATIONSHIP -- destination

Task Details:
======= Existing Graph Memories:=======
{existing_memories}

======= New Graph Memory:=======
{new_memories}

Output:
Provide a list of update instructions, each specifying the source, target, and the new relationship to be set. Only include memories that require updates.
"""

EXTRACT_RELATIONS_PROMPT = """

You are an advanced algorithm designed to extract structured information from text to construct knowledge graphs. Your goal is to capture comprehensive and accurate information. Follow these key principles:

1. Extract only explicitly stated information from the text.
2. Establish relationships among the entities provided.
3. Use "USER_ID" as the source entity for any self-references (e.g., "I," "me," "my," etc.) in user messages.
CUSTOM_PROMPT

Relationships:
    - Use consistent, general, and timeless relationship types.
    - Example: Prefer "professor" over "became_professor."
    - Relationships should only be established among the entities explicitly mentioned in the user message.

Entity Consistency:
    - Ensure that relationships are coherent and logically align with the context of the message.
    - Maintain consistent naming for entities across the extracted data.

Strive to construct a coherent and easily understandable knowledge graph by eshtablishing all the relationships among the entities and adherence to the user's context.

Adhere strictly to these guidelines to ensure high-quality knowledge graph extraction."""

DELETE_RELATIONS_SYSTEM_PROMPT = """
You are a graph memory manager specializing in identifying, managing, and optimizing relationships within graph-based memories. Your primary task is to analyze a list of existing relationships and determine which ones should be deleted based on the new information provided.
Input:
1. Existing Graph Memories: A list of current graph memories, each containing source, relationship, and destination information.
2. New Text: The new information to be integrated into the existing graph structure.
3. Use "USER_ID" as node for any self-references (e.g., "I," "me," "my," etc.) in user messages.

Guidelines:
1. Identification: Use the new information to evaluate existing relationships in the memory graph.
2. Deletion Criteria: Delete a relationship only if it meets at least one of these conditions:
   - Outdated or Inaccurate: The new information is more recent or accurate.
   - Contradictory: The new information conflicts with or negates the existing information.
3. DO NOT DELETE if their is a possibility of same type of relationship but different destination nodes.
4. Comprehensive Analysis:
   - Thoroughly examine each existing relationship against the new information and delete as necessary.
   - Multiple deletions may be required based on the new information.
5. Semantic Integrity:
   - Ensure that deletions maintain or improve the overall semantic structure of the graph.
   - Avoid deleting relationships that are NOT contradictory/outdated to the new information.
6. Temporal Awareness: Prioritize recency when timestamps are available.
7. Necessity Principle: Only DELETE relationships that must be deleted and are contradictory/outdated to the new information to maintain an accurate and coherent memory graph.

Note: DO NOT DELETE if their is a possibility of same type of relationship but different destination nodes. 

For example: 
Existing Memory: alice -- loves_to_eat -- pizza
New Information: Alice also loves to eat burger.

Do not delete in the above example because there is a possibility that Alice loves to eat both pizza and burger.

Memory Format:
source -- relationship -- destination

Provide a list of deletion instructions, each specifying the relationship to be deleted.
"""

class GraphPrompts(PromptTemplates):
    """
    Prompts for graph-based memory operations.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize graph prompts.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        # Store custom prompts from config if provided
        self._custom_update_graph_prompt = None
        self._custom_extract_relations_prompt = None
        self._custom_delete_relations_prompt = None
        
        if config:
            # Support both graph_store config structure and direct config
            graph_store_config = config.get("graph_store", {})
            if isinstance(graph_store_config, dict):
                self._custom_update_graph_prompt = graph_store_config.get("custom_update_graph_prompt")
                self._custom_extract_relations_prompt = graph_store_config.get("custom_extract_relations_prompt") or graph_store_config.get("custom_prompt")
                self._custom_delete_relations_prompt = graph_store_config.get("custom_delete_relations_prompt")
            # Also support direct config keys
            if not self._custom_update_graph_prompt:
                self._custom_update_graph_prompt = config.get("custom_update_graph_prompt")
            if not self._custom_extract_relations_prompt:
                self._custom_extract_relations_prompt = config.get("custom_extract_relations_prompt") or config.get("custom_prompt")
            if not self._custom_delete_relations_prompt:
                self._custom_delete_relations_prompt = config.get("custom_delete_relations_prompt")
    
    def get_update_graph_prompt(self, existing_memories: str, new_memories: str) -> str:
        """
        Get graph update prompt.
        
        Args:
            existing_memories: Existing graph memories
            new_memories: New graph memories to integrate
            
        Returns:
            Formatted prompt
        """
        # Use custom prompt if provided, otherwise use default
        prompt_template = self._custom_update_graph_prompt or UPDATE_GRAPH_PROMPT
        try:
            return prompt_template.format(
                existing_memories=existing_memories, 
                new_memories=new_memories
            )
        except KeyError:
            # If custom prompt doesn't have format placeholders, return as-is or append
            if "{existing_memories}" not in prompt_template or "{new_memories}" not in prompt_template:
                logger.warning("Custom update graph prompt missing format placeholders, appending data")
                return f"{prompt_template}\n\nExisting Memories:\n{existing_memories}\n\nNew Memories:\n{new_memories}"
            return prompt_template.format(
                existing_memories=existing_memories, 
                new_memories=new_memories
            )
    
    def get_extract_relations_prompt(self, text: str) -> str:
        """
        Get relations extraction prompt.
        
        Args:
            text: Text to extract relations from
            
        Returns:
            Formatted prompt
        """
        # Use custom prompt if provided, otherwise use default
        prompt = self._custom_extract_relations_prompt or EXTRACT_RELATIONS_PROMPT
        return prompt.replace("USER_ID", "USER_ID")
    
    def get_delete_relations_prompt(self, existing_memories: str, new_text: str, user_id: str = "USER_ID") -> tuple[str, str]:
        """
        Get delete relations prompt.
        
        Args:
            existing_memories: Existing graph memories
            new_text: New text information
            user_id: User ID for self-references
            
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        # Use custom prompt if provided, otherwise use default
        system_prompt = self._custom_delete_relations_prompt or DELETE_RELATIONS_SYSTEM_PROMPT
        system_prompt = system_prompt.replace("USER_ID", user_id)
        user_prompt = f"Here are the existing memories: {existing_memories} \n\n New Information: {new_text}"
        
        return system_prompt, user_prompt
    
    def get_system_prompt(self, prompt_type: str = "extract_relations") -> str:
        """
        Get system prompt for graph operations.
        
        Args:
            prompt_type: Type of system prompt (extract_relations, delete_relations)
            
        Returns:
            System prompt
        """
        if prompt_type == "extract_relations":
            # Use custom prompt if provided, otherwise use default
            return self._custom_extract_relations_prompt or EXTRACT_RELATIONS_PROMPT
        elif prompt_type == "delete_relations":
            # Use custom prompt if provided, otherwise use default
            return self._custom_delete_relations_prompt or DELETE_RELATIONS_SYSTEM_PROMPT
        else:
            return self._custom_extract_relations_prompt or EXTRACT_RELATIONS_PROMPT