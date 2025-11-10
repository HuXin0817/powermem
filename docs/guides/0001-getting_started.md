# Getting Started Guide

Welcome to powermem! This guide will help you get started quickly.

## Installation

### Basic Installation

```bash
pip install powermem
```

### With Dependencies

```bash
# With LLM and vector store dependencies
pip install powermem[llm,vector_stores]

# For development with all dependencies
pip install powermem[dev,test,llm,vector_stores,extras]
```

## Quick Start

### Simplest Example

```python
from powermem import create_memory

# Auto-loads from .env or uses mock providers
memory = create_memory()

# Add a memory
memory.add(messages="User likes Python programming", user_id="user123")

# Search memories
results = memory.search("user preferences", user_id="user123")
for result in results.get('results', []):
    print(f"- {result['memory']}")
```

### With Configuration

Create a `.env` file:

```env
LLM_PROVIDER=qwen
LLM_API_KEY=your_api_key
LLM_MODEL=qwen-plus
EMBEDDING_PROVIDER=qwen
EMBEDDING_API_KEY=your_api_key
EMBEDDING_MODEL=text-embedding-v4
```

Then use:

```python
from powermem import create_memory

memory = create_memory()  # Auto-loads from .env
```

## Basic Concepts

### Memory

A memory is a piece of information stored in powermem:

```python
memory.add(
    messages="User prefers email support",
    user_id="user123"
)
```

### User ID

Identifies the user associated with memories:

```python
memory.add(messages="Preference", user_id="user123")
results = memory.search("preferences", user_id="user123")
```

### Agent ID

For multi-agent scenarios:

```python
memory = Memory(config=config, agent_id="support_agent")
memory.add(messages="Memory", user_id="user123", agent_id="support_agent")
```

### Metadata

Additional information about memories:

```python
memory.add(
    messages="User preference",
    user_id="user123",
    metadata={
        "category": "preference",
        "importance": "high"
    }
)
```

## Core Operations

### Adding Memories

```python
# Simple text
memory.add(messages="User likes Python", user_id="user123")

# With metadata
memory.add(
    messages="User prefers email",
    user_id="user123",
    metadata={"category": "preference"}
)

# From conversation (intelligent)
memory.add(
    messages=[
        {"role": "user", "content": "I'm Alice, a software engineer"},
        {"role": "assistant", "content": "Nice to meet you!"}
    ],
    user_id="user123",
    infer=True  # Enable intelligent fact extraction
)
```

### Searching Memories

```python
# Basic search
results = memory.search(
    query="user preferences",
    user_id="user123"
)

# With limit
results = memory.search(
    query="user preferences",
    user_id="user123",
    limit=5
)

# With metadata filter
results = memory.search(
    query="user preferences",
    user_id="user123",
    metadata_filter={"category": "preference"}
)
```

### Updating Memories

```python
# Update content
memory.update(
    memory_id=123,
    content="Updated preference"
)

# Update metadata
memory.update(
    memory_id=123,
    content="Updated preference",  # content is required
    metadata={"updated_at": "2024-01-01"}
)
```

### Deleting Memories

```python
# Delete single memory
memory.delete(memory_id=123)

# Delete all user memories
memory.delete_all(user_id="user123")
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
LLM_PROVIDER=qwen
LLM_API_KEY=your_api_key
LLM_MODEL=qwen-plus
EMBEDDING_PROVIDER=qwen
EMBEDDING_API_KEY=your_api_key
EMBEDDING_MODEL=text-embedding-v4
DATABASE_PROVIDER=sqlite
```

### Programmatic Configuration

```python
from powermem import Memory

config = {
    'llm': {
        'provider': 'qwen',
        'config': {
            'api_key': 'your_api_key',
            'model': 'qwen-plus'
        }
    },
    'embedder': {
        'provider': 'qwen',
        'config': {
            'api_key': 'your_api_key',
            'model': 'text-embedding-v4'
        }
    },
    'vector_store': {
        'provider': 'sqlite',
        'config': {'path': './memories.db'}
    }
}

memory = Memory(config=config)
```

## Next Steps

1. **Try Examples**: See [Examples](../examples/) for detailed scenarios
2. **Learn Configuration**: Read [Configuration Guide](configuration.md)
3. **Multi-Agent**: Explore [Multi-Agent Guide](multi_agent.md)
4. **API Reference**: Check [API Documentation](../api/)

## Common Tasks

### Task 1: Store User Preferences

```python
memory.add(messages="User likes Python", user_id="user123")
memory.add(messages="User prefers email support", user_id="user123")
```

### Task 2: Retrieve User Context

```python
results = memory.search(
    query="user preferences and interests",
    user_id="user123"
)
```

### Task 3: Multi-Agent Setup

```python
support_agent = Memory(config=config, agent_id="support_agent")
sales_agent = Memory(config=config, agent_id="sales_agent")

support_agent.add(messages="Customer prefers email", user_id="customer123")
sales_agent.add(messages="Customer interested in AI", user_id="customer123")
```

### Task 4: Intelligent Memory

```python
memory.add(
    messages=[
        {"role": "user", "content": "I'm Alice, a software engineer"},
        {"role": "assistant", "content": "Nice to meet you!"}
    ],
    user_id="user123",
    infer=True  # Automatically extracts facts
)
```

## Troubleshooting

### Common Issues

**Issue**: "No API key found"
- **Solution**: Create `.env` file or use mock providers

**Issue**: "Database connection failed"
- **Solution**: Check database configuration and connectivity

**Issue**: "Memory not found"
- **Solution**: Verify memory_id (should be int) and user_id match

## See Also

- [Configuration Guide](configuration.md)
- [Examples](../examples/)
- [API Reference](../api/)

