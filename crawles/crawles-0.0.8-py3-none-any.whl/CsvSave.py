import csv


class CsvSave(object):
    """csv文件存储"""

    def __init__(self, filename, mode='r+',
                 encoding='gbk',
                 newline='',
                 **kwargs):

        self._f = open(filename, mode,
                       encoding=encoding,
                       newline=newline,
                       **kwargs)

        if 'r' in mode and '+' not in mode:
            self._csv_f = csv.reader(self._f)
        else:
            self._csv_f = csv.writer(self._f)

    def head(self, head_list):
        """头数据写入"""
        if not isinstance(head_list, list):
            raise Exception('写入类型错误')
        self._csv_f.writerow(head_list)

    def writerow(self, list_data):
        """写入一行[9,'no']"""
        self._csv_f.writerow(list_data)

    def writerows(self, list_data):
        """一次写入多行[[8,'yes'],[9,'no']]"""
        self._csv_f.writerows(list_data)

    def close(self):
        self._f.close()

    def __del__(self):
        self._f.close()

    def __enter__(self):
        """上下文管理器返回"""
        return self  # 不要返回句柄，否则讲将不用有head写入

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器关闭"""
        self._f.close()


csv_save = CsvSave
if __name__ == '__main__':
    pass
    csv_obj = CsvSave('data.csv', mode='w+')
    csv_obj.head(['1', '2', '3', '4'])
    csv_obj.writerow(['a', 'b', 'c', 'd'])
    csv_obj.writerows([['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']])

    with CsvSave('data.csv', mode='w+') as csv_obj:
        csv_obj.head(['1', '2', '3', '4'])
        csv_obj.writerow(['a', 'b', 'c', 'd'])
        csv_obj.writerows([['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']])
