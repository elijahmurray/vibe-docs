# Vibe Docs: MCP Server Installation and Usage Guide

## Installation

Vibe Docs is designed to be used as a Model Context Protocol (MCP) server, which allows it to be integrated with MCP-compatible tools and IDEs like Windsurf.

### Installation Steps

```bash
# Clone from source
git clone https://github.com/yourusername/vibe-docs.git
cd vibe-docs

# Install dependencies
npm install
```

Then build and run the MCP server:

```bash
# Build the TypeScript code
npm run build

# Run the MCP server
npm run vibe-docs-mcp
```

## Usage as an MCP Server

### Basic Workflow

When using Vibe Docs as an MCP server, you'll interact with it through an MCP-compatible client or IDE:

1. **Start the MCP server**:
   ```bash
   npm run vibe-docs-mcp
   ```
   This starts the server on the standard input/output streams.

2. **Connect with an MCP client**:
   Configure your MCP client (like Windsurf IDE) to connect to the server.

3. **Available MCP Tools**:
   The MCP server provides the following tools:

   #### `init-docs`
   Initializes a new documentation structure with template files.
   - **Parameters**:
     - `directory`: Target directory for documentation (default: './docs')
     - `template`: Template to use (default: 'standard')
   - **Example**:
     ```json
     {
       "directory": "./project-docs",
       "template": "standard"
     }
     ```
   - **Result**: Creates a documentation directory with template files for PRD, instructions, user stories, and design documents.

   #### `generate-docs`
   Generates documentation based on the content of a PRD file.
   - **Parameters**:
     - `inputFile`: Path to the PRD file (default: './docs/prd.md')
     - `outputTypes`: Array of document types to generate (default: ['instructions', 'user-stories', 'design-doc'])
     - `updateExisting`: Whether to update existing files (default: false)
     - `model`: Anthropic model to use (default: 'claude-3-haiku-20240307')
     - `anthropicApiKey`: Optional API key override
   - **Example**:
     ```json
     {
       "inputFile": "./docs/prd.md",
       "outputTypes": ["instructions", "design-doc"],
       "updateExisting": true
     }
     ```
   - **Result**: Generates the specified document types based on the PRD content.

   #### `validate-docs`
   Validates the documentation structure and content for completeness.
   - **Parameters**:
     - `directory`: Directory containing documentation (default: './docs')
     - `fix`: Whether to attempt to fix issues automatically (default: false)
   - **Example**:
     ```json
     {
       "directory": "./docs",
       "fix": true
     }
     ```
   - **Result**: Reports on missing sections or files and optionally attempts to fix them.

   #### `update-docs`
   Updates existing documentation based on changes to the PRD.
   - **Parameters**:
     - `inputFile`: Path to the updated PRD file (default: './docs/prd.md')
     - `outputTypes`: Array of document types to update (default: all existing docs)
     - `model`: Anthropic model to use (default: 'claude-3-haiku-20240307')
   - **Example**:
     ```json
     {
       "inputFile": "./docs/prd.md",
       "outputTypes": ["instructions"]
     }
     ```
   - **Result**: Updates the specified documents to reflect changes in the PRD.

   #### `set-api-key`
   Sets the Anthropic API key for document generation.
   - **Parameters**:
     - `apiKey`: Your Anthropic API key
     - `model`: Optional default model to use (default: 'claude-3-haiku-20240307')
   - **Example**:
     ```json
     {
       "apiKey": "sk-ant-api03-...",
       "model": "claude-3-opus-20240229"
     }
     ```
   - **Result**: Saves the API key to the configuration file for future use.

4. **Configuration**:
   Before using the documentation generation features, set your Anthropic API key:
   ```json
   // In your MCP client configuration
   {
     "anthropicApiKey": "your-api-key-here"
   }
   ```
   Or use the `set-api-key` tool to configure it.



## Configuration

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

## Workflow Tips

1. **Start with a clear product vision**: Before using any MCP tools, have a clear understanding of what you want to build.

2. **Be thorough with your PRD**: The more detailed your PRD, the better the derived documents will be.

3. **Iterative updates**: As your project evolves, update your PRD first, then use the `update-docs` tool to keep all documentation in sync.

4. **Version control**: Commit your documentation alongside your code to track its evolution.

5. **AI collaboration**: Use the generated `instructions.md` when working with AI coding tools for best results.

## MCP Integration Guide

### Connecting to Windsurf IDE

1. **Start the MCP server**:
   ```bash
   npm run vibe-docs-mcp
   ```

2. **Configure Windsurf**:
   In your Windsurf IDE, add a new MCP connection with the following settings in your `mcp_config.json` file:
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

3. **Using MCP Tools**:
   Once connected, you can use the Vibe Docs tools directly from Windsurf:

   #### Workflow Example
   1. **Initialize Documentation**:
      - Select the `init-docs` tool
      - Specify a directory (e.g., "./docs")
      - Choose a template (e.g., "standard")
      - This will create the initial documentation structure

   2. **Create Your PRD**:
      - Edit the generated `prd.md` file in your docs directory
      - Fill in all the required sections

   3. **Validate Documentation**:
      - Use the `validate-docs` tool to check for completeness
      - Review any warnings or errors

   4. **Generate Documentation**:
      - Use the `generate-docs` tool to create derived documents
      - Select which document types to generate
      - Review the generated files

   5. **Update Documentation**:
      - After making changes to your PRD, use `update-docs`
      - This will update the derived documents while preserving manual edits

4. **Troubleshooting**:
   - If the connection fails, check that the MCP server is running
   - Verify your Anthropic API key is properly set in the configuration
   - Check the server logs for any error messages
   - Make sure the paths in your MCP configuration are correct
   - Ensure you've built the TypeScript code with `npm run build`
