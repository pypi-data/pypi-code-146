from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createAppUidObjects(cls, count: int) -> ServiceData:
        """
        Create appuid object for datasets
        An appuid is an NX concept which maps to an instance of a POM application object. This service will create a
        set of empty appuid objects for the caller.
        
        
        Use cases:
        NX stores their CAD data in Teamcenter with dataset instances of type UGMASTER. NX only allows one data file
        (i.e. .prt) to be stored with a dataset. There is also a limit of one UGMASTER dataset per item revision. When
        NX needs to associate multiple data files (such as drawings, cam files etc ) with an item revision, they need a
        mechanism to be able to find the data file and know which dataset it is stored with. To do this NX creates an
        appuid and associates it with the dataset using the named reference name APPUID. They also store the uid of the
        appuid in the data file. When they need to access the data file they extract the appuid uid from the data file
        then search for the dataset that contains this appuid using the 'GetItemAndRelatedObjects' service. They can
        then either download the data file or update it. 
        This operation allows NX to create a series of POM application objects at one time to associate with the data
        files they are about to check in.
        """
        return cls.execute_soa_method(
            method_name='createAppUidObjects',
            library='Internal-Cad',
            service_date='2007_12',
            service_name='DataManagement',
            params={'count': count},
            response_cls=ServiceData,
        )
