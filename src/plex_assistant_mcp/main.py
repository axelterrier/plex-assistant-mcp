#!/usr/bin/env python3
"""
Plex Assistant MCP - Model Context Protocol server for Plex management
"""

import os
import sys
import logging

from mcp.server.fastmcp import FastMCP

from .plex_client import PlexClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Plex client
PLEX_URL = os.getenv("PLEX_URL", "http://localhost:32400")
PLEX_TOKEN = os.getenv("PLEX_TOKEN", "")

if not PLEX_TOKEN:
    logger.error("PLEX_TOKEN environment variable not set")
    sys.exit(1)

plex_client = PlexClient(PLEX_URL, PLEX_TOKEN)
logger.info(f"Connected to Plex at {PLEX_URL}")

# Create MCP server with FastMCP
mcp = FastMCP("plex-assistant")


@mcp.tool()
def test_plex_connection() -> dict:
    """Test connection to Plex server and display server info"""
    try:
        info = plex_client.get_server_info()
        return {
            "status": "connected",
            "message": f"Connected to {info.get('friendlyName', 'Plex server')}",
            "server_info": info,
        }
    except Exception as e:
        return {"status": "error", "message": f"Connection failed: {str(e)}"}


@mcp.tool()
def get_server_info() -> dict:
    """Get detailed Plex server information"""
    try:
        info = plex_client.get_server_info()
        return {"success": True, "data": info}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_libraries() -> dict:
    """Get all media libraries in Plex"""
    try:
        libraries = plex_client.get_libraries()
        return {
            "success": True,
            "count": len(libraries),
            "data": libraries,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_library_statistics() -> dict:
    """Get statistics about all libraries"""
    try:
        stats = plex_client.get_library_statistics()
        return {"success": True, "data": stats}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def search_content(query: str, limit: int = 20) -> dict:
    """Search for content across all libraries by title or keywords"""
    try:
        results = plex_client.search(query, limit=limit)
        return {
            "success": True,
            "query": query,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def search_in_library(query: str, library_key: str, media_type: str = "", limit: int = 20) -> dict:
    """Search for content in a specific library"""
    try:
        results = plex_client.search_in_library(query, library_key, media_type, limit)
        return {
            "success": True,
            "query": query,
            "library_key": library_key,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_currently_playing() -> dict:
    """Get list of currently playing sessions"""
    try:
        sessions = plex_client.get_currently_playing()
        return {
            "success": True,
            "active_sessions": len(sessions),
            "sessions": sessions,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_playlists() -> dict:
    """Get all playlists in the Plex server"""
    try:
        playlists = plex_client.get_playlists()
        return {
            "success": True,
            "count": len(playlists),
            "playlists": playlists,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def create_playlist(title: str, description: str = "") -> dict:
    """Create a new playlist"""
    try:
        result = plex_client.create_playlist(title, items=None, description=description)
        return {"success": result.get("success", False), "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_to_watchlist(title: str) -> dict:
    """Add a movie or show to watchlist"""
    try:
        item = plex_client.find_item(title)
        if not item:
            return {"success": False, "error": f"Could not find '{title}'"}
        
        result = plex_client.add_to_collection(item["key"], "Watchlist")
        return {
            "success": result,
            "title": title,
            "message": f"Added '{title}' to Watchlist" if result else f"Failed to add '{title}' to Watchlist",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def toggle_watched(title: str, watched: bool = True) -> dict:
    """Mark content as watched or unwatched"""
    try:
        item = plex_client.find_item(title)
        if not item:
            return {"success": False, "error": f"Could not find '{title}'"}
        
        if watched:
            result = plex_client.set_watched(item["key"])
            message = f"Marked '{title}' as watched"
        else:
            result = plex_client.set_unwatched(item["key"])
            message = f"Marked '{title}' as unwatched"
        
        return {
            "success": result,
            "title": title,
            "watched": watched,
            "message": message if result else f"Failed to update '{title}'",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def mark_collection(title: str, collection_name: str) -> dict:
    """Add content to a collection"""
    try:
        item = plex_client.find_item(title)
        if not item:
            return {"success": False, "error": f"Could not find '{title}'"}
        
        result = plex_client.add_to_collection(item["key"], collection_name)
        return {
            "success": result,
            "title": title,
            "collection": collection_name,
            "message": f"Added '{title}' to '{collection_name}'" if result else f"Failed to add '{title}' to '{collection_name}'",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    logger.info("Plex Assistant MCP server started")
    mcp.run()