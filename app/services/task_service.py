import json
from typing import Optional, List, Dict
from datetime import datetime
from app.models.task_model import Task, Priority
from app.models.request_models import TaskResponse


class TaskService:
    
    def __init__(self, task_repository):
        self.task_repository = task_repository
    
    def create_task(
        self,
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
        saved_task = self.task_repository.create(task)
        
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
    
    def get_task_by_id(self, task_id: int) -> TaskResponse:
        """
        Get a task by ID
        """
        task = self.task_repository.get_by_id(task_id)
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
    
    def get_all_tasks(self) -> List[TaskResponse]:
        """
        Get all tasks
        """
        tasks = self.task_repository.get_all()

        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                due_date=task.due_date,
                completed=task.completed,
                created_at=task.created_at,
                priority=task.priority,
                tags=json.loads(task.tags) if task.tags else None,
                mini_tasks=json.loads(task.mini_tasks) if task.mini_tasks else None
            ) for task in tasks
        ]
    
    def update_task(
        self,
        task_id: int,
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
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        # Update only provided fields
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title.strip()
        
        if description is not None:
            task.description = description.strip() if description else None
        
        if due_date is not None:
            task.due_date = due_date
        
        if priority is not None:
            task.priority = priority
        
        if completed is not None:
            task.completed = completed
        
        if tags is not None:
            task.tags = json.dumps(tags)
        
        if mini_tasks is not None:
            task.mini_tasks = json.dumps(mini_tasks)
        
        updated_task = self.task_repository.update(task)
        
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
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID
        """
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        return self.task_repository.delete(task_id)
