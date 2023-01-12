# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import datetime
import io
from enum import Enum
from typing import TypeVar, Any, Set, Dict

from aiohttp import ClientResponse

from agconnect.common_server.src.agc_client import AGCClient
from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.query.cloud_db_zone_config import CloudDBZoneConfig
from agconnect.database_server.src.query.cloud_db_zone_object_operator import CloudDBZoneObjectOperator
from agconnect.database_server.src.query.cloud_db_zone_object_operator_constraint import \
    CloudDBZoneObjectOperatorConstraint
from agconnect.database_server.src.query import cloud_db_zone_query
from agconnect.database_server.src.query.cloud_db_zone_snapshot import CloudDBZoneSnapshot
from agconnect.database_server.src.services.cloud_db_service import CloudDBService
from agconnect.database_server.src.services.transaction import TransactionFunction, Transaction, OperationType
from agconnect.database_server.src.utils.aggregare_type import AggregateType
from agconnect.database_server.src.utils.condition_type import ConditionType
from agconnect.database_server.src.utils.condition_validate import ConditionValidate
from agconnect.database_server.src.utils.data_model_helper import DataModelHelper
from agconnect.database_server.src.utils.field_type import FieldType
from agconnect.database_server.src.utils.utils import Utils

MAX_OBJECT_LIST_NUM = 1000
MAX_OBJECTS_CAPACITY = 20 * 1024 * 1024
MAX_FAILED_COUNT = 5

RequestOperationTypeMap = {
    'UPSERT': {"operationType": 0, "resKey": 'upsertNumber'},
    'INSERT': {"operationType": 1, "resKey": 'insertNumber'},
    'DELETE': {"operationType": 2, "resKey": 'delNumber'},
    'RECYCLEBIN_DELETE': {"operationType": 3, "resKey": 'delNumber'},
    'RECOVERY': {"operationType": 4, "resKey": 'recoveryNumber'},
}


class RequestOperationType(Enum):
    UPSERT = 'UPSERT',
    INSERT = 'INSERT',
    DELETE = 'DELETE',
    RECYCLEBIN_DELETE = 'RECYCLEBIN_DELETE',
    RECOVERY = 'RECOVERY',
    QUERY_DELETED_DATA_RETENTION_PERIOD = 'QUERY_DELETED_DATA_RETENTION_PERIOD',
    DELETED_DATA_RETENTION_PERIOD = 'DELETED_DATA_RETENTION_PERIOD'


class AggregateResponseKey(str, Enum):
    AVG = 'average',
    SUM = 'sum',
    MAX = 'maximum',
    MIN = 'minimum',
    COUNT = 'count'


class CloudDBZone(CloudDBService):
    __CLOUD_DB_ZONE_CONFIG: CloudDBZoneConfig
    __QUERIES_URL = 'v4/syncObjects/queries'
    __TRANSACTION_QUERIES_URL = "v4/syncObjects/queries"
    __DATA_URL = 'v3/syncObjects'
    __ALL_DATA_URL = 'v3/syncAllObjects'
    __TRANSACTION_URL = 'v3/transaction'
    __KEY_ORDER_BY_FIELD_NAME = "orderByFieldName"
    __KEY_ORDER_BY_FIELD_DIRECTION = "orderByDirection"
    __UPDATE_URL = "v4/object"
    __RECOVERY_URL = "v1/objectsRecovery"

    T = TypeVar('T')

    def __init__(self, agc_client: AGCClient, cloud_db_zone_config: CloudDBZoneConfig):
        super().__init__(agc_client)
        if not cloud_db_zone_config or not cloud_db_zone_config.get_cloud_db_zone_name():
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.VALUE_IS_NULL))
        self.__cloud_db_zone_config = cloud_db_zone_config

    def get_cloud_db_zone_config(self) -> CloudDBZoneConfig:
        return self.__cloud_db_zone_config

    async def execute_transaction_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery,
                                        is_query_delete: bool):
        clazz = cloud_db_zone_query_obj.get_clazz()
        my_obj = clazz()
        self.__verify_pagination_query(cloud_db_zone_query_obj, my_obj)

        request_url = self._URL_PREFIX + CloudDBZone.__TRANSACTION_QUERIES_URL
        data = {
            "objectTypeName": my_obj.get_class_name(),
            "cloudDBZoneName": self.get_cloud_db_zone_config().get_cloud_db_zone_name(),
            "isQueryDelete": is_query_delete,
            "queryConditions": Utils.serialize_query_conditions(cloud_db_zone_query_obj.get_query_conditions(),
                                                                my_obj.get_field_type_map())
        }

        request_id = Utils.get_request_id()
        resp = await self._request_sender.send_post_request(request_url, request_id, data)
        try:
            await CloudDBZone._check_response_body(resp)
            resp_json = await resp.json()
            if resp_json.get('data'):
                return resp_json.get('data')
            elif resp_json.get('errorCodeV2'):
                raise AGConnectCloudDBException(error_code=resp_json.get('errorCodeV2'),
                                                error_message=resp_json.get('info'))

        except Exception:
            return await self.__resend_transaction_query(request_url, request_id, data)

    async def __resend_transaction_query(self, request_url, request_id, data):
        resp = await self._request_sender.send_post_request(request_url, request_id, data)
        try:
            await self._check_response_body(resp)
            resp_json = await resp.json()
            if resp_json.get('data'):
                return resp_json.get('data')
            elif resp_json.get('errorCodeV2'):
                if resp_json.get('errorCodeV2') == 2001018:
                    raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE,
                                                    error_message=ErrorCodeMap.get(
                                                        CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE))
        except AGConnectCloudDBException as err:
            logger.warning(f"Query catch error, request_id: {request_id}")
            raise err

    async def execute_upsert(self, object_list):
        return await self.__handle_increment_data(object_list, RequestOperationType.UPSERT)

    async def execute_insert(self, object_list):
        return await self.__handle_increment_data(object_list, RequestOperationType.INSERT)

    async def execute_recovery(self, object_list):
        return await self.__handle_increment_data(object_list, RequestOperationType.RECOVERY)

    async def execute_update(self, operator: CloudDBZoneObjectOperator,
                             constraint: CloudDBZoneObjectOperatorConstraint = None):
        if len(operator.get_update_map()) == 0 and len(operator.get_increment_map()) == 0:
            logger.warning("The updated and incremental field size is 0, no need to update.")
            return 0

        request_url = self._URL_PREFIX + CloudDBZone.__UPDATE_URL
        self.__check_operator(operator)
        self.__check_constraint(operator.get_object(), constraint)

        request_id = Utils.get_request_id()
        data = self.__get_update_data(operator, constraint)
        resp = await self._request_sender.send_put_request(request_url, request_id, data)
        try:
            data = await resp.json()
            await CloudDBZone._check_response_body(resp)
            return data.get('affectNum')
        except AGConnectCloudDBException:
            return await self.__resend_update_request(request_url, request_id, data)

    async def execute_delete(self, object_list) -> int:
        return await self.__execute_delete_internal(object_list, False)

    async def execute_recycle_bin_delete(self, object_list) -> int:
        return await self.__execute_delete_internal(object_list, True)

    async def execute_delete_all(self, clazz):
        if not clazz:
            logger.warning("The class is none")
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
        Utils.clazz_check(clazz)
        my_obj = clazz()
        request_url = CloudDBZone._URL_PREFIX + CloudDBZone.__ALL_DATA_URL
        data = {
            "objectTypeName": my_obj.get_class_name(),
            "cloudDBZoneName": self.get_cloud_db_zone_config().get_cloud_db_zone_name()
        }
        return await self._object_delete_response(request_url, data)

    async def execute_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery) -> CloudDBZoneSnapshot:
        return await self.__execute_query_internal(cloud_db_zone_query_obj, False)

    async def execute_recycle_bin_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery,
                                        begin: datetime.datetime = None,
                                        end: datetime.datetime = None) -> CloudDBZoneSnapshot:
        if not begin and not end:
            return await self.__execute_query_internal(cloud_db_zone_query_obj, True)
        if not begin or not end or begin > end:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.INPUT_PARAMETER_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INPUT_PARAMETER_INVALID,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.INPUT_PARAMETER_INVALID))
        return await self.__execute_query_internal(cloud_db_zone_query_obj, True, begin, end)

    async def execute_average_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery,
                                    field_name: str) -> int:
        data = self.__form_aggregate_query_data(cloud_db_zone_query_obj, field_name, str(AggregateType.AVG.value))
        response_key = f"{AggregateResponseKey.AVG}({field_name})"
        return await self.__aggregate_query_response(data, response_key)

    async def execute_sum_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery, field_name: str):
        data = self.__form_aggregate_query_data(cloud_db_zone_query_obj, field_name, str(AggregateType.SUM.value))
        response_key = f"{AggregateResponseKey.SUM}({field_name})"
        return await self.__aggregate_query_response(data, response_key)

    async def execute_maximum_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery,
                                    field_name: str) -> int:
        data = self.__form_aggregate_query_data(cloud_db_zone_query_obj, field_name, str(AggregateType.MAX.value))
        response_key = f"{AggregateResponseKey.MAX}({field_name})"
        return await self.__aggregate_query_response(data, response_key)

    async def execute_minimal_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery,
                                    field_name: str) -> int:
        data = self.__form_aggregate_query_data(cloud_db_zone_query_obj, field_name, str(AggregateType.MIN.value))
        response_key = f"{AggregateResponseKey.MIN}({field_name})"
        return await self.__aggregate_query_response(data, response_key)

    async def execute_count_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery, field_name: str):
        data = self.__form_aggregate_query_data(cloud_db_zone_query_obj, field_name, str(AggregateType.COUNT.value))
        response_key = f"{AggregateResponseKey.COUNT}({field_name})"
        return await self.__aggregate_query_response(data, response_key)

    async def run_transaction(self, transaction_function: TransactionFunction) -> bool:
        if not transaction_function:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
        return await self.__get_cloud_db_zone_result(transaction_function)

    async def __get_cloud_db_zone_result(self, func: TransactionFunction):
        transaction = Transaction(self)
        is_transaction_result = False
        count = 0
        while not is_transaction_result and count < MAX_FAILED_COUNT:
            try:
                if isinstance(func, Transaction):
                    logger.warning(ErrorCodeMap.get(CloudDBErrorCode.CLASS_INVALID))
                    raise AGConnectCloudDBException(error_code=CloudDBErrorCode.CLASS_INVALID,
                                                    error_message=ErrorCodeMap.get(CloudDBErrorCode.CLASS_INVALID))
                is_transaction_result = await func.apply(transaction)
                if not is_transaction_result or is_transaction_result is None:
                    logger.warning("user function return false, transaction failed.")
                    return False
                transaction.sort_verify_object_list()
                CloudDBZone.__verify_transaction(transaction)
                transaction_result = await self.__get_transaction_result(transaction)
                is_transaction_result = CloudDBZone.resp_check_transaction_result(transaction_result)
                if is_transaction_result is False:
                    break
                count += 1
            finally:
                transaction.release()

        return is_transaction_result

    @staticmethod
    def __verify_transaction(transaction: Transaction):
        upload_size = 0
        for operation in transaction.transaction_list:
            if operation.get("operation_Type") == OperationType.UPSERT or operation.get(
                    "operation_Type") == OperationType.DELETE:
                upload_size = upload_size + len(operation.objects)
                if upload_size > MAX_OBJECT_LIST_NUM:
                    logger.warning(ErrorCodeMap.get(CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))
                    raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW,
                                                    error_message=ErrorCodeMap.get(
                                                        CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))
        if len(transaction.need_verify_objects_list) > MAX_OBJECT_LIST_NUM:
            logger.warning("Too many query results in the transaction.")
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))

    async def __get_transaction_result(self, transaction: Transaction):
        if transaction.is_transaction_empty():
            logger.warning("nothing need to execute in this transaction, transaction succeed.")
            return 'transaction empty'

        request_url = self._URL_PREFIX + self.__TRANSACTION_URL
        data = {
            "cloudDBZoneName": self.get_cloud_db_zone_config().get_cloud_db_zone_name(),
            "needVerifyObjectsList": transaction.need_verify_objects_list,
            "transactionList": transaction.transaction_list
        }

        if len(data) > MAX_OBJECTS_CAPACITY:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))

        request_id = Utils.get_request_id()

        def convert_bytesio_to_str(source):
            if isinstance(source, list):
                for i, item in enumerate(source):
                    source[i] = convert_bytesio_to_str(item)
            elif isinstance(source, dict):
                for key, value in source.items():
                    source[key] = convert_bytesio_to_str(value)
            elif isinstance(source, io.BytesIO):
                source = source.getvalue().decode('utf-8')
            return source

        data = convert_bytesio_to_str(data)
        try:
            resp = await self._request_sender.send_post_request(request_url, request_id, data)
            if resp.status == 200:
                return resp.status
            if resp.status == 413 and resp.reason == 'Request Entity Too Large':
                return resp.status
        except AGConnectCloudDBException:
            await self.__resend_get_transaction_result(request_url, request_id, data)

    async def __resend_get_transaction_result(self, request_url, request_id, data):
        try:
            resp = await self._request_sender.send_post_request(request_url, request_id, data, True)
            if resp.status == 200:
                return True
        except Exception as err:
            logger.warning(f"Transaction catch error, requestId: {request_id}")
            if self._is_err_response_not_valid(err):
                return
            return False

    @staticmethod
    def resp_check_transaction_result(transaction_result):
        is_transaction_result = None
        if transaction_result == 'transaction empty' or transaction_result == 200:
            is_transaction_result = True
        elif transaction_result == 413:
            is_transaction_result = False
        elif transaction_result is None:
            is_transaction_result = None
        return is_transaction_result

    def __verify_pagination_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery,
                                  my_obj: Any) -> None:
        if not self.__is_pagination_query(cloud_db_zone_query_obj.get_query_conditions()):
            return

        all_order_bys = self.__get_all_order_bys(cloud_db_zone_query_obj.get_query_conditions())
        order_by_field_nameset = all_order_bys.get(self.__KEY_ORDER_BY_FIELD_NAME)
        order_by_direction_array = all_order_bys.get(self.__KEY_ORDER_BY_FIELD_DIRECTION)

        if ConditionType.ASCEND.value in order_by_direction_array and ConditionType.DESCEND.value \
                in order_by_direction_array:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ORDER_BY_ONLY_SUPPORT_ONE_DIRECTION))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ORDER_BY_ONLY_SUPPORT_ONE_DIRECTION,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ORDER_BY_ONLY_SUPPORT_ONE_DIRECTION))

        if len(order_by_field_nameset) != len(order_by_direction_array):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATION_ORDER_BY_HAS_DUPLICATE_FIELD))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PAGINATION_ORDER_BY_HAS_DUPLICATE_FIELD,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.PAGINATION_ORDER_BY_HAS_DUPLICATE_FIELD))

        has_sorted = False
        for query_condition in cloud_db_zone_query_obj.get_query_conditions():
            condition_type = query_condition.get("conditionType")
            if Utils.is_aggregate_type(condition_type):
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATE_NOT_SUPPORT_AGGREGATE))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PAGINATE_NOT_SUPPORT_AGGREGATE,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.PAGINATE_NOT_SUPPORT_AGGREGATE))

            order_by_not_equal_to_condition_type = ConditionType.ORDER_BY != condition_type
            equal_to = ConditionType.EQUAL_TO != condition_type
            last_condition = ConditionType.LIMIT != condition_type and not Utils.is_pagination_type(condition_type)
            if order_by_not_equal_to_condition_type and equal_to and last_condition:
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_ONLY_SUPPORTED))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_ONLY_SUPPORTED,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_ONLY_SUPPORTED))

            if ConditionType.EQUAL_TO == condition_type:
                if has_sorted:
                    logger.warning(ErrorCodeMap.get(CloudDBErrorCode.EQUAL_TO_NOT_BEFORE_ORDER_BY))
                    raise AGConnectCloudDBException(error_code=CloudDBErrorCode.EQUAL_TO_NOT_BEFORE_ORDER_BY,
                                                    error_message=ErrorCodeMap.get(
                                                        CloudDBErrorCode.EQUAL_TO_NOT_BEFORE_ORDER_BY))
                self.__check_pagination_equal_to(query_condition, my_obj, order_by_field_nameset)

            if ConditionType.ORDER_BY == condition_type:
                has_sorted = True
                CloudDBZone.__check_pagination_order_by(query_condition, my_obj)

    @staticmethod
    def __check_pagination_equal_to(query_condition: Any, my_obj: Any,
                                    order_by_field_nameset: Set[str]):
        field_name = query_condition.get("fieldName")
        field_type_map = my_obj.get_field_type_map()

        if field_name in my_obj.get_primary_key_list():
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATE_EQUAL_TO_NOT_SUPPORT_PRIMARY_KEY))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PAGINATE_EQUAL_TO_NOT_SUPPORT_PRIMARY_KEY,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.PAGINATE_EQUAL_TO_NOT_SUPPORT_PRIMARY_KEY))

        if field_name in order_by_field_nameset:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATE_EQUAL_TO_FIELD_IS_SAME_WITH_ORDER_BY))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PAGINATE_EQUAL_TO_FIELD_IS_SAME_WITH_ORDER_BY,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.PAGINATE_EQUAL_TO_FIELD_IS_SAME_WITH_ORDER_BY))

        if field_type_map.get(field_name) == FieldType.Text:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATE_EQUAL_TO_NOT_SUPPORT_TEXT))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PAGINATE_EQUAL_TO_NOT_SUPPORT_TEXT,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.PAGINATE_EQUAL_TO_NOT_SUPPORT_TEXT))

    @staticmethod
    def __check_pagination_order_by(query_condition: Any, my_obj: Any):
        field_name = query_condition.get("fieldName")
        field_type_map = my_obj.get_field_type_map()
        field_type = field_type_map.get(field_name)
        if field_type == FieldType.ByteArray or field_type == FieldType.Text or field_type == FieldType.Boolean:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATE_ORDER_BY_NOT_SUPPORT_TYPE))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PAGINATE_ORDER_BY_NOT_SUPPORT_TYPE,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.PAGINATE_ORDER_BY_NOT_SUPPORT_TYPE))

    async def __handle_increment_data(self, object_list, op_type: RequestOperationType):
        try:
            objects = self.__object_list_transform(object_list)
            if len(objects) == 0:
                logger.warning(f"ObjectList is empty when execute {op_type}.")
                return 0

            data = self.__form_data(objects, op_type)
        except Exception as e:
            raise e

        suffix_url = self.__RECOVERY_URL if op_type == RequestOperationType.RECOVERY else self.__DATA_URL
        request_url = self._URL_PREFIX + suffix_url
        request_id = Utils.get_request_id()
        try:
            resp = await self._request_sender.send_post_request(request_url, request_id, data)
            await self._check_response_body(resp)
            data = await resp.json()
            return data.get(RequestOperationTypeMap.get(op_type.name).get("resKey"))
        except AGConnectCloudDBException:
            return await self.__resend_upsert_request(request_url, request_id, data, op_type)

    async def __resend_update_request(self, request_url, request_id, data):
        try:
            resp = await self._request_sender.send_put_request(request_url, request_id, data)
            await self._check_response_body(resp)
            return resp.get("data").get("affectNum")
        except Exception as err:
            logger.warning(f"Update catch error, request_id: {request_id}")
            if self._is_err_response_not_valid:
                return None
            raise AGConnectCloudDBException(str(err)) from err

    async def __resend_upsert_request(self, request_url, request_id, data, operation_type):
        try:
            resp = await self._request_sender.send_put_request(request_url, request_id, data)
            await self._check_response_body(resp)
            return resp.get("data").get(RequestOperationTypeMap.get(operation_type).get("resKey"))
        except Exception as err:
            logger.warning(f"{operation_type} catch error, request_id: {request_id}")
            if self._is_err_response_not_valid:
                return None
            raise AGConnectCloudDBException(str(err)) from err

    def __get_update_data(self, operator: CloudDBZoneObjectOperator,
                          constraint: CloudDBZoneObjectOperatorConstraint = None):
        data = {
            "cloudDBZoneName": self.get_cloud_db_zone_config().get_cloud_db_zone_name(),
            "objectTypeName": (operator.get_object().get_class_name()),
            "primaryKey": CloudDBZone.__get_primary_keys(operator.get_object())
        }

        if operator.get_increment_map() and len(operator.get_increment_map()) != 0:
            data["increment"] = Utils.serialize_map_object(operator.get_object(), operator.get_increment_map())

        if operator.get_update_map() and len(operator.get_update_map()) != 0:
            data["update"] = Utils.serialize_map_object(operator.get_object(), operator.get_update_map())

        if constraint:
            data["conditions"] = Utils.serialize_query_conditions(constraint.get_conditions(),
                                                                  operator.get_object().get_field_type_map())
        return data

    def __execute_delete_internal(self, object_list: [T], is_delete_dis_used: bool = None):
        try:
            objects = self.__object_list_transform(object_list)
            if len(objects) == 0:
                logger.warning("ObjectList is empty when execute Delete.")
                return 0
            op_type = RequestOperationType.RECYCLEBIN_DELETE if is_delete_dis_used else RequestOperationType.DELETE
            data = self.__form_data(objects, op_type, is_delete_dis_used)
        except AGConnectCloudDBException as err:
            raise err

        request_url = self._URL_PREFIX + self.__DATA_URL
        return self._object_delete_response(request_url, data)

    def __form_data(self, objects: [Any], operation_type: RequestOperationType = None,
                    is_delete_dis_used: bool = False):
        data = {
            "cloudDBZoneName": self.get_cloud_db_zone_config().get_cloud_db_zone_name(),
            "objectTypeName": objects[0].__class__.__name__,
            "objects": Utils.serialize_objects(objects)
        }

        if operation_type == RequestOperationType.UPSERT.value or operation_type == RequestOperationType.INSERT.value:
            data[operation_type] = RequestOperationTypeMap.get(str(operation_type))
        elif operation_type == RequestOperationType.RECYCLEBIN_DELETE:
            data['isDeleteDisused'] = is_delete_dis_used

        if len(data) > MAX_OBJECTS_CAPACITY:
            logger.warning("upsert data size is more than 20MB")
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))
        return data

    @staticmethod
    def __check_operator(operator: CloudDBZoneObjectOperator) -> None:
        obj = operator.get_object()
        DataModelHelper.check_primary_keys(obj)
        increment_map = operator.get_increment_map()
        update_map = operator.get_update_map()
        field_name_set = set()

        for field_name, value in increment_map.items():
            field_name_set.add(field_name)
            DataModelHelper.check_operator_field(field_name, value, obj, True)

        for field_name, value in update_map.items():
            field_name_set.add(field_name)
            DataModelHelper.check_operator_field(field_name, value, obj)

        if len(field_name_set) < len(increment_map) + len(update_map):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.DUPLICATE_FIELD))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DUPLICATE_FIELD,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DUPLICATE_FIELD))

    def __form_aggregate_query_data(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery,
                                    field_name: str,
                                    aggregate_type: str):
        if not cloud_db_zone_query_obj:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.AGGREGATE_QUERY_CLOUDDB_ZONE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.AGGREGATE_QUERY_CLOUDDB_ZONE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.AGGREGATE_QUERY_CLOUDDB_ZONE_IS_NULL))
        clazz = cloud_db_zone_query_obj.get_clazz()
        my_obj = clazz()
        CloudDBZone.__check_aggregate_query_input(my_obj, field_name, aggregate_type)

        query_conditions = cloud_db_zone_query_obj.get_query_conditions()
        query_conditions.append({
            "fieldName": field_name,
            "conditionType": aggregate_type
        })

        return {
            "objectTypeName": my_obj.get_class_name(),
            "cloudDBZoneName": self.get_cloud_db_zone_config().get_cloud_db_zone_name(),
            "queryConditions": Utils.serialize_query_conditions(query_conditions, my_obj.get_field_type_map())
        }

    @staticmethod
    def __check_aggregate_query_input(my_obj: Any, field_name: str, aggregate_type: str):
        if not field_name:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.AGGREGATE_QUERY_FIELD_NAME_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.AGGREGATE_QUERY_FIELD_NAME_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.AGGREGATE_QUERY_FIELD_NAME_IS_NULL))

        field_type_map = my_obj.get_field_type_map()
        if field_name not in field_type_map:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.AGGREGATE_QUERY_ENTITY_DO_NOT_HAVE_FIELD))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.AGGREGATE_QUERY_ENTITY_DO_NOT_HAVE_FIELD,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.AGGREGATE_QUERY_ENTITY_DO_NOT_HAVE_FIELD))

        if field_name in my_obj.get_encrypted_field_list() and aggregate_type != AggregateType.COUNT.value:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY))
        field_type = field_type_map.get(field_name)
        if aggregate_type != AggregateType.COUNT and not Utils.is_numeric_field(field_type):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.AGGREGATE_QUERY_FIELD_TYPE_IS_NOT_NUMERIC))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.AGGREGATE_QUERY_FIELD_TYPE_IS_NOT_NUMERIC,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.AGGREGATE_QUERY_FIELD_TYPE_IS_NOT_NUMERIC))

    async def __aggregate_query_response(self, data: Any, response_key: str):
        request_url = self._URL_PREFIX + self.__QUERIES_URL
        request_id = Utils.get_request_id()
        resp = await self._request_sender.send_post_request(request_url, request_id, data)
        try:
            data = await resp.json()
            CloudDBZone.__aggregate_response_check(resp, data)
            return data["data"][0][response_key]
        except AGConnectCloudDBException:
            return await self.__resend_aggregate_query(request_url, request_id, data, response_key)

    @staticmethod
    def __is_pagination_query(query_conditions: Any) -> bool:
        is_pagination_query = False
        for query_condition in query_conditions:
            if Utils.is_pagination_type(query_condition.get("conditionType")):
                if is_pagination_query:
                    logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_MORE_THAN_ONE))
                    raise AGConnectCloudDBException(
                        error_code=CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_MORE_THAN_ONE,
                        error_message=ErrorCodeMap.get(
                            CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_MORE_THAN_ONE))
                is_pagination_query = True
        return is_pagination_query

    def __get_all_order_bys(self, query_conditions: Any):
        all_order_bys = {self.__KEY_ORDER_BY_FIELD_NAME: [], self.__KEY_ORDER_BY_FIELD_DIRECTION: []}
        for query_condition in query_conditions:
            if query_condition.get('conditionType') == ConditionType.ORDER_BY.value:
                order_by_list = all_order_bys.get(self.__KEY_ORDER_BY_FIELD_NAME)
                order_by_list.append(query_condition.get('fieldName'))
                order_by_array = all_order_bys.get(self.__KEY_ORDER_BY_FIELD_DIRECTION)
                order_by_array.append(query_condition.get('value'))
        return all_order_bys

    @staticmethod
    def __get_primary_keys(obj: Any):
        primary_keys = {}
        primary_key_list = obj.get_primary_key_list()
        for key in primary_key_list:
            primary_keys[key] = obj.__dict__.get(key)
        return primary_keys

    @staticmethod
    def __object_list_transform(object_list) -> [T]:
        if not object_list:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(
                error_code=CloudDBErrorCode.VALUE_IS_NULL,
                error_message=ErrorCodeMap.get(
                    CloudDBErrorCode.VALUE_IS_NULL))
        if Utils.is_array(object_list):
            objects = object_list
        else:
            objects = [object_list]

        for obj in objects:
            if obj is None:
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
                raise AGConnectCloudDBException(
                    error_code=CloudDBErrorCode.VALUE_IS_NULL,
                    error_message=ErrorCodeMap.get(
                        CloudDBErrorCode.VALUE_IS_NULL))

        CloudDBZone.__check_input_data(objects)
        return objects

    @staticmethod
    def __check_input_data(objects):
        if len(objects) > MAX_OBJECT_LIST_NUM:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))
            raise AGConnectCloudDBException(
                error_code=CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW,
                error_message=ErrorCodeMap.get(
                    CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))
        Utils.check_schema_data_size(objects)

    @staticmethod
    def __response_check(response: ClientResponse, response_json: Dict[str, str] = None) -> None:
        if not response or not response.status:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.RESPONSE_IS_INVALID))
            raise AGConnectCloudDBException(
                error_code=CloudDBErrorCode.RESPONSE_IS_INVALID,
                error_message=ErrorCodeMap.get(
                    CloudDBErrorCode.RESPONSE_IS_INVALID))
        if response.status == 200:
            if not response_json.get("data"):
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.RESPONSE_IS_INVALID))
                raise AGConnectCloudDBException(
                    error_code=CloudDBErrorCode.RESPONSE_IS_INVALID,
                    error_message=ErrorCodeMap.get(
                        CloudDBErrorCode.RESPONSE_IS_INVALID))

    @staticmethod
    def __aggregate_response_check(response: Any, response_json: Any):
        CloudDBZone.__response_check(response, response_json)
        if "errorCodeV2" not in response_json:
            if not response_json["data"][0]:
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.RESPONSE_IS_INVALID))
                raise AGConnectCloudDBException(
                    error_code=CloudDBErrorCode.RESPONSE_IS_INVALID,
                    error_message=ErrorCodeMap.get(
                        CloudDBErrorCode.RESPONSE_IS_INVALID))
        elif response.status == 200:
            if not response_json.get("data"):
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.RESPONSE_IS_INVALID))
                raise AGConnectCloudDBException(
                    error_code=CloudDBErrorCode.RESPONSE_IS_INVALID,
                    error_message=ErrorCodeMap.get(
                        CloudDBErrorCode.RESPONSE_IS_INVALID))
        else:
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.OBJECT_TYPE_DOES_NOT_EXIST,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.OBJECT_TYPE_DOES_NOT_EXIST))

    async def __resend_aggregate_query(self, request_url, request_id, data, response_key):
        try:
            resp = await self._request_sender.send_post_request(request_url, request_id, data, True)
            response_json = await resp.json()
            CloudDBZone.__aggregate_response_check(resp, response_json)
            return resp.get('data').get('data').get(0).get(response_key)
        except AGConnectCloudDBException as err:
            log_string = "Query catch error, requestId: {}".format(request_id)
            logger.warning(log_string)
            if self._is_err_response_not_valid(err):
                return
            raise err

    @staticmethod
    def __check_constraint(obj: Any, constraint: CloudDBZoneObjectOperatorConstraint = None):
        if not constraint:
            return
        if not isinstance(obj, constraint.get_clazz()):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.OPERATOR_MISMATCH_CONSTRAINT))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.OPERATOR_MISMATCH_CONSTRAINT,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.OPERATOR_MISMATCH_CONSTRAINT))

        ConditionValidate.check_condition_len(constraint.get_conditions())
        validate = ConditionValidate(constraint.get_clazz())
        for condition in constraint.get_conditions():
            validate.check_condition(condition)

    @staticmethod
    def __get_index_by_query_condition(query_conditions: Any, primary_key_list: Any) -> [Any]:
        index_list: [str] = []
        for query_condition in query_conditions:
            condition_type = query_condition.get("condition_type")
            if condition_type != ConditionType.ORDER_BY and condition_type != ConditionType.EQUAL_TO:
                return None
            field_name = query_condition.get("fieldName")
            if field_name:
                index_list.append(field_name)
        for primary_key in primary_key_list:
            if primary_key not in index_list:
                index_list.append(primary_key)

        return index_list

    async def __execute_query_internal(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery,
                                       is_query_delete: bool,
                                       begin: datetime.datetime = None, end: datetime.datetime = None):
        if not cloud_db_zone_query_obj:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_CONDITION_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_CONDITION_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.QUERY_CONDITION_IS_NULL))

        clazz = cloud_db_zone_query_obj.get_clazz()
        my_obj = clazz()
        self.__verify_pagination_query(cloud_db_zone_query_obj, my_obj)
        request_url = self._URL_PREFIX + self.__QUERIES_URL
        field_type_map = my_obj.get_field_type_map()
        data = {
            "objectTypeName": my_obj.get_class_name(),
            "cloudDBZoneName": self.get_cloud_db_zone_config().get_cloud_db_zone_name(),
            "isQueryDelete": is_query_delete,
            "queryConditions": Utils.serialize_query_conditions(cloud_db_zone_query_obj.get_query_conditions(),
                                                                field_type_map, begin, end)
        }

        request_id = Utils.get_request_id()
        response_json = None
        try:
            resp = await self._request_sender.send_post_request(request_url, request_id, data)
            response_json = await resp.json()
            CloudDBZone.__response_check(resp, response_json)
            deserialized_objects = Utils.deserialize_objects(response_json.get('data'), field_type_map,
                                                             cloud_db_zone_query_obj.get_clazz())
            snap_short = CloudDBZoneSnapshot(deserialized_objects)
            return snap_short
        except Exception as err:
            log_string = "Query catch error, requestId: {}".format(request_id)
            logger.warning(log_string)
            try:
                if self._is_err_response_not_valid(err, response_json):
                    return
            except AGConnectCloudDBException as error_code_v2:
                if CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_FAILED_FOR_NO_INDEX == error_code_v2:
                    raise AGConnectCloudDBException(
                        error_code=CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_FAILED_FOR_NO_INDEX,
                        error_message="No such index for pagination query: [" + str(
                            self.__get_index_by_query_condition(cloud_db_zone_query_obj.get_query_conditions(),
                                                                my_obj.get_primary_key_list())) + "]") from err
                raise err from err
