import pytest
from app.models import Task

class TestTaskModel:
    def test_task_creation(self):
        task = Task(1, "Learn Jenkins")
        assert task.id == 1
        assert task.name == "Learn Jenkins"

    def test_to_dict_method(self):
        task = Task(2, "Write Tests")
        assert task.to_dict() == {
            'id': 2,
            'name': "Write Tests"
        }