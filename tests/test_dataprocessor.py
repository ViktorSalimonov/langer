import sys

from server.task import ProcessingTask

sys.path.insert(0, 'home/salv/Projects/langer')
from server.dataprocessor import DataProcessor


import unittest

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        self.dp = DataProcessor("123")
        self.text1 = "Привет, как дела?"
        self.text2 = "Hi! How it's going?"
        self.text3 =  "Le projet de loi de finances 2019"

        self.word1 = "Поиск"
        self.word2 = "Come"
        self.word3 = "loi"

    def test_lang_detect(self):
        self.assertEqual(self.dp.lang_detection(self.text1)[0], "ru")
        self.assertEqual(self.dp.lang_detection(self.text2)[0], "en")
        self.assertEqual(self.dp.lang_detection(self.text3)[0], "fr")

    def test_lang_detect2(self):
        self.assertEqual(self.dp.lang_detection(self.word1)[0], "ru")
        self.assertEqual(self.dp.lang_detection(self.word2)[0], "en")
        self.assertEqual(self.dp.lang_detection(self.word3)[0], "fr")

    def test_stat(self):
        dp = DataProcessor("123")
        task = ProcessingTask("http://ya.ru", "Привет, как дела? Как жизнь?!")
        dp.process(task)
        stat = dp.get_stat()
        print(stat)
        self.assertEqual(len(dp.persist.axes[0]), 5)


if __name__ == '__main__':
    unittest.main()