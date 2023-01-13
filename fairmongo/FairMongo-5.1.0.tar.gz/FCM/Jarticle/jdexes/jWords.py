from F import DATE
from F import DICT
from F.LOG import Log
from FCM.Jarticle import JQ
from FCM.Jarticle.jProvider import jSearch

Log = Log("jCompany")

WORDS_COLLECTION = "words"

""" Master Class to work with Companies Collection """
class jWords(jSearch):

    @classmethod
    def constructor_jwords(cls):
        nc = cls()
        nc.construct_mcollection(WORDS_COLLECTION)
        return nc

    def add_words(self, date, words):
        # get words for date
        # merge words dict
        existingRecord = self.get_word_list_for_date(date)
        existingWordsDict = DICT.get("grams", existingRecord, False)
        if existingWordsDict:
            pass
        masterQuery = {
            "articleDate": date,
            "updatedDate": DATE.mongo_date_today_str(),
            "grams": DICT.get("grams", words),
            "bigrams": DICT.get("bigrams", words),
            "trigrams": DICT.get("trigrams", words),
            "quadgrams": DICT.get("quadgrams", words)
        }
        self.update_record(JQ.DATE(date), masterQuery)

    def get_word_list_for_date(self, date):
        return self.base_query(JQ.DATE(date))

    def add_words_to_list_for_date(self):
        pass


if __name__ == '__main__':
    jc = jWords.constructor_jwords()
