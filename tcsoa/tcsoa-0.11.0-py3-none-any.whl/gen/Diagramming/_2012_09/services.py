from __future__ import annotations

from tcsoa.gen.Diagramming._2012_09.DiagramManagement import CreateOrUpdateTemplateInputInfo1
from tcsoa.gen.Diagramming._2011_06.DiagramManagement import CreateOrUpdateTemplateResponse
from tcsoa.base import TcService


class DiagramManagementService(TcService):

    @classmethod
    def createOrUpdateTemplate(cls, inputData: CreateOrUpdateTemplateInputInfo1) -> CreateOrUpdateTemplateResponse:
        """
        This operation creates a Diagram Template which is used for creating diagrams for Teamcenter objects. A Diagram
        Template is nothing but a place holder for all the necessary information for creating a diagram. It holds the
        Application Domain which defines how Teamcenter objects will appear on the diagram, Transfer Mode used for
        traversing the given Teamcenter object, the Relation Rule used for finding out the relations between the
        objects to be shown on the diagram, the Stencil or Visio Template which has all the required shapes and the
        Property Map xml file which has the corresponding Teamcenter object mapping.  One can also specify if the
        interface shapes are to be hidden on the diagram created using this template. In such case, even if there are
        interface objects associated with the objects, they are not shown on the diagram.
        
        Use cases:
        Use case 1:
        You can create a diagram template which will be used for creating diagrams. You can provide all the necessary
        information like the Application Domain, the Transfer mode, the Relation Rule, the Stencil/template and the
        property map file and chose if the interface shapes are not to be shown on the diagram. Once user opts to hide
        the shapes, it cannot be modified.
        
        Use case 2: 
        You can select an existing template and edit it. The Description, the Relation Rule can be modified. 
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateTemplate',
            library='Diagramming',
            service_date='2012_09',
            service_name='DiagramManagement',
            params={'inputData': inputData},
            response_cls=CreateOrUpdateTemplateResponse,
        )
