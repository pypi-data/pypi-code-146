from __future__ import annotations

from tcsoa.gen.Core._2009_10.DataManagement import GetTablePropertiesResponse, GetItemFromAttributeResponse, TableInfo, GetItemFromAttributeInfo
from tcsoa.gen.Core._2007_01.DataManagement import GetItemFromIdPref
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.BusinessObjects import Table
from tcsoa.base import TcService
from tcsoa.gen.Core._2009_10.ProjectLevelSecurity import UserProjectsInfoResponse, UserProjectsInfoInput


class DataManagementService(TcService):

    @classmethod
    def getTableProperties(cls, table: List[Table]) -> GetTablePropertiesResponse:
        """
        This operation allows client applications to obtain the properties pertaining to one or more Table Business
        Objects. Client developers will need to pass in references to each Table that they need to query information
        on.  Note that the input vector needs to contain only references to the Teamcenter Table business object, this
        operation cannot be used to fetch properties of any other Business Objects.
        
        Use cases:
        This operation can be used by a client developer, when he/she deals with obtaining specific Table Business
        Object specific properties. Typically, Table Business Objects are not themselves visible in the Teamcenter
        workspace and appear as properties of other owning objects that are visible in the workspace.  The typical
        scenario in such cases is that a user attempts to obtain/view all properties of the the owning object, which
        may have one or more reference properties pointing to a Table.  A custom UI would need to display the Table
        related properties on the parent object in such cases and rendering these properties would require the client
        applications to obtain such information using the getTableProperties operation.
        One such example of existing usage of this operation, is the existing Teamcenter Rich Client functionality for
        viewing properties an Integer type of Parameter Definition [ ParmDefIntRevision Business Object ]. This
        Business Object and the functionality for viewing its properties are provided by the add on Calibration and
        Configuration Data Management module, through custom stylesheets which render a Table like UI for each
        referenced Table property.  At the time of rendering the UI, the client operations call the getTableProperties
        operation to obtain properties such as the number of rows, number of columns, labels for each row and column,
        the type of the cells and cell values and descriptions for each cell in the table.
        """
        return cls.execute_soa_method(
            method_name='getTableProperties',
            library='Core',
            service_date='2009_10',
            service_name='DataManagement',
            params={'table': table},
            response_cls=GetTablePropertiesResponse,
        )

    @classmethod
    def setTableProperties(cls, tableData: List[TableInfo]) -> ServiceData:
        """
        This operation allows client applications to set the properties pertaining to one or more Table business
        objects. Client developers will need to set information pertaining to the number of rows, columns, descriptions
        of each row and column, and cell information for each cell of the Table. The cell information must contain the
        type of cell, value to be placed in the cell, and optionally, a description of those values. The current
        operation only works on cells of specific types and it is mandatory that the type of the cells being set on the
        input structure corresponds to one of the cell types defined in the database schema viewable through the BMIDE.
        Supported valid types are:
        - TableCellInt
        - TableCellString
        - TableCellDouble
        - TableCellLogical
        - TableCellHex
        - TableCellSED
        - TableCellBCD
        - TableCellDate
        
        
        
        Use cases:
        This operation can be used by a client developer, when he/she deals with setting Table Business Object specific
        properties. Typically, Table Business Objects are not themselves visible in the Teamcenter workspace and appear
        as properties of other owning objects that are visible in the workspace. Modification to the owning objects,
        may involve changes to one or more of the Table properties that they reference through the Table.  In such
        cases, the setTableProperties is to be called, passing in the input structure which is setup to specify the
        modified values.
        One such example of existing usage of this operation, is the existing Teamcenter Rich Client functionality for
        modification of an Integer type of Parameter Definition [ ParmDefIntRevision Business Object ]. This Business
        Object and the functionality for its modification are provided by the add on Calibration and Configuration Data
        Management module.  During modification, of the integer parameter definition object, client code renders table
        like UI for each table property of the Parameter Definition, gathers the input values from the UI and populates
        a vector of the input structure of type TableInfo, sets the type of thecells to TableCellInt and makes the
        operation call. Client code will then parse the Service Data returned from the operation to obtain a handle to
        the updated Table Business Object. Errors, if any were encountered during the operation execution, are handled
        via the Service Data.
        """
        return cls.execute_soa_method(
            method_name='setTableProperties',
            library='Core',
            service_date='2009_10',
            service_name='DataManagement',
            params={'tableData': tableData},
            response_cls=ServiceData,
        )

    @classmethod
    def getItemFromAttribute(cls, infos: List[GetItemFromAttributeInfo], nRev: int, pref: GetItemFromIdPref) -> GetItemFromAttributeResponse:
        """
        This service retrieves Item and its related ItemRevision objects based on the supplied attribute key-value
        pairs supplied in the 'infos' list. All the key-value pairs except for the 'rev_id' key are used to create a
        query for Item objects.
        
        Once a set of Item objects have been retrieved, their ItemRevision objects are retrieved based on the following
        rules:
        - If  'nRev' is a negative value then all the ItemRevision objects are returned
        - If 'nRev' is a positive value then the 'nRev' most recent ItemRevision objects are returned. If 'nRev' is
        greater than the number of revisions then all of them are returned.
        - If 'nRev' is zero and a 'rev_id' attribute key was supplied in the attribute key-value pairs, then that
        ItemRevision object is returned.
        - If 'nRev' is zero and rev ids values were supplied in the 'GetItemFromAttributeInfo' object then all of the
        specified rev ids will be returned.
        
        """
        return cls.execute_soa_method(
            method_name='getItemFromAttribute',
            library='Core',
            service_date='2009_10',
            service_name='DataManagement',
            params={'infos': infos, 'nRev': nRev, 'pref': pref},
            response_cls=GetItemFromAttributeResponse,
        )


class ProjectLevelSecurityService(TcService):

    @classmethod
    def getUserProjects(cls, userProjectsInfoInputs: List[UserProjectsInfoInput]) -> UserProjectsInfoResponse:
        """
        This operation returns the list of  TC_Project objects for each of  the users in the input structure based on
        the additional criteria like active projects only, user privileged projects only and programs only. The output
        for this operation is a UserProjectsInfoResponse structure.
        """
        return cls.execute_soa_method(
            method_name='getUserProjects',
            library='Core',
            service_date='2009_10',
            service_name='ProjectLevelSecurity',
            params={'userProjectsInfoInputs': userProjectsInfoInputs},
            response_cls=UserProjectsInfoResponse,
        )
