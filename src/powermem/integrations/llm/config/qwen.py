from typing import Any, Callable, Optional

from powermem.integrations.llm.config.base import BaseLLMConfig


class QwenConfig(BaseLLMConfig):
    """
    Configuration class for Qwen-specific parameters.
    Inherits from BaseLLMConfig and adds Qwen-specific settings.
    """

    def __init__(
            self,
            # Base parameters
            model: Optional[str] = None,
            temperature: float = 0.1,
            api_key: Optional[str] = None,
            max_tokens: int = 2000,
            top_p: float = 0.1,
            top_k: int = 1,
            enable_vision: bool = False,
            vision_details: Optional[str] = "auto",
            http_client_proxies: Optional[dict] = None,
            # Qwen-specific parameters
            dashscope_base_url: Optional[str] = None,
            enable_search: bool = False,
            search_params: Optional[dict] = None,
            # Response monitoring callback
            response_callback: Optional[Callable[[Any, dict, dict], None]] = None,
    ):
        """
        Initialize Qwen configuration.

        Args:
            model: Qwen model to use, defaults to None
            temperature: Controls randomness, defaults to 0.1
            api_key: DashScope API key, defaults to None
            max_tokens: Maximum tokens to generate, defaults to 2000
            top_p: Nucleus sampling parameter, defaults to 0.1
            top_k: Top-k sampling parameter, defaults to 1
            enable_vision: Enable vision capabilities, defaults to False
            vision_details: Vision detail level, defaults to "auto"
            http_client_proxies: HTTP client proxy settings, defaults to None
            dashscope_base_url: DashScope API base URL, defaults to None
            enable_search: Enable web search capability, defaults to False
            search_params: Parameters for web search, defaults to None
            response_callback: Optional callback for monitoring LLM responses.
        """
        # Initialize base parameters
        super().__init__(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=max_tokens,
            top_p=top_p,
            top_k=top_k,
            enable_vision=enable_vision,
            vision_details=vision_details,
            http_client_proxies=http_client_proxies,
        )

        # Qwen-specific parameters
        self.dashscope_base_url = dashscope_base_url
        self.enable_search = enable_search
        self.search_params = search_params or {}

        # Response monitoring
        self.response_callback = response_callback
