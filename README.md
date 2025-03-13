# Vibe Docs - AI-Enhanced Documentation Scaffolding

Vibe Docs is a documentation scaffolding tool designed specifically for AI-assisted development. It creates a standardized structure that helps AI tools understand your project and provide high-quality assistance.

## Features

- **Project-specific documentation** tailored to your project type (fullstack, API-only, frontend, etc.)
- **AI-ready knowledge base** designed for Cursor, Windsurf, Claude, and other AI assistants
- **Feature tracking** with AI-powered detection of implemented features
- **Minimal scaffolding mode** for quick setup with TODOs
- **MCP server integration** for use with Model Context Protocol

## Installation

### Using pipx (Recommended)

For Python applications like vibe-docs, `pipx` is the recommended installation method as it automatically creates an isolated environment:

```bash
# Install pipx if you don't have it
brew install pipx       # macOS
python -m pip install --user pipx   # Other platforms

# Install vibe-docs
pipx install vibe-docs
```

### Using a Virtual Environment

If you're seeing "externally managed environment" errors (PEP 668), use a virtual environment:

```bash
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install inside the virtual environment
pip install vibe-docs
```

### Other Installation Methods

```bash
# Install for current user only (may avoid permission issues)
pip install --user vibe-docs

# Install directly from GitHub
pip install git+https://github.com/elijahmurray/vibe-docs.git

# On macOS with Homebrew Python, you might need this flag (use with caution)
pip install --break-system-packages vibe-docs
```

### Dependencies

Vibe Docs requires Python 3.13+ and the following libraries (automatically installed):
- click
- mcp
- pydantic
- rich
- questionary
- anthropic (for AI feature detection)

## Quick Start

```bash
# Navigate to your existing project
cd your-project-directory

# Initialize documentation for your project
vibe init your-project-name

# Update documentation with AI feature detection
vibe update --ai

# Check feature implementation status
vibe status
```

## Commands

### Initialize a Project

```bash
vibe init PROJECT_NAME [--template TEMPLATE]
```

Run this command from within your existing project repository. The PROJECT_NAME is the name of your project (used in documentation), not a folder name. This command creates a `docs/` folder in your current directory with:
- `project_coding_docs.md` - Primary AI knowledge base
- `features.md` - Feature tracking document
- `implementation_plan.md` - Development roadmap
- AI assistant rule files (for Cursor and Windsurf)
- Various instruction documents in `docs/instructions/`

### Update Documentation

```bash
vibe update [--section SECTION] [--ai] [--api-key API_KEY]
```

Updates your documentation, with options to:
- Update specific sections only
- Use AI to detect which features are implemented (requires Anthropic API key)

### Check Status

```bash
vibe status [--format FORMAT]
```

Shows implementation status of features, with output in text or JSON format.

## MCP Server

Vibe Docs includes an MCP server for integration with AI tools:

```bash
# Start the MCP server
mcp-server-vibe-docs
```

## Troubleshooting

### "Externally Managed Environment" Error

This error occurs on modern Python installations (particularly with Homebrew Python on macOS) that implement PEP 668:

```
× This environment is externally managed
```

**Solution options:**

1. **Use pipx (recommended)**: 
   ```bash
   brew install pipx
   pipx install vibe-docs
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install vibe-docs
   ```

3. **Only if necessary**, override the protection (not recommended):
   ```bash
   pip install --break-system-packages vibe-docs
   ```

### Other Installation Issues

If you encounter other installation issues:

```bash
# Try installing with --user flag
pip install --user vibe-docs

# Check Python version (requires 3.13+)
python --version
```

### AI Feature Detection

If AI feature detection isn't working:

1. Ensure you have a valid Anthropic API key
2. Set the `ANTHROPIC_API_KEY` environment variable or use `--api-key`
3. Make sure your features.md file has proper feature descriptions
4. Check that your codebase has actual code files (not just config files)

## Development

For local development:

```bash
git clone https://github.com/elijahmurray/vibe-docs.git
cd vibe-docs
pip install -e .
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.