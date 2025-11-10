"""
Version information management
"""

__version__ = "0.1.0"
__version_info__ = tuple(map(int, __version__.split(".")))

# Version history
VERSION_HISTORY = {
    "0.1.0": "2025-10-16 - Initial version release",
}

def get_version() -> str:
    """Get current version number"""
    return __version__

def get_version_info() -> tuple:
    """Get version info tuple"""
    return __version_info__

def get_version_history() -> dict:
    """Get version history"""
    return VERSION_HISTORY
