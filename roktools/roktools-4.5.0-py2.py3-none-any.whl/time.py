from collections import namedtuple
import datetime
import math

WeekTow = namedtuple('WeekTow', 'week tow day_of_week')

GPS_TIME_START = datetime.datetime(1980, 1, 6, 0, 0, 0)
J2000_TIME_START = datetime.datetime(2000, 1, 1, 12, 0, 0)
SECONDS_IN_DAY = 24 * 60 * 60
SECONDS_IN_WEEK = 86400 * 7
GPS_AS_J2000 = -630763200

class Timespan:
    def __init__(self, start: datetime.datetime, end: datetime.datetime):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start} - {self.end}"
    
    def overlap(self, other: 'Timespan') -> bool:
        return (self.start <= other.end) and (self.end >= other.start)
    
    def duration(self) -> datetime.timedelta:
        return self.end - self.start
    
    def duration_seconds(self) -> int:
        return int((self.end - self.start).total_seconds())
    
    def duration_minutes(self) -> float:
        return self.duration_seconds() / 60
    
    def duration_hours(self) -> float:
        return self.duration_minutes() / 60
    
    def duration_days(self) -> float:
        return self.duration_hours() / 24

        
def to_week_tow(epoch: datetime.datetime) -> WeekTow:
    """
    Convert from datetime to GPS week

    >>> to_week_tow(datetime.datetime(1980, 1, 6))
    WeekTow(week=0, tow=0.0, day_of_week=0)
    >>> to_week_tow(datetime.datetime(2005, 1, 28, 13, 30))
    WeekTow(week=1307, tow=480600.0, day_of_week=5)

    Conversion method based on algorithm provided in this link
    http://www.novatel.com/support/knowledge-and-learning/published-papers-and-documents/unit-conversions/
    """

    timedelta = epoch - GPS_TIME_START

    gpsw = int(timedelta.days / 7)
    day = timedelta.days - 7 * gpsw
    tow = timedelta.microseconds * 1e-6 + timedelta.seconds + day * SECONDS_IN_DAY

    return WeekTow(gpsw, tow, day)


# ------------------------------------------------------------------------------

def from_week_tow(week: int, tow: float) -> datetime.datetime:
    """
    Convert from datetime to GPS week

    >>> from_week_tow(0, 0.0)
    datetime.datetime(1980, 1, 6, 0, 0)
    >>> from_week_tow(1307, 480600.0)
    datetime.datetime(2005, 1, 28, 13, 30)
    """

    delta = datetime.timedelta(weeks=week, seconds=tow)

    return GPS_TIME_START + delta


def weektow_to_datetime(tow: float, week: int) -> datetime.datetime:
    import warnings
    warnings.warn("This function will be replaced by 'from_week_tow'", DeprecationWarning, stacklevel=2)
    return from_week_tow(week, tow)


def weektow_to_j2000(tow: float, week: int) -> float:
    """
    Convert from GPS week and time of the week (in seconds) to j2000 seconds

    The week and tow values can be vectors, and thus it will return a vector of
    tuples.

    >>> weektow_to_j2000(0, 0.0)
    -630763200.0
    """

    j2000s = week * SECONDS_IN_WEEK
    j2000s += tow

    # Rebase seconds from GPS start origin to J2000 start origin
    j2000s += GPS_AS_J2000

    return j2000s


def to_j2000(epoch: datetime.datetime) -> float:
    """
    Convert from datetime toj2000 seconds

    >>> to_j2000(datetime.datetime(2005, 1, 28, 13, 30))
    160191000.0
    """
    week_tow = to_week_tow(epoch)
    return weektow_to_j2000(week_tow.tow, week_tow.week)

def from_j2000(j2000s: int, fraction_of_seconds: float = 0.0) -> datetime.datetime:
    """
    Convert from J2000 epoch to datetime

    >>> from_j2000(160191000)
    datetime.datetime(2005, 1, 28, 13, 30)

    >>> from_j2000(160191000, fraction_of_seconds = 0.1)
    datetime.datetime(2005, 1, 28, 13, 30, 0, 100000)
    """

    microseconds = int(fraction_of_seconds * 1.0e6)
    epoch = J2000_TIME_START + datetime.timedelta(seconds=j2000s, microseconds=microseconds)

    return epoch


def epoch_range(start_epoch, end_epoch, interval_s):
    """
    Iterate between 2 epochs with a given interval

    >>> import datetime
    >>> st = datetime.datetime(2015, 10, 1,  0,  0,  0)
    >>> en = datetime.datetime(2015, 10, 1,  0, 59, 59)
    >>> interval_s = 15 * 60
    >>> ','.join([str(d) for d in epoch_range(st, en, interval_s)])
    '2015-10-01 00:00:00,2015-10-01 00:15:00,2015-10-01 00:30:00,2015-10-01 00:45:00'
    >>> st = datetime.datetime(2015, 10, 1,  0,  0,  0)
    >>> en = datetime.datetime(2015, 10, 1,  1,  0,  0)
    >>> interval_s = 15 * 60
    >>> ','.join([str(d) for d in epoch_range(st, en, interval_s)])
    '2015-10-01 00:00:00,2015-10-01 00:15:00,2015-10-01 00:30:00,2015-10-01 00:45:00,2015-10-01 01:00:00'
    """

    total_seconds = (end_epoch - start_epoch).total_seconds() + interval_s / 2.0
    n_intervals_as_float = total_seconds / interval_s
    n_intervals = int(n_intervals_as_float)
    if math.fabs(n_intervals - n_intervals_as_float) >= 0.5:
        n_intervals = n_intervals + 1

    for q in range(n_intervals):
        yield start_epoch + datetime.timedelta(seconds=interval_s * q)



