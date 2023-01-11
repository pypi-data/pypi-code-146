from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Visualization._2010_09.DataManagement import FindProductViewForNodesResultRespose, GatherSnapshot3DInput, NewSnapshot3DInput, Snapshot3DInfoResponse, Snapshot3DUpdateResponse, Snapshot3DUpdateStructureFilesResponse, FindNodesInProductViewResultResponse, GatherSnapshot3DListResponse, CreateSnapshot3DResponse, Snapshot3DInfoInput, SearchCriteria, Snapshot3DUpdateInput, Snapshot3DStructureFilesInput
from tcsoa.gen.Internal.Visualization._2010_09.StructureManagement import CreateVisSCInfo, CreateVisSCResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getSnapshot3DInfo(cls, snapshot3DInputList: List[Snapshot3DInfoInput]) -> Snapshot3DInfoResponse:
        """
        This service is used by the visualization integrations in order to gather the information needed to open a
        Product View Dataset and apply it to recreate a 3D scene.  The service gets individual SnapshotViewData Dataset
        information for a list of Product View Datasets of interest including all the named reference file information,
        all the objects related to the Dataset by GRM or named reference, and all the visible lines.  This information
        is used by the viewer to open up the appropriate structure, expand the structure and load the visible lines for
        the Product View, and recreate the 3D scene by applying the viewFile PLMXML.
        
        The client needs to first find the SnapshotViewData Dataset, so the tag can be added to the
        'Snapshot3DInfoInput'.  One or more SnapshotViewData Dataset tags can be added to the vector to get information
        on many Product Views. If more than one Dataset tag is used, it is important to use unique 'clientId' strings
        in the input since they are used as keys in the return output map. If the same 'clientId' string is used,
        information will be lost.
        
        The related objects are used to identify the top line of the structure (e.g. VisTopLevelRef), and to get the
        configuration of the structure to open (e.g. VisStructureContext object).
        
        The visible lines are used to expand the structure and load the appropriate occurrences in order to recreate
        the 3D scene.  This consists of an array of clone stable UIDs or absolute occurrence UIDs depending on the
        version of the Product View model.  The output data will indicate the visible line type in the
        'Snapshot3DVisibleLines' using the uidtype. If the type is a clone stable UID chain, this is a / delimited
        string that represents a path from the root of the structure to the visible line of interest. This list will be
        obtained by processing the structure PLMXML file.
        
        The file information provides the core files that need to be opened by the viewer (e.g. the viewFile PLMXML
        and/or the structure file PLMXML).  The viewFile is used to recreate the 3D scene, and the structure file can
        be used to open the static structure for the Product View to recreate the exact same scene that was saved
        originally.
        
        Use cases:
        This service helps provide the viewer with information to load Product View Datasets.  There are 3 main use
        cases for loading Product Views, each described in more detail below.
        
        Load Product View:
        - In this case the static structure for the visible lines and their descendants is loaded from the Product View
        data model via the structure PLMXML file.  This returns the Product View to the exact as saved state.
        - Load dynamic Product View using stored configuration rules. In this case the structure configuration
        information stored in the Product View data model that represents the configuration of the structure when the
        Product View was saved is used to reconfigure the latest structure with the same configuration rules before the
        scene is recreated.
        - Load dynamic Product View using current configuration rules. In this case the current BOM window
        configuration established in the Structure Manager (SM), Multi Structure Manager (MSM), or Manufacturing
        Process Planner (MPP) application is the structure used to apply the Product View on.
        
        
        
        Load static Product View:
        - User selects one or more Product View objects (SnapShotViewData Datasets) in My Teamcenter and sends those to
        open in visualization.
        - The visualization client gets the list of Datasets to open, builds up the 'Snapshot3DInfoInput' structure for
        each Dataset, and calls the 'getSnapshot3DInfo' operation for the Product Views.
        - The system reads the data model and returns the visible lines list, the named references, and related
        objects.  
        - The viewer downloads the files of interest from the Dataset (e.g. structure PLMXML file, viewFile PLMXML, vpl
        markup layers).  
        - The viewer loads the structure PLMXML file, loads the markup layers (vpl files), and then merges in the
        viewFile PLMXML to recreate the 3D scene.
        
        
        
        Load dynamic Product View using stored configuration rules:
        - User selects one or more Product View objects (SnapShotViewData Datasets) in My Teamcenter and sends those to
        open in visualization.
        - The visualization client gets the list of Datasets to open, builds up the 'Snapshot3DInfoInput' structure for
        each Dataset, and calls the 'getSnapshot3DInfo' operation for the Product Views.
        - The system reads the data model and returns the visible lines list, the named references, and related
        objects.  
        - The viewer downloads the files of interest from the Dataset (structure PLMXML file, viewFile PLMXML, vpl
        markup layers).  
        - The viewer uses the related objects information to get the top line and the configuration information for the
        structure via the VisStructureContext object, and calls the 'createBOMsFromRecipes' operation to configure the
        structure properly.
        - The viewer uses the visible line information to expand the BOM structure and fetch BOMLines.  If clone stable
        occurrence id chains are the type of visible lines returned, the Viewer starts at the top of the structure and
        uses the 'expandPSOneLevel' operation to expand the structure and load it.  If the absolute occurrences are the
        type of visible lines returned or the preference to prune the structure during Product View load is active, the
        viewer uses the 'expandPSFromOccurrenceList' operation to expand the structure and fetch the visible BOMLines.
        - Once the configured structure is loaded and expanded, the viewer loads the markup layers (vpl files), and
        then merges in the viewFile PLMXML to recreate the 3D scene.
        
        
        
        Load dynamic Product View using current configuration rules:
        - User sends a structure to Structure Manager (SM), Multi Structure Manager (MSM), or Manufacturing Process
        Planner (MPP) and configures the structure with revision rules, variant rules, effectivity, etc
        - The user brings up the Product View gallery and finds Product Views of interest (which will eventually invoke
        the 'gatherSnapshot3DList' operation). 
        - The user selects some Product Views and sends those to visualization.  For standalone visualization the
        VisStructureContext sent with the launch file is used to configure the BOMWindow to the current configuration
        from the launching application.  For embedded visualization, the current BOMWindow configuration is used.
        - The visualization client gets the list of Datasets to open, builds up the 'Snapshot3DInfoInput' structure for
        each Dataset, and calls the 'getSnapshot3DInfo' operation for the Product Views.
        - The system reads the data model and returns the visible lines list, the named references, and related
        objects.  
        - The viewer downloads the files of interest from the Dataset (structure PLMXML file, viewFile PLMXML, vpl
        markup layers).  
        - The viewer uses the visible line information to expand the BOM structure and fetch BOMLines if they are not
        already loaded.  If clone stable occurrence ID chains are the type of visible lines returned, the Viewer starts
        at the top of the structure and uses the 'expandPSOneLevel' operation to expand the structure and load it.  If
        the absolute occurrences are the type of visible lines returned or the preference to prune the structure during
        Product View load is active, the viewer uses the 'expandPSFromOccurrenceList' operation to expand the structure
        and fetch the visible BOMLines.
        - Once the configured structure is loaded and expanded, the viewer loads the markup layers (vpl files), and
        then merges in the viewFile PLMXML to recreate the 3D scene.
        
        """
        return cls.execute_soa_method(
            method_name='getSnapshot3DInfo',
            library='Internal-Visualization',
            service_date='2010_09',
            service_name='DataManagement',
            params={'snapshot3DInputList': snapshot3DInputList},
            response_cls=Snapshot3DInfoResponse,
        )

    @classmethod
    def updateSnapshot3D(cls, snapshot3DUpdateInputList: List[Snapshot3DUpdateInput]) -> Snapshot3DUpdateResponse:
        """
        This service updates the Product View data model (or portions of it if desired) consisting of a
        SnapShotViewData Dataset and associated files and relationships.   The call is bulk based and can thus update
        multiple Datasets at a time.  Inputs include the list of Datasets to update and for each Dataset the
        'attachToBOMLine' (A reference to BOMLine to which snapshot Dataset is to be attached), a Boolean
        'createStructureFile' that controls whether or not to create the structure PLMXML file, a Boolean
        'updateVisibleLinesList' along with a 'visibleLinesList' structure used to force the visible line list to be
        updated for Product Views, and the 'namedRefFileInfoList' containing all the file information for the named
        references that are to be uploaded as part of the update.
        
        This service can be used in three different ways:
        
        - Complete update operation. 
        - In conjunction with 'createSnapshot3D' to optimize the performance of initial Product View creation.
        - In conjunction with 'updateSnapshot3DStructureFiles' to optimize performance for Product View updates.
        
        
        
        Use cases:
        Complete update operation:
        - User selects one or more Product View Datasets in Teamcenter and sends those to open in visualization.
        - The visualization client calls the 'getSnapshot3DInfo' service with product view Dataset object as input
        reads the model and returns the visible lines list, the named references, and related objects.  The viewer then
        opens the appropriate product structure, configures it, and applies the Product View by loading the view file
        to recreate the 3D scene.
        - The user modifies the 3D scene by editing / removing / adding markup layers, changing visibility, adjusting
        material settings and colors, repositioning parts, and other common functions supported by Teamcenter
        visualization. 
        - User checks out the Dataset and then invokes the Product View update action in the viewer.
        - Client gathers the list of visible BOMLines for the 3D scene (if changed).
        - Client gathers the attach to BOMLine as the save location for the Product View (if changed).
        - Client exports the Product View files locally that capture the view state data: a viewFile (*.plmxml), a
        thumbnail image (*.jpg, *.cgm), 0..n markup layers (*.vpl) optional, a preview image (*.*) optional, and a 3D
        Geometry Asset file (asset) optional.  From these files and knowledge of the model, the client builds up the
        namedRefFileInfoList for the SnapShotViewData Dataset needed for uploading the files.
        - Client calls the 'updateSnapshot3D' operation and passes the following as input (for each Product View to
        update): snapshot3DDataset tag, 'attachToBOMLine' if changed, 'createStructureFile' = True,
        'updateVisibleLinesList' = False, 'namedRefFileInfoList' containing all the updated files information.
        - Teamcenter/Server updates the complete Product View data model based on the inputs and creates a new version
        of the SnapShotViewData Dataset.  The complete model is updated per the inputs of this call which may end up
        deleting old files that were attached to the previous version but not specified for this version.
        
        
        
        In conjunction with createSnapshot3D:
        - Client application with visualization capabilities loads a Product Structure and visualizes 3D geometry from
        Teamcenter.  
        - The Client application creates a 3D scene by creating markup layers, adjusting material settings and colors,
        repositioning parts, setting visibility, and other common functions supported by Teamcenter visualization
        applications.
        - Client gathers the list of visible BOMLines for the 3D scene
        - Client gathers the attach to BOMLine as the save location for the Product View
        - Client gathers Dataset info (name, description, etc) from the user
        - Client starts a separate thread that will invoke the 'createSnapshot3D' service and passes the
        'attachToBOMLine', 'datasetInfo', 'visibleLinesList', and True for generating the structure PLMXML file on the
        server.  Client does not pass the files to be uploaded in the Dataset (i.e. the name reference information is
        left out).
        - Teamcenter/Server creates partial (incomplete) Product View data model consisting of a SnapShotViewData
        Dataset, a reference to the top line of the structure, the structure configuration (VisStructureContext), and a
        structure (PLMXML) file.  The core files attached required by the data model (viewFile PLMXML and thumbnail
        image) as well as optional files not yet attached.
        - Client concurrently exports the following files locally that capture the view data: a viewFile (*.plmxml), a
        thumbnail image (*.jpg, *.cgm), 0..n markup layers (*.vpl) optional, a preview image (*.*) optional, and a 3D
        Geometry Asset file (asset) optional.  From these files and knowledge of the model, the client builds up the
        'namedRefFileInfoList' needed for uploading the files.
        - Client calls the 'updateSnapshot3D' operation to upload all the files that attach to the SnapShotViewData
        Dataset and passes the Dataset object UID to update, the BOMLine to attach the Dataset to (if different from
        where attached currently), 'createStructureFile' Boolean set to False (since it was created during the
        'createSnapshot3D' call), 'updateVisibleLinesList' Boolean set to False, 'namedRefFileInfoList' containing all
        the file information for the uploaded files.
        - Teamcenter/Server creates the complete Product View data model.
        
        
        
        In conjunction with updateSnapshot3DStructureFiles:
        - User selects one or more Product View objects in Teamcenter and sends those to open in visualization.
        - The visualization client calls the 'getSnapshot3DInfo' operation for the Product Views, which reads the model
        and returns the visible lines list, the named references, and related objects.  The viewer then opens the
        appropriate product structure, configures it, and applies the Product View by loading the viewFile to recreate
        the 3D scene.
        - The user modifies the 3D scene by editing / removing / adding markup layers, changing visibility, adjusting
        material settings and colors, repositioning parts, and other common functions supported by Teamcenter
        visualization. 
        - User checks out the Dataset and invokes the Product View update action in the viewer.
        - Client gathers the list of visible BOMLines for the 3D scene (if changed).
        - Client gathers the attach to BOMLine as the save location for the Product View (if changed).
        - Client starts a separate thread that will invoke the 'updateSnapshot3DStructureFiles' operation and passes
        the SnapShotViewData Dataset and the visible lines.  This function exports a new structure PLMXML file and
        attaches the new file to the new Dataset version.   
        - Concurrently with the 'updateSnapshot3DStructureFiles' operation, the client exports the Product View files
        locally that capture the view state data: a viewFile (*.plmxml), a thumbnail image (*.jpg, *.cgm), 0..n markup
        layers (*.vpl) <optional>, a preview image (*.*) optional, and a 3D Geometry Asset file (asset) optional . 
        From these files and knowledge of the model, the client builds up the 'namedRefFileInfoList' for the
        SnapShotViewData Dataset needed for uploading the files.
        - Client calls the 'updateSnapshot3D' operation and passes the following as input (for each Product View to
        update): 'snapshot3DDataset' tag, 'attachToBOMLine' if changed, 'createStructureFile' = False,
        'updateVisibleLinesList' = False, 'namedRefFileInfoList' containing all the updated files information.
        - Teamcenter/Server updates the SnapShotViewData Dataset based on the inputs by creating a new version of the
        Dataset.  The complete model is updated per the inputs of this call which may end up deleting old files that
        were attached to the previous version but not specified for this version.
        
        """
        return cls.execute_soa_method(
            method_name='updateSnapshot3D',
            library='Internal-Visualization',
            service_date='2010_09',
            service_name='DataManagement',
            params={'snapshot3DUpdateInputList': snapshot3DUpdateInputList},
            response_cls=Snapshot3DUpdateResponse,
        )

    @classmethod
    def updateSnapshot3DStructureFiles(cls, snapshot3DStructureFilesInput: List[Snapshot3DStructureFilesInput]) -> Snapshot3DUpdateStructureFilesResponse:
        """
        This operation updates the 3D structure files within the set of existing Product Views (SnapShotViewData
        datasets) specified.  The structure PLMXML file is exported based on the structure configuration obtained from
        the visible BOMLine list specified in the input, and it contains only the visible lines and their descendants. 
        The structure PLMXML file is created based on the ExportProductView transfer mode.  The VisStructureContext
        object attached to the model is also updated if needed to match the configuration specified by the input
        bomlines.  
        
        The Product View data model (SnapShotViewData dataset) requires a structure PLMXML file export of all the
        visible lines and their descendents.  Structure PLMXML file generation is expensive from a performance
        perspective.  This service is provided as a means for clients to optimize performance for Product View model
        update by running this operation concurrently with other client operations such as exporting files from the
        viewer.  Leveraging concurrency speeds up the overall update process for Product Views.  
        
        This service can also be leveraged for batch update of the structure PLMXML files for product views for use
        cases where Product Views can be updated offline by some utility if desired.  
        
        
        Use cases:
        There are two main use cases where this service is utilized: 1) Optimized update operation, and 2) Offline
        batch update of product views.  The first use case is an optimization done for performance reasons.  Structure
        PLMXML file generation can be time consuming, thus doing this concurrently with other time consuming operations
        such as viewer file export operations can reduce the overall Product View save times.  The batch update use
        case is done when the structure upon which the Product View is based has been updated, and there is a group of
        product views that needs to be updated due to this structure change.  In this case the service is utilized by
        some utility program that is updating product views in some way.
        
        Optimized update operation:
        - User selects one or more Product View objects in Teamcenter and sends those to open in visualization.
        - The visualization client calls 'getSnapshot3DInfo' for the Product Views, which reads the model and returns
        the visible lines list, the named references, and related objects.  The viewer then opens the appropriate
        product structure, configures it, and applies the Product View by loading the viewFile to recreate the 3D scene.
        - The user modifies the 3D scene by editing / removing / adding markup layers, changing visibility, adjusting
        material settings and colors, repositioning parts, and other common functions supported by Teamcenter
        visualization. 
        - User invokes the Product View update action in the viewer.
        - Client gathers the list of visible bomlines for the 3D scene (if changed).
        - Client gathers the attach to BomLine as the save location for the Product View (if changed).
        - Client starts a separate thread that will invoke the 'updateSnapshot3DStructureFiles' operation and passes
        the SnapShotViewData dataset and the visible lines.  This function exports a new structure PLMXML file and
        uploads the new file to the snapshot dataset.   
        - Concurrently with the 'updateSnapshot3DStructureFiles' operation call, the client exports the Product View
        files locally that capture the view state data: a viewFile (*.plmxml), a thumbnail image (*.jpg, *.cgm), 0..n
        markup layers (*.vpl) optional, a preview image (*.*) optional, and a 3D Geometry Asset file (asset) optional .
         From these files and knowledge of the model, the client builds up the 'namedRefFileInfoList' for the
        SnapShotViewData dataset needed for uploading the files.
        - Client calls the 'updateSnapshot3D' operation and passes the following as input (for each Product View to
        update): 'snapshot3DDataset' tag, 'attachToBOMLine' if changed, 'createStructureFile' = False,
        'updateVisibleLinesList' = False, 'namedRefFileInfoList' containing all the updated files information.
        - Teamcenter/Server updates the SnapShotViewData Dataset based on the inputs. The complete model is updated per
        the inputs of this call which may end up deleting old files.
        
        
        
        Batch update operation:
        - Some process is conducted that determines the structure upon which a Product View is based has been modified
        in some way that affects the product view display.
        - The structure is opened and configured per some external input.
        - The Product Views attached to this structure are determined.
        - For each Product View, the model for the Product View is interrogated, and the visible line list retrieved
        using the 'getSnapshot3DInfo' operation.
        - BomLines are expanded for the visible line list by using something like the 'expandPSFromOccurrenceList'
        operation.
        - The 'snapshot3DStructureFilesInput' structure is built containing the SnapShotViewData Dataset and the
        visible line list for this Dataset.
        - Steps 4 through 6 are repeated for all Product Views to update.
        - The 'updateSnapshot3DStructureFiles' operation call is made.
        - The system updates the structure PLMXML files for each SnapShotViewData Dataset specified on the input.
        
        """
        return cls.execute_soa_method(
            method_name='updateSnapshot3DStructureFiles',
            library='Internal-Visualization',
            service_date='2010_09',
            service_name='DataManagement',
            params={'snapshot3DStructureFilesInput': snapshot3DStructureFilesInput},
            response_cls=Snapshot3DUpdateStructureFilesResponse,
        )

    @classmethod
    def createSnapshot3D(cls, newSnapshot3DInputList: List[NewSnapshot3DInput]) -> CreateSnapshot3DResponse:
        """
        This operation creates the Product View data model (or portions of it if desired) consisting of a
        SnapShotViewData Dataset and associated files and relationships A live BOMWindow must be configured for the
        loaded structure with BOMLines expanded for all the visible lines to be captured in the product view.  These
        visible lines along with a BOMLine where user wishes to attach the Dataset is to be sent as input to the
        operation. Product view Dataset creation information (name and description) should be sent as input to the
        operation as well. Two files are ultimately required by the data model (a viewFile (PLMXML) file, and a
        thumbnail image (jpg, cgm)).  Several optional files can also be specified (a preview image (*.*), motion
        (vfm), markup layers (vpl), and 3D Geometry Asset image (asset)).  These files can first be exported prior to
        calling this service, and the entire model will be created by this service.
        
        The server implementation of this operation will create the structure (PLMXML) file that represents an export
        of the structure for all visible lines and their descendants if specified.  However, creation of the structure
        (PLMXML) file can be very costly from a performance perspective.  As a result, the service has been set up so
        that the caller can initiate this call early in the save process just to create the basics of the model
        including export of structure file before gathering the required files from the viewer (i.e. Thumbnail (jpg,
        cgm), ViewFile (PLMXML), and the optional files) and uploading them.  If this approach is used, the viewer
        files must be saved later using the 'UpdateSnapshot3D' operation.  The operation is set up to handle both
        approaches.
        
        The server implementation of this service creates a VisStructureContext object (or objects) representing the
        configuration of the loaded structure based on the BOPWindow or BOMWindow specified via the BOMLines passed for
        the visible lines. This object is capable of storing configuration information for Product and Process
        structures, including composition structures.  This allows clients to reopen a Product View with the exact same
        structure configuration that was in effect when the Product View was created for all the structure types
        supported by the BVR model.
        
        The service returns the map between client IDs and created Dataset objects which may or may not have all the
        necessary files attached depending on the calling implementation.
        
        Use cases:
        This operation is for clients that have loaded a 3D structure from Teamcenter with a live connection to a
        BOMWindow on the server, with live references to BOMLines within that structure representing the visible lines
        and attach to location.  The visible lines will be recorded as the occurrences that must be loaded to restore
        the Product View, and the attach to location will be the ItemRevision (pointed to by BOMLine) where the user
        wants the Product View stored attached. A new VisTopLevelRef relation is also created between new snapshot
        Dataset and BOMView corresponding to loaded structure.
        
        There are two basic use cases for calling this method: 
        - Create complete model. 
        - Create partial model, upload files later.
        
        
        
        Create complete model:
        - Client application with visualization capabilities loads a Product Structure and visualizes 3D geometry from
        Teamcenter.  
        - The Client application creates a 3D scene by creating markup layers, adjusting material settings and colors,
        temporary repositioning parts, setting visibility, and other common functions supported by Teamcenter
        visualization applications.
        - Client gathers the list of visible BOMLines for the 3D scene.
        - Client gathers the attach to BOMLine as the save location for the Product View.
        - Client gathers Dataset info (name, description, etc) from the user.
        - Client exports the following files locally that capture the view data: a viewFile (*.plmxml), a thumbnail
        image (*.jpg, *.cgm), 0..n markup layers (*.vpl) <optional>, a preview image (*.*) <optional>, and a 3D
        Geometry Asset file (asset) <optional> .  From these files and knowledge of the model, the client builds up the
        named reference information for the SnapShotViewData Dataset needed for uploading the files.
        - Client calls 'createSnapshot3D' operation and passes a reference to BOMLine to which snapshot Dataset is to
        be attached, datasetInfo, visibleLinesList, named reference information, and a Boolean true for generating the
        structure PLMXML file on the server.
        - Teamcenter/Server creates the complete Product View data model per the configuration of the BOPWindow or
        BOMWindow and the inputs.
        
        
        
        Create partial model, upload files later:
        - Client application with visualization capabilities loads a Product Structure and visualizes 3D geometry from
        Teamcenter.  
        - Client application creates a 3D scene by creating markup layers, adjusting material settings and colors,
        repositioning parts, setting visibility, and other common functions supported by Teamcenter visualization
        applications.
        - Client gathers the list of visible BOMLines for the 3D scene.
        - Client gathers the attach to BOMLine as the save location for the Product View.
        - Client gathers Dataset info (name, description, etc) from the user.
        - Client starts a separate thread that will invoke the 'createSnapshot3D' service and passes the
        'attachToBOMLine', 'datasetInfo', 'visibleLinesList', and a Boolean true for generating the structure PLMXML
        file on the server.  Client does NOT pass the files that attach to the Dataset (i.e. the named reference
        information is left out).
        - Teamcenter/Server creates partial (incomplete) Product View data model consisting of a SnapShotViewData
        Dataset, a reference to the top line of the structure, the structure configuration (VisStructureContext), and a
        structure (PLMXML) file.  The core files required by the data model (viewFile PLMXML and thumbnail image) as
        well as optional files are not yet attached.
        - Client concurrently exports the following files locally that capture the view data: a viewFile (*.plmxml), a
        thumbnail image (*.jpg, *.cgm), 0..n markup layers (*.vpl) <optional>, a preview image (*.*) <optional>, and a
        3D Geometry Asset file (asset) <optional> .  From these files and knowledge of the model, the client builds up
        the named reference information for the SnapShotViewData Dataset needed for uploading the files.
        - Client calls the 'updateSnapshot3D' operation to upload all the files that attach to the SnapShotViewData
        Dataset
        - System creates the complete Product View data model.
        
        """
        return cls.execute_soa_method(
            method_name='createSnapshot3D',
            library='Internal-Visualization',
            service_date='2010_09',
            service_name='DataManagement',
            params={'newSnapshot3DInputList': newSnapshot3DInputList},
            response_cls=CreateSnapshot3DResponse,
        )

    @classmethod
    def findProductViewsForNodes(cls, searchCriteria: List[SearchCriteria]) -> FindProductViewForNodesResultRespose:
        """
        Find all product views within the specified scope and returns the product views and the nodes present in the
        product view out of the input nodes.
        """
        return cls.execute_soa_method(
            method_name='findProductViewsForNodes',
            library='Internal-Visualization',
            service_date='2010_09',
            service_name='DataManagement',
            params={'searchCriteria': searchCriteria},
            response_cls=FindProductViewForNodesResultRespose,
        )

    @classmethod
    def gatherSnapshot3DList(cls, input: List[GatherSnapshot3DInput]) -> GatherSnapshot3DListResponse:
        """
        THIS OPERATION IS DEFINED FOR FUTURE USE AND HAS NOT BEEN IMPLEMENTED.
        
        This operation is intended for population of the Product View Gallery with Product Views, displayed as
        thumbnails.  The operation returns only enough information to populate the Product View Gallery (but no more)
        to ensure gallery performance is good.  The input is a list of BOMLines where the SnapshotViewData may be
        attached and GRM relation to be followed to gather snapshots.  The return is a list of SnapshotViewData
        Datasets mapped to the BOMLines sent along with their thumbnail and preview (optional) images as IMANFile
        objects.  This allows the caller to retrieve the files for thumbnail and preview image display without further
        server interaction.  
        
        The gather behavior can be tailored by the client by adjusting the input arguments that specify which type of
        GRM relations to traverse for the specific bomlines passed.  For example, if the VisTopLevelRef is specified
        along with the top bomline and no other criteria, all the SnapshotViewData Datasets captured in the top line
        context will be found, regardless of where they are attached.  However, if IMAN_3D_snap_shot and VisTopLevelRef
        are specified, then it will filter the results and only return the SnapshotViewData Datasets attached to the
        top line.
        
        
        Use cases:
        The primary use case for this service is to implement the logic for displaying Product Views in the Product
        View Gallery behind a single service operation so that all clients can benefit from the same basic business
        logic.  
        
        The logic can be summarized as follows:
        - Get the list of Product Views from attachments panel (Attachments Window) for the selected line.
        - If nothing is returned from the attachments window, get the Product Views related to the selected item
        revision via an IMAN_3D_snap_shot relationship.
        - Filter out the product views that do not have the VisTopLevelRef reference that matches the top line BOMView
        (ensure the top level context matches so the occurrence references resolve).
        
        
        
        The Product View Gallery population use case for this service is a follows:
        
        Product View Gallery population:
        - User sends a structure to Structure Manager (SM), Multi Structure Manager (MSM), or Manufacturing Process
        Planner (MPP), configures the structure, and may do some level of structure expansion.
        - User turns on the Product View gallery to find a list of Product Views to display
        - Client gathers the top BOMLine, and optionally gathers additional BOMLines depending on the desired filtering
        criteria.  Most typically, the top BOMLine and reference type VisTopLevelRef are specified as the inputs to the
        service if it is desired to find all Product Views for this top level context.  However, if selected BOMLines
        and the reference type IMAN_3D_snap_shot are sent, the return is further filtered to only provide those
        snapshots attached to the selected bomline.  The system builds up the 'GatherSnapshot3DInput' structure with
        this filtering information.
        - Client calls the 'gatherSnapshot3DList' operation which then finds all the Product Views that match the
        filter criteria along with their thumbnail and preview images and returns them to the caller.  
        - Teamcenter/Server downloads the thumbnail images from the Teamcenter File Management System (FMS) for the
        gallery display
        - Client updates the gallery after getting the output from the service to include the returned Product Views.
        
        """
        return cls.execute_soa_method(
            method_name='gatherSnapshot3DList',
            library='Internal-Visualization',
            service_date='2010_09',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GatherSnapshot3DListResponse,
        )

    @classmethod
    def getNodesPresentInProductView(cls, searchScope: List[BusinessObject], productView: BusinessObject, nodesToSearch: List[BusinessObject]) -> FindNodesInProductViewResultResponse:
        """
        This function returns the nodes present in the given product view. This SOA will be called once the PVs are
        updated and to show the nodes (out of the input node list) present in the PV.
        """
        return cls.execute_soa_method(
            method_name='getNodesPresentInProductView',
            library='Internal-Visualization',
            service_date='2010_09',
            service_name='DataManagement',
            params={'searchScope': searchScope, 'productView': productView, 'nodesToSearch': nodesToSearch},
            response_cls=FindNodesInProductViewResultResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def createVisSC(cls, info: List[CreateVisSCInfo]) -> CreateVisSCResponse:
        """
        This operation takes a list of ConfigurationContext/top line object pairs and creates a VisStructureContext
        object based on that input. The user may optionally supply a list of occurrences in the form of UID chains and
        a file reference for the static PLMXML representation of the configuration. If an occurrence list or a static
        structure file are supplied they will be set as properties on the VisStructureContext object. The list of
        occurrences can be used to populate/expand any BOMWindows that are subsequently created using the output
        VisStructureContext object (e.g. see 'expandPSFromOccurrenceList').
        
        Use cases:
        When the user desires to create a single persistent object that records a particular configuration recipe and
        the caller already has the component objects that make up the configuration. This case might occur if the
        configuration elements of a BOMWindow were captured but the BOMWindow was then deleted. This is often the case
        when using the Teamcenter Thin Client.
        
        The 'createVisSC' operation requires input configuration objects and their top lines. Therefore, these objects
        must have been obtained based on some previous configuration scenario.
        """
        return cls.execute_soa_method(
            method_name='createVisSC',
            library='Internal-Visualization',
            service_date='2010_09',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=CreateVisSCResponse,
        )
