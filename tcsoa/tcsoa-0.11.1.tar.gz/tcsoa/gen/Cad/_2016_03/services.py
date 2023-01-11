from __future__ import annotations

from tcsoa.gen.Cad._2016_03.StructureManagement import BoolMap, FindModelViewsInStructureResponse
from tcsoa.gen.BusinessObjects import BusinessObject, ConfigurationContext
from tcsoa.gen.Cad._2016_03.DataManagement import ModelViewProxyInfo, ModelViewPaletteInfo, CreateOrUpdateMVPaletteResponse, OwningModelAndCadLmd, CreateOrUpdateModelViewProxiesResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createOrUpdateModelViewPalette(cls, mvPaletteInfo: List[ModelViewPaletteInfo]) -> CreateOrUpdateMVPaletteResponse:
        """
        Creates, updates or deletes a model view palette (Fnd0ModelViewPalette) object and its groups. The model view
        palette supports Visualization tools in creating and managing model view groups (Fnd0ModelViewGroup) during
        creation of a Disclosure object (an Item or Workset that discloses installation assembly designs). The
        disclosed model view proxy objects may be grouped by this operation.
        Using this API, applications can create and update a list of objects in bulk. Providing better context and
        fewer calls from the CAD clients than otherwise would be achieved using standard object create and update
        service operations.
        
        Use cases:
        This API supports the following use cases
        
        Use Case 1: Creation of Model View Palette and Model View Groups for a Design Disclosure
        
        The operation can be used for supporting creation of a disclosure object. The disclosure object will most
        commonly be a Workset (Cpd0Workset subtype) but may also be a specific type of ItemRevision. The actual
        disclosure object may be pre-existing but would not be acting as a disclosure until this operation creates and
        attaches the desired list of disclosed Model View Proxy references.
        
        The purpose of a design disclosure is to act as a 3D equivalent of a 2D drawing of individual installation
        assemblies (IA.) This disclosure object will collect all geometry needed to show both the IA and its assembly
        PMI. After the various PMI and Model Views within the disclosure have been created, they must be "disclosed". 
        
        To be considered as disclosed by a disclosure object, a Model View Proxy must be referenced by a Model View
        Group (Fnd0ModelViewGroup)that is referenced by a Model View Palette (Fnd0ModelViewPalette) that is associated
        to the disclosure object.
        
        The 'paletteIsComplete' input must be set to true for creation of a Model View Palette, as it makes no sense to
        be false.
        
        Use Case 2: Update of Model View Palette and Model View Groups for a Design Disclosure
        If 'groupsToDelete' is set then see Use case 3 for details, else if 'paletteIsComplete' is set to true, then
        the system will:
          1) Process 'groupsAndProxies', creating or updating various Groups.
          2) Check the existing Group list on the Palette to determine if any existing Groups in the current Palette
        list are not in the input 'groupsAndProxies' input. If so, then set aside such existing Groups for deletion.
          3) Set the list of existing and newly created Groups (from step 1 above) onto the Palette.
          4) Now delete the now unreferenced Groups (from step 2) if any.
        
        If paletteIsComplete is set to false, the system will:
          1) process groupsAndProxies, creating or updating various Groups.
          2) Again, if groupsToDelete is set then see Use case 3 for details. This must be done before re-ordering the
        Palette's sequence of Groups in order for the input sequence order values to be understood correctly by the
        system.
          3) Set the list of existing and newly created Groups (from step 1 above) onto the Palette list of Groups
        (using any specified newOrderSequenceNumber if one was given. If any newOrderSequenceNumber is within the range
        of existing Groups, and that existing Group is not in the groupsAndProxies being given a new sequence number,
        then the existing group being replaced in that sequence number will be set aside to be placed at the end of the
        sequence.
          4) Now place any set-aside (due to be pushed out of place or being given a sequence value of 0) Groups at the
        end of the Palette's list of Groups.
        
        
        Use Case 3: Delete of existing Model View Palette and/or specific Groups within the Palette
        
        To delete an entire Palette and all its Groups, the caller will simply send both the disclosure and the
        deletePalette flag.
        The system will :
        - Verify write permission on the disclosure object in order to proceed.
        - Remove the relation between the disclosure object and the Model View Palette.
        - Delete the Model View Palette
        - Delete all the Model View Groups that were previously referenced by the Model View Palette
        
        
        
        To delete only specified Groups out of all those currently existing on a Palette, the caller will send the
        Groups to delete in the groupsToDelete list.
        The system will:
        - Note: write permission on the Model View Palette is required.
        - Remove all the specified Model View Groups from the reference list on the Model View Palette, preserving the
        order among the remaining Model View Groups referenced by the Palette.
        - Delete the now unreferenced Model View Groups.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateModelViewPalette',
            library='Cad',
            service_date='2016_03',
            service_name='DataManagement',
            params={'mvPaletteInfo': mvPaletteInfo},
            response_cls=CreateOrUpdateMVPaletteResponse,
        )

    @classmethod
    def createOrUpdateModelViewProxies(cls, mvProxyInfos: List[ModelViewProxyInfo], updatedOwningModels: List[OwningModelAndCadLmd]) -> CreateOrUpdateModelViewProxiesResponse:
        """
        Creates, updates or deletes a set of model view proxy (Fnd0ModelViewProxy) objects. Supports CAD tools in
        creating and managing model view proxy objects during Part save. The model view proxy objects are each a proxy
        for a master model view in the Part's CAD file.
        Using this API, applications can create and update proxy objects in bulk, with better context and less calls
        from CAD clients than may otherwise be achieved using standard object create and update SOAs.
        
        Use cases:
        This API supports the following use cases:
        Use Case 1: Creation of new model view proxy 
         The following operation can be used for creating model view proxies for specified owning objects (usually
        ItemRevisions.)
        - Model view proxies have a model view CAD Id (fnd0ModelViewIdCAD) which Id is unique within the set of model
        view proxies associated to the same owning object.
        - During the model view proxies initial creation (but not during a subsequent save-as or revise), a clone
        stable ID is generated which can help in identifying equivalent proxy objects for cases where the
        fnd0ModelViewIdCAD wasn't tracked but rather the proxy object itself.
        - An optional thumbnail file may be identified that a CAD tool has generated for the actual CAD model view.
        - During the operation, the server creates and saves the new model view proxies in context of an already
        existing owning object. The operation returns the new objects to the caller.
        
        
        
        Use Case 2: Update of existing model view proxy 
        The following operation can be used for updating existing model view proxies.
        - Model View Proxies are found by applications via the fnd0OwnedModelViews property of workspaceObject objects.
        - The existing model view proxies can be updated using operation createOrUpdateModelViewProxies. The
        application specifies which model view proxies are to be updated.  Note: the business object type ('boType')
        and owning object ('owningModel') do not need to be set on the input because they are already known to the
        model view proxy and cannot be changed.  The application sets changed property values.
        
        
        
        Use Case 3: Delete of existing model view proxy
        The operation can be used for deleting existing model view proxies due to either the CAD designer removing the
        actual model view or due to a decision that there is no need for that model view to have a proxy any longer.
        - Model View Proxies are found by applications via the fnd0OwnedModelViews property of certain types of
        WorkspaceObject objects (currently this property is only available at  ItemRevision ).
        - The existing model view proxies can be deleted using operation createOrUpdateModelViewProxies. The
        application specifies which model view proxies are to be modified ('modelView') and that they are to be deleted
        ('deleteProxy' set to true.)  The server will attempt to delete the model view proxy and if successful, the
        deleted object list will be updated on the ServiceData of the response.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateModelViewProxies',
            library='Cad',
            service_date='2016_03',
            service_name='DataManagement',
            params={'mvProxyInfos': mvProxyInfos, 'updatedOwningModels': updatedOwningModels},
            response_cls=CreateOrUpdateModelViewProxiesResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def findModelViewsInStructure(cls, disclosure: BusinessObject, structureScope: List[BusinessObject], configurationContext: ConfigurationContext, withDisclosureIntent: List[str], options: BoolMap) -> FindModelViewsInStructureResponse:
        """
        Finds Model View Proxy ( Fnd0ModelViewProxy) objects associated to any objects within the specified structure.
        This operation is most often used when creating a disclosure object.
        
        Objects that act as a disclosure are Items or Worksets that have a relation of Fnd0DisclosingObject to the
        actual design objects being disclosed and hence intend to have a list of disclosed Model View Proxy objects.
        
        Use cases:
        This API supports the following use cases:
        Use Case 1: Creation of a new design disclosure
        
        The operation can be used for supporting creation of a disclosure object. The disclosure object will most
        commonly be a Workset (Cpd0Workset subtype) but may also be a specific type of Item Revision. The actual
        disclosure object may be pre-existing but would not be acting as a disclosure until this operation creates and
        attaches the desired list of disclosed model view references.
        
        The purpose of a design disclosure is to act as a 3D equivalent of a 2D drawing. This disclosure object will
        collect all geometry including background geometry if necessary and PMI needed to show all views describing the
        detailed design for the object being disclosed. The disclosure content may be organized into the following item
        revisions or subsets (depending on the disclosure type):
        - Foreground content - actual installation assembly reference
        - Background content - context of a product into which the installation assembly is used.
        - Separately collected geometry - such as welds between the foreground and background objects. 
        
        
        
        To create the correct model view list (see the createOrUpdateModelViewPalette service operation), the client
        and user must first find candidate model view proxies from which to choose the necessary proxies to disclose.
        
        During the operation, a designer would create a Workset to collect all geometry needed to support  installation
        assembly PMI. It is done to collect assemblies being installed and where they are being installed so that PMI
        and model views associated with this combination can be authored and then disclosed. The following types of
        geometry may be collected in a single Workset:
        - Foreground Subset
        - Background Subset
        - ItemRevision (Weld Collector)
        
        
        
        - Multiple CAD Designers will be concurrently authoring PMI and Model Views (MVs) for disclosure at multiple
        levels of the sub-assemblies under the installation assembly. All the MVs authored at this time are
        undisclosed. However, some of them will be marked as a candidates for disclosure.
        - Owning model (ItemRevision) must exist prior to creating the MV proxy in teamcenter by a new service
        operation createOrUpdateModelViewProxies. The owing model will be specified as a request parameter for each MV
        proxy.
        
        
        
        - A visualization user begins Disclosure authoring by retrieving the above mentioned collector workset and
        making sure it has disclosing object (Fnd0DisclosingObject) relations to the actual installation item revisions
        whose design is being disclosed. They will then use the findModelViewsInStructure operation to find model views
        that are marked as candidates for disclosure and then use a third operation (createOrUpdateModelViewPalette) to
        create the list of actually disclosed model views to be persisted for the Disclosure being updated. 
        
        
        Note:
        Candidate Disclosed Model Views will be retrieved from objects in the Foreground Installation Assembly realized
        subset content, and the Weld Collector Item Revision. They will not belong to either Standard Parts or
        Background Geometry unless the 'withDisclosureIntent'  value is appropriately set or the "skipBackgroundScope"
        option is set to false.
        
        
        Use Case 2: Update of an existing design disclosure
        
        The operation can also be used for supporting the update of a disclosure object. In this use case, the
        disclosed list of model view proxy references is compared with the current design content. Some proxies
        previously disclosed may not be found in the new structure, or some of the proxies may have revised owning
        objects and the service provides this type of information to the caller.
        
        To create the correct model view list (see the createOrUpdateModelViewPalette service operation), the client
        and user must first find candidate model view proxies to remove from the existing list and which candidate
        model view proxies to add to the existing disclosure list.
        
        During the operation :
        
        A visualization user begins Disclosure update by retrieving the above mentioned collector workset. They will
        then use this findModelViewsInStructure operation to find new model views that are marked as candidates for
        disclosure and then use a third operation (createOrUpdateModelViewPalette) to update the list of actually
        disclosed model views to be persisted for the Disclosure being updated. While calling
        findModelViewsInStructure, if the disclosure is passed in as the 'structureScope', then the "compareWithMVList"
        option may also be set. This will request the server to also compare the found model view proxy objects in the
        structure against those model view proxies currently listed as disclosed by the disclosure object, calling out
        ( in 'unfoundFromModelViewList') those which are in the model view list but no longer found in the structure.
        Also returned when known are proposed replacement proxy objects for each such now missing proxy ( in
        'possibleMatching' .)
        """
        return cls.execute_soa_method(
            method_name='findModelViewsInStructure',
            library='Cad',
            service_date='2016_03',
            service_name='StructureManagement',
            params={'disclosure': disclosure, 'structureScope': structureScope, 'configurationContext': configurationContext, 'withDisclosureIntent': withDisclosureIntent, 'options': options},
            response_cls=FindModelViewsInStructureResponse,
        )
