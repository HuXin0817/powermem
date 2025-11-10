# Multi-Agent Guide

Complete guide to using powermem in multi-agent scenarios.

## Overview

powermem supports multiple agents working with shared or isolated memory spaces. This enables:

- Agent isolation and privacy
- Cross-agent collaboration
- Shared memory access
- Permission control

## Basic Multi-Agent Setup

### Creating Agent-Specific Memories

```python
from powermem import Memory, auto_config

config = auto_config()

# Create memory instances for different agents
support_agent = Memory(config=config, agent_id="support_agent")
sales_agent = Memory(config=config, agent_id="sales_agent")
tech_agent = Memory(config=config, agent_id="tech_agent")
```

### Adding Agent Memories

```python
customer_id = "customer_12345"

# Support agent adds memory
support_agent.add(
    messages="Customer prefers email support over phone calls",
    user_id=customer_id,
    metadata={"category": "communication_preference"}
)

# Sales agent adds memory
sales_agent.add(
    messages="Customer interested in AI-powered features",
    user_id=customer_id,
    metadata={"category": "product_interest"}
)

# Technical agent adds memory
tech_agent.add(
    messages="Customer uses Python and PostgreSQL in their tech stack",
    user_id=customer_id,
    metadata={"category": "technical_info"}
)
```

## Agent Isolation

### Agent-Specific Search

Each agent can search only their own memories:

```python
# Support agent searches their memories
support_results = support_agent.search(
    query="customer preferences",
    user_id=customer_id,
    agent_id="support_agent"  # Filter by agent
)

for result in support_results.get('results', []):
    print(f"- {result['memory']}")
```

### Memory Isolation

Memories are automatically isolated by `agent_id`:

```python
# These memories are separate
support_agent.add(messages="Memory 1", user_id="user123")
sales_agent.add(messages="Memory 2", user_id="user123")

# Each agent only sees their own memories
```

## Cross-Agent Collaboration

### Cross-Agent Search

Search across all agents by omitting `agent_id`:

```python
# Search across all agents
all_results = support_agent.search(
    query="customer information",
    user_id=customer_id
    # No agent_id filter - searches all agents
)

for result in all_results.get('results', []):
    agent_id = result.get('agent_id', 'Unknown')
    print(f"[{agent_id}] {result['memory']}")
```

### Shared Memory Access

Agents can access shared memories:

```python
# All agents can access this memory
shared_memory = Memory(config=config, agent_id="shared")

shared_memory.add(
    messages="Project status: In progress",
    user_id="team",
    metadata={"scope": "GROUP"}
)
```

## Memory Scopes

### Scope Types

- **AGENT**: Agent-specific memories
- **USER**: User-specific memories
- **GROUP**: Group/shared memories
- **SYSTEM**: System-wide memories

### Setting Scope

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
    metadata_filter={"scope": "AGENT"}
)
```

## Permission Control

### Setting Permissions

```python
from powermem.agent.components.permission_controller import PermissionController

permission = PermissionController(config=config)

# Set read-only permission
permission.set_permission(
    agent_id="alice",
    memory_id=123,  # memory_id should be int
    permission="READ_ONLY"
)

# Set read-write permission
permission.set_permission(
    agent_id="bob",
    memory_id=123,  # memory_id should be int
    permission="READ_WRITE"
)
```

### Checking Access

```python
# Check if agent can access memory
can_access = permission.check_access(
    agent_id="bob",
    memory_id=123  # memory_id should be int
)

if can_access:
    memory_data = memory.get(123)  # memory_id should be int
```

## Privacy Protection

### Privacy Levels

- **PUBLIC**: Visible to all agents
- **PRIVATE**: Only visible to owner
- **SHARED**: Visible to specific agents
- **RESTRICTED**: Restricted access

### Setting Privacy

```python
from powermem.agent.components.privacy_protector import PrivacyProtector

privacy = PrivacyProtector(config=config)

# Set privacy level
privacy.set_privacy_level(
    memory_id=123,  # memory_id should be int
    level="PRIVATE"
)

# Check if memory can be shared
can_share = privacy.can_share(
    memory_id=123,  # memory_id should be int
    target_agent_id="bob"
)
```

## Collaboration Tracking

### Tracking Collaboration

```python
from powermem.agent.components.collaboration_coordinator import CollaborationCoordinator

coordinator = CollaborationCoordinator(config=config)

# Track collaboration between agents
coordinator.track_collaboration(
    agent_ids=["alice", "bob"],
    memory_id=123,  # memory_id should be int
    context="Working on API integration"
)
```

## Use Cases

### Use Case 1: Customer Support Team

```python
# Multiple support agents working with same customer
support_agent_1 = Memory(config=config, agent_id="support_agent_1")
support_agent_2 = Memory(config=config, agent_id="support_agent_2")

customer_id = "customer_123"

# Each agent adds their own memories
support_agent_1.add(
    messages="Customer reported login issue",
    user_id=customer_id
)

support_agent_2.add(
    messages="Customer issue resolved",
    user_id=customer_id
)

# Both agents can see all customer memories
all_issues = support_agent_1.search(
    "customer issues",
    user_id=customer_id
)
```

### Use Case 2: Development Team

```python
# Developers working on same project
alice_dev = Memory(config=config, agent_id="alice_dev")
bob_dev = Memory(config=config, agent_id="bob_dev")

project_id = "project_ai_platform"

# Each developer adds project memories
alice_dev.add(
    messages="Implemented authentication module",
    user_id="alice",
    run_id=project_id,
    metadata={"scope": "development"}
)

bob_dev.add(
    messages="Created database schema",
    user_id="bob",
    run_id=project_id,
    metadata={"scope": "development"}
)

# Search project-wide memories
project_memories = alice_dev.search(
    "project progress",
    run_id=project_id
)
```

### Use Case 3: Multi-Agent System

```python
# Different types of agents
support_agent = Memory(config=config, agent_id="support")
sales_agent = Memory(config=config, agent_id="sales")
tech_agent = Memory(config=config, agent_id="tech")

customer_id = "customer_123"

# Each agent maintains their own memory space
support_agent.add(
    messages="Customer prefers email support",
    user_id=customer_id,
    metadata={"category": "support"}
)

sales_agent.add(
    messages="Customer interested in enterprise plan",
    user_id=customer_id,
    metadata={"category": "sales"}
)

# But can access shared customer context
customer_context = support_agent.search(
    "customer information",
    user_id=customer_id
)
```

## Best Practices

1. **Use consistent agent_ids**: Always specify agent_id when creating memories
2. **Set appropriate scopes**: Use scopes to control memory visibility
3. **Configure permissions**: Set permissions for sensitive memories
4. **Track collaboration**: Use collaboration coordinator for team work
5. **Privacy by default**: Set appropriate privacy levels
6. **Document agent roles**: Document what each agent does
7. **Monitor cross-agent access**: Track cross-agent memory access

## See Also

- [Agent APIs](../api/agents.md)
- [Examples](../examples/)
- [Getting Started Guide](getting_started.md)

