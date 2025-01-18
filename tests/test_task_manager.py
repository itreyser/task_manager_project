import pytest
from app.task_manager import TaskManager


@pytest.fixture
def task_manager():
    return TaskManager()


def test_add_task(task_manager):
    task1 = task_manager.add_task("Task1", "low")
    assert task1["name"] == "Task1"
    assert task1["priority"] == "low"
    assert task1["completed"] == False
    assert len(task_manager.list_tasks()) == 1

def test_negative_add_task(task_manager):
    with pytest.raises(ValueError):
        task_manager.add_task("Task2", "negative_priority")



def test_list_tasks(task_manager):
    assert task_manager.list_tasks() == []

def test_mark_task_completed(task_manager):
    task = task_manager.add_task("Task66")
    task_manager.mark_task_completed("Task66")
    assert task["completed"] == True

def test_negative_mark_task_completed(task_manager):
    with pytest.raises(ValueError):
        task_manager.mark_task_completed("asd")


def test_remove_task(task_manager):
    task_manager.add_task("Task1", "low")
    assert task_manager.remove_task("Task1")["name"] == "Task1"

def test_negative_remove_task(task_manager):
    with pytest.raises(ValueError):
        task_manager.remove_task("asd")
