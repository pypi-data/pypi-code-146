from __future__ import annotations

from tcsoa.gen.Diagramming._2011_06.DiagramManagement import CreateDiagramInputInfo, GetDiagramMembersResponse, OpenDiagramInputInfo, SaveDiagramInputInfo, OpenDiagramResponse, SaveDiagramResponse, GetDiagramMembersInputInfo, CreateOrUpdateTemplateInputInfo, CreateDiagramResponse, CreateOrUpdateTemplateResponse
from typing import List
from tcsoa.base import TcService


class DiagramManagementService(TcService):

    @classmethod
    def openDiagram(cls, inputData: List[OpenDiagramInputInfo]) -> OpenDiagramResponse:
        """
        This operation opens a Visio Diagram created for a Teamcenter object (WorkspaceObject/ Item Revision/ Folder/
        BOMLine). The objects and relations shown on the diagram are gathered by executing the Transfer Mode and
        Relation Rule specified on the diagram template. Relation Rule specifies the relations to be shown between the
        objects.
        Only those objects appear on the diagram for which there is a Visio Shape in the stencil and there is mapping
        defined between the Shape and the Teamcenter object in the mapping xml file. Mapping file has details about how
        to define the mappings.
        If the contents of the root object of the diagram are changed, for instance, a BOM structure changes or the
        contents of the folder are modified, then the diagram will show only the current information. This is because
        every time a diagram is opened, Transfer mode and Relation Rules are applied.
        
        Use cases:
        You can select a Teamcenter object and launch the open diagram dialog which shows the list of all diagrams
        created for that object. You can select a diagram to open. A Visio diagram is opened on the RAC. The content of
        the diagram is decided by the Transfer mode and the Relation Rule.
        """
        return cls.execute_soa_method(
            method_name='openDiagram',
            library='Diagramming',
            service_date='2011_06',
            service_name='DiagramManagement',
            params={'inputData': inputData},
            response_cls=OpenDiagramResponse,
        )

    @classmethod
    def saveDiagram(cls, inputData: List[SaveDiagramInputInfo]) -> SaveDiagramResponse:
        """
        This operation saves Visio Diagram(s) created for a Teamcenter object (WorkspaceObject/ Item Revision/ Folder/
        BOMLine). When a Visio diagram is saved, a skeleton file (.vdx) is created and stored as a dataset to hold all
        the non Teamcenter information, like notes if any. A preview image of the diagram content is also stored as an
        image data set. These Dataset objects are attached to the diagram object.
        For the Teamcenter business objects appearing on the diagram, Fnd0ShapeRelation objects are created with the
        diagram object to hold the position information so that the shapes appear in their original position and format
        next time the diagram is opened.
        
        Use cases:
        You can create or open an existing diagram and make changes to it. You can then save the diagram.
        """
        return cls.execute_soa_method(
            method_name='saveDiagram',
            library='Diagramming',
            service_date='2011_06',
            service_name='DiagramManagement',
            params={'inputData': inputData},
            response_cls=SaveDiagramResponse,
        )

    @classmethod
    def createDiagram(cls, inputData: List[CreateDiagramInputInfo]) -> CreateDiagramResponse:
        """
        This operation creates a Visio Diagram for a Teamcenter object (WorkspaceObject/ ItemRevision/ Folder/ BOMLine)
        using a Diagram Template. The objects and relations shown on the diagram are gathered by executing the Transfer
        Mode and Relation Rule specified on the diagram template. Relation Rule specifies the relations to be shown
        between the objects.
        Only those objects appear on the diagram for which there is a Visio Shape in the stencil and there is mapping
        defined between the Shape and the Teamcenter object in the mapping xml file. Mapping file has details about how
        to define the mappings.
        While creating a diagram, if user selects the "Open Diagram" option, the diagram object is created on the
        server and all the necessary information is returned in the response which is utilized to open the Visio
        diagram. If user does not select the option, then just the diagram object is created.
        
        
        Use cases:
        You can select a Teamcenter object in RAC and create a Visio diagram for the same by selecting a Diagram Domain
        and a Diagram Template.
        """
        return cls.execute_soa_method(
            method_name='createDiagram',
            library='Diagramming',
            service_date='2011_06',
            service_name='DiagramManagement',
            params={'inputData': inputData},
            response_cls=CreateDiagramResponse,
        )

    @classmethod
    def createOrUpdateTemplate(cls, inputData: CreateOrUpdateTemplateInputInfo) -> CreateOrUpdateTemplateResponse:
        """
        createOrUpdateTemplate provides the ability to either create a new diagram template or modify an existing
        diagram template.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateTemplate',
            library='Diagramming',
            service_date='2011_06',
            service_name='DiagramManagement',
            params={'inputData': inputData},
            response_cls=CreateOrUpdateTemplateResponse,
        )

    @classmethod
    def getDiagramMembers(cls, inputData: List[GetDiagramMembersInputInfo]) -> GetDiagramMembersResponse:
        """
        This operation retrieves the specific types of members of the diagram based on its membership types. Following
        are the types of members apart from the ones that appear on the diagram as a result of transfer mode traversal
        and relationship rules. 
        - User Added - The objects which are added to the diagram by the user. E.g. an Item object which is copied from
        Teamcenter and then pasted on to the diagram.
        - User Omitted - The objects which are deleted by the user from the diagram. E.g. user can remove an object
        from the diagram only. The object is removed from the diagram and not from database. It can be retrieved and
        again shown on the diagram.
        
        
        
        Use cases:
        None.
        """
        return cls.execute_soa_method(
            method_name='getDiagramMembers',
            library='Diagramming',
            service_date='2011_06',
            service_name='DiagramManagement',
            params={'inputData': inputData},
            response_cls=GetDiagramMembersResponse,
        )
