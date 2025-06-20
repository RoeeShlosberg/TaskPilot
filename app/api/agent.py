from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from datetime import datetime
from sqlmodel import Session
from ..db.session import get_session
from ..services.task_service import TaskService
from ..repositories.task_repository import TaskRepository
from ..agents.gpt_agent import build_prompt_summary, build_prompt_recommendation, query_gpt

router = APIRouter(prefix="/agent", tags=["AI Agent"])

# Dependency injection functions
def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)

def get_task_service(repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(repo)

@router.get("/summary", response_model=Dict[str, Any])
async def get_project_summary(task_service: TaskService = Depends(get_task_service)):
    """
    Get an AI-generated summary of the current project status.
    
    Returns a comprehensive analysis of all tasks including:
    - Overall project health and progress
    - Key achievements and critical issues
    - Timeline analysis and recommendations
    """
    try:
        # Get all tasks
        tasks = task_service.get_all_tasks()
        
        # Build the prompt with all task details
        prompt = build_prompt_summary(tasks)
        
        # Query GPT for summary
        summary = await query_gpt(prompt)
        
        # Prepare response with metadata
        completed_tasks = len([t for t in tasks if t.completed])
        pending_tasks = len([t for t in tasks if not t.completed])
        
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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate project summary: {str(e)}"
        )

@router.get("/recommendations", response_model=Dict[str, Any])
async def get_task_recommendations(task_service: TaskService = Depends(get_task_service)):
    """
    Get AI-generated task prioritization and productivity recommendations.
    
    Returns intelligent suggestions for:
    - Immediate priority tasks
    - Weekly focus areas
    - Time management strategies
    - Risk mitigation for overdue tasks
    """
    try:
        # Get all tasks
        tasks = task_service.get_all_tasks()
        
        # Build the recommendation prompt
        prompt = build_prompt_recommendation(tasks)
        
        # Query GPT for recommendations
        recommendations = await query_gpt(prompt)
        
        # Analyze pending tasks for metadata
        pending_tasks = [t for t in tasks if not t.completed]
        high_priority_tasks = len([t for t in pending_tasks if t.priority == "high"])
        overdue_tasks = []
        
        now = datetime.utcnow()
        for task in pending_tasks:
            if task.due_date and task.due_date < now:
                overdue_tasks.append(task.id)
        
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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate task recommendations: {str(e)}"
        )

@router.get("/health")
async def agent_health_check():
    """
    Check if the AI agent is properly configured and accessible.
    """
    import os
    
    openai_key_configured = bool(os.getenv("OPENAI_API_KEY"))
    
    return {
        "status": "healthy" if openai_key_configured else "configuration_required",
        "openai_configured": openai_key_configured,
        "service": "TaskPilot AI Agent",
        "version": "1.0.0"
    }
