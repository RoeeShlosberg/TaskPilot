from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Union
from datetime import datetime
from app.models.task_model import Priority
import json


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
    tags: Optional[Union[List[str], str]] = None
    mini_tasks: Optional[Union[Dict[str, bool], str]] = None

    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v

    @field_validator('mini_tasks', mode='before')
    @classmethod
    def parse_mini_tasks(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v


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
