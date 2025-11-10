import logging
import os
from typing import Any, Dict, List, Optional
import asyncio
from dotenv import load_dotenv
import sys

load_dotenv()


class AsyncTokenTracker:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.cached_tokens = 0
        self._lock = asyncio.Lock()

    async def track_token(self, usage):
        """Asynchronously update token count"""
        async with self._lock:
            self.prompt_tokens += usage.prompt_tokens
            self.completion_tokens += usage.completion_tokens
            self.total_tokens += usage.total_tokens
            if hasattr(usage, 'prompt_tokens_details') and usage.prompt_tokens_details:
                if hasattr(usage.prompt_tokens_details, 'cached_tokens'):
                    self.cached_tokens += usage.prompt_tokens_details.cached_tokens

    def get_token_count(self):
        return self.total_tokens

    def get_detailed_stats(self):
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "cached_tokens": self.cached_tokens
        }

    def reset(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.cached_tokens = 0


async_token_tracker = AsyncTokenTracker()


def get_token_count():
    return async_token_tracker.get_token_count()


# Read token statistics configuration from environment variables
TOKEN_COUNTING = os.getenv("TOKEN_COUNTING", "true").lower() in ("true", "1", "yes")
ENABLE_EXPLICIT_CACHE = os.getenv("ENABLE_EXPLICIT_CACHE", "false").lower() in ("true", "1", "yes")
ENABLE_PROMPT_OPTIMIZATION = os.getenv("ENABLE_PROMPT_OPTIMIZATION", "false").lower() in ("true", "1", "yes")
if TOKEN_COUNTING:
    print("Token counting enabled")
    import sys
    from openai.resources.chat.completions.completions import Completions
    import openai.resources.chat.chat


    class CountCompletions(Completions):
        def _safe_async_track_token(self, token_count):
            """Thread-safe async token tracking"""
            import asyncio
            try:
                # Try to get current event loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If event loop is running, create task
                    asyncio.create_task(async_token_tracker.track_token(token_count))
                else:
                    # If event loop is not running, run directly
                    loop.run_until_complete(async_token_tracker.track_token(token_count))
            except RuntimeError:
                # If no event loop, create a new one
                asyncio.run(async_token_tracker.track_token(token_count))

        def _process_cache_control(self, messages):
            """
            Process cache control logic, supporting ephemeral cache type.

            Args:
                messages: Original message list

            Returns:
                Processed message list with cache control support
            """
            # Check if explicit cache is enabled
            if not ENABLE_EXPLICIT_CACHE:
                return messages

            processed_messages = []

            for message in messages:
                processed_message = message.copy()

                # Check if it's the last message and contains content array
                if (message.get("role") == "user" and
                        isinstance(message.get("content"), list) and
                        message == messages[-1]):

                    # Process cache control in content array
                    processed_content = []
                    for content_item in message["content"]:
                        if isinstance(content_item, dict):
                            processed_item = content_item.copy()

                            # Check if cache_control is included
                            if "cache_control" in processed_item:
                                cache_control = processed_item["cache_control"]
                                if cache_control.get("type") == "ephemeral":
                                    # Set special marker for ephemeral cache
                                    processed_item["cache_control"] = cache_control

                            processed_content.append(processed_item)
                        else:
                            processed_content.append(content_item)

                    processed_message["content"] = processed_content

                processed_messages.append(processed_message)

            return processed_messages

        def create(self, *args, **kwargs):
            # Process cache control logic before sending request
            if 'messages' in kwargs:
                kwargs['messages'] = self._process_cache_control(kwargs['messages'])

            resp = super().create(*args, **kwargs)
            if hasattr(resp, 'usage') and resp.usage:
                # Use thread-safe async solution
                # print(resp.usage)
                self._safe_async_track_token(resp.usage)
            return resp


    module = sys.modules['openai.resources.chat.chat']
    setattr(module, 'Completions', CountCompletions)


from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field
from powermem import Memory

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
EMBEDDER_MODEL_BASE_URL = os.getenv("EMBEDDER_MODEL_BASE_URL", OPENAI_BASE_URL)
EMBEDDER_MODEL = os.getenv("EMBEDDER_MODEL", "text-embedding-3-small")
DB_TYPE= os.getenv("db_type", "oceanbase")
VECTOR_WEIGHT = os.getenv("VECTOR_WEIGHT", "0.5")
FTS_WEIGHT = os.getenv("FTS_WEIGHT", "0.5")
vector_store=None
if DB_TYPE == "oceanbase":
    vector_store={
        "provider": "oceanbase",
        "config": {
            "host": "127.0.0.1",
            "port": "2881",
            "user": "root",
            "password": "******",
            "db_name": "ai_work",
            "collection_name": "powermem_collection",
            "embedding_model_dims": 1536,
            "index_type": "HNSW",
            "vidx_metric_type": "l2",
            "vector_weight": float(VECTOR_WEIGHT),
            "fts_weight": float(FTS_WEIGHT),
        },
    }
elif DB_TYPE == "postgres":
    vector_store={
        "provider": "pgvector",
        "config": {
            "host": "127.0.0.1",
            "port": "5432",
            "user": "postgres",
            "password": "******",
            "dbname": "ai_work",
            "collection_name": "memories",
            "embedding_model_dims": 1536,
            "diskann": True,
            "hnsw": True,
        },
    }
DEFAULT_CONFIG = {
    "version": "v1.1",
    "vector_store": vector_store,
    "llm": {"provider": "openai",
            "config": {"openai_base_url": OPENAI_BASE_URL, "api_key": OPENAI_API_KEY, "temperature": 0.2,
                       "model": LLM_MODEL}},
    "embedder": {"provider": "openai",
                 "config": {"openai_base_url": EMBEDDER_MODEL_BASE_URL, "api_key": OPENAI_API_KEY, "model": EMBEDDER_MODEL,
                            "embedding_dims": 1536}},
    "history_db_path": "history.db",
}

MEMORY_INSTANCE = Memory.from_config(DEFAULT_CONFIG)

app = FastAPI(
    title="PowerMem REST APIs",
    description="A REST API for managing and searching memories for your AI Agents and Apps.",
    version="1.0.0",
)


class Message(BaseModel):
    role: str = Field(..., description="Role of the message (user or assistant).")
    content: str = Field(..., description="Message content.")


class MemoryCreate(BaseModel):
    messages: List[Message] = Field(..., description="List of messages to store.")
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    run_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query.")
    user_id: Optional[str] = None
    run_id: Optional[str] = None
    agent_id: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


@app.post("/configure", summary="Configure PowerMem")
def set_config(config: Dict[str, Any]):
    """Set memory configuration."""
    global MEMORY_INSTANCE
    MEMORY_INSTANCE = Memory.from_config(config)
    return {"message": "Configuration set successfully"}


@app.post("/memories", summary="Create memories")
def add_memory(memory_create: MemoryCreate):
    """Store new memories."""
    if not any([memory_create.user_id, memory_create.agent_id, memory_create.run_id]):
        raise HTTPException(status_code=400, detail="At least one identifier (user_id, agent_id, run_id) is required.")

    params = {k: v for k, v in memory_create.model_dump().items() if v is not None and k != "messages"}
    try:
        response = MEMORY_INSTANCE.add(messages=[m.model_dump() for m in memory_create.messages], **params)
        return JSONResponse(content=response)
    except Exception as e:
        logging.exception("Error in add_memory:")  # This will log the full traceback
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memories", summary="Get memories")
def get_all_memories(
        user_id: Optional[str] = None,
        run_id: Optional[str] = None,
        agent_id: Optional[str] = None,
):
    """Retrieve stored memories."""
    if not any([user_id, run_id, agent_id]):
        raise HTTPException(status_code=400, detail="At least one identifier is required.")
    try:
        params = {
            k: v for k, v in {"user_id": user_id, "run_id": run_id, "agent_id": agent_id}.items() if v is not None
        }
        return MEMORY_INSTANCE.get_all(**params)
    except Exception as e:
        logging.exception("Error in get_all_memories:")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memories/{memory_id}", summary="Get a memory")
def get_memory(memory_id: int):
    """Retrieve a specific memory by ID."""
    try:
        return MEMORY_INSTANCE.get(memory_id)
    except Exception as e:
        logging.exception("Error in get_memory:")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", summary="Search memories")
def search_memories(search_req: SearchRequest):
    """Search for memories based on a query."""
    try:
        params = {k: v for k, v in search_req.model_dump().items() if v is not None and k != "query"}
        return MEMORY_INSTANCE.search(query=search_req.query, **params)
    except Exception as e:
        logging.exception("Error in search_memories:")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/memories/{memory_id}", summary="Update a memory")
def update_memory(memory_id: int, updated_memory: Dict[str, Any]):
    """Update an existing memory with new content.

    Args:
        memory_id (int): ID of the memory to update
        updated_memory (str): New content to update the memory with

    Returns:
        dict: Success message indicating the memory was updated
    """
    try:
        return MEMORY_INSTANCE.update(memory_id=memory_id, data=updated_memory)
    except Exception as e:
        logging.exception("Error in update_memory:")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memories/{memory_id}/history", summary="Get memory history")
def memory_history(memory_id: int):
    """Retrieve memory history."""
    try:
        return MEMORY_INSTANCE.history(memory_id=memory_id)
    except Exception as e:
        logging.exception("Error in memory_history:")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/memories/{memory_id}", summary="Delete a memory")
def delete_memory(memory_id: int):
    """Delete a specific memory by ID."""
    try:
        MEMORY_INSTANCE.delete(memory_id=memory_id)
        return {"message": "Memory deleted successfully"}
    except Exception as e:
        logging.exception("Error in delete_memory:")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/memories", summary="Delete all memories")
def delete_all_memories(
        user_id: Optional[str] = None,
        run_id: Optional[str] = None,
        agent_id: Optional[str] = None,
):
    """Delete all memories for a given identifier."""
    if not any([user_id, run_id, agent_id]):
        raise HTTPException(status_code=400, detail="At least one identifier is required.")
    try:
        params = {
            k: v for k, v in {"user_id": user_id, "run_id": run_id, "agent_id": agent_id}.items() if v is not None
        }
        MEMORY_INSTANCE.delete_all(**params)
        return {"message": "All relevant memories deleted"}
    except Exception as e:
        logging.exception("Error in delete_all_memories:")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset", summary="Reset all memories")
def reset_memory():
    """Completely reset stored memories."""
    try:
        MEMORY_INSTANCE.reset()
        return {"message": "All memories reset"}
    except Exception as e:
        logging.exception("Error in reset_memory:")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", summary="Redirect to the OpenAPI documentation", include_in_schema=False)
def home():
    """Redirect to the OpenAPI documentation."""
    return RedirectResponse(url="/docs")


@app.get("/token_count", summary="Get token count")
def get_token_count_endpoint():
    """Get token count."""
    return {"token_count": async_token_tracker.get_detailed_stats()}


@app.post("/reset_token_count", summary="Reset token count")
def reset_token_count():
    """Reset token count."""
    async_token_tracker.reset()
    return {"message": "Token count reset"}