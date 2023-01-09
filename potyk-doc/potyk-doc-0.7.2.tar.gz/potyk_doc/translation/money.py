import numbers
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Union, Dict, Tuple, Any, cast, Optional
from potyk_lib.fp import If, pipe
from potyk_lib.num import decimal_round
from potyk_doc.money import Currency
from potyk_doc.translation.number import int_to_ru

CurrencyShorthands = {Currency.Rubles: "руб.", Currency.Tenge: "тг."}

RUBS: Dict[Tuple, str] = {(1,): "рубль", (2, 3, 4): "рубля", (0, 5, 6, 7, 8, 9): "рублей"}
PENNIES: Dict[Tuple, str] = {(1,): "копейка", (2, 3, 4): "копейки", (0, 5, 6, 7, 8, 9): "копеек"}


@dataclass()
class NumberAttrTranslator:
    """
    >>> from unittest.mock import MagicMock
    >>> summary = MagicMock(order_sum=3681.76, bool_=True)
    >>> NumberAttrTranslator(summary).order_sum
    '3 681 (Три тысячи шестьсот восемьдесят один) рубль 76 копеек'
    >>> NumberAttrTranslator(summary, attr_suffix='_str').bool_
    True
    >>> NumberAttrTranslator(summary, attr_suffix='_str').order_sum_str
    '3 681 (Три тысячи шестьсот восемьдесят один) рубль 76 копеек'
    >>> NumberAttrTranslator(summary, attr_suffix='_str').order_sum
    3681.76
    >>> NumberAttrTranslator(summary, attr_suffix='_str').bool_
    True

    """
    translatable: Any
    attr_suffix: Optional[str] = None

    def __getattr__(self, attr: str) -> str:
        is_number = lambda val: isinstance(val, numbers.Number) and not isinstance(val, bool)
        cut_suffix = lambda attr: re.sub(fr'{self.attr_suffix}$', '', attr)
        get_val = lambda attr: getattr(self.translatable, attr)
        translate = lambda val: sum_to_ru(val) if is_number(val) else val

        return (
            If(self.attr_suffix)
            .then(
                lambda: If(attr.endswith(self.attr_suffix))
                .then(lambda: pipe(cut_suffix, get_val, translate)(attr))
                .el(lambda: get_val(attr))
            )
            .el(lambda: pipe(get_val, translate)(attr))
            .get()
        )


def sum_to_ru(
    number: Union[int, float, Decimal],
    with_number: bool = True,
    currency: Currency = Currency.Rubles,
    with_pennies: bool = True,
) -> str:
    """
    >>> sum_to_ru(3681)
    '3 681 (Три тысячи шестьсот восемьдесят один) рубль 00 копеек'
    >>> sum_to_ru(13620)
    '13 620 (Тринадцать тысяч шестьсот двадцать) рублей 00 копеек'
    >>> sum_to_ru(3681, with_number=False)
    'Три тысячи шестьсот восемьдесят один рубль 00 копеек'
    >>> sum_to_ru(3681, with_pennies=False)
    '3 681 (Три тысячи шестьсот восемьдесят один) рубль'
    >>> sum_to_ru(1488, currency=Currency.Tenge)
    '1 488 (Одна тысяча четыреста восемьдесят восемь) тенге 00 тиын'
    >>> sum_to_ru(Decimal('-811.02'))
    '-811 (Минус восемьсот одиннадцать) рублей 02 копейки'
    """
    int_number = int(number)
    number_rest = cast(float, abs(number - int(number)))

    number_str = f"{int_number:,}".replace(",", " ")
    ru_number = int_to_ru(int_number)

    normalized_rest = normalize_pennies(number_rest)

    currency_str, pennies_str = _get_currency_names(currency, int_number, normalized_rest)

    if with_number:
        currency_str = f"{number_str} ({ru_number}) {currency_str}"
    else:
        currency_str = f"{ru_number} {currency_str}"

    if with_pennies:
        pennies_str = f" {normalized_rest} {pennies_str}"
    else:
        pennies_str = ""

    return f"{currency_str}{pennies_str}"


def _get_currency_names(
    currency: Currency, int_number: int, normalized_res: str
) -> Tuple[str, str]:
    if currency == Currency.Rubles:
        currency_str = create_ruble_str(int_number)
        pennies_str = create_pennies_str(normalized_res)
    elif currency == Currency.Tenge:
        currency_str = "тенге"
        pennies_str = "тиын"
    else:
        raise ValueError(f"Invalid currency: {currency}")

    return currency_str, pennies_str


def create_ruble_str(number: int) -> str:
    """
    >>> create_ruble_str(1)
    'рубль'
    >>> create_ruble_str(11)
    'рублей'
    >>> create_ruble_str(108)
    'рублей'
    >>> create_ruble_str(332)
    'рубля'
    >>> create_ruble_str(999)
    'рублей'
    """
    if number % 100 in range(11, 20):
        return "рублей"

    last_digit = number % 10
    return next(
        ruble_str for ruble_digits, ruble_str in RUBS.items() if last_digit in ruble_digits
    )


def normalize_pennies(number_rest: Union[float, Decimal]) -> str:
    """"
    >>> normalize_pennies(0)
    '00'
    >>> normalize_pennies(0.1)
    '10'
    >>> normalize_pennies(0.04)
    '04'
    >>> normalize_pennies(0.01)
    '01'
    >>> normalize_pennies(0.02)
    '02'
    """
    if not number_rest:
        rest_part = "00"
    else:
        rest_part = str(decimal_round(number_rest))[2:]
        if len(rest_part) == 1:
            rest_part += "0"

    return rest_part


def create_pennies_str(normalized_rest: str) -> str:
    """
    >>> create_pennies_str("00")
    'копеек'
    >>> create_pennies_str("10")
    'копеек'
    >>> create_pennies_str("04")
    'копейки'
    >>> create_pennies_str("01")
    'копейка'
    """
    if int(normalized_rest) % 100 in range(11, 20):
        return "копеек"

    return next(v for k, v in PENNIES.items() if int(normalized_rest[-1]) in k)
