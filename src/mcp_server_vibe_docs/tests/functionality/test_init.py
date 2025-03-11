"""Tests for the project initialization functionality."""

import os
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from mcp_server_vibe_docs.modules.functionality.init import initialize_project, _extract_features
from mcp_server_vibe_docs.modules.data_types import Project


@pytest.fixture
def temp_db():
    """Create a temporary database file."""
    fd, path = tempfile.mkstemp()
    yield Path(path)
    os.close(fd)
    os.unlink(path)


@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


def test_initialize_project(temp_db, temp_dir):
    """Test project initialization."""
    # Explicitly call init_db to ensure the tables exist
    from mcp_server_vibe_docs.modules.init_db import init_db
    init_db(temp_db)
    
    with patch('questionary.text') as mock_text, \
            patch('mcp_server_vibe_docs.modules.functionality.init._create_template_files') as mock_create_files, \
            patch('mcp_server_vibe_docs.modules.functionality.init._extract_features', return_value=[]) as mock_extract:
        
        # Mock questionary responses
        mock_text.return_value.ask.side_effect = [
            "Project description",
            "Microservice architecture",
            "API, Database, Frontend",
            "Python 3.13+",
            "Docker",
            "pip install my-project",
            "Follow PEP 8",
            "Write tests for all functions",
        ]
        
        # Set current working directory to temp_dir
        with patch('pathlib.Path.cwd', return_value=temp_dir):
            # Run the initialization
            result = initialize_project("test-project", "default", temp_db)
            
            # Verify result
            assert "initialized successfully" in result
            
            # Verify directory creation
            project_dir = temp_dir / "test-project"
            assert project_dir.exists()
            
            # Verify database creation
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name, path, template FROM projects")
            project = cursor.fetchone()
            assert project is not None
            assert project[0] == "test-project"
            assert project[1] == str(project_dir)
            assert project[2] == "default"
            conn.close()


def test_extract_features(temp_dir):
    """Test feature extraction from features.md file."""
    # Create a test features.md file
    features_file = temp_dir / "features.md"
    content = """# Project Features

This document tracks the implementation status of planned features.

## Core Features
- [ ] Feature 1: Description of feature 1
- [x] Feature 2: Description of feature 2

## Future Enhancements
- [ ] Enhancement 1: Description of enhancement 1
"""
    features_file.write_text(content)
    
    # Extract features
    features = _extract_features(features_file)
    
    # Verify extraction
    assert len(features) == 3
    
    assert features[0]["name"] == "Feature 1"
    assert features[0]["description"] == "Description of feature 1"
    assert features[0]["completed"] is False
    assert features[0]["category"] == "Core Features"
    
    assert features[1]["name"] == "Feature 2"
    assert features[1]["description"] == "Description of feature 2"
    assert features[1]["completed"] is True
    assert features[1]["category"] == "Core Features"
    
    assert features[2]["name"] == "Enhancement 1"
    assert features[2]["description"] == "Description of enhancement 1"
    assert features[2]["completed"] is False
    assert features[2]["category"] == "Future Enhancements"