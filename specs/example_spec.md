# Vibe Docs - Your Documentation Scaffolding Tool

Vibe Docs is a documentation scaffolding tool that helps you create and maintain comprehensive project documentation with the assistance of AI. By establishing a standardized structure for your documentation, Vibe Docs ensures that AI tools have the full context needed to provide high-quality assistance throughout your project's lifecycle.

Using the MCP (Model Context Protocol), Vibe Docs can initialize your documentation structure, guide you through filling in the details, and help you track the implementation status of your planned features.

## Implementation Notes
- DEFAULT_SQLITE_DATABASE_PATH = Path.home() / ".vibe_docs.db" - place in constants.py
- Always force (auto update) tags to be lowercase, trim whitespace, and use dash instead of spaces or underscores
- MCP commands will return whatever the command returns
- Libraries should be:
  - click
  - mcp
  - pydantic
  - rich (for enhanced terminal output)
  - questionary (for interactive prompts)
  - pytest (dev dependency)
  - sqlite3 (standard library)
- Use `uv add <package>` to add libraries
- We're using uv to manage the project
- Add mcp-server-vibe-docs = "mcp_server_vibe_docs:main" to the project.scripts section in pyproject.toml

## API

```
# Initialize a new documentation structure
vibe init <project_name> [--template <template_name>]

# Update existing documentation
vibe update [--section <section_name>]

# Check feature implementation status
vibe status [--format <format>]
```

### Example API Calls
```
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

## Project Structure
- src/
  - mcp_server_vibe_docs/
    - server.py
      - serve(sqlite_database: Path | None) -> None
      - pass sqlite_database to every tool call (--db arg)
    - modules/
      - __init__.py
      - init_db.py
      - data_types.py
        - class Project(BaseModel)
        - class Template(BaseModel)
        - class Feature(BaseModel)
        - class Section(BaseModel)
      - constants.py
        - DEFAULT_SQLITE_DATABASE_PATH: Path = Path.home() / ".vibe_docs.db"
        - TEMPLATE_PATHS: Dict[str, Path]
      - functionality/
        - __init__.py
        - init.py
          - initialize_project(project_name: str, template: str = "default") -> None
        - update.py
          - update_documentation(section: Optional[str] = None) -> None
        - status.py
          - get_feature_status(format: str = "text") -> Union[str, dict]
      - templates/
        - default/
          - instructions/
            - getting_started.md
            - architecture.md
            - api_reference.md
            - deployment.md
            - contributing.md
          - features.md
        - api/
          - instructions/
            - endpoints.md
            - authentication.md
            - rate_limiting.md
            - versioning.md
          - features.md
    - tests/
      - __init__.py
      - functionality/
        - test_init.py
        - test_update.py
        - test_status.py
      - templates/
        - test_template_loading.py

## Features
- Project initialization with customizable templates
- Interactive prompts to fill in documentation details
- Feature status tracking with completion indicators
- Documentation update capability for evolving projects
- Multiple output formats for feature status (text, JSON)

## Template Structure

Each template follows a standardized structure that includes instruction files and a features tracking file:

### Default Template
```
templates/default/
├── instructions/
│   ├── getting_started.md       # Project setup and initial configuration
│   ├── architecture.md          # System architecture and design patterns
│   ├── api_reference.md         # API endpoints and usage examples
│   ├── deployment.md            # Deployment procedures and environments
│   └── contributing.md          # Contribution guidelines and workflows
├── features.md                  # Feature tracking with completion status
├── project_coding_docs.md       # AI knowledge base for the project
├── implementation_plan.md       # Step-by-step plan for AI execution
├── cursorrules.md               # Rules for Cursor AI assistance
└── windsurfrules.md             # Rules for Windsurf AI assistance
```

### API Template
```
templates/api/
├── instructions/
│   ├── endpoints.md             # API endpoints documentation
│   ├── authentication.md        # Authentication methods and security
│   ├── rate_limiting.md         # Rate limiting policies
│   ├── versioning.md            # API versioning strategy
│   ├── app_flow.md              # Application flow documentation
│   ├── backend_structure.md     # Backend architecture and structure
│   ├── frontend_guidelines.md   # Frontend development guidelines
│   ├── prd.md                   # Product requirements document
│   ├── project_status.md        # Current project status overview
│   └── tech_stack.md            # Technology stack documentation
├── features.md                  # Feature tracking with completion status
├── project_coding_docs.md       # AI knowledge base for the project
├── implementation_plan.md       # Step-by-step plan for AI execution
├── cursorrules.md               # Rules for Cursor AI assistance
└── windsurfrules.md             # Rules for Windsurf AI assistance
```

### Template File Contents

#### features.md
```markdown
# Project Features

This document tracks the implementation status of planned features.

## Core Features
- [ ] Feature 1: Description of feature 1
- [ ] Feature 2: Description of feature 2
- [x] Feature 3: Description of feature 3 (Completed)

## Future Enhancements
- [ ] Enhancement 1: Description of enhancement 1
- [ ] Enhancement 2: Description of enhancement 2
```

#### project_coding_docs.md
```markdown
# Project Coding Documentation

This document serves as an AI knowledge base for the project.

## Project Overview
{{project_overview}}

## Architecture
{{architecture_description}}

## Key Components
{{key_components}}

## Data Models
{{data_models}}

## API Endpoints
{{api_endpoints}}

## Development Practices
{{development_practices}}
```

#### implementation_plan.md
```markdown
# Implementation Plan

This document outlines the step-by-step plan for AI execution.

## Phase 1: Setup
- [ ] Step 1: {{step_1_description}}
- [ ] Step 2: {{step_2_description}}

## Phase 2: Core Implementation
- [ ] Step 3: {{step_3_description}}
- [ ] Step 4: {{step_4_description}}

## Phase 3: Testing and Refinement
- [ ] Step 5: {{step_5_description}}
- [ ] Step 6: {{step_6_description}}

## Phase 4: Deployment
- [ ] Step 7: {{step_7_description}}
- [ ] Step 8: {{step_8_description}}
```

#### cursorrules.md
```markdown
# Cursor AI Rules

## Project: {{project_name}}

### General Guidelines
- {{guideline_1}}
- {{guideline_2}}

### Code Style
- {{code_style_1}}
- {{code_style_2}}

### Testing Requirements
- {{testing_requirement_1}}
- {{testing_requirement_2}}

### Documentation Standards
- {{documentation_standard_1}}
- {{documentation_standard_2}}
```

#### instructions/getting_started.md (Example)
```markdown
# Getting Started

## Project: {{project_name}}

### Prerequisites
- {{prerequisite_1}}
- {{prerequisite_2}}

### Installation
```bash
{{installation_command}}
```

### Configuration
{{configuration_instructions}}

### Quick Start
{{quick_start_guide}}
```

During initialization, the user will be prompted to fill in the placeholders (text surrounded by `{{}}`) with project-specific information.

## Implementation Workflow

1. Create "project coding docs" as AI knowledge base
   - Generate comprehensive documentation about the project architecture and components
   - Ensure AI has full context for code generation and debugging

2. Create "implementation plan" so AI can execute code
   - Break down development into clear, manageable steps
   - Define acceptance criteria for each step

3. Create "instructions" folder and attach docs in Cursor
   - Organize documentation in a structured manner
   - Make documentation easily accessible within the IDE

4. Add cursorrules/windsurfrules files
   - Define guidelines for AI assistance in Cursor and Windsurf
   - Ensure consistent code style and practices

5. Use Sonnet 3.5/3.7 to code and GPT o1 to debug
   - Leverage appropriate AI models for different tasks
   - Optimize the development workflow

6. Ask AI to update implementation plan after each step
   - Track progress and adjust the plan as needed
   - Ensure the implementation stays on track

## Validation (close the loop)
- Use `uv run pytest` to validate the tests pass
- Use `uv run mcp-server-vibe-docs --help` to validate the MCP server works
- Verify template files are properly created during initialization
- Check that feature status correctly reflects implementation progress
- Confirm that AI can successfully follow the implementation plan
