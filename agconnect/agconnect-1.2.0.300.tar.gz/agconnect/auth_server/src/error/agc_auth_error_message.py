# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

class AuthErrorCode:
    CLIENT_INITIALIZE_FAILED = {'code': '11000',
                                'message': 'Failed to initialize the client'}

    PROJECT_DO_NOT_SET_REGION = {'code': '11001',
                                 'message': 'No data storage location is set for the project'}

    UID_IS_INVALID = {'code': '11002',
                      'message': 'Uid is invalid.'}

    SIGN_PRIVATE_KEY_IS_INVALID = {'code': '11003',
                                   'message': 'The private key for user signature is invalid.'}

    PHOTO_URL_INVALID = {'code': '11004',
                         'message': 'Photo url invalid.'}

    FAILED_TO_SIGN_JWT = {'code': '11005',
                          'message': 'Jwt signature failed.'}

    FAILED_TO_GENERATE_RSA_KEY_PAIR = {'code': '11006',
                                       'message': 'Failed to generate the rsa public and private keys.'}

    INVALID_IMPORT_USER_DATA = {'code': '11007',
                                'message': 'The imported user file data is invalid.'}

    IMPORT_USER_DATA_OVER_LIMIT_SIZE = {'code': '11008',
                                        'message': 'The number of imported users exceeds the upper limit.'}

    INVALID_IMPORT_USER_FILE = {'code': '11009',
                                'message': 'The imported user file is invalid.'}

    INVALID_ACCESS_IMPORT_USER_FILE = {'code': '11010',
                                       'message': 'No permission to read the imported user file.'}

    IMPORT_USER_FAILED = {'code': '11011',
                          'message': 'Import user failed.'}

    EXPORT_USER_DATA_FILEPATH_IS_INVALID = {'code': '11012',
                                            'message': 'The exported user file path is invalid.'}

    GET_BLOCK_USER_LIST_FAILED = {'code': '11013',
                                  'message': 'Get block user list failed.'}

    GET_EXPORT_USER_FAILED = {'code': '11014',
                              'message': 'Get export user failed.'}

    INVALID_ACCESS_EXPORT_USER_FILE = {'code': '11015',
                                       'message': 'No permission to write the file for exporting user.'}

    EXPORT_USER_TO_FILE_FAILED = {'code': '11016',
                                  'message': 'Export user to file failed.'}

    REVOKE_REFRESH_UID_IS_NULL = {'code': '11017',
                                  'message': 'Uid for revoke tokens is null.'}

    REVOKE_REFRESH_FAILED = {'code': '11018',
                             'message': 'Revoke tokens failed.'}

    VERIFY_ACCESS_IS_NULL = {'code': '11019',
                             'message': 'Access token for verify access tokens is null.'}

    ACCESS_INVALID_FORMAT = {'code': '11020',
                             'message': 'Access token invalid format.'}

    ACCESS_VERIFY_FAILED = {'code': '11021',
                            'message': 'Access token verify failed.'}

    JWT_EXPIRE = {'code': '11022',
                  'message': 'Jwt expire'}

    GET_PUBLIC_KEY_FAILED = {'code': '11023',
                             'message': 'Import user failed.'}

    ACCESS_ALG_IS_INVALID = {'code': '11024',
                             'message': 'Access token algorithm is invalid.'}

    ACCESS_KID_IS_INVALID = {'code': '11025',
                             'message': 'Access token kid is invalid.'}

    JWT_VERIFY_FAILED = {'code': '11026',
                         'message': 'Jwt verify failed.'}

    JWT_REVOKED = {'code': '11027',
                   'message': 'jwt revoked.'}

    EXPORT_USER_FILE_DIR_NOT_EXIST = {'code': '11028',
                                      'message': 'Folder of export user file does not exist.'}

    INVOKE_INTERFACE_FAIL = {'code': '11029',
                             'message': 'Invoke interface failed.'}

    AUTH_CLI_REQUEST_FAIL = {'code': '66000',
                             'message': 'Request by Auth HTTP Client is failed.'}
