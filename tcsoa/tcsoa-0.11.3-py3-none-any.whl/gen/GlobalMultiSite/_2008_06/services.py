from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TransferOptionSet
from tcsoa.gen.GlobalMultiSite._2008_06.ImportExport import ExportObjectsToOfflinePackageResponse, ImportObjectsFromOfflinePackageResponse
from typing import List
from tcsoa.gen.GlobalMultiSite._2007_06.ImportExport import NamesAndValue
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importObjectsFromOfflinePackage(cls, fmsTicket: str, optionSetTag: TransferOptionSet, optionNamesAndValues: List[NamesAndValue], sessionOptionAndValues: List[NamesAndValue]) -> ImportObjectsFromOfflinePackageResponse:
        """
        This operation imports the data of a briefcase into Teamcenter. A packed briefcase contains a TC XML file which
        holds a number of Teamcenter objects and related physical dataset files. After import, those objects will be
        replica in the importing site.
        
        Use cases:
        In data exchange, user may transfer a briefcase file from the source site to a remote site. In the importing
        site, user can use this operation to import the briefcase file into Teamcenter. After import, the objects held
        in the TC XML file will be created or updated if they have been imported before, physical dataset files will
        uploaded and attached to the related datasets.
        """
        return cls.execute_soa_method(
            method_name='importObjectsFromOfflinePackage',
            library='GlobalMultiSite',
            service_date='2008_06',
            service_name='ImportExport',
            params={'fmsTicket': fmsTicket, 'optionSetTag': optionSetTag, 'optionNamesAndValues': optionNamesAndValues, 'sessionOptionAndValues': sessionOptionAndValues},
            response_cls=ImportObjectsFromOfflinePackageResponse,
        )

    @classmethod
    def exportObjectsToOfflinePackage(cls, reason: str, sites: List[BusinessObject], objects: List[BusinessObject], optionSetTag: TransferOptionSet, optionNamesAndValues: List[NamesAndValue], sessionOptionAndValues: List[NamesAndValue]) -> ExportObjectsToOfflinePackageResponse:
        """
        Exports the objects to an offline package called briefcase. This operation returns a structure which includes
        the briefcase's FMS file ticket and exporter log file's FMS ticket. The briefcase ticket is used for
        downloading the briefcase file from the server to the client side by using FMS utility. Exporter log ticket is
        used for downloading the exporter log. 
        The briefcase is a package contains an exported TC XML file and a set of physical dataset files. The TC XML
        file holds the exported objects traversed by TC XML Export framework with the input TransferOptionSet and
        options, session options.
        Exporter log include the exporting status of the related objects. 
        
        
        Use cases:
        User can set a list of root objects, a destination site, a transfer option set, a list of traverse options and
        a list of session options. All the objects which can be traversed by the option set and options will be
        exported into an output TC XML file. The physical Iman files related exported dataset objects will be
        downloaded and packed into the briefcase file along with the TC XML file.
        """
        return cls.execute_soa_method(
            method_name='exportObjectsToOfflinePackage',
            library='GlobalMultiSite',
            service_date='2008_06',
            service_name='ImportExport',
            params={'reason': reason, 'sites': sites, 'objects': objects, 'optionSetTag': optionSetTag, 'optionNamesAndValues': optionNamesAndValues, 'sessionOptionAndValues': sessionOptionAndValues},
            response_cls=ExportObjectsToOfflinePackageResponse,
        )
