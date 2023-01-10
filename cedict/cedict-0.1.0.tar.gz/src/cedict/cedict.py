#! usr/env/python
# coding=utf-8


import os
import string
import csv
from sqlite3 import connect

ABSPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORDS_DB_PATH = ABSPATH + "/cedict/db/words.db"
WORDS_CSV_PATH = ABSPATH + "/cedict/csv/EnWords.csv"


class DictionaryData:
    def __init__(self):
        self.conn = connect(WORDS_DB_PATH)
        self.cur = self.conn.cursor()


def search(word, dictionary_data):
    if check_if_english(word):
        dictionary_data.cur.execute(f'SELECT * FROM words where english LIKE "{word}";')
        rows = dictionary_data.cur.fetchall()
        if rows:
            return rows[0]
        else:
            return ()
    else:
        dictionary_data.cur.execute(f'SELECT * FROM words where chinese LIKE "%{word}%";')
        rows = dictionary_data.cur.fetchall()
        return reduce_chinese_result(rows, word)


def check_if_english(word):
    for i in word:
        if i not in string.printable:
            break
    else:
        return True
    return False


def reduce_chinese_result(result_list, word):
    result_list.sort(key=tuple_size)
    for row in result_list:
        for n in row[1].split(","):
            n = n.replace("n.", "").replace("adj.", "").replace("adv.", "").replace("vt.", "").replace("v.", "")
            if n == word:
                return row
    else:
        if result_list:
            return result_list[0]
        else:
            return ()


def tuple_size(tuple):
    return len(tuple[1])


class DbSetup:
    def __init__(self):

        self.del_db_if_exists()

        self.conn = connect(WORDS_DB_PATH)
        self.cur = self.conn.cursor()

    def del_db_if_exists(self):
        if os.path.exists(WORDS_DB_PATH):
            os.remove(WORDS_DB_PATH)

    def setup(self):
        print('creating table for words')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS words (english TEXT, chinese TEXT)''')

        print('inserting EnWords csv into database')
        with open(WORDS_CSV_PATH, 'r', encoding="utf8") as f:
            csv_content = csv.reader(f)
            for index, i in enumerate(csv_content):
                if index == 0:
                    continue
                print('inserting ' + str(i))
                self.cur.execute('INSERT INTO words VALUES (?,?);', i)

        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    dict_db = DictionaryData()
    print(search("apple", dict_db))
