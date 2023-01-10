# -*- coding: utf-8 -*-
""" Time Helper and Utility Methods """


from datetime import datetime


class TimeHelper(object):
    """ Time Helper and Utility Methods """

    def ts_to_dict(ts: str or int) -> dict:
        """ Transform a Timestamp into a typed Dictionary

        Args:
            ts (str or int): any timestamp

        Raises:
            NotImplementedError: Unrecognized isoweekday value

        Returns:
            dict: a typed dictionary for the timestamp
        """

        dt = datetime.fromtimestamp(int(ts))

        def day_of_week(x: int) -> str:
            if x == 1:
                return 'Monday'
            if x == 2:
                return 'Tuesday'
            if x == 3:
                return 'Wednesday'
            if x == 4:
                return 'Thursday'
            if x == 5:
                return 'Friday'
            if x == 6:
                return 'Saturday'
            if x == 7:
                return 'Sunday'
            raise NotImplementedError(x)

        return {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'dayname': day_of_week(dt.isoweekday()),
            'iso': dt.isoformat()
        }
