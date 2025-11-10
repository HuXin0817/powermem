# Agent APIs Reference

powermem provides comprehensive multi-agent memory management capabilities.

## Agent Memory Management

### Creating Agent-Specific Memories

```python
from powermem import Memory, auto_config

config = auto_config()

# Create memory instances for different agents
support_agent = Memory(config=config, agent_id="support_agent")
sales_agent = Memory(config=config, agent_id="sales_agent")
tech_agent = Memory(config=config, agent_id="tech_agent")
```

### Agent-Specific Operations

#### Adding Agent Memories

```python
# Support agent adds memory
support_agent.add(
    messages="Customer prefers email support",
    user_id="customer123",
    agent_id="support_agent",
    metadata={"category": "preference"}
)

# Sales agent adds memory
sales_agent.add(
    messages="Customer interested in AI features",
    user_id="customer123",
    agent_id="sales_agent",
    metadata={"category": "interest"}
)
```

#### Agent-Specific Search

```python
# Search only support agent memories
results = support_agent.search(
    query="customer preferences",
    user_id="customer123",
    agent_id="support_agent"  # Filter by agent
)
```

#### Cross-Agent Search

```python
# Search across all agents
results = support_agent.search(
    query="customer information",
    user_id="customer123"
    # No agent_id filter - searches all agents
)
```

## Multi-Agent Memory Manager

### Using MultiAgentMemoryManager

```python
from powermem.agent.implementations.multi_agent import MultiAgentMemoryManager
from powermem.agent.components.collaboration_coordinator import CollaborationCoordinator
from powermem.agent.components.permission_controller import PermissionController

config = auto_config()

# Create multi-agent manager
manager = MultiAgentMemoryManager(config=config)

# Register agents
manager.register_agent("alice", "developer")
manager.register_agent("bob", "developer")
manager.register_agent("charlie", "qa")
```

### Agent Components

#### Collaboration Coordinator

Manages agent collaboration and shared memories.

```python
from powermem.agent.components.collaboration_coordinator import CollaborationCoordinator

coordinator = CollaborationCoordinator(config=config)

# Track collaboration
coordinator.track_collaboration(
    agent_ids=["alice", "bob"],
    memory_id="memory_123",
    context="Working on API integration"
)
```

#### Permission Controller

Controls access permissions for agent memories.

```python
from powermem.agent.components.permission_controller import PermissionController

permission = PermissionController(config=config)

# Set permissions
permission.set_permission(
    agent_id="alice",
    memory_id="memory_123",
    permission="READ_WRITE"
)

# Check access
can_access = permission.check_access(
    agent_id="bob",
    memory_id="memory_123"
)
```

#### Privacy Protector

Manages privacy levels and data protection.

```python
from powermem.agent.components.privacy_protector import PrivacyProtector

privacy = PrivacyProtector(config=config)

# Set privacy level
privacy.set_privacy_level(
    memory_id="memory_123",
    level="PRIVATE"
)

# Check if memory can be shared
can_share = privacy.can_share(
    memory_id="memory_123",
    target_agent_id="bob"
)
```

#### Scope Controller

Manages memory scopes (AGENT, USER, GROUP, etc.).

```python
from powermem.agent.components.scope_controller import ScopeController

scope = ScopeController(config=config)

# Set memory scope
scope.set_scope(
    memory_id="memory_123",
    scope="AGENT"
)

# Get memories by scope
agent_memories = scope.get_by_scope(
    agent_id="alice",
    scope="AGENT"
)
```

## Memory Scopes

powermem supports different memory scopes:

- **AGENT**: Agent-specific memories
- **USER**: User-specific memories
- **GROUP**: Group/shared memories
- **SYSTEM**: System-wide memories

### Setting Memory Scope

```python
memory.add(
    messages="Project status update",
    user_id="alice",
    agent_id="alice_dev",
    metadata={"scope": "AGENT"}
)
```

### Scope-Based Search

```python
# Search only agent-scoped memories
results = memory.search(
    query="project status",
    user_id="alice",
    filters={"scope": "AGENT"}
)
```

## Multi-User Memory Manager

For multi-user scenarios:

```python
from powermem.agent.implementations.multi_user import MultiUserMemoryManager

config = auto_config()

# Create multi-user manager
manager = MultiUserMemoryManager(config=config)

# Add user-specific memory
manager.add_user_memory(
    user_id="user123",
    messages="User preference",
    metadata={"category": "preference"}
)

# Search user memories
results = manager.search_user_memories(
    user_id="user123",
    query="preferences"
)
```

## Hybrid Memory Manager

For hybrid scenarios combining multi-agent and multi-user:

```python
from powermem.agent.implementations.hybrid import HybridMemoryManager

config = auto_config()

# Create hybrid manager
manager = HybridMemoryManager(config=config)

# Add memory with both agent and user context
manager.add(
    messages="Collaborative memory",
    user_id="user123",
    agent_id="agent456",
    metadata={"scope": "GROUP"}
)
```

## Best Practices

1. **Use agent_id consistently**: Always specify agent_id when creating memories
2. **Scope appropriately**: Use appropriate memory scopes for isolation
3. **Set permissions**: Configure permissions for sensitive memories
4. **Track collaboration**: Use collaboration coordinator for shared work
5. **Privacy by default**: Set appropriate privacy levels

## See Also

- [Multi-Agent Guide](../guides/multi_agent.md)
- [Memory API](memory.md)
- [Configuration API](configuration.md)

