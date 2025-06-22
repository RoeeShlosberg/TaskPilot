from sqlmodel import Session, select
from app.models.task_model import Task
from app.models.request_models import TaskUpdateRequest
import json


def create_task(session: Session, task: Task, user_id: int) -> Task:
    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task_by_id(session: Session, task_id: int, user_id: int) -> Task | None:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return session.exec(statement).first()


def get_all_tasks(session: Session, user_id: int) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()


def update_task(
    session: Session, task_id: int, task_update: TaskUpdateRequest, user_id: int
) -> Task | None:
    db_task = get_task_by_id(session, task_id=task_id, user_id=user_id)
    if not db_task:
        return None    # Only update fields that are explicitly provided and not None
    task_data = task_update.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in task_data.items():
        if hasattr(db_task, key):
            # Convert tags and mini_tasks to JSON strings for database storage
            if key == "tags" and value is not None:
                setattr(db_task, key, json.dumps(value))
            elif key == "mini_tasks" and value is not None:
                setattr(db_task, key, json.dumps(value))
            else:
                setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    db_task = get_task_by_id(session, task_id=task_id, user_id=user_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True
