'''
Classes to handle ChangeInstances on NetOrca
'''

import logging
import netorca_sdk.constants as const
from netorca_sdk.base import BaseObj, Endpoint
from netorca_sdk.elements import teams, applications
from netorca_sdk.elements import declarations, sis
from urllib.parse import urljoin
from netorca_sdk.utils.decorators import owner_required

logger = logging.getLogger(__name__)

class ChangeInstanceObj(BaseObj):
    '''
    Change instance object
    '''
    def __init__(self, *args, **kwargs):
        self.class_map = {
            "service_item": {'module': sis, 'name': 'ServiceItemObj'},
            "new_declaration": {'module': declarations, 'name': 'DeclarationObj'},
            "owner": {'module': teams, 'name': 'TeamsObj'},
            "application": {'module': applications, 'name': 'ApplicationObj'}
        }
        super().__init__(*args, **kwargs)
        self._validate_input()
        self._create_paths()

    def _validate_input(self):
        '''
        Makes sure that required field exist in the change instance input
        :return: None
        '''
        required_fields = ['uuid', 'state']
        if not all(i in self.input.keys() for i in required_fields):
            print('hit')
            raise ValueError('Required fields were not provided in ChangeInstanceObj initialisation')

    def _create_paths(self):
        '''
        Creates the paths for any updates
        :return: None
        '''
        if self.context == 'owner':
            self.base_path = const._PATH_CHANGE_INSTANCES_OWNER
        elif self.context == 'consumer':
            self.base_path = const._PATH_CHANGE_INSTANCES_CONSUMER
        else:
            raise ValueError(f'Context f{ self.context } is not supported')

    def _modify_change_state(self, new_state, deployed_item):
        '''
        Put request to modify the change state
        :return:
        '''
        if deployed_item:
            data = {
                'state': new_state,
                'deployed_item': deployed_item
            }
        else:
            data = {
                'state': new_state,
                'deployed_item': {}
            }
        path = urljoin(self.base_path, self.uuid+'/')
        response = self.conn.put(path, data)
        if response.status_code == 200:
            return new_state
        else:
            logger.warning(f'Failed to update Change Instance {self.uuid}')
            return None
        # Update to completed here

    @owner_required
    def complete_change(self, deployed_item={}):
        '''
        Mark change as completed
        :param deployed_item: dict -> deployed item dictionary
        :return: new state
        '''
        if self.state == const.NETORCA_STATES_APPROVED:
            return self._modify_change_state(const.NETORCA_STATES_COMPLETED, deployed_item)
        else:
            logger.warning('Cannot complete change, not in correct state')
            return None

    @owner_required
    def error_change(self, deployed_item={}):
        '''
        Mark change as errored
        :param deployed_item:
        :return:
        '''
        if self.state != const.NETORCA_STATES_COMPLETED or self.state != const.NETORCA_STATES_ERROR:
            return self._modify_change_state(const.NETORCA_STATES_ERROR, deployed_item)
        else:
            logger.warning('Cannot complete change, not in correct state')
            return None

            # Update change state here

    @owner_required
    def approve_change(self, deployed_item={}):
        '''
        Mark change as approved
        :param deployed_item:
        :return:
        '''
        if self.state == const.NETORCA_STATES_PENDING:
            # Update to approved here
            return self._modify_change_state(const.NETORCA_STATES_APPROVED, deployed_item)
        else:
            logger.warning('Cannot approve change, it not in the PENDING state')
            return None


class ChangeInstances(Endpoint):
    def __init__(self, conn, context='owner'):
        '''
        Initialises the class
        :param conn: Connection object
        :param context: str -> consumer or serviceowner context
        '''
        self.settings = {
            'owner_path': const._PATH_CHANGE_INSTANCES_OWNER,
            'consumer_path': const._PATH_CHANGE_INSTANCES_CONSUMER,
            'filters': [
                'consumer_owner_uuid',
                'service_owner_uuid',
                'application_uuid',
                'service_uuid',
                'service_item_uuid',
                'request_uuid'
            ]
        }
        self.class_ = ChangeInstanceObj
        super().__init__(conn, context)

# class ChangeInstances:
#     '''
#     Class to connect to the ChangeInstances API
#     '''
#     def __init__(self, conn, context='owner'):
#         '''
#         Initialise
#         :param conn: base.Connection instance
#         '''
#         self.conn = conn
#         self.context = context
#         if self.context=='owner':
#             self.path = const._PATH_CHANGE_INSTANCES_OWNER
#         elif self.context=='consumer':
#             self.path = const._PATH_CHANGE_INSTANCES_CONSUMER
#         else:
#             raise AttributeError('context type not supported')
#         self.objs = []
#
#     def get_all(self, state=None, service_uuid=None):
#         '''
#         Gets all the change instances
#         :param state: str -> state to filter by
#         :param service_uuid: str -> uuid of a Service to filter by
#         :return:
#         '''
#         filters = {}
#         if state:
#             filters['state'] = state
#         if service_uuid:
#             filters['service_uuid'] = service_uuid
#         response = self.conn.get(path=self.path, filters=filters)
#         if response.status_code == 200 and response.json()['results']:
#             for item in response.json()['results']:
#                 self.objs.append(ChangeInstanceObj(self.conn, self.context, item))
#         else:
#             raise ConnectionError('No results return from ChangeInstance API, something went wrong')
#
#     def get_single(self, uuid):
#         '''
#         Returns a single change_instance based on uuid or id
#         :param uuid: str -> uuid
#         :return: ChangeInstanceObj instance
#         '''
#         url = urljoin(self.path, uuid)
#         response = self.conn.get(path=url)
#         if response.status_code==200:
#             return ChangeInstanceObj(self.conn, self.context, response.json())
#         else:
#             logger.warning('CI not found')
#             return None







