"""
Entry point for running the MCP server as a module.

Usage:
    python -m powermem.mcp
    python -m powermem.mcp --config config.json
    python -m powermem.mcp --env .env
"""

from .server import main

if __name__ == "__main__":
    main()
