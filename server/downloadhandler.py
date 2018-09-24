import threading
from queue import Empty
import requests

from server.task import URLTask

class DownloadHandler(object):

    def __init__(self, task_queue):
        self.task_queue = task_queue
        self.lock = threading.Lock()

    def put_url(self, url):
        if self.url_valid(url) == True:
            task = URLTask(url)
            self.lock.acquire()
            self.task_queue.put(task)
            self.lock.release()
        else:
            pass

    def url_valid(self, url):
        try:
            request = requests.get(url)
            if request.status_code == requests.codes.ok:
                return True
        except:
            return False
