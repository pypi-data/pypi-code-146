''''
Contains the Constants used by ansible modules
'''
NETORCA_STATES_ERROR = 'ERROR'
NETORCA_STATES_PENDING = 'PENDING'
NETORCA_STATES_APPROVED = 'APPROVED'
NETORCA_STATES_COMPLETED = 'COMPLETED'
NETORCA_VALID_STATES = [
    NETORCA_STATES_ERROR,
    NETORCA_STATES_PENDING,
    NETORCA_STATES_APPROVED,
    NETORCA_STATES_COMPLETED
]

FIELDS_URL = 'url'
FIELDS_USER = 'username'
FIELDS_API_KEY = 'token'
FIELDS_PASS = 'password'
FIELDS_STATE = 'state'
FIELDS_SERVICE = 'service_name'
FIELDS_UUID = 'uuid'
FIELDS_DEPLOYED_ITEM = 'deployed_item'


_PATH_LOGIN = "/api-token-auth/"
_PATH_CHANGE_INSTANCES_OWNER = "/orcabase/serviceowner/change_instances/"
_PATH_CHANGE_INSTANCES_CONSUMER = "/orcabase/consumer/change_instances/"
_PATH_SERVICE_ITEMS_OWNER = "/orcabase/serviceowner/service_items/"
_PATH_SERVICE_ITEMS_CONSUMER = "/orcabase/consumer/service_items/"
_PATH_SERVICE_OWNER = "/orcabase/serviceowner/services/"
_PATH_SERVICE_CONSUMER = "/orcabase/consumer/services/"
_PATH_TEAMS = "/account/teams/"
