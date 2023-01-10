from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TransferMode, RevisionRule, ItemRevision
from tcsoa.gen.GlobalMultiSite._2010_04.ImportExport import ExportObjectsToPLMXMLResponse, ImportObjectsFromPLMXMLResponse
from typing import List
from tcsoa.gen.GlobalMultiSite._2007_12.ImportExport import NamesAndValues
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importObjectsFromPLMXML(cls, xmlFileTicket: str, namedRefFileTickets: List[str], transfermode: TransferMode, icRev: ItemRevision, sessionOptions: List[NamesAndValues]) -> ImportObjectsFromPLMXMLResponse:
        """
        The importObjectsFromPLMXML operation will import the objects from a PLMXML file. The XML file and the named
        reference files for datasets should be uploaded to transient volume before the calling of this operation. User
        can use getTransientFileTicketsForUpload operation from core.FileManagementService to generate the ticket and
        then call putFileViaTicket operation from soa.client.FileManagementUtility to perform the file upload to
        transient volume.
        
        Use cases:
        Use Case 1: Import PLMXML file to database
        You can import PLMXML file by specify:
        1)    The xml file that you want to import.
        2)    The related dataset file you want to import.
        3)    Transfer mode that you want to traverse to the xml.
        4)    The incremental change context.
        5)    Session options.
        
        
        Exceptions:
        >203474    will throw while the input file name is too long.
        Other PIE failure in the whole import process.
        """
        return cls.execute_soa_method(
            method_name='importObjectsFromPLMXML',
            library='GlobalMultiSite',
            service_date='2010_04',
            service_name='ImportExport',
            params={'xmlFileTicket': xmlFileTicket, 'namedRefFileTickets': namedRefFileTickets, 'transfermode': transfermode, 'icRev': icRev, 'sessionOptions': sessionOptions},
            response_cls=ImportObjectsFromPLMXMLResponse,
        )

    @classmethod
    def exportObjectsToPLMXML(cls, exportObjects: List[BusinessObject], transfermode: TransferMode, revRule: RevisionRule, languages: List[str], xmlFileName: str, sessionOptions: List[NamesAndValues]) -> ExportObjectsToPLMXMLResponse:
        """
        The 'exportObjectsToPLMXML' operation will generate a PLMXML file and a export log file for the input object
        list, transfer mode, revision rule and language set.
        
        Use cases:
        Use Case 1: Export object to PLMXML file
        You can export any business object by specify:
        1)    The objects that you want to exported.
        2)    Transfer mode and revision rule.
        3)    Languages that for localization value.
        4)    Xml file name.
        5)    Session options.
        
        
        Exceptions:
        >203331  will throw while all input objects is invalid objects.
        203447  will throw while fail to get download ticket from FMS.
        203486  will throw while the input XML file name contains full file path.
        Other PIE failure in the whole export process.
        """
        return cls.execute_soa_method(
            method_name='exportObjectsToPLMXML',
            library='GlobalMultiSite',
            service_date='2010_04',
            service_name='ImportExport',
            params={'exportObjects': exportObjects, 'transfermode': transfermode, 'revRule': revRule, 'languages': languages, 'xmlFileName': xmlFileName, 'sessionOptions': sessionOptions},
            response_cls=ExportObjectsToPLMXMLResponse,
        )
