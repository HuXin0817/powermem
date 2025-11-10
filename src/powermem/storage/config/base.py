from abc import ABC
from typing import Any, Dict

from pydantic import BaseModel, model_validator


class BaseVectorStoreConfig(BaseModel, ABC):
    """
    Base configuration class for all vector store providers.
    
    This class provides common validation logic that is shared
    across all vector store implementations.
    """
    
    @model_validator(mode="before")
    @classmethod
    def validate_extra_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that no extra fields are provided beyond what's defined in the model.
        
        This is a common validation pattern across all vector store configs.
        """
        allowed_fields = set(cls.model_fields.keys())
        input_fields = set(values.keys())
        extra_fields = input_fields - allowed_fields
        
        if extra_fields:
            raise ValueError(
                f"Extra fields not allowed: {', '.join(extra_fields)}. "
                f"Please input only the following fields: {', '.join(allowed_fields)}"
            )
        return values
