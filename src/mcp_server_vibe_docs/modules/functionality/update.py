"""Documentation update functionality."""

import os
import sqlite3
import json
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

import anthropic
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..constants import DEFAULT_SQLITE_DATABASE_PATH


console = Console()


async def analyze_codebase_with_claude(
    project_path: Path, 
    features_path: Path,
    api_key: str
) -> Dict[str, bool]:
    """Analyze codebase with Claude to determine feature completion status.
    
    Args:
        project_path: Path to the project
        features_path: Path to the features.md file
        api_key: Anthropic API key
        
    Returns:
        Dictionary mapping feature names to completion status
    """
    # Create Claude client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Read features file
    with open(features_path, "r") as f:
        features_content = f.read()
    
    # Get a sample of the codebase (max 100 files)
    code_samples = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Analyzing project files...", total=None)
        
        # Skip common directories that don't contain application code
        exclude_dirs = {".git", "node_modules", "dist", "build", ".venv", "__pycache__"}
        
        # Find all code files
        code_files = []
        for root, dirs, files in os.walk(project_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # Only include common code file extensions
            for file in files:
                if any(file.endswith(ext) for ext in [".js", ".jsx", ".ts", ".tsx", ".py", ".go", ".java", ".rb", ".php", ".html", ".css", ".cs"]):
                    code_files.append(os.path.join(root, file))
        
        # Limit to 100 files max
        if len(code_files) > 100:
            code_files = code_files[:100]
        
        # Read files
        for file_path in code_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    relative_path = os.path.relpath(file_path, project_path)
                    content = f.read()
                    code_samples.append(f"File: {relative_path}\n\n```\n{content[:2000]}...\n```\n\n")
            except Exception as e:
                # Skip files that can't be read
                pass
    
    # Prepare prompt for Claude
    code_context = "\n".join(code_samples[:10])  # Limit to first 10 files to stay within token limits
    
    prompt = f"""I'll provide you with a features list from a project and some code samples. Please analyze the code and determine which features appear to be implemented.

Features list:
{features_content}

Code samples:
{code_context}

For each feature in the features list, determine if it appears to be implemented based on the code samples.
Return your analysis as a JSON object with feature names as keys and boolean values (true if implemented, false if not).
Format your response as a valid JSON object and nothing else.

Example:
```json
{{
  "User authentication": true,
  "Resource management API": false,
  "Real-time data synchronization": false
}}
```
"""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Claude is analyzing your codebase...", total=None)
        
        try:
            # Send to Claude
            response = await asyncio.to_thread(
                client.messages.create,
                model="claude-3-5-sonnet-20240620",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract JSON from the response
            content = response.content[0].text
            
            # Find JSON in the response (it might be wrapped in code blocks)
            if "```json" in content:
                json_text = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_text = content.split("```")[1].split("```")[0].strip()
            else:
                json_text = content.strip()
            
            # Parse result
            result = json.loads(json_text)
            return result
            
        except Exception as e:
            console.print(f"[red]Error analyzing codebase: {str(e)}[/red]")
            return {}


def update_documentation(section: Optional[str] = None, db_path: Optional[Path] = None, use_ai: bool = False, api_key: Optional[str] = None) -> str:
    """Update existing documentation.
    
    Args:
        section: Optional section name to update
        db_path: Path to the SQLite database file
        use_ai: Whether to use AI for feature detection
        api_key: Anthropic API key (required if use_ai is True)
        
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
    
    # Check if we need to use AI for feature detection
    if use_ai and not api_key:
        # Try to get API key from environment variable
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        # If still not found, prompt the user
        if not api_key:
            console.print("[yellow]AI feature detection requires an Anthropic API key.[/yellow]")
            use_anthropic = questionary.confirm(
                "Do you want to provide an Anthropic API key for AI feature detection?",
                default=True
            ).ask()
            
            if use_anthropic:
                api_key = questionary.password(
                    "Enter your Anthropic API key (will not be stored):"
                ).ask()
            else:
                use_ai = False
                console.print("[yellow]Continuing without AI feature detection...[/yellow]")
    
    # Create an async event loop to run the async functions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
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
                # Run async function
                loop.run_until_complete(
                    _update_features(section_path, project_path, project_id, cursor, use_ai, api_key)
                )
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
    
    # Close the event loop
    loop.close()
    
    # Update project timestamp
    cursor.execute(
        "UPDATE projects SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (project_id,)
    )
    
    conn.commit()
    conn.close()
    
    return f"Documentation updated successfully for project: {project_name}"


async def _update_features(
    features_path: Path, 
    project_path: Path,
    project_id: int, 
    cursor: sqlite3.Cursor,
    use_ai: bool = False, 
    api_key: Optional[str] = None
) -> None:
    """Update features in features.md file and database.
    
    Args:
        features_path: Path to the features.md file
        project_path: Path to the project root
        project_id: Project ID in the database
        cursor: Database cursor
        use_ai: Whether to use AI for feature detection
        api_key: Anthropic API key (required if use_ai is True)
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
    
    # If using AI, analyze codebase to detect feature completion
    ai_feature_status = {}
    if use_ai and api_key:
        try:
            console.print("[cyan]Using Claude to analyze your codebase and detect completed features...[/cyan]")
            ai_feature_status = await analyze_codebase_with_claude(project_path, features_path, api_key)
            
            if ai_feature_status:
                console.print(Panel.fit(
                    "Claude has analyzed your codebase and detected the following features as implemented:\n" +
                    "\n".join([f"- {name}" for name, status in ai_feature_status.items() if status]),
                    title="AI Feature Detection",
                    border_style="green"
                ))
        except Exception as e:
            console.print(f"[red]Error analyzing codebase with Claude: {str(e)}[/red]")
            console.print("[yellow]Continuing with manual feature update...[/yellow]")
    
    # Update feature status
    for category, features in features_by_category.items():
        console.print(f"\n[bold]{category}:[/bold]")
        
        for feature in features:
            feature_id = feature["id"]
            feature_name = feature["name"]
            feature_description = feature["description"]
            completed = feature["completed"]
            
            # Check if AI detected this feature
            ai_detected = None
            if use_ai and api_key and ai_feature_status:
                for ai_feature_name, ai_status in ai_feature_status.items():
                    if feature_name.lower() in ai_feature_name.lower() or ai_feature_name.lower() in feature_name.lower():
                        ai_detected = ai_status
                        break
            
            # Set default based on AI detection or current status
            default_value = ai_detected if ai_detected is not None else completed
            
            # AI recommendation text
            ai_text = ""
            if ai_detected is not None:
                ai_text = " [green](AI detected as implemented)[/green]" if ai_detected else " [yellow](AI detected as not implemented)[/yellow]"
            
            # Ask user to confirm or update status
            prompt = f"{feature_name}: {feature_description}{ai_text}"
            
            status = questionary.select(
                prompt,
                choices=[
                    {"name": "✅ Completed", "value": True},
                    {"name": "❌ Not Completed", "value": False},
                    {"name": "Skip (no change)", "value": None}
                ],
                default="✅ Completed" if default_value else "❌ Not Completed"
            ).ask()
            
            # If skipped, use current status
            if status is None:
                continue
                
            # Update if changed
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