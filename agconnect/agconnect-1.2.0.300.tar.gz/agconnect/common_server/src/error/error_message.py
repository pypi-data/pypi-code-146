# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

class ErrorCodeConstant:
    FS_READ_FAIL = {'code': '10101', 'message': 'Fs read fail.'}

    FS_WRITE_FAIL = {'code': '10102', 'message': 'Fs write fail.'}

    URL_VALIDATE_FAIL = {'code': '10201', 'message': 'Url validate fail.'}

    METHOD_NOT_EXIST = {'code': '10202', 'message': 'Url method not exist.'}

    URL_NOT_EXIST = {
        'code': '10203',
        'message': 'Url is not found, please check your url path.',
    }

    FILE_NOT_EXIST = {
        'code': '10204',
        'message': 'File not exist.',
    }

    NOT_A_FILE = {
        'code': '10205',
        'message': 'Path is not a file path.',
    }

    FILE_NO_READ_PERMISSION = {
        'code': '10206',
        'message': 'No permission to read the file.',
    }

    ENV_NOT_NODEJS = {
        'code': '10301',
        'message': 'Currently, only the nodejs environment is supported.',
    }

    CREDENTIAL_ENV_NOT_SET = {
        'code': '10302',
        'message': 'No credential file path and AGC_CONFIG not set.',
    }

    LOAD_SERVICE_CONFIG_ERROR = {
        'code': '10400',
        'message': 'Load service config error.',
    }

    LOAD_CUSTOM_CONFIG_ERROR = {
        'code': '10401',
        'message': 'Load custom config error.',
    }

    CREDENTIAL_PARSER = {'code': '10501', 'message': 'Parser credential fail.'}

    AGC_CLIENT_PARA = {'code': '10601',
                       'message': 'Create agc client parameter error.'}

    AGC_CLIENT_EXIST = {'code': '10602',
                        'message': 'Agc client name already exist.'}

    AGC_CLIENT_CREDENTIAL = {'code': '10603',
                             'message': 'Agc client credential fail.'}

    AGC_CLIENT_NOT_EXIST = {'code': '10604',
                            'message': 'Agc client name not exist.'}

    INVALID_REGION = {'code': '10605',
                      'message': 'Init gc client with invalid region.'}

    REQUEST_TOK_FAILED = {'code': '10606',
                          'message': 'Request access token failed.'}

    CREATE_HTTP_CLIENT_RESPONSE_TYPE = {
        'code': '10701',
        'message': 'Create http client response type error.'
                   'Only support arraybuffer|blob|document|json|text|stream'
    }

    REQUEST_FAILED = {
        'code': '10799',
        'message': 'HTTP Request is failed.',
    }

    GET_CREDENTIAL_NULL = {'code': 12000, 'message': 'the credential is null'}

    @staticmethod
    def to_message(err) -> str:
        return err['code'] + ': ' + err['message']
