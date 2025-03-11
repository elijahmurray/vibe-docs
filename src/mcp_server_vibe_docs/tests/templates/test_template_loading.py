"""Tests for template loading functionality."""

import os
from pathlib import Path

import pytest

from mcp_server_vibe_docs.modules.constants import TEMPLATE_PATHS


def test_template_paths_exist():
    """Test that template paths defined in constants exist."""
    for template_name, template_path in TEMPLATE_PATHS.items():
        assert template_path.exists(), f"Template path for {template_name} does not exist: {template_path}"


def test_template_structure():
    """Test that templates have the required structure."""
    for template_name, template_path in TEMPLATE_PATHS.items():
        # Check for required files
        assert (template_path / "features.md").exists(), f"features.md missing for {template_name}"
        assert (template_path / "project_coding_docs.md").exists(), f"project_coding_docs.md missing for {template_name}"
        assert (template_path / "implementation_plan.md").exists(), f"implementation_plan.md missing for {template_name}"
        assert (template_path / "cursorrules.md").exists(), f"cursorrules.md missing for {template_name}"
        assert (template_path / "windsurfrules.md").exists(), f"windsurfrules.md missing for {template_name}"
        
        # Check for instructions directory
        instructions_dir = template_path / "instructions"
        assert instructions_dir.exists(), f"instructions directory missing for {template_name}"
        assert instructions_dir.is_dir(), f"instructions is not a directory for {template_name}"
        
        # Check that instructions directory has at least one file
        instruction_files = list(instructions_dir.glob("*.md"))
        assert len(instruction_files) > 0, f"No instruction files found for {template_name}"


def test_default_template_contents():
    """Test that the default template has the required content."""
    default_template_path = TEMPLATE_PATHS["default"]
    
    # Check features.md
    features_md = default_template_path / "features.md"
    content = features_md.read_text()
    assert "# Project Features" in content
    assert "## Core Features" in content
    assert "## Future Enhancements" in content
    
    # Check project_coding_docs.md
    project_docs_md = default_template_path / "project_coding_docs.md"
    content = project_docs_md.read_text()
    assert "# Project Coding Documentation" in content
    assert "{{project_overview}}" in content
    
    # Check implementation_plan.md
    impl_plan_md = default_template_path / "implementation_plan.md"
    content = impl_plan_md.read_text()
    assert "# Implementation Plan" in content
    assert "## Phase 1: Setup" in content


def test_api_template_contents():
    """Test that the API template has the required content."""
    api_template_path = TEMPLATE_PATHS["api"]
    
    # Check features.md
    features_md = api_template_path / "features.md"
    content = features_md.read_text()
    assert "# Project Features" in content
    
    # Check specific API instructions
    instructions_dir = api_template_path / "instructions"
    
    endpoints_md = instructions_dir / "endpoints.md"
    assert endpoints_md.exists()
    content = endpoints_md.read_text()
    assert "# API Endpoints" in content
    
    auth_md = instructions_dir / "authentication.md"
    assert auth_md.exists()
    content = auth_md.read_text()
    assert "# Authentication" in content
    
    rate_limiting_md = instructions_dir / "rate_limiting.md"
    assert rate_limiting_md.exists()
    content = rate_limiting_md.read_text()
    assert "# Rate Limiting" in content