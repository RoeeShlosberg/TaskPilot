from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from app.models.task_model import Priority


class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime  # Required field
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None
    mini_tasks: Optional[Dict[str, bool]] = None


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    completed: Optional[bool] = None
    tags: Optional[List[str]] = None
    mini_tasks: Optional[Dict[str, bool]] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    completed: bool
    created_at: datetime
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None
    mini_tasks: Optional[Dict[str, bool]] = None
