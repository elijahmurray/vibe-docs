# {{project_name}} Documentation

This folder contains project documentation structured specifically for AI-assisted development.

## Documentation Structure

### Primary AI Knowledge Files (Root Directory)
These files in the root of the docs/ directory are designed to be loaded directly into AI tools:

- **project_coding_docs.md** - The primary knowledge base for AI tools (attach this first)
- **features.md** - Tracks implementation status of planned features
- **implementation_plan.md** - Step-by-step implementation plan
- **cursorrules.md** - Guidelines for Cursor AI
- **windsurfrules.md** - Guidelines for Windsurf AI

### Reference Documents (Instructions Folder)
The `instructions/` folder contains detailed reference documentation:

- **getting_started.md** - Project setup and onboarding
- **api_reference.md** - Detailed API documentation
- **architecture.md** - System architecture details
- **frontend_guidelines.md** - Frontend development guidelines (if applicable)
- **backend_guidelines.md** - Backend development guidelines (if applicable)

## Working with AI

### Setup for AI Tools

#### Cursor
1. Open your project in Cursor
2. Go to Settings → AI → Knowledge
3. Add `docs/project_coding_docs.md` as a knowledge file
4. Add `docs/cursorrules.md` as a rules file

#### Windsurf
1. Open your project in Windsurf
2. Navigate to the AI panel
3. Add `docs/project_coding_docs.md` to your knowledge base
4. Add `docs/windsurfrules.md` as your rules file

#### For other AI tools (GitHub Copilot, Claude, etc.)
- Copy/paste relevant sections from `project_coding_docs.md` into your prompts
- Reference specific documentation as needed in your prompts

### Effective Prompting Patterns

- "Based on our project_coding_docs.md, help me implement [feature]"
- "Following our API conventions in api_reference.md, design an endpoint for [feature]"
- "Using our established patterns, help me create a test for [component]"
- "Review this code based on our project guidelines"

## Maintaining This Documentation

1. Keep these documents updated as your project evolves
2. Add new endpoints to api_reference.md as they're implemented
3. Update features.md to track implementation progress
4. Fill in TODOs throughout the documentation with project specifics