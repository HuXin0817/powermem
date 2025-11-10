# Memory API Reference

`Memory` is the core synchronous memory management class in powermem. It provides a simple interface for storing, retrieving, and managing memories in LLM applications.

## Class: `Memory`

```python
from powermem import Memory

memory = Memory(config=config)
```

### Constructor

#### `Memory(config=None, storage_type=None, llm_provider=None, embedding_provider=None, agent_id=None)`

Create a new Memory instance.

**Parameters:**
- `config` (dict, optional): Configuration dictionary. If None, loads from environment variables.
- `storage_type` (str, optional): Storage backend type (deprecated, use config).
- `llm_provider` (str, optional): LLM provider name (deprecated, use config).
- `embedding_provider` (str, optional): Embedding provider name (deprecated, use config).
- `agent_id` (str, optional): Agent identifier for multi-agent scenarios.

**Example:**
```python
from powermem import Memory, auto_config

# Auto-load from .env
config = auto_config()
memory = Memory(config=config, agent_id="my_agent")
```

### Core Methods

#### `add(messages, user_id=None, agent_id=None, run_id=None, metadata=None, filters=None, scope=None, memory_type=None, prompt=None, infer=True)`

Add a memory to the store.

**Parameters:**
- `messages` (str | dict | list[dict]): Memory content. Can be:
  - A string (will be converted to a message)
  - A single message dict with `role` and `content`
  - A list of message dicts in OpenAI format
- `user_id` (str, optional): User identifier.
- `agent_id` (str, optional): Agent identifier.
- `run_id` (str, optional): Run/conversation identifier.
- `metadata` (dict, optional): Additional metadata.
- `filters` (dict, optional): Filter metadata for advanced filtering.
- `scope` (str, optional): Memory scope (e.g., 'user', 'agent', 'session').
- `memory_type` (str, optional): Memory type classification.
- `prompt` (str, optional): Custom prompt for intelligent processing.
- `infer` (bool): Enable intelligent memory processing (default: True).

**Returns:**
- `dict`: Result containing added memory information.

**Example:**
```python
# Simple text memory
result = memory.add(
    messages="User likes Python programming",
    user_id="user123"
)

# With intelligent processing (default)
result = memory.add(
    messages=[
        {"role": "user", "content": "I'm Alice, a software engineer"},
        {"role": "assistant", "content": "Nice to meet you!"}
    ],
    user_id="user123"
    # infer=True by default - enables intelligent fact extraction
)

# Single message dict
result = memory.add(
    messages={"role": "user", "content": "I prefer dark mode"},
    user_id="user123"
)
```

#### `search(query, user_id=None, agent_id=None, run_id=None, filters=None, limit=30, threshold=None)`

Search for memories using semantic similarity.

**Parameters:**
- `query` (str): Search query string.
- `user_id` (str, optional): Filter by user ID.
- `agent_id` (str, optional): Filter by agent ID.
- `run_id` (str, optional): Filter by run ID.
- `filters` (dict, optional): Metadata filters for advanced filtering.
- `limit` (int): Maximum number of results (default: 30).
- `threshold` (float, optional): Similarity threshold (0.0-1.0) for filtering results.

**Returns:**
- `dict`: Search results with memories and scores. Format:
  ```python
  {
      "results": [
          {
              "memory": "memory content",
              "metadata": {...},
              "score": 0.85,
              "id": 123,
              ...
          }
      ],
      "relations": [...]  # If graph store is enabled
  }
  ```

**Example:**
```python
results = memory.search(
    query="user preferences",
    user_id="user123",
    limit=5,
    threshold=0.7  # Only return results with similarity >= 0.7
)

for result in results.get('results', []):
    print(f"Memory: {result['memory']}")
    print(f"Score: {result.get('score', 0)}")
```

#### `get(memory_id, user_id=None, agent_id=None)`

Retrieve a specific memory by ID.

**Parameters:**
- `memory_id` (int): Memory identifier.
- `user_id` (str, optional): User identifier for permission check.
- `agent_id` (str, optional): Agent identifier for permission check.

**Returns:**
- `dict | None`: Memory data or None if not found.

**Example:**
```python
memory_data = memory.get(123, user_id="user123")
if memory_data:
    print(f"Content: {memory_data.get('memory', '')}")
```

#### `update(memory_id, content=None, user_id=None, agent_id=None, metadata=None)`

Update an existing memory.

**Parameters:**
- `memory_id` (int): Memory identifier.
- `content` (str, optional): New memory content.
- `user_id` (str, optional): User identifier for permission check.
- `agent_id` (str, optional): Agent identifier for permission check.
- `metadata` (dict, optional): Updated metadata.

**Returns:**
- `dict`: Updated memory data.

**Example:**
```python
updated = memory.update(
    memory_id=123,
    content="User prefers Python over Java",
    user_id="user123",
    metadata={"updated_at": "2024-01-01"}
)
```

#### `delete(memory_id, user_id=None, agent_id=None)`

Delete a memory by ID.

**Parameters:**
- `memory_id` (int): Memory identifier.
- `user_id` (str, optional): User identifier for permission check.
- `agent_id` (str, optional): Agent identifier for permission check.

**Returns:**
- `bool`: True if deleted, False otherwise.

**Example:**
```python
success = memory.delete(123, user_id="user123")
```

#### `delete_all(user_id=None, agent_id=None, run_id=None)`

Delete all memories matching criteria.

**Parameters:**
- `user_id` (str, optional): Filter by user ID.
- `agent_id` (str, optional): Filter by agent ID.
- `run_id` (str, optional): Filter by run ID.

**Returns:**
- `dict`: Deletion result with count.

**Example:**
```python
result = memory.delete_all(user_id="user123")
print(f"Deleted {result.get('count', 0)} memories")
```

#### `get_all(user_id=None, agent_id=None, run_id=None, limit=100, offset=0, filters=None)`

Retrieve all memories matching criteria.

**Parameters:**
- `user_id` (str, optional): Filter by user ID.
- `agent_id` (str, optional): Filter by agent ID.
- `run_id` (str, optional): Filter by run ID.
- `limit` (int): Maximum number of results (default: 100).
- `offset` (int): Offset for pagination (default: 0).
- `filters` (dict, optional): Metadata filters for advanced filtering.

**Returns:**
- `dict`: All matching memories. Format:
  ```python
  {
      "results": [
          {
              "id": 123,
              "memory": "content",
              "metadata": {...},
              ...
          }
      ],
      "relations": [...]  # If graph store is enabled
  }
  ```

**Example:**
```python
all_memories = memory.get_all(user_id="user123", limit=50, offset=0)
for mem in all_memories.get('results', []):
    print(f"- {mem.get('memory', '')}")
```

### Intelligent Memory Features

When `infer=True` (default), Memory automatically:

- **Fact Extraction**: Extracts facts from conversations
- **Duplicate Detection**: Prevents duplicate memories
- **Memory Updates**: Updates existing memories when information changes
- **Conflict Resolution**: Handles contradictory information
- **Memory Consolidation**: Merges related memories

**Note:** Intelligent processing is enabled by default. Set `infer=False` to disable it for simple storage operations.

See [Intelligent Memory Guide](../guides/intelligent_memory.md) for more details.

### Error Handling

All methods may raise exceptions. Common errors:

- `ValueError`: Invalid parameters
- `ConnectionError`: Storage backend connection issues
- `RuntimeError`: LLM or embedding service errors

**Example:**
```python
try:
    result = memory.add(memory="Test", user_id="user123")
except Exception as e:
    print(f"Error: {e}")
```

