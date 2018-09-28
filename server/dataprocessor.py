import json
import re
import langid
import pandas as pd
import threading
import time


class DataProcessor(threading.Thread):
    SLEEP_INTERVAL = 10

    def __init__(self, processing_queue):
        threading.Thread.__init__(self)
        self.processing_queue = processing_queue
        self.persist = pd.DataFrame(columns=['url', 'sntc', 'lang', 'conf'])


    def get_task(self):
        return self.processing_queue.get()


    def lang_detection(self, text):
        lang, confidence = langid.classify(text)
        return lang, confidence


    def get_words(self, text):
        return re.compile('\w+').findall(text)


    def get_sentences(self, text):
        sentences = list(map(str.strip, re.split(r"[.!?](?!$)", text)))
        return sentences


    @staticmethod
    def generate_statistics(df):
        uniq_pages = df['url'].unique()
        uniq_langs = df['lang'].unique()
        lang_count_pages = df.groupby('lang').apply(lambda x: x['url'].nunique())
        lang_count_words = df.groupby('lang').apply(lambda x: x['sntc'].nunique())
        #word_frequency = df.groupby('lang').apply(lambda x: x['word'].value_counts())
        result = {
            "total_unique_pages": uniq_pages.tolist(),
            "total_unique_languages": uniq_langs.tolist(),
            "language_page_count": lang_count_pages.to_dict(),
            "language_sentence_count": lang_count_words.to_dict(),
            #"word frequency": word_frequency.to_dict()

        }
        return result


    def get_stat(self):
        return DataProcessor.generate_statistics(self.persist)


    def process(self, task):
        sentences = self.get_sentences(task.content)
        df = pd.DataFrame(columns=['url', 'sntc', 'lang', 'conf'])
        for sentence in sentences:
            lang, conf = self.lang_detection(sentence)
            stats_entry = [task.url, sentence, lang, conf]
            df.loc[len(df)] = stats_entry

        self.persist = self.persist.append(df, ignore_index=True)


    def run(self):
        while True:
            task = self.get_task()
            if task is None:
                time.sleep(self.SLEEP_INTERVAL)
            else:
                self.process(task)

                # with open("result/statistics.json", "w") as write_file:
                #     json.dump(statistics, write_file, ensure_ascii=False)