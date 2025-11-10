from typing import Optional

from pydantic import BaseModel, Field, field_validator


class LLMConfig(BaseModel):
    provider: str = Field(description="Provider of the LLM (e.g., 'ollama', 'openai')", default="openai")
    config: Optional[dict] = Field(description="Configuration for the specific LLM", default={})

    @field_validator("config")
    def validate_config(cls, v, info):
        provider = info.data.get("provider")
        if provider in (
            "openai",
            "ollama",
            "anthropic",
            "openai_structured",
            "gemini",
            "deepseek",
            "vllm",
            "langchain",
            "qwen",
        ):
            return v
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
