# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from __future__ import annotations
from typing import TypeVar, Generic, Any, Type

from agconnect.database_server.src.utils.condition_type import ConditionType
from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.utils.condition_validate import ConditionValidate

T = TypeVar('T')


class CloudDBZoneObjectOperatorConstraint(Generic[T]):
    __clazz: Type[T]
    __conditions: Any = []
    __condition_validate: ConditionValidate

    def __init__(self, clazz: Type[T]):
        self.__clazz = clazz
        self.__conditions = []
        self.__condition_validate = ConditionValidate(clazz)

    @property
    def clazz(self):
        return self.__clazz

    @property
    def conditions(self):
        return self.__conditions

    def get_conditions(self):
        return self.__conditions

    def get_clazz(self):
        return self.__clazz

    @staticmethod
    def where(clazz: Type[T]) -> CloudDBZoneObjectOperatorConstraint:
        if not clazz:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
        return CloudDBZoneObjectOperatorConstraint(clazz)

    def equal_to(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.EQUAL_TO, field_name, value)
        return self

    def not_equal_to(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.NOT_EQUAL_TO, field_name, value)
        return self

    def greater_than(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.GREATER_THAN, field_name, value)
        return self

    def greater_than_equal_to(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.GREATER_THAN_OR_EQUAL_TO, field_name, value)
        return self

    def less_than(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.LESS_THAN, field_name, value)
        return self

    def less_than_or_equal_to(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.LESS_THAN_OR_EQUAL_TO, field_name, value)
        return self

    def inside(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.IN, field_name, value)
        return self

    def is_null(self, field_name: str) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.IS_NULL, field_name)
        return self

    def is_not_null(self, field_name: str) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.IS_NOT_NULL, field_name)
        return self

    def ends_with(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.ENDS_WITH, field_name, value)
        return self

    def begins_with(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.BEGINS_WITH, field_name, value)
        return self

    def contains(self, field_name: str, value: Any) -> CloudDBZoneObjectOperatorConstraint:
        self.add_condition(ConditionType.CONTAINS, field_name, value)
        return self

    def add_condition(self, condition_type: ConditionType, field_name: str, value: Any = None) -> None:
        condition_object: Any = {"fieldName": field_name, "conditionType": condition_type, "value": value}
        self.__condition_validate.check_condition(condition_object)
        self.conditions.append(condition_object)
        ConditionValidate.check_condition_len(self.conditions)
