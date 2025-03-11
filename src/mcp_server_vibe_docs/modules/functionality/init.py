"""Project initialization functionality."""

import os
import sqlite3
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any

import questionary
from rich.console import Console
from rich.panel import Panel

from ..data_types import Project, Template, Feature
from ..constants import TEMPLATE_PATHS
from ..init_db import init_db


console = Console()


def initialize_project(project_name: str, template: str = "default", db_path: Optional[Path] = None) -> str:
    """Initialize a new documentation project with the specified template.
    
    Args:
        project_name: Name of the project
        template: Template to use (default or api)
        db_path: Path to the SQLite database file
        
    Returns:
        A message indicating successful initialization
    """
    if not db_path:
        from ..constants import DEFAULT_SQLITE_DATABASE_PATH
        db_path = DEFAULT_SQLITE_DATABASE_PATH
    
    # Initialize database if it doesn't exist
    if not db_path.exists():
        init_db(db_path)
    
    # Validate template
    if template not in TEMPLATE_PATHS:
        return f"Error: Template '{template}' not found. Available templates: {', '.join(TEMPLATE_PATHS.keys())}"
    
    # Create project directory
    project_dir = Path.cwd() / project_name
    if project_dir.exists():
        return f"Error: Directory '{project_dir}' already exists"
    
    project_dir.mkdir(parents=True)
    
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert project into database
    cursor.execute(
        "INSERT INTO projects (name, path, template) VALUES (?, ?, ?)",
        (project_name, str(project_dir), template)
    )
    project_id = cursor.lastrowid
    
    # Create documentation structure
    docs_dir = project_dir / "docs"
    docs_dir.mkdir()
    
    template_dir = TEMPLATE_PATHS[template]
    
    # Create template directories
    instructions_dir = docs_dir / "instructions"
    instructions_dir.mkdir()
    
    # Create instruction files with placeholders
    prompt_responses = _prompt_for_template_values(project_name)
    
    # Copy and populate template files
    _create_template_files(template_dir, docs_dir, prompt_responses, project_id, cursor)
    
    # Extract features from features.md and add to database
    features = _extract_features(docs_dir / "features.md")
    for feature in features:
        cursor.execute(
            "INSERT INTO features (project_id, name, description, completed, category) VALUES (?, ?, ?, ?, ?)",
            (project_id, feature["name"], feature["description"], feature["completed"], feature["category"])
        )
    
    conn.commit()
    conn.close()
    
    # Create detailed next steps message
    next_steps = [
        f"✅ Project '{project_name}' initialized successfully with the '{template}' template",
        "",
        "Next Steps:",
        "1. Review docs/README.md to understand the documentation structure",
        "2. Fill in the TODO sections in docs/project_coding_docs.md (primary AI knowledge base)",
        "3. Document your API endpoints and features",
        "4. Set up your AI coding assistant:",
        "   - Cursor: Add docs/project_coding_docs.md as knowledge and docs/cursorrules.md as rules",
        "   - Windsurf: Add docs/project_coding_docs.md to knowledge base",
        "   - Other AI tools: Reference docs/project_coding_docs.md in your prompts",
        "",
        f"Your documentation is located at: {project_dir}/docs"
    ]

    console.print(Panel.fit(
        "\n".join(next_steps),
        title="Vibe Docs",
        border_style="green"
    ))
    
    return f"Project '{project_name}' initialized successfully with the '{template}' template"


def _prompt_for_template_values(project_name: str) -> Dict[str, str]:
    """Prompt the user for template values.
    
    Args:
        project_name: Name of the project
        
    Returns:
        Dictionary of placeholder values
    """
    console.print(Panel.fit(
        "Please provide information to populate your documentation templates (press Enter to skip any question):",
        title="Template Configuration",
        border_style="blue"
    ))
    
    # Start with project type selection
    project_type = questionary.select(
        "What type of project is this?",
        choices=["fullstack", "api-only", "frontend-only", "library", "other"],
        default="fullstack"
    ).ask()
    
    # Ask if they want minimal scaffolding
    minimal_mode = questionary.confirm(
        "Would you like minimal scaffolding with TODOs to fill in later?", 
        default=True
    ).ask()
    
    responses = {
        "project_name": project_name,
        "project_type": project_type,
    }
    
    # If minimal mode, return with basic placeholders
    if minimal_mode:
        console.print("[green]✅ Using minimal mode with TODOs for you to fill in later[/green]")
        responses.update({
            "project_overview": "<!-- TODO: Add project overview -->",
            "key_components": "<!-- TODO: List key components -->",
            "api_description": "<!-- TODO: Describe your API -->",
            "frontend_stack": "<!-- TODO: Describe frontend technologies -->",
            "backend_stack": "<!-- TODO: Describe backend technologies -->",
            "data_models": "<!-- TODO: Document data models -->",
            "coding_standards": "<!-- TODO: Define coding standards -->",
        })
        return responses
    
    # Otherwise, ask detailed questions
    if project_type in ["fullstack", "frontend-only"]:
        frontend_stack = questionary.text(
            "Frontend Technologies (e.g., React, Vue, Angular):"
        ).ask() or "<!-- TODO: Document frontend technologies -->"
        responses["frontend_stack"] = frontend_stack
    
    if project_type in ["fullstack", "api-only"]:
        backend_stack = questionary.text(
            "Backend Technologies (e.g., Express, Django, Rails):"
        ).ask() or "<!-- TODO: Document backend technologies -->"
        responses["backend_stack"] = backend_stack
    
    # Common questions for all project types
    responses["project_overview"] = questionary.text(
        "Project Overview (brief description):"
    ).ask() or "<!-- TODO: Add project overview -->"
    
    responses["key_components"] = questionary.text(
        "Key Components (comma-separated):"
    ).ask() or "<!-- TODO: List key components -->"
    
    responses["api_description"] = questionary.text(
        "API Description (if applicable):"
    ).ask() or "<!-- TODO: Describe your API -->"
    
    responses["data_models"] = questionary.text(
        "Data Models (comma-separated):"
    ).ask() or "<!-- TODO: Document data models -->"
    
    responses["coding_standards"] = questionary.text(
        "Coding Standards (e.g., PEP 8, Airbnb style):"
    ).ask() or "<!-- TODO: Define coding standards -->"
    
    return responses


def _create_template_files(
    template_dir: Path, 
    docs_dir: Path, 
    values: Dict[str, str], 
    project_id: int, 
    cursor: sqlite3.Cursor
) -> None:
    """Create template files with populated values.
    
    Args:
        template_dir: Path to the template directory
        docs_dir: Path to the project docs directory
        values: Dictionary of placeholder values
        project_id: Project ID in the database
        cursor: Database cursor
    """
    # Create instructions directory
    instructions_dest = docs_dir / "instructions"
    instructions_dest.mkdir(exist_ok=True)
    
    # Copy instructions based on project type
    instructions_src = template_dir / "instructions"
    project_type = values.get("project_type", "fullstack")
    
    # Core files all projects need
    core_instruction_files = ["getting_started.md", "architecture.md", "api_reference.md"]
    
    # Add frontend/backend guidelines based on project type
    if project_type in ["fullstack", "frontend-only"]:
        core_instruction_files.append("frontend_guidelines.md")
    
    if project_type in ["fullstack", "api-only", "library"]:
        core_instruction_files.append("backend_guidelines.md")
    
    # Copy instruction files
    if instructions_src.exists():
        for file_name in core_instruction_files:
            file_path = instructions_src / file_name
            if file_path.exists():
                _copy_and_populate_file(file_path, instructions_dest / file_name, values, project_id, cursor)
    
    # Copy other template files
    for file_name in ["README.md", "features.md", "project_coding_docs.md", "implementation_plan.md", 
                      "cursorrules.md", "windsurfrules.md"]:
        src_file = template_dir / file_name
        if src_file.exists():
            _copy_and_populate_file(src_file, docs_dir / file_name, values, project_id, cursor)


def _copy_and_populate_file(
    src_path: Path, 
    dest_path: Path, 
    values: Dict[str, str], 
    project_id: int, 
    cursor: sqlite3.Cursor
) -> None:
    """Copy a file and populate placeholders with values.
    
    Args:
        src_path: Source file path
        dest_path: Destination file path
        values: Dictionary of placeholder values
        project_id: Project ID in the database
        cursor: Database cursor
    """
    if not src_path.exists():
        # For testing/development, create an empty file
        content = f"# {dest_path.stem.replace('_', ' ').title()}\n\nTODO: Add content"
    else:
        with open(src_path, "r") as f:
            content = f.read()
    
    # Replace placeholders
    for key, value in values.items():
        placeholder = f"{{{{{key}}}}}"
        content = content.replace(placeholder, value)
    
    # Write populated file
    with open(dest_path, "w") as f:
        f.write(content)
    
    # Add to sections table
    relative_path = dest_path.relative_to(dest_path.parent.parent.parent)
    cursor.execute(
        "INSERT INTO sections (project_id, name, file_path, content) VALUES (?, ?, ?, ?)",
        (project_id, dest_path.stem, str(relative_path), content)
    )


def _extract_features(features_file: Path) -> List[Dict[str, Any]]:
    """Extract features from the features.md file.
    
    Args:
        features_file: Path to the features.md file
        
    Returns:
        List of feature dictionaries
    """
    features = []
    current_category = "Core Features"
    
    if not features_file.exists():
        return features
    
    with open(features_file, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("## "):
            current_category = line[3:].strip()
        elif line.startswith("- [ ] ") or line.startswith("- [x] "):
            completed = line.startswith("- [x] ")
            rest = line[6:] if completed else line[6:]
            
            if ":" in rest:
                name, description = rest.split(":", 1)
                name = name.strip()
                description = description.strip()
                
                features.append({
                    "name": name,
                    "description": description,
                    "completed": completed,
                    "category": current_category
                })
    
    return features