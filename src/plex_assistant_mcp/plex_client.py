"""
Plex API client wrapper
Handles all communication with Plex server
"""

import logging
from typing import Any, Dict, List, Optional
from plexapi.server import PlexServer
from plexapi.exceptions import Unauthorized, NotFound

logger = logging.getLogger(__name__)


class PlexClient:
    """Wrapper for Plex API interactions"""

    def __init__(self, url: str, token: str):
        """Initialize Plex client"""
        self.url = url
        self.token = token
        try:
            self.plex = PlexServer(url, token)
            logger.info(f"Connected to Plex server: {self.plex.friendlyName}")
        except Unauthorized:
            logger.error("Invalid Plex token")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Plex: {e}")
            raise

    def test_connection(self) -> bool:
        """Test connection to Plex server"""
        try:
            # Test by getting library sections
            sections = self.plex.library.sections()
            return len(sections) >= 0
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def get_server_info(self) -> Dict[str, Any]:
        """Get Plex server information"""
        try:
            return {
                "friendlyName": self.plex.friendlyName,
                "machineIdentifier": self.plex.machineIdentifier,
                "version": self.plex.version,
                "platform": self.plex.platform,
                "platformVersion": self.plex.platformVersion,
            }
        except Exception as e:
            logger.error(f"Failed to get server info: {e}")
            return {}

    def get_libraries(self) -> List[Dict[str, Any]]:
        """Get all libraries"""
        try:
            libraries = []
            for section in self.plex.library.sections():
                # Get count by searching all items
                try:
                    items = section.all()
                    count = len(items)
                except:
                    count = 0
                
                libraries.append(
                    {
                        "key": section.key,
                        "title": section.title,
                        "type": section.type,
                        "count": count,
                    }
                )
            return libraries
        except Exception as e:
            logger.error(f"Failed to get libraries: {e}")
            return []

    def get_library_statistics(self) -> Dict[str, Any]:
        """Get statistics for all libraries"""
        try:
            stats = {
                "total_items": 0,
                "by_type": {},
                "libraries": [],
            }

            for section in self.plex.library.sections():
                section_type = section.type
                try:
                    items = section.all()
                    section_count = len(items)
                except:
                    section_count = 0

                stats["total_items"] += section_count

                if section_type not in stats["by_type"]:
                    stats["by_type"][section_type] = 0
                stats["by_type"][section_type] += section_count

                stats["libraries"].append(
                    {
                        "title": section.title,
                        "type": section_type,
                        "count": section_count,
                    }
                )

            return stats
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}

    def search(
        self, query: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search across all libraries"""
        try:
            results = []
            search_results = self.plex.search(query, limit=limit)

            for item in search_results:
                result = self._format_item(item)
                if result:
                    results.append(result)

            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def search_in_library(
        self,
        query: str,
        library_key: str,
        media_type: str = "",
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Search in specific library"""
        try:
            library = self.plex.library.getByKey(library_key)
            if not library:
                return []

            results = []

            # Search by title
            items = library.search(query, limit=limit)

            for item in items:
                if media_type and not isinstance(item, type(media_type)):
                    continue

                result = self._format_item(item)
                if result:
                    results.append(result)

            return results
        except Exception as e:
            logger.error(f"Library search failed: {e}")
            return []

    def get_currently_playing(self) -> List[Dict[str, Any]]:
        """Get currently playing sessions"""
        try:
            sessions = []
            for session in self.plex.sessions():
                sessions.append(
                    {
                        "title": getattr(session, "title", "Unknown"),
                        "user": session.usernames[0] if session.usernames else "Unknown",
                        "type": session.type,
                        "duration": getattr(session, "duration", 0),
                        "viewOffset": getattr(session, "viewOffset", 0),
                    }
                )
            return sessions
        except Exception as e:
            logger.error(f"Failed to get sessions: {e}")
            return []

    def get_playlists(self) -> List[Dict[str, Any]]:
        """Get all playlists"""
        try:
            playlists = []
            for playlist in self.plex.playlists():
                playlists.append(
                    {
                        "key": playlist.key,
                        "title": playlist.title,
                        "playlistType": playlist.playlistType,
                        "itemCount": len(playlist),
                    }
                )
            return playlists
        except Exception as e:
            logger.error(f"Failed to get playlists: {e}")
            return []

    def create_playlist(
        self, title: str, items: Optional[List] = None, description: str = ""
    ) -> Dict[str, Any]:
        """Create a new playlist"""
        try:
            playlist = self.plex.createPlaylist(title, items=items)
            return {
                "success": True,
                "key": playlist.key,
                "title": playlist.title,
                "itemCount": len(playlist),
            }
        except Exception as e:
            logger.error(f"Failed to create playlist: {e}")
            return {"success": False, "error": str(e)}

    def find_item(self, title: str) -> Optional[Dict[str, Any]]:
        """Find an item by title"""
        try:
            results = self.search(title, limit=5)
            if results:
                return results[0]
            return None
        except Exception as e:
            logger.error(f"Failed to find item: {e}")
            return None

    def set_watched(self, item_key: str) -> bool:
        """Mark item as watched"""
        try:
            item = self.plex.library.getByKey(item_key)
            if item:
                item.markWatched()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to mark as watched: {e}")
            return False

    def set_unwatched(self, item_key: str) -> bool:
        """Mark item as unwatched"""
        try:
            item = self.plex.library.getByKey(item_key)
            if item:
                item.markUnwatched()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to mark as unwatched: {e}")
            return False

    def add_to_collection(self, item_key: str, collection_name: str) -> bool:
        """Add item to collection"""
        try:
            item = self.plex.library.getByKey(item_key)
            if item:
                item.addCollection(collection_name)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to add to collection: {e}")
            return False

    def remove_from_collection(self, item_key: str, collection_name: str) -> bool:
        """Remove item from collection"""
        try:
            item = self.plex.library.getByKey(item_key)
            if item:
                item.removeCollection(collection_name)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove from collection: {e}")
            return False

    def _format_item(self, item: Any) -> Optional[Dict[str, Any]]:
        """Format a Plex item to dictionary"""
        try:
            result = {
                "key": item.key,
                "title": getattr(item, "title", "Unknown"),
                "type": getattr(item, "type", "unknown"),
                "ratingKey": getattr(item, "ratingKey", ""),
            }

            # Add type-specific fields
            if hasattr(item, "year"):
                result["year"] = item.year
            if hasattr(item, "rating"):
                result["rating"] = item.rating
            if hasattr(item, "tagline"):
                result["tagline"] = item.tagline
            if hasattr(item, "duration"):
                result["duration"] = item.duration
            if hasattr(item, "viewCount"):
                result["viewCount"] = item.viewCount
            if hasattr(item, "summary"):
                result["summary"] = item.summary[:200] if item.summary else ""

            return result
        except Exception as e:
            logger.error(f"Failed to format item: {e}")
            return None