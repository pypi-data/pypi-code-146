# Copyright (c) Huawei Technologies Co. Ltd. 2022. All rights reserved.

from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode

ErrorCodeMap = dict()


def init():
    ErrorCodeMap[CloudDBErrorCode.VALUE_IS_NULL] = "the value is null."
    ErrorCodeMap[CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW] = "data size is overflow."
    ErrorCodeMap[CloudDBErrorCode.QUERY_CONDITION_IS_NULL] = "cloudDBZoneQuery must not be null."
    ErrorCodeMap[CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_IS_NULL] = "field name must not be null."
    ErrorCodeMap[CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_DO_NOT_EXIST] = "the field name does not exist."
    ErrorCodeMap[CloudDBErrorCode.INPUT_LIMIT_OR_OFFSET_LESS_THAN_ZERO] = "input Limit and Offset can not less than 0."
    ErrorCodeMap[CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL] = "values must not be null."
    ErrorCodeMap[CloudDBErrorCode.GET_ACCESS_TOKEN_FAIL] = "get accessToken fail."
    ErrorCodeMap[CloudDBErrorCode.NETTY_COMMUNICATION_ERROR] = "netty communication error."
    ErrorCodeMap[CloudDBErrorCode.AGGREGATE_QUERY_CLOUDDB_ZONE_IS_NULL] = \
        "aggregateQuery input, cloudDBZoneQuery must not be null."
    ErrorCodeMap[CloudDBErrorCode.AGGREGATE_QUERY_FIELD_NAME_IS_NULL] = \
        "aggregateQuery input, field name must not be null."
    ErrorCodeMap[CloudDBErrorCode.AGGREGATE_QUERY_FIELD_TYPE_IS_NOT_NUMERIC] = \
        "aggregateQuery input, the field type is not numeric."
    ErrorCodeMap[CloudDBErrorCode.AGGREGATE_QUERY_ENTITY_DO_NOT_HAVE_FIELD] = \
        "aggregateQuery input, the field name does not exist."
    ErrorCodeMap[CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL] = "query input, query object is null."
    ErrorCodeMap[CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_MORE_THAN_ONE] = "only one pagination query is supported."
    ErrorCodeMap[CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_ONLY_SUPPORTED] = \
        "the query condition of pagination only support EqualTo, OrderBy, Limit."
    ErrorCodeMap[CloudDBErrorCode.PAGINATE_EQUAL_TO_NOT_SUPPORT_PRIMARY_KEY] = \
        "the query condition EqualTo field of pagination does not support primary key."
    ErrorCodeMap[CloudDBErrorCode.PAGINATE_ORDER_BY_NOT_SUPPORT_TYPE] = \
        "the query of pagination OrderBy field does not support ByteArray, Boolean, Text."
    ErrorCodeMap[CloudDBErrorCode.PAGINATE_EQUAL_TO_FIELD_IS_SAME_WITH_ORDER_BY] = \
        "the query condition of pagination EqualTo field can not be the same with OrderBy field."
    ErrorCodeMap[CloudDBErrorCode.FAIL_TO_PARSE_QUERY_DATA] = "fail to parse query data in transaction."
    ErrorCodeMap[CloudDBErrorCode.PAGINATE_NOT_SUPPORT_AGGREGATE] = \
        "the query condition of pagination does not support aggregate query."
    ErrorCodeMap[CloudDBErrorCode.EQUAL_TO_NOT_BEFORE_ORDER_BY] = \
        "the EqualTo must be before OrderBy in the query of pagination."
    ErrorCodeMap[CloudDBErrorCode.PAGINATE_EQUAL_TO_NOT_SUPPORT_TEXT] = \
        "the query of pagination EqualTo field does not support Text."
    ErrorCodeMap[CloudDBErrorCode.ORDER_BY_ONLY_SUPPORT_ONE_DIRECTION] = \
        "the query of OrderBy support only one direction."
    ErrorCodeMap[CloudDBErrorCode.PAGINATION_ORDER_BY_HAS_DUPLICATE_FIELD] = \
        "the query of pagination OrderBy has duplicate field."
    ErrorCodeMap[CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY] = "this query type does not support byteArray."
    ErrorCodeMap[CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY_OR_BOOLEAN] = \
        "this query type does not support byteArray or boolean."
    ErrorCodeMap[CloudDBErrorCode.ONLY_SUPPORT_TEXT_AND_STRING] = "this query type only supports Text and String."
    ErrorCodeMap[CloudDBErrorCode.NUMBER_IS_INVALID] = "The number input is NaN, infinity or negative infinity."
    ErrorCodeMap[CloudDBErrorCode.CLASS_INVALID] = "the input class is invalid."
    ErrorCodeMap[CloudDBErrorCode.FAIL_TO_GET_CREDENTIAL] = "Fail to get credential."
    ErrorCodeMap[CloudDBErrorCode.RESPONSE_IS_INVALID] = "Response is invalid."
    ErrorCodeMap[CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY] = "encrypted field does not support query."
    ErrorCodeMap[CloudDBErrorCode.USERID_IS_INVALID] = "userId input is invalid."
    ErrorCodeMap[CloudDBErrorCode.OBJECT_IS_INVALID] = "the input object is invalid."
    ErrorCodeMap[CloudDBErrorCode.ORDERBY_DO_NOT_SUPPORT_TEXT_OR_BYTEARRAY] = \
        "OrderBy does not support ByteArray or Text."
    ErrorCodeMap[CloudDBErrorCode.DATE_STRING_INVALID] = "The date string is invalid."
    ErrorCodeMap[CloudDBErrorCode.AGCONNECT_CLOUDDB_NOT_INITIALIZE] = "The AGConnectCloudDB has not been initialized."
    ErrorCodeMap[CloudDBErrorCode.DATABASE_NAME_INVALID] = "The CloudDB Zone Name is invalid."
    ErrorCodeMap[CloudDBErrorCode.ONLY_SUPPORT_ONE_SCHEMA] = "only one object type is supported for batch operations."
    ErrorCodeMap[CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER] = \
        "the string contains illegal character, use the ByteArray type if you intend to send raw bytes."
    ErrorCodeMap[CloudDBErrorCode.DUPLICATE_FIELD] = "duplicate field name."
    ErrorCodeMap[CloudDBErrorCode.FIELD_NOT_EXIST] = "field name does not exist."
    ErrorCodeMap[CloudDBErrorCode.INVALID_FIELD_TYPE] = "invalid field type."
    ErrorCodeMap[CloudDBErrorCode.INCREMENTAL_FIELD_ONLY_SUPPORT_NUMERIC] = \
        "incremental field only support numeric type."
    ErrorCodeMap[CloudDBErrorCode.PRIMARY_KEY_REQUIRED] = "primary key field is required."
    ErrorCodeMap[CloudDBErrorCode.CONDITION_EXCEEDS_LIMIT] = "the number of conditions exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.INVALID_CONDITION] = "invalid condition."
    ErrorCodeMap[CloudDBErrorCode.PRIMARY_KEY_ENCRYPTED_FIELD_CANNOT_BE_UPDATED] = \
        "primary key and encrypted fields cannot be updated and increased."
    ErrorCodeMap[CloudDBErrorCode.OPERATOR_MISMATCH_CONSTRAINT] = \
        "The class of CloudDBZoneObjectOperatorConstraint mismatch the instance of CloudDBZoneObjectOperator."
    ErrorCodeMap[CloudDBErrorCode.ERROR_QUERY_DATA_SIZE_TOO_LARGE] = "the capacity of objects exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE] = "the size of object list exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.SCHEMA_NOT_EXISTING] = "object type does not exist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATABASE_NOT_EXIST] = "CloudDBZone does not exist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_INVALID] = \
        "invalid data. The data type of the transmitted data does not match that of" \
        " the field value to be operated, or the data is out of range."
    ErrorCodeMap[CloudDBErrorCode.PARAMETER_INVALID] = "invalid parameter."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_NOT_CONCLUDE_PRIMARY_KEY] = \
        "input data does not contain the primary key field."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_NOT_CONTAIN_QUERY_CONDITION] = "invalid query condition."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_FIELD_NAME_OR_VALUE_NULL] = "invalid field name or value."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_FAILED_FOR_NO_INDEX] = \
        "the pagination query condition field is inconsistent with the index field or " \
        "the field sequence is inconsistent. A new index is required for {0}."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_TRANSACTION_SEQUENCE_INCORRECT] = \
        "incorrect transaction execution sequence."
    ErrorCodeMap[CloudDBErrorCode.URL_INVALID] = "invalid CloudDB URL."
    ErrorCodeMap[CloudDBErrorCode.TABLE_NAME_INVALID] = "invalid object type name."
    ErrorCodeMap[CloudDBErrorCode.AUTHENTICATION_ERROR] = "authentication failed."
    ErrorCodeMap[CloudDBErrorCode.HTTPS_METHOD_INVALID] = "the request type is not supported."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_JSON_INVALID] = "invalid JSON."
    ErrorCodeMap[CloudDBErrorCode.TOO_MANY_REQUESTS] = "too many requests. The system is too busy to process them."
    ErrorCodeMap[CloudDBErrorCode.QUOTA_NOT_ENOUGH] = "insufficient service quota."
    ErrorCodeMap[CloudDBErrorCode.CHARGE_NOT_ENOUGH] = "service arrears."
    ErrorCodeMap[CloudDBErrorCode.SYSTEM_ERROR] = "system error."
    ErrorCodeMap[CloudDBErrorCode.OBJECT_TYPE_DOES_NOT_EXIST] = "object type does not exist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_SIZE_ZERO] = "the number of input data records is 0."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_MISMATCH_WITH_SCHEMA] = "input data field does not match " \
                                                                          "the object type definition."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_FIELD_EMPTY_WHEN_NOT_NULL] = "value of the field cannot be null."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_SIZE_EXCEED] = \
        "single piece of inserted data volume exceeds the upper limit."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_NOT_IN_ARRAY] = "inserted data is not of the array type."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_ENCRYPT_FIELD_CAN_NOT_BE_QUERY_CONDITION] = \
        "encrypted fields cannot be used as query conditions."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_FIELD_NAME_NOT_EXIST] = "queried field does not exist."
    ErrorCodeMap[CloudDBErrorCode.NOT_SUPPORT_QUERY_DATA_TYPE] = \
        "not support the queried data type under {0} condition."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_IN_QUERY_CONDITION_VALUE_NOT_ARRAY] = \
        "the value range queried by the In condition is not in the array."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_IN_QUERY_CONDITION_VALUE_ARRAY_SIZE_ZERO] = \
        "the array size of the value range queried by the In condition is 0."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_ORDER_BY_DATA_INVALID] = "invalid OrderBy value."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_NOT_SUPPORT_QUERY] = "the query condition is not supported."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_LIMIT_DATA_INVALID] = "invalid Limit query condition."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_FUNCTION_IS_NOT_SUPPORT] = "the function is not supported."
    ErrorCodeMap[CloudDBErrorCode.OPERATE_DATA_OVERSIZE] = \
        "the total number of data records to be inserted or deleted is greater than 1000."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_ORDER_GROUP_NOT_EXIST] = \
        "the query conditions GroupBy and OrderBy cannot coexist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SELECT_GROUP_FIELD_SAME] = \
        "if the GroupBy query condition exists, the query field (non- aggregate query) must exist in GroupBy."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_GROUP_BY_FIELD_MUST_INDEX] = "the value of GroupBy must contain an index."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_EQUAL_TO_NOT_SUPPORT_PRIMARY_KEY] = \
        "the EqualTo pagination query condition does not support primary keys."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_CONDITION_NUM_ERROR] = \
        "only one pagination query condition is supported."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_OBJECT_IS_NULL] = \
        "the input object of pagination query condition is null."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_ORDER_BY_NOT_SUPPORT_TYPE] = \
        "the OrderBy pagination query condition does not support the Text, Boolean, or ByteArray type."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_EQUAL_TO_SUPPORT_TYPE] = \
        "the EqualTo pagination query condition does not support the Text type."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_ORDER_BY_DIRECTION_CONSISTENT] = \
        "the sequence of the OrderBy query condition must be the same."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PAGINATION_QUERY_SEQUENCE] = \
        "the pagination query condition must be after the range query condition and before the Limit query condition."
    ErrorCodeMap[CloudDBErrorCode.CLOUD_PAGINATION_ORDER_BY_HAS_DUPLICATE_FIELD] = \
        "the OrderBy pagination query condition does not support duplicate field names."
    ErrorCodeMap[CloudDBErrorCode.CLOUD_SELECT_QUERY_NOT_REPEAT] = \
        "the Select statement does not support duplicate field names or aliases."
    ErrorCodeMap[CloudDBErrorCode.NOT_SUPPORT_DATA_TYPE] = "MIME type error,only support json/octet-stream."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_FIELD_NAME_NOT_EXIST_IN_UPDATE] = "updated field does not exist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_ENCRYPTED_FIELDS_CANNOT_BE_UPDATED] = "encrypted fields cannot be updated."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_EXCEEDS_LIMIT_IN_WHERE_CONDITION] = \
        "schema exceeds the limit in the where condition."
    ErrorCodeMap[CloudDBErrorCode.LISTENER_TOO_MANY] = \
        "the trigger capacity is full. Release the capacity and try again."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_EXPORT_TOO_MANY] = "exported data size is too large."
    ErrorCodeMap[CloudDBErrorCode.AGC_CLOUD_GATEWAY_INVALID] = "invalid AppGallery Connect gateway."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_APP_CREATION_FAILURE] = "CloudDB service is not enabled."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INDEX_NUMBER_EXCEED] = \
        "number of indexes exceeds the specification limitations {0}."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INDEX_FIELD_NUMBER_EXCEED] = \
        "number of fields in the index exceeds the specification limitations {0}."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INDEX_NAME_INVALID] = "invalid index name."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INDEX_FIELDS_REPEAT] = "duplicate fields in an index."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INDEX_FIELD_NOT_EXIST_IN_SCHEMA] = "index field does not exist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INDEX_FIELD_NOT_SUPPORT_SOME_TYPE] = \
        "type of the index field {0} does not meet the specifications."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INDEX_LIST_NOT_ARRAY] = "fields of each index are not in the array."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_INDEXES_NOT_ARRAY] = "index field is not in the array."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_INDEX_NOT_JSON_TYPE] = "index is not in the JSON format."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_INDEX_SETTING_INVALID] = "invalid index."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PRIMARY_KEY_NUMBER_EXCEED] = \
        "number of primary keys exceeds the specification limitations {0}."
    ErrorCodeMap[
        CloudDBErrorCode.ERROR_CODE_ENCRYPT_FIELD_BE_PRIMARY_KEY] = "encrypted field cannot be set in a primary key."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PRIMARY_KEY_NOT_SUPPORT_SOME_TYPE] = \
        "type of the primary key field {0} does not meet the specifications."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PRIMARY_KEY_SHALL_NOT_NULL] = "primary key field is required."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PRIMARY_KEY_SHALL_NOT_SET_DEFAULT_VALUE] = \
        "default value cannot be set for the primary key."
    ErrorCodeMap[CloudDBErrorCode.NOT_NULL_FIELD_NOT_SUPPORT_SOME_TYPE] = \
        "type of the non-null field {0} does not meet the specifications."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_ENCRYPT_FIELD_NOT_SET_NOT_NULL] = \
        "encrypted fields cannot be set to a non-empty value."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_FIELD_DEFAULT_VALUE_INVALID] = "default value of type overflows."
    ErrorCodeMap[CloudDBErrorCode.SCHEMA_DEFAULT_VALUE_NOT_SUPPORT] = \
        "type of the default value field {0} does not meet the specifications."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_DEFAULT_VALUE_EMPTY] = \
        "only the default value of a string type can be set to an empty string."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DEFAULT_VALUE_INVALID] = "invalid default value."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_ENCRYPT_FIELD_SET_DEFAULT_VALUE] = \
        "default value cannot be set for an encrypted field."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_NOT_SET_DEFAULT_VALUE_AS_NOT_NULL_TRUE] = \
        "default value is not set for the non-null field."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_RIGHT_NOT_ARRAY_TYPE] = "permission is not in the array."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_RIGHT_EMPTY] = "the permission field is required."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_RIGHT_MEMBER_NOT_JSON_TYPE] = \
        "role and permission are not in the JSON format."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_RIGHT_MISMATCH_WITH_ROLE] = "permission does not match the role."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_RIGHT_NOT_SETTING] = "no permission is set for the object type {0}."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_RIGHT_SETTING_FOR_NOT_EXIST_SCHEMA] = \
        "permission is set for an object type that does not exist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_RIGHT_NOT_SUPPORT] = "unsupported permission is set."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_VERSION_INVALID] = "invalid object type version number."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_FIELD_NUMBER_EXCEED] = \
        "number of object type fields exceeds the upper limit {0}."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_STRING_TYPE_NUMBER_EXCEED] = \
        "number of fields of the string type exceeds the upper limit {0}."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMAS_JSON_EMPTY] = "object type is not in the JSON."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMAS_MEMBER_NOT_JSON_TYPE] = \
        "object type member is not in the JSON format."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_FIELDS_NOT_ARRAY] = \
        "input field of the object type is not in the array."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_FIELDS_NOT_EXIST] = "object type does not contain fields."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_FIELDS_NOT_JSON_TYPE] = \
        "field in the object type is not in the JSON format."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_FIELD_ATTRIBUTES_EMPTY] = "object type field is incomplete."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_FIELD_NAME_INVALID] = \
        "object type field name does not meet the specifications."
    ErrorCodeMap[CloudDBErrorCode.SCHEMA_FIELD_ATTRIBUTES_NOT_BOOLEAN] = \
        "incorrect properties related to the Boolean type in the object type field {0}."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_NO_PRIMARY_KEY] = "primary key is not set for the object type {0}."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_INVALID] = "invalid object type."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_PACKAGE_NAME_INVALID] = \
        "invalid package name of the exported object type."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_PACKAGE_EXPORT_ERROR] = \
        "an exception occurred when the object type package is exported."
    ErrorCodeMap[CloudDBErrorCode.WRITE_DATA_SIZE_EXCEED_PER_SECOND] = \
        "the data written per second exceeds 10 MB. Adjust the amount of data written."
    ErrorCodeMap[CloudDBErrorCode.ENCRYPT_FIELD_PERMISSION_INVALID] = \
        "permissions of everyone or authenticated users cannot be set for object types containing encrypted fields."
    ErrorCodeMap[CloudDBErrorCode.ENCRYPT_FIELD_NUM_EXCEED] = \
        "a maximum of five fields can be encrypted for an object type."
    ErrorCodeMap[CloudDBErrorCode.ENCRYPT_FIELD_TYPE_INVALID] = \
        "fields of the Text and ByteArray types cannot be encrypted."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_EXPORT_DATA_PARA_INVALID] = "invalid parameter for exporting data."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_EXPORT_ENCRYPT_SCHEMA] = \
        "data of object types containing encrypted fields cannot be exported."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_IMPORT_ENCRYPT_SCHEMA] = \
        "importing data to object types that contain encrypted fields is not supported."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_SIZE_BIGGER_THAN_ONE] = \
        "number of downloaded data records is greater than 1."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PROCESS_ID_INVALID] = "query progress does not exist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_NUMBER_EXCEED] = "the number of tables exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.PRIMARY_KEY_NOT_SUPPORT_CHANGE] = "the primary key cannot be modified."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PERMISSION_DENIED] = "permission denied."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_DATA_UPSERT_TOO_LARGE] = \
        "the size of the data to be written exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.UPDATE_FIELDS_COUNT_EXCEED_LIMIT] = "the count of update fields exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.OPERATORS_COUNT_IN_EXPRESSION_EXCEED_LIMIT] = \
        "the count of operators in expression exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.SCHEMA_ALREADY_CHANGED] = "the original object type has been changed."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_SCHEMA_FIELD_NAME_SAME] = "duplicate field name."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INDEX_NAME_REPEAT] = "duplicate index name."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PARAM_INVALID] = "invalid parameter."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_NOT_NULL_FIELD_CANNOT_BE_NULL] = "not null field can not be null."
    ErrorCodeMap[CloudDBErrorCode.PRIMARY_KEY_CANNOT_BE_UPDATED] = "the primary key cannot be updated."
    ErrorCodeMap[CloudDBErrorCode.ERROR_TRANSACTION_FAILED_DATA_CHANGED] = "the cache plan has been changed."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_VALUE_OUT_OF_RANGE] = "the value range exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_IMPORT_DATA_INDEX_FIELD_VALUE_LENGTH_EXCEED] = \
        "the number of index fields exceeds the limit."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_INVALID_INCREMENT_OR_UPDATE] = "invalid increment or update."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_FIELD_TYPE_CANNOT_INCREMENT] = \
        "user input data value field type can not increment."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_TOO_MANY_QUERY_CONDITION] = "too many query condition."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_OBJECT_NOT_EXIST] = \
        "the record corresponding to the primary key does not exist."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_PRIMARY_KEY_DUPLICATE] = "primary key duplicated."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_FIELD_TYPE_NOT_SUPPORT_INCREMENT] = \
        "field type not support increment operation."
    ErrorCodeMap[CloudDBErrorCode.ERROR_CODE_VIOLATES_UNIQUE_CONSTRAINT] = "violates unique constraint."


init()


def get_error_message(code=str):
    if len(ErrorCodeMap) == 0:
        init()
    message = ErrorCodeMap.get(code)
    return message if message is not None else "internal error"
