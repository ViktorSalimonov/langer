import sys
sys.path.insert(0, 'home/salv/Projects/langer')
from server.ratelimiter import RateLimiter
from server.task import URLTask
import time

from queue import Queue

import unittest

class TestRateLimiter(unittest.TestCase):

    def setUp(self):
        task1 = URLTask("https://www.google.com/")
        task2 = URLTask("https://ya.ru/")
        task3 = URLTask("https://strategium.ru/")
        task4 = URLTask("https://paradoxplaza.com/")
        task5 = URLTask("https://vk.com/")
        task6 = URLTask("https://wildberries.ru/")
        task7 = URLTask("https://sberbank.ru/")
        task_queue_tmp = Queue()
        task_queue_tmp.put(task1)
        task_queue_tmp.put(task2)
        task_queue_tmp.put(task3)
        task_queue_tmp.put(task4)
        task_queue_tmp.put(task5)
        task_queue_tmp.put(task6)
        task_queue_tmp.put(task7)
        self.q = task_queue_tmp


    def test_get_task(self):
        rl = RateLimiter(self.q)
        self.assertIsNotNone(rl.get_task())
        self.assertIsNotNone(rl.get_task())
        self.assertIsNotNone(rl.get_task())


    def test_get_task2(self):
        rl = RateLimiter(self.q)
        self.assertIsNotNone(rl.get_task())
        self.assertIsNotNone(rl.get_task())
        self.assertIsNotNone(rl.get_task())
        self.assertIsNone(rl.get_task())

    def test_get_test3(self):
        rl = RateLimiter(self.q)
        self.assertIsNotNone(rl.get_task())
        self.assertIsNotNone(rl.get_task())
        self.assertIsNotNone(rl.get_task())
        self.assertIsNone(rl.get_task())
        time.sleep(62)
        self.assertIsNotNone(rl.get_task())
        self.assertIsNotNone(rl.get_task())
        self.assertIsNotNone(rl.get_task())
        self.assertIsNone(rl.get_task())



if __name__ == '__main__':
    unittest.main()