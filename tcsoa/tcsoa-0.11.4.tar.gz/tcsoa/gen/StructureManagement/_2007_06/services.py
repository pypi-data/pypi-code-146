from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.gen.StructureManagement._2007_06.PublishByLink import PublishDataInfo, SourceAndTargets, LineAndWindow, CompletenessCheckInputData, FindTargetsResponse, PublishLinkInfo, LogicallyEquivalentLinesResponse, PublishLinksResponse, GetSourceTopLevelResponse, CompletenessCheckResponse, FindSourceResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class PublishByLinkService(TcService):

    @classmethod
    def getSourceTopLevel(cls, targets: List[BOMLine]) -> GetSourceTopLevelResponse:
        """
        Finds source of PublishLink for given target BOMLine. For the source of the PublishLink finds context PSBOMView.
        
        Use cases:
        Find context PSBOMView for the source of PublishLink.
        """
        return cls.execute_soa_method(
            method_name='getSourceTopLevel',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'targets': targets},
            response_cls=GetSourceTopLevelResponse,
        )

    @classmethod
    def completenessCheck(cls, input: List[CompletenessCheckInputData]) -> CompletenessCheckResponse:
        """
        Recursively evaluates completeness for BOMLine objects having underlying component as Part.  A BOMLine which
        requires positioned designed is marked as complete if underlying PartRevision has primary representation OR
        BOMLine has source associated via PublishLink object. If a BOMLine does not need positioned designed then such
        BOMLine is marked as complete as well. This operation also supports recursively clearing completeness results.
        
        If required the BOM is expanded internally. In case of packed BOMLines, if any of the BOMLine is incomplete
        then that packed line is marked as incomplete.
        
        
        Use cases:
        - Recursively perform completeness check for Part structure.
        - Recursively clears completeness check for Part structure.
        
        """
        return cls.execute_soa_method(
            method_name='completenessCheck',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'input': input},
            response_cls=CompletenessCheckResponse,
        )

    @classmethod
    def publishData(cls, publishDataInfos: List[PublishDataInfo]) -> PublishLinksResponse:
        """
        Copies 'Absolute Transformation Matrix' and/or JT from source BOMLine to target BOMLine objects. If a
        PublishLink does not exist for source and target then a new PublishLink is created with input dataFlags. In
        case if PublishLink already exists then dataFlags of the PublishLink object is updated.
        
        Input 'dataFlags' is used to determine which data has to be copied. Unless context was explicitly set - the
        data on target BOMLines is stored in-context of top BOMLine of the target BOMWindow. 
        
        The DirectModel Dataset is attached with Rendering relation. If the target BOMLine is an assembly then PLMXML
        file is created based on RevisionRule of the source BOMWindow and attached to target BOMLine as Text Dataset
        with Rendering relation. In case, in-context Dataset with Rendering relation already exists then that is
        replaced with the new one. The BOMWindow is saved after attaching the Dataset.
        
        Below validations are performed during operation and failures are reported in 'ServiceData'.
        
        - 'dataFlags' contains a valid value.
        - Target BOMLine requires positioned design.
        - Item type of source and target BOMLine as per PUBLISH_AlignableSourceTypes and PUBLISH_AlignableTargetTypes
        preference respectively.
        - Type name is a valid TCType name.
        - PSBOMView of the source is local.
        - No PublishLink exists other than source and target as in input.
        
        
        
        Use cases:
        Perform in-context association between occurrences of two structures and copy 'Absolute Transformation Matrix'
        and/or JT from source to target BOMLine objects.
        """
        return cls.execute_soa_method(
            method_name='publishData',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'publishDataInfos': publishDataInfos},
            response_cls=PublishLinksResponse,
        )

    @classmethod
    def createLinks(cls, linkInfos: List[PublishLinkInfo]) -> PublishLinksResponse:
        """
        Creates PublishLink between AbsOccurrenceViewQualifier of source and target BOMLines. The 'dataFlags' attribute
        of the PublishLink is set to 0 as no data was published. The operation also saves new PublishLink object. 
        
        Following validations are performed during operation and failures are reported in 'ServiceData'.
        
        - Item type of source and target BOMLine as per PUBLISH_AlignableSourceTypes and PUBLISH_AlignableTargetTypes
        preference respectively.
        - Type name is a valid TCType name.
        - PSBOMView of the source is local.
        - No PublishLink exists with source as input source.
        - No PublishLink exists with target as input target.
        
        
        
        Use cases:
        Perform in-context association between occurrences of two structures.
        """
        return cls.execute_soa_method(
            method_name='createLinks',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'linkInfos': linkInfos},
            response_cls=PublishLinksResponse,
        )

    @classmethod
    def addTargets(cls, input: List[SourceAndTargets]) -> PublishLinksResponse:
        """
        Adds AbsOccViewQualifier of target BOMLine objects to the existing PublishLink of input source BOMLine. The
        operation also saves updated PublishLink. 
        
        Following validations are performed during operation and failures are reported in 'ServiceData'.
        
        - PublishLink exists with source as input source and user has access to it.
        - Item type of source and target BOMLine as per PUBLISH_AlignableSourceTypes and PUBLISH_AlignableTargetTypes
        preference respectively.
        - No PublishLink exists with target as input target.
        - Logical identity of all target BOMLine is same.
        - Logical identity of source and target BOMLines is same.
        
        
        
        Use cases:
        Add in-context occurrence as target to an existing PublishLink for given source.
        """
        return cls.execute_soa_method(
            method_name='addTargets',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'input': input},
            response_cls=PublishLinksResponse,
        )

    @classmethod
    def deleteLinkForSource(cls, sources: List[BOMLine]) -> ServiceData:
        """
        Finds and deletes PublishLink for input source BOMLine objects.
        
        Use cases:
        Delete PublishLink.
        """
        return cls.execute_soa_method(
            method_name='deleteLinkForSource',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'sources': sources},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteTargetsFromLink(cls, targets: List[BOMLine]) -> ServiceData:
        """
        Deletes AbsOccViewQualifier of target BOMLines from the existing PublishLink.  If the target being removed is
        the last one for PublishLink then PublishLink is also deleted. Otherwise operation saves updated PublishLink.
        
        Following validations are performed during operation.
        
        PublishLink exists whose target as input
        
        
        Use cases:
        Detach target BOMLine from PublishLink.
        """
        return cls.execute_soa_method(
            method_name='deleteTargetsFromLink',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'targets': targets},
            response_cls=ServiceData,
        )

    @classmethod
    def findLinesWithSameLogicalIdentity(cls, input: List[LineAndWindow]) -> LogicallyEquivalentLinesResponse:
        """
        Finds logically equivalent BOMLines in BOMWindow for list of input BOMLines.
        
        BOMLines are said to be identical if their AbsoluteOccurrence objects have same 'Usage Address' and 'Positioned
        Designator'.
        
        Use cases:
        Find equivalent BOMLine objects and associate them.
        """
        return cls.execute_soa_method(
            method_name='findLinesWithSameLogicalIdentity',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'input': input},
            response_cls=LogicallyEquivalentLinesResponse,
        )

    @classmethod
    def findSourceInWindow(cls, input: List[LineAndWindow]) -> FindSourceResponse:
        """
        Finds source of the PublishLink in source BOMWindow for input target BOMLine objects. Source is returned as
        BOMLine.
        
        
        Use cases:
        Determine if BOMWindow has source for input target BOMLine objects.
        """
        return cls.execute_soa_method(
            method_name='findSourceInWindow',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'input': input},
            response_cls=FindSourceResponse,
        )

    @classmethod
    def findTargetsInWindow(cls, input: List[LineAndWindow]) -> FindTargetsResponse:
        """
        Finds target of the PublishLink in target BOMWindow for input source BOMLine objects. Targets are returned as
        BOMLine objects.
        
        Use cases:
        - Determine if BOMWindow has targets for input source BOMLine.
        - Find targets for source of PublishLink and subsequently use found target BOMLine objects to delete links.
        
        """
        return cls.execute_soa_method(
            method_name='findTargetsInWindow',
            library='StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'input': input},
            response_cls=FindTargetsResponse,
        )
