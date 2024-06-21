from sqlalchemy.orm import Session

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from domain.model.models import Task
from repository.task_repository import TaskRepository

class TaskService():

    def create_task(db: Session, title: str, description: str, status: str):
        task = Task(title=title, description=description, status=status)
        return TaskRepository.create_task(db, task)

    def get_task(db: Session, task_id: int):
        return TaskRepository.read_task(db, task_id)

    def get_tasks(db: Session):
        return TaskRepository.find_all_task(db)

    def update_task(db: Session, task_id: int, title: str = None, description: str = None, status: str = None):
        task_data = {k: v for k, v in {"title": title, "description": description, "status": status}.items() if v is not None}
        return TaskRepository.update_task(db, task_id, task_data)

    def delete_task(db: Session, task_id: int):
        return TaskRepository.delete_task(db, task_id)