from typing import Optional

from pydantic import Field

from powermem.storage.config.base import BaseVectorStoreConfig


class SQLiteConfig(BaseVectorStoreConfig):
    """Configuration for SQLite vector store."""
    
    database_path: str = Field(
        default="./data/powermem_dev.db",
        description="Path to SQLite database file"
    )
    collection_name: str = Field(
        default="memories",
        description="Name of the collection/table"
    )
    enable_wal: bool = Field(
        default=True,
        description="Enable Write-Ahead Logging for better concurrency"
    )
    timeout: int = Field(
        default=30,
        description="Connection timeout in seconds"
    )

