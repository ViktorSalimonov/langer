import re
import langid
import threading
import time


class DataProcessor(threading.Thread):
    SLEEP_INTERVAL = 10

    def __init__(self, processing_queue):
        threading.Thread.__init__(self)
        self.processing_queue = processing_queue
        self.stats = {
            "total_pages_count": 0,
            "unique_langs": []
        }


    def get_task(self):
        return self.processing_queue.get()

    def lang_detection(self, text):
        lang, confidence = langid.classify(text)
        return lang


    def get_word(self, text):
        return re.compile('\w+').findall(text)


    def statistics(self, word, lang):
        if lang not in self.stats["unique_langs"]:
            self.stats["unique_langs"].append(lang)


    def run(self):
        while True:
            task = self.get_task()
            if task is None:
                time.sleep(self.SLEEP_INTERVAL)
            else:
                self.stats["total_pages_count"] += 1
                self.lang_detection(task.content)
                words = self.get_word(task.content)
                for word in words:
                    lang = self.lang_detection(word)
                    self.statistics(word, lang)