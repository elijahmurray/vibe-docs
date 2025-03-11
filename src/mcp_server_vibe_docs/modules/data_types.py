"""Data type definitions for vibe-docs."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


class Feature(BaseModel):
    """Represents a project feature to be tracked."""
    
    id: Optional[int] = None
    project_id: int
    name: str
    description: str
    completed: bool = False
    category: str = "Core Features"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Section(BaseModel):
    """Represents a documentation section."""
    
    id: Optional[int] = None
    project_id: int
    name: str
    file_path: Path
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Template(BaseModel):
    """Represents a documentation template."""
    
    id: Optional[int] = None
    name: str
    path: Path
    description: str = ""
    sections: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)


class Project(BaseModel):
    """Represents a documentation project."""
    
    id: Optional[int] = None
    name: str
    path: Path
    template: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = []
    
    @property
    def normalized_tags(self) -> List[str]:
        """Normalize tags to lowercase, trimmed with dashes instead of spaces/underscores."""
        return [
            tag.lower().strip().replace(" ", "-").replace("_", "-")
            for tag in self.tags
        ]