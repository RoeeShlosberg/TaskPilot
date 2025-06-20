from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from datetime import datetime
from sqlmodel import Session
import logging
from ..db.session import get_session
from ..services.task_service import TaskService
from ..repositories.task_repository import TaskRepository
from ..agents.gpt_agent import get_project_summary_cached, get_task_recommendations_cached
from ..cache.redis_cache import cache

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agent", tags=["AI Agent"])

# Dependency injection functions
def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)

def get_task_service(repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(repo)

@router.get("/summary", response_model=Dict[str, Any])
async def get_project_summary_endpoint(task_service: TaskService = Depends(get_task_service)):
    """
    Get an AI-generated summary of the current project status.
    
    Returns a comprehensive analysis of all tasks including:
    - Overall project health and progress
    - Key achievements and critical issues
    - Timeline analysis and recommendations    """
    logger.info("AI Summary requested")
    try:
        # Get all tasks
        tasks = task_service.get_all_tasks()
        logger.info(f"Retrieved {len(tasks)} tasks for summary")
          # Get cached or fresh summary
        summary = await get_project_summary_cached(tasks)
        
        # Prepare response with metadata
        completed_tasks = len([t for t in tasks if t.completed])
        pending_tasks = len([t for t in tasks if not t.completed])
        
        logger.info(f"AI Summary generated - {completed_tasks} completed, {pending_tasks} pending tasks")
        
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
        logger.error(f"Error generating project summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate project summary: {str(e)}"
        )

@router.get("/recommendations", response_model=Dict[str, Any])
async def get_task_recommendations_endpoint(task_service: TaskService = Depends(get_task_service)):
    """
    Get AI-generated task prioritization and productivity recommendations.
    
    Returns intelligent suggestions for:
    - Immediate priority tasks
    - Weekly focus areas
    - Time management strategies
    - Risk mitigation for overdue tasks    """
    logger.info("AI Recommendations requested")
    try:
        # Get all tasks
        tasks = task_service.get_all_tasks()
        logger.info(f"Retrieved {len(tasks)} tasks for recommendations")
        
        # Get cached or fresh recommendations
        recommendations = await get_task_recommendations_cached(tasks)
        
        # Analyze pending tasks for metadata
        pending_tasks = [t for t in tasks if not t.completed]
        high_priority_tasks = len([t for t in pending_tasks if t.priority == "high"])
        overdue_tasks = []
        
        now = datetime.utcnow()
        for task in pending_tasks:
            if task.due_date and task.due_date < now:
                overdue_tasks.append(task.id)
        
        logger.info(f"AI Recommendations generated - {len(pending_tasks)} pending, {high_priority_tasks} high priority, {len(overdue_tasks)} overdue")
        
        return {
            "recommendations": recommendations,
            "metadata": {
                "total_pending_tasks": len(pending_tasks),
                "high_priority_tasks": high_priority_tasks,
                "overdue_tasks": len(overdue_tasks),
                "overdue_task_ids": overdue_tasks
            },
            "generated_at": datetime.utcnow().isoformat(),
            "prompt_type": "task_recommendations"
        }
        
    except Exception as e:
        logger.error(f"Error generating task recommendations: {str(e)}")
        raise HTTPException(
            status_code=500,
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
