# Integrations Guide

Guide to integrating powermem with various frameworks and services.

## LangChain Integration

### Basic Integration

```python
from langchain.memory import ConversationBufferMemory
from powermem import Memory, auto_config

# Create powermem instance
config = auto_config()
powermem = Memory(config=config)

# Use with LangChain
class PowermemMemory(ConversationBufferMemory):
    def __init__(self, powermem_instance, user_id, **kwargs):
        super().__init__(**kwargs)
        self.powermem = powermem_instance
        self.user_id = user_id
    
    def save_context(self, inputs, outputs):
        super().save_context(inputs, outputs)
        
        # Save to powermem
        messages = [
            {"role": "user", "content": str(inputs)},
            {"role": "assistant", "content": str(outputs)}
        ]
        self.powermem.add(
            messages=messages,
            user_id=self.user_id,
            infer=True
        )
    
    def load_memory_variables(self, inputs):
        # Load from powermem
        query = str(inputs)
        results = self.powermem.search(
            query=query,
            user_id=self.user_id,
            limit=5
        )
        
        # Format for LangChain
        memory_variables = {
            "history": "\n".join([
                result['memory'] for result in results.get('results', [])
            ])
        }
        
        return memory_variables
```

### Usage with LangChain

```python
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

llm = OpenAI()
memory = PowermemMemory(powermem, user_id="user123")

chain = ConversationChain(
    llm=llm,
    memory=memory
)

chain.run("Hello, I'm Alice")
```

## FastAPI Integration

### Creating API Endpoints

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from powermem import Memory, auto_config

app = FastAPI()
config = auto_config()
memory = Memory(config=config)

class MemoryRequest(BaseModel):
    memory: str
    user_id: str
    metadata: dict = {}

class SearchRequest(BaseModel):
    query: str
    user_id: str
    limit: int = 10

@app.post("/memories")
async def add_memory(request: MemoryRequest):
    try:
        result = memory.add(
            messages=request.memory,
            user_id=request.user_id,
            metadata=request.metadata
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memories/search")
async def search_memories(request: SearchRequest):
    try:
        results = memory.search(
            query=request.query,
            user_id=request.user_id,
            limit=request.limit
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Async Integration

### Using with Async Frameworks

```python
from powermem import AsyncMemory, auto_config
import asyncio

async def async_example():
    config = auto_config()
    async_memory = AsyncMemory(config=config)
    await async_memory.initialize()
    
    # Add memory
    await async_memory.add(
        messages="User preference",
        user_id="user123"
    )
    
    # Search
    results = await async_memory.search(
        query="preferences",
        user_id="user123"
    )
    
    return results

# Run async
results = asyncio.run(async_example())
```

## Custom LLM Integration

### Implementing Custom LLM Provider

```python
from powermem.integrations.llm.base import LLMBase

class CustomLLM(LLMBase):
    def __init__(self, config):
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'default')
    
    def generate(self, prompt, **kwargs):
        # Your custom LLM implementation
        response = your_llm_client.generate(
            prompt=prompt,
            model=self.model,
            api_key=self.api_key
        )
        return response
    
    def extract_facts(self, messages):
        # Custom fact extraction logic
        facts = your_custom_extractor(messages)
        return facts
```

## Custom Embedding Integration

### Implementing Custom Embedder

```python
from powermem.integrations.embeddings.base import EmbedderBase

class CustomEmbedder(EmbedderBase):
    def __init__(self, config):
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'default')
    
    def embed(self, text):
        # Your custom embedding implementation
        embedding = your_embedding_client.embed(
            text=text,
            model=self.model,
            api_key=self.api_key
        )
        return embedding
    
    def embed_batch(self, texts):
        # Batch embedding
        embeddings = []
        for text in texts:
            embeddings.append(self.embed(text))
        return embeddings
```

## Custom Storage Integration

### Implementing Custom Vector Store

```python
from powermem.storage.base import VectorStoreBase

class CustomVectorStore(VectorStoreBase):
    def __init__(self, config):
        self.connection = your_database_connect(config)
    
    def add(self, memory, embedding, metadata):
        # Your custom storage implementation
        self.connection.insert({
            'memory': memory,
            'embedding': embedding,
            'metadata': metadata
        })
    
    def search(self, query_embedding, limit, filters):
        # Your custom search implementation
        results = self.connection.similarity_search(
            query_embedding=query_embedding,
            limit=limit,
            filters=filters
        )
        return results
```

## OpenAI Integration

### Using OpenAI Models

```env
LLM_PROVIDER=openai
LLM_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4
EMBEDDING_PROVIDER=openai
EMBEDDING_API_KEY=your_openai_api_key
EMBEDDING_MODEL=text-embedding-3-large
```

```python
from powermem import create_memory

memory = create_memory()  # Auto-loads OpenAI config from .env
```

## Anthropic Integration

### Using Claude Models

```env
LLM_PROVIDER=anthropic
LLM_API_KEY=your_anthropic_api_key
LLM_MODEL=claude-3-opus-20240229
```

```python
from powermem import create_memory

memory = create_memory()  # Auto-loads Anthropic config
```

## Qwen Integration

### Using Qwen Models

```env
LLM_PROVIDER=qwen
LLM_API_KEY=your_dashscope_api_key
LLM_MODEL=qwen-plus
EMBEDDING_PROVIDER=qwen
EMBEDDING_API_KEY=your_dashscope_api_key
EMBEDDING_MODEL=text-embedding-v4
```

```python
from powermem import create_memory

memory = create_memory()  # Auto-loads Qwen config
```

## Best Practices

1. **Use environment variables**: Keep API keys in .env files
2. **Error handling**: Always handle exceptions in integrations
3. **Async for scale**: Use AsyncMemory for high-throughput scenarios
4. **Custom providers**: Implement custom providers when needed
5. **Testing**: Test integrations thoroughly

## See Also

- [Getting Started Guide](getting_started.md)
- [Configuration Guide](configuration.md)
- [API Reference](../api/)

