from __future__ import annotations

from tcsoa.gen.Internal.BusinessModeler._2011_06.DataModelManagement import ServerCacheResponse
from tcsoa.base import TcService


class DataModelManagementService(TcService):

    @classmethod
    def updateClientMetaCache(cls, option: int) -> str:
        """
        update client meta cache basd on delta xml during BMIDE hot deploy.
        """
        return cls.execute_soa_method(
            method_name='updateClientMetaCache',
            library='Internal-BusinessModeler',
            service_date='2011_06',
            service_name='DataModelManagement',
            params={'option': option},
            response_cls=str,
        )

    @classmethod
    def updateServerMetaCache(cls, option: int) -> ServerCacheResponse:
        """
        This Teamcenter Service generates or deletes the metadata cache based on the value passed in the input
        argument. If the argument (option=0) is defined for creating the metadata cache, then the metadata cache is
        created and saved into a binary file and persisted in the database in the form of a dataset. If the argument
        (option=1) is defined for deleting the metadata cache, then the existing metadata cache dataset in the database
        is deleted. The Teamcenter servers starting up after this point will run in the local cache mode. NOTE: This
        operation is invoked during live deployment from BMIDE
        
        Use cases:
        Use case 1: Update the metadata cache to improve Teamcenter server memory footprint and performance after live
        deployment of data model changes such as Business Objects, Properties and Constants
        
        Turn on the option by setting it to 0, and deploy the metadata changes to the database. The metadata cache
        binary file will be generated and the cache dataset will be updated in the database. The Teamcenter server(s)
        will pick up the updated cache. 
        
        Use case 2: Delete the metadata cache after live deployment of data model changes such as Business Objects,
        Properties and Constants
        
        Turn off the option by setting it to 1, and deploy the metadata changes to the database. The metadata cache
        dataset will be deleted from the database if it exists. Teamcenter server(s) functioning at the moment will
        continue to use the stale cache i.e., the deployed metadata will not be reflected in these caches. Teamcenter
        server(s) starting up after this stage will run in the local cache mode.
        
        NOTE: In order to improve live deploy performance, typically, interim deployments will be done with the option
        set to 1. Finally, when user is done with metadata changes, the option can be set to 0 so that cache is
        generated on the server which improves Teamcenter performance.
        """
        return cls.execute_soa_method(
            method_name='updateServerMetaCache',
            library='Internal-BusinessModeler',
            service_date='2011_06',
            service_name='DataModelManagement',
            params={'option': option},
            response_cls=ServerCacheResponse,
        )
