import os
from prettytable import PrettyTable

def count_in_file(file_name):
    res = {'code': 0,
        'comments': 0,
        'empty': 0,}
    
    with open(file_name, 'r', encoding='UTF-8') as f:
        strings = f.readlines()
        
    is_comment = ''
    for string in strings:
        s = string.replace(' ', '').replace('\n', '')
        if is_comment != '':
            res['comments'] += 1
            if string[-4:-1] == is_comment:
                is_comment = '' 
        elif s == '':
            res['empty'] += 1
        elif s[0] == '#':
            res['comments'] += 1
        elif s.startswith("'''") or s.startswith('"""'):
            res['comments'] += 1
            if string[-4:-1] == s[:3]:
                continue
            is_comment = s[:3]
        else:
            res['code'] += 1
    return res
        

def get_all_files(dirs):
    res = []
    new_dirs = []
    for dir_name in dirs:
        for i in os.scandir(dir_name):
            if os.path.isfile(i):
                if i.name[i.name.find('.'):] == '.py':
                    res.append(i.path)
            else:
                new_dirs.append(i.path)
    if new_dirs == []:
        return res
    return res + get_all_files(new_dirs)
    

def count_in_dir(dir_name):
    dirs = [dir_name]
    files = get_all_files(dirs)

    table = PrettyTable(['file_name', 'code', 'comments', 'empty'])
    sum_res = {'code': 0,
            'comments': 0,
            'empty': 0,}
    for file in files:
        q = count_in_file(file)
        sum_res['code'] += q['code']
        sum_res['comments'] += q['comments']
        sum_res['empty'] += q['empty']
        table.add_row([file, q['code'], q['comments'], q['empty']])
    table.add_row(['Total', sum_res['code'], sum_res['comments'], sum_res['empty']])
    print(table)