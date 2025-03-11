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
    
    console.print(Panel.fit(
        f"✅ Project '{project_name}' initialized successfully with the '{template}' template",
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
        "Please provide information to populate your documentation templates:",
        title="Template Configuration",
        border_style="blue"
    ))
    
    responses = {
        "project_name": project_name,
        "project_overview": questionary.text(
            "Project Overview:"
        ).ask(),
        "architecture_description": questionary.text(
            "Architecture Description:"
        ).ask(),
        "key_components": questionary.text(
            "Key Components (comma-separated):"
        ).ask(),
        "prerequisite_1": questionary.text(
            "Prerequisite 1:"
        ).ask(),
        "prerequisite_2": questionary.text(
            "Prerequisite 2:"
        ).ask(),
        "installation_command": questionary.text(
            "Installation Command:"
        ).ask(),
        "guideline_1": questionary.text(
            "Coding Guideline 1:"
        ).ask(),
        "guideline_2": questionary.text(
            "Coding Guideline 2:"
        ).ask(),
    }
    
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
    # Copy instructions
    instructions_src = template_dir / "instructions"
    instructions_dest = docs_dir / "instructions"
    
    if instructions_src.exists():
        for file_path in instructions_src.glob("*.md"):
            _copy_and_populate_file(file_path, instructions_dest / file_path.name, values, project_id, cursor)
    
    # Copy other template files
    for file_name in ["features.md", "project_coding_docs.md", "implementation_plan.md", 
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