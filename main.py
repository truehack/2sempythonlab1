from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: int
    name: str
    priority: int
    status: TaskStatus = TaskStatus.PENDING

    def __repr__(self):
        return f"Task(id={self.id}, name='{self.name}', priority={self.priority}, status={self.status.value})"


class TaskQueue:
    def __init__(self):
        self.tasks = []
        self.counter = 0

    def add_task(self, name, priority=0):
        self.counter += 1
        task = Task(self.counter, name, priority)
        self.tasks.append(task)
        return task

    def __iter__(self):
        for task in self.tasks:
            yield task

    def __len__(self):
        return len(self.tasks)

    def filter_by_priority(self, min_priority):
        for task in self.tasks:
            if task.priority >= min_priority:
                yield task


def main():
    q = TaskQueue()
    q.add_task("Тестовая задача")
    print(f"Очередь задач: {len(q)} элементов")

if __name__ == "__main__":
    main()