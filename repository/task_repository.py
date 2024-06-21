from sqlalchemy.orm import Session

from domain.model.models import Task

class TaskRepository():

    def create_task(db: Session, task: Task) -> Task:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def update_task(db: Session, task_id: int, task_data: dict):
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            for key, value in task_data.items():
                setattr(task, key, value)
            db.commit()
            db.refresh(task)
        return task

    def delete_task(db: Session, task_id: int):
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
        return task

    def read_task(db: Session, task_id):
        return db.query(Task).filter(Task.id == task_id).first()

    def find_all_task(db: Session):
        return db.query(Task).all()
