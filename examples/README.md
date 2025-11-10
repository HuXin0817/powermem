# Powermem Examples

This directory contains various examples demonstrating how to use powermem with different configurations and use cases.

## Examples Overview

### 1. Basic Usage (`basic_usage.py`)
- **Database**: SQLite
- **Purpose**: Simple memory operations demonstration
- **Configuration**: Auto-loads from `configs/.env` or uses mock providers
- **Run**: `python examples/basic_usage.py`
- **✨ Simplified**: Now uses `create_memory()` for easy setup with automatic config loading

### 2. Agent Memory Demo (`agent_memory.py`)
- **Database**: OceanBase (configurable)
- **Purpose**: Unified interface for all agent memory scenarios
- **Features**: Auto mode detection, multi-agent, multi-user, hybrid modes, intelligent memory with Ebbinghaus algorithm
- **Run**: `python examples/agent_memory.py`
- **✨ Unified**: Single API for all scenarios, automatic mode detection
- **Demonstrates**: 
  - Auto, multi-agent, multi-user, and hybrid modes
  - Intelligent memory management with importance scoring
  - Ebbinghaus forgetting curve algorithm
  - Memory deletion and reset operations

### 3. Intelligent Memory Demo (`intelligent_memory_demo.py`)
- **Database**: OceanBase (configurable)
- **Purpose**: Advanced intelligent memory management features
- **Features**: Fact extraction, duplicate detection, conflict resolution, memory consolidation
- **Run**: `python examples/intelligent_memory_demo.py`
- **Demonstrates**:
  - Automatic fact extraction from conversations
  - Duplicate detection and deduplication
  - Information updates and consolidation
  - Conflict resolution (contradiction handling)
  - Comparison between simple and intelligent modes

## Configuration Files

- `configs/powermem.env` - OceanBase configuration template (copy from `configs/powermem.env.example` if needed)


## Quick Start

1. **Choose your database backend**:
   - **SQLite** (simple, file-based): Works out of the box, no configuration needed
   - **OceanBase** (enterprise, scalable): Requires `configs/powermem.env` configuration

2. **Configure your environment** (for OceanBase):
   ```bash
   # Copy and edit the OceanBase configuration
   cp configs/powermem.env.example configs/powermem.env
   # Edit configs/powermem.env with your OceanBase credentials and API keys
   ```

3. **Run an example**:
   ```bash
   # Basic SQLite example (works without config)
   python examples/basic_usage.py
   
   # Unified agent memory demo (RECOMMENDED)
   # Requires OceanBase configuration
   python examples/agent_memory.py
   
   # Intelligent memory management demo
   # Requires OceanBase configuration
   python examples/intelligent_memory_demo.py
   
   # Run specific scenario in intelligent memory demo
   python examples/intelligent_memory_demo.py 1  # Run scenario 1
   python examples/intelligent_memory_demo.py compare  # Compare modes
   ```

## Database Backends

### SQLite
- **Pros**: Simple setup, no external dependencies, good for development
- **Cons**: Limited scalability, single-user access
- **Use Case**: Development, testing, small applications

### OceanBase
- **Pros**: High performance, scalable, enterprise features, multi-user support
- **Cons**: Requires OceanBase installation, more complex setup
- **Use Case**: Production applications, large-scale deployments

## Unified Agent Memory Interface

The new unified interface provides a single, consistent API for all agent memory scenarios:

### Auto Mode (Recommended)
```python
from powermem.agent import AgentMemory
from powermem import auto_config
from dotenv import load_dotenv

# Load configuration from environment
load_dotenv('configs/powermem.env')  # or your config path
config = auto_config()

# Automatic mode detection
agent_memory = AgentMemory(config, mode='auto')

# Same API regardless of detected mode
agent_memory.add("Memory content", user_id="user123", agent_id="agent456")
results = agent_memory.search("query", user_id="user123")
```

### Multi-Agent Mode
```python
from powermem.agent import AgentMemory
from powermem import auto_config
from dotenv import load_dotenv

load_dotenv('configs/powermem.env')
config = auto_config()

# Explicit multi-agent mode
agent_memory = AgentMemory(config, mode='multi_agent')

# Create agents
support_agent = agent_memory.create_agent("support_agent", "Customer Support")
sales_agent = agent_memory.create_agent("sales_agent", "Sales Agent")

# Agent-specific operations
support_agent.add("Customer prefers email support", user_id="customer_123")
sales_agent.add("Customer budget is $1000/month", user_id="customer_123")

# Group management
agent_memory.create_group("customer_team", ["support_agent", "sales_agent"])
```

### Multi-User Mode
```python
from powermem.agent import AgentMemory
from powermem import auto_config
from dotenv import load_dotenv

load_dotenv('configs/powermem.env')
config = auto_config()

# Multi-user mode
agent_memory = AgentMemory(config, mode='multi_user')

# User-specific memories
agent_memory.add("Alice likes Python", user_id="alice")
agent_memory.add("Bob prefers Java", user_id="bob")

# User-specific search
alice_memories = agent_memory.search("Python", user_id="alice")
```

### Hybrid Mode
```python
from powermem.agent import AgentMemory
from powermem import auto_config
from dotenv import load_dotenv

load_dotenv('configs/powermem.env')
config = auto_config()

# Hybrid mode with dynamic switching
agent_memory = AgentMemory(config, mode='hybrid')

# Automatic context detection
agent_memory.add("Support agent handled complaint", agent_id="support_agent")
agent_memory.add("User Alice requested features", user_id="alice")

# Mode switching
agent_memory.switch_mode('multi_agent')
```

### Key Benefits
- **Single API** - Consistent interface across all modes
- **Automatic Detection** - Intelligent mode selection
- **Easy Migration** - Simple upgrade from existing code
- **Mode Flexibility** - Switch between modes as needed

## Configuration Examples

### SQLite Configuration
```env
DATABASE_PROVIDER=sqlite
DATABASE_PATH=./data/powermem_dev.db
DATABASE_ENABLE_WAL=true
DATABASE_TIMEOUT=30
```

### OceanBase Configuration
```env
DATABASE_PROVIDER=oceanbase
DATABASE_HOST=localhost
DATABASE_PORT=2881
DATABASE_USER=root
DATABASE_PASSWORD=password
DATABASE_NAME=test
DATABASE_COLLECTION_NAME=memories
DATABASE_VECTOR_METRIC_TYPE=cosine
DATABASE_INDEX_TYPE=ivfflat
EMBEDDING_DIMS=1536
```

## Features Demonstrated

### Basic Features
- ✅ **Memory Storage**: Add, update, delete memories
- ✅ **Semantic Search**: Find similar memories using vector similarity
- ✅ **Multi-user Support**: Isolate memories by user ID
- ✅ **Multi-agent Support**: Agent-specific memory management
- ✅ **Metadata Support**: Attach custom metadata to memories
- ✅ **Real-time Operations**: Immediate memory operations
- ✅ **Vector Embeddings**: High-dimensional vector storage
- ✅ **Configuration Management**: Environment-based configuration

### Advanced Features (Agent Memory & Intelligent Memory)
- ✅ **Intelligent Memory Management**: Automatic importance scoring and memory type classification
- ✅ **Ebbinghaus Forgetting Curve**: Automatic review schedule generation based on memory importance
- ✅ **Fact Extraction**: Automatic extraction of facts from conversations
- ✅ **Duplicate Detection**: Smart deduplication to prevent redundant memories
- ✅ **Conflict Resolution**: Automatic handling of contradictory information
- ✅ **Memory Consolidation**: Merging related memories for better organization
- ✅ **Mode Detection**: Automatic detection of multi-agent vs multi-user contexts
- ✅ **Memory Reset**: Complete memory store reset functionality

## Dependencies

### Common Dependencies
- `python-dotenv` - Environment variable loading
- `dashscope` - Qwen API integration

### OceanBase Dependencies
- `pyobvector` - OceanBase vector operations
- `sqlalchemy` - Database ORM

Install all dependencies:
```bash
pip install python-dotenv dashscope pyobvector sqlalchemy
```

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **Configuration Errors**: Check environment variable values
3. **Connection Issues**: Verify database connectivity
4. **API Key Issues**: Ensure valid API keys are configured

### Getting Help
- Check individual example documentation
- Review configuration templates
- Verify database connectivity
- Check API key validity
