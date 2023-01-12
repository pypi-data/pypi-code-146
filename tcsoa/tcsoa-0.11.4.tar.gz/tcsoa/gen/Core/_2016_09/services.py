from __future__ import annotations

from tcsoa.gen.Core._2016_09.DataManagement import CreateAttachResponse
from tcsoa.gen.Core._2015_07.DataManagement import CreateIn2
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createAttachAndSubmitObjects(cls, inputs: List[CreateIn2]) -> CreateAttachResponse:
        """
        This is a generic operation for creation of business objects. This will also create any secondary (compound)
        objects that need to be created, assuming the CreateInput2 for the secondary object is represented in the
        nested CreateInput2 object. e.g. Item is primary object that also creates an  Item Master and ItemRevision.
        ItemRevision in turn creates ItemRevision Master. The input for all these levels is passed in through the
        recursive CreateInput2 object.
        
        This operation also performs following tasks:
        - A list of file names can be passed in through the dataToBeRelated input of the CreateIn2 input object, and
        Dataset objects for the files will be created and related to the created business object. The information
        needed to subsequently upload the file contents will be passed back to the user in the CreateAttachResponse
        object.
        - Submit the created business object to a workflow process. The input for creating the workflow process is
        passed in through the workflowData input of CreateIn2 object. 
        - Relate the created business object to the input target object.
        - If the created business object is under Item Revision Definition Configuration (IRDC) control, proposed file
        attachments are first evaluated against the object's IRDC settings to check if they are valid or not. Invalid
        files will be discarded. If the created business object is not under IRDC control, the files will simply be
        related to the created business object as Dataset objects.
        - Proposed file attachments to the created business object are specified as file names rather than unique ids
        of existing business objects. Empty Dataset objects are created and write tickets are fetched for the files
        that will be uploaded as named references.
        
        
        
        Use cases:
        Use Case 1: Create an Item object under IRDC control.
        
        The user wants to create and Item and its associated objects, and furthermore will set some of the create
        inputs so that the newly created object will be under Item Revision Definition Configuration (IRDC) control. No
        files or workflow inputs are provided.
        
        Use Case 2: Create an Item object under IRDC control and submit it to a workflow.
        
        As with Use Case 1, but the name of a workflow template is provided. After the Item object is created, it will
        be submitted to the specified workflow.
        
        Use Case 2: Create an Item object under IRDC control, attach files, and submit it to a workflow.
        
        As with Use Case 2, but a list of file names is provided. After the Item object is created, one Dataset object
        will be created for each file name and related to the ItemRevision. File tickets will be passed back to the
        user in the CreateAttachResponse object so that the files can be uploaded to the Dataset objects' named
        references. Then the newly created Item is submitted to the specified workflow.
        """
        return cls.execute_soa_method(
            method_name='createAttachAndSubmitObjects',
            library='Core',
            service_date='2016_09',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=CreateAttachResponse,
        )
