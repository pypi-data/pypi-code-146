from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2016_04.DataManagement import GetInitialTableRowDataResponse, GetStyleSheetResponse, LoadDataForEditingResponse, GetStyleSheetIn, SaveEditAndSubmitInfo, LoadDataForEditingInfo
from typing import List
from tcsoa.gen.Internal.AWS2._2012_10.DataManagement import SaveEditAndSubmitResponse
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getStyleSheet(cls, processEntireXRT: bool, input: List[GetStyleSheetIn]) -> GetStyleSheetResponse:
        """
        This operation returns the stylesheets and the required data to present that stylesheet for each input object.
        
        Use cases:
        Use Case 1: Open an object in ActiveWorkspace.
        When an object is selected in ActiveWorkspace, the user may choose to invoke the open operation. When that
        operation is executed the getStylesheet call is invoked and the Stylesheet is processed in order to display the
        data to the user.
        
        Use Case 2: List view with Summary
        When an object is selected in the ActiveWorkspace navigator, when in list view with summary mode, the
        getStyleSheet SOA operation is invoked, and the returned data is parsed/processed in order to present the data
        to the user in the Summary panel.
        
        Use Case 3: Show Object Info
        When an object is selected in ActiveWorkspace, a user may choose the "Show Object Info" command.  When
        executed, a panel slides out from the right hand side of the application, and the selected objects data is
        presented.  In order to populate the panel, the getStylesheet call is invoked and the returned data is parsed
        and processed in order to build the UI.
        """
        return cls.execute_soa_method(
            method_name='getStyleSheet',
            library='Internal-AWS2',
            service_date='2016_04',
            service_name='DataManagement',
            params={'processEntireXRT': processEntireXRT, 'input': input},
            response_cls=GetStyleSheetResponse,
        )

    @classmethod
    def loadDataForEditing(cls, inputs: List[LoadDataForEditingInfo]) -> LoadDataForEditingResponse:
        """
        This SOA method ensures that the properties can be edited, and returns the last save date of the related
        objects for optimistic edit
        """
        return cls.execute_soa_method(
            method_name='loadDataForEditing',
            library='Internal-AWS2',
            service_date='2016_04',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=LoadDataForEditingResponse,
        )

    @classmethod
    def saveEditAndSubmitToWorkflow(cls, inputs: List[SaveEditAndSubmitInfo]) -> SaveEditAndSubmitResponse:
        """
        This operation saves the modified properties for the given input objects and submits the objects to a workflow.
        The workflow is submitted only if all of the save operations are successful. If the save fails for a single
        object  none of  the input objects will be submitted to a workflow.
        
        Use cases:
        User can modify the object(s) properties and submit the object(s) to workflow in one operation. This operation
        first saves the modified properties and then initiates the workflow process for all input objects.
        """
        return cls.execute_soa_method(
            method_name='saveEditAndSubmitToWorkflow',
            library='Internal-AWS2',
            service_date='2016_04',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SaveEditAndSubmitResponse,
        )

    @classmethod
    def getInitialTableRowData(cls, owningObject: BusinessObject, tablePropertyName: str) -> GetInitialTableRowDataResponse:
        """
        This operation returns the proposed values to act as initial values when a new row object needs to be added to
        the table. User can then do further modification as needed, and perform save operation to create the row object
        in the database.
        
        Use cases:
        When user clicks on the add button for table property, client can add a temporary row showing some of the
        system generated properties populated. Property value generation will honor related LOVs, naming rules, default
        values etc. The newly added row should behave as if user has added a new row. User can then perform save to
        make the row persist in the database.
        
        Exceptions:
        >141156  An error has occurred while creating initial row values of type tablePropertyName. Please refer to the
        Teamcenter server syslog file for more information.
        """
        return cls.execute_soa_method(
            method_name='getInitialTableRowData',
            library='Internal-AWS2',
            service_date='2016_04',
            service_name='DataManagement',
            params={'owningObject': owningObject, 'tablePropertyName': tablePropertyName},
            response_cls=GetInitialTableRowDataResponse,
        )
