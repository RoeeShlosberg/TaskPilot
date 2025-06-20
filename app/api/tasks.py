from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.models.task_model import Task
from app.models.request_models import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository


router = APIRouter(prefix="/tasks", tags=["tasks"])


# Dependency injection functions
def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)


def get_task_service(repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(repo)


@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreateRequest, 
    service: TaskService = Depends(get_task_service)
):
    """
    Create a new task
    """
    try:
        task = service.create_task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            tags=task_data.tags,
            mini_tasks=task_data.mini_tasks
        )
        return task
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """
    Get a task by ID
    """
    try:
        task = service.get_task_by_id(task_id)
        return task
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    service: TaskService = Depends(get_task_service)
):
    """
    Get all tasks
    """
    try:
        tasks = service.get_all_tasks()
        return tasks
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    service: TaskService = Depends(get_task_service)
):
    """
    Update a task by ID
    """
    try:
        task = service.update_task(
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            completed=task_data.completed,
            tags=task_data.tags,
            mini_tasks=task_data.mini_tasks
        )
        return task
        
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """
    Delete a task by ID
    """
    try:
        success = service.delete_task(task_id)
        if success:
            return {"message": f"Task {task_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """
    Get a task by ID
    """
    try:
        task = service.get_task_by_id(task_id)
        return task
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    service: TaskService = Depends(get_task_service)
):
    """
    Update a task by ID
    """
    try:
        task = service.update_task(
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            completed=task_data.completed,
            tags=task_data.tags,
            mini_tasks=task_data.mini_tasks
        )
        return task
        
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """
    Delete a task by ID
    """
    try:
        success = service.delete_task(task_id)
        if success:
            return {"message": f"Task {task_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
