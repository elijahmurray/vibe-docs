# Vibe Docs MCP Server - Usage Guide

## Overview

Vibe Docs is a Model Context Protocol (MCP) server that helps you create and maintain comprehensive project documentation with AI assistance. This guide demonstrates how to use the MCP server effectively with an MCP client like Windsurf IDE.

## Quick Start

1. **Install and build the server:**

```bash
# Clone the repository
git clone https://github.com/yourusername/vibe-docs.git
cd vibe-docs

# Install dependencies
npm install

# Build the TypeScript code
npm run build
```

2. **Start the MCP server:**

```bash
npm run vibe-docs-mcp
```

3. **Configure your MCP client:**

In your MCP client (e.g., Windsurf IDE), add a configuration for the Vibe Docs server:

```json
{
  "mcpServers": {
    "vibe-docs": {
      "command": "node",
      "args": [
        "/path/to/vibe-docs/dist/index.js"
      ],
      "cwd": "/path/to/vibe-docs",
      "env": {
        "ANTHROPIC_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

4. **Connect to the MCP server:**

Connect to the Vibe Docs MCP server from your client to access the documentation tools.

5. **Use the MCP tools:**

Use the available MCP tools to create and manage your documentation:
- `init-docs`: Initialize documentation structure
- `generate-docs`: Generate documentation from PRD
- `validate-docs`: Validate documentation structure
- `update-docs`: Update documentation as your project evolves
- `set-api-key`: Set the Anthropic API key

## Common MCP Workflows

### Starting a New Project

1. **Initialize documentation structure:**
   Use the `init-docs` MCP tool with parameters. For most reliable results, use absolute paths:
   ```json
   {
     "directory": "/absolute/path/to/your/project/docs",
     "template": "standard"
   }
   ```
   
   Alternatively, you can use relative paths, but be aware they're relative to your current project directory:
   ```json
   {
     "directory": "./docs",
     "template": "standard"
   }
   ```

2. **Edit the PRD:**
   Open the generated `docs/prd.md` file in your editor and fill it out with your project requirements.

3. **Validate the PRD:**
   Use the `validate-docs` MCP tool with parameters:
   ```json
   {
     "directory": "./docs"
   }
   ```

4. **Generate all related documents:**
   Use the `generate-docs` MCP tool with parameters:
   ```json
   {
     "inputFile": "./docs/prd.md",
     "outputTypes": ["instructions", "user-stories", "design-doc"]
   }
   ```

### Updating Existing Documentation

1. **After updating your PRD:**
   Use the `validate-docs` MCP tool to check for completeness.

2. **Update derived documents:**
   Use the `update-docs` MCP tool with parameters:
   ```json
   {
     "inputFile": "./docs/prd.md"
   }
   ```

### Selective Document Generation

1. **Generate only specific document types:**
   Use the `generate-docs` MCP tool with parameters:
   ```json
   {
     "inputFile": "./docs/prd.md",
     "outputTypes": ["instructions", "user-stories"]
   }
   ```

## MCP Server Configuration

You can configure the Vibe Docs MCP server in the following ways:

### API Key Configuration

1. **Environment variable:**
   ```bash
   export ANTHROPIC_API_KEY=your-api-key-here
   ```

2. **Configuration file:**
   Create a file at `~/.vibe-docs/config.json`:
   ```json
   {
     "apiKey": "your-api-key-here",
     "model": "claude-3-haiku-20240307"
   }
   ```

3. **Using the MCP tool:**
   Use the `set-api-key` tool from your MCP client with parameters:
   ```json
   {
     "apiKey": "your-api-key-here",
     "model": "claude-3-haiku-20240307"
   }
   ```
```

## Example Output

After running Vibe Docs on a project, your documentation structure will look like:

```
docs/
├── README.md (documentation guide)
├── prd.md (product requirements document)
├── instructions.md (AI-optimized instructions)
├── user-stories.md (user scenarios)
└── design-doc.md (technical architecture)
```

## Best Practices

1. Start with a detailed PRD as your source of truth
2. Keep the PRD updated as requirements change
3. Use the `validate-docs` MCP tool regularly to ensure completeness
4. Use the `update-docs` MCP tool to keep derived documents in sync
5. Share the documentation with your development team and AI assistant tools
6. Configure your MCP client with the correct path to the Vibe Docs server
7. Ensure your Anthropic API key is properly set before generating documentation
8. Use the latest Anthropic Claude models for best results