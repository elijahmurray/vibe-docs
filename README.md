# Vibe Docs

Vibe Docs is a documentation scaffolding tool designed to streamline the vibe coding workflow. It helps you create and maintain comprehensive project documentation with the assistance of AI, ensuring that AI tools have the full context needed for high-quality coding assistance.

## Installation

```bash
npm install -g vibe-docs
```

### API Key Setup

Vibe Docs requires an Anthropic API key to generate documentation using Claude LLMs. You can set this up in two ways:

1. Environment variable:
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

2. Using the config command:
```bash
vibe config:set-api-key
```

You can manage your configuration with these commands:

```bash
# View current config
vibe config

# Set API key
vibe config:set-api-key

# Set model to use
vibe config:set-model claude-3-haiku-20240307

# Vibe only supports Anthropic's Claude models

# Reset to defaults
vibe config:reset
```

## Commands

### `vibe init`

Initializes a new documentation structure in your project.

```bash
vibe init [options]
```

Options:
- `--dir <directory>` - Target directory for documentation (default: './docs')
- `--template <template>` - Template to use (default: 'standard')

This creates a docs folder with template files for:
- `prd.md` (Product Requirements Document)
- `instructions.md` (AI-optimized instructions)
- `user-stories.md` (User stories)
- `design-doc.md` (Design document)

### `vibe generate`

Generates derived documentation from your PRD.

```bash
vibe generate [options]
```

Options:
- `--input <file>` - Input PRD file path (default: './docs/prd.md')
- `--output-all` - Generate all document types
- `--output <types>` - Specific document types to generate (comma-separated)
- `--update-existing` - Update existing documents
- `--model <n>` - LLM model to use (default: 'gpt-4')

### `vibe update`

Updates documentation as your project evolves.

```bash
vibe update [options]
```

Options:
- `--input <file>` - Input file to update from (default: './docs/prd.md')
- `--check` - Check for inconsistencies without updating
- `--model <n>` - LLM model to use (default: 'gpt-4')

### `vibe validate`

Validates your documentation for completeness.

```bash
vibe validate [options]
```

Options:
- `--dir <directory>` - Directory to validate (default: './docs')
- `--fix` - Attempt to fix issues automatically

## Workflow

1. Run `vibe init` to create documentation templates
2. Fill in your PRD with project requirements
3. Run `vibe validate` to ensure your PRD is complete
4. Run `vibe generate` to create derived documents
5. As your project evolves, update your PRD and run `vibe update`

## Documentation Structure

### PRD (prd.md)
The core document that captures all project requirements. This serves as the source of truth for your project.

### Instructions (instructions.md)
AI-optimized guidance for code generation tools. This is what you'll refer to when using AI coding assistants.

### User Stories (user-stories.md)
Structured user narratives that clarify how users will interact with your software.

### Design Document (design-doc.md)
Technical architecture and visual design specifications.

## Configuration

Create a `vibe.config.js` file in your project root to customize behavior:

```javascript
module.exports = {
  docsDir: './documentation',
  templates: {
    prd: './custom-templates/prd.md',
    // other custom templates...
  },
  llm: {
    model: 'gpt-4',
    temperature: 0.7
  },
  validation: {
    requiredSections: ['Project Overview', 'Core Features', 'Technical Requirements']
  }
};
```

## License

MIT