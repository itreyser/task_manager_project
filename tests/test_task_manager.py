import allure
import pytest
from app.task_manager import TaskManager


@pytest.fixture
def task_manager():
    return TaskManager()


@allure.feature("Добавление таски")
@allure.story("Успешное добавление задачи")
def test_add_task(task_manager):
    task1 = task_manager.add_task("Task1", "low")
    with allure.step("Проверка, что имя таски == Task1)"):
        assert task1["name"] == "Task1"
    with allure.step("Проверка, что приоритет таски == low)"):
        assert task1["priority"] == "low"
    with allure.step("Проверка, что статус выполнения таски == False)"):
        assert task1["completed"] == False
    with allure.step("Проверка, что количество тасок = 1)"):
        assert len(task_manager.list_tasks()) == 1


@allure.feature("Добавление таски")
@allure.story("Неуспешное добавление задачи")
def test_negative_add_task(task_manager):
    with allure.step("Проверка, что выбрасывается исключение"):
        with pytest.raises(ValueError):
            task_manager.add_task("Task2", "negative_priority")


@allure.feature("Задача")
@allure.story("Просмотр списка задач")
def test_list_tasks(task_manager):
    with allure.step("Проверка, что вернулся пустой список задач"):
        assert task_manager.list_tasks() == []


@allure.feature("Задача")
@allure.story("Успешное выполнение задачи")
def test_mark_task_completed(task_manager):
    with allure.step("Добавление задачи"):
        task = task_manager.add_task("Task66")
    with allure.step("Переход задачи в статус = выполнено"):
        task_manager.mark_task_completed("Task66")
    with allure.step("Проверка, что задача выполнена"):
        assert task["completed"] == True


@allure.feature("Задача")
@allure.story("Неуспешное выполнение несуществующей задачи")
def test_negative_mark_task_completed(task_manager):
    with pytest.raises(ValueError):
        with allure.step("Пробрасывание в функцию несуществующей таски"):
            task_manager.mark_task_completed("asd")


@allure.feature("Задача")
@allure.story("Успешное удаление задачи из списка")
def test_remove_task(task_manager):
    with allure.step("Добавление задачи в список"):
        task_manager.add_task("Task1", "low")
    with allure.step("Удаление задачи и сверка имени удаленной задачи"):
        assert task_manager.remove_task("Task1")["name"] == "Task1"


@allure.feature("Задача")
@allure.story("Неуспешное удаление задачи из списка")
def test_negative_remove_task(task_manager):
    with pytest.raises(ValueError):
        with allure.step("Удаление задачи, которой нету в списке"):
            task_manager.remove_task("asd")
