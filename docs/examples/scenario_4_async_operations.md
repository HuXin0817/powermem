# Scenario 4: Async Operations

This scenario demonstrates how to use powermem's async operations for high-performance, concurrent memory operations.

## Prerequisites

- Completed Scenario 1
- Understanding of async/await in Python
- powermem installed

## Understanding Async Operations

Async operations enable:
- Non-blocking memory operations
- Concurrent processing
- High-throughput scenarios
- Better performance for I/O-bound operations

## Step 1: Initialize Async Memory

First, let's create and initialize an AsyncMemory instance:

```python
# async_operations_example.py
import asyncio
from powermem import AsyncMemory, auto_config

async def main():
    config = auto_config()
    
    # Create async memory instance
    async_memory = AsyncMemory(config=config)
    
    # Initialize (required for async)
    await async_memory.initialize()
    
    print("✓ AsyncMemory initialized successfully!")

# Run async function
asyncio.run(main())
```

**Run this code:**
```bash
python async_operations_example.py
```

**Expected output:**
```
✓ AsyncMemory initialized successfully!
```

## Step 2: Add Memories Asynchronously

Add memories using async methods:

```python
# async_operations_example.py
import asyncio
from powermem import AsyncMemory, auto_config

async def main():
    config = auto_config()
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    # Add memory asynchronously
    result = await async_memory.add(
        "User likes Python programming",  # messages parameter (first positional argument)
        user_id="user123"
    )
    
    # Handle result - check if results list is not empty
    results_list = result.get('results', [])
    if results_list:
        memory_id = results_list[0].get('id', 'N/A')
        print(f"✓ Memory added! ID: {memory_id}")
    else:
        print("✓ Memory operation completed (may have been deduplicated)")

asyncio.run(main())
```

**Run this code:**
```bash
python async_operations_example.py
```

**Expected output:**
```
✓ Memory added! ID: mem_xxx
```

## Step 3: Concurrent Memory Operations

Add multiple memories concurrently:

```python
# async_operations_example.py
import asyncio
from powermem import AsyncMemory, auto_config

async def main():
    config = auto_config()
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    # Add multiple memories concurrently
    memories = [
        "User likes Python programming",
        "User prefers email support",
        "User works as a software engineer",
        "User favorite color is blue"
    ]
    
    # Create tasks for concurrent execution
    tasks = [
        async_memory.add(mem, user_id="user123")  # messages as first positional argument
        for mem in memories
    ]
    
    # Execute all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    print(f"✓ Added {len(results)} memories concurrently")

asyncio.run(main())
```

**Run this code:**
```bash
python async_operations_example.py
```

**Expected output:**
```
✓ Added 4 memories concurrently
```

## Step 4: Async Search

Search memories asynchronously:

```python
# async_operations_example.py
import asyncio
from powermem import AsyncMemory, auto_config

async def main():
    config = auto_config()
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    # Add some memories first
    await async_memory.add("User likes Python", user_id="user123")
    await async_memory.add("User prefers email", user_id="user123")
    
    # Search asynchronously
    results = await async_memory.search(
        query="user preferences",
        user_id="user123",
        limit=5
    )
    
    print(f"Found {len(results.get('results', []))} memories:")
    for result in results.get('results', []):
        print(f"  - {result['memory']}")

asyncio.run(main())
```

**Run this code:**
```bash
python async_operations_example.py
```

**Expected output:**
```
Found 2 memories:
  - User prefers email
  - User likes Python
```

## Step 5: Batch Processing

Process memories in batches:

```python
# async_operations_example.py
import asyncio
from powermem import AsyncMemory, auto_config

async def main():
    config = auto_config()
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    # Large list of memories
    memories = [
        f"Memory {i}: User preference {i}"
        for i in range(100)
    ]
    
    # Process in batches
    batch_size = 10
    for i in range(0, len(memories), batch_size):
        batch = memories[i:i+batch_size]
        
        # Create tasks for batch
        tasks = [
            async_memory.add(mem, user_id="user123")  # messages as first positional argument
            for mem in batch
        ]
        
        # Execute batch concurrently
        await asyncio.gather(*tasks)
        
        print(f"✓ Processed batch {i//batch_size + 1}")

asyncio.run(main())
```

**Run this code:**
```bash
python async_operations_example.py
```

**Expected output:**
```
✓ Processed batch 1
✓ Processed batch 2
✓ Processed batch 3
...
```

## Step 6: Async with Intelligent Memory

Use async operations with intelligent memory features:

```python
# async_operations_example.py
import asyncio
from powermem import AsyncMemory, auto_config

async def main():
    config = auto_config()
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    # Add memory with intelligent processing
    result = await async_memory.add(
        messages=[
            {"role": "user", "content": "I'm Alice, a software engineer"},
            {"role": "assistant", "content": "Nice to meet you!"}
        ],
        user_id="user123",
        infer=True  # Enable intelligent fact extraction
    )
    
    print(f"✓ Processed conversation, extracted {len(result.get('results', []))} memories:")
    for mem in result.get('results', []):
        print(f"  - {mem.get('memory', '')}")

asyncio.run(main())
```

**Run this code:**
```bash
python async_operations_example.py
```

**Expected output:**
```
✓ Processed conversation, extracted 1 memories:
  - Is Alice, a software engineer
```

## Step 7: Async Update and Delete

Update and delete memories asynchronously:

```python
# async_operations_example.py
import asyncio
from powermem import AsyncMemory, auto_config

async def main():
    config = auto_config()
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    # Add memory (using infer=False to ensure it's added for demo purposes)
    # In production, you might want infer=True for intelligent deduplication
    result = await async_memory.add(
        "User likes Python",  # messages as first positional argument
        user_id="user123",
        infer=False  # Disable intelligent deduplication for demo
    )
    
    # Handle result - check if results list is not empty
    results_list = result.get('results', [])
    if not results_list:
        print("Error: No memory was added")
        raise ValueError("Cannot update/delete: memory was not added")
    
    memory_id = results_list[0].get('id')
    if not memory_id:
        print("Error: Memory ID not found in result")
        raise ValueError("Cannot update/delete: memory ID not found")
    
    # Update memory
    updated = await async_memory.update(
        memory_id=memory_id,
        content="User loves Python programming"
    )
    print(f"✓ Updated memory: {updated.get('memory', 'N/A')}")
    
    # Delete memory
    success = await async_memory.delete(memory_id)
    if success:
        print(f"✓ Deleted memory {memory_id}")

asyncio.run(main())
```

**Run this code:**
```bash
python async_operations_example.py
```

**Expected output:**
```
✓ Updated memory: User loves Python programming
✓ Deleted memory mem_xxx
```

## Step 8: FastAPI Integration Example

Use async memory in FastAPI:

```python
# fastapi_example.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from powermem import AsyncMemory, auto_config

config = auto_config()
async_memory = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize async memory
    global async_memory
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    yield
    # Shutdown: cleanup (if needed)
    # async_memory cleanup can be added here if needed

app = FastAPI(lifespan=lifespan)

class MemoryRequest(BaseModel):
    memory: str
    user_id: str

@app.post("/memories")
async def add_memory(request: MemoryRequest):
    try:
        result = await async_memory.add(
            request.memory,  # messages as first positional argument
            user_id=request.user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memories/search")
async def search_memories(query: str, user_id: str):
    try:
        results = await async_memory.search(
            query=query,
            user_id=user_id
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Complete Example

Here's a complete async example:

```python
# complete_async_example.py
import asyncio
from powermem import AsyncMemory, auto_config

async def main():
    config = auto_config()
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    print("=" * 80)
    print("Async Memory Operations Demo")
    print("=" * 80)
    
    # Step 1: Add memories concurrently
    print("\n[Step 1] Adding Memories Concurrently")
    print("-" * 60)
    
    memories = [
        "User likes Python programming",
        "User prefers email support",
        "User works as a software engineer"
    ]
    
    tasks = [
        async_memory.add(mem, user_id="user123")  # messages as first positional argument
        for mem in memories
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"✓ Added {len(results)} memories concurrently")
    
    # Step 2: Search asynchronously
    print("\n[Step 2] Searching Memories")
    print("-" * 60)
    
    search_results = await async_memory.search(
        query="user preferences",
        user_id="user123"
    )
    
    print(f"Found {len(search_results.get('results', []))} memories:")
    for result in search_results.get('results', []):
        print(f"  - {result['memory']}")
    
    # Step 3: Batch processing
    print("\n[Step 3] Batch Processing")
    print("-" * 60)
    
    batch_memories = [f"Memory {i}" for i in range(20)]
    batch_size = 5
    
    for i in range(0, len(batch_memories), batch_size):
        batch = batch_memories[i:i+batch_size]
        tasks = [
            async_memory.add(mem, user_id="user123")  # messages as first positional argument
            for mem in batch
        ]
        await asyncio.gather(*tasks)
        print(f"✓ Processed batch {i//batch_size + 1}")
    
    print("\n" + "=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
```

**Run this code:**
```bash
python complete_async_example.py
```

## Extension Exercises

### Exercise 1: Concurrent Searches

Perform multiple searches concurrently:

```python
async def concurrent_searches():
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    queries = [
        "user preferences",
        "user interests",
        "user information"
    ]
    
    tasks = [
        async_memory.search(query=q, user_id="user123")
        for q in queries
    ]
    
    results = await asyncio.gather(*tasks)
    return results
```

### Exercise 2: Async with Error Handling

Add error handling to async operations:

```python
async def safe_add(memory, user_id):
    try:
        result = await async_memory.add(memory, user_id=user_id)  # messages as first positional argument
        return result
    except Exception as e:
        print(f"Error adding memory: {e}")
        return None
```

### Exercise 3: Rate Limiting

Implement rate limiting for async operations:

```python
import asyncio

async def rate_limited_add(memories, user_id, rate=5):
    semaphore = asyncio.Semaphore(rate)
    
    async def add_with_limit(memory):
        async with semaphore:
            return await async_memory.add(memory, user_id=user_id)  # messages as first positional argument
    
    tasks = [add_with_limit(mem) for mem in memories]
    return await asyncio.gather(*tasks)
```

## When to Use Async

Use `AsyncMemory` when:
- Processing many memories concurrently
- Building async web applications (FastAPI, aiohttp)
- Implementing batch processing pipelines
- Need non-blocking operations

Use `Memory` when:
- Simple synchronous scripts
- Interactive notebooks
- Simple use cases without concurrency

## Next Steps

- **Scenario 5**: Learn custom integrations
- **AsyncMemory API**: See [AsyncMemory API](../api/async_memory.md)
- **Integrations Guide**: Check [Integrations Guide](../guides/integrations.md)

