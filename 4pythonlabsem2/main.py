import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Protocol, Dict
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TaskHandler(Protocol):
    async def handle(self, task_data: Any) -> Any:
        ...


@dataclass
class Task:
    task_id: int
    task_type: str
    data: Dict[str, Any]


@dataclass
class TaskResult:
    task_id: int
    success: bool
    result: Any = None
    error: str = ""


class PrintTaskHandler:
    async def handle(self, task_data: Any) -> Any:
        text = task_data.get("msg", task_data) if isinstance(task_data, dict) else task_data
        logger.info(f"Печатаем сообщение: {text}")
        await asyncio.sleep(0.1)
        return f"Сообщение выведено: {text}"


class CalculateTaskHandler:
    async def handle(self, task_data: Any) -> Any:
        logger.info("Выполняем расчет")
        await asyncio.sleep(0.1)

        if isinstance(task_data, dict):
            numbers = task_data.get("numbers", [])
            if numbers:
                total = sum(numbers)
                average = total / len(numbers)
                return {
                    "sum": total,
                    "average": average
                }

        return "Расчет завершен"


class FileTaskHandler:
    @asynccontextmanager
    async def open_file(self, filename: str):
        logger.info(f"Открываем файл: {filename}")
        try:
            yield filename
        finally:
            logger.info(f"Закрываем файл: {filename}")
            await asyncio.sleep(0.05)

    async def handle(self, task_data: Any) -> Any:
        filename = "default.txt"
        if isinstance(task_data, dict):
            filename = task_data.get("filename", filename)

        logger.info(f"Обработка файла: {filename}")
        async with self.open_file(filename) as file_name:
            await asyncio.sleep(0.1)
            return f"Файл {file_name} обработан"


class AsyncTaskExecutor:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.handlers: Dict[str, TaskHandler] = {}
        self.running = False
        logger.info("Исполнитель создан")

    def register(self, task_type: str, handler: TaskHandler):
        self.handlers[task_type] = handler
        logger.info(f"Обработчик для '{task_type}' добавлен")

    async def add_task(self, task: Task):
        await self.queue.put(task)
        logger.info(f"Задача {task.task_id} добавлена в очередь")

    async def process_task(self, task: Task) -> TaskResult:
        logger.info(f"Начинаем обработку задачи {task.task_id}")

        handler = self.handlers.get(task.task_type)
        if handler is None:
            error_text = f"Нет обработчика для типа задачи '{task.task_type}'"
            logger.error(error_text)
            return TaskResult(task.task_id, False, error=error_text)

        try:
            result = await handler.handle(task.data)
            return TaskResult(task.task_id, True, result=result)
        except Exception as e:
            logger.error(f"Ошибка в задаче {task.task_id}: {e}")
            return TaskResult(task.task_id, False, error=str(e))

    async def run(self, timeout: float = 3.0):
        self.running = True
        logger.info("Исполнитель запущен")

        while self.running:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                result = await self.process_task(task)

                if result.success:
                    logger.info(f"Задача {result.task_id} выполнена: {result.result}")
                else:
                    logger.warning(f"Задача {result.task_id} не выполнена: {result.error}")

                self.queue.task_done()

            except asyncio.TimeoutError:
                if self.queue.empty():
                    logger.info("Очередь пуста, завершаем работу")
                    break
            except Exception as e:
                logger.error(f"Ошибка в основном цикле: {e}")

        self.running = False
        logger.info("Исполнитель остановлен")


async def main():
    executor = AsyncTaskExecutor()

    executor.register("print", PrintTaskHandler())
    executor.register("calc", CalculateTaskHandler())
    executor.register("file", FileTaskHandler())

    tasks = [
        Task(1, "print", {"msg": "Привет"}),
        Task(2, "calc", {"numbers": [1, 2, 3]}),
        Task(3, "file", {"filename": "data.txt"}),
        Task(4, "unknown", {"x": 42}),
    ]

    for task in tasks:
        await executor.add_task(task)

    await executor.run(timeout=3.0)


if __name__ == "__main__":
    asyncio.run(main())