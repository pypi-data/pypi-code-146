from string import punctuation
from collections import Counter
import re
import demoji



class WordTools():
    """Tools for formating string"""
    @classmethod
    def count_word(cls, words_list):
        d = {}
        words_count =  Counter(words_list).most_common()
        for item in words_count:
            k,v = item
            if k:
                d[k] = v
        return d

    @classmethod
    def text_cleaner(cls, text):
        """clean string text"""
        text = text.lower()
        text = re.sub('[%s]' % re.escape(punctuation), ' ', text)
        text = re.sub('\d+', ' ', text)
        text = re.sub('\n', ' ', text)
        return text

    @classmethod
    def extract_emojis(cls, text):
        d = {}
        emojis_list = list(demoji.findall(text))
        emojis_found = [c for c in text if c in emojis_list]
        for e in emojis_found:
            d[e] = emojis_found.count(e)
        return dict(sorted(d.items(), key = lambda item: item[1], reverse=True)) if d else {"-":0}
    

    @classmethod
    def __count_times(cls, counter, template):
        for t in template:
                if t not in counter.keys():
                    counter[t] = 0

        counter = sorted(counter.items(), key= lambda d : template.index(d[0]))
        return dict(counter)

    @classmethod
    def months_list(cls):
        return ["January", "February", "March", "April", "May","June", "July", "August","September", "October", "November", "December"]

    @classmethod
    def days_list(cls):
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    @classmethod
    def count_hour(cls, datetime_list):
        """Count the occurences of hours on list of timestamp"""
        hours_template = range(0,24)
        hours_count = Counter([ i.hour for i in datetime_list])
        return cls.__count_times(hours_count, hours_template)


    @classmethod
    def count_day(cls, datetime_list):
        """Count the occurences of days on list of timestamps"""

        days_template = cls.days_list()
        days_count = Counter([ i.day_name() for i in datetime_list])

        return cls.__count_times(days_count, days_template)

    @classmethod
    def count_month(cls, datetime_list):
        "Count the occurences of mnth in list of timestamps"
        months_template = cls.months_list()
        months_count = Counter([ i.month_name() for i in datetime_list])
        return cls.__count_times(months_count, months_template)

    @classmethod
    def month_name(cls, index):
        return cls.months_list()[index-1]

    