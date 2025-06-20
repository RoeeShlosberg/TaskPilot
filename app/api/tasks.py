from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import logging

from app.db.session import get_session
from app.models.task_model import Task
from app.models.request_models import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository

logger = logging.getLogger(__name__)
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
    logger.info(f"Creating new task: {task_data.title}")
    try:
        task = service.create_task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            tags=task_data.tags,
            mini_tasks=task_data.mini_tasks
        )
        logger.info(f"Task created successfully with ID: {task.id}")
        return task
        
    except ValueError as e:
        logger.warning(f"Invalid task data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """
    Get a task by ID
    """
    logger.info(f"Task required with ID: {task_id}")
    try:
        task = service.get_task_by_id(task_id)
        logger.info(f"Retrieved task with ID: {task_id}")
        return task
        
    except ValueError as e:
        logger.warning(f"Task with ID {task_id} not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching task with ID {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    service: TaskService = Depends(get_task_service)
):
    """
    Get all tasks
    """
    logger.info("Fetching all tasks")
    try:
        tasks = service.get_all_tasks()
        logger.info(f"Retrieved {len(tasks)} tasks")
        return tasks
        
    except Exception as e:
        logger.error(f"Error fetching all tasks: {e}")
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
    logger.info(f"Updating task with ID: {task_id}")
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
        logger.info(f"Task with ID {task_id} updated successfully")
        return task
        
    except ValueError as e:
        if "not found" in str(e):
            logger.warning(f"Task with ID {task_id} not found: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        else:
            logger.warning(f"Invalid task update data for ID {task_id}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating task with ID {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """
    Delete a task by ID
    """
    logger.info(f"Deleting task with ID: {task_id}")
    try:
        success = service.delete_task(task_id)
        if success:
            logger.info(f"Task with ID {task_id} deleted successfully")
            return {"message": f"Task {task_id} deleted successfully"}
        else:
            logger.warning(f"Task with ID {task_id} not found for deletion")
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        
    except ValueError as e:
        logger.warning(f"Error deleting task with ID {task_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting task with ID {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """
    Get a task by ID
    """
    logger.info(f"Fetching task with ID: {task_id}")
    try:
        task = service.get_task_by_id(task_id)
        logger.info(f"Retrieved task with ID: {task_id}")
        return task
        
    except ValueError as e:
        logger.warning(f"Task with ID {task_id} not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching task with ID {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

