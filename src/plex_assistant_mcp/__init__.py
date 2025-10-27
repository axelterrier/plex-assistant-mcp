"""Plex Assistant MCP - Model Context Protocol server for Plex management"""

__version__ = "1.0.0"
__author__ = "Plex Assistant"

from .plex_client import PlexClient
from .tools import get_tool_definitions

__all__ = ["PlexClient", "get_tool_definitions"]
