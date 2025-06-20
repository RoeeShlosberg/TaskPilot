import json
import os
import requests
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from ..models.task_model import Task

load_dotenv()

# OpenRouter configuration
API_PROVIDER = os.getenv("AI_PROVIDER", "openrouter")  # ope            "max_tokens": 150  # Very short, punchy advice only           "content": "You are TaskPilot AI. For SUMMARIES: analyze the current state objectively. For RECOMMENDATIONS: give ONLY actionable advice, NO summary, NO repeating task details. Be direct, helpful, and brief (2-3 sentences max)."router, groq, huggingface, mock
API_KEY = os.getenv("AI_API_KEY")  # Your OpenRouter API key

def format_task_details(task: Task) -> str:
    """Format a single task with all its details for prompt inclusion."""
    details = [f"Title: {task.title}"]
    
    if task.description:
        details.append(f"Description: {task.description}")
    
    details.append(f"Status: {'✅ Completed' if task.completed else '⏳ Pending'}")
    
    if task.priority:
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        details.append(f"Priority: {priority_emoji.get(task.priority, '')} {task.priority.upper()}")
    
    if task.due_date:
        now = datetime.utcnow()
        if task.due_date < now and not task.completed:
            status = "⚠️ OVERDUE"
        elif task.due_date.date() == now.date():
            status = "📅 Due Today"
        else:
            status = f"📅 Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
        details.append(status)
    
    if task.tags:
        try:
            tags_list = json.loads(task.tags)
            if tags_list:
                details.append(f"Tags: {', '.join(tags_list)}")
        except (json.JSONDecodeError, TypeError):
            pass
    
    if task.mini_tasks:
        try:
            mini_tasks_dict = json.loads(task.mini_tasks)
            if mini_tasks_dict:
                completed_mini = sum(1 for done in mini_tasks_dict.values() if done)
                total_mini = len(mini_tasks_dict)
                details.append(f"Sub-tasks: {completed_mini}/{total_mini} completed")
                for mini_task, is_done in mini_tasks_dict.items():
                    status_icon = "✅" if is_done else "⏳"
                    details.append(f"  {status_icon} {mini_task}")
        except (json.JSONDecodeError, TypeError):
            pass
    
    details.append(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    return "\n".join(details)

def build_prompt_summary(tasks: List[Task]) -> str:
    """Build a comprehensive prompt for getting a project summary."""
    if not tasks:
        return "I currently have no tasks in my project. Please provide a brief overview of how to get started with task management and project organization."
    
    prompt = "I need a comprehensive but short summary of my current project status. Here are all my tasks with detailed information:\n\n"
    
    # Group tasks by status
    completed_tasks = [t for t in tasks if t.completed]
    pending_tasks = [t for t in tasks if not t.completed]
    
    # Add statistics
    prompt += f"📊 OVERVIEW:\n"
    prompt += f"Total tasks: {len(tasks)}\n"
    prompt += f"Completed: {len(completed_tasks)} ({len(completed_tasks)/len(tasks)*100:.1f}%)\n"
    prompt += f"Pending: {len(pending_tasks)} ({len(pending_tasks)/len(tasks)*100:.1f}%)\n\n"
    
    # Add overdue tasks if any
    now = datetime.utcnow()
    overdue_tasks = [t for t in pending_tasks if t.due_date and t.due_date < now]
    if overdue_tasks:
        prompt += f"⚠️ OVERDUE TASKS ({len(overdue_tasks)}):\n"
        for task in overdue_tasks:
            prompt += f"{format_task_details(task)}\n\n"
    
    # Add high priority pending tasks
    high_priority_tasks = [t for t in pending_tasks if t.priority == "high"]
    if high_priority_tasks:
        prompt += f"🔴 HIGH PRIORITY PENDING TASKS ({len(high_priority_tasks)}):\n"
        for task in high_priority_tasks:
            prompt += f"{format_task_details(task)}\n\n"
    
    # Add all other pending tasks
    other_pending = [t for t in pending_tasks if t not in overdue_tasks and t not in high_priority_tasks]
    if other_pending:
        prompt += f"📋 OTHER PENDING TASKS ({len(other_pending)}):\n"
        for task in other_pending:
            prompt += f"{format_task_details(task)}\n\n"
    
    # Add completed tasks
    if completed_tasks:
        prompt += f"✅ COMPLETED TASKS ({len(completed_tasks)}):\n"
        for task in completed_tasks:
            prompt += f"{format_task_details(task)}\n\n"    
    prompt += """
Analyze my project status and provide a summary covering:
• Current state: completion rate, task distribution by priority
• Timeline status: what's on track, overdue, or approaching deadlines  
• Project health: patterns in task types, progress on mini-tasks, trends, bottlenecks, or notable progress

Focus on describing what IS, not what I should DO. Keep it informative but concise (3 sentences)."""
    
    return prompt

def build_prompt_recommendation(tasks: List[Task]) -> str:
    """Build a detailed prompt for getting task prioritization recommendations."""
    if not tasks:
        return "I have no tasks currently. Please provide recommendations on how to start organizing and planning tasks effectively."
    
    pending_tasks = [t for t in tasks if not t.completed]
    
    if not pending_tasks:
        return "All my tasks are completed! Please provide recommendations for maintaining productivity and planning future tasks."
    
    prompt = "I need intelligent task prioritization recommendations. Here are my pending tasks with complete details:\n\n"
    
    now = datetime.utcnow()
    
    # Add context about current situation
    prompt += f"📅 Current time: {now.strftime('%Y-%m-%d %H:%M UTC')}\n"
    prompt += f"📋 Total pending tasks: {len(pending_tasks)}\n\n"
    
    # Add all pending tasks with full details
    prompt += "PENDING TASKS:\n"
    for i, task in enumerate(pending_tasks, 1):
        prompt += f"\n{i}. {format_task_details(task)}\n"
    
    # Add completed tasks for context
    completed_tasks = [t for t in tasks if t.completed]
    if completed_tasks:
        prompt += f"\n✅ COMPLETED TASKS (for context):\n"
        for task in completed_tasks:
            prompt += f"- {task.title} (completed on {task.created_at.strftime('%Y-%m-%d')})\n"    
    prompt += """

Give me quick action items - NO explanations:

🔥 **Today:** What's my #1 task?
📅 **This Week:** Top 2 priorities?
⏰ **Time:** Quick estimates?

Keep it super brief!"""
    
    return prompt

async def query_gpt(prompt: str) -> str:
    """Query AI service with the given prompt and return the response."""
    try:
        if API_PROVIDER == "mock" or not API_KEY:
            return get_mock_response(prompt)
        elif API_PROVIDER == "openrouter":
            return await query_openrouter(prompt)
        elif API_PROVIDER == "groq":
            return await query_groq(prompt)
        elif API_PROVIDER == "huggingface":
            return await query_huggingface(prompt)
        else:
            return get_mock_response(prompt)
    except Exception as e:
        return f"Sorry, I encountered an error while processing your request: {str(e)}. Please check your AI service configuration and try again."

def get_mock_response(prompt: str) -> str:
    """Return a mock response for testing purposes."""
    if "summary" in prompt.lower():
        return """
🎯 **PROJECT HEALTH: GOOD PROGRESS** 

**📊 Overall Status:**
Your TaskPilot project shows solid momentum with 5 active tasks spanning critical areas from DevOps automation to team coordination.

**🔴 URGENT PRIORITIES:**
- **Setup CI/CD Pipeline** (Due June 25) - High priority DevOps foundation
- **Design Authentication System** (Due June 28) - Critical security implementation with 33% progress

**⚠️ IMMEDIATE ATTENTION:**
- **Database Performance Optimization** - OVERDUE since June 22! This needs immediate action.
- **Team Meeting Planning** - Due tomorrow (June 21) but mostly prepared

**✅ POSITIVE MOMENTUM:**
- Authentication system shows good progress (research and design phases complete)
- Team meeting is well-prepared (room booked, invites sent)
- Database analysis already started

**🎯 RECOMMENDATIONS:**
1. **TODAY:** Address overdue database optimization task
2. **THIS WEEK:** Complete team meeting and focus on CI/CD pipeline
3. **NEXT WEEK:** Push authentication system to completion

**📈 SUCCESS INDICATORS:**
- Good mix of strategic (DevOps, Security) and operational (Meeting) tasks
- Realistic timelines for most tasks
- Clear progress tracking through mini-tasks

Your project demonstrates strong planning with diverse priorities. Focus on the overdue database task first, then maintain momentum on the high-priority items.
        """
    else:
        return """
🚀 **IMMEDIATE ACTION PLAN**

**🔥 TOP PRIORITY (TODAY):**
1. **Optimize Database Performance** - OVERDUE! 
   - Complete "Add database indexes" (50% done)
   - Implement connection pooling
   - Estimated time: 4-6 hours

**📅 THIS WEEK FOCUS:**
2. **Plan Team Meeting** (Due tomorrow)
   - ✅ Room booked, invites sent
   - ⏳ Prepare agenda (30 min)
   - ⏳ Gather status updates (1 hour)

3. **Setup CI/CD Pipeline** (Due June 25)
   - Start with GitHub Actions workflow
   - Parallel track: automated testing setup
   - Estimated time: 2-3 days

**🎯 STRATEGIC RECOMMENDATIONS:**

**Time Allocation:**
- Morning: Database optimization (high focus work)
- Afternoon: Team meeting prep + CI/CD planning
- Next 3 days: CI/CD implementation

**Risk Mitigation:**
- Database task is blocking other performance work
- Authentication system has good momentum - don't lose it
- CI/CD is foundational - prioritize after database fix

**Dependencies:**
1. Database optimization → Performance testing
2. CI/CD setup → Automated deployment
3. Team meeting → Project alignment

**💡 PRODUCTIVITY TIPS:**
- Batch similar tasks (all database work together)
- Use mini-task progress to maintain motivation
- Schedule authentication work after CI/CD completion

**Next Actions:**
1. ⚡ Fix database indexes (2 hours)
2. 📋 Prepare meeting agenda (30 min)  
3. 🔧 Create CI/CD workflow template (1 hour)        """

async def query_openrouter(prompt: str) -> str:
    """Query OpenRouter API with a free model."""
    if not API_KEY:
        return get_mock_response(prompt)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",  # Optional: your app URL
        "X-Title": "TaskPilot"  # Optional: your app name
    }
    data = {
        "model": "microsoft/wizardlm-2-8x22b",  # Free high-quality model
        "messages": [
            {
                "role": "system",
                "content": "You are TaskPilot AI, a friendly task helper. For SUMMARIES: analyze what's happening. For RECOMMENDATIONS: give casual, practical advice like a helpful friend. Keep it short (3-4 sentences), be conversational not formal."
            },
            {"role": "user", "content": prompt}
        ],        "temperature": 0.7,
        "max_tokens": 200  # Very short, punchy responses
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

async def query_groq(prompt: str) -> str:
    """Query Groq API (free tier available)."""
    if not API_KEY:
        return get_mock_response(prompt)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",  # Free model
        "messages": [
            {
                "role": "system",
                "content": "You are TaskPilot AI, a professional project management assistant. Provide clear, actionable, and insightful advice for task management and project organization. Use emojis appropriately to make responses visually appealing and easy to scan."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

async def query_huggingface(prompt: str) -> str:
    """Query Hugging Face Inference API."""
    if not API_KEY:
        return get_mock_response(prompt)
    
    url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"inputs": prompt}
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()[0]["generated_text"]
