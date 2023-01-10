from __future__ import annotations

from tcsoa.gen.GlobalMultiSite._2011_06.ImportExport import CreateGSIdentitiesResponse, GetHashedUIDResponse, TIEGSIdentityInput
from typing import List
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def createGSIdentities(cls, gsIdVect: List[TIEGSIdentityInput]) -> CreateGSIdentitiesResponse:
        """
        This operation takes array of GSIdentityInput structure as input and creates GSIdentity objects in Teamcenter.
        This operation allows for creation of GSIdentities in bulk which is required for GMS co-existence scenarios
        following bulk load import of legacy data into Teamcenter.Whenever an object is exported from a source site the
        record of each imported object is stored in GSIdentity object,which has some basic information of the site that
        owns the object,the type of the class of imported object and 14 digit Unique Identifier string (UID)
        represtening the object.Every imported object will have a corresponding entry in GSIdentity object.This entry
        will be used later during a re-import or sychronize operations internally by importer module.
        
        Use cases:
        This operation is used by user to create GSIds for objects imported by bulk loader.It creates GSIds for non
        GSId based TcXML objects.
        """
        return cls.execute_soa_method(
            method_name='createGSIdentities',
            library='GlobalMultiSite',
            service_date='2011_06',
            service_name='ImportExport',
            params={'gsIdVect': gsIdVect},
            response_cls=CreateGSIdentitiesResponse,
        )

    @classmethod
    def getHashedUID(cls, ownSiteId: int, hashKey: str) -> GetHashedUIDResponse:
        """
        This operation takes a hash key as input and generates a valid Teamcenter Unique Identifier  a 14 character
        long unique string UID based on it. For migrating data from legacy systems to Teamcenter using bulk load import
        of TC XML, this operation can be used to generate UIDs for legacy objects. The UID is composed by using Fowler
        Noll Vo (FNV) hash algorithm for an arbitrary and unique input string.
        
        Use cases:
        This is used during data migration between legacy system such as Enterpise to Teamcenter .
        Used by the importer to generate a UID.
        """
        return cls.execute_soa_method(
            method_name='getHashedUID',
            library='GlobalMultiSite',
            service_date='2011_06',
            service_name='ImportExport',
            params={'ownSiteId': ownSiteId, 'hashKey': hashKey},
            response_cls=GetHashedUIDResponse,
        )
