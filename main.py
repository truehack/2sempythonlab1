from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskError(Exception):
    pass


class DescriptionDescriptor:
    def __get__(self, obj, objtype=None):
        return obj._description

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TaskError("Описание должно быть строкой")

        if value.strip() == "":
            raise TaskError("Описание не может быть пустым")

        if len(value) > 500:
            raise TaskError("Слишком длинное описание")

        obj._description = value


class PriorityDescriptor:
    def __get__(self, obj, objtype=None):
        return obj._priority

    def __set__(self, obj, value):
        if not isinstance(value, Priority):
            raise TaskError("Приоритет должен быть типа Priority")

        obj._priority = value


class StatusDescriptor:
    def __get__(self, obj, objtype=None):
        return obj._status

    def __set__(self, obj, value):
        if not isinstance(value, TaskStatus):
            raise TaskError("Статус должен быть типа TaskStatus")

        obj._status = value


class Task:
    description = DescriptionDescriptor()
    priority = PriorityDescriptor()
    status = StatusDescriptor()

    def __init__(self, description, priority=Priority.MEDIUM, status=TaskStatus.NEW):
        
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._completed_at = None

        self.description = description
        self.priority = priority
        self.status = status

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    @property
    def completed_at(self):
        return self._completed_at

    @property
    def is_ready(self):
        return self.status in (TaskStatus.NEW, TaskStatus.IN_PROGRESS)

    @property
    def is_urgent(self):
        return self.priority in (Priority.HIGH, Priority.CRITICAL)

    def start(self):
        if self.status != TaskStatus.NEW:
            raise TaskError("Можно начать только новую задачу")

        self.status = TaskStatus.IN_PROGRESS

    def complete(self):
        if self.status != TaskStatus.IN_PROGRESS:
            raise TaskError("Можно завершить только задачу в работе")

        self.status = TaskStatus.COMPLETED
        self._completed_at = datetime.now()

    def cancel(self):
        if self.status in (TaskStatus.COMPLETED, TaskStatus.CANCELLED):
            raise TaskError("Эту задачу уже нельзя отменить")

        self.status = TaskStatus.CANCELLED

    def __str__(self):
        return f"Task({self.id[:8]}, {self.description}, {self.priority.name}, {self.status.name})"

if __name__ == "__main__":
    task = Task("Проверить запуск", Priority.HIGH)
    print(task)
    task.start()
    print(f"Статус: {task.status.name}")
    print(f"Готова к выполнению: {task.is_ready}")