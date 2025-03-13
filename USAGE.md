# Vibe Docs - Usage Guide

## Overview

Vibe Docs is a documentation scaffolding tool that helps you create and maintain comprehensive project documentation with AI assistance. This guide demonstrates how to use the tool effectively.

## Quick Start

1. **Install the tool:**

```bash
npm install -g vibe-docs
```

2. **Initialize documentation in your project:**

```bash
vibe init
```

This creates a `docs` directory with template files for your project documentation.

3. **Fill in your PRD:**

Edit the `docs/prd.md` file to describe your project requirements.

4. **Validate your documentation:**

```bash
vibe validate
```

5. **Generate derived documents from your PRD:**

```bash
vibe generate --output-all
```

6. **Update documentation as your project evolves:**

```bash
vibe update
```

## Common Workflows

### Starting a New Project

```bash
# Create a new project
mkdir my-project && cd my-project

# Initialize documentation structure
vibe init

# Edit the PRD
# (Open docs/prd.md in your editor and fill it out)

# Validate the PRD
vibe validate

# Generate all related documents
vibe generate --output-all
```

### Updating Existing Documentation

```bash
# After updating your PRD
vibe validate
vibe update
```

### Selective Document Generation

```bash
# Generate only instructions and user stories
vibe generate --output instructions,user-stories
```

## Configuration

Create a `vibe.config.js` file in your project root to customize behavior:

```javascript
module.exports = {
  docsDir: './documentation',
  templates: {
    prd: './custom-templates/prd.md',
  },
  llm: {
    model: 'gpt-4',
    temperature: 0.7
  },
  validation: {
    requiredSections: ['Project Overview', 'Core Features']
  }
};
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
3. Run `vibe validate` regularly to ensure completeness
4. Use `vibe update` to keep derived documents in sync
5. Share the documentation with your development team and AI assistant tools