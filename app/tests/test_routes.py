import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestTaskRoutes:
    def test_get_empty_tasks(self, client):
        response = client.get('/tasks')
        assert response.status_code == 200
        assert response.json == {'tasks': []}

    def test_add_task(self, client):
        response = client.post('/tasks', json={'name': 'New Task'})
        assert response.status_code == 201
        assert 'id' in response.json
        assert response.json['name'] == 'New Task'

    def test_get_tasks_after_add(self, client):
        client.post('/tasks', json={'name': 'Task 1'})
        response = client.get('/tasks')
        assert response.status_code == 200
        assert len(response.json['tasks']) == 1

    def test_add_task_invalid_data(self, client):
        response = client.post('/tasks', json={})
        assert response.status_code == 400