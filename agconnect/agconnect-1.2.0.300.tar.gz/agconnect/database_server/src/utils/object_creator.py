# Copyright (c) Huawei Technologies Co., Ltd. 2020-2020. All rights reserved.

import json
import os
import re
import sys

from agconnect.common_server import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap

json_fields = {'indexes', 'objectTypeName', 'indexName', 'isNeedEncrypt', 'indexList', 'notNull', 'fieldType',
               'belongPrimaryKey', 'rights', 'role', 'schemaVersion', 'sortType', 'permissions', 'defaultValue',
               'fields', 'fieldName', 'objectTypes'}
json_required_fields = {'objectTypes', 'objectTypeName', 'indexes', 'indexList', 'fieldName', 'fields', 'fieldType',
                        'belongPrimaryKey'}


def get_all_keys(data):
    keys = []
    if isinstance(data, dict):
        keys.extend(data.keys())
        for value in data.values():
            keys.extend(get_all_keys(value))
    elif isinstance(data, list):
        for item in data:
            keys.extend(get_all_keys(item))
    return set(keys)


def get_index_list(indexes):
    index_list = []
    for index in indexes:
        index_list_elements = []
        for i in index['indexList']:
            if isinstance(i, dict):
                index_list_elements.append(i['fieldName'])
            if isinstance(i, str):
                index_list_elements.append(i)
        if index_list.count(','.join(index_list_elements)) == 0:
            index_list.append(','.join(index_list_elements))
    return index_list


def split_string_and_lower(s):
    if not len(s) <= 2:
        s = s[0].lower() + s[1:]
        parts = re.split(r'(?=[A-Z])', s)
        return '_'.join(parts).lower()
    else:
        return s.lower()


def is_json_obj(file_path):
    try:
        json.load(open(file_path))
        return True
    except ValueError:
        return False
    except FileNotFoundError:
        return False


def is_json_file(filename):
    try:
        extension = os.path.splitext(filename)[1]
        return extension == ".json"
    except FileNotFoundError:
        return False


def iterate_over_object_types(data, directory):
    for object_type in data['objectTypes']:
        file_name = split_string_and_lower(object_type['objectTypeName'])
        class_name = object_type['objectTypeName']
        fields = object_type['fields']
        indexes = object_type['indexes']
        class_text = f"class {class_name}:\n"
        return_dict = iterate_over_fields(fields, class_text)
        text = return_dict.get('class_text')
        field_type_map = return_dict.get('field_type_map')
        primary_key_list = return_dict.get('primary_key_list')
        encrypted_field_list = return_dict.get('encrypted_field_list')
        get_set_text = return_dict.get('get_set_text')

        class_text = text
        index_list = get_index_list(indexes)
        args_dict = {'class_text': class_text, 'field_type_map': field_type_map, 'class_name': class_name,
                     'primary_key_list': primary_key_list, 'index_list': index_list,
                     'encrypted_field_list': encrypted_field_list, 'get_set_text': get_set_text}
        class_text = generate_class_text(args_dict)
        fd = os.open(os.path.join(directory, f"{file_name}.py"), os.O_CREAT | os.O_WRONLY, 0o644)
        with os.fdopen(fd, 'w') as f:
            f.write(class_text)


def iterate_over_fields(fields, class_text):
    field_type_map = {}
    primary_key_list = []
    get_set_text = ''
    encrypted_field_list = []
    for field in fields:
        class_text += f"    {field['fieldName']} = None\n"
        field_type_map[field['fieldName']] = field['fieldType']
        if field['belongPrimaryKey']:
            primary_key_list.append(field['fieldName'])
        if 'Encrypt' in field['fieldName']:
            encrypted_field_list.append(field['fieldName'])
        get_set_text += "\n"
        get_set_text += f"    def set_{split_string_and_lower(field['fieldName'])}(self, " \
                        f"{split_string_and_lower(field['fieldName'])}):\n"
        get_set_text += f"        self.{field['fieldName']} = {split_string_and_lower(field['fieldName'])}\n"
        get_set_text += "\n"
        get_set_text += f"    def get_{split_string_and_lower(field['fieldName'])}(self):\n"
        get_set_text += f"        return self.{field['fieldName']}\n"
    return_dict = {'class_text': class_text, 'field_type_map': field_type_map, 'primary_key_list': primary_key_list,
                   'encrypted_field_list': encrypted_field_list, 'get_set_text': get_set_text}
    return return_dict


def generate_class_text(args_dict):
    class_text = args_dict.get('class_text')
    field_type_map = args_dict.get('field_type_map')
    class_name = args_dict.get('class_name')
    primary_key_list = args_dict.get('primary_key_list')
    index_list = args_dict.get('index_list')
    encrypted_field_list = args_dict.get('encrypted_field_list')
    get_set_text = args_dict.get('get_set_text')

    class_text += "\n"
    class_text += f"    @staticmethod\n"
    class_text += f"    def get_field_type_map():\n"
    class_text += f"        return {field_type_map}\n"
    class_text += "\n"
    class_text += f"    @staticmethod\n"
    class_text += f"    def get_class_name():\n"
    class_text += f"        return '{class_name}'\n"
    class_text += "\n"
    class_text += f"    @staticmethod\n"
    class_text += f"    def get_primary_key_list():\n"
    class_text += f"        return {primary_key_list}\n"
    class_text += "\n"
    class_text += f"    @staticmethod\n"
    class_text += f"    def get_index_list():\n"
    class_text += f"        return {index_list}\n"
    class_text += "\n"
    class_text += f"    @staticmethod\n"
    class_text += f"    def get_encrypted_field_list():\n"
    class_text += f"        return {encrypted_field_list}\n"
    class_text += get_set_text

    return class_text


def create_class_from_json(json_file_path, directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except TypeError:
        logger.error("The directory is not a string")
        return False

    if not json_file_path or not directory:
        logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
        raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                        error_message=ErrorCodeMap.get(CloudDBErrorCode.
                                                                       ERROR_CODE_DATA_INVALID))
    if not is_json_obj(json_file_path) or not is_json_file(json_file_path):
        logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
        raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                        error_message=ErrorCodeMap.get(CloudDBErrorCode.
                                                                       ERROR_CODE_DATA_INVALID))
    file = open(json_file_path)
    json_data_obj = json.load(file)
    file.close()
    json_keys = get_all_keys(json_data_obj)
    res = json_keys.issubset(json_fields) or json_required_fields.issubset(json_keys)
    if not res:
        logger.error('json file is not correct, fields are not matched')
        return False
    data = json_data_obj

    iterate_over_object_types(data, directory)
    return True


if __name__ == '__main__':
    json_path = sys.argv[1]
    model_directory_path = sys.argv[2]
    create_class_from_json(json_path, model_directory_path)
