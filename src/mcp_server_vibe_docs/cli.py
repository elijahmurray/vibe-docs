"""Command-line interface for vibe-docs."""

import click
from pathlib import Path
from typing import Optional

from .modules.functionality.init import initialize_project
from .modules.functionality.status import get_feature_status
from .modules.functionality.update import update_documentation
from .modules.constants import DEFAULT_SQLITE_DATABASE_PATH
from .server import serve as serve_mcp


@click.group()
@click.option(
    "--db",
    type=click.Path(exists=False),
    help="Custom SQLite database path",
)
@click.pass_context
def cli(ctx, db: Optional[str] = None):
    """Vibe Docs - Documentation scaffolding tool for AI-assisted project documentation."""
    ctx.ensure_object(dict)
    ctx.obj["db_path"] = Path(db) if db else DEFAULT_SQLITE_DATABASE_PATH


@cli.command()
@click.argument("project_name")
@click.option(
    "--template",
    default="default",
    help="Template to use (default or api)",
)
@click.pass_context
def init(ctx, project_name: str, template: str):
    """Initialize a new documentation structure."""
    result = initialize_project(project_name, template, ctx.obj["db_path"])
    click.echo(result)


@cli.command()
@click.option(
    "--section",
    help="Optional section name to update",
)
@click.option(
    "--ai",
    is_flag=True,
    help="Use AI to analyze codebase and detect completed features",
)
@click.option(
    "--api-key",
    help="Anthropic API key for AI feature detection (optional, can use ANTHROPIC_API_KEY env var)",
)
@click.pass_context
def update(ctx, section: Optional[str] = None, ai: bool = False, api_key: Optional[str] = None):
    """Update existing documentation.
    
    With --ai flag, uses Claude to analyze your codebase and detect completed features.
    """
    result = update_documentation(section, ctx.obj["db_path"], ai, api_key)
    click.echo(result)


@cli.command()
@click.option(
    "--format",
    default="text",
    help="Output format (text or json)",
)
@click.pass_context
def status(ctx, format: str):
    """Check feature implementation status."""
    result = get_feature_status(format, ctx.obj["db_path"])
    click.echo(result)


@cli.command()
@click.pass_context
def serve(ctx):
    """Start the MCP server."""
    click.echo("Starting Vibe Docs MCP server...")
    serve_mcp(ctx.obj["db_path"])


if __name__ == "__main__":
    cli(obj={})