from potyk_doc.translation._num2t4ru import num2text


def int_to_ru(number: int) -> str:
    """
    >>> int_to_ru(3681)
    'Три тысячи шестьсот восемьдесят один'
    """
    return num2text(number).capitalize()
