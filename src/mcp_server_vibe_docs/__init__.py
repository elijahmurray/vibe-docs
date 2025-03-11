"""MCP for generating documentation for AI IDEs to read."""

from .server import main
from .cli import cli

__all__ = ["main", "cli"]