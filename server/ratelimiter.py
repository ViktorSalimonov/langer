import datetime


class RateLimiter(object):

    RATE_LIMIT = 3  # tasks per minute

    def __init__(self, task_queue):
        self.task_queue = task_queue
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
            task = self.task_queue.get()
            if task is not None:
                self.time_list.append([self.__now(), task.id])
                return task
        return None