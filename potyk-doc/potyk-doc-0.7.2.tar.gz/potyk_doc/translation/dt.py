import datetime as dt
from dataclasses import dataclass
from typing import Union

from potyk_doc.translation.case import Case

MONTHS = {
    Case.Nominative: {
        1: "январь",
        2: "февраль",
        3: "март",
        4: "апрель",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "август",
        9: "сентябрь",
        10: "октябрь",
        11: "ноябрь",
        12: "декабрь",
    },
    Case.Genitive: {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    },
    Case.Prepositional: {
        1: "январе",
        2: "феврале",
        3: "марте",
        4: "апреле",
        5: "мае",
        6: "июне",
        7: "июле",
        8: "августе",
        9: "сентябре",
        10: "октябре",
        11: "ноябре",
        12: "декабре",
    },
}


def date_to_ru(date_: dt.date, case: Case = Case.Genitive, without_day: bool = False) -> str:
    """
    >>> date_to_ru(dt.date(2019, 3, 11))
    '11 марта 2019 г.'
    >>> date_to_ru(dt.date(2019, 2, 14), Case.Prepositional, without_day=True)
    'феврале 2019 г.'
    """
    ru_date = RuDate(date_, case)
    if without_day:
        return ru_date.month_with_year

    return str(ru_date)


@dataclass()
class RuDate:
    """
    >>> ru_date = RuDate(dt.datetime(2019, 1, 22))
    >>> str(ru_date)
    '22 январь 2019 г.'
    >>> ru_date.month
    'январь'
    >>> ru_date.year
    '2019 г.'
    >>> ru_date.month_with_year
    'январь 2019 г.'
    >>> ru_date = RuDate(dt.datetime(2019, 1, 22), Case.Genitive)
    >>> str(ru_date)
    '22 января 2019 г.'
    """

    date_: Union[dt.date, dt.datetime]
    case: Case = Case.Nominative

    def __str__(self) -> str:
        return f"{self.date_.day} {self.month} {self.year}"

    @property
    def month(self) -> str:
        return MONTHS[self.case][self.date_.month]

    @property
    def year(self) -> str:
        return f"{self.date_.year} г."

    @property
    def month_with_year(self) -> str:
        """
        >>> ru_date = RuDate(dt.datetime(2019, 1, 22))
        >>> ru_date.month_with_year
        'январь 2019 г.'
        """
        return f"{self.month} {self.year}"
