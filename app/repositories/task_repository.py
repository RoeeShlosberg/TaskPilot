from sqlmodel import Session, select
from app.models.task_model import Task


class TaskRepository:
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, task: Task) -> Task:
        """
        Save a new task to database
        """
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def get_by_id(self, task_id: int) -> Task:
        """
        Get a task by ID
        """
        return self.session.get(Task, task_id)
    
    def get_all(self) -> list[Task]:
        """
        Get all tasks
        """
        result = self.session.exec(select(Task)).all()
        return result
    
    def update(self, task: Task) -> Task:
        """
        Update an existing task
        """
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def delete(self, task_id: int) -> bool:
        """
        Delete a task by ID
        """
        task = self.session.get(Task, task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False
