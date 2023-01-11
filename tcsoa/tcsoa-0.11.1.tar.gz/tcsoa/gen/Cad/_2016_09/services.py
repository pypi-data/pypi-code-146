from __future__ import annotations

from tcsoa.gen.Cad._2016_09.StructureManagement import ReconcilePaletteResponse, NextReconcilePaletteInput, FindModelViewsResponse, FindModelViewsInput, ReconcilePaletteInput
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def continueFindModelViews(cls, searchID: str, stopFind: bool) -> FindModelViewsResponse:
        """
        Continues a search for model views that was started by the startFindModelViews operation. The input 'searchID'
        specifies which partial find to continue.
        """
        return cls.execute_soa_method(
            method_name='continueFindModelViews',
            library='Cad',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'searchID': searchID, 'stopFind': stopFind},
            response_cls=FindModelViewsResponse,
        )

    @classmethod
    def continueReconcilePalette(cls, reconcilePaletteInput: NextReconcilePaletteInput) -> ReconcilePaletteResponse:
        """
        This operation continues the reconciliation of Fnd0ModelViewProxy object references in a Fnd0ModelViewPalette
        object for a given product structure and configuration. The Fnd0ModelViewProxy objects are authored and managed
        by  CAD applications, and their lifecycle is delegated to their CAD owning model's lifecycle.  As the CAD
        owning models are updated, so are their Fnd0ModelViewProxy objects.  However, the Fnd0ModelViewPalette objects
        that reference these Fnd0ModelViewProxy objects are not automatically updated during CAD model update in all
        cases, because there are times when this update needs to be carefully controlled by users.  Consequently, the
        Fnd0ModelViewPalette can get out of synchronization with the structure it is attached to.  This service
        operation is provided to help reconcile differences between the loaded structure configuration and an existing
        Fnd0ModelViewPalette in a user controlled manner.  It provides the caller with information about which
        Fnd0ModelViewProxy objects should be removed and which should be replaced by analyzing the current configured
        structure and comparing it to what was found in an existing Fnd0ModelViewPalette.
        The Fnd0ModelViewPalette contains Fnd0ModelViewProxy object references for  components belonging to the product
        structure. When the components in the structure gets revised, cloned, removed, or a model view is deleted or
        unpublished, or when the structure configuration gets changed, the Fnd0ModelViewPalette needs to be reconciled
        against the current structure in order to get the proper Fnd0ModelViewProxy objects corresponding to the
        updated structure. Using this operation, a list of Fnd0ModelViewProxy objects that need to be replaced or
        removed for a given Fnd0ModelViewPalette can be identified, retrieved, and presented to user, so that the user
        can carefully control the update of the Fnd0ModelViewPalette for the various update use cases.
        This operation is designed in such a way that the caller can use it in a threaded operation and display results
        in batches instead of waiting for the entire reconciliation process to be complete which may take a fair amount
        of time for large structures. Before invoking this this operation, the 'startReconcilePalette' operation should
        have been invoked for the same 'clientID'.
        Note: The reconcile process has to be closed by the caller using the 'continueReconcilePalette' operation with
        'stopReconcile' as true. For example the caller calls 'startReconcilePalette' operation followed by
        'continueReconcilePalette' operation. Once the finished variable is returned as true in the response the caller
        calls 'continueReconcilePalette' with 'stopReconcile' as true so that the resources are freed up in the server.
        
        Use cases:
        The operation supports the following use cases.
        Use Case 1 :  Update a Fnd0ModelViewPalette per informal engineering change (i.e. overwrite)
        1.An authoring user creates a detailed design in a CAD application.  The user creates and publishes Model Views
        describing the design details. The Model Views are persisted in Teamcenter as Fnd0ModelViewProxy objects using
        the operation 'createOrUpdateModelViewProxies'.
        2.The authoring user opens a configured product structure in a visualization enabled Teamcenter application and
        finds the published Fnd0ModelViewProxy objects in the product structure using the operation
        'findModelViewsInStructure'.
        3.The authoring user selects a limited subset of the Fnd0ModelViewProxy objects found, adds them to a Palette,
        organizes them for presentation by re-ordering and grouping, and creates a Fnd0ModelViewPalette object in
        Teamcenter which references Fnd0ModelViewProxy objects using the operation 'createOrUpdateModelViewPalette'.
        4.A reviewing user opens the product structure configuration along with the Fnd0ModelViewPalette into a
        visualization enabled Teamcenter application, reviews each Model View for accuracy, creates review comments for
        changes that need to be made, and submits those changes to the CAD Designer that authored the original detailed
        design.
        5.The authoring user receives the review comments from various reviewing users, and uses the CAD application to
        make changes to the CAD model(s) such as add or remove components, reposition or change parts, add, delete, or
        change model views, publish or unpublish model views, etc.  The updated CAD models are saved to Teamcenter
        along with updated Fnd0ModelViewProxy objects using the operation 'createOrUpdateModelViewProxies'.  Since this
        is informal change, the CAD models are typically overwritten as opposed to revised.
        6.The authoring user opens the configured product structure with attached Fnd0ModelViewPalette created in step
        3 in a visualization enabled Teamcenter application, and some of the Fnd0ModelViewProxy objects referenced by
        the Fnd0ModelViewPalette are no longer valid relative to the current structure due to the CAD model changes. 
        The user invokes the palette reconcile action which triggers the operation 'startReconcilePalette' followed by
        'continueReconcilePalette'. The results are displayed to the user providing information on which
        Fnd0ModelViewProxy objects are still valid, which need to be replaced, and which need to be removed in order to
        update the Palette.  The results are streamed to the client  in batches, so the user is updated on progress and
        can choose to stop the reconcile operation at any time.
        7.The authoring user updates the Fnd0ModelViewPalette per the changes suggested by this operation, and saves
        the palette updates using the operation 'createOrUpdateModelViewPalette'.
        
        Use Case 2: Update a Fnd0ModelViewPalette to a different structure configuration
        1.The user opens a structure configuration different from that used to author the original Fnd0ModelViewPalette
        (per use case 1), and sends this to the visualization enabled palette authoring tool in Teamcenter.
        2.The user opens the Fnd0ModelViewPalette and invokes the palette reconcile action which triggers the operation
        'startReconcilePalette' followed by 'continueReconcilePalette'. The results are displayed to the user providing
        which Fnd0ModelViewProxy objects cannot be found, which are still valid, which need to be replaced, and which
        need to be removed in order to reconcile the Palette to the current structure configuration. The results are
        streamed to the client  in batches, so the user is updated on progress and can choose to stop the reconcile
        operation at any time.
        3.The authoring user updates the Fnd0ModelViewPalette per the changes suggested by the operation, and saves the
        palette updates using the operation 'createOrUpdateModelViewPalette'. The updated structure configuration
        information used for the updated palette is stored with the palette. 
        
        Use Case 3 : Update a Fnd0ModelViewPalette per formal engineering change (i.e. Revise)
        1.The user of a CAD application makes changes to the CAD model(s) representing the detailed design such as
        revising components, add, delete, or change model views, publish or unpublish model views, etc during revise of
        a detailed design.  The revised CAD models are saved to Teamcenter, where new and updated Fnd0ModelViewProxy
        objects are published using the operation 'createOrUpdateModelViewProxies' and Teamcenter deep copy rules come
        into play.
        2.The user opens the configured product structure with attached Fnd0ModelViewPalette (see use case 1) in a
        visualization enabled Teamcenter application, and some of the Fnd0ModelViewProxy objects referenced by the
        Fnd0ModelViewPalette are no longer valid due to the revised CAD model(s).  Some of the Fnd0ModelViewProxy
        objects in the Fnd0ModelViewPalette are from previous revisions of the revised components, others cannot be
        found. The user invokes the palette reconcile action which triggers the operation 'startReconcilePalette'
        followed by 'continueReconcilePalette'. The results are displayed to the user providing information on which
        Fnd0ModelViewProxy objects are still valid, which need to be replaced with Fnd0ModelViewProxy objects on new
        revisions of the CAD models, and which need to be removed in order to update the Palette.  The results are
        streamed to the client  in batches, so the user is updated on progress and can choose to stop and restart the
        reconcile operation at any time.
        3.The user updates the Fnd0ModelViewPalette per the changes suggested by this operation, and saves the updated
        palette using the operation 'createOrUpdateModelViewPalette'.
        """
        return cls.execute_soa_method(
            method_name='continueReconcilePalette',
            library='Cad',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'reconcilePaletteInput': reconcilePaletteInput},
            response_cls=ReconcilePaletteResponse,
        )

    @classmethod
    def startFindModelViews(cls, findInput: FindModelViewsInput) -> FindModelViewsResponse:
        """
        Finds Model View Proxy (Fnd0ModelViewProxy) objects associated to any objects within the specified structure.
        This operation is most often used when creating a disclosure object.
        
        Objects that act as a disclosure are Items or Worksets that have a relation of Fnd0DisclosingObject to the
        actual design objects being disclosed and hence intend to have a list of disclosed Model View Proxy objects.
        
        Used in conjunction with the continueFindModelViews operation. If the preference MVFindMinNodeCount has a
        value, that value is the minimum number of structure nodes to search before returning with 'finished' as false.
        
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
        Foreground content - actual installation assembly reference
        Background content - context of a product into which the installation assembly is used.
        Separately collected geometry - such as welds between the foreground and background objects. 
        
        To create the correct model view list (see the createOrUpdateModelViewPalette service operation), the client
        and user must first find candidate model view proxies from which to choose the necessary proxies to disclose.
        
        During the operation, a designer would create a Workset to collect all geometry needed to support  installation
        assembly PMI. It is done to collect assemblies being installed and where they are being installed so that PMI
        and model views associated with this combination can be authored and then disclosed. The following types of
        geometry may be collected in a single Workset:
        Foreground Subset
        Background Subset
        ItemRevision (Weld Collector)
        
        Multiple CAD Designers will be concurrently authoring PMI and Model Views (MVs) for disclosure at multiple
        levels of the sub-assemblies under the installation assembly. All the MVs authored at this time are
        undisclosed. However, some of them will be marked as a candidates for disclosure.
        Owning model (ItemRevision) must exist prior to creating the MV proxy in teamcenter by a new service operation
        createOrUpdateModelViewProxies. The owing model will be specified as a request parameter for each MV proxy.
        
        A visualization user begins Disclosure authoring by retrieving the above mentioned collector workset and making
        sure it has disclosing object (Fnd0DisclosingObject) relations to the actual installation item revisions whose
        design is being disclosed. They will then use the startFindModelViews operation followed by the
        continueFindModelViews operation to find model views that are marked as candidates for disclosure and then use
        a third operation (createOrUpdateModelViewPalette) to create the list of actually disclosed model views to be
        persisted for the Disclosure being updated. 
        Note:
        Candidate Disclosed Model Views will be retrievedfrom all structure nodes that are not suppressed or children
        of suppressed nodes, and then filtered only by any provided values in the 'withDisclosureIntents'.
        """
        return cls.execute_soa_method(
            method_name='startFindModelViews',
            library='Cad',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'findInput': findInput},
            response_cls=FindModelViewsResponse,
        )

    @classmethod
    def startReconcilePalette(cls, reconcilePaletteInput: ReconcilePaletteInput) -> ReconcilePaletteResponse:
        """
        This operation starts the reconciliation of Fnd0ModelViewProxy object references in a Fnd0ModelViewPalette
        object for a given product structure and configuration. The Fnd0ModelViewProxy objects are authored and managed
        by  CAD applications, and their lifecycle is delegated to their CAD owning model's lifecycle.  As the CAD
        owning models are updated, so are their Fnd0ModelViewProxy objects.  However, the Fnd0ModelViewPalette objects
        that reference these Fnd0ModelViewProxy objects are not automatically updated during CAD model update in all
        cases, because there are times when this update needs to be carefully controlled by users.  Consequently, the
        Fnd0ModelViewPalette can get out of synchronization with the structure it is attached to. This service
        operation is provided to help reconcile differences between the loaded structure configuration and an existing
        Fnd0ModelViewPalette in a user controlled manner.  It provides the caller with information about which
        Fnd0ModelViewProxy objects should be removed and which should be replaced by analyzing the current configured
        structure and comparing it to what was found in an existing Fnd0ModelViewPalette.
        The Fnd0ModelViewPalette contains Fnd0ModelViewProxy object references for  components belonging to the product
        structure. When the components in the structure gets revised, cloned, removed, or a model view is deleted or
        unpublished, or when the structure configuration gets changed, the Fnd0ModelViewPalette needs to be reconciled
        against the current structure in order to get the proper Fnd0ModelViewProxy objects corresponding to the
        updated structure.  Using this operation, a list of Fnd0ModelViewProxy objects that need to be replace or
        removed for a given Fnd0ModelViewPalette can be identified, retrieved and presented to user, so that the user
        can carefully control the update of the Fnd0ModelViewPalette for the various update use cases.
        This operation is designed in such a way that the caller can use it in a threaded operation and display results
        in batches instead of waiting for the entire reconciliation process to be complete which may take a fair amount
        of time for large structures. This operation is thus supplemented by 'continueReconcilePalette' operation.
        Note: The reconcile process has to be closed by the caller using the 'continueReconcilePalette' operation with
        'stopReconcile' as true. For example the caller calls 'startReconcilePalette' operation followed by
        'continueReconcilePalette' operation. Once the finished variable is returned as true in the response the caller
        calls 'continueReconcilePalette' with 'stopReconcile' as true so that the resources are freed up in the server.
        
        Use cases:
        The operation supports the following use cases.
        Use Case 1 : Update a Fnd0ModelViewPalette per informal engineering change (i.e. overwrite)
        1. An authoring user creates a detailed design in a CAD application.  The user creates and publishes Model
        Views describing the design details. The Model Views are persisted in Teamcenter as Fnd0ModelViewProxy objects
        using the operation 'createOrUpdateModelViewProxies'.
        2. The authoring user opens a configured product structure in a visualization enabled Teamcenter application
        and finds the published Fnd0ModelViewProxy objects in the product structure using the operation
        'findModelViewsInStructure'.
        3. The authoring user selects a limited subset of the Fnd0ModelViewProxy objects found, adds them to a Palette,
        organizes them for presentation by re-ordering and grouping, and creates a Fnd0ModelViewPalette object in
        Teamcenter which references Fnd0ModelViewProxy objects using the operation 'createOrUpdateModelViewPalette'.
        4. A reviewing user opens the product structure configuration along with the Fnd0ModelViewPalette into a
        visualization enabled Teamcenter application, reviews each Model View for accuracy, creates review comments for
        changes that need to be made, and submits those changes to the CAD Designer that authored the original detailed
        design.
        5. The authoring user receives the review comments from various reviewing users, and uses the CAD application
        to make changes to the CAD model(s) such as add or remove components, reposition or change parts, add, delete,
        or change model views, publish or unpublish model views, etc.  The updated CAD models are saved to Teamcenter
        along with updated Fnd0ModelViewProxy objects using the operation 'createOrUpdateModelViewProxies'.  Since this
        is informal change, the CAD models are typically overwritten as opposed to revised.
        6. The authoring user opens the configured product structure with attached Fnd0ModelViewPalette created in step
        3 in a visualization enabled Teamcenter application, and some of the Fnd0ModelViewProxy objects referenced by
        the Fnd0ModelViewPalette are no longer valid relative to the current structure due to the CAD model changes. 
        The user invokes the palette reconcile action which triggers the operation 'startReconcilePalette' followed by
        'continueReconcilePalette'. The results are displayed to the user providing information on which
        Fnd0ModelViewProxy objects are still valid, which need to be replaced, and which need to be removed in order to
        update the Palette.  The results are streamed to the client  in batches, so the user is updated on progress and
        can choose to stop the reconcile operation at any time.
        7. The authoring user updates the Fnd0ModelViewPalette per the changes suggested by this operation, and saves
        the palette updates using the operation 'createOrUpdateModelViewPalette'.
        
        Use Case 2: Update a Fnd0ModelViewPalette to a different structure configuration
        1.The user opens a structure configuration different from that used to author the original Fnd0ModelViewPalette
        (per use case 1), and sends this to the visualization enabled palette authoring tool in Teamcenter.
        2.The user opens the Fnd0ModelViewPalette and invokes the palette reconcile action which triggers the operation
        'startReconcilePalette' followed by 'continueReconcilePalette'. The results are displayed to the user providing
        which Fnd0ModelViewProxy objects cannot be found, which are still valid, which need to be replaced, and which
        need to be removed in order to reconcile the Palette to the current structure configuration.  The results are
        streamed to the client  in batches, so the user is updated on progress and can choose to stop the reconcile
        operation at any time.
        3.The authoring user updates the Fnd0ModelViewPalette per the changes suggested by the operation, and saves the
        palette updates using the operation 'createOrUpdateModelViewPalette'. The updated structure configuration
        information used for the palette update is stored with the palette.
        
        Use Case 3 : Update a Fnd0ModelViewPalette per formal engineering change (i.e. Revise)
        1.The user of a CAD application makes changes to the CAD model(s) representing the detailed design such as
        revising components, add, delete, or change model views, publish or unpublish model views, etc during revise of
        a detailed design.  The revised CAD models are saved to Teamcenter, where new and updated Fnd0ModelViewProxy
        objects are published using the operation 'createOrUpdateModelViewProxies' and Teamcenter deep copy rules come
        into play.
        2.The user opens the configured product structure with attached Fnd0ModelViewPalette (see use case 1) in a
        visualization enabled Teamcenter application, and some of the Fnd0ModelViewProxy objects referenced by the
        Fnd0ModelViewPalette are no longer valid due to the revised CAD model(s).  Some of the Fnd0ModelViewProxy
        objects in the Fnd0ModelViewPalette are from previous revisions of the revised components, others cannot be
        found. The user invokes the palette reconcile action which triggers the operation 'startReconcilePalette'
        followed by 'continueReconcilePalette'. The results are displayed to the user providing information on which
        Fnd0ModelViewProxy objects are still valid, which need to be replaced with Fnd0ModelViewProxy objects on new
        revisions of the CAD models, and which need to be removed in order to update the Palette.  The results are
        streamed to the client  in batches, so the user is updated on progress and can choose to stop and restart the
        reconcile operation at any time.
        3.The user updates the Fnd0ModelViewPalette per the changes suggested by this operation, and saves the updated
        palette using the operation 'createOrUpdateModelViewPalette'.
        """
        return cls.execute_soa_method(
            method_name='startReconcilePalette',
            library='Cad',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'reconcilePaletteInput': reconcilePaletteInput},
            response_cls=ReconcilePaletteResponse,
        )
