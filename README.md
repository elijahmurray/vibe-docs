# Vibe Docs MCP Server

Vibe Docs is a Model Context Protocol (MCP) server designed to streamline the vibe coding workflow. It helps you create and maintain comprehensive project documentation with the assistance of AI, ensuring that AI tools have the full context needed for high-quality coding assistance.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/vibe-docs.git
cd vibe-docs

# Install dependencies
npm install

# Build the TypeScript code
npm run build
```

### API Key Setup

Vibe Docs requires an Anthropic API key to generate documentation using Claude LLMs. You can set this up in three ways:

1. **Environment variable**:
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

2. **Configuration file**:
Create a file at `~/.vibe-docs/config.json`:
```json
{
  "apiKey": "your-api-key-here",
  "model": "claude-3-haiku-20240307"
}
```

3. **Using the MCP tool**:
Use the `set-api-key` tool from your MCP client to configure the API key with the following parameters:
```json
{
  "apiKey": "your-api-key-here",
  "model": "claude-3-haiku-20240307"
}
```

## MCP Server Tools

Vibe Docs provides the following MCP tools for documentation generation and management:

### `init-docs`

Initializes a new documentation structure in your project.

**Parameters**:
- `directory`: Target directory for documentation (default: './docs')
- `template`: Template to use (default: 'standard')

**Example**:
```json
{
  "directory": "./project-docs",
  "template": "standard"
}
```

This creates a docs folder with template files for:
- `prd.md` (Product Requirements Document)
- `instructions.md` (AI-optimized instructions)
- `user-stories.md` (User stories)
- `design-doc.md` (Design document)

### `generate-docs`

Generates derived documentation from your PRD.

**Parameters**:
- `inputFile`: Path to the PRD file (default: './docs/prd.md')
- `outputTypes`: Array of document types to generate (default: ['instructions', 'user-stories', 'design-doc'])
- `updateExisting`: Whether to update existing files (default: false)
- `model`: Anthropic model to use (default: 'claude-3-haiku-20240307')
- `anthropicApiKey`: Optional API key override

**Example**:
```json
{
  "inputFile": "./docs/prd.md",
  "outputTypes": ["instructions", "design-doc"],
  "updateExisting": true
}
```

### `update-docs`

Updates existing documentation based on changes to the PRD.

**Parameters**:
- `inputFile`: Path to the updated PRD file (default: './docs/prd.md')
- `outputTypes`: Array of document types to update (default: all existing docs)
- `model`: Anthropic model to use (default: 'claude-3-haiku-20240307')

**Example**:
```json
{
  "inputFile": "./docs/prd.md",
  "outputTypes": ["instructions"]
}
```

### `validate-docs`

Validates the documentation structure and content for completeness.

**Parameters**:
- `directory`: Directory containing documentation (default: './docs')
- `fix`: Whether to attempt to fix issues automatically (default: false)

**Example**:
```json
{
  "directory": "./docs",
  "fix": true
}
```

### `set-api-key`

Sets the Anthropic API key for document generation.

**Parameters**:
- `apiKey`: Your Anthropic API key
- `model`: Optional default model to use (default: 'claude-3-haiku-20240307')

**Example**:
```json
{
  "apiKey": "sk-ant-api03-...",
  "model": "claude-3-opus-20240229"
}
```

## MCP Workflow

1. **Start the MCP server**:
   ```bash
   npm run mcp
   ```

2. **Connect with an MCP client**:
   Configure your MCP client (like Windsurf IDE) to connect to the server.

3. **Initialize documentation**:
   Use the `init-docs` tool to create documentation templates.

4. **Fill in your PRD**:
   Edit the generated `prd.md` file with your project requirements.

5. **Validate documentation**:
   Use the `validate-docs` tool to ensure your PRD is complete.

6. **Generate derived documents**:
   Use the `generate-docs` tool to create AI-generated documentation based on your PRD.

7. **Update as needed**:
   As your project evolves, update your PRD and use the `update-docs` tool to keep documentation in sync.

## Documentation Structure

### PRD (prd.md)
The core document that captures all project requirements. This serves as the source of truth for your project.

### Instructions (instructions.md)
AI-optimized guidance for code generation tools. This is what you'll refer to when using AI coding assistants.

### User Stories (user-stories.md)
Structured user narratives that clarify how users will interact with your software.

### Design Document (design-doc.md)
Technical architecture and visual design specifications.

## MCP Server Configuration

For the MCP server, you can configure the Anthropic API key in one of these ways:

1. **Environment variable**:
   ```bash
   export ANTHROPIC_API_KEY=your-api-key-here
   ```

2. **Configuration file**:
   Create a file at `~/.vibe-docs/config.json`:
   ```json
   {
     "apiKey": "your-api-key-here",
     "model": "claude-3-haiku-20240307"
   }
   ```

3. **Set via MCP tool**:
   Use the `set-api-key` tool from your MCP client to configure the API key.
```

## License

MIT