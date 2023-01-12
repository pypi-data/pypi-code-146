import logging
from random import randint

from deprecated import deprecated
from typing import List, Dict

from tcsoa.backend import RestBackend
from tcsoa.config import TcSoaConfig
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2010_09.DataManagement import PropInfo, NameValueStruct1
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Core._2007_12.Session import StateNameValue
from tcsoa.gen.Core._2011_06.Session import Credentials
from tcsoa.gen.Core.services import DataManagementService, SessionService


class TcConnection:
    def __init__(self, url: str, username: str, password: str, descrimator: str = None, insecure: bool = False):
        """
        This class aims to provide a simple interface to create a Teamcenter connection.
        Use it either like so:
            >>> conn = TcConnection('http://my.teamcenter:7001/tc', 'dcproxy', 'dcproxy')
            >>> try:
            >>>     # do TC stuff
            >>> finally:
            >>>     conn.close()
        Or with the Context Manager syntax like this:
            >>> with TcConnection('http://my.teamcenter:7001/tc', 'dcproxy', 'dcproxy'):
            >>>     # do TC stuff
        Or - if you are fearless - just like that
            >>> TcConnection('http://my.teamcenter:7001/tc', 'dcproxy', 'dcproxy')
            >>> # do TC stuff
            >>> TcSoaBasics.logout()


        :param url: Your Teamcenter URL, like 'http://my.teamcenter:7001/tc'
        :param username: The Teamcenter username to be used to connect to Teamcenter
        :param password: The Teamcenter password of the username provided to connect to Teamcenter
        :param descrimator: The descrimator to use - if not provided, a random descriminator will be used
        :param insecure: A flag for convenience to disable TLS checking
        """
        self.url = url
        self.username = username
        self.password = password
        self.descrimator = descrimator
        self.insecure = insecure

        self.connect()

    def __enter__(self):
        pass

    def connect(self):
        TcSoaConfig.backend = RestBackend(self.url)
        if self.insecure:
            TcSoaConfig.backend.session.verify = False
            import urllib3
            urllib3.disable_warnings()

        TcSoaBasics.setCredentials(self.username, self.password)
        TcSoaBasics.descrimator = self.descrimator if self.descrimator else f'TcSoa_{randint(0, 999999)}'
        login_result = TcSoaBasics.login()
        login_success = len(login_result['PartialErrors']) == 0
        if login_success:
            logging.info(f'Logged in on Server {TcSoaBasics.server} - with log file {TcSoaBasics.log_file}')
            return self
        else:
            errors = '\n'.join(login_result['PartialErrors'])
            logging.error('Error occured when logging in:\n' + errors)
            raise ConnectionError(errors)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        TcSoaBasics.logout()


class TcSoaBasics:
    NULLTAG = 'AAAAAAAAAAAAAA'

    # Login configuration
    username = None
    password = None
    group = ''
    role = ''
    locale = 'en_US'
    descrimator = 'TcSoa.py'

    # Server Information
    log_file: str = None
    server: str = None

    @classmethod
    def setCredentials(cls, username, password, group='', role=''):
        cls.username = username
        cls.password = password
        cls.group = group
        cls.role = role

    @classmethod
    def login(cls):
        login_response = SessionService().login3(
            credentials=Credentials(
                user=cls.username,
                password=cls.password,
                group=cls.group,
                role=cls.role,
                locale=cls.locale,
                descrimator=cls.descrimator,
            )
        )
        cls.log_file = login_response.serverInfo['LogFile']
        cls.server = login_response.serverInfo['HostName']
        return login_response

    @classmethod
    def logout(cls):
        return SessionService().logout()

    @classmethod
    def load_objects(cls, uids: List[str]) -> Dict[str, BusinessObject]:
        if not uids:
            return dict()
        load_objs_result = DataManagementService().loadObjects(uids=uids)
        model_objects = load_objs_result['modelObjects']
        return {p: model_objects[p] for p in load_objs_result['plain']}

    @classmethod
    def load_object(cls, uid: str):
        obj = None
        for obj in cls.load_objects([uid]).values():
            break
        return obj

    @classmethod
    def getProperties(cls, objects: List[BusinessObject], properties: List[str]) -> Dict[str, BusinessObject]:
        response = DataManagementService().getProperties(
            objects=objects,
            attributes=properties
        )
        return {uid: response['modelObjects'][uid] for uid in response['plain']}

    @classmethod
    @deprecated(version="0.5.0", reason="Use the other getPropXXXX methods instead.")
    def getProperty(cls, bo: BusinessObject, prop_name: str):
        return cls.getProperties([bo], [prop_name])[bo['uid']]['props'][prop_name]

    @classmethod
    def getPropString(cls, bo: BusinessObject, prop_name: str):
        lst = cls.getPropStringList(bo, prop_name)
        return lst[0] if lst else None

    @classmethod
    def getPropStringList(cls, bo: BusinessObject, prop_name: str):
        return cls.getProperties([bo], [prop_name])[bo['uid']]['props'][prop_name].get('uiValues', list())

    @classmethod
    def getMultiPropStringList(cls, bos: List[BusinessObject], prop_name: str) -> Dict[str, List[str]]:
        return {uid: obj.prop(prop_name) for uid, obj in cls.getProperties(bos, [prop_name]).items()}

    @classmethod
    def getMultiPropString(cls, bos: List[BusinessObject], prop_name: str) -> Dict[str, str]:
        return {uid: val_list[0] for uid, val_list in cls.getMultiPropStringList(bos, prop_name).items()}

    @classmethod
    def getPropObject(cls, bo: BusinessObject, prop_name: str) -> BusinessObject:
        lst = cls.getPropObjectList(bo, prop_name)
        return lst[0] if lst else None

    @classmethod
    def getPropObjectList(cls, bo: BusinessObject, prop_name: str) -> List[BusinessObject]:
        response: ServiceData = DataManagementService().getProperties(
            objects=[bo],
            attributes=[prop_name],
        )
        ref_obj_uids = response.modelObjects[bo.uid].prop(prop_name, db_value=True)
        return [response.modelObjects[uid] for uid in ref_obj_uids if uid]

    @classmethod
    def getMultiPropObjectList(cls, bos: List[BusinessObject], prop_name: str) -> Dict[str, List[BusinessObject]]:
        response = DataManagementService().getProperties(
            objects=bos,
            attributes=[prop_name],
        )
        obj2refs_map = {bo.uid: response.modelObjects[bo.uid].prop(prop_name, db_value=True) for bo in bos}
        return {uid: [response.modelObjects[ref] for ref in refs if ref] for uid, refs in obj2refs_map.items()}

    @classmethod
    def getMultiPropObject(cls, bos: List[BusinessObject], prop_name: str) -> Dict[str, BusinessObject]:
        return {uid: val_list[0] for uid, val_list in cls.getMultiPropObjectList(bos, prop_name).items()}

    @classmethod
    def bool2property_str(cls, val: bool) -> str:
        return '1' if val else '0'

    @classmethod
    def setMultiPropString(cls, bo: BusinessObject, prop2val_map: Dict[str, str]):
        DataManagementService.setProperties2(
            info=[
                PropInfo(
                    object=bo,
                    vecNameVal=[
                        NameValueStruct1(
                            name=prop_name,
                            values=[prop_val]
                        )
                        for prop_name, prop_val in prop2val_map.items()
                    ]
                )
            ],
            options=[],
        )

    @classmethod
    def setPropString(cls, bo: BusinessObject, prop_name: str, prop_val: str):
        DataManagementService.setProperties2(
            info=[
                PropInfo(
                    object=bo,
                    vecNameVal=[
                        NameValueStruct1(
                            name=prop_name,
                            values=[prop_val]
                        )
                    ]
                )
            ],
            options=[],
        )

    @classmethod
    def setBypass(cls, enabled=True):
        return SessionService().setUserSessionState(
            pairs=[
                StateNameValue(
                    name='fnd0bypassflag',
                    value=cls.bool2property_str(enabled)
                )
            ]
        )

    @classmethod
    def set_object_load_policy(cls, bo_name: str, properties: List[str]):
        TcSoaConfig.backend.set_object_load_policy(bo_name, properties)

    @classmethod
    def add_object_load_policy(cls, bo_name: str, properties: List[str]):
        TcSoaConfig.backend.add_object_load_policy(bo_name, properties)

    @classmethod
    def clear_object_load_policy(cls, bo_name: str):
        TcSoaConfig.backend.clear_object_load_policy(bo_name)

    @classmethod
    def clear_all_object_load_policies(cls):
        TcSoaConfig.backend.clear_all_object_load_policies()

    @classmethod
    def get_cached_obj(cls, uid: str):
        obj = TcSoaConfig.internal_get_obj(uid)
        if obj is not None:
            bo = BusinessObject()
            bo.uid = bo.objectID = obj['uid']
            bo.type = obj['type']
            bo.className = obj['className']
            return bo
        return None
