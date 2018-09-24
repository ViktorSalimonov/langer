import threading
import time

class DownloadWorker(threading.Thread):
    SLEEP_INTERVAL = 10

    def __init__(self, rl, data_processor):
        threading.Thread.__init__(self)
        self.data_processor = data_processor
        self.rl = rl

    def get_task(self):
        return self.rl.get_task()

    def processing(self, task):
        self.data_processor.put_task(task)

    def run(self):
        while True:
            task = self.get_task()
            if task is None:
                time.sleep(self.SLEEP_INTERVAL)
            else:
                self.processing(task)