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
        self.persist = pd.DataFrame(columns=['url', 'word', 'lang', 'conf'])


    def get_task(self):
        return self.processing_queue.get()

    def lang_detection(self, text):
        lang, confidence = langid.classify(text)
        return lang, confidence


    def get_word(self, text):
        return re.compile('\w+').findall(text)

    @staticmethod
    def generate_statistics(df):
        uniq_pages = df['url'].unique()
        uniq_langs = df['lang'].unique()
        lang_count_pages = df.groupby('lang').apply(lambda x: x['url'].nunique())
        lang_count_words = df.groupby('lang').apply(lambda x: x['word'].nunique())
        word_frequency = df.groupby('lang').apply(lambda x: x['word'].value_counts())
        result = {
            "unique pages": uniq_pages.tolist(),
            "unique languages": uniq_langs.tolist(),
            "pages count": lang_count_pages.to_dict(),
            "language - unique words count": lang_count_words.to_dict(),
            "word frequency": word_frequency.to_dict()

        }
        return result

    def get_stat(self):
        return DataProcessor.generate_statistics(self.persist)

    def process(self, task):
        words = self.get_word(task.content)
        print(words)
        df = pd.DataFrame(columns=['url', 'word', 'lang', 'conf'])
        for word in words:
            lang, conf = self.lang_detection(word)
            stats_entry = [task.url, word, lang, conf]
            df.loc[len(df)] = stats_entry

        self.persist = self.persist.append(df, ignore_index=True)

    def run(self):
        while True:
            task = self.get_task()
            if task is None:
                time.sleep(self.SLEEP_INTERVAL)
            else:
                #content_lang, confidence = self.lang_detection(task.content)
                self.process(task)
                # with open("result/statistics.json", "w") as write_file:
                #     json.dump(statistics, write_file, ensure_ascii=False)