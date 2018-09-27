import sys
sys.path.insert(0, 'home/salv/Projects/langer')
from server.downloadhandler import DownloadHandler

import unittest

class TestDownloadHandler(unittest.TestCase):

    def setUp(self):
        self.url1 = "http://www.google.com/"
        self.url2 = "https://ya.ru/"
        self.url3 = "hdts://sdsdf.dddd"
        self.dh = DownloadHandler("123")

    def test_is_valid(self):
        self.assertEqual(self.dh.is_valid(self.url1), True)
        self.assertEqual(self.dh.is_valid(self.url2), True)
        self.assertEqual(self.dh.is_valid(self.url3), False)



if __name__ == '__main__':
    unittest.main()