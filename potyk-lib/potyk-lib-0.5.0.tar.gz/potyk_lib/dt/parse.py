from typing import cast, List, Tuple

from dateutil import parser

__all__ = ['parse_ru_date']


class RuParserInfo(parser.parserinfo):
    MONTHS = cast(
        List[Tuple[str, ...]],
        [(u"янв.", u"Январь", u'января'),
         (u"февр.", u"Февраль"),
         (u"март", u"Март"),
         (u"апр.", u"Апрель"),
         (u"май", u"Май"),
         (u"июнь", u"Июнь"),
         (u"июль", u"Июль"),
         (u"авг.", u"Август"),
         (u"сент.", u"Сентябрь",),
         (u"окт.", u"Октябрь"),
         (u"нояб.", u"Ноябрь"),
         (u"дек.", u"Декабрь", u'декабря')]
    )


def parse_ru_date(date_str):
    """
    https://stackoverflow.com/a/37485484/5500609

    >>> parse_ru_date(u'30 декабря 2021')
    datetime.date(2021, 12, 30)
    >>> parse_ru_date(u'1 января 2022')
    datetime.date(2022, 1, 1)
    """
    return parser.parse(date_str, parserinfo=RuParserInfo()).date()
