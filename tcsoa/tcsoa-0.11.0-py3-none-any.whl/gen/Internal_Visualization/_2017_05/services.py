from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Visualization._2017_05.DataManagement import Snapshot3DInfoResponse2, Snapshot3DInfoInput2
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getSnapshot3DInfo2(cls, snapshot3DInputList: List[Snapshot3DInfoInput2]) -> Snapshot3DInfoResponse2:
        """
        This service is used by the visualization integrations to gather the information needed to open a Product View
        (i.e. a SnapShotVisData Dataset) and apply it to recreate a 3D scene. The service gets SnapShotViewData Dataset
        information for a list of Product Views  of interest including all the named reference file information, all
        the supporting objects related to the Dataset by GRM or named reference, and all the visible lines referenced.
        This information is used by the viewer to open up the appropriate structure and configuration, expand the
        structure and load the visible lines , and recreate the 3D scene by applying the viewFile PLMXML.
        
        The client specifies  the SnapShotViewData Dataset objects to be opened, and the objects are added to the
        Snapshot3DInfoInput2 input structure. One or more SnapShotViewData Dataset objects can be added to the list to
        get information on many Product Views in batch. If more than one object is used, it is important to use unique
        clientId strings in the input, since they are used as keys in the return output map. If the same clientId
        string is used, information will be lost.
        
        The related objects returned are used to identify the top line of the structure (e.g. VisTopLevelRef), and to
        get the configuration of the structure to open (e.g. VisStructureContext object).
        
        The visible lines are used to expand the structure and load the appropriate occurrences in order to recreate
        the 3D scene. This consists of an array of strings that represent clone stable IDs, absolute occurrence IDs, or
        ID&rsquo;s in context,  depending on the version of the Product View data model. The output data will indicate
        the visible line type in the Snapshot3DVisibleLines using the uidtype. If the type is a clone stable UID chain,
        this is a &lsquo;/&rsquo; delimited string that represents a path from the root of the structure to the visible
        line of interest. This list will be obtained by processing the structure PLMXML file.
        
        The return information also provides the core files that need to be opened by the viewer (e.g. the viewFile
        PLMXML and/or the structure file PLMXML). The viewFile is used to recreate the 3D scene, and the structure file
        can be used to open the static structure for the Product View to recreate the same scene that was saved
        originally.
        
        Use cases:
        This service helps provide the viewer with information to load Product View objects. There are 3 main use cases
        for loading Product Views, each described in more detail below.
        
        
        &bull;Load Static Product View: In this case the static structure for the visible lines and their descendants
        is loaded from the Product View data model via the structure PLMXML file. This returns the Product View to the
        as saved state as far as product structure goes, but changes to part level JTs due to overwrite operations can
        still be present.
        &bull;Load dynamic Product View: In this case the structure configuration information stored in the Product
        View data model that represents the configuration of the structure when the Product View was last saved is used
        to reconfigure the structure with the same configuration rules before the scene is recreated. 
        &bull;Load dynamic Product View: In this case the current BOM window configuration established in the Structure
        Manager (SM), Multi Structure Manager (MSM), or Manufacturing Process Planner (MPP) application is the
        structure configuration used to apply the Product View on.
        
        
        Load static Product View:
        &bull;User selects one or more Product View objects (SnapShotViewData Dataset objects) in My Teamcenter and
        sends those to open in visualization. 
        &bull;The visualization client gets the list of objects to open, builds up the Snapshot3DInfoInput2 input
        structure for each Dataset, and calls the getSnapshot3DInfo operation for the Product Views. 
        &bull;The system reads the data model and returns the visible lines list, the named references for the files,
        and related objects. 
        &bull;The viewer downloads the files of interest from the Dataset (e.g. structure PLMXML file, viewFile PLMXML,
        and 3D markup layers (vpl markup layers)). 
        &bull;The viewer loads the structure PLMXML file, loads the markup layers (vpl files), and then merges in the
        viewFile PLMXML to recreate the 3D scene.
        
        Load dynamic Product View using stored configuration rules:
        &bull;User selects one or more Product View objects in My Teamcenter and sends those to open in visualization. 
        &bull;The visualization client gets the list of related objects to open, builds up the Snapshot3DInfoInput2
        structure for each Dataset, and calls the getSnapshot3DInfo operation for the Product Views. 
        &bull;The system reads the data model and returns the visible lines list, the named references, and related
        objects. 
        &bull;The viewer downloads the files of interest from the Dataset (structure PLMXML file, viewFile PLMXML, vpl
        markup layers). 
        &bull;The viewer uses the related objects information to get the top line and the configuration information for
        the structure via the VisStructureContext object, and calls the createBOMsFromRecipes operation to configure
        the structure properly. 
        &bull;The viewer uses the visible line information to expand the BOM structure and fetch BOMLine objects. If
        clone stable occurrence id chains are the type of visible lines returned, the Viewer starts at the top of the
        structure and uses the expandPSOneLevel operation to expand the structure and load it. If the absolute
        occurrences are the type of visible lines returned or the preference to prune the structure during Product View
        load is active, the viewer uses the expandPSFromOccurrenceList operation to expand the structure and fetch the
        visible BOMLine objects. 
        &bull;Once the configured structure is loaded and expanded, the viewer loads the markup layers (vpl files), and
        then merges in the viewFile PLMXML to recreate the 3D scene.
        
        Load dynamic Product View using current configuration rules:
        &bull; User sends a structure to Structure Manager (SM), Multi Structure Manager (MSM), or Manufacturing
        Process Planner (MPP) and configures the structure with revision rules, variant rules, effectivity, etc. 
        &bull; The user brings up the Product View gallery, and the system finds Product Views of interest by calling
        the gatherSnapshot3DList operation.  
        &bull; The user selects some Product Views and sends those to visualization. For standalone visualization a
        VisStructureContext is sent from the launching client with the launch file that represents the current
        configuration of the BOMWindow. For embedded visualization, the current BOMWindow configuration is already
        known.
        &bull; The visualization client gets the list of objects to open, builds up the Snapshot3DInfoInput2 structure
        for each object, and calls the getSnapshot3DInfo operation for the Product Views. 
        &bull; The system reads the data model and returns the visible lines list, the named references, and related
        objects. 
        &bull; The viewer downloads the files of interest from the Dataset (structure PLMXML file, viewFile PLMXML, vpl
        markup layers). 
        &bull; The viewer uses the visible line information to expand the BOM structure and fetch BOMLine objects if
        they are not already loaded. If clone stable occurrence ID chains are the type of visible lines returned, the
        Viewer starts at the top of the structure and uses the expandPSOneLevel operation to expand the structure and
        load it. If the absolute occurrences are the type of visible lines returned or the preference to prune the
        structure during Product View load is active, the viewer uses the expandPSFromOccurrenceList operation to
        expand the structure and fetch the visible BOMLine objects. 
        &bull; Once the configured structure is loaded and expanded, the viewer loads the markup layers (.vpl files),
        and then merges in the view File PLMXML to recreate the 3D scene.
        """
        return cls.execute_soa_method(
            method_name='getSnapshot3DInfo2',
            library='Internal-Visualization',
            service_date='2017_05',
            service_name='DataManagement',
            params={'snapshot3DInputList': snapshot3DInputList},
            response_cls=Snapshot3DInfoResponse2,
        )
