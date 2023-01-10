'''
Classes to handle Services on NetOrca
'''

import netorca_sdk.constants as const
from netorca_sdk.base import BaseObj, Endpoint
from netorca_sdk.elements import teams


class ServiceObj(BaseObj):
    def __init__(self, *args, **kwargs):
        self.class_map = {
            "owner": {'module': teams, 'name': 'TeamObj'}
        }
        super().__init__(*args, **kwargs)

class Services(Endpoint):
    def __init__(self, conn, context='owner'):
        '''
        Initialises the class
        :param conn: Connection object
        :param context: str -> consumer or serviceowner context
        '''
        self.settings = {
            'owner_path': const._PATH_SERVICE_OWNER,
            'consumer_path': const._PATH_SERVICE_CONSUMER,
            'filters': [
                'owner_uuid'
            ]
        }
        self.class_ = ServiceObj
        super().__init__(conn, context)

    def get_service_by_name(self, name):
        '''
        Returns a ServiceObj that matches the inputted name.
        :param name: str -> name of the Service
        :return: ServiceObj
        '''
        self.get_all()
        for obj in self.objs:
            if obj.name == name:
                return obj
        return None

# class Services:
#     '''
#     Class to connect to the ChangeInstances API
#     '''
#     def __init__(self, conn, context='owner'):
#         '''
#         Initialise
#         :param conn: base.Connection instance
#         :param serivce: uuid of the Service to filter by
#         '''
#         self.conn = conn
#         self.context = context
#         if self.context=='owner':
#             self.path = const._PATH_SERVICE_OWNER
#         elif self.context=='consumer':
#             self.path = const._PATH_SERVICE_CONSUMER
#         else:
#             raise AttributeError('context type not supported')
#         self.objs = []
#
#     def get_all(self):
#         '''
#         Gets all Services
#         :return: None
#         '''
#         response = self.conn.get(path=self.path)
#         if response.status_code == 200 and response.json()['results']:
#             for item in response.json()['results']:
#                 self.objs.append(ServiceObj(self.conn, self.context, item))
#         else:
#             raise ConnectionError('No results return from ServiceAPI, something went wrong')
#
#     def get_service_by_name(self, name):
#         '''
#         Returns a ServiceObj that matches the inputted name.
#         :param name: str -> name of the Service
#         :return: ServiceObj
#         '''
#         self.get_all()
#         for obj in self.objs:
#             if obj.name == name:
#                 return obj
#         return None
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
#             return ServiceObj(self.conn, self.context, response.json())
#         else:
#             logger.warning('Service not found')
#             return None