import unittest
import asyncio

from main import AsyncTaskExecutor, Task, PrintTaskHandler, CalculateTaskHandler, FileTaskHandler


class TestAsyncTaskExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = AsyncTaskExecutor()
        self.executor.register("print", PrintTaskHandler())
        self.executor.register("calc", CalculateTaskHandler())
        self.executor.register("file", FileTaskHandler())

    def test_register_handler(self):
        self.assertIn("print", self.executor.handlers)
        self.assertIn("calc", self.executor.handlers)
        self.assertIn("file", self.executor.handlers)

    def test_unknown_task_type(self):
        task = Task(1, "unknown", {})
        result = asyncio.run(self.executor.process_task(task))
        self.assertFalse(result.success)
        self.assertIn("Нет обработчика", result.error)

    def test_print_task(self):
        task = Task(2, "print", {"msg": "Привет"})
        result = asyncio.run(self.executor.process_task(task))
        self.assertTrue(result.success)
        self.assertIn("Привет", result.result)

    def test_calc_task(self):
        task = Task(3, "calc", {"numbers": [1, 2, 3]})
        result = asyncio.run(self.executor.process_task(task))
        self.assertTrue(result.success)
        self.assertEqual(result.result["sum"], 6)
        self.assertEqual(result.result["average"], 2)

    def test_file_task(self):
        task = Task(4, "file", {"filename": "data.txt"})
        result = asyncio.run(self.executor.process_task(task))
        self.assertTrue(result.success)
        self.assertIn("data.txt", result.result)

    def test_calc_task_without_numbers(self):
        task = Task(5, "calc", {})
        result = asyncio.run(self.executor.process_task(task))
        self.assertTrue(result.success)
        self.assertEqual(result.result, "Расчет завершен")

    def test_file_task_without_filename(self):
        task = Task(6, "file", {})
        result = asyncio.run(self.executor.process_task(task))
        self.assertTrue(result.success)
        self.assertIn("default.txt", result.result)
        
    def test_print_task_with_string(self):
        task = Task(13, "print", "Просто строка")
        result = asyncio.run(self.executor.process_task(task))
        self.assertTrue(result.success)
        self.assertIn("Просто строка", result.result)

    def test_run_processes_tasks(self):
        async def run_executor():
            await self.executor.add_task(Task(20, "print", {"msg": "A"}))
            await self.executor.add_task(Task(21, "calc", {"numbers": [2, 3]}))
            await self.executor.run(timeout=1.0)
    
        asyncio.run(run_executor())
        self.assertFalse(self.executor.running)


if __name__ == "__main__":
    unittest.main()