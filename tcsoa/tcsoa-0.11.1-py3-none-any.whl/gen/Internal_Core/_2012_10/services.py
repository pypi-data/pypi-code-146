from __future__ import annotations

from tcsoa.gen.Internal.Core._2012_10.DataManagement import CreateResponse2, CreateIn2
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createRelateAndSubmitObjects(cls, inputs: List[CreateIn2]) -> CreateResponse2:
        """
        This is a generic operation for creation of business objects. This will also create any secondary (compounded)
        objects that need to be created, assuming the CreateInput2 for the secondary object is represented in the
        recursive CreateInput2 object. e.g. Item is primary object that also creates Item Master and ItemRevision.
        ItemRevision in turn creates ItemRevision Master. The input for all these levels is passed in through the
        recursive CreateInput2 object.
        
        This operation also performs following tasks:
        - Relate the created business object and the additional data passed in through the dataToBeRelated input of
        CreateIn2 object.
        - Submit the created business object to the workflow process. The input for creating the workflow process is
        passed in through the workflowData input of CreateIn2 object.
        - Relate the created business object to the input target object.
        
        
        
        Use cases:
        Use this operation to create an object after obtaining user input on the fields of the create dialog. This call
        is typically preceded by a call to Teamcenter::Soa::Core::_2008_06::PropDescriptor::getCreateDesc or to the
        Client Meta Model layer to retrieve Create Descriptor for a business object.
        
        Create Item
        For example, to create an Item, client will get the Create Descriptor associated with the Item from the client
        Meta model (The associated descriptor type can be found by looking at the constant value for the CreateInput
        constant that is attached to Item). Alternatively, for clients that do not use the client Meta model, the
        Descriptor for Item can be obtained by invoking getCreateDesc operation. The descriptor information can then be
        used to populate the Create dialog for the business object. Once the Create dialog is populated the
        createObjects operation can be called to create the object.
        
        Create Problem Report
        User want to create a new Problem Report (Change) object and attach an existing Word doc dataset as "Reference"
        or "ProblemItem" relation. Here User also wants to submit the created Problem Report object to the workflow
        with predefined Workflow template for Problem Report object type.
        """
        return cls.execute_soa_method(
            method_name='createRelateAndSubmitObjects',
            library='Internal-Core',
            service_date='2012_10',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=CreateResponse2,
        )
