import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from service.task_service import TaskService
from domain.model.models import Task
from repository.task_repository import TaskRepository

@pytest.fixture
def mock_task_repository():
    return Mock(spec=TaskRepository)


def test_create_task(mock_task_repository):
    db = Mock(spec=Session)
    task_data = {"title": "New Task", "description": "Task Description", "status": "Pendente"}
    task_instance = Task(id=1, **task_data)
    mock_task_repository.create_task.return_value = task_instance

    TaskService.TaskRepository = mock_task_repository
    task = TaskService.create_task(db, **task_data)

    assert task.title == "New Task"


def test_get_task(mock_task_repository):
    db = Mock(spec=Session)
    task_instance = Task(id=1, title="New Task", description="Task Description", status="Pendente")  
    
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = task_instance
    db.query.return_value = mock_query
    
    TaskService.TaskRepository = mock_task_repository
    task = TaskService.get_task(db, 1)
    print(task.title)

    assert task.title == "New Task"


def test_get_tasks(mock_task_repository):
    db = Mock(spec=Session)
    task_instance_list = [Task(id=1, title="New Task", description="Task Description 1", status="Pendente"),
                          Task(id=2, title="New Task 2", description="Task Description 2", status="Concluída")]
    
    
    mock_query = MagicMock()
    mock_query.all.return_value = task_instance_list
    db.query.return_value = mock_query
    
    TaskService.TaskRepository = mock_task_repository
    tasks = TaskService.get_tasks(db)

    assert len(tasks) >= 2
    assert tasks[0].title == "New Task"
    assert tasks[1].title == "New Task 2"


def test_update_task(mock_task_repository):
    db = Mock(spec=Session)
    updated_task_data = {"title": "Updated Task", "description": "Updated Description", "status": "Concluída"}
    mock_task_repository.update_task.return_value = Task(id=1, **updated_task_data)

    TaskService.TaskRepository = mock_task_repository
    task = TaskService.update_task(db, 1, **updated_task_data)

    assert task.title == "Updated Task"
    assert task.description == "Updated Description"
    assert task.status == "Concluída"


def test_delete_task(mock_task_repository):
    db = Mock(spec=Session)
    task_instance = Task(id=1, title="Updated Task", description="Updated Description", status="Concluída")
    
    
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = task_instance
    db.query.return_value = mock_query
    
    TaskService.TaskRepository = mock_task_repository
    result = TaskService.delete_task(db, 1)

    assert result.title == "Updated Task"
