# Vibe Docs - Your Documentation Scaffolding Tool

Vibe Docs is a documentation scaffolding tool that helps you create and maintain comprehensive project documentation with the assistance of AI. By establishing a standardized structure for your documentation, Vibe Docs ensures that AI tools have the full context needed to provide high-quality assistance throughout your project's lifecycle.

## Features

- Project initialization with customizable templates
- Interactive prompts to fill in documentation details
- Feature status tracking with completion indicators
- Documentation update capability for evolving projects
- Multiple output formats for feature status (text, JSON)

## Installation

```bash
uv add vibe-docs
```

## Usage

```bash
# Initialize a new documentation structure
vibe init <project_name> [--template <template_name>]

# Update existing documentation
vibe update [--section <section_name>]

# Check feature implementation status
vibe status [--format <format>]
```

### Example Commands

```bash
# Initialize a new project with default template
vibe init my-awesome-project

# Initialize with a specific template
vibe init my-api-project --template api

# Update the entire documentation
vibe update

# Update a specific section
vibe update --section architecture

# Check feature implementation status
vibe status

# Export feature status as JSON
vibe status --format json
```

## Templates

Vibe Docs comes with two built-in templates:

1. **Default Template** - General purpose documentation structure
2. **API Template** - Specialized for API documentation

Each template includes:
- Feature tracking
- Instructions for different aspects of the project
- AI knowledge base setup
- Implementation planning
- AI rules for popular AI coding assistants

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/vibe-docs.git
cd vibe-docs

# Install development dependencies
uv add -e dev

# Run tests
uv run pytest
```