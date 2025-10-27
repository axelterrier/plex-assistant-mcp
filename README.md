# Plex Assistant MCP

🎬 **MCP (Model Context Protocol) server for managing your Plex library through AI assistants like Claude.**

Plex Assistant MCP enables you to control Plex directly from Claude Desktop or any MCP-compatible client. Search for content, manage playlists, mark items as watched, and get library statistics using natural language!

## Features

- 🔍 **Search** - Find movies, shows, music, and photos across all libraries
- 📊 **Statistics** - View library overview and content breakdown
- 👥 **Live Sessions** - See who's watching what right now
- 📋 **Playlists** - Create, view, and manage playlists
- ✅ **Watchlist** - Mark content as watched/unwatched
- 🏷️ **Collections** - Organize content into custom collections
- 📡 **Server Info** - Get Plex server details and status
- 🎯 **Advanced Search** - Filter by library, media type, and more

## Prerequisites

- **Python** ≥ 3.12
- **uv** - Fast Python package manager ([Install here](https://github.com/astral-sh/uv))
- **Plex Server** - Running instance with admin access
- **Claude Desktop** - Latest version (or any MCP-compatible client)

## Quick Start

### 1. Clone or Create Project

```bash
# Create project directory
mkdir plex-assistant-mcp
cd plex-assistant-mcp

# Or clone if you have a repo
git clone https://github.com/yourusername/plex-assistant-mcp.git
cd plex-assistant-mcp
```

### 2. Initialize with uv

```bash
# Initialize Python project
uv init

# Install dependencies
uv sync
```

### 3. Configure Plex Connection

Create a `.env` file at the project root:

```env
PLEX_URL=http://your-ip:32400
PLEX_TOKEN=your-plex-auth-token
```

#### How to Find Your Plex Token

**Method 1: Using PlexAPI (Automatic)**
```bash
python3 -c "from plexapi.myplex import MyPlexAccount; account = MyPlexAccount(username='your-email', password='your-password'); print(account.authenticationToken)"
```

**Method 2: Browser DevTools**
1. Open https://app.plex.tv/desktop/
2. Open DevTools (F12) → Network tab
3. Look for any request to `plex.tv`
4. Find header `X-Plex-Token` - copy that value

**Method 3: Plex Settings**
1. Open Plex Web App
2. Settings → Your Account → Scroll to "Authorized Applications"
3. Generate a token in your Plex account settings

### 4. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

Add the following MCP server configuration:

```json
{
  "mcpServers": {
    "plex-assistant": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/YourUsername/Documents/plex-assistant-mcp",
        "run",
        "src/plex_assistant_mcp/main.py"
      ],
      "env": {
        "PLEX_URL": "http://192.168.1.100:32400",
        "PLEX_TOKEN": "your-actual-token-here"
      }
    }
  }
}
```

**Important:** 
- Update the `--directory` path to match your installation
- Replace `PLEX_URL` with your actual Plex server address
- Replace `PLEX_TOKEN` with your actual authentication token

### 5. Restart Claude Desktop

Close and reopen Claude Desktop. The Plex tools will now be available!

## Usage Examples

### Search for Content

```
"Search for The Matrix in my library"
"Find all movies from 2024"
"Show me TV shows with drama in the title"
```

### Library Management

```
"How many items do I have in my Plex library?"
"Show me my movie library statistics"
"What libraries do I have?"
```

### Active Sessions

```
"Who's watching something right now?"
"Show me current Plex sessions"
```

### Watchlist & Marking

```
"Mark The Dark Knight as watched"
"Add Oppenheimer to my watchlist"
"Mark this show as unwatched"
```

### Playlists

```
"Create a playlist called Favorites"
"Show me all my playlists"
"Get my available playlists"
```

### Collections

```
"Add this to my Sci-Fi collection"
"Mark Inception as part of my Best Movies collection"
```

## Available Tools

| Tool | Description |
|------|-------------|
| `test_plex_connection` | Test connection to Plex server |
| `get_server_info` | Get Plex server details |
| `get_libraries` | List all media libraries |
| `get_library_statistics` | Get library statistics and breakdown |
| `search_content` | Search across all libraries |
| `search_in_library` | Search within a specific library |
| `get_currently_playing` | See active sessions and what's being watched |
| `get_playlists` | List all playlists |
| `create_playlist` | Create a new playlist |
| `add_to_watchlist` | Add item to watchlist |
| `toggle_watched` | Mark content as watched/unwatched |
| `mark_collection` | Add item to a collection |

## Local Development & Testing

### Run the MCP Server Directly

```bash
export PLEX_URL="http://your-ip:32400"
export PLEX_TOKEN="your-token"
uv run src/plex_assistant_mcp/main.py
```

The server will start and wait for MCP commands via stdio.

### Test Connection

```bash
python3 << 'EOF'
from src.plex_assistant_mcp.plex_client import PlexClient
import os

client = PlexClient(
    os.getenv("PLEX_URL", "http://localhost:32400"),
    os.getenv("PLEX_TOKEN", "")
)
print("Connection test:", client.test_connection())
print("Server info:", client.get_server_info())
EOF
```

## Project Structure

```
plex-assistant-mcp/
├── src/
│   └── plex_assistant_mcp/
│       ├── __init__.py           # Package initialization
│       ├── main.py               # MCP server entry point
│       ├── plex_client.py         # Plex API wrapper
│       └── tools.py              # MCP tool definitions & handlers
├── pyproject.toml                # Project configuration
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
└── README.md                     # This file
```

## Troubleshooting

### Error: `PLEX_TOKEN environment variable not set`

**Solution:** Make sure your `.env` file exists and contains:
```env
PLEX_URL=http://your-ip:32400
PLEX_TOKEN=your-token
```

### Error: `Connection refused` or `Unable to connect`

**Solutions:**
- Verify Plex is running on your server
- Check that the `PLEX_URL` is correct (including IP and port)
- Test the URL in your browser: `http://your-ip:32400`
- Check firewall rules on your server
- Ensure Claude Desktop can reach your Plex server

### Error: `HTTP 401: Unauthorized`

**Solutions:**
- Verify your `PLEX_TOKEN` is correct
- Generate a new token if the old one expired
- Ensure you're using the correct authentication token format

### Error: `No results found` for search

**Solutions:**
- Try different spelling or keywords
- Use exact titles if possible
- Check that content exists in your Plex library
- Verify library is properly indexed

### Claude Desktop Shows No Plex Tools

**Solutions:**
- Verify the configuration file is properly formatted JSON
- Restart Claude Desktop completely (not just refresh)
- Check the MCP server logs in Claude Desktop settings
- Verify the `--directory` path is correct
- Test connection manually to ensure Plex is reachable

## API Reference

### PlexClient Methods

```python
# Connection
test_connection() -> bool

# Server & Libraries
get_server_info() -> Dict[str, Any]
get_libraries() -> List[Dict[str, Any]]
get_library_statistics() -> Dict[str, Any]

# Search & Discovery
search(query: str, limit: int = 20) -> List[Dict[str, Any]]
search_in_library(query: str, library_key: str, media_type: str = "") -> List[Dict[str, Any]]
find_item(title: str) -> Optional[Dict[str, Any]]

# Sessions
get_currently_playing() -> List[Dict[str, Any]]

# Playlists
get_playlists() -> List[Dict[str, Any]]
create_playlist(title: str, items: Optional[List] = None, description: str = "") -> Dict[str, Any]

# Content Management
set_watched(item_key: str) -> bool
set_unwatched(item_key: str) -> bool
add_to_collection(item_key: str, collection_name: str) -> bool
remove_from_collection(item_key: str, collection_name: str) -> bool
```

## Resources

- [Plex Official Site](https://www.plex.tv/)
- [Plex API Documentation](https://www.plex.tv/en/media-server-downloads/documentation/)
- [PlexAPI Python Library](https://github.com/pkkid/python-plexapi)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Documentation](https://docs.claude.com/)

## Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source and available under the MIT License.

## Disclaimer

This project is not officially affiliated with Plex or Anthropic. Use at your own risk and ensure you have proper authorization to access your Plex server.

---

Made with ❤️ for Plex enthusiasts who want AI-powered library management
