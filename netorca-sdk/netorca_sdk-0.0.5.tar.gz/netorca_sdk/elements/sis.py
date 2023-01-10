'''
Classes to handle ServiceItems on NetOrca
'''

import netorca_sdk.constants as const
from netorca_sdk.base import BaseObj, Endpoint
from netorca_sdk.elements import teams, applications, services
from netorca_sdk.elements import declarations


class ServiceItemObj(BaseObj):
    def __init__(self, *args, **kwargs):
        self.class_map = {
            "service": {'module': services, 'name': 'ServiceObj'},
            "declaration": {'module': declarations, 'name': 'DeclarationObj'},
            "team": {'module': teams, 'name': 'TeamsObj'},
            "application": {'module': applications, 'name': 'ApplicationObj'}
        }
        super().__init__(*args, **kwargs)


    def _create_paths(self):
        '''
        Creates the paths for any updates
        :return: None
        '''
        if self.context == 'owner':
            self.base_path = const._PATH_SERVICE_ITEMS_OWNER
        elif self.context == 'consumer':
            self.base_path = const._PATH_SERVICE_ITEMS_CONSUMER
        else:
            raise ValueError(f'Context f{ self.context } is not supported')


class ServiceItems(Endpoint):
    def __init__(self, conn, context='owner'):
        '''
        Initialises the class
        :param conn: Connection object
        :param context: str -> consumer or serviceowner context
        '''
        self.settings = {
            'owner_path': const._PATH_SERVICE_ITEMS_OWNER,
            'consumer_path': const._PATH_SERVICE_ITEMS_CONSUMER,
            'filters': [
                'consumer_owner_uuid',
                'service_owner_uuid',
                'service_uuid',
                'service_name',
                'application_uuid',
                'runtime_state',
                'change_state'
            ]
        }
        self.class_ = ServiceItemObj
        super().__init__(conn, context)

# class ServiceItems:
#     '''
#     Class to connect to the ServiceItems API
#     '''
#     def __init__(self, conn, context='owner'):
#         '''
#         Initialise
#         :param conn: base.Connection instance
#         :param serivce: str -> name of service (if NONE gets all available services)
#         '''
#         self.conn = conn
#         self.context = context
#         if self.context=='owner':
#             self.path = const._PATH_SERVICE_ITEMS_OWNER
#         elif self.context=='consumer':
#             self.path = const._PATH_SERVICE_ITEMS_CONSUMER
#         else:
#             raise AttributeError('context type not supported')
#         self.objs = []
#
#     def get_all(self, service_uuid):
#         '''
#         Gets all change instances for a particular state
#         :return: None
#         '''
#         filters = {}
#         if service_uuid:
#             filters['service_uuid'] == service_uuid
#         response = self.conn.get(path=self.path, fitlers=filters)
#         if response.status_code == 200 and response.json()['results']:
#             for item in response.json()['results']:
#                 self.objs.append(ServiceItemObj(self.conn, self.context, item))
#         else:
#             raise ConnectionError('No results return from ChangeInstance API, something went wrong')
#
#
#     def get_single(self, uuid):
#         '''
#         Returns a single service item by uuid
#         :param uuid:
#         :return: ServiceItemObj
#         '''
#         url = urljoin(self.path, uuid)
#         response = self.conn.get(path=url)
#         if response.status_code == 200:
#             return ServiceItemObj(self.conn, self.context, response.json())
#         else:
#             logger.warning('SI not found')
#             return None