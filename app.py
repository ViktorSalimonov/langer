from flask import Flask, request
from queue import Queue

from server.dataprocessor import DataProcessor
from server.downloadhandler import DownloadHandler
from server.downloadworker import DownloadWorker
from server.ratelimiter import RateLimiter

app = Flask(__name__)

WORKERS_COUNT = 3

download_queue = Queue()
processing_queue = Queue()

download_handler = DownloadHandler(download_queue)
rate_limiter = RateLimiter(download_queue)

for i in range(WORKERS_COUNT):
    thread = DownloadWorker(rate_limiter, processing_queue)
    thread.daemon = True
    thread.start()

data_processor = DataProcessor(processing_queue)
data_processor.daemon = True
data_processor.start()


def create_tasks(text):
    lines = text.splitlines()
    for line in lines:
        global download_handler
        download_handler.put_url(line)


@app.route("/result")
def result():
    global data_processor
    stats = data_processor.stats
    return str(stats)


@app.route("/task", methods=['POST'])
def put():
    if request.method == 'POST':
        create_tasks(request.data)
    return 'task route'


@app.route("/")
def index():
    return 'index route'


if __name__ == '__main__s':
    app.run()