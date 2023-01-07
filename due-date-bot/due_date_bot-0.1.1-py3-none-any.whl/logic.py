from datetime import datetime, timedelta
from typing import List, Union

# https://www.babycentre.co.uk/a1004000/average-fetal-length-and-weight-chart
dataset = [  # length [cm], mass [g]
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (1.6, 1),  # 8th week
    (2.3, 2),
    (3.1, 4),
    (4.1, 7),
    (5.4, 14),
    (7.4, 23),
    (8.7, 43),
    (10.1, 70),
    (11.6, 100),
    (13.0, 140),
    (14.2, 190),
    (15.3, 240),
    (25.6, 300),
    (26.7, 360),
    (27.8, 430),
    (28.9, 500),
    (30.0, 600),
    (34.6, 660),
    (35.6, 760),
    (36.6, 875),
    (37.6, 1000),
    (38.6, 1200),
    (39.9, 1300),
    (41.1, 1500),
    (42.4, 1700),
    (43.7, 1900),
    (45.0, 2100),
    (46.2, 2400),
    (47.4, 2600),
    (48.6, 2900),
    (49.8, 3100),
    (50.7, 3300),
    (51.2, 3500),
    (51.5, 3600),
    (51.7, 3700)
]


class Pregnancy:

    pregnancy_duration: timedelta = timedelta(weeks=40)
    due_date: datetime

    def __init__(self, due_date: Union[datetime, str]) -> None:
        if isinstance(due_date, str):
            due_date = self.__parse_datetime(due_date)
        self.due_date = due_date

    @staticmethod
    def __parse_datetime(date: str):
        return datetime.fromisoformat(date)

    @staticmethod
    def __interpolate(week, day):
        if week < 0 or week >= len(dataset):
            return
        if day < 0 or day >7:
            return
        if week >= (len(dataset) - 1):
            return dataset[week]
        size0, grams0 = dataset[week]
        size1, grams1 = dataset[week + 1]

        coefficient = day/7
        return size0 + coefficient * (size1 - size0), grams0 + coefficient * (grams1 - grams0)


    @classmethod
    def from_last_menstrual_cycle(cls, last_period_first_day: Union[datetime, str]):
        if isinstance(last_period_first_day, str):
            last_period_first_day = cls.__parse_datetime(last_period_first_day)
        return cls(last_period_first_day - timedelta(days=90) + timedelta(days=370))

    @classmethod
    def from_conception_date(cls, conception_date: Union[datetime, str]):
        if isinstance(conception_date, str):
            conception_date = cls.__parse_datetime(conception_date)
        return cls(conception_date + timedelta(days=266))

    @classmethod
    def by_type(cls, date: Union[datetime, str], type_: str):
        if type_ == "menstrual":
            return cls.from_last_menstrual_cycle(date)
        if type_ == "conception":
            return cls.from_conception_date(date)
        return cls(date)

    @property
    def remaining(self) -> timedelta:
        return self.due_date - datetime.now()

    @property
    def elapsed(self) -> timedelta:
        return datetime.now() - (self.due_date - self.pregnancy_duration)

    @property
    def elapsed_mm_dd(self) -> [int, int]:
        months_r = int(self.elapsed.days / 30)
        days_r = self.elapsed.days - months_r * 30
        return months_r, days_r

    @property
    def remaining_mm_dd(self) -> [int, int]:
        months_r = int(self.remaining.days / 30)
        days_r = self.remaining.days - months_r * 30
        return months_r, days_r

    @property
    def week(self) -> int:
        week, _ = self.week_plus
        return week

    @property
    def day(self) -> int:
        _, day = self.week_plus
        return day

    @property
    def week_plus(self) -> List[int]:
        weeks = int(self.elapsed.days/7)
        days = self.elapsed.days - (weeks * 7)
        return [weeks, days]

    @property
    def grams(self) -> float:
        _, grams = self.__interpolate(*self.week_plus)
        return round(grams, 1)

    @property
    def size(self) -> float:
        size, _ = self.__interpolate(*self.week_plus)
        return round(size, 1)
