# API Reference

## Project: {{project_name}}

## CLI Commands

### Initialize
```bash
vibe init <project_name> [--template <template_name>]
```

Initializes a new documentation structure with the specified project name and optional template.

**Arguments:**
- `project_name`: Name of the project (required)
- `--template`: Template to use (default or api)

### Update
```bash
vibe update [--section <section_name>]
```

Updates the documentation, either all sections or a specific section.

**Arguments:**
- `--section`: Optional section name to update

### Status
```bash
vibe status [--format <format>]
```

Checks the feature implementation status.

**Arguments:**
- `--format`: Output format (text or json)