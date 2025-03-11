"""Documentation update functionality."""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

import questionary
from rich.console import Console
from rich.panel import Panel

from ..constants import DEFAULT_SQLITE_DATABASE_PATH


console = Console()


def update_documentation(section: Optional[str] = None, db_path: Optional[Path] = None) -> str:
    """Update existing documentation.
    
    Args:
        section: Optional section name to update
        db_path: Path to the SQLite database file
        
    Returns:
        A message indicating the update status
    """
    if not db_path:
        db_path = DEFAULT_SQLITE_DATABASE_PATH
    
    if not db_path.exists():
        return "Error: No projects found. Initialize a project first using 'vibe init'."
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get active project (most recently updated)
    cursor.execute(
        "SELECT id, name, path FROM projects ORDER BY updated_at DESC LIMIT 1"
    )
    project = cursor.fetchone()
    
    if not project:
        conn.close()
        return "Error: No projects found. Initialize a project first using 'vibe init'."
    
    project_id = project["id"]
    project_name = project["name"]
    project_path = Path(project["path"])
    
    console.print(Panel.fit(
        f"Updating documentation for project: {project_name}",
        title="Vibe Docs",
        border_style="blue"
    ))
    
    # Get sections to update
    if section:
        cursor.execute(
            "SELECT id, name, file_path, content FROM sections WHERE project_id = ? AND name = ?",
            (project_id, section)
        )
        sections = cursor.fetchall()
        if not sections:
            conn.close()
            return f"Error: Section '{section}' not found"
    else:
        cursor.execute(
            "SELECT id, name, file_path, content FROM sections WHERE project_id = ?",
            (project_id,)
        )
        sections = cursor.fetchall()
    
    # Update each section
    for section_data in sections:
        section_id = section_data["id"]
        section_name = section_data["name"]
        section_path = project_path / section_data["file_path"]
        
        if not section_path.exists():
            console.print(f"[yellow]Warning: Section file {section_path} not found, skipping[/yellow]")
            continue
        
        # Read current content
        with open(section_path, "r") as f:
            current_content = f.read()
        
        # Get user input for updating
        console.print(f"\n[bold]Updating {section_name}:[/bold]")
        update_choice = questionary.select(
            f"Would you like to update {section_name}?",
            choices=["Yes", "No"]
        ).ask()
        
        if update_choice == "Yes":
            # Handle features.md differently
            if section_name == "features":
                _update_features(section_path, project_id, cursor)
            else:
                new_content = questionary.text(
                    "Enter new content (or press Enter to keep current content):",
                    default=current_content
                ).ask()
                
                if new_content != current_content:
                    # Update file
                    with open(section_path, "w") as f:
                        f.write(new_content)
                    
                    # Update database
                    cursor.execute(
                        "UPDATE sections SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                        (new_content, section_id)
                    )
    
    # Update project timestamp
    cursor.execute(
        "UPDATE projects SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (project_id,)
    )
    
    conn.commit()
    conn.close()
    
    return f"Documentation updated successfully for project: {project_name}"


def _update_features(features_path: Path, project_id: int, cursor: sqlite3.Cursor) -> None:
    """Update features in features.md file and database.
    
    Args:
        features_path: Path to the features.md file
        project_id: Project ID in the database
        cursor: Database cursor
    """
    # Get existing features from database
    cursor.execute(
        "SELECT id, name, description, completed, category FROM features WHERE project_id = ? ORDER BY category, id",
        (project_id,)
    )
    existing_features = cursor.fetchall()
    
    # Group features by category
    features_by_category: Dict[str, List[Dict[str, Any]]] = {}
    for feature in existing_features:
        category = feature["category"]
        if category not in features_by_category:
            features_by_category[category] = []
        
        features_by_category[category].append({
            "id": feature["id"],
            "name": feature["name"],
            "description": feature["description"],
            "completed": feature["completed"]
        })
    
    # Update feature status
    for category, features in features_by_category.items():
        console.print(f"\n[bold]{category}:[/bold]")
        
        for feature in features:
            feature_id = feature["id"]
            feature_name = feature["name"]
            feature_description = feature["description"]
            completed = feature["completed"]
            
            status = questionary.select(
                f"{feature_name}: {feature_description}",
                choices=[
                    {"name": "✅ Completed", "value": True},
                    {"name": "❌ Not Completed", "value": False}
                ],
                default="✅ Completed" if completed else "❌ Not Completed"
            ).ask()
            
            if status != completed:
                cursor.execute(
                    "UPDATE features SET completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (status, feature_id)
                )
    
    # Add new feature option
    add_new = questionary.select(
        "Would you like to add a new feature?",
        choices=["Yes", "No"]
    ).ask()
    
    if add_new == "Yes":
        category = questionary.select(
            "Select category:",
            choices=list(features_by_category.keys()) + ["New Category"]
        ).ask()
        
        if category == "New Category":
            category = questionary.text("Enter new category name:").ask()
        
        name = questionary.text("Feature name:").ask()
        description = questionary.text("Feature description:").ask()
        completed = questionary.select(
            "Status:",
            choices=[
                {"name": "✅ Completed", "value": True},
                {"name": "❌ Not Completed", "value": False}
            ],
            default="❌ Not Completed"
        ).ask()
        
        cursor.execute(
            "INSERT INTO features (project_id, name, description, completed, category) VALUES (?, ?, ?, ?, ?)",
            (project_id, name, description, completed, category)
        )
    
    # Regenerate features.md
    _regenerate_features_file(features_path, project_id, cursor)


def _regenerate_features_file(features_path: Path, project_id: int, cursor: sqlite3.Cursor) -> None:
    """Regenerate the features.md file based on database content.
    
    Args:
        features_path: Path to the features.md file
        project_id: Project ID in the database
        cursor: Database cursor
    """
    # Get all features grouped by category
    cursor.execute(
        "SELECT name, description, completed, category FROM features WHERE project_id = ? ORDER BY category, id",
        (project_id,)
    )
    features = cursor.fetchall()
    
    # Group by category
    features_by_category = {}
    for feature in features:
        category = feature["category"]
        if category not in features_by_category:
            features_by_category[category] = []
        
        features_by_category[category].append({
            "name": feature["name"],
            "description": feature["description"],
            "completed": feature["completed"]
        })
    
    # Generate content
    lines = ["# Project Features", "", "This document tracks the implementation status of planned features.", ""]
    
    for category, category_features in features_by_category.items():
        lines.append(f"## {category}")
        
        for feature in category_features:
            name = feature["name"]
            description = feature["description"]
            completed = feature["completed"]
            
            checkbox = "[x]" if completed else "[ ]"
            lines.append(f"- {checkbox} {name}: {description}")
        
        lines.append("")
    
    # Write to file
    with open(features_path, "w") as f:
        f.write("\n".join(lines))