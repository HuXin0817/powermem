[English](README.md) | [中文](README_CN.md) | [日本語](README_JP.md)

<p align="center">
    <a href="https://github.com/oceanbase/powermem/blob/master/LICENSE">
        <img alt="license" src="https://img.shields.io/badge/license-Apache%202.0-green.svg" />
    </a>
    <a href="https://img.shields.io/badge/python%20-3.10.0%2B-blue.svg">
        <img alt="pyversions" src="https://img.shields.io/badge/python%20-3.10.0%2B-blue.svg" />
    </a>
    <a href="https://deepwiki.com/oceanbase/powermem">
        <img alt="Ask DeepWiki" src="https://deepwiki.com/badge.svg" />
    </a>
</p>

# PowerMem - Intelligent Memory System

In AI application development, enabling large language models to persistently "remember" historical conversations, user preferences, and contextual information is a core challenge. PowerMem combines a hybrid storage architecture of vector retrieval, full-text search, and graph databases, and introduces the Ebbinghaus forgetting curve theory from cognitive science to build a powerful memory infrastructure for AI applications. The system also provides comprehensive multi-agent support capabilities, including agent memory isolation, cross-agent collaboration and sharing, fine-grained permission control, and privacy protection mechanisms, enabling multiple AI agents to achieve efficient collaboration while maintaining independent memory spaces.

PowerMem is deeply optimized for OceanBase database, including hybrid retrieval capabilities of vector search and full-text search, support for Sub Stores for data partitioning management, automatic vector index configuration, and flexible selection of various vector index types (HNSW, IVF, FLAT, etc.), providing excellent performance and scalability for large-scale enterprise applications. Whether building intelligent customer service systems, personalized AI assistants, or multi-agent collaboration platforms, PowerMem provides enterprise-grade memory management capabilities, enabling AI to truly have "memory" capabilities.

## Architecture

![Architecture Diagram](docs/images/powermem_en.png)

PowerMem is built with a modular architecture that supports:

- **Core Memory Engine**: Base memory operations and intelligent management
- **Agent Framework**: Multi-agent support with collaboration and permissions
- **Storage Adapters**: Pluggable storage backends (vector, graph, and hybrid)
- **Graph Storage**: Relationship-based graph storage for complex memory interconnections
- **LLM Integrations**: Multiple LLM provider support
- **Embedding Services**: Various embedding model integrations

For detailed architecture information, see the [Architecture Guide](docs/architecture/overview.md).

## Key Features

### Intelligent Memory Management
- **Ebbinghaus Forgetting Curve**: Smart memory optimization based on cognitive science
- **Automatic Importance Scoring**: AI-powered memory importance evaluation
- **Memory Decay & Reinforcement**: Dynamic memory retention based on usage patterns
- **Intelligent Retrieval**: Context-aware memory search and ranking

### Multi-Agent Support
- **Agent Isolation**: Separate memory spaces for different agents
- **Cross-Agent Collaboration**: Shared memory access and collaboration tracking
- **Permission Control**: Fine-grained access control for agent memories
- **Privacy Protection**: Built-in privacy controls and data protection

### Multiple Storage Backends
- **OceanBase**: Default enterprise-grade, scalable vector database with deep optimizations:
  - Hybrid retrieval capabilities of vector search and full-text search
  - Sub Stores support for data partitioning management
  - Automatic vector index configuration
  - Flexible selection of various vector index types (HNSW, IVF, FLAT, etc.)
- **SQLite**: Lightweight, file-based storage for development
- **PostgreSQL**: Open-source vector database solution
- **Custom Adapters**: Extensible storage architecture

### Graph-Based Memory Storage
- **Knowledge Graph**: Extract entities and relationships to build knowledge graphs
- **Graph Retrieval**: Multi-hop graph traversal for complex memory relationships
- **Relationship Search**: Discover connections between memories through graph queries
- **Hybrid Storage**: Combine vector search with graph relationships for enhanced retrieval

## Quick Start

### Installation

```bash
# Basic installation
pip install powermem

# With LLM and vector store dependencies
pip install powermem[llm,vector_stores]

# For development with all dependencies
pip install powermem[dev,test,llm,vector_stores,extras]
```

### Basic Usage

**✨ Simplest Way**: Create memory from `.env` file automatically!

```python
from powermem import create_memory

# Automatically loads from .env or uses mock providers
memory = create_memory()

# Add memory
memory.add("User likes coffee", user_id="user123")

# Search memories
memories = memory.search("user preferences", user_id="user123")
for memory in memories:
    print(f"- {memory.get('memory')}")
```

For more detailed examples and usage patterns, see the [Getting Started Guide](docs/guides/0001-getting_started.md).

## Documentation

- **[Getting Started](docs/guides/0001-getting_started.md)**: Installation and quick start guide
- **[Configuration Guide](docs/guides/0002-configuration.md)**: Complete configuration options
- **[Multi-Agent Guide](docs/guides/0004-multi_agent.md)**: Multi-agent scenarios and examples
- **[Integrations Guide](docs/guides/0005.integrations.md)**: LLM and embedding provider integrations
- **[API Documentation](docs/api/overview.md)**: Complete API reference
- **[Architecture Guide](docs/architecture/overview.md)**: System architecture and design
- **[Examples](docs/examples/overview.md)**: Interactive Jupyter notebooks and use cases

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/powermem/powermem.git
cd powermem

# Install development dependencies
pip install -e ".[dev,test,llm,vector_stores]"
```

## Contributing

We welcome contributions! Please see our contributing guidelines and code of conduct.

## Support

- **Issues**: [GitHub Issues](https://github.com/oceanbase/powermem/issues)
- **Discussions**: [GitHub Discussions](https://github.com/oceanbase/powermem/discussions)

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.