import html2text
import requests
import threading
import time

from server.task import ProcessingTask

class DownloadWorker(threading.Thread):
    SLEEP_INTERVAL = 10

    def __init__(self, rl, processing_queue):
        threading.Thread.__init__(self)
        self.processing_queue = processing_queue
        self.rl = rl


    def get_task(self):
        return self.rl.get_task()


    def get_content(self, url):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        html_content = requests.get(url)
        content = h.handle(html_content.text)
        return content


    def download(self, task):
        url = task.url
        content = self.get_content(url)
        task = ProcessingTask(url, content)
        self.processing_queue.put(task)


    def run(self):
        while True:
            task = self.get_task()
            if task is None:
                time.sleep(self.SLEEP_INTERVAL)
            else:
                self.download(task)