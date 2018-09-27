import re
import langid
import threading
import time

import json
import pandas as pd


class DataProcessor(threading.Thread):
    SLEEP_INTERVAL = 10

    def __init__(self, processing_queue):
        threading.Thread.__init__(self)
        self.processing_queue = processing_queue
        self.df = pd.DataFrame(columns=['url', 'word', 'lang', 'conf'])


    def get_task(self):
        return self.processing_queue.get()

    def lang_detection(self, text):
        lang, confidence = langid.classify(text)
        return lang, confidence


    def get_word(self, text):
        return re.compile('\w+').findall(text)


    def run(self):
        while True:
            task = self.get_task()
            if task is None:
                time.sleep(self.SLEEP_INTERVAL)
            else:
                self.lang_detection(task.content)
                words = self.get_word(task.content)
                for word in words:
                    lang, conf = self.lang_detection(word)
                    stats_entry = [task.url, word, lang, conf]
                    self.df.loc[len(self.df)] = stats_entry
                uniq_pages = self.df['url'].unique()
                uniq_langs = self.df['lang'].unique()
                lang_count_pages = self.df.groupby('lang').apply(lambda x: x['url'].nunique())
                lang_count_words = self.df.groupby('lang').apply(lambda x: x['word'].nunique())
                word_frequency = self.df['word'].value_counts()

                result = {
                    "unique pages": uniq_pages.tolist(),
                    "unique languages": uniq_langs.tolist(),
                    "language - pages count": lang_count_pages.to_dict(),
                    "language - unique words count": lang_count_words.to_dict(),
                    "word frequency": word_frequency.to_dict()
                }

                with open("result/statistics.json", "w") as write_file:
                    json.dump(result, write_file)