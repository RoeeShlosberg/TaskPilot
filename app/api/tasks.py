from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
import logging

from app.db.session import get_session
from app.models.user_model import User
from app.models.request_models import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from app.services.task_service import TaskService
from app.api.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["tasks"])


# Dependency injection function
def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    return TaskService(session)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreateRequest, 
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.
    """
    logger.info(f"User '{current_user.username}' creating new task: {task_data.title}")
    try:
        task = service.create_task(
            user_id=current_user.id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            tags=task_data.tags,
            mini_tasks=task_data.mini_tasks
        )
        logger.info(f"Task created successfully with ID: {task.id} for user '{current_user.username}'")
        return task
    except ValueError as e:
        logger.warning(f"Invalid task data for user '{current_user.username}': {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating task for user '{current_user.username}': {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by ID, only if it belongs to the authenticated user.
    """
    logger.info(f"User '{current_user.username}' requesting task with ID: {task_id}")
    try:
        task = service.get_task_by_id(task_id, current_user.id)
        logger.info(f"Retrieved task with ID: {task_id} for user '{current_user.username}'")
        return task
    except ValueError:
        logger.warning(f"Task with ID {task_id} not found for user '{current_user.username}'")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except Exception as e:
        logger.error(f"Error fetching task {task_id} for user '{current_user.username}': {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    
@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks for the authenticated user.
    """
    logger.info(f"Fetching all tasks for user '{current_user.username}'")
    try:
        tasks = service.get_all_tasks(current_user.id)
        logger.info(f"Retrieved {len(tasks)} tasks for user '{current_user.username}'")
        return tasks
    except Exception as e:
        logger.error(f"Error fetching all tasks for user '{current_user.username}': {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    """
    Update a task by ID, only if it belongs to the authenticated user.
    """
    logger.info(f"User '{current_user.username}' updating task with ID: {task_id}")
    try:
        task = service.update_task(
            task_id=task_id,
            user_id=current_user.id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            completed=task_data.completed,
            tags=task_data.tags,
            mini_tasks=task_data.mini_tasks
        )
        logger.info(f"Task with ID {task_id} updated successfully for user '{current_user.username}'")
        return task
    except ValueError as e:
        if "not found" in str(e):
            logger.warning(f"Task with ID {task_id} not found for user '{current_user.username}': {str(e)}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            logger.warning(f"Invalid task update data for ID {task_id} from user '{current_user.username}': {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        # Re-raise HTTPExceptions so they reach FastAPI properly
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user '{current_user.username}': {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task by ID, only if it belongs to the authenticated user.
    """
    logger.info(f"User '{current_user.username}' deleting task with ID: {task_id}")
    try:
        success = service.delete_task(task_id, current_user.id)
        if not success:
            logger.warning(f"Task with ID {task_id} not found for deletion by user '{current_user.username}'")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        logger.info(f"Task with ID {task_id} deleted successfully for user '{current_user.username}'")
    except HTTPException:
        # Re-raise HTTPExceptions so they reach FastAPI properly
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user '{current_user.username}': {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

