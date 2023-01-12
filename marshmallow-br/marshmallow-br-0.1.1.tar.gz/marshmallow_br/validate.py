# -*- coding: utf-8 -*-
import re
from itertools import cycle

from marshmallow.validate import *

__all__ = ("CNH", "CNPJ", "CPF", "Certificate", "Phone")


class CNH(Validator):
    """Validate a CNH."""

    CNH_REGEX = re.compile(
        r"^(?:[0-9]{10}(?:\-?)[0-9])$",
        re.IGNORECASE | re.UNICODE,
    )

    default_message = "Not a valid CNH."

    def __init__(self, *, error: str | None = None) -> None:
        self.error = error or self.default_message  # type: str
        self.REGEX = self.CNH_REGEX

    def _format_error(self, value: ...) -> str:
        return self.error.format(input=value)

    def __call__(self, value: ...) -> str:
        message = self._format_error(value)
        if len(set(value)) == 1 or not self.REGEX.match(value):
            raise ValidationError(message)

        numbers = [int(digit) for digit in str(value) if digit.isdigit()]
        if len(numbers) != 11:
            raise ValidationError(message)

        dsc = 0
        expected_digit = sum(numbers[9 - i] * i for i in range(9, 0, -1)) % 11
        if expected_digit >= 10:
            expected_digit = 0
            dsc = 2
        if numbers[9] != expected_digit:
            raise ValidationError(message)

        expected_digit = (sum(numbers[i-1] * i for i in range(1, 10)) % 11) - dsc
        if expected_digit < 0:
            expected_digit += 11
        if expected_digit >= 10:
            expected_digit = 0
        if numbers[10] != expected_digit:
            raise ValidationError(message)

        return value


class CNPJ(Validator):
    """Validate a CNPJ."""

    CNPJ_REGEX = re.compile(
        r"".join(
            (
                r"^",
                r"(?:[0-9]{2})\.?",
                r"(?:[0-9]{3})\.?",
                r"(?:[0-9]{3})\/?",
                r"(?:[0-9]{4})\-?",
                r"(?:[0-9]{2})",
                r"$",
            )
        ),
        re.IGNORECASE | re.UNICODE,
    )

    default_message = "Not a valid CNPJ."

    def __init__(self, *, error: str | None = None) -> None:
        self.error = error or self.default_message  # type: str
        self.REGEX = self.CNPJ_REGEX

    def _format_error(self, value: ...) -> str:
        return self.error.format(input=value)

    def __call__(self, value: ...) -> str:
        message = self._format_error(value)
        if len(set(value)) == 1 or not self.REGEX.match(value):
            raise ValidationError(message)

        numbers = [int(digit) for digit in str(value) if digit.isdigit()][::-1]
        if len(numbers) != 14:
            raise ValidationError(message)

        expected_digit = (sum(a * b for a, b in zip(numbers[2:], cycle(range(2, 10)))) * 10 % 11) % 10
        if numbers[1] != expected_digit:
            raise ValidationError(message)

        expected_digit = (sum(a * b for a, b in zip(numbers[1:], cycle(range(2, 10)))) * 10 % 11) % 10
        if numbers[0] != expected_digit:
            raise ValidationError(message)

        return value


class CPF(Validator):
    """Validate a CPF."""

    CPF_REGEX = re.compile(
        r"".join(
            (
                r"^",
                r"(?:[0-9]{3})\.?",
                r"(?:[0-9]{3})\.?",
                r"(?:[0-9]{3})\-?",
                r"(?:[0-9]{2})",
                r"$",
            )
        ),
        re.IGNORECASE | re.UNICODE,
    )

    default_message = "Not a valid CPF."

    def __init__(self, *, error: str | None = None) -> None:
        self.error = error or self.default_message  # type: str
        self.REGEX = self.CPF_REGEX

    def _format_error(self, value: ...) -> str:
        return self.error.format(input=value)

    def __call__(self, value: ...) -> str:
        message = self._format_error(value)
        if len(set(value)) == 1 or not self.REGEX.match(value):
            raise ValidationError(message)

        numbers = [int(digit) for digit in str(value) if digit.isdigit()]
        if len(numbers) != 11:
            raise ValidationError(message)

        expected_digit = (sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1))) * 10 % 11) % 10
        if numbers[9] != expected_digit:
            raise ValidationError(message)

        expected_digit = (sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1))) * 10 % 11) % 10
        if numbers[10] != expected_digit:
            raise ValidationError(message)

        return value


class Certificate(Validator):
    """Validate a Brazilian birth, marriage and death certificates."""

    CERTIFICATE_REGEX = re.compile(
        r"".join(
            (
                r"^",
                r"(?:[0-9]{6})[\.\s]?",
                r"(?:[0-9]{2})[\.\s]?",
                r"(?:[0-9]{2})[\.\s]?",
                r"(?:[0-9]{4})[\.\s]?",
                r"(?:[1-4])[\.\s]?",  # type
                r"(?:[0-9]{5})[\.\s]?",
                r"(?:[0-9]{3})[\.\s]?",
                r"(?:[0-9]{7})\-?",
                r"(?:[0-9]{2})",
                r"$",
            )
        ),
        re.IGNORECASE | re.UNICODE,
    )

    default_message = "Not a valid certificate."

    def __init__(
        self,
        *,
        type_: int | None = None,
        error: str | None = None,
    ) -> None:
        self.type_ = type_
        self.error = error or self.default_message  # type: str
        self.REGEX = self.CERTIFICATE_REGEX

    def _format_error(self, value: ...) -> str:
        return self.error.format(input=value)

    def _generate_digit(self, value: list[int]) -> int:
        s = 0
        m = 32 - len(value)
        for i in range(len(value)):
            s += int(value[i]) * m
            m += 1
            m = 0 if m > 10 else m
        s = s % 11
        s = 1 if s > 9 else s
        return s

    def __call__(self, value: ...) -> str:
        message = self._format_error(value)
        if len(set(value)) == 1 or not self.REGEX.match(value):
            raise ValidationError(message)

        numbers = [int(digit) for digit in str(value) if digit.isdigit()]
        if len(numbers) != 32:
            raise ValidationError(message)

        expected_digit = self._generate_digit(numbers[:-2])
        if numbers[-2] != expected_digit:
            raise ValidationError(message)

        expected_digit = self._generate_digit(numbers[:-2] + [expected_digit])
        if numbers[-1] != expected_digit:
            raise ValidationError(message)

        return value


class Phone(Validator):
    """Validate a Brazilian phone number."""

    # ref: https://www.gov.br/anatel/pt-br/regulado/numeracao/plano-de-numeracao-brasileiro
    DDI_BR = "55"
    DDD_BR = (
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "22", "24", "27", "28",
        "31", "32", "33", "34", "35", "37", "38", "41", "42", "43", "44", "45", "46", "47",
        "48", "49", "51", "53", "54", "55", "61", "62", "63", "64", "65", "66", "67", "68",
        "69", "71", "73", "74", "75", "77", "79", "81", "82", "83", "84", "85", "86", "87",
        "88", "89", "91", "92", "93", "94", "95", "96", "97", "98", "99",
    )
    PHONE_NUMBER_REGEX = re.compile(
        r"".join(
            (
                r"^",
                r"(?:(?:\+|00)?(?P<ddi>" + DDI_BR + r")\s?)?",  # DDI
                r"(?:(?:\(?(?P<ddd>" + "|".join(DDD_BR) + r")\)?)\s?)?",  # DDD
                r"(?:(?P<number_part_one>(?:9\d|[2-9])\d{3})[-\s]?(?P<number_part_two>\d{4}))",  # number
                r"$",
            )
        ),
        re.IGNORECASE | re.UNICODE,
    )

    default_message = "Not a valid phone number."

    def __init__(
        self,
        *,
        require_ddi: bool | None = None,
        require_ddd: bool | None = None,
        error: str | None = None,
    ) -> None:
        self.require_ddi = require_ddi
        self.require_ddd = require_ddd
        self.error = error or self.default_message  # type: str
        self.REGEX = self.PHONE_NUMBER_REGEX

    def _repr_args(self) -> str:
        return f"require_ddi={self.require_ddi!r} require_ddd={self.require_ddd!r}"

    def _format_error(self, value: str) -> str:
        return self.error.format(input=value)

    def __call__(self, value: str) -> str:
        _match = self.REGEX.match(value)
        message = self._format_error(value)
        if (
            not _match
            or (self.require_ddi and not _match.group(1))
            or (self.require_ddd and not _match.group(2))
        ):
            raise ValidationError(message)
        return value
