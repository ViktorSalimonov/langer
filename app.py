from flask import Flask, request
from queue import Queue

from server.downloadhandler import DownloadHandler
from server.ratelimiter import RateLimiter

app = Flask(__name__)

url_task_queue = Queue()

download_handler = DownloadHandler(url_task_queue)
rate_limiter = RateLimiter(url_task_queue)




def create_tasks(text):
    lines = text.splitlines()
    for line in lines:
        global download_handler
        download_handler.put_url(line)


@app.route("/result")
def result():
    return 'result route'


@app.route("/task", methods=['POST'])
def put():
    if request.method == 'POST':
        create_tasks(request.data)
    return 'task route'


@app.route("/")
def index():
    return 'index route'


if __name__ == "__main__":
    app.run()