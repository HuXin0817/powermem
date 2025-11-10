# Scenario 2: Intelligent Memory

This scenario demonstrates powermem's intelligent memory features - automatic fact extraction, duplicate detection, conflict resolution, and more.

## Prerequisites

- Completed Scenario 1
- powermem installed
- LLM provider configured (for intelligent features)

## Understanding Intelligent Memory

Intelligent memory enables powermem to:
- Extract facts from conversations automatically
- Detect and prevent duplicates
- Update existing memories when information changes
- Resolve conflicts between contradictory information
- Consolidate related memories

## Step 1: Enable Intelligent Processing

First, let's see how to enable intelligent processing:

```python
# intelligent_memory_example.py
from powermem import create_memory

memory = create_memory()

# Add memory with intelligent processing (infer=True)
result = memory.add(
    messages=[
        {"role": "user", "content": "Hi, my name is Alice. I'm a software engineer at Google."},
        {"role": "assistant", "content": "Nice to meet you, Alice! That's interesting."},
        {"role": "user", "content": "I love Python programming and machine learning."}
    ],
    user_id="user_001",
    infer=True  # Enable intelligent fact extraction
)

print(f"✓ Processed conversation, extracted {len(result.get('results', []))} memories:")
for i, mem in enumerate(result.get('results', []), 1):
    print(f"  {i}. {mem.get('memory', '')}")
```

**Run this code:**
```bash
python intelligent_memory_example.py
```

**Expected output:**
```
✓ Processed conversation, extracted 3 memories:
  1. Name is Alice
  2. Is a software engineer at Google
  3. Loves Python programming and machine learning
```

## Step 2: Duplicate Detection

Intelligent memory automatically detects duplicates:

```python
# intelligent_memory_example.py
from powermem import create_memory

memory = create_memory()
user_id = "user_001"

# First addition
print("1. Adding initial memory...")
result1 = memory.add(
    messages=[
        {"role": "user", "content": "I'm Alice, a software engineer"},
        {"role": "assistant", "content": "I remember that!"}
    ],
    user_id=user_id,
    infer=True
)
print(f"   Added {len(result1.get('results', []))} memories")

# Try to add duplicate
print("\n2. Attempting to add duplicate...")
result2 = memory.add(
    messages=[
        {"role": "user", "content": "I'm Alice, a software engineer"},
        {"role": "assistant", "content": "I know!"}
    ],
    user_id=user_id,
    infer=True
)

results = result2.get('results', [])
if results:
    event = results[0].get('event', 'N/A')
    print(f"   Event: {event}")
    if event == 'NONE':
        print("   ✓ Duplicate detected, no new memory created")
else:
    print("   ✓ Duplicate detected, skipped")
```

**Run this code:**
```bash
python intelligent_memory_example.py
```

**Expected output:**
```
1. Adding initial memory...
   Added 2 memories

2. Attempting to add duplicate...
   Event: NONE
   ✓ Duplicate detected, no new memory created
```

## Step 3: Information Updates

When information changes, memories are automatically updated:

```python
# intelligent_memory_example.py
from powermem import create_memory

memory = create_memory()
user_id = "user_001"

# Initial information
print("1. Adding initial information...")
memory.add(
    messages=[
        {"role": "user", "content": "I work at Google as a software engineer"}
    ],
    user_id=user_id,
    infer=True
)

# Information update
print("\n2. Updating information...")
result = memory.add(
    messages=[
        {"role": "user", "content": "I recently moved to Meta as a senior ML engineer"}
    ],
    user_id=user_id,
    infer=True
)

print("\n3. Checking results...")
for mem in result.get('results', []):
    event = mem.get('event', 'N/A')
    print(f"   Event: {event}")
    if event == 'UPDATE':
        print(f"   Updated memory:")
        print(f"     Old: {mem.get('previous_memory', 'N/A')}")
        print(f"     New: {mem.get('memory', 'N/A')}")
```

**Run this code:**
```bash
python intelligent_memory_example.py
```

**Expected output:**
```
1. Adding initial information...
2. Updating information...
3. Checking results...
   Event: UPDATE
   Updated memory:
     Old: Works at Google as a software engineer
     New: Works at Meta as a senior ML engineer
```

## Step 4: Adding New Information

New, non-conflicting information is added normally:

```python
# intelligent_memory_example.py
from powermem import create_memory

memory = create_memory()
user_id = "user_001"

# Add existing memories
memory.add(
    messages=[
        {"role": "user", "content": "I'm Alice, a software engineer"}
    ],
    user_id=user_id,
    infer=True
)

# Add new information
print("Adding new information...")
result = memory.add(
    messages=[
        {"role": "user", "content": "I like to drink coffee every morning and I have two cats."},
        {"role": "assistant", "content": "That's nice! What are your cats' names?"},
        {"role": "user", "content": "Their names are Fluffy and Whiskers."}
    ],
    user_id=user_id,
    infer=True
)

print(f"\n✓ Added {len(result.get('results', []))} new memories:")
for mem in result.get('results', []):
    event = mem.get('event', 'N/A')
    print(f"  [{event}] {mem.get('memory', '')}")
```

**Run this code:**
```bash
python intelligent_memory_example.py
```

**Expected output:**
```
Adding new information...

✓ Added 3 new memories:
  [ADD] Likes to drink coffee every morning
  [ADD] Has two cats
  [ADD] Cats named Fluffy and Whiskers
```

## Step 5: Conflict Resolution

When contradictory information is detected, the system resolves conflicts:

```python
# intelligent_memory_example.py
from powermem import create_memory

memory = create_memory()
user_id = "user_001"

# Add initial preference
print("1. Adding initial preference...")
memory.add(
    messages=[
        {"role": "user", "content": "I like to drink coffee every morning"}
    ],
    user_id=user_id,
    infer=True
)

# Contradictory information
print("\n2. Adding contradictory information...")
result = memory.add(
    messages=[
        {"role": "user", "content": "Actually, I don't like coffee anymore. I prefer tea now."}
    ],
    user_id=user_id,
    infer=True
)

print("\n3. Conflict resolution results:")
for mem in result.get('results', []):
    event = mem.get('event', 'N/A')
    print(f"   Event: {event}")
    if event == 'DELETE':
        print(f"     Deleted: {mem.get('memory', 'N/A')}")
    elif event == 'ADD':
        print(f"     Added: {mem.get('memory', 'N/A')}")
```

**Run this code:**
```bash
python intelligent_memory_example.py
```

**Expected output:**
```
1. Adding initial preference...
2. Adding contradictory information...
3. Conflict resolution results:
   Event: DELETE
     Deleted: Likes to drink coffee every morning
   Event: ADD
     Added: Prefers tea instead of coffee
```

## Step 6: Memory Consolidation

Related memories are consolidated:

```python
# intelligent_memory_example.py
from powermem import create_memory

memory = create_memory()
user_id = "user_001"

# Initial memory
print("1. Adding initial memory...")
memory.add(
    messages=[
        {"role": "user", "content": "I love Python programming"}
    ],
    user_id=user_id,
    infer=True
)

# More detailed information
print("\n2. Adding more detailed information...")
result = memory.add(
    messages=[
        {"role": "user", "content": "I love Python, especially for deep learning. I use TensorFlow and PyTorch a lot."}
    ],
    user_id=user_id,
    infer=True
)

print("\n3. Consolidation results:")
for mem in result.get('results', []):
    event = mem.get('event', 'N/A')
    if event == 'UPDATE':
        print(f"   Updated memory:")
        print(f"     Old: {mem.get('previous_memory', 'N/A')}")
        print(f"     New: {mem.get('memory', 'N/A')}")
    else:
        print(f"   [{event}] {mem.get('memory', '')}")
```

**Run this code:**
```bash
python intelligent_memory_example.py
```

**Expected output:**
```
1. Adding initial memory...
2. Adding more detailed information...
3. Consolidation results:
   Updated memory:
     Old: Loves Python programming
     New: Loves Python programming, especially for deep learning using TensorFlow and PyTorch
```

## Complete Example

Here's a complete example demonstrating all intelligent features:

```python
# complete_intelligent_example.py
from powermem import create_memory

def main():
    memory = create_memory()
    user_id = "demo_user"
    
    print("=" * 80)
    print("Intelligent Memory Demo")
    print("=" * 80)
    
    # Scenario 1: Initial addition
    print("\n[Scenario 1] Initial Memory Addition")
    print("-" * 60)
    result = memory.add(
        messages=[
            {"role": "user", "content": "Hi, my name is Alice. I'm a software engineer at Google."},
            {"role": "assistant", "content": "Nice to meet you, Alice!"},
            {"role": "user", "content": "I love Python programming and machine learning."}
        ],
        user_id=user_id,
        infer=True
    )
    print(f"✓ Extracted {len(result.get('results', []))} memories")
    
    # Scenario 2: Duplicate detection
    print("\n[Scenario 2] Duplicate Detection")
    print("-" * 60)
    result = memory.add(
        messages=[
            {"role": "user", "content": "I'm Alice, a software engineer"}
        ],
        user_id=user_id,
        infer=True
    )
    if result.get('results', []):
        if result['results'][0].get('event') == 'NONE':
            print("✓ Duplicate detected, skipped")
    
    # Scenario 3: Information update
    print("\n[Scenario 3] Information Update")
    print("-" * 60)
    result = memory.add(
        messages=[
            {"role": "user", "content": "I recently moved to Meta as a senior ML engineer"}
        ],
        user_id=user_id,
        infer=True
    )
    for mem in result.get('results', []):
        if mem.get('event') == 'UPDATE':
            print(f"✓ Updated: {mem.get('previous_memory')} → {mem.get('memory')}")
    
    # Scenario 4: New information
    print("\n[Scenario 4] Adding New Information")
    print("-" * 60)
    result = memory.add(
        messages=[
            {"role": "user", "content": "I like to drink coffee every morning and I have two cats."}
        ],
        user_id=user_id,
        infer=True
    )
    print(f"✓ Added {len(result.get('results', []))} new memories")
    
    # Scenario 5: Conflict resolution
    print("\n[Scenario 5] Conflict Resolution")
    print("-" * 60)
    result = memory.add(
        messages=[
            {"role": "user", "content": "Actually, I prefer tea instead of coffee now."}
        ],
        user_id=user_id,
        infer=True
    )
    for mem in result.get('results', []):
        event = mem.get('event', '')
        if event == 'DELETE':
            print(f"✓ Deleted conflicting memory")
        elif event == 'ADD':
            print(f"✓ Added new preference")
    
    # Final summary
    print("\n" + "=" * 80)
    print("Final Memory Summary")
    print("=" * 80)
    all_memories = memory.get_all(user_id=user_id)
    print(f"\nTotal memories: {len(all_memories.get('results', []))}")
    for i, mem in enumerate(all_memories.get('results', []), 1):
        print(f"  {i}. {mem.get('memory', '')}")
    
    print("\n" + "=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
```

**Run this code:**
```bash
python complete_intelligent_example.py
```

## Extension Exercises

### Exercise 1: Compare Simple vs Intelligent Mode

Compare adding memories with and without intelligent processing:

```python
from powermem import create_memory

memory = create_memory()

# Simple mode
print("1. Simple mode (infer=False):")
result1 = memory.add("User likes Python", user_id="user123", infer=False)
print(f"   Added memory directly: {result1.get('results', [{}])[0].get('memory', 'N/A')}")

# Intelligent mode
print("\n2. Intelligent mode (infer=True):")
result2 = memory.add(
    messages=[{"role": "user", "content": "I like Python programming"}],
    user_id="user123",
    infer=True
)

print("   Extracted memories:")
for mem in result2.get('results', []):
    event = mem.get('event', 'N/A')
    memory_text = mem.get('memory', '')
    print(f"   - [{event}] {memory_text}")
    
print("\n✓ Comparison completed. Intelligent mode extracts facts automatically!")
```

### Exercise 2: Track Memory Events

Monitor different memory operations:

```python
from powermem import create_memory

memory = create_memory()

# Example: Add memory and check the event type
result = memory.add(
    messages=[
        {"role": "user", "content": "I love working with machine learning"}
    ],
    user_id="user123",
    infer=True
)

print("Processing results:")
for mem in result.get('results', []):
    event = mem.get('event')
    if event == 'ADD':
        print(f"✓ New memory added: {mem.get('memory', '')}")
    elif event == 'UPDATE':
        print(f"✓ Memory updated: {mem.get('previous_memory', '')} → {mem.get('memory', '')}")
    elif event == 'DELETE':
        print(f"✓ Memory deleted: {mem.get('memory', '')}")
    elif event == 'NONE':
        print("✓ Duplicate detected, skipped")
```

### Exercise 3: Complex Conversations

Process longer conversations:

```python
from powermem import create_memory

memory = create_memory()

# Long conversation with multiple facts
long_conversation = [
    {"role": "user", "content": "I'm Alice, a software engineer at Google."},
    {"role": "assistant", "content": "Nice to meet you!"},
    {"role": "user", "content": "I work on machine learning projects."},
    {"role": "assistant", "content": "That's interesting!"},
    {"role": "user", "content": "I use Python, TensorFlow, and PyTorch."},
]

print("Processing long conversation...")
result = memory.add(
    messages=long_conversation,
    user_id="user123",
    infer=True
)

print(f"\n✓ Extracted {len(result.get('results', []))} memories:")
for i, mem in enumerate(result.get('results', []), 1):
    event = mem.get('event', 'N/A')
    memory_text = mem.get('memory', '')
    print(f"  {i}. [{event}] {memory_text}")
```

## Next Steps

- **Scenario 3**: Explore multi-agent scenarios
- **Scenario 4**: Learn async operations
- **Architecture**: See [Intelligent Features](../architecture/intelligent_features.md)

