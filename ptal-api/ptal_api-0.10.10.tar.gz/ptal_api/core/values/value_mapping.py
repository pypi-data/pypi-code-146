from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Any, Dict, Type

from sgqlc.types import Input

from ptal_api.schema.api_schema import (
    ValueInput, DateTimeValueInput, DateInput, StringValueInput, IntValueInput,
    DoubleValueInput, LinkValueInput
)


class AbstractValueMapper(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_value_input(value: Any) -> Input:
        pass

    @staticmethod
    @abstractmethod
    def get_tdm_value_format(value: Any) -> Dict:
        pass


class StringValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: str) -> Input:
        string_input = StringValueInput()
        string_input.value = value

        value_input = ValueInput()
        value_input.string_value_input = string_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: str) -> Dict:
        return {'value': value}


class IntValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: int) -> Input:
        int_input = IntValueInput()
        int_input.value = value

        value_input = ValueInput()
        value_input.int_value_input = int_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: int) -> Dict:
        return {'value': value}


class DoubleValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: float) -> Input:
        double_input = DoubleValueInput()
        double_input.value = value

        value_input = ValueInput()
        value_input.double_value_input = double_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: float) -> Dict:
        return {'value': value}


class DateValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: date) -> Input:
        date_obj = DateInput()
        date_obj.day = value.day
        date_obj.month = value.month
        date_obj.year = value.year

        date_input = DateTimeValueInput()
        date_input.date = date_obj

        value_input = ValueInput()
        value_input.date_time_value_input = date_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: date) -> Dict:
        return {
            'date': {
                'day': value.day,
                'month': value.month,
                'year': value.year
            }
        }


class LinkValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: str) -> Input:
        link_input = LinkValueInput()
        link_input.link = value

        value_input = ValueInput()
        value_input.link_value_input = link_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: str) -> Dict:
        return {'link': value}


def get_map_helper(value_type: str) -> Type[AbstractValueMapper]:
    if value_type == 'String':
        return StringValueMapper
    elif value_type == 'Int':
        return IntValueMapper
    elif value_type == 'Double':
        return DoubleValueMapper
    elif value_type == 'Date':
        return DateValueMapper
    elif value_type == 'Link':
        return LinkValueMapper
    else:
        raise NotImplementedError(f'{value_type} type not implemented')
