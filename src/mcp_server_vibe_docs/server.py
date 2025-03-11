"""MCP server implementation for vibe-docs."""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import mcp
import uvicorn
from mcp.server.fastmcp import FastMCP

from .modules.functionality.init import initialize_project
from .modules.functionality.status import get_feature_status
from .modules.functionality.update import update_documentation
from .modules.constants import DEFAULT_SQLITE_DATABASE_PATH


def serve(sqlite_database: Optional[Path] = None) -> None:
    """Start the MCP server with the specified database path."""
    db_path = sqlite_database or DEFAULT_SQLITE_DATABASE_PATH
    
    app = FastMCP(
        server_name="vibe-docs",
        server_description="Documentation scaffolding tool for AI-assisted project documentation",
    )

    @app.tool(
        name="init",
        description="Initialize a new documentation structure"
    )
    async def init_tool(project_name: str, template: str = "default") -> str:
        """Initialize a new documentation structure.
        
        Args:
            project_name: Name of the project
            template: Template to use (default or api)
        """
        return initialize_project(project_name, template, db_path)

    @app.tool(
        name="update",
        description="Update existing documentation"
    )
    async def update_tool(section: Optional[str] = None, use_ai: bool = False, api_key: Optional[str] = None) -> str:
        """Update existing documentation.
        
        Args:
            section: Optional section name to update
            use_ai: Whether to use AI to analyze codebase and detect completed features
            api_key: Anthropic API key for AI feature detection (optional)
        """
        return update_documentation(section, db_path, use_ai, api_key)

    @app.tool(
        name="status",
        description="Check feature implementation status"
    )
    async def status_tool(format: str = "text") -> str:
        """Check feature implementation status.
        
        Args:
            format: Output format (text or json)
        """
        result = get_feature_status(format, db_path)
        if format == "json" and isinstance(result, dict):
            return json.dumps(result)
        return result

    # Run the server
    uvicorn.run(app, host="127.0.0.1", port=8000)


def main() -> None:
    """Entry point for the MCP server."""
    serve()


if __name__ == "__main__":
    main()