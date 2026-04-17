import pytest
from datetime import datetime

from main import Task, Priority, TaskStatus, TaskError


@pytest.fixture
def fresh_task():
    return Task("Подготовить отчёт", Priority.MEDIUM)


def test_init_defaults(fresh_task):
    assert fresh_task.description == "Подготовить отчёт"
    assert fresh_task.priority == Priority.MEDIUM
    assert fresh_task.status == TaskStatus.NEW
    assert isinstance(fresh_task.id, str)
    assert isinstance(fresh_task.created_at, datetime)
    assert fresh_task.completed_at is None


def test_update_description_ok(fresh_task):
    fresh_task.description = "Новое название задачи"
    assert fresh_task.description == "Новое название задачи"


def test_reject_empty_desc(fresh_task):
    with pytest.raises(TaskError):
        fresh_task.description = ""


def test_reject_non_string_desc(fresh_task):
    with pytest.raises(TaskError):
        fresh_task.description = 42


def test_reject_oversized_desc(fresh_task):
    with pytest.raises(TaskError):
        fresh_task.description = "x" * 600


def test_change_priority(fresh_task):
    fresh_task.priority = Priority.CRITICAL
    assert fresh_task.priority == Priority.CRITICAL


def test_priority_rejects_string(fresh_task):
    with pytest.raises(TaskError):
        fresh_task.priority = "HIGH"


def test_change_status(fresh_task):
    fresh_task.status = TaskStatus.IN_PROGRESS
    assert fresh_task.status == TaskStatus.IN_PROGRESS


def test_status_rejects_raw_value(fresh_task):
    with pytest.raises(TaskError):
        fresh_task.status = "in_progress"


def test_is_ready_flag(fresh_task):
    assert fresh_task.is_ready is True
    
    fresh_task.start()
    assert fresh_task.is_ready is True
    
    fresh_task.complete()
    assert fresh_task.is_ready is False


def test_urgency_logic(fresh_task):
    assert fresh_task.is_urgent is False
    
    fresh_task.priority = Priority.CRITICAL
    assert fresh_task.is_urgent is True


def test_start_transition(fresh_task):
    fresh_task.start()
    assert fresh_task.status == TaskStatus.IN_PROGRESS


def test_start_twice_fails(fresh_task):
    fresh_task.start()
    with pytest.raises(TaskError):
        fresh_task.start()


def test_complete_sets_time(fresh_task):
    fresh_task.start()
    fresh_task.complete()
    
    assert fresh_task.status == TaskStatus.COMPLETED
    assert fresh_task.completed_at is not None


def test_complete_on_new_fails(fresh_task):
    with pytest.raises(TaskError):
        fresh_task.complete()


def test_cancel_new_task(fresh_task):
    fresh_task.cancel()
    assert fresh_task.status == TaskStatus.CANCELLED


def test_cancel_completed_forbidden(fresh_task):
    fresh_task.start()
    fresh_task.complete()
    
    with pytest.raises(TaskError):
        fresh_task.cancel()


def test_repr_contains_main_fields():
    t = Task("Финальная проверка", Priority.LOW)
    s = str(t)
    
    assert "Task(" in s
    assert "Финальная проверка" in s
    assert "LOW" in s