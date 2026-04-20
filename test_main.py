import unittest
from main import TaskQueue, TaskStatus


class TestTaskQueue(unittest.TestCase):
    
    def setUp(self):
        self.q = TaskQueue()
    
    def test_add_task(self):
        t = self.q.add_task("A", 5)
        self.assertEqual(t.name, "A")
        self.assertEqual(t.priority, 5)
        self.assertEqual(len(self.q), 1)
    
    def test_len(self):
        self.assertEqual(len(self.q), 0)
        self.q.add_task("A")
        self.q.add_task("B")
        self.assertEqual(len(self.q), 2)
    
    def test_iter(self):
        self.q.add_task("A")
        self.q.add_task("B")
        self.assertEqual([t.name for t in self.q], ["A", "B"])
    
    def test_iter_twice(self):
        self.q.add_task("A")
        self.q.add_task("B")
        self.assertEqual(list(self.q)[0].name, list(self.q)[0].name)
    
    def test_filter_priority(self):
        self.q.add_task("Low", 1)
        self.q.add_task("High", 10)
        result = list(self.q.filter_by_priority(5))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].priority, 10)
    
    def test_filter_empty(self):
        self.q.add_task("Low", 1)
        self.assertEqual(list(self.q.filter_by_priority(100)), [])
    
    def test_ids(self):
        t1 = self.q.add_task("A")
        t2 = self.q.add_task("B")
        self.assertEqual(t1.id, 1)
        self.assertEqual(t2.id, 2)
    
    def test_str(self):
        t = self.q.add_task("Test", 99)
        self.assertIn("Test", str(t))
        self.assertIn("99", str(t))
    
    def test_empty_queue_iter(self):
        self.assertEqual(list(self.q), [])
    
    def test_status_default(self):
        t = self.q.add_task("Test")
        self.assertEqual(t.status, TaskStatus.PENDING)
    
    def test_status_change(self):
        t = self.q.add_task("Test")
        t.status = TaskStatus.COMPLETED
        self.assertEqual(t.status, TaskStatus.COMPLETED)

if __name__ == "__main__":
    unittest.main()
