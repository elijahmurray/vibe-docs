"""Tests for the feature status functionality."""

import os
import json
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from mcp_server_vibe_docs.modules.functionality.status import get_feature_status


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
    
    # Insert test features
    features = [
        ("Feature 1", "Description of feature 1", 0, "Core Features"),
        ("Feature 2", "Description of feature 2", 1, "Core Features"),
        ("Feature 3", "Description of feature 3", 0, "Core Features"),
        ("Enhancement 1", "Description of enhancement 1", 0, "Future Enhancements"),
        ("Enhancement 2", "Description of enhancement 2", 1, "Future Enhancements")
    ]
    
    for name, description, completed, category in features:
        cursor.execute(
            "INSERT INTO features (project_id, name, description, completed, category) VALUES (?, ?, ?, ?, ?)",
            (project_id, name, description, completed, category)
        )
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    os.close(fd)
    os.unlink(path)


def test_get_feature_status_text_format(temp_db):
    """Test getting feature status in text format."""
    with patch('rich.console.Console.print') as mock_print:
        result = get_feature_status(format="text", db_path=temp_db)
        
        # Verify console output was called
        assert mock_print.called
        
        # Verify result text
        assert "test-project" in result
        assert "2/5" in result  # 2 out of 5 features completed
        assert "40.0%" in result  # 40% completion rate


def test_get_feature_status_json_format(temp_db):
    """Test getting feature status in JSON format."""
    result = get_feature_status(format="json", db_path=temp_db)
    
    # Verify result is proper JSON
    assert isinstance(result, dict)
    
    # Verify content
    assert result["project"] == "test-project"
    assert result["total_features"] == 5
    assert result["completed_features"] == 2
    assert result["completion_percentage"] == 40.0
    
    # Verify categories
    assert "Core Features" in result["categories"]
    assert "Future Enhancements" in result["categories"]
    
    # Verify features in categories
    core_features = result["categories"]["Core Features"]
    assert len(core_features) == 3
    assert core_features[0]["name"] == "Feature 1"
    # SQLite might store booleans as integers (0 or 1), so check for either False or 0
    assert core_features[0]["completed"] is False or core_features[0]["completed"] == 0
    assert core_features[1]["name"] == "Feature 2"
    # SQLite might store booleans as integers (0 or 1), so check for either True or 1
    assert core_features[1]["completed"] is True or core_features[1]["completed"] == 1
    
    future_enhancements = result["categories"]["Future Enhancements"]
    assert len(future_enhancements) == 2
    assert future_enhancements[0]["name"] == "Enhancement 1"
    assert future_enhancements[0]["completed"] is False or future_enhancements[0]["completed"] == 0
    assert future_enhancements[1]["name"] == "Enhancement 2"
    assert future_enhancements[1]["completed"] is True or future_enhancements[1]["completed"] == 1


def test_get_feature_status_no_database():
    """Test getting feature status with no database."""
    # Use a non-existent path
    non_existent_path = Path("/non/existent/path/db.sqlite")
    
    # Test text format
    text_result = get_feature_status(format="text", db_path=non_existent_path)
    assert "Error: No projects found" in text_result
    
    # Test JSON format
    json_result = get_feature_status(format="json", db_path=non_existent_path)
    assert "error" in json_result
    assert "No projects found" in json_result["error"]


def test_get_feature_status_no_projects(temp_db):
    """Test getting feature status with no projects in database."""
    # Clear the projects table
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects")
    conn.commit()
    conn.close()
    
    # Test text format
    text_result = get_feature_status(format="text", db_path=temp_db)
    assert "Error: No projects found" in text_result
    
    # Test JSON format
    json_result = get_feature_status(format="json", db_path=temp_db)
    assert "error" in json_result
    assert "No projects found" in json_result["error"]