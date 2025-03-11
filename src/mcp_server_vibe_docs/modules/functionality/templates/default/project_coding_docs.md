# AI Knowledge Base: {{project_name}}

This document serves as the primary knowledge base for AI pair programming. When working with AI tools like Cursor, GitHub Copilot, or Claude, point them to this document first for project context.

## Project Overview
{{project_overview}}

## Project Type
{{project_type}}

## Technology Stack

### Frontend
{{frontend_stack}}

### Backend
{{backend_stack}}

## Key Components
{{key_components}}

## API Documentation

### API Overview
{{api_description}}

### Endpoints
<!-- TODO: Document your API endpoints here -->
```
GET /api/resource - Get all resources
GET /api/resource/:id - Get resource by ID
POST /api/resource - Create a new resource
PUT /api/resource/:id - Update a resource
DELETE /api/resource/:id - Delete a resource
```

## Data Models
{{data_models}}

## Coding Standards
{{coding_standards}}

## Development Workflow
<!-- TODO: Document your development workflow here -->
1. Create feature branch from main
2. Implement feature with tests
3. Run test suite
4. Create pull request
5. Code review and approval
6. Merge to main

## Common Commands
<!-- TODO: Document common commands used in development -->
```bash
# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## Working with AI
When using AI assistants with this project:

1. Use this document as the primary knowledge source (attach this file in Cursor/Windsurf)
2. For feature implementation, refer to features.md
3. For step-by-step development plan, refer to implementation_plan.md
4. Cursor and Windsurf users should check the respective rules files

Example prompts for AI:
- "Based on our project_coding_docs.md, help me implement the user authentication API"
- "Using our data models from the knowledge base, create a database schema"
- "Following our API conventions, help me design the endpoint for [feature]"