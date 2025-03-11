"""Initialize the SQLite database for vibe-docs."""

import sqlite3
from pathlib import Path


def init_db(db_path: Path) -> None:
    """Initialize the SQLite database with the required schema.
    
    Args:
        db_path: Path to the SQLite database file
    """
    # Create parent directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        template TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create project_tags table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_tags (
        project_id INTEGER,
        tag TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
        PRIMARY KEY (project_id, tag)
    )
    """)
    
    # Create features table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS features (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        completed BOOLEAN DEFAULT 0,
        category TEXT DEFAULT 'Core Features',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    )
    """)
    
    # Create sections table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    )
    """)
    
    # Create templates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        path TEXT NOT NULL,
        description TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create template_sections table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS template_sections (
        template_id INTEGER,
        section_name TEXT NOT NULL,
        FOREIGN KEY (template_id) REFERENCES templates (id) ON DELETE CASCADE,
        PRIMARY KEY (template_id, section_name)
    )
    """)
    
    conn.commit()
    conn.close()