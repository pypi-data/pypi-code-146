import csv

with open('pinyin_list.txt', 'r', encoding='utf-8') as f:
    pinyin_list = [x.strip().split() for x in f.readlines()]

with open('pinyin_list.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['pinyin', 'count', 'zi'])
    for each in pinyin_list:
        writer.writerow([each[0], len(each[1]), each[1]])
