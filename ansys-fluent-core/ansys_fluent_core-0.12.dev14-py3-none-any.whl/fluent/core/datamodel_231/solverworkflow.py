#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import (
    PyMenu,
    PyParameter,
    PyTextual,
    PyNumerical,
    PyDictionary,
    PyNamedObjectContainer,
    PyCommand
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
        self.JournalCommand = self.__class__.JournalCommand(service, rules, "JournalCommand", path)
        self.TWF_AssociateMesh = self.__class__.TWF_AssociateMesh(service, rules, "TWF_AssociateMesh", path)
        self.TWF_BasicMachineDescription = self.__class__.TWF_BasicMachineDescription(service, rules, "TWF_BasicMachineDescription", path)
        self.TWF_BladeRowAnalysisScope = self.__class__.TWF_BladeRowAnalysisScope(service, rules, "TWF_BladeRowAnalysisScope", path)
        self.TWF_CompleteWorkflowSetup = self.__class__.TWF_CompleteWorkflowSetup(service, rules, "TWF_CompleteWorkflowSetup", path)
        self.TWF_CreateCFDModel = self.__class__.TWF_CreateCFDModel(service, rules, "TWF_CreateCFDModel", path)
        self.TWF_ImportMesh = self.__class__.TWF_ImportMesh(service, rules, "TWF_ImportMesh", path)
        self.TWF_MapRegionInfo = self.__class__.TWF_MapRegionInfo(service, rules, "TWF_MapRegionInfo", path)
        self.TWF_ReportDefMonitors = self.__class__.TWF_ReportDefMonitors(service, rules, "TWF_ReportDefMonitors", path)
        self.TWF_TurboPhysics = self.__class__.TWF_TurboPhysics(service, rules, "TWF_TurboPhysics", path)
        self.TWF_TurboRegionsZones = self.__class__.TWF_TurboRegionsZones(service, rules, "TWF_TurboRegionsZones", path)
        self.TWF_TurboSurfaces = self.__class__.TWF_TurboSurfaces(service, rules, "TWF_TurboSurfaces", path)
        self.TWF_TurboTopology = self.__class__.TWF_TurboTopology(service, rules, "TWF_TurboTopology", path)
        super().__init__(service, rules, path)

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.EnableTurboMeshing = self.__class__.EnableTurboMeshing(service, rules, path + [("EnableTurboMeshing", "")])
            super().__init__(service, rules, path)

        class EnableTurboMeshing(PyParameter):
            """
            Parameter EnableTurboMeshing of value type bool.
            """
            pass

    class JournalCommand(PyCommand):
        """
        Command JournalCommand.

        Parameters
        ----------
        JournalString : str

        Returns
        -------
        bool
        """
        pass

    class TWF_AssociateMesh(PyCommand):
        """
        Command TWF_AssociateMesh.

        Parameters
        ----------
        AMChildName : str
        AMSelectComponentScope : str
        UseWireframe : bool
        RenameCellZones : str
        DefaultAMRowNumList : List[str]
        DefaultAMCellZonesList : List[str]
        AMRowNumList : List[str]
        OldAMCellZonesList : List[str]
        NewAMCellZonesList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_BasicMachineDescription(PyCommand):
        """
        Command TWF_BasicMachineDescription.

        Parameters
        ----------
        ComponentType : str
        ComponentName : str
        NumRows : int
        RowNumList : List[str]
        OldRowNameList : List[str]
        NewRowNameList : List[str]
        OldRowTypeList : List[str]
        NewRowTypeList : List[str]
        OldNumOfBladesList : List[str]
        NewNumOfBladesList : List[str]
        OldEnableTipGapList : List[str]
        NewEnableTipGapList : List[str]
        CombustorType : str

        Returns
        -------
        bool
        """
        pass

    class TWF_BladeRowAnalysisScope(PyCommand):
        """
        Command TWF_BladeRowAnalysisScope.

        Parameters
        ----------
        ASChildName : str
        ASSelectComponent : str
        ASRowNumList : List[str]
        OldASIncludeRowList : List[str]
        NewASIncludeRowList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_CompleteWorkflowSetup(PyCommand):
        """
        Command TWF_CompleteWorkflowSetup.


        Returns
        -------
        bool
        """
        pass

    class TWF_CreateCFDModel(PyCommand):
        """
        Command TWF_CreateCFDModel.

        Parameters
        ----------
        CFDMChildName : str
        CFDMSelectMeshAssociation : str
        AxisOfRotation : str
        DelayCFDModelCreation : bool
        RestrictToFactors : bool
        EstimateNumBlades : bool
        CFDMRowNumList : List[str]
        OldCFDMNumOfBladesList : List[str]
        NewCFDMNumOfBladesList : List[str]
        OldCFDMModelBladesList : List[str]
        NewCFDMModelBladesList : List[str]
        OldCFDMAngleOffset : List[str]
        NewCFDMAngleOffset : List[str]
        OldCFDMBladesPerSectorList : List[str]
        NewCFDMBladesPerSectorList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_ImportMesh(PyCommand):
        """
        Command TWF_ImportMesh.

        Parameters
        ----------
        AddChild : str
        MeshFilePath : str
        MeshFilePath_old : str
        MeshName : str
        CellZoneNames : List[str]
        ListItemLevels : List[str]
        ListItemTitles : List[str]
        ListOfCellZones : str

        Returns
        -------
        bool
        """
        pass

    class TWF_MapRegionInfo(PyCommand):
        """
        Command TWF_MapRegionInfo.

        Parameters
        ----------
        MRChildName : str
        MRSelectCellZone : str
        UseWireframe : bool
        DefaultMRRegionNameList : List[str]
        DefaultMRFaceZoneList : List[str]
        MRRegionNameList : List[str]
        OldMRFaceZoneList : List[str]
        NewMRFaceZoneList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_ReportDefMonitors(PyCommand):
        """
        Command TWF_ReportDefMonitors.

        Parameters
        ----------
        RDIsoSurfaceNumList : List[str]
        OldCreateContourList : List[str]
        NewCreateContourList : List[str]
        TurboContoursList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_TurboPhysics(PyCommand):
        """
        Command TWF_TurboPhysics.

        Parameters
        ----------
        States : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class TWF_TurboRegionsZones(PyCommand):
        """
        Command TWF_TurboRegionsZones.

        Parameters
        ----------
        States : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class TWF_TurboSurfaces(PyCommand):
        """
        Command TWF_TurboSurfaces.

        Parameters
        ----------
        NumIsoSurfaces : int
        IsoSurfaceNumList : List[str]
        OldIsoSurfaceNameList : List[str]
        NewIsoSurfaceNameList : List[str]
        OldIsoSurfaceValueList : List[str]
        NewIsoSurfaceValueList : List[str]
        SurfacesList : List[str]

        Returns
        -------
        bool
        """
        pass

    class TWF_TurboTopology(PyCommand):
        """
        Command TWF_TurboTopology.

        Parameters
        ----------
        TopologyName : str
        UseWireframe : bool
        DefaultTopologyNameList : List[str]
        DefaultTopologyZoneList : List[str]
        TopologyNameList : List[str]
        OldTopologyZoneList : List[str]
        NewTopologyZoneList : List[str]

        Returns
        -------
        bool
        """
        pass

