# Configuration Guide

Complete guide to configuring powermem for different environments and use cases.

## Configuration Methods

### Method 1: Environment Variables (Recommended)

Create a `.env` file in your project root:

```env
# LLM Configuration
LLM_PROVIDER=qwen
LLM_API_KEY=your_api_key
LLM_MODEL=qwen-plus
LLM_TEMPERATURE=0.7

# Embedding Configuration
EMBEDDING_PROVIDER=qwen
EMBEDDING_API_KEY=your_api_key
EMBEDDING_MODEL=text-embedding-v4

# Vector Store Configuration
DATABASE_PROVIDER=sqlite
DATABASE_PATH=./memories.db
```

Then use auto-configuration:

```python
from powermem import create_memory

memory = create_memory()  # Auto-loads from .env
```

### Method 2: Programmatic Configuration

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

## LLM Providers

### Qwen (Alibaba Cloud)

```env
LLM_PROVIDER=qwen
LLM_API_KEY=your_dashscope_api_key
LLM_MODEL=qwen-plus
LLM_TEMPERATURE=0.7
LLM_BASE_URL=https://dashscope.aliyuncs.com/api/v1
```

### OpenAI

```env
LLM_PROVIDER=openai
LLM_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
```

### Anthropic Claude

```env
LLM_PROVIDER=anthropic
LLM_API_KEY=your_anthropic_api_key
LLM_MODEL=claude-3-opus-20240229
LLM_TEMPERATURE=0.7
```

### Ollama (Local)

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama2
LLM_BASE_URL=http://localhost:11434
```

## Embedding Providers

### Qwen Embeddings

```env
EMBEDDING_PROVIDER=qwen
EMBEDDING_API_KEY=your_dashscope_api_key
EMBEDDING_MODEL=text-embedding-v4
EMBEDDING_DIMS=1536
```

### OpenAI Embeddings

```env
EMBEDDING_PROVIDER=openai
EMBEDDING_API_KEY=your_openai_api_key
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMS=3072
```

### HuggingFace

```env
EMBEDDING_PROVIDER=huggingface
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMS=384
```

## Vector Store Configuration

### SQLite (Development)

```env
DATABASE_PROVIDER=sqlite
DATABASE_PATH=./memories.db
```

**Use Cases:**
- Development and testing
- Single-user applications
- Prototyping

### OceanBase (Production)

```env
DATABASE_PROVIDER=oceanbase
DATABASE_HOST=127.0.0.1
DATABASE_PORT=2881
DATABASE_USER=root@sys
DATABASE_PASSWORD=password
DATABASE_NAME=powermem
DATABASE_COLLECTION_NAME=memories
DATABASE_EMBEDDING_MODEL_DIMS=1536
DATABASE_VECTOR_METRIC_TYPE=cosine
DATABASE_INDEX_TYPE=IVF_FLAT
```

**Use Cases:**
- Production deployments
- Enterprise applications
- High-scale scenarios

### PostgreSQL

```env
DATABASE_PROVIDER=postgresql
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_NAME=powermem
```

**Prerequisites:**
- PostgreSQL with pgvector extension

## Intelligent Memory Configuration

```env
INTELLIGENT_MEMORY_ENABLED=true
INTELLIGENT_MEMORY_INITIAL_RETENTION=1.0
INTELLIGENT_MEMORY_DECAY_RATE=0.1
INTELLIGENT_MEMORY_REINFORCEMENT_FACTOR=0.3
INTELLIGENT_MEMORY_WORKING_THRESHOLD=0.8
INTELLIGENT_MEMORY_SHORT_TERM_THRESHOLD=0.6
INTELLIGENT_MEMORY_LONG_TERM_THRESHOLD=0.4
```

**Parameters:**
- `initial_retention`: Starting retention score (0.0-1.0)
- `decay_rate`: How fast memories decay (0.0-1.0)
- `reinforcement_factor`: Reinforcement strength (0.0-1.0)
- `*_threshold`: Thresholds for memory phases

## Agent Configuration

```env
AGENT_ENABLED=true
AGENT_MEMORY_MODE=auto
AGENT_DEFAULT_SCOPE=AGENT
AGENT_DEFAULT_PRIVACY_LEVEL=PRIVATE
AGENT_DEFAULT_COLLABORATION_LEVEL=READ_ONLY
AGENT_DEFAULT_ACCESS_PERMISSION=OWNER_ONLY
```

## Audit Configuration

```env
AUDIT_ENABLED=true
AUDIT_LOG_FILE=./logs/audit.log
AUDIT_LOG_LEVEL=INFO
AUDIT_RETENTION_DAYS=90
```

## Configuration Examples

### Development Configuration

```python
config = {
    'vector_store': {
        'provider': 'sqlite',
        'config': {'path': './dev.db'}
    },
    'llm': {
        'provider': 'ollama',
        'config': {'model': 'llama2'}
    },
    'embedder': {
        'provider': 'huggingface',
        'config': {'model': 'sentence-transformers/all-MiniLM-L6-v2'}
    }
}
```

### Production Configuration

```python
config = {
    'vector_store': {
        'provider': 'oceanbase',
        'config': {
            'host': 'prod-db.example.com',
            'port': 2881,
            'user': 'prod_user',
            'password': 'secure_password',
            'db_name': 'powermem_prod'
        }
    },
    'llm': {
        'provider': 'qwen',
        'config': {
            'api_key': 'production_key',
            'model': 'qwen-plus'
        }
    },
    'embedder': {
        'provider': 'qwen',
        'config': {
            'api_key': 'production_key',
            'model': 'text-embedding-v4'
        }
    },
    'intelligent_memory': {
        'enabled': True,
        'initial_retention': 1.0,
        'decay_rate': 0.1
    },
    'audit': {
        'enabled': True,
        'log_file': '/var/log/powermem/audit.log'
    }
}
```

## Configuration Validation

```python
from powermem.config_loader import validate_config

config = {...}
is_valid, errors = validate_config(config)

if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

## Environment-Specific Configuration

### Development

Use SQLite and mock/local providers:

```env
DATABASE_PROVIDER=sqlite
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=huggingface
```

### Staging

Use production-like setup:

```env
DATABASE_PROVIDER=oceanbase
DATABASE_HOST=staging-db.example.com
LLM_PROVIDER=qwen
EMBEDDING_PROVIDER=qwen
```

### Production

Full production configuration:

```env
DATABASE_PROVIDER=oceanbase
DATABASE_HOST=prod-db.example.com
LLM_PROVIDER=qwen
EMBEDDING_PROVIDER=qwen
INTELLIGENT_MEMORY_ENABLED=true
AUDIT_ENABLED=true
```

## Best Practices

1. **Use .env files**: Keep configuration separate from code
2. **Never commit secrets**: Add `.env` to `.gitignore`
3. **Validate configuration**: Use `validate_config()` before deployment
4. **Environment-specific configs**: Different configs for dev/staging/prod
5. **Monitor configuration**: Log configuration at startup (without secrets)

## See Also

- [Getting Started Guide](getting_started.md)
- [Configuration API](../api/configuration.md)
- [Examples](../examples/)

