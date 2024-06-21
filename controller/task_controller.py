from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from repository.task_repository import TaskRepository
from service.task_service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_user_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)

@task_router.post("/")
def create_task(title: str, description: str, status: str, db: Session = Depends(get_db)):
    return TaskService.create_task(db, title, description, status)

@task_router.get("/")
def read_tasks(db: Session = Depends(get_db)):
    return TaskService.get_tasks(db)

@task_router.get("/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = TaskService.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada...")
    return task

@task_router.put("/{task_id}")
def update_task(task_id: int, title: str = None, description: str = None, status: str = None, db: Session = Depends(get_db)):
    return TaskService.update_task(db, task_id, title, description, status)

@task_router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    TaskService.delete_task(db, task_id)
    return {"detail": "Tarefa excluída!"}
