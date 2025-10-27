#!/usr/bin/env python3
"""
Test script to verify Plex connection and functionality
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from plex_assistant_mcp.plex_client import PlexClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PLEX_URL = os.getenv("PLEX_URL", "http://localhost:32400")
PLEX_TOKEN = os.getenv("PLEX_TOKEN", "")


def test_connection():
    """Test basic connection"""
    print("🔌 Testing Plex connection...")
    try:
        client = PlexClient(PLEX_URL, PLEX_TOKEN)
        if client.test_connection():
            print("✅ Connection successful!")
            return client
        else:
            print("❌ Connection test failed")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None


def test_server_info(client: PlexClient):
    """Get server info"""
    print("\n📡 Server Information:")
    info = client.get_server_info()
    for key, value in info.items():
        print(f"   {key}: {value}")


def test_libraries(client: PlexClient):
    """Get libraries"""
    print("\n📚 Libraries:")
    libraries = client.get_libraries()
    for lib in libraries:
        print(f"   - {lib['title']} ({lib['type']}): {lib['count']} items")


def test_statistics(client: PlexClient):
    """Get statistics"""
    print("\n📊 Library Statistics:")
    stats = client.get_library_statistics()
    print(f"   Total items: {stats.get('total_items', 0)}")
    print("   By type:")
    for media_type, count in stats.get("by_type", {}).items():
        print(f"      - {media_type}: {count}")


def test_search(client: PlexClient):
    """Test search functionality"""
    print("\n🔍 Testing search (searching for 'matrix'):")
    results = client.search("matrix", limit=5)
    if results:
        for result in results:
            print(f"   - {result['title']} ({result['type']})")
    else:
        print("   No results found")


def test_sessions(client: PlexClient):
    """Get active sessions"""
    print("\n👥 Currently Playing:")
    sessions = client.get_currently_playing()
    if sessions:
        for session in sessions:
            progress = f"{session['viewOffset']/1000:.0f}s / {session['duration']/1000:.0f}s" if session.get('duration') else "N/A"
            print(f"   - {session['title']}")
            print(f"     User: {session['user']}")
            print(f"     Type: {session['type']}")
            print(f"     Progress: {progress}")
    else:
        print("   Nobody is watching anything right now")


def test_playlists(client: PlexClient):
    """Get playlists"""
    print("\n📋 Playlists:")
    playlists = client.get_playlists()
    if playlists:
        for playlist in playlists:
            print(f"   - {playlist['title']} ({playlist['playlistType']}): {playlist['itemCount']} items")
    else:
        print("   No playlists found")


def main():
    """Run all tests"""
    print("=" * 50)
    print("🎬 Plex Assistant MCP - Connection Test")
    print("=" * 50)
    print(f"\nPlex URL: {PLEX_URL}")
    print(f"Token: {PLEX_TOKEN[:10]}..." if PLEX_TOKEN else "Token: NOT SET")

    if not PLEX_TOKEN:
        print("\n⚠️  PLEX_TOKEN not set in environment or .env file")
        print("   See README.md for instructions on how to get your token")
        return

    client = test_connection()
    if not client:
        return

    # Run all tests
    try:
        test_server_info(client)
        test_libraries(client)
        test_statistics(client)
        test_search(client)
        test_sessions(client)
        test_playlists(client)

        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Error during tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
