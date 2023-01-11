from __future__ import annotations

from tcsoa.gen.Internal.Mmv._2012_09.SpatialStructureManagement import GetNodeBBoxIn, GetNodeBBoxResponse, AcquireSpatialHierarchyResponse, CreateMmvCursorResponse, IsSpatialHierarchyIn, GetSpatialCellsReadTicketsResponse, SearchScope, AcquireSpatialHierarchyIn, ReleaseSpatialHierarchyIn, SpatialHierCellInfo, IsSpatialHierarchyLatestResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SpatialStructureManagementService(TcService):

    @classmethod
    def getSpatialCellsReadTickets(cls, input: SpatialHierCellInfo) -> GetSpatialCellsReadTicketsResponse:
        """
        This is the primary method used during rendering via MMV technology.  The visualization client traverses a
        spatial hierarchy (.mmv file) downloaded from the server that contains an array of cells, and submits
        individual cells that it expects to be visible to the server for configuration and resolution into occurrences
        by calling this service.  The JT part and transformation information from the occurrences is returned and then
        loaded and rendered by the client.  This operation is called continuously during the VGR rendering process.  As
        the actual geometry is loaded the visibility occlusion is refined and more 'GetSpatialCellsReadTickets' calls
        are made, but the amount of cells decreases over time along with the service calls as the scene stabilizes. 
        This rendering approach is referred to as Visibility Guided Rendering (VGR), where a spatial hierarchy is used
        to determine which geometry is visible for a given visibility request.
        This service depends on first running the MMV index harvester process to create the Fnd0SpatialHierarchy
        dataset and populate the MMV occurrence tables on the server.  The dataset contains an .mmv file that
        represents the spatial hierarchy the viewer loads and traverses during rendering.  The database tables contain
        a mapping between the cells of the spatial hierarchy and the occurrences in the structure that was harvested. 
        The harvested structure can be unconfigured, or partially configured.  Thus the spatial hierarchy can represent
        an unconfigured or partially configured model.  This method basically takes a list of cells to be rendered by
        the client, looks up their corresponding occurrences in Teamcenter, configures BOMLines for the occurrences
        referenced by these cells applying the appropriate configuration rules of the current BOMWindow, and returns
        these occurrences to the client along with the JT file information.  The basic idea is to only configure the
        occurrences that are visible, thus reducing overall work and time required to render the large model.
        This operation gets the information of configured occurrences that are located in an array of cells.  In
        addition to the cell information, this operation also takes as input one or more cursor objects that are
        created with the 'createMMVCursor' service.  The cursors contain the visibility scopes to be applied when
        configuring these cells.  The visibility scope refers to a set of occurrences (parts or assemblies) within
        which visible geometry is to be displayed.  Providing the visibility scope to the server enables the client to
        render a specific subassembly directly from the spatial hierarchy (.mmv file) without first knowing the
        occurrences within that subassembly.  The client renders from the spatial hierarchy regardless if the entire
        model or a specific subset of the model is being set visible.  During rendering, the server will only return
        occurrences from the 'GetSpatialCellsReadTickets' calls that are contained within the visibility scoping set
        specified by the client.  If the client wishes to set the entire model visible, the scoping set is left blank. 
        If the client is to render a specific subassembly, the scoping set is the occurrence thread path of the
        specific subassembly.
        Any combination of cursor objects in the input cursor array can be applied on each cell, and this combination
        is represented by a 32 bit signed integer for this cell.  Each bit in the 32 bit integer, except the highest
        sign bit, indicates whether or not the corresponding cursor in the cursor array is enabled for the cell.  For
        example, integration value of 0x0003 would indicate that the first and second cursor in the input cursor array
        is enabled.  At most 31 cursor objects can be handled by any single operation.  
        The returned occurrence information includes BOMLine, transform, JT file location and ticket, and to what
        cursors each occurrence belongs using a similar bitmask mechanism as described above.
        
        Use cases:
        The visualization client performs the following sequence when viewing a configured assembly from Teamcenter
        using MMV technology:
            1.    Construct a BOMWindow with the appropriate configuration for the structure of interest
            2.    Determine if MMV based rendering can be used for this structure by invoking 
        'acquireSpatialHierarchy' and passing the top line of the structure
                a.    If MMV possible, a view lock is applied on the Fnd0SpatialHierarchy dataset attached to the
        ItemRevision that represents the top line of the structure, and a read file ticket is returned for the spatial
        hierarchy (*.mmv) file for subsequent download.
                b.    If MMV rendering is not possible, the appropriate error is returned to the client.  This can
        happen most often if the structure was not harvested, or if the configuration of interest does not match the
        configuration that was harvested.
            3.    Prior to rendering, the visualization client needs to set the view frustum for the visibility request
        of interest.  This is done by first calling the 'getNodeBBox' service for all the occurrences that are to be
        set visible in order to setup the view.  The bounding box information returned is processed and the view setup
        properly prior to rendering.
            4.    Prior to rendering from the spatial hierarchy the client must first create an mmv cursor via the
        'createMmvCursor', and specify the visibility scoping set in the cursor.  If the entire model is to be set
        visible, the visibility scope is not specified.  If a specific set of occurrences are to be set visible (e.g.
        one or more subassemblies), the visibility scoping set must be set to the occurrence thread paths representing
        the occurrences in scope (e.g. the subassemblies and parts to render).
            5.    Rendering is now ready to begin.  Rendering consists of traversing the spatial hierarchy and
        resolving cells to visible occurrences, and occurrences are loaded.   Spatial cells are supplied to the
        'GetSpatialCellsReadTickets' along with spatial hierarchy dataset uid, BOMWindow and the cursor object.  The
        initial cursor contains the visibility scoping set.  Configured occurrences are returned from the call.
            6.    The client downloads the JT parts referenced by the visible occurrences returned, loads the geometry,
        and applies the transformation.  The geometry is rendered.  The VGR algorithm reevaluates the visibility based
        on the real loaded geometry, and determines additional cells that need to be loaded.
            7.    The process returns to step 5 above and repeats continuously until the rendering stabilizes and the
        picture is complete.  The calls to 'GetSpatialCellsReadTickets' eventually stop when the rendering completes.
        """
        return cls.execute_soa_method(
            method_name='getSpatialCellsReadTickets',
            library='Internal-Mmv',
            service_date='2012_09',
            service_name='SpatialStructureManagement',
            params={'input': input},
            response_cls=GetSpatialCellsReadTicketsResponse,
        )

    @classmethod
    def isSpatialHierarchyLatest(cls, input: IsSpatialHierarchyIn) -> IsSpatialHierarchyLatestResponse:
        """
        This operation is called periodically (via polling) by the viewer when it is running in Kiosk mode to see if
        there is a new MMV spatial hierarchy (.mmv file) available for loading.  This service operation checks if the
        supplied Fnd0SpatialHierarchy dataset version is the latest or not.  Since the MMV harvester is intended to run
        constantly, a new version of the spatial hierarchy may become available for the client at any time.  This
        allows the viewer to detect when a newer version of the spatial hierarchy is available, and update itself to
        the latest model indexed by the MMV harvester.  If a new Fnd0SpatialHierarchy dataset version is created by the
        harvester and found by this method, the viewer will unload the current spatial hierarchy, download the new .mmv
        file, load the new spatial hierarchy, and rerender the model.
        
        Use cases:
        The Visualization client can be placed in a kiosk mode, where it polls the server for updated spatial hierarchy
        datasets.  In this mode, the viewer will periodically call the 'isSpatialHierarchyLatest' service to see if a
        new spatial hierarchy file is available.  If one is found, the viewer will update to the new spatial hierarchy
        file and reestablish its state as follows:
            1.    Viewer periodically checks for new Fnd0SpatialHierarchy dataset version by calling
        'isSpatialHierarchyLatest'.  If none found, it waits and calls again later.  However, if found the following
        steps then occur.
            2.    Viewer captures its current state by saving a vis session file locally containing all the snapshots
        and authored data relevant for the session.  This includes a snapshot of the current 3D scene, along with the
        configuration information for the structure currently loaded.  The configuration information is stored as a
        VisStructureContext object in Teamcenter.
            3.    Viewer unloads the spatial hierarchy and 3D model by closing the 3D document
            4.    Viewer loads the vis session back up, which causes the structure to be reopened and configured the
        way it had been configured prior to the update.  The 'createBOMsFromRecipes' service is used to reestablish the
        structure configuration.
            5.    The viewer applies the snapshot that represented the scene that was present in the kiosk prior to the
        spatial hierarchy update.  This causes the occurrence references within the snapshot to resolve, which then
        results in loading the appropriate product Structure into the viewer.  Once the product structure is loaded,
        the visibility request is made.  For subassembly visibility requests, the cursor is created with the visibility
        scoping set, and MMV rendering commences to create the scene.  
            6.    The viewer goes back to kiosk mode, going back to whatever it was doing before the update.
        """
        return cls.execute_soa_method(
            method_name='isSpatialHierarchyLatest',
            library='Internal-Mmv',
            service_date='2012_09',
            service_name='SpatialStructureManagement',
            params={'input': input},
            response_cls=IsSpatialHierarchyLatestResponse,
        )

    @classmethod
    def releaseMmvCursor(cls, mmvCursors: List[BusinessObject]) -> ServiceData:
        """
        This operation releases a runtime cursor object in the tcserver that was previously created by the
        'createMmvCursor' function.  This service is intended to be called when the client has completed rendering a
        particular visibility request and the 'GetSpatialCellsReadTickets' calls have completed.
        
        Use cases:
        The Visualization client releases the cursor once the user closes the assemblies or completes the visualization
        rendering cycle for subassemblies.  
        The visualization client performs the following sequence when viewing a configured assembly from Teamcenter
        using MMV technology:
            1.    Construct a BOMWindow with the appropriate configuration for the structure of interest
            2.    Determine if MMV based rendering can be used for this structure by invoking 
        'acquireSpatialHierarchy' and passing the top line of the structure
                a.    If MMV possible, a view lock is applied on the Fnd0SpatialHierarchy dataset attached to the
        ItemRevision that represents the top line of the structure, and a read file ticket is returned for the spatial
        hierarchy (*.mmv) file for subsequent download.
                b.    If MMV rendering is not possible, the appropriate error is returned to the client.  This can
        happen most often if the structure was not harvested, or if the configuration of interested does not match the
        configuration that was harvested.
            3.    To start rendering from the spatial hierarchy the client must first create an mmv cursor via the
        'createMmvCursor', and specify the visibility scoping set in the cursor.  If the entire model is to be set
        visible, the visibility scope is not specified.  If a specific set of occurrences are to be set visible (e.g.
        one or more subassemblies), the visibility scoping set must be set to the occurrence thread paths representing
        the occurrences in scope (e.g. the subassemblies and parts to render).
            4.    The visualization client renders the geometry using MMV by making a series of
        'GetSpatialCellsReadTickets' calls to configure and resolve spatial cells into occurrences that are
        subsequently loaded and rendered.
            5.    When the rendering of the subassembly is complete or when the 3D document window is closed or if
        viewer itself is closed the client calls the 'releaseMmvCursor' to free the cursor resources.
        """
        return cls.execute_soa_method(
            method_name='releaseMmvCursor',
            library='Internal-Mmv',
            service_date='2012_09',
            service_name='SpatialStructureManagement',
            params={'mmvCursors': mmvCursors},
            response_cls=ServiceData,
        )

    @classmethod
    def releaseSpatialHierarchy(cls, input: ReleaseSpatialHierarchyIn) -> ServiceData:
        """
        Since the MMV harvester is running continuously on the server, the MMV spatial index can be updated at any
        time, even when clients are using it.  Thus, clients obtain a read lock on the spatial hierarchy dataset (.mmv)
        when it is opened via the 'acquireSpatialHierarchy' service.  However, when the client is no longer using the
        spatial hierarchy, the read lock should be released.  This operation releases a lock on the set of dataset
        versions in the current tcserver process.  This reduces the lock counts of these dataset versions by 1.  The
        visualization client calls this method whenever the 3D document that is rendered via MMV technology is closed,
        or if the viewer itself is closed.  
        Releasing the view lock on the dataset version allows the harvester to delete this version in its next run when
        no lock remains on the dataset version.  Provisions are also made for the harvester to check the tcserver
        session process table and release locks when process go away for unexpected reasons such as crashes.
        
        Use cases:
        The visualization client performs the following sequence when viewing a configured assembly from Teamcenter
        using MMV technology:
            1.    Construct a BOMWindow with the appropriate configuration for the structure of interest
            2.    Determine if MMV based rendering can be used for this structure by invoking 
        'acquireSpatialHierarchy' and passing the top line of the structure
                a.    If MMV possible, a view lock is applied on the Fnd0SpatialHierarchy dataset attached to the
        ItemRevision that represents the top line of the structure, and a read file ticket is returned for the spatial
        hierarchy (*.mmv) file for subsequent download.
                b.    If MMV rendering is not possible, the appropriate error is returned to the client.  This can
        happen most often if the structure was not harvested, or if the configuration of interest does not match the
        configuration that was harvested.
            3.    Render the model using MMV technology
            4.    If 3D document window closed or if viewer itself is closed, call the 'releaseSpatialHierarchy'
        service to release the read lock the client has on the Fnd0SpatialHierarchy dataset.
        """
        return cls.execute_soa_method(
            method_name='releaseSpatialHierarchy',
            library='Internal-Mmv',
            service_date='2012_09',
            service_name='SpatialStructureManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def createMmvCursor(cls, scope: SearchScope) -> CreateMmvCursorResponse:
        """
        This operation creates a runtime cursor object that is later used with the 'GetSpatialCellsReadTickets' service
        to maintain server state (progress) during rendering when a series of 'GetSpatialCellsReadTickets' calls are
        made.  That is, the next 'GetSpatialCellsReadTickets' call starts where the last call left off via the runtime
        cursor.   When the cursor is first created, the visibility scope at the visualization client side must be
        specified.  The visibility scope refers to a set of occurrences (parts or assemblies) within which visible
        geometry is to be displayed.  Providing the visibility scope to the server enables the client to render one or
        more specific subassemblies directly from the spatial hierarchy (.mmv file) without first knowing the
        occurrences within these subassemblies.  The client renders from the spatial hierarchy regardless if the entire
        model or a specific subset of the model is being set visible.  During rendering, the server will only return
        occurrences from the 'GetSpatialCellsReadTickets' calls that are contained within the visibility scoping set
        specified by the client.  If the client wishes to set the entire model visible, the scoping set is left blank. 
        If the client is to render one or more specific subassemblies, the scoping set is the occurrence thread paths
        of these specific subassemblies.
        The visibility scoping set can only be specified during cursor creation via this call.  If the visibility
        changes, a new cursor must be created prior to the 'GetSpatialCellsReadTickets' calls made during the rendering
        process.
        
        
        Use cases:
        The visualization client performs the following sequence when viewing a configured assembly from Teamcenter
        using MMV technology:
            1.    Construct a BOMWindow with the appropriate configuration for the structure of interest
            2.    Determine if MMV based rendering can be used for this structure by invoking 
        'acquireSpatialHierarchy' and passing the top line of the structure
                a.    If MMV possible, a view lock is applied on the Fnd0SpatialHierarchy dataset attached to the
        ItemRevision that represents the top line of the structure, and a read file ticket is returned for the spatial
        hierarchy (*.mmv) file for subsequent download.
                b.    If MMV rendering is not possible, the appropriate error is returned to the client.  This can
        happen most often if the structure was not harvested, or if the configuration of interested does not match the
        configuration that was harvested.
            3.    To commence rendering from the spatial hierarchy the client must first create an mmv cursor via the
        'createMmvCursor', and specify the visibility scoping set in the cursor.  If the entire model is to be set
        visible, the visibility scope is not specified.  If a specific set of occurrences are to be set visible (e.g.
        one or more subassemblies), the visibility scoping set must be set to the occurrence thread paths representing
        the occurrences in scope (e.g. the subassemblies and parts to render).
            4.    The visualization client renders the geometry using MMV by making a series of
        'GetSpatialCellsReadTickets' calls to configure and resolve spatial cells into occurrences that are
        subsequently loaded and rendered.
        """
        return cls.execute_soa_method(
            method_name='createMmvCursor',
            library='Internal-Mmv',
            service_date='2012_09',
            service_name='SpatialStructureManagement',
            params={'scope': scope},
            response_cls=CreateMmvCursorResponse,
        )

    @classmethod
    def acquireSpatialHierarchy(cls, input: AcquireSpatialHierarchyIn) -> AcquireSpatialHierarchyResponse:
        """
        The visualization client calls this service when a configured structure is opened from Teamcenter to determine
        whether or not the model can be rendered using MMV technology.  To use MMV technology, the structure must have
        been harvested and an MMV spatial index created, and the configuration of the structure of interest must match
        the configurations that were harvested.  If these conditions are met, the service returns dataset information
        and a read ticket to the spatial hierarchy  (.mmv) file that is read and used for MMV rendering; otherwise, an
        error is returned.
        This operation returns the latest version of Fnd0SpatialHierarchy dataset attached to the input BOMLine 
        Itemrevision in the case MMV rendering is possible (i.e. the structure has been harvested).  The dataset
        returned is locked for viewing and the associated information including ImanFile, original file name, and
        ticket information is returned.  The lock is applied to prevent this version from being removed by the mmv
        index harvester that may be schedule to be run periodically to update the spatial index.  That is, when
        multiple clients are viewing a structure using MMV technology, they must not be adversely affected by the MMV
        harvester when it updates the spatial index.  This is accomplished by having the clients create a read lock on
        the Fnd0SpatialHierarchy dataset , indicating to the harvester that it must not delete MMV indexes that are
        currently in use, but rather it must create a new version of the spatial index dataset.  A map array is
        returned to map the returned dataset version array to the input BOMLine array.  
        The service also validates whether or not the spatial hierarchy file (.mmv) can be used for the current
        structure being viewed.  The MMV index harvester supports unconfigured harvesting as well as preconfigured
        harvesting to limit the scope of what was harvested if desired.  The Fnd0SpatialHierarchy dataset created by
        the harvester contains a record of the configuration of the structure used to generate the spatial hierarchy. 
        The configuration of the current bomwindow (passed in as the top line of the structure) is checked to make sure
        it matches the configuration that was used to generate the spatial index.   If the configurations match, the
        Fnd0SpatialHierarchy dataset information will be returned.  If they do not match, an error is returned
        indicating that particular configuration was not harvested.
        
        Use cases:
        The visualization client performs the following sequence when viewing a configured assembly from Teamcenter
        using MMV technology:
            1.    Construct a bomwindow with the appropriate configuration for the structure of interest
            2.    Determine if MMV based rendering can be used for this structure by invoking 
        'acquireSpatialHierarchy' and passing the top line of the structure
                a.    If MMV possible, a view lock is applied on the Fnd0SpatialHierarchy dataset attached to the
        ItemRevision that represents the top line of the structure, and a read file ticket is returned for the spatial
        hierarchy (*.mmv) file for subsequent download by the client.
                b.    If MMV rendering is not possible, the appropriate error is returned to the client.  This can
        happen most often if the structure was not harvested, or if the configuration of interest does not match the
        configuration that was harvested.
            3.    Render the geometry based on user action using MMV if possible.  If MMV possible, download the load
        the .mmv file and render from the spatial hierarchy.  If not possible, use traditional large model
        visualization rendering technology.
        """
        return cls.execute_soa_method(
            method_name='acquireSpatialHierarchy',
            library='Internal-Mmv',
            service_date='2012_09',
            service_name='SpatialStructureManagement',
            params={'input': input},
            response_cls=AcquireSpatialHierarchyResponse,
        )

    @classmethod
    def getNodeBBox(cls, input: GetNodeBBoxIn) -> GetNodeBBoxResponse:
        """
        This operation gets bounding box (bbox) information for a set of input node objects from the MMV index on the
        server. Each object is represented by a series of UIDs representing its occurrence thread path. The returned
        'NodeBBox' array is parallel to the input node array.  A 'NodeBBox' structure may contain multiple bounding
        boxes, meaning that there can be multiple node bbox records for the node as the node may represent a
        subassembly.
        The advantage of this approach is that the bounding boxes can be rapidly computed from the MMV index and
        positioned in model space, so the performance is very high.
        
        Use cases:
        The Visualization client must properly set the view frustum when prompted by the user to view a subassembly by
        clicking the node in the tree structure to ensure the proper zoom level for the assembly.  In addition, the
        viewer must support actions such as fit all in cases where the product structure is not yet known.  This
        requires the bounding box information be positioned in model space for the nodes to be set visible.  
        After the Fnd0SpatialHierarchy (.mmv file) has been acquired using 'acquireSpatialHierarchy' operation, the
        file is loaded.  When a visibility request is received from the user (e.g. by clicking one or more nodes in the
        assembly tree), the viewer must get the bounding box for these specified nodes as follows:
            1.    Get the occurrence thread uid paths from the tree structure.
            2.    Invoke the 'getNodeBBox' operation by supplying it with the occurrence thread uid paths, and use the
        returned bounding box to set the view frustum. 
            3.    Determine which cells from the spatial hierarchy need to be configured based on their position
        relative to the bounding box information.
            4.    The client traverses only the bounding box scoped cells of the spatial hierarchy during rendering,
        and submits those to the server for configuration and resolution.
        """
        return cls.execute_soa_method(
            method_name='getNodeBBox',
            library='Internal-Mmv',
            service_date='2012_09',
            service_name='SpatialStructureManagement',
            params={'input': input},
            response_cls=GetNodeBBoxResponse,
        )
