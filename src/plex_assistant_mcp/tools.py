"""
MCP Tool definitions and handlers for Plex operations
"""

import logging
from typing import Any, Dict, List
import mcp.types as types

from .plex_client import PlexClient

logger = logging.getLogger(__name__)


def get_tool_definitions() -> List[types.Tool]:
    """Get all MCP tool definitions"""
    return [
        types.Tool(
            name="test_plex_connection",
            description="Test connection to Plex server and display server info",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_server_info",
            description="Get detailed Plex server information (name, version, platform)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_libraries",
            description="Get all media libraries in Plex (Movies, TV, Music, Photos, etc.)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_library_statistics",
            description="Get statistics about all libraries (total items, breakdown by type)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="search_content",
            description="Search for content across all libraries by title or keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (movie/show/album title or keywords)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 20)",
                        "default": 20,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_in_library",
            description="Search for content in a specific library",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "library_key": {
                        "type": "string",
                        "description": "Library key (obtained from get_libraries)",
                    },
                    "media_type": {
                        "type": "string",
                        "description": "Filter by type: movie, show, track, artist, album, photo (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 20)",
                        "default": 20,
                    },
                },
                "required": ["query", "library_key"],
            },
        ),
        types.Tool(
            name="get_currently_playing",
            description="Get list of currently playing sessions and who is watching what",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_playlists",
            description="Get all playlists in the Plex server",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="create_playlist",
            description="Create a new playlist",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Playlist title",
                    },
                    "description": {
                        "type": "string",
                        "description": "Playlist description (optional)",
                        "default": "",
                    },
                },
                "required": ["title"],
            },
        ),
        types.Tool(
            name="add_to_watchlist",
            description="Add a movie or show to watchlist (mark as wanted)",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the movie or show",
                    },
                },
                "required": ["title"],
            },
        ),
        types.Tool(
            name="toggle_watched",
            description="Mark content as watched or unwatched",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the content",
                    },
                    "watched": {
                        "type": "boolean",
                        "description": "True to mark as watched, False to mark as unwatched (default: True)",
                        "default": True,
                    },
                },
                "required": ["title"],
            },
        ),
        types.Tool(
            name="mark_collection",
            description="Add content to a collection (e.g., 'Favorites', 'Comedy')",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the content",
                    },
                    "collection_name": {
                        "type": "string",
                        "description": "Name of the collection to add to",
                    },
                },
                "required": ["title", "collection_name"],
            },
        ),
    ]


# Tool handlers


async def handle_get_server_info(client: PlexClient) -> Dict[str, Any]:
    """Handler for get_server_info tool"""
    try:
        info = client.get_server_info()
        if info:
            return {
                "success": True,
                "data": info,
            }
        return {"success": False, "error": "Unable to retrieve server info"}
    except Exception as e:
        logger.error(f"Error getting server info: {e}")
        return {"success": False, "error": str(e)}


async def handle_get_libraries(client: PlexClient) -> Dict[str, Any]:
    """Handler for get_libraries tool"""
    try:
        libraries = client.get_libraries()
        return {
            "success": True,
            "count": len(libraries),
            "data": libraries,
        }
    except Exception as e:
        logger.error(f"Error getting libraries: {e}")
        return {"success": False, "error": str(e)}


async def handle_get_statistics(client: PlexClient) -> Dict[str, Any]:
    """Handler for get_library_statistics tool"""
    try:
        stats = client.get_library_statistics()
        if stats:
            return {
                "success": True,
                "data": stats,
            }
        return {"success": False, "error": "Unable to retrieve statistics"}
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return {"success": False, "error": str(e)}


async def handle_search_content(
    client: PlexClient, query: str, limit: int
) -> Dict[str, Any]:
    """Handler for search_content tool"""
    try:
        results = client.search(query, limit=limit)
        return {
            "success": True,
            "query": query,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        logger.error(f"Error searching content: {e}")
        return {"success": False, "error": str(e)}


async def handle_search_in_library(
    client: PlexClient, query: str, library_key: str, media_type: str, limit: int
) -> Dict[str, Any]:
    """Handler for search_in_library tool"""
    try:
        results = client.search_in_library(query, library_key, media_type, limit)
        return {
            "success": True,
            "query": query,
            "library_key": library_key,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        logger.error(f"Error searching in library: {e}")
        return {"success": False, "error": str(e)}


async def handle_get_currently_playing(client: PlexClient) -> Dict[str, Any]:
    """Handler for get_currently_playing tool"""
    try:
        sessions = client.get_currently_playing()
        return {
            "success": True,
            "active_sessions": len(sessions),
            "sessions": sessions,
        }
    except Exception as e:
        logger.error(f"Error getting currently playing: {e}")
        return {"success": False, "error": str(e)}


async def handle_get_playlists(client: PlexClient) -> Dict[str, Any]:
    """Handler for get_playlists tool"""
    try:
        playlists = client.get_playlists()
        return {
            "success": True,
            "count": len(playlists),
            "playlists": playlists,
        }
    except Exception as e:
        logger.error(f"Error getting playlists: {e}")
        return {"success": False, "error": str(e)}


async def handle_create_playlist(
    client: PlexClient, title: str, description: str
) -> Dict[str, Any]:
    """Handler for create_playlist tool"""
    try:
        result = client.create_playlist(title, items=None, description=description)
        return {
            "success": result.get("success", False),
            "data": result,
        }
    except Exception as e:
        logger.error(f"Error creating playlist: {e}")
        return {"success": False, "error": str(e)}


async def handle_add_to_watchlist(client: PlexClient, title: str) -> Dict[str, Any]:
    """Handler for add_to_watchlist tool"""
    try:
        item = client.find_item(title)
        if not item:
            return {"success": False, "error": f"Could not find '{title}'"}

        # Add to a "Watchlist" collection
        result = client.add_to_collection(item["key"], "Watchlist")
        return {
            "success": result,
            "title": title,
            "message": f"Added '{title}' to Watchlist" if result else f"Failed to add '{title}' to Watchlist",
        }
    except Exception as e:
        logger.error(f"Error adding to watchlist: {e}")
        return {"success": False, "error": str(e)}


async def handle_toggle_watched(
    client: PlexClient, title: str, watched: bool
) -> Dict[str, Any]:
    """Handler for toggle_watched tool"""
    try:
        item = client.find_item(title)
        if not item:
            return {"success": False, "error": f"Could not find '{title}'"}

        if watched:
            result = client.set_watched(item["key"])
            message = f"Marked '{title}' as watched"
        else:
            result = client.set_unwatched(item["key"])
            message = f"Marked '{title}' as unwatched"

        return {
            "success": result,
            "title": title,
            "watched": watched,
            "message": message if result else f"Failed to update '{title}'",
        }
    except Exception as e:
        logger.error(f"Error toggling watched: {e}")
        return {"success": False, "error": str(e)}


async def handle_mark_collection(
    client: PlexClient, title: str, collection_name: str
) -> Dict[str, Any]:
    """Handler for mark_collection tool"""
    try:
        item = client.find_item(title)
        if not item:
            return {"success": False, "error": f"Could not find '{title}'"}

        result = client.add_to_collection(item["key"], collection_name)
        return {
            "success": result,
            "title": title,
            "collection": collection_name,
            "message": f"Added '{title}' to '{collection_name}'" if result else f"Failed to add '{title}' to '{collection_name}'",
        }
    except Exception as e:
        logger.error(f"Error marking collection: {e}")
        return {"success": False, "error": str(e)}
