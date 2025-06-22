from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import datetime
from sqlmodel import Session
import logging
import time
from ..db.session import get_session
from ..services.task_service import TaskService
from ..models.user_model import User
from ..api.dependencies import get_current_user
from ..agents.gpt_agent import get_project_summary_cached, get_task_recommendations_cached
from ..cache.redis_cache import cache

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agent", tags=["AI Agent"])

# Dependency injection function
def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    return TaskService(session)

@router.get("/summary", response_model=Dict[str, Any])
async def get_project_summary_endpoint(
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    """
    Get an AI-generated summary of the current project status for the authenticated user.
    
    Returns a comprehensive analysis of all tasks including:
    - Overall project health and progress
    - Key achievements and critical issues
    - Timeline analysis and recommendations
    """
    logger.info(f"AI Summary requested for user '{current_user.username}'")
    try:
        start_time = time.time()
        # Get all tasks for the current user
        tasks = task_service.get_all_tasks(current_user.id)
        logger.info(f"Retrieved {len(tasks)} tasks for summary for user '{current_user.username}'")
        
        if not tasks:
            return {
                "summary": "No tasks found. Start by creating some tasks to get a summary.",
                "metadata": {
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "pending_tasks": 0,
                    "completion_rate": 0
                },
                "generated_at": datetime.utcnow().isoformat(),
                "prompt_type": "project_summary"
            }

        # Get cached or fresh summary
        summary = await get_project_summary_cached(tasks)
        
        # Prepare response with metadata
        completed_tasks = len([t for t in tasks if t.completed])
        pending_tasks = len(tasks) - completed_tasks
        
        end_time = time.time()
        logger.info(f"AI Summary generated for user '{current_user.username}' - {completed_tasks} completed, {pending_tasks} pending. Time taken: {end_time - start_time:.2f} seconds")
        
        return {
            "summary": summary,
            "metadata": {
                "total_tasks": len(tasks),
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "completion_rate": round(completed_tasks / len(tasks) * 100, 1) if tasks else 0
            },
            "generated_at": datetime.utcnow().isoformat(),
            "prompt_type": "project_summary"
        }
        
    except Exception as e:
        logger.error(f"Error generating project summary for user '{current_user.username}': {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate project summary: {str(e)}"
        )

@router.get("/recommendations", response_model=Dict[str, Any])
async def get_task_recommendations_endpoint(
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    """
    Get AI-generated task prioritization and productivity recommendations for the authenticated user.
    
    Returns intelligent suggestions for:
    - Immediate priority tasks
    - Weekly focus areas
    - Time management strategies
    - Risk mitigation for overdue tasks
    """
    logger.info(f"AI Recommendations requested for user '{current_user.username}'")
    try:
        start_time = time.time()
        # Get all tasks for the current user
        tasks = task_service.get_all_tasks(current_user.id)
        logger.info(f"Retrieved {len(tasks)} tasks for recommendations for user '{current_user.username}'")

        if not tasks:
            return {
                "recommendations": "No tasks found. Add some tasks to get recommendations.",
                "metadata": {
                    "pending_tasks": 0,
                    "high_priority_tasks": 0,
                    "overdue_tasks": 0
                },
                "generated_at": datetime.utcnow().isoformat(),
                "prompt_type": "task_recommendations"
            }

        # Get cached or fresh recommendations
        recommendations = await get_task_recommendations_cached(tasks)
        
        # Analyze pending tasks for metadata
        pending_tasks = [t for t in tasks if not t.completed]
        high_priority_tasks = len([t for t in pending_tasks if t.priority and t.priority.lower() == "high"])
        
        now = datetime.utcnow()
        overdue_task_count = sum(1 for task in pending_tasks if task.due_date and task.due_date < now)
        
        end_time = time.time()
        logger.info(f"AI Recommendations generated for user '{current_user.username}' - {len(pending_tasks)} pending, {high_priority_tasks} high priority, {overdue_task_count} overdue. Time taken: {end_time - start_time:.2f} seconds")
        
        return {
            "recommendations": recommendations,
            "metadata": {
                "pending_tasks": len(pending_tasks),
                "high_priority_tasks": high_priority_tasks,
                "overdue_tasks": overdue_task_count
            },
            "generated_at": datetime.utcnow().isoformat(),
            "prompt_type": "task_recommendations"
        }
        
    except Exception as e:
        logger.error(f"Error generating task recommendations for user '{current_user.username}': {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate task recommendations: {str(e)}"
        )

@router.get("/cache/stats")
async def get_cache_stats():
    """
    Get Redis cache statistics and health status.
    """
    logger.info("Cache stats requested")
    try:
        stats = cache.get_cache_stats()
        logger.info(f"Cache stats retrieved - {stats.get('total_keys', 0)} keys, connected: {stats.get('connected', False)}")
        return {
            "cache_stats": stats,
            "service": "Redis Cache",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get cache stats: {str(e)}"
        )

@router.delete("/cache/clear")
async def clear_cache():
    """
    Clear all AI response cache entries.    """
    logger.info("Cache clear requested")
    try:
        success = cache.clear_all()
        if success:
            logger.info("Cache cleared successfully")
            return {
                "message": "Cache cleared successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            logger.warning("Failed to clear cache")
            raise HTTPException(
                status_code=500,
                detail="Failed to clear cache"
            )
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )

@router.get("/health")
async def agent_health_check():
    """
    Check if the AI agent and cache are properly configured and accessible.
    """
    import os
    
    ai_key_configured = bool(os.getenv("AI_API_KEY"))
    cache_stats = cache.get_cache_stats()
    
    return {
        "status": "healthy" if ai_key_configured else "configuration_required",
        "ai_configured": ai_key_configured,
        "ai_provider": os.getenv("AI_PROVIDER", "mock"),
        "cache_connected": cache_stats.get("connected", False),
        "service": "TaskPilot AI Agent",
        "version": "1.0.0"
    }
