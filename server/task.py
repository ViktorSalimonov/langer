import datetime
import uuid

class Task(object):

    def __init__(self):
        self.created = datetime.datetime.utcnow()
        self.id = uuid.uuid4().hex

class URLTask(Task):

    def __init__(self, url):
        super().__init__()
        self.url = url