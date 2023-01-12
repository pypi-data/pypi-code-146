from __future__ import annotations

from typing import List
from tcsoa.gen.DocumentManagement._2011_06.AttributeExchange import ResolveAttrMappingsAndSetPropertiesResponse, ResolveAttrMappingsAndGetPropertiesResponse, ResolveAttrMappingsAndGetPropertiesInfo, ResolveAttrMappingsAndSetPropertiesInfo
from tcsoa.base import TcService


class AttributeExchangeService(TcService):

    @classmethod
    def resolveAttrMappingsAndGetProperties(cls, info: List[ResolveAttrMappingsAndGetPropertiesInfo]) -> ResolveAttrMappingsAndGetPropertiesResponse:
        """
        This operation processes the metadata exchange mapping information between the client application and
        Teamcenter from the provided input list of ResolveAttrMappingsAndGetPropertiesInfo structure (containing the
        metadata exchange mapping information from the client application).  The operation then gets and returns the
        property  values of the corresponding Teamcenter object from provided input information.
        
        Use cases:
        Metadata exchange between Teamcenter and Microsoft Office Word application
        From the Teamcenter client for Microsoft Office Word 2010, a user opens and checks out a WordX Dataset.  User
        then clicks on the Teamcenter ribbon and clicks on Attribute Exchange> Configurations> Create.  From here user
        can set up the metadata exchange between the properties of the Microsoft Office Word file properties and the
        properties of the Teamcenter object.  
        
        In the configuration, user can set the direction of the metadata exchange either as File to Teamcenter,
        Teamcenter to File, or Two Way.  In this case, user selects Teamcenter to File for the metadata exchange from
        the client to Teamcenter.  User sets up the property mapping by selecting a file property (Comments for
        example) and selecting a Teamcenter object property (object_desc for example), and saves the attribute exchange
        configuration.  User then clicks on Attribute Exchange>Reload button.  The Microsoft Office Word initiates this
        operation and gets Teamcenter object property (object_desc for example) value back.  To verify the client file
        property gets updated, from Microsoft Office Word menu File, select Info (in the left panel), then select
        Properties (in the right panel), then select Show Document Panel.
        """
        return cls.execute_soa_method(
            method_name='resolveAttrMappingsAndGetProperties',
            library='DocumentManagement',
            service_date='2011_06',
            service_name='AttributeExchange',
            params={'info': info},
            response_cls=ResolveAttrMappingsAndGetPropertiesResponse,
        )

    @classmethod
    def resolveAttrMappingsAndSetProperties(cls, info: List[ResolveAttrMappingsAndSetPropertiesInfo]) -> ResolveAttrMappingsAndSetPropertiesResponse:
        """
        This operation processes the metadata exchange mapping information between the client and Teamcenter from the
        provided input list of ResolveAttrMappingsAndSetPropertiesInfo structure (containing the metadata exchange
        mapping information from the client application).  The operation sets the Teamcenter property values based on
        the provided input information.
        
        
        Use cases:
        Metadata exchange between Teamcenter and Microsoft Office Word application
        
        From the Teamcenter client for Microsoft Office Word 2010, a user opens and checks out a WordX Dataset.  User
        then clicks on the Teamcenter ribbon and clicks on Attribute Exchange >Configurations>Create.  From here user
        can set up the metadata exchange between the properties of the Microsoft Office Word file and the properties of
        the Teamcenter object.  
        
        In the configuration, user can set the direction of the metadata exchange either as File to Teamcenter,
        Teamcenter to File, or Two Way.  In this case, user selects File to Teamcenter for the metadata exchange, pick
        a file property (Comment for example), pick a Teamcenter object property (object_desc for example), and save
        the attribute exchange configuration.  From Microsoft Office Word menu File, select Info (left panel), then
        select Properties (right panel)>Show Document Panel.  Update the Comments text box in the Document Properties
        Panel with some text.  Now select Teamcenter ribbon and click on Save.  Save and check in the Dataset.  During
        this process, the Microsoft Office Word initiates this operation and updates Teamcenter object property
        (object_desc for example) value.  User can verify the Teamcenter object property (object_desc for example) by
        login to a Teamcenter client such as Rich Application Client (RAC), do a View properties on the Teamcenter
        object.
        """
        return cls.execute_soa_method(
            method_name='resolveAttrMappingsAndSetProperties',
            library='DocumentManagement',
            service_date='2011_06',
            service_name='AttributeExchange',
            params={'info': info},
            response_cls=ResolveAttrMappingsAndSetPropertiesResponse,
        )
