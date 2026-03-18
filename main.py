from dataclasses import dataclass
from typing import Protocol, Iterator, List
import json
from typing_extensions import runtime_checkable


@dataclass
class Task:
    id: int
    payload: str


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterator[Task]:
        ...


class TaskGenerator:
    def __init__(self, count: int = 5):
        self.count = count

    def get_tasks(self) -> Iterator[Task]:
        for i in range(self.count):
            yield Task(id=i, payload=f"Задача номер {i}")


class FileSource:

    def __init__(self, filename: str):
        self.filename = filename
        self._raw_data: List[dict] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self._raw_data = json.load(f)
        except FileNotFoundError:
            print(f"[WARN] Файл {self.filename} не найден")
            self._raw_data = []
        except json.JSONDecodeError:
            print(f"[WARN] Ошибка JSON в файле {self.filename}")
            self._raw_data = []

    def get_tasks(self) -> Iterator[Task]:
        for item in self._raw_data:
            yield Task(id=item["id"], payload=item["payload"])


class ApiSource:

    def __init__(self, raw_data: List[dict] = None):
        self._raw_data = raw_data if raw_data is not None else []

    def get_tasks(self) -> Iterator[Task]:
        for item in self._raw_data:
            yield Task(id=item["id"], payload=item["payload"])


def process_tasks(source: TaskSource) -> None:
    if not isinstance(source, TaskSource):
        raise TypeError(f"Источник {source} не соответствует контракту TaskSource")

    print(f"\n--- Обработка: {source.__class__.__name__} ---")
    for task in source.get_tasks():
        print(f"[OK] ID={task.id} | {task.payload}")


if __name__ == "__main__":
    gen_source = TaskGenerator(count=3)
    process_tasks(gen_source)
    
    file_data = [
        {"id": 100, "payload": "Из файла: 1"},
        {"id": 101, "payload": "Из файла: 2"},
    ]
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(file_data, f, ensure_ascii=False, indent=2)

    
    file_source = FileSource("tasks.json")
    process_tasks(file_source)

    
    api_data = [
        {"id": 500, "payload": "API: Уведомление"},
        {"id": 501, "payload": "API: Статистика"},
    ]
    api_source = ApiSource(raw_data=api_data)
    process_tasks(api_source)

    print("\nВсе задачи обработаны")

