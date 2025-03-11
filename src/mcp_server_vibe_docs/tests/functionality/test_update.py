"""Tests for the documentation update functionality."""

import os
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from mcp_server_vibe_docs.modules.functionality.update import update_documentation, _regenerate_features_file


@pytest.fixture
def temp_db():
    """Create a temporary database file with test data."""
    fd, path = tempfile.mkstemp()
    db_path = Path(path)
    
    # Create test database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        template TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE sections (
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
    
    cursor.execute("""
    CREATE TABLE features (
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
    
    # Insert test data
    cursor.execute(
        "INSERT INTO projects (name, path, template) VALUES (?, ?, ?)",
        ("test-project", "/tmp/test-project", "default")
    )
    project_id = cursor.lastrowid
    
    cursor.execute(
        "INSERT INTO sections (project_id, name, file_path, content) VALUES (?, ?, ?, ?)",
        (project_id, "getting_started", "docs/instructions/getting_started.md", "# Getting Started\n\nTest content")
    )
    
    cursor.execute(
        "INSERT INTO sections (project_id, name, file_path, content) VALUES (?, ?, ?, ?)",
        (project_id, "features", "docs/features.md", "# Features\n\n- [ ] Feature 1: Test feature")
    )
    
    cursor.execute(
        "INSERT INTO features (project_id, name, description, completed, category) VALUES (?, ?, ?, ?, ?)",
        (project_id, "Feature 1", "Test feature", 0, "Core Features")
    )
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    os.close(fd)
    os.unlink(path)


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        project_dir = Path(tmpdirname) / "test-project"
        project_dir.mkdir()
        
        # Create docs directory
        docs_dir = project_dir / "docs"
        docs_dir.mkdir()
        
        # Create instructions directory
        instructions_dir = docs_dir / "instructions"
        instructions_dir.mkdir()
        
        # Create test files
        getting_started_file = instructions_dir / "getting_started.md"
        getting_started_file.write_text("# Getting Started\n\nTest content")
        
        features_file = docs_dir / "features.md"
        features_file.write_text("# Features\n\n- [ ] Feature 1: Test feature")
        
        yield project_dir


def test_update_documentation_no_projects(temp_db):
    """Test update with no projects in database."""
    # Clear the projects table
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects")
    conn.commit()
    conn.close()
    
    # Run update
    result = update_documentation(db_path=temp_db)
    
    # Verify result
    assert "Error: No projects found" in result


def test_update_documentation(temp_db, temp_project_dir):
    """Test documentation update."""
    # Mock the project path to use our temp directory
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("UPDATE projects SET path = ?", (str(temp_project_dir),))
    conn.commit()
    conn.close()
    
    with patch('questionary.select') as mock_select, \
            patch('questionary.text') as mock_text:
        
        # Mock responses
        mock_select.return_value.ask.side_effect = ["Yes", "No", "No"]
        mock_text.return_value.ask.return_value = "# Getting Started\n\nUpdated content"
        
        # Run update
        result = update_documentation(db_path=temp_db)
        
        # Verify result
        assert "Documentation updated successfully" in result
        
        # Verify file content was updated
        getting_started_file = temp_project_dir / "docs" / "instructions" / "getting_started.md"
        assert getting_started_file.read_text() == "# Getting Started\n\nUpdated content"
        
        # Verify database was updated
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM sections WHERE name = 'getting_started'")
        content = cursor.fetchone()[0]
        conn.close()
        
        assert content == "# Getting Started\n\nUpdated content"


def test_regenerate_features_file(temp_db, temp_project_dir):
    """Test regeneration of features.md file."""
    # Create test features
    features = [
        {"name": "Feature 1", "description": "Description 1", "completed": False, "category": "Core Features"},
        {"name": "Feature 2", "description": "Description 2", "completed": True, "category": "Core Features"},
        {"name": "Enhancement 1", "description": "Enhancement desc", "completed": False, "category": "Future Enhancements"}
    ]
    
    # Setup database
    conn = sqlite3.connect(temp_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Clear existing features
    cursor.execute("DELETE FROM features")
    
    # Get project ID
    cursor.execute("SELECT id FROM projects LIMIT 1")
    project_id = cursor.fetchone()["id"]
    
    # Add test features
    for feature in features:
        cursor.execute(
            "INSERT INTO features (project_id, name, description, completed, category) VALUES (?, ?, ?, ?, ?)",
            (project_id, feature["name"], feature["description"], feature["completed"], feature["category"])
        )
    
    conn.commit()
    
    # Create features file
    features_file = temp_project_dir / "docs" / "features.md"
    
    # Regenerate the file
    _regenerate_features_file(features_file, project_id, cursor)
    
    # Verify file content
    content = features_file.read_text()
    
    # Check content includes all features
    assert "# Project Features" in content
    assert "## Core Features" in content
    assert "- [ ] Feature 1: Description 1" in content
    assert "- [x] Feature 2: Description 2" in content
    assert "## Future Enhancements" in content
    assert "- [ ] Enhancement 1: Enhancement desc" in content
    
    conn.close()