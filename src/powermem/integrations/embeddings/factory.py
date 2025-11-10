"""
Embedding factory for creating embedding instances

This module provides a factory for creating different embedding instances.
"""

import importlib
from typing import Optional

from powermem.integrations.embeddings.config.base import BaseEmbedderConfig
from powermem.integrations.embeddings.mock import MockEmbeddings


def load_class(class_type):
    module_path, class_name = class_type.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class EmbedderFactory:
    provider_to_class = {
        "openai": "powermem.integrations.embeddings.openai.OpenAIEmbedding",
        "ollama": "powermem.integrations.embeddings.ollama.OllamaEmbedding",
        "huggingface": "powermem.integrations.embeddings.huggingface.HuggingFaceEmbedding",
        "azure_openai": "powermem.integrations.embeddings.azure_openai.AzureOpenAIEmbedding",
        "gemini": "powermem.integrations.embeddings.gemini.GoogleGenAIEmbedding",
        "vertexai": "powermem.integrations.embeddings.vertexai.VertexAIEmbedding",
        "together": "powermem.integrations.embeddings.together.TogetherEmbedding",
        "lmstudio": "powermem.integrations.embeddings.lmstudio.LMStudioEmbedding",
        "langchain": "powermem.integrations.embeddings.langchain.LangchainEmbedding",
        "aws_bedrock": "powermem.integrations.embeddings.aws_bedrock.AWSBedrockEmbedding",
        "qwen": "powermem.integrations.embeddings.qwen.QwenEmbedding",
    }

    @classmethod
    def create(cls, provider_name, config, vector_config: Optional[dict]):
        # Handle mock provider directly
        if provider_name == "mock":
            return MockEmbeddings()
        if provider_name == "upstash_vector" and vector_config and vector_config.enable_embeddings:
            return MockEmbeddings()
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            embedder_instance = load_class(class_type)
            base_config = BaseEmbedderConfig(**config)
            return embedder_instance(base_config)
        else:
            raise ValueError(f"Unsupported Embedder provider: {provider_name}")
