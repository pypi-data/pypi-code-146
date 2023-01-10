import csv
from pathlib import Path

pinyin_file = Path(__file__).parent / 'pinyin_list.csv'

csv_file = open(pinyin_file, 'r', encoding='utf-8')
reader = csv.DictReader(csv_file)
PINYIN_ZI_DICT = {x['pinyin']: x['zi'] for x in reader}
PINYIN_LIST = PINYIN_ZI_DICT.keys()
csv_file.close()
