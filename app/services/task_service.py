import json
from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import Session
from app.models.task_model import Task, Priority
from app.models.request_models import TaskResponse, TaskUpdateRequest
from app.repositories import task_repository
import logging
logger = logging.getLogger(__name__)

class TaskService:
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_task(
        self,
        user_id: int,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        mini_tasks: Optional[Dict[str, bool]] = None
    ) -> TaskResponse:
        """
        Create a new task with business logic validation
        """
        # Validate required fields
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")
        
        if not due_date:
            raise ValueError("Due date is required")
        
        # Convert complex types to JSON strings for storage
        tags_json = json.dumps(tags) if tags else None
        mini_tasks_json = json.dumps(mini_tasks) if mini_tasks else None
        
        # Create task object
        task = Task(
            title=title.strip(),
            description=description.strip() if description else None,
            due_date=due_date,
            priority=priority,
            tags=tags_json,
            mini_tasks=mini_tasks_json
        )
        
        # Save via repository
        saved_task = task_repository.create_task(self.db, task, user_id)
        
        # Convert back to response format with proper JSON objects
        return TaskResponse(
            id=saved_task.id,
            title=saved_task.title,
            description=saved_task.description,
            due_date=saved_task.due_date,
            completed=saved_task.completed,
            created_at=saved_task.created_at,
            priority=saved_task.priority,
            tags=json.loads(saved_task.tags) if saved_task.tags else None,
            mini_tasks=json.loads(saved_task.mini_tasks) if saved_task.mini_tasks else None
        )
    
    def get_task_by_id(self, task_id: int, user_id: int) -> TaskResponse:
        """
        Get a task by ID
        """
        task = task_repository.get_task_by_id(self.db, task_id, user_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            completed=task.completed,
            created_at=task.created_at,
            priority=task.priority,
            tags=json.loads(task.tags) if task.tags else None,
            mini_tasks=json.loads(task.mini_tasks) if task.mini_tasks else None
        )
    
    def get_all_tasks(self, user_id: int) -> List[TaskResponse]:
        """
        Get all tasks
        """
        tasks = task_repository.get_all_tasks(self.db, user_id)

        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                due_date=task.due_date,
                completed=task.completed,
                created_at=task.created_at,
                priority=task.priority,                tags=json.loads(task.tags) if task.tags else None,
                mini_tasks=json.loads(task.mini_tasks) if task.mini_tasks else None
            ) for task in tasks
        ]
    
    def update_task(
        self,
        task_id: int,
        user_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[Priority] = None,
        completed: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        mini_tasks: Optional[Dict[str, bool]] = None
    ) -> TaskResponse:
        """
        Update an existing task
        """
        if title is not None and not title.strip():
            raise ValueError("Title cannot be empty")

        # Create task update object with only provided fields
        update_data = {}
        if title is not None:
            update_data["title"] = title.strip()
        if description is not None:
            update_data["description"] = description.strip() if description else None
        if due_date is not None:
            update_data["due_date"] = due_date
        if priority is not None:
            update_data["priority"] = priority
        if completed is not None:
            update_data["completed"] = completed
        if tags is not None:
            update_data["tags"] = json.dumps(tags) if tags else None
        if mini_tasks is not None:
            update_data["mini_tasks"] = json.dumps(mini_tasks) if mini_tasks else None

        task_update = TaskUpdateRequest(**update_data)
        
        updated_task = task_repository.update_task(
            session=self.db, 
            task_id=task_id, 
            task_update=task_update, 
            user_id=user_id
        )

        if not updated_task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        return TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            due_date=updated_task.due_date,
            completed=updated_task.completed,
            created_at=updated_task.created_at,
            priority=updated_task.priority,
            tags=json.loads(updated_task.tags) if updated_task.tags else None,
            mini_tasks=json.loads(updated_task.mini_tasks) if updated_task.mini_tasks else None
        )
    
    def delete_task(self, task_id: int, user_id: int) -> bool:
        """
        Delete a task by ID
        """
        success = task_repository.delete_task(self.db, task_id, user_id)
        return success
