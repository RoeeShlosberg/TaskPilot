from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    
    priority: Optional[Priority] = None
    tags: Optional[str] = None       # JSON array: '["work", "personal"]'
    mini_tasks: Optional[str] = None # JSON object: '{"Setup env": true, "Write code": false}'
