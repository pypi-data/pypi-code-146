from datetime import datetime, date, timedelta
import datefinder
import calendar
from dateutil.relativedelta import relativedelta


class ClassTime:
    """Class to maintain the default and standard date and time application wide.
        Class have the following methods in the class by far:
            add_date
            add_hour
            add_min
            alternative
            check_am_pm
            daily
            get_date_and_time
            get_day_of_week
            get_weekdays
            is_time_passed
            now_date
            now_time
            string_to_date
            string_to_time
            string_to_time_with_date
            string_value
            subtract_date
            subtract_hour
            subtract_min
            time_digit
            weekends
    """
    now_time = datetime.now().time().__format__('%H:%M:%S')
    now_date = date.today()
    how_many = 0
    string_value = ' '

    def subtract_hour(self, from_time, how_many):
        self.how_many = how_many
        """Need from time and number of hours needs to be subtracted. returns datetime.datetime value"""
        from_time = str(from_time).split('.')[0]
        new_time = (datetime.strptime(str(from_time), '%H:%M:%S') - timedelta(hours=int(self.how_many))).time()
        return new_time

    def add_hour(self, from_time, how_many):
        self.how_many = how_many
        """Need from time and number of hours needs to be Added. returns datetime.date value"""
        from_time = str(from_time).split('.')[0]
        new_time = (datetime.strptime(str(from_time), '%H:%M:%S') + timedelta(hours=int(self.how_many))).time()
        return new_time

    def subtract_date(self, from_date, how_many):
        self.how_many = how_many
        """Need from date and number of days needs to be subtracted. returns datetime.date value"""
        new_date = datetime.strptime(str(from_date - timedelta(days=int(self.how_many))), '%Y-%m-%d')
        return new_date

    def add_date(self, from_date, how_many):
        self.how_many = how_many
        """Need from date and number of days needs to be added. returns datetime.date value"""
        new_date = datetime.strptime(str(from_date + timedelta(days=int(self.how_many))), '%Y-%m-%d')
        return new_date

    def string_to_date(self, date_string):
        """Need date which need to be converted into datetime.datetime format."""
        self.string_value = date_string
        convert_date = datetime.strptime(str(self.string_value), '%Y-%m-%d').date()
        return convert_date

    def string_to_time(self, time_string):
        """Need time which need to be converted into datetime.datetime format."""
        self.string_value = time_string
        convert_time = datetime.strptime(str(self.string_value), '%H:%M:%S').time()
        return convert_time

    def get_day_of_week(self):
        """Return the day number in string format being 0 as Monday and 6 as Sunday"""
        self.string_value = datetime.today().weekday()
        return str(self.string_value)

    def subtract_min(self, from_time, how_many):
        """Need from time and number of minutes needs to be subtracted. returns datetime.datetime value"""
        self.string_value = str(from_time).split('.')[0]
        new_time = (datetime.strptime(str(self.string_value), '%H:%M:%S') -
                    timedelta(minutes=int(how_many))).time()
        return new_time

    def add_min(self, from_time, how_many):
        """Need from time and number of minutes needs to be subtracted. returns datetime.datetime value"""
        self.string_value = str(from_time).split('.')[0]
        new_time = (datetime.strptime(str(self.string_value), '%H:%M:%S') +
                    timedelta(minutes=int(how_many))).time()
        return new_time

    def string_to_time_with_date(self, time_string):
        """string to time with date value: 1900-01-01 19:14:02 <class 'datetime.datetime'> the date will be always
        1900-01-01 """
        self.string_value = datetime.strptime(str(time_string), '%H:%M:%S')
        return self.string_value

    def daily(self):
        """Get tomorrow's date"""
        return self.add_date(self.now_date, 1)

    def weekends(self):
        date_format = self.string_to_date(self.now_date)
        weekday_count = calendar.weekday(
            day=date_format.day, month=date_format.month, year=date_format.year)
        if int(weekday_count) == 5:
            return_date = self.add_date(str(date_format), 1)
        else:
            saturday = date_format + \
                       timedelta((calendar.SATURDAY - date_format.weekday()) % 7)
            return_date = saturday
        # print(return_date)
        return return_date

    def upcoming_weekends_from_specific_date(self, string_date):
        date_format = self.string_to_date(string_date)
        weekday_count = calendar.weekday(
            day=date_format.day, month=date_format.month, year=date_format.year)
        if int(weekday_count) == 5:
            return_date = self.add_date(str(date_format), 1)
        else:
            saturday = date_format + \
                       timedelta((calendar.SATURDAY - date_format.weekday()) % 7)
            return_date = saturday
        # print(return_date)
        return return_date

    def get_weekdays(self):
        date_format = self.string_to_date(self.now_date)
        weekday_count = calendar.weekday(
            day=date_format.day, month=date_format.month, year=date_format.year)
        if int(weekday_count) in [5, 6, 4]:
            monday = date_format + \
                     timedelta((calendar.MONDAY - date_format.weekday()) % 7)
            return_date = monday
        else:
            return_date = self.add_date(date_format, 1)
        # print(return_date)
        return return_date

    def alternative(self):
        return_date = self.add_date(self.now_date, 2)
        return return_date

    def is_time_passed(self, item_time):
        try:
            # print(item_time, (string_to_time(get_time())-string_to_time(item_time)).days)
            if (self.string_to_time_with_date(self.now_time) - self.string_to_time_with_date(item_time)).days < 0:
                # print(False)
                return False
            else:
                # print(True)
                return True
        except Exception as e:
            print(e)
            # print(False)
            return False

    def get_date_and_time_for_alarm(self, text_string):
        get_date_and_time = False
        item_date, item_time = '', ''
        reminder_date = list(datefinder.find_dates(text_string))
        for item in reminder_date:
            item_date = item.date()
            item_time = item.time()
            if (self.string_to_time_with_date(self.now_time) - self.string_to_time_with_date(item_time)).days < 0:
                get_date_and_time = False
            else:
                get_date_and_time = True
            if get_date_and_time is True:
                item_date = item_date + timedelta(days=1)
        return get_date_and_time, str(item_date), str(item_time)

    def get_date_and_time(self, text_string):
        self.string_value = text_string
        item_date, item_time = '', ''
        reminder_date = list(datefinder.find_dates(self.string_value))
        for item in reminder_date:
            item_date = item.date()
            item_time = item.time()
        return str(item_date), str(item_time)

    def check_am_pm(self, text_string):
        self.string_value = text_string
        try:
            if str(self.string_value).lower().__contains__('a.m.') or str(self.string_value).lower().__contains__(
                    'p.m.'):
                return self.string_value
            elif str(self.string_value).lower().__contains__('a.m') or str(self.string_value).lower().__contains__(
                    'p.m'):
                return self.string_value
            elif str(self.string_value).lower().__contains__('am') or str(self.string_value).lower().__contains__('pm'):
                return self.string_value
            else:
                return False
        except Exception as e:
            print(e)
            pass

    def time_digit(self, text_string):
        self.string_value = ""
        for word in text_string:
            if word.isdigit():
                self.string_value = self.string_value + str(word)
        if self.string_value == "":
            return False
        else:
            return self.string_value

    def task_in_next_hour(self, task_time):
        try:
            now_time = self.add_min(str(self.now_time), how_many=1)
            if self.string_to_time(now_time).replace(second=0) == self.string_to_time(task_time).replace(second=0):
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def get_date_after_month(self, text_date, month_num):
        """add month to date"""
        result = self.string_to_date(date_string=str(text_date))
        result = datetime(year=result.year,month=result.month, day=result.day, hour=0, minute=0, second=0)
        result = result + relativedelta(months=month_num)
        return result

    def get_date_before_month(self, text_date, month_num):
        """ Subtract the month from the date"""
        result = self.string_to_date(date_string=str(text_date))
        result = datetime(year=result.year,month=result.month, day=result.day, hour=0, minute=0, second=0)
        result = result - relativedelta(months=month_num)
        return result
