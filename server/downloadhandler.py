import re
import threading

from server.task import DownloadTask


class DownloadHandler(object):

    def __init__(self, download_queue):
        self.download_queue = download_queue
        self.lock = threading.Lock()

    def put_url(self, url):
        url = url.decode('UTF-8')
        if self.is_valid(url):
            task = DownloadTask(url)
            self.lock.acquire()
            self.download_queue.put(task)
            self.lock.release()

    def is_valid(self, url):
        regex = re.compile('^(?:http)s?://')
        if re.match(regex, url):
            return True
        else:
            return False