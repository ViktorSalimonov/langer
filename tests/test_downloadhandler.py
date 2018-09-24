import sys
sys.path.insert(0, 'home/salv/Projects/langer')
from server.downloadhandler import DownloadHandler

import unittest

class TestDownloadHandler(unittest.TestCase):

    def setUp(self):
        self.url1 = "https://www.google.com/"
        self.url2 = "https://ya.ru/"
        self.url3 = "hdts://sdsdf.dddd"

    def test_url_valid(self):
        self.assertEqual(DownloadHandler.url_valid(self, self.url1), True)
        self.assertEqual(DownloadHandler.url_valid(self, self.url2), True)
        self.assertEqual(DownloadHandler.url_valid(self, self.url3), False)


if __name__ == '__main__':
    unittest.main()