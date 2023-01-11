from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, StructureContext, CfgAttachmentLine
from tcsoa.gen.Manufacturing._2009_06.StructureManagement import GetAttachmentLineChildrenResponse, CreateOrUpdateAttachmentsData, GetBOMLineAttachmentsResponse, GetStructureContextActivityLinesResponse, GetStructureContextTopLinesResponse, GetBOMLineActivitiesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def getStructureContextActivityLines(cls, scs: List[StructureContext]) -> GetStructureContextActivityLinesResponse:
        """
        Given a vector of StructureContext objects, for each - get the activitylines that are attached to the SC by the
        relation - TC_SC_activities. Currently, this is only created during a population of WorkInstruction page by
        selecting an activity. The following properties are available to the client irrespective of policy:
        al_activity_object_name, al_activity_time
        """
        return cls.execute_soa_method(
            method_name='getStructureContextActivityLines',
            library='Manufacturing',
            service_date='2009_06',
            service_name='StructureManagement',
            params={'scs': scs},
            response_cls=GetStructureContextActivityLinesResponse,
        )

    @classmethod
    def getStructureContextTopLines(cls, scs: List[StructureContext]) -> GetStructureContextTopLinesResponse:
        """
        method to get the toplines of specified StructureContext. Client is responsible for closing any windows that
        are returned during this call. The following properties are available irrespective of policy:bl_line_name
        """
        return cls.execute_soa_method(
            method_name='getStructureContextTopLines',
            library='Manufacturing',
            service_date='2009_06',
            service_name='StructureManagement',
            params={'scs': scs},
            response_cls=GetStructureContextTopLinesResponse,
        )

    @classmethod
    def closeAttachmentWindow(cls, lines: List[BOMLine]) -> ServiceData:
        """
        close any attachment window that got created for the bomline during the soa session. This will only close the
        attachment windows that are created to support the attachment line soa calls.
        """
        return cls.execute_soa_method(
            method_name='closeAttachmentWindow',
            library='Manufacturing',
            service_date='2009_06',
            service_name='StructureManagement',
            params={'lines': lines},
            response_cls=ServiceData,
        )

    @classmethod
    def createOrUpdateAttachments(cls, attachments: List[CreateOrUpdateAttachmentsData]) -> ServiceData:
        """
        create or update attachments. The following properties are loaded automatically for the
        line:me_cl_object_name,me_cl_object_type,me_cl_object_desc and these for the workspaceobject:object_name,
        object_type, object_desc irrespective of policy files.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateAttachments',
            library='Manufacturing',
            service_date='2009_06',
            service_name='StructureManagement',
            params={'attachments': attachments},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteAttachments(cls, lines: List[CfgAttachmentLine]) -> ServiceData:
        """
        remove the specified attachment lines. Only if these lines have a parent is this action performed.
        """
        return cls.execute_soa_method(
            method_name='deleteAttachments',
            library='Manufacturing',
            service_date='2009_06',
            service_name='StructureManagement',
            params={'lines': lines},
            response_cls=ServiceData,
        )

    @classmethod
    def getAttachmentLineChildren(cls, attlines: List[CfgAttachmentLine]) -> GetAttachmentLineChildrenResponse:
        """
        given a vector of input attachmentlines - for each - get the immediate level of child attachment lines.
        For each attachment line the following properties are available on client side automatically:me_cl_object_name,
        me_cl_object_type, me_cl_object_desc
        """
        return cls.execute_soa_method(
            method_name='getAttachmentLineChildren',
            library='Manufacturing',
            service_date='2009_06',
            service_name='StructureManagement',
            params={'attlines': attlines},
            response_cls=GetAttachmentLineChildrenResponse,
        )

    @classmethod
    def getBOMLineActivities(cls, bomLines: List[BOMLine]) -> GetBOMLineActivitiesResponse:
        """
        given a bomline get it's activities (these activities are really the children of the root activity associated
        with the bomline). This assumes that the bomline is  a bopline. The following properties are available on
        client side for each line irrespective of policy: al_activity_object_name, al_activity_time. If the actual
        attachments of these activity lines are desired - use the getProperties method of DataManagementService with
        al_object as the property name.
        """
        return cls.execute_soa_method(
            method_name='getBOMLineActivities',
            library='Manufacturing',
            service_date='2009_06',
            service_name='StructureManagement',
            params={'bomLines': bomLines},
            response_cls=GetBOMLineActivitiesResponse,
        )

    @classmethod
    def getBOMLineAttachments(cls, bomlines: List[BOMLine], filter: List[str]) -> GetBOMLineAttachmentsResponse:
        """
        given a bomline get it's attachments. The follow properties are available on client side irrespective of
        policy: me_cl_object_name, me_cl_object_type, me_cl_object_desc
        """
        return cls.execute_soa_method(
            method_name='getBOMLineAttachments',
            library='Manufacturing',
            service_date='2009_06',
            service_name='StructureManagement',
            params={'bomlines': bomlines, 'filter': filter},
            response_cls=GetBOMLineAttachmentsResponse,
        )
