# Scenario 3: Multi-Agent

This scenario demonstrates how to use powermem with multiple agents - creating agent-specific memories, cross-agent collaboration, and memory isolation.

## Prerequisites

- Completed Scenario 1
- Basic understanding of multi-agent systems
- powermem installed

## Understanding Multi-Agent Memory

In multi-agent scenarios:
- Each agent has isolated memory space
- Agents can share memories when needed
- Cross-agent search enables collaboration
- Memory scopes control visibility

## Step 1: Create Multiple Agents

First, let's create memory instances for different agents:

```python
# multi_agent_example.py
from powermem import create_memory, auto_config

config = auto_config()

# Create memory instances for different agents
support_agent = create_memory(config=config, agent_id="support_agent")
sales_agent = create_memory(config=config, agent_id="sales_agent")
tech_agent = create_memory(config=config, agent_id="tech_agent")

print("✓ Created memory instances for:")
print("  - Support Agent")
print("  - Sales Agent")
print("  - Technical Agent")
```

**Run this code:**
```bash
python multi_agent_example.py
```

**Expected output:**
```
✓ Created memory instances for:
  - Support Agent
  - Sales Agent
  - Technical Agent
```

## Step 2: Add Agent-Specific Memories

Each agent adds memories to their own space:

```python
# multi_agent_example.py
from powermem import create_memory, auto_config

config = auto_config()
customer_id = "customer_12345"

# Create agents
support_agent = create_memory(config=config, agent_id="support_agent")
sales_agent = create_memory(config=config, agent_id="sales_agent")
tech_agent = create_memory(config=config, agent_id="tech_agent")

# Support agent adds memory
support_agent.add(
    "Customer prefers email support over phone calls",
    user_id=customer_id,
    metadata={"category": "communication_preference"}
)

# Sales agent adds memory
sales_agent.add(
    "Customer interested in AI-powered features and automation",
    user_id=customer_id,
    metadata={"category": "product_interest"}
)

# Technical agent adds memory
tech_agent.add(
    "Customer uses Python and PostgreSQL in their tech stack",
    user_id=customer_id,
    metadata={"category": "technical_info"}
)

print("✓ Added memories for each agent")
```

**Run this code:**
```bash
python multi_agent_example.py
```

**Expected output:**
```
✓ Added memories for each agent
```

## Step 3: Agent-Specific Search

Each agent can search only their own memories:

```python
# multi_agent_example.py
from powermem import create_memory, auto_config

config = auto_config()
customer_id = "customer_12345"

# Create agents
support_agent = create_memory(config=config, agent_id="support_agent")
sales_agent = create_memory(config=config, agent_id="sales_agent")

# Add memories
support_agent.add(
    "Customer prefers email support",
    user_id=customer_id
)
sales_agent.add(
    "Customer interested in AI features",
    user_id=customer_id
)

# Support agent searches their memories
print("Support Agent Search:")
support_results = support_agent.search(
    query="customer preferences",
    user_id=customer_id,
    agent_id="support_agent"
)
for result in support_results.get('results', []):
    print(f"  - {result['memory']}")

# Sales agent searches their memories
print("\nSales Agent Search:")
sales_results = sales_agent.search(
    query="customer interests",
    user_id=customer_id,
    agent_id="sales_agent"
)
for result in sales_results.get('results', []):
    print(f"  - {result['memory']}")
```

**Run this code:**
```bash
python multi_agent_example.py
```

**Expected output:**
```
Support Agent Search:
  - Customer prefers email support

Sales Agent Search:
  - Customer interested in AI features
```

## Step 4: Cross-Agent Search

Search across all agents by omitting agent_id:

```python
# multi_agent_example.py
from powermem import create_memory, auto_config

config = auto_config()
customer_id = "customer_12345"

# Create agents
support_agent = create_memory(config=config, agent_id="support_agent")
sales_agent = create_memory(config=config, agent_id="sales_agent")
tech_agent = create_memory(config=config, agent_id="tech_agent")

# Add memories for each agent
support_agent.add("Customer prefers email support", user_id=customer_id)
sales_agent.add("Customer interested in AI features", user_id=customer_id)
tech_agent.add("Customer uses Python and PostgreSQL", user_id=customer_id)

# Cross-agent search (no agent_id filter)
print("Cross-Agent Search:")
all_results = support_agent.search(
    query="customer information",
    user_id=customer_id
    # No agent_id - searches all agents
)

print(f"Found {len(all_results.get('results', []))} memories across all agents:")
for result in all_results.get('results', []):
    agent_id = result.get('agent_id', 'Unknown')
    print(f"  [{agent_id}] {result['memory']}")
```

**Run this code:**
```bash
python multi_agent_example.py
```

**Expected output:**
```
Cross-Agent Search:
Found 3 memories across all agents:
  [support_agent] Customer prefers email support
  [sales_agent] Customer interested in AI features
  [tech_agent] Customer uses Python and PostgreSQL
```

## Step 5: Project Collaboration

Multiple agents working on the same project:

```python
# multi_agent_example.py
from powermem import create_memory, auto_config

config = auto_config()
project_id = "project_ai_platform"

# Create developer agents
alice_dev = create_memory(config=config, agent_id="alice_dev")
bob_dev = create_memory(config=config, agent_id="bob_dev")
charlie_qa = create_memory(config=config, agent_id="charlie_qa")

# Alice adds development memory
alice_dev.add(
    "Implemented user authentication module with JWT tokens",
    user_id="alice",
    run_id=project_id,
    metadata={"scope": "development", "module": "authentication"}
)

# Bob adds development memory
bob_dev.add(
    "Created database schema for user profiles",
    user_id="bob",
    run_id=project_id,
    metadata={"scope": "development", "module": "database"}
)

# Charlie adds QA memory
charlie_qa.add(
    "Found critical bug in user registration flow",
    user_id="charlie",
    run_id=project_id,
    metadata={"scope": "testing", "issue_type": "bug"}
)

# Search project-wide memories
print("Project Status Search:")
project_results = alice_dev.search(
    query="project status and progress",
    run_id=project_id
)

for result in project_results.get('results', []):
    agent_id = result.get('agent_id', 'Unknown')
    scope = result.get('metadata', {}).get('scope', 'Unknown')
    print(f"  [{agent_id}] [{scope}] {result['memory']}")
```

**Run this code:**
```bash
python multi_agent_example.py
```

**Expected output:**
```
Project Status Search:
  [alice_dev] [development] Implemented user authentication module with JWT tokens
  [bob_dev] [development] Created database schema for user profiles
  [charlie_qa] [testing] Found critical bug in user registration flow
```

## Step 6: Memory Scopes

Using memory scopes to control visibility:

```python
# multi_agent_example.py
from powermem import create_memory, auto_config

config = auto_config()

# Create agent
agent = create_memory(config=config, agent_id="demo_agent")

# Add memories with different scopes
agent.add(
    "Agent-specific memory",
    user_id="user123",
    metadata={"scope": "AGENT"}
)

agent.add(
    "User-specific memory",
    user_id="user123",
    metadata={"scope": "USER"}
)

agent.add(
    "Group memory",
    user_id="user123",
    metadata={"scope": "GROUP"}
)

# Search by scope using filters parameter
# Note: For nested metadata fields, use the key path like "metadata.scope"
print("Agent-scoped memories:")
results = agent.search(
    query="memories",
    user_id="user123",
    filters={"metadata.scope": "AGENT"}
)
for result in results.get('results', []):
    print(f"  - {result['memory']}")

# Alternative: Search all memories and filter in Python
print("\nAll memories:")
all_results = agent.search(
    query="memories",
    user_id="user123"
)
for result in all_results.get('results', []):
    scope = result.get('metadata', {}).get('scope', 'Unknown')
    print(f"  [{scope}] {result['memory']}")
```

**Run this code:**
```bash
python multi_agent_example.py
```

**Expected output:**
```
Agent-scoped memories:
  - Agent-specific memory
```

## Step 7: Memory Isolation

Verify that memories are isolated by agent:

```python
# multi_agent_example.py
from powermem import create_memory, auto_config

config = auto_config()
user_id = "user123"

# Create two agents
agent1 = create_memory(config=config, agent_id="agent1")
agent2 = create_memory(config=config, agent_id="agent2")

# Agent1 adds memory
agent1.add("Agent1's memory", user_id=user_id)

# Agent2 adds memory
agent2.add("Agent2's memory", user_id=user_id)

# Agent1 searches (should only see their own)
print("Agent1 search:")
results1 = agent1.search(query="memories", user_id=user_id, agent_id="agent1")
for result in results1.get('results', []):
    print(f"  - {result['memory']}")

# Agent2 searches (should only see their own)
print("\nAgent2 search:")
results2 = agent2.search(query="memories", user_id=user_id, agent_id="agent2")
for result in results2.get('results', []):
    print(f"  - {result['memory']}")
```

**Run this code:**
```bash
python multi_agent_example.py
```

**Expected output:**
```
Agent1 search:
  - Agent1's memory

Agent2 search:
  - Agent2's memory
```

## Complete Example

Here's a complete multi-agent example:

```python
# complete_multi_agent_example.py
from powermem import create_memory, auto_config

def main():
    config = auto_config()
    customer_id = "customer_12345"
    
    print("=" * 80)
    print("Multi-Agent Memory Demo")
    print("=" * 80)
    
    # Create agents
    support_agent = create_memory(config=config, agent_id="support_agent")
    sales_agent = create_memory(config=config, agent_id="sales_agent")
    tech_agent = create_memory(config=config, agent_id="tech_agent")
    
    print("\n[Step 1] Adding Agent-Specific Memories")
    print("-" * 60)
    
    # Add memories for each agent
    support_agent.add(
        "Customer prefers email support over phone calls",
        user_id=customer_id,
        metadata={"category": "communication"}
    )
    
    sales_agent.add(
        "Customer interested in AI-powered features",
        user_id=customer_id,
        metadata={"category": "interest"}
    )
    
    tech_agent.add(
        "Customer uses Python and PostgreSQL",
        user_id=customer_id,
        metadata={"category": "technical"}
    )
    
    print("✓ Added memories for each agent")
    
    print("\n[Step 2] Agent-Specific Search")
    print("-" * 60)
    
    # Support agent search
    print("Support Agent:")
    support_results = support_agent.search(
        query="customer preferences",
        user_id=customer_id,
        agent_id="support_agent"
    )
    for result in support_results.get('results', []):
        print(f"  - {result['memory']}")
    
    print("\n[Step 3] Cross-Agent Search")
    print("-" * 60)
    
    # Cross-agent search
    all_results = support_agent.search(
        query="customer information",
        user_id=customer_id
    )
    
    print(f"Found {len(all_results.get('results', []))} memories across all agents:")
    for result in all_results.get('results', []):
        agent_id = result.get('agent_id', 'Unknown')
        print(f"  [{agent_id}] {result['memory']}")
    
    print("\n" + "=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
```

**Run this code:**
```bash
python complete_multi_agent_example.py
```

## Extension Exercises

### Exercise 1: Team Collaboration

Create a team scenario with multiple developers:

```python
config = auto_config()
project_id = "project_xyz"

dev1 = create_memory(config=config, agent_id="dev1")
dev2 = create_memory(config=config, agent_id="dev2")

# Each developer adds project memories
dev1.add("Implemented feature X", run_id=project_id)
dev2.add("Implemented feature Y", run_id=project_id)

# Search project-wide
results = dev1.search("project progress", run_id=project_id)
```

### Exercise 2: Customer Service Team

Create a customer service scenario:

```python
config = auto_config()
customer_id = "customer_123"

agent1 = create_memory(config=config, agent_id="cs_agent_1")
agent2 = create_memory(config=config, agent_id="cs_agent_2")

# Both agents work with same customer
agent1.add("Customer reported issue A", user_id=customer_id)
agent2.add("Customer issue resolved", user_id=customer_id)

# Both can see customer history
history = agent1.search("customer issues", user_id=customer_id)
```

### Exercise 3: Memory Scopes

Experiment with different memory scopes:

```python
agent = create_memory(config=config, agent_id="agent")

# Add memories with different scopes
agent.add("Private memory", metadata={"scope": "AGENT"})
agent.add("Shared memory", metadata={"scope": "GROUP"})

# Search by scope using filters parameter
# Note: For nested metadata fields, use the key path like "metadata.scope"
private = agent.search("memory", filters={"metadata.scope": "AGENT"})
for result in private.get('results', []):
    print(f"  - {result['memory']}")

print("\nShared memories (GROUP scope):")
shared = agent.search("memory", filters={"metadata.scope": "GROUP"})
```

## Next Steps

- **Scenario 4**: Learn async operations
- **Multi-Agent Guide**: See [Multi-Agent Guide](../guides/multi_agent.md)
- **Agent APIs**: Check [Agent APIs](../api/agents.md)

