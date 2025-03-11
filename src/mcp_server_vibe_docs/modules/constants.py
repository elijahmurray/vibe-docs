"""Constants for the vibe-docs server."""

from pathlib import Path
from typing import Dict

# Default database path
DEFAULT_SQLITE_DATABASE_PATH: Path = Path.home() / ".vibe_docs.db"

# Template paths mapping
TEMPLATE_PATHS: Dict[str, Path] = {
    "default": Path(__file__).parent / "functionality" / "templates" / "default",
    "api": Path(__file__).parent / "functionality" / "templates" / "api",
}