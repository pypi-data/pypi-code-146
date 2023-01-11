from __future__ import annotations

from tcsoa.gen.Internal.Visualization._2010_09.DataManagement import CreateSnapshot3DResponse
from typing import List
from tcsoa.gen.Internal.Visualization._2012_10.DataManagement import NewSnapshot3DInput
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createSnapshot3D(cls, input: List[NewSnapshot3DInput]) -> CreateSnapshot3DResponse:
        """
        This operation creates the Product View data model (or portions of it if desired) consisting of a
        SnapShotViewData Dataset and associated files and relationships.  The visible lines along with a BusinessObject
        where the Dataset is to be attached are sent as input to the operation. Product view Dataset creation
        information (name and description) should be sent as input to the operation as well. Two files are ultimately
        required by the data model (a viewFile (PLMXML) file, and a thumbnail image (jpg, cgm)).  Several optional
        files can also be specified (a preview image (*.*), motion (vfm), markup layers (vpl), and 3D Geometry Asset
        image (asset)).  These files can first be exported prior to calling this service, and the entire model will be
        created by this service.
        
        The server implementation of this operation will create the structure (PLMXML) file that represents an export
        of the structure for all visible lines and their descendants if specified.  However, creation of the structure
        (PLMXML) file can be very costly from a performance perspective.  As a result, the service has been set up so
        that the caller can initiate this call early in the save process just to create the basics of the model
        including export of structure file before gathering the required files from the viewer (i.e. Thumbnail (jpg,
        cgm), ViewFile (PLMXML), and the optional files) and uploading them.  If this approach is used, the viewer
        files must be saved later using the UpdateSnapshot3D operation.  The operation is set up to handle both
        approaches.
        
        In the case the input visible lines are BOMLines, the server implementation of this service creates a
        VisStructureContext object (or objects) representing the configuration of the loaded structure based on the
        BOPWindow or BOMWindow specified via the BOMLines passed for the visible lines. This object is capable of
        storing configuration information for Product and Process structures, including composition structures.  This
        allows clients to reopen a Product View with the exact same structure configuration that was in effect when the
        Product View was created for all the structure types supported by the BVR model.
        
        The service returns the map between client IDs and created Dataset objects which may or may not have all the
        necessary files attached depending on the calling implementation.
        
        Use cases:
        This operation is for clients that have loaded a 3D structure from Teamcenter in the
        Active Workspace 3D Viewer. The 'attach to' location is the object where the Product view stored is to be
        attached.'
        
        Currently there is one basic use case for calling this method:
        
        - Create dataset with view PLMXML, thumbnail and high resolution only, for Active Workspace View Captures.
        
        
        
        View Capture Generation:
        
        
        - Client application with visualization capabilities loads a Product structure and visualizes 3D geometry from
        Teamcenter.
        - Client gathers the list of visible Business Objects for the 3D scene.
        - Client gathers the attach to Object as the save location for the Product View.
        - Client gathers Dataset info (name, description, etc) from the user.
        - Client exports the following files locally that capture the view data: a viewFile (*.plmxml), a thumbnail
        image (*.jpg, *.cgm), and a preview image (*.*).  
        - From these files and knowledge of the model, the client build up the named reference information for the
        SnapShotViewData Dataset needed for uploading the files.
        - Client calls createSnapshot3D operation and passes a reference to Object to which snapshot Dataset is to be
        attached, relation to use (View Capture), datasetInfo, visibleLinesList, and named reference information
        - Teamcenter/Server creates the complete Product View data model per the inputs.
        
        """
        return cls.execute_soa_method(
            method_name='createSnapshot3D',
            library='Internal-Visualization',
            service_date='2012_10',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateSnapshot3DResponse,
        )
