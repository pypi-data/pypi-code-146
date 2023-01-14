import time


class Date:
    def __init(self):
        pass

    @staticmethod
    def date_range(start_date, end_date):
        start_ts = int(time.mktime(time.strptime(start_date, '%Y-%m-%d')))
        end_ts = int(time.mktime(time.strptime(end_date, '%Y-%m-%d')))
        dates = []
        while start_ts <= end_ts:
            cur_date = time.strftime('%Y-%m-%d', time.localtime(start_ts))
            start_ts += 24 * 3600
            dates.append(cur_date)
        return dates


if __name__ == '__main__':
    date = Date()
    date.date_range('2022-01-01', '2022-01-09')

