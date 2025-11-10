#!/usr/bin/env python3
"""
Setup script for powermem development environment

This script sets up the development environment for powermem.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_environment():
    """Setup development environment."""
    print("Setting up powermem development environment...")
    
    # Create necessary directories
    directories = [
        "data",
        "logs",
        "configs",
        "tests/data",
        "tests/logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_example = Path(".env.example")
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print("Created .env file from .env.example")
        else:
            print("Warning: .env.example not found")
    
    # Install development dependencies
    print("Installing development dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", ".[dev]"], check=True)
        print("Development dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install development dependencies: {e}")
        return False
    
    # Run tests to verify setup
    print("Running tests to verify setup...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "tests/unit/", "-v"], check=True)
        print("Tests passed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Tests failed: {e}")
        return False
    
    print("Development environment setup completed successfully!")
    return True

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
