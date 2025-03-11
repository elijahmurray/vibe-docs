"""Feature status functionality."""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Union, Optional, Any

from rich.console import Console
from rich.table import Table

from ..constants import DEFAULT_SQLITE_DATABASE_PATH


console = Console()


def get_feature_status(format: str = "text", db_path: Optional[Path] = None) -> Union[str, Dict[str, Any]]:
    """Get the implementation status of features.
    
    Args:
        format: Output format (text or json)
        db_path: Path to the SQLite database file
        
    Returns:
        Feature status in the specified format
    """
    if not db_path:
        db_path = DEFAULT_SQLITE_DATABASE_PATH
    
    if not db_path.exists():
        if format == "json":
            return {"error": "No projects found. Initialize a project first using 'vibe init'."}
        return "Error: No projects found. Initialize a project first using 'vibe init'."
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get active project (most recently updated)
    cursor.execute(
        "SELECT id, name FROM projects ORDER BY updated_at DESC LIMIT 1"
    )
    project = cursor.fetchone()
    
    if not project:
        conn.close()
        if format == "json":
            return {"error": "No projects found. Initialize a project first using 'vibe init'."}
        return "Error: No projects found. Initialize a project first using 'vibe init'."
    
    project_id = project["id"]
    project_name = project["name"]
    
    # Get features grouped by category
    cursor.execute(
        """
        SELECT name, description, completed, category 
        FROM features 
        WHERE project_id = ? 
        ORDER BY category, id
        """,
        (project_id,)
    )
    features = cursor.fetchall()
    
    # Group features by category
    features_by_category: Dict[str, List[Dict[str, Any]]] = {}
    for feature in features:
        category = feature["category"]
        if category not in features_by_category:
            features_by_category[category] = []
        
        features_by_category[category].append({
            "name": feature["name"],
            "description": feature["description"],
            "completed": feature["completed"]
        })
    
    # Calculate completion stats
    total_features = len(features)
    completed_features = sum(1 for feature in features if feature["completed"])
    completion_percentage = (completed_features / total_features * 100) if total_features > 0 else 0
    
    # Format output
    if format == "json":
        return {
            "project": project_name,
            "total_features": total_features,
            "completed_features": completed_features,
            "completion_percentage": completion_percentage,
            "categories": features_by_category
        }
    else:  # text format
        output = []
        
        # Create table
        table = Table(title=f"Feature Status for {project_name}")
        table.add_column("Category", style="cyan")
        table.add_column("Feature", style="green")
        table.add_column("Description")
        table.add_column("Status", justify="center")
        
        for category, category_features in features_by_category.items():
            for i, feature in enumerate(category_features):
                name = feature["name"]
                description = feature["description"]
                completed = feature["completed"]
                
                # Only show category name in first row of the category
                cat_display = category if i == 0 else ""
                status = "✅" if completed else "❌"
                
                table.add_row(cat_display, name, description, status)
        
        # Add summary row
        table.add_section()
        table.add_row("", "", f"Completed: {completed_features}/{total_features}", f"{completion_percentage:.1f}%")
        
        console.print(table)
        
        # Return simple string for MCP
        return f"Project: {project_name} - {completed_features}/{total_features} features completed ({completion_percentage:.1f}%)"