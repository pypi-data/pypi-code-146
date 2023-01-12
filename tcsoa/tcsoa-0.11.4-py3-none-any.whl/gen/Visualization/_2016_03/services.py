from __future__ import annotations

from typing import List
from tcsoa.gen.Visualization._2016_03.DataManagement import MetaDataStampOutputResponse, MetaDataStampInputInfo
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getMetaDataStampWithContext(cls, metaDataStampInfos: List[MetaDataStampInputInfo]) -> MetaDataStampOutputResponse:
        """
        This operation retrieves metadata stamp files for Teamcenter objects based on the context within which these
        objects are being displayed.  For example, when a user prints a model view, the stamp will vary based on the
        context within which this model view is printed.  Printing the model view in owning model context provides one
        stamp, while printing the same view from within a disclosure context produces another stamp.
        
        The metadata stamp is generated based on the list of objects and the context of those objects using the
        metaDataStampInfos list. The transient ticket for the generated *.mds file is returned. The ticket can then be
        used to retrieve the file using a FMS method like FccProxy::downloadFiles. 
        
        The Teamcenter default implementation uses a Metadatastamp template containing an MDS file with Teamcenter
        property names and default values. The Teamcenter site preference MetaDataStamp_template is used to find the
        item where the template files is stored. This file is processed and each Attribute specified will be replaced
        with the matching object property values if found. The output mds file will be written to the transient volume
        and the transient ticket of the file is sent to client in the response data. The customization hook provided
        with this interface may wish to use the same template mds file as a starting point.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes).
        
        Use cases:
        This method is called by visualization when integrating with Teamcenter for printing objects like
        Fnd0ModelViewProxy and SnaphotViewData datasets that are loaded into some higher level product context. The
        user loads a configured product structure, or some high level object that sets context in Teamcenter. Within
        this structure or context, the user finds objects they wish to print, and invokes a print action, The stamping
        context is the higher level context within which the stamping metadata is retrieved from (e.g. the root node of
        the product structure), and the stamped objects are the individual objects that are to be printed (e.g. model
        views or product Views). Stamp files (tickets) are returned to the caller, and these files are used by
        visualization to place metadata markings on views printed. The stamp file represents a metadata stamp overlay
        on top of the printed image and often contains control information for printed detailed design data.
        
        The MDS file created by this service can also be used by the VisView Convert and Print utilities.
        
        This service may also be useful for customizations that leverage Siemens Embedded visualization toolkits, and
        thus it is a public service.
        """
        return cls.execute_soa_method(
            method_name='getMetaDataStampWithContext',
            library='Visualization',
            service_date='2016_03',
            service_name='DataManagement',
            params={'metaDataStampInfos': metaDataStampInfos},
            response_cls=MetaDataStampOutputResponse,
        )
