import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock
from repository.task_repository import TaskRepository
from domain.model.models import Task

@pytest.fixture
def db():
    return Mock(spec=Session)


def test_create_task(db):
    task_data = Task(title="New Task", description="Task Description", status="Pendente")
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = task_data

    task = TaskRepository.create_task(db, task_data)

    assert task.title == "New Task"
    db.add.assert_called_once_with(task_data)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(task_data)


def test_get_task(db):
    task_data = Task(id=1, title="Task 1", description="Description 1", status="Pendente")
    db.query.return_value.filter.return_value.first.return_value = task_data

    task = TaskRepository.read_task(db, 1)

    assert task.title == "Task 1"
    db.query.return_value.filter.return_value.first.assert_called_once()


def test_get_tasks(db):
    task_data = [Task(id=1, title="Task 1", description="Description 1", status="Pendente")]
    mock_query = Mock()
    mock_query.all.return_value = task_data
    db.query.return_value = mock_query

    tasks = TaskRepository.find_all_task(db)

    assert len(tasks) >= 1
    assert tasks[0].title == "Task 1"
    db.query.return_value.all.assert_called_once()


def test_update_task(db):
    task_data = Task(id=1, title="Task 1", description="Description 1", status="Pendente")
    updated_data = {"title": "Updated Task", "description": "Updated Description", "status": "Concluída"}
    db.query.return_value.filter.return_value.first.return_value = task_data

    task = TaskRepository.update_task(db, 1, updated_data)

    assert task.title == "Updated Task"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(task_data)


def test_delete_task(db):
    task_data = Task(id=1, title="Updated Task", description="Updated Description", status="Concluída")
    db.query.return_value.filter.return_value.first.return_value = task_data

    task = TaskRepository.delete_task(db, 1)
    print(task.title)
    assert task.title == "Updated Task"
    db.delete.assert_called_once_with(task_data)
    db.commit.assert_called_once()
