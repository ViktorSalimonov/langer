import datetime


class RateLimiter(object):

    RATE_LIMIT = 3  # tasks per minute

    def __init__(self, download_queue):
        self.download_queue = download_queue
        self.time_list = []


    def __is_allowed(self):
        if len(self.time_list) == 0:
            return True
        delta_time = datetime.timedelta(minutes=1)
        last_attempts = list(filter(lambda x: self.__now() - x[0] < delta_time, self.time_list))
        for s in self.time_list:
            if s not in last_attempts:
                self.time_list.remove(s)
        return len(last_attempts) < self.RATE_LIMIT


    def __now(self):
        return datetime.datetime.utcnow()


    def get_task(self):
        if self.__is_allowed():
            task = self.download_queue.get()
            if task is not None:
                self.time_list.append([self.__now(), task.id])
                return task
        return None