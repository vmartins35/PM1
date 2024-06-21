import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, ANY
from main import app
from service.task_service import TaskService
from domain.model.models import Task

client = TestClient(app)

@pytest.fixture
def mock_task_service():
    return Mock(spec=TaskService)

@pytest.fixture(autouse=True)
def override_dependency(mock_task_service):
    app.dependency_overrides[TaskService] = lambda: mock_task_service

def test_create_task(mock_task_service):
    task_data = {"title":"New Task", "description":"Task Description", "status":"Pendente"}
    mock_task_service.create_task.return_value = Task(id=1, **task_data)

    response = client.post("/tasks/", params=task_data)

    print(response.status_code)

    assert response.status_code == 200  
    assert response.json()['title'] == "New Task"

def test_read_tasks(mock_task_service):
    mock_task_service.get_tasks.return_value = [Task(id=1, title="New Task", description="Task Description", status="Pendente")]
    response = client.get("/tasks/")
    
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]['title'] == "New Task"

def test_read_task(mock_task_service):
    mock_task_service.get_task.return_value = Task(id=1, title="New Task", description="Task Description", status="Pendente")

    response = client.get("/tasks/1")
    
    assert response.status_code == 200
    assert response.json()['title'] == "New Task"

def test_read_task_not_found(mock_task_service):
    mock_task_service.get_task.return_value = None

    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()['message'] == "Tarefa não encontrada..." 

def test_update_task(mock_task_service):
    updated_task = {"title":"Updated Task", "description":"Updated Description", "status":"Concluída"}
    mock_task_service.update_task.return_value = Task(id=1, **updated_task)

    response = client.put("/tasks/1", params=updated_task)

    assert response.status_code == 200
    assert response.json()['title'] == "Updated Task"

def test_delete_task(mock_task_service):
    mock_task_service.delete_task.return_value = None

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json()['detail'] == "Tarefa excluída!"
