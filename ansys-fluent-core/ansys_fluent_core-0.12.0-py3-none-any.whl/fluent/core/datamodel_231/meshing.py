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
        self.AddBoundaryLayers = self.__class__.AddBoundaryLayers(service, rules, "AddBoundaryLayers", path)
        self.AddBoundaryLayersForPartReplacement = self.__class__.AddBoundaryLayersForPartReplacement(service, rules, "AddBoundaryLayersForPartReplacement", path)
        self.AddBoundaryType = self.__class__.AddBoundaryType(service, rules, "AddBoundaryType", path)
        self.AddLocalSizingFTM = self.__class__.AddLocalSizingFTM(service, rules, "AddLocalSizingFTM", path)
        self.AddLocalSizingWTM = self.__class__.AddLocalSizingWTM(service, rules, "AddLocalSizingWTM", path)
        self.AddMultiZoneControls = self.__class__.AddMultiZoneControls(service, rules, "AddMultiZoneControls", path)
        self.AddShellBoundaryLayers = self.__class__.AddShellBoundaryLayers(service, rules, "AddShellBoundaryLayers", path)
        self.AddThickness = self.__class__.AddThickness(service, rules, "AddThickness", path)
        self.Capping = self.__class__.Capping(service, rules, "Capping", path)
        self.ChooseMeshControlOptions = self.__class__.ChooseMeshControlOptions(service, rules, "ChooseMeshControlOptions", path)
        self.ChoosePartReplacementOptions = self.__class__.ChoosePartReplacementOptions(service, rules, "ChoosePartReplacementOptions", path)
        self.CloseLeakage = self.__class__.CloseLeakage(service, rules, "CloseLeakage", path)
        self.ComplexMeshingRegions = self.__class__.ComplexMeshingRegions(service, rules, "ComplexMeshingRegions", path)
        self.ComputeSizeField = self.__class__.ComputeSizeField(service, rules, "ComputeSizeField", path)
        self.CreateBackgroundMesh = self.__class__.CreateBackgroundMesh(service, rules, "CreateBackgroundMesh", path)
        self.CreateCollarMesh = self.__class__.CreateCollarMesh(service, rules, "CreateCollarMesh", path)
        self.CreateComponentMesh = self.__class__.CreateComponentMesh(service, rules, "CreateComponentMesh", path)
        self.CreateContactPatch = self.__class__.CreateContactPatch(service, rules, "CreateContactPatch", path)
        self.CreateExternalFlowBoundaries = self.__class__.CreateExternalFlowBoundaries(service, rules, "CreateExternalFlowBoundaries", path)
        self.CreateGapCover = self.__class__.CreateGapCover(service, rules, "CreateGapCover", path)
        self.CreateLocalRefinementRegions = self.__class__.CreateLocalRefinementRegions(service, rules, "CreateLocalRefinementRegions", path)
        self.CreateOversetInterfaces = self.__class__.CreateOversetInterfaces(service, rules, "CreateOversetInterfaces", path)
        self.CreatePorousRegions = self.__class__.CreatePorousRegions(service, rules, "CreatePorousRegions", path)
        self.CreateRegions = self.__class__.CreateRegions(service, rules, "CreateRegions", path)
        self.DefineLeakageThreshold = self.__class__.DefineLeakageThreshold(service, rules, "DefineLeakageThreshold", path)
        self.DescribeGeometryAndFlow = self.__class__.DescribeGeometryAndFlow(service, rules, "DescribeGeometryAndFlow", path)
        self.DescribeOversetFeatures = self.__class__.DescribeOversetFeatures(service, rules, "DescribeOversetFeatures", path)
        self.ExtractEdges = self.__class__.ExtractEdges(service, rules, "ExtractEdges", path)
        self.ExtrudeVolumeMesh = self.__class__.ExtrudeVolumeMesh(service, rules, "ExtrudeVolumeMesh", path)
        self.GenerateInitialSurfaceMesh = self.__class__.GenerateInitialSurfaceMesh(service, rules, "GenerateInitialSurfaceMesh", path)
        self.GeneratePrisms = self.__class__.GeneratePrisms(service, rules, "GeneratePrisms", path)
        self.GenerateTheMultiZoneMesh = self.__class__.GenerateTheMultiZoneMesh(service, rules, "GenerateTheMultiZoneMesh", path)
        self.GenerateTheSurfaceMeshFTM = self.__class__.GenerateTheSurfaceMeshFTM(service, rules, "GenerateTheSurfaceMeshFTM", path)
        self.GenerateTheSurfaceMeshWTM = self.__class__.GenerateTheSurfaceMeshWTM(service, rules, "GenerateTheSurfaceMeshWTM", path)
        self.GenerateTheVolumeMeshFTM = self.__class__.GenerateTheVolumeMeshFTM(service, rules, "GenerateTheVolumeMeshFTM", path)
        self.GenerateTheVolumeMeshWTM = self.__class__.GenerateTheVolumeMeshWTM(service, rules, "GenerateTheVolumeMeshWTM", path)
        self.GeometrySetup = self.__class__.GeometrySetup(service, rules, "GeometrySetup", path)
        self.IdentifyConstructionSurfaces = self.__class__.IdentifyConstructionSurfaces(service, rules, "IdentifyConstructionSurfaces", path)
        self.IdentifyDeviatedFaces = self.__class__.IdentifyDeviatedFaces(service, rules, "IdentifyDeviatedFaces", path)
        self.IdentifyOrphans = self.__class__.IdentifyOrphans(service, rules, "IdentifyOrphans", path)
        self.IdentifyRegions = self.__class__.IdentifyRegions(service, rules, "IdentifyRegions", path)
        self.ImportBodyOfInfluenceGeometry = self.__class__.ImportBodyOfInfluenceGeometry(service, rules, "ImportBodyOfInfluenceGeometry", path)
        self.ImportGeometry = self.__class__.ImportGeometry(service, rules, "ImportGeometry", path)
        self.ImproveSurfaceMesh = self.__class__.ImproveSurfaceMesh(service, rules, "ImproveSurfaceMesh", path)
        self.ImproveVolumeMesh = self.__class__.ImproveVolumeMesh(service, rules, "ImproveVolumeMesh", path)
        self.LinearMeshPattern = self.__class__.LinearMeshPattern(service, rules, "LinearMeshPattern", path)
        self.LoadCADGeometry = self.__class__.LoadCADGeometry(service, rules, "LoadCADGeometry", path)
        self.LocalScopedSizingForPartReplacement = self.__class__.LocalScopedSizingForPartReplacement(service, rules, "LocalScopedSizingForPartReplacement", path)
        self.ManageZones = self.__class__.ManageZones(service, rules, "ManageZones", path)
        self.MeshFluidDomain = self.__class__.MeshFluidDomain(service, rules, "MeshFluidDomain", path)
        self.ModifyMeshRefinement = self.__class__.ModifyMeshRefinement(service, rules, "ModifyMeshRefinement", path)
        self.PartManagement = self.__class__.PartManagement(service, rules, "PartManagement", path)
        self.PartReplacementSettings = self.__class__.PartReplacementSettings(service, rules, "PartReplacementSettings", path)
        self.RemeshSurface = self.__class__.RemeshSurface(service, rules, "RemeshSurface", path)
        self.RunCustomJournal = self.__class__.RunCustomJournal(service, rules, "RunCustomJournal", path)
        self.SeparateContacts = self.__class__.SeparateContacts(service, rules, "SeparateContacts", path)
        self.SetUpPeriodicBoundaries = self.__class__.SetUpPeriodicBoundaries(service, rules, "SetUpPeriodicBoundaries", path)
        self.SetupBoundaryLayers = self.__class__.SetupBoundaryLayers(service, rules, "SetupBoundaryLayers", path)
        self.ShareTopology = self.__class__.ShareTopology(service, rules, "ShareTopology", path)
        self.SizeControlsTable = self.__class__.SizeControlsTable(service, rules, "SizeControlsTable", path)
        self.TransformVolumeMesh = self.__class__.TransformVolumeMesh(service, rules, "TransformVolumeMesh", path)
        self.UpdateBoundaries = self.__class__.UpdateBoundaries(service, rules, "UpdateBoundaries", path)
        self.UpdateRegionSettings = self.__class__.UpdateRegionSettings(service, rules, "UpdateRegionSettings", path)
        self.UpdateRegions = self.__class__.UpdateRegions(service, rules, "UpdateRegions", path)
        self.UpdateTheVolumeMesh = self.__class__.UpdateTheVolumeMesh(service, rules, "UpdateTheVolumeMesh", path)
        self.WrapMain = self.__class__.WrapMain(service, rules, "WrapMain", path)
        self.Write2dMesh = self.__class__.Write2dMesh(service, rules, "Write2dMesh", path)
        super().__init__(service, rules, path)

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.FTMRegionData = self.__class__.FTMRegionData(service, rules, path + [("FTMRegionData", "")])
            self.AreaUnit = self.__class__.AreaUnit(service, rules, path + [("AreaUnit", "")])
            self.EnableCleanCAD = self.__class__.EnableCleanCAD(service, rules, path + [("EnableCleanCAD", "")])
            self.EnableComplexMeshing = self.__class__.EnableComplexMeshing(service, rules, path + [("EnableComplexMeshing", "")])
            self.EnableOversetMeshing = self.__class__.EnableOversetMeshing(service, rules, path + [("EnableOversetMeshing", "")])
            self.EnablePrimeMeshing = self.__class__.EnablePrimeMeshing(service, rules, path + [("EnablePrimeMeshing", "")])
            self.InitialVersion = self.__class__.InitialVersion(service, rules, path + [("InitialVersion", "")])
            self.LengthUnit = self.__class__.LengthUnit(service, rules, path + [("LengthUnit", "")])
            self.NormalMode = self.__class__.NormalMode(service, rules, path + [("NormalMode", "")])
            self.VolumeUnit = self.__class__.VolumeUnit(service, rules, path + [("VolumeUnit", "")])
            super().__init__(service, rules, path)

        class FTMRegionData(PyMenu):
            """
            Singleton FTMRegionData.
            """
            def __init__(self, service, rules, path):
                self.AllOversetNameList = self.__class__.AllOversetNameList(service, rules, path + [("AllOversetNameList", "")])
                self.AllOversetSizeList = self.__class__.AllOversetSizeList(service, rules, path + [("AllOversetSizeList", "")])
                self.AllOversetTypeList = self.__class__.AllOversetTypeList(service, rules, path + [("AllOversetTypeList", "")])
                self.AllOversetVolumeFillList = self.__class__.AllOversetVolumeFillList(service, rules, path + [("AllOversetVolumeFillList", "")])
                self.AllRegionFilterCategories = self.__class__.AllRegionFilterCategories(service, rules, path + [("AllRegionFilterCategories", "")])
                self.AllRegionLeakageSizeList = self.__class__.AllRegionLeakageSizeList(service, rules, path + [("AllRegionLeakageSizeList", "")])
                self.AllRegionLinkedConstructionSurfaceList = self.__class__.AllRegionLinkedConstructionSurfaceList(service, rules, path + [("AllRegionLinkedConstructionSurfaceList", "")])
                self.AllRegionMeshMethodList = self.__class__.AllRegionMeshMethodList(service, rules, path + [("AllRegionMeshMethodList", "")])
                self.AllRegionNameList = self.__class__.AllRegionNameList(service, rules, path + [("AllRegionNameList", "")])
                self.AllRegionOversetComponenList = self.__class__.AllRegionOversetComponenList(service, rules, path + [("AllRegionOversetComponenList", "")])
                self.AllRegionSizeList = self.__class__.AllRegionSizeList(service, rules, path + [("AllRegionSizeList", "")])
                self.AllRegionSourceList = self.__class__.AllRegionSourceList(service, rules, path + [("AllRegionSourceList", "")])
                self.AllRegionTypeList = self.__class__.AllRegionTypeList(service, rules, path + [("AllRegionTypeList", "")])
                self.AllRegionVolumeFillList = self.__class__.AllRegionVolumeFillList(service, rules, path + [("AllRegionVolumeFillList", "")])
                super().__init__(service, rules, path)

            class AllOversetNameList(PyTextual):
                """
                Parameter AllOversetNameList of value type List[str].
                """
                pass

            class AllOversetSizeList(PyTextual):
                """
                Parameter AllOversetSizeList of value type List[str].
                """
                pass

            class AllOversetTypeList(PyTextual):
                """
                Parameter AllOversetTypeList of value type List[str].
                """
                pass

            class AllOversetVolumeFillList(PyTextual):
                """
                Parameter AllOversetVolumeFillList of value type List[str].
                """
                pass

            class AllRegionFilterCategories(PyTextual):
                """
                Parameter AllRegionFilterCategories of value type List[str].
                """
                pass

            class AllRegionLeakageSizeList(PyTextual):
                """
                Parameter AllRegionLeakageSizeList of value type List[str].
                """
                pass

            class AllRegionLinkedConstructionSurfaceList(PyTextual):
                """
                Parameter AllRegionLinkedConstructionSurfaceList of value type List[str].
                """
                pass

            class AllRegionMeshMethodList(PyTextual):
                """
                Parameter AllRegionMeshMethodList of value type List[str].
                """
                pass

            class AllRegionNameList(PyTextual):
                """
                Parameter AllRegionNameList of value type List[str].
                """
                pass

            class AllRegionOversetComponenList(PyTextual):
                """
                Parameter AllRegionOversetComponenList of value type List[str].
                """
                pass

            class AllRegionSizeList(PyTextual):
                """
                Parameter AllRegionSizeList of value type List[str].
                """
                pass

            class AllRegionSourceList(PyTextual):
                """
                Parameter AllRegionSourceList of value type List[str].
                """
                pass

            class AllRegionTypeList(PyTextual):
                """
                Parameter AllRegionTypeList of value type List[str].
                """
                pass

            class AllRegionVolumeFillList(PyTextual):
                """
                Parameter AllRegionVolumeFillList of value type List[str].
                """
                pass

        class AreaUnit(PyTextual):
            """
            Parameter AreaUnit of value type str.
            """
            pass

        class EnableCleanCAD(PyParameter):
            """
            Parameter EnableCleanCAD of value type bool.
            """
            pass

        class EnableComplexMeshing(PyParameter):
            """
            Parameter EnableComplexMeshing of value type bool.
            """
            pass

        class EnableOversetMeshing(PyParameter):
            """
            Parameter EnableOversetMeshing of value type bool.
            """
            pass

        class EnablePrimeMeshing(PyParameter):
            """
            Parameter EnablePrimeMeshing of value type bool.
            """
            pass

        class InitialVersion(PyTextual):
            """
            Parameter InitialVersion of value type str.
            """
            pass

        class LengthUnit(PyTextual):
            """
            Parameter LengthUnit of value type str.
            """
            pass

        class NormalMode(PyParameter):
            """
            Parameter NormalMode of value type bool.
            """
            pass

        class VolumeUnit(PyTextual):
            """
            Parameter VolumeUnit of value type str.
            """
            pass

    class AddBoundaryLayers(PyCommand):
        """
        Command AddBoundaryLayers.

        Parameters
        ----------
        AddChild : str
        ReadPrismControlFile : str
        BLControlName : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        TransitionRatio : float
        Rate : float
        FirstHeight : float
        FaceScope : Dict[str, Any]
        RegionScope : List[str]
        BlLabelList : List[str]
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LocalPrismPreferences : Dict[str, Any]
        BLZoneList : List[str]
        BLRegionList : List[str]
        CompleteRegionScope : List[str]
        CompleteBlLabelList : List[str]
        CompleteBLZoneList : List[str]
        CompleteBLRegionList : List[str]
        CompleteZoneSelectionList : List[str]
        CompleteLabelSelectionList : List[str]

        Returns
        -------
        bool
        """
        pass

    class AddBoundaryLayersForPartReplacement(PyCommand):
        """
        Command AddBoundaryLayersForPartReplacement.

        Parameters
        ----------
        AddChild : str
        ReadPrismControlFile : str
        BLControlName : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        TransitionRatio : float
        Rate : float
        FirstHeight : float
        FaceScope : Dict[str, Any]
        RegionScope : List[str]
        BlLabelList : List[str]
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LocalPrismPreferences : Dict[str, Any]
        BLZoneList : List[str]
        BLRegionList : List[str]
        CompleteRegionScope : List[str]
        CompleteBlLabelList : List[str]
        CompleteBLZoneList : List[str]
        CompleteBLRegionList : List[str]
        CompleteZoneSelectionList : List[str]
        CompleteLabelSelectionList : List[str]

        Returns
        -------
        bool
        """
        pass

    class AddBoundaryType(PyCommand):
        """
        Command AddBoundaryType.

        Parameters
        ----------
        MeshObject : str
        NewBoundaryLabelName : str
        NewBoundaryType : str
        BoundaryFaceZoneList : List[str]
        Merge : str
        ZoneLocation : List[str]

        Returns
        -------
        bool
        """
        pass

    class AddLocalSizingFTM(PyCommand):
        """
        Command AddLocalSizingFTM.

        Parameters
        ----------
        LocalSettingsName : str
        SelectionType : str
        ObjectSelectionList : List[str]
        LabelSelectionList : List[str]
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        EdgeSelectionList : List[str]
        LocalSizeControlParameters : Dict[str, Any]
        ValueChanged : str
        CompleteZoneSelectionList : List[str]
        CompleteLabelSelectionList : List[str]
        CompleteObjectSelectionList : List[str]
        CompleteEdgeSelectionList : List[str]

        Returns
        -------
        bool
        """
        pass

    class AddLocalSizingWTM(PyCommand):
        """
        Command AddLocalSizingWTM.

        Parameters
        ----------
        AddChild : str
        BOIControlName : str
        BOIGrowthRate : float
        BOIExecution : str
        BOISize : float
        BOIMinSize : float
        BOIMaxSize : float
        BOICurvatureNormalAngle : float
        BOICellsPerGap : float
        BOIScopeTo : str
        IgnoreOrientation : str
        BOIZoneorLabel : str
        BOIFaceLabelList : List[str]
        BOIFaceZoneList : List[str]
        EdgeLabelList : List[str]
        TopologyList : List[str]
        BOIPatchingtoggle : bool
        DrawSizeControl : bool
        ZoneLocation : List[str]
        CompleteFaceZoneList : List[str]
        CompleteFaceLabelList : List[str]
        CompleteEdgeLabelList : List[str]
        CompleteTopologyList : List[str]

        Returns
        -------
        bool
        """
        pass

    class AddMultiZoneControls(PyCommand):
        """
        Command AddMultiZoneControls.

        Parameters
        ----------
        ControlType : str
        MultiZName : str
        MeshMethod : str
        FillWith : str
        UseSweepSize : str
        MaxSweepSize : float
        RegionScope : List[str]
        SourceMethod : str
        ParallelSelection : bool
        LabelSourceList : List[str]
        ZoneSourceList : List[str]
        ZoneLocation : List[str]
        AssignSizeUsing : str
        Intervals : int
        Size : float
        SmallestHeight : float
        BiasMethod : str
        GrowthMethod : str
        GrowthRate : float
        BiasFactor : float
        EdgeLabelList : List[str]
        CFDSurfaceMeshControls : Dict[str, Any]
        CompleteRegionScope : List[str]
        CompleteEdgeScope : List[str]

        Returns
        -------
        bool
        """
        pass

    class AddShellBoundaryLayers(PyCommand):
        """
        Command AddShellBoundaryLayers.

        Parameters
        ----------
        AddChild : str
        BLControlName : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        LastAspectRatio : float
        Rate : float
        FirstHeight : float
        FaceLabelList : List[str]
        EdgeLabelList : List[str]
        PrimeShellBLPreferences : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class AddThickness(PyCommand):
        """
        Command AddThickness.

        Parameters
        ----------
        ZeroThicknessName : str
        SelectionType : str
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        ObjectSelectionList : List[str]
        LabelSelectionList : List[str]
        Distance : float

        Returns
        -------
        bool
        """
        pass

    class Capping(PyCommand):
        """
        Command Capping.

        Parameters
        ----------
        PatchName : str
        ZoneType : str
        PatchType : str
        SelectionType : str
        LabelSelectionList : List[str]
        ZoneSelectionList : List[str]
        TopologyList : List[str]
        CreatePatchPreferences : Dict[str, Any]
        ObjectAssociation : str
        NewObjectName : str
        PatchObjectName : str
        CapLabels : List[str]
        ZoneLocation : List[str]
        CompleteZoneSelectionList : List[str]
        CompleteLabelSelectionList : List[str]
        CompleteTopologyList : List[str]

        Returns
        -------
        bool
        """
        pass

    class ChooseMeshControlOptions(PyCommand):
        """
        Command ChooseMeshControlOptions.

        Parameters
        ----------
        ReadOrCreate : str
        SizeControlFileName : str
        WrapSizeControlFileName : str
        CreationMethod : str
        ViewOption : str
        GlobalMin : float
        GlobalMax : float
        GlobalGrowthRate : float
        MeshControlOptions : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class ChoosePartReplacementOptions(PyCommand):
        """
        Command ChoosePartReplacementOptions.

        Parameters
        ----------
        AddPartManagement : str
        AddPartReplacement : str
        AddLocalSizing : str
        AddBoundaryLayer : str
        AddUpdateTheVolumeMesh : str

        Returns
        -------
        bool
        """
        pass

    class CloseLeakage(PyCommand):
        """
        Command CloseLeakage.

        Parameters
        ----------
        CloseLeakageOption : bool

        Returns
        -------
        bool
        """
        pass

    class ComplexMeshingRegions(PyCommand):
        """
        Command ComplexMeshingRegions.

        Parameters
        ----------
        ComplexMeshingRegionsOption : bool

        Returns
        -------
        bool
        """
        pass

    class ComputeSizeField(PyCommand):
        """
        Command ComputeSizeField.

        Parameters
        ----------
        ComputeSizeFieldControl : str

        Returns
        -------
        bool
        """
        pass

    class CreateBackgroundMesh(PyCommand):
        """
        Command CreateBackgroundMesh.

        Parameters
        ----------
        RefinementRegionsName : str
        CreationMethod : str
        BOIMaxSize : float
        BOISizeName : str
        SelectionType : str
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        ObjectSelectionList : List[str]
        ZoneSelectionSingle : List[str]
        ObjectSelectionSingle : List[str]
        BoundingBoxObject : Dict[str, Any]
        OffsetObject : Dict[str, Any]
        CylinderObject : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class CreateCollarMesh(PyCommand):
        """
        Command CreateCollarMesh.

        Parameters
        ----------
        RefinementRegionsName : str
        CreationMethod : str
        BOIMaxSize : float
        BOISizeName : str
        SelectionType : str
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        ObjectSelectionList : List[str]
        ZoneSelectionSingle : List[str]
        ObjectSelectionSingle : List[str]
        BoundingBoxObject : Dict[str, Any]
        OffsetObject : Dict[str, Any]
        CylinderObject : Dict[str, Any]
        VolumeFill : str

        Returns
        -------
        bool
        """
        pass

    class CreateComponentMesh(PyCommand):
        """
        Command CreateComponentMesh.

        Parameters
        ----------
        RefinementRegionsName : str
        CreationMethod : str
        BOIMaxSize : float
        BOISizeName : str
        SelectionType : str
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        ObjectSelectionList : List[str]
        ZoneSelectionSingle : List[str]
        ObjectSelectionSingle : List[str]
        BoundingBoxObject : Dict[str, Any]
        OffsetObject : Dict[str, Any]
        CylinderObject : Dict[str, Any]
        VolumeFill : str

        Returns
        -------
        bool
        """
        pass

    class CreateContactPatch(PyCommand):
        """
        Command CreateContactPatch.

        Parameters
        ----------
        ContactPatchName : str
        SelectionType : str
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        ObjectSelectionList : List[str]
        LabelSelectionList : List[str]
        GroundZoneSelectionList : List[str]
        Distance : float
        FeatureAngle : float
        PatchHole : bool
        FlipDirection : bool

        Returns
        -------
        bool
        """
        pass

    class CreateExternalFlowBoundaries(PyCommand):
        """
        Command CreateExternalFlowBoundaries.

        Parameters
        ----------
        ExternalBoundariesName : str
        CreationMethod : str
        ExtractionMethod : str
        SelectionType : str
        ObjectSelectionList : List[str]
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        ObjectSelectionSingle : List[str]
        ZoneSelectionSingle : List[str]
        LabelSelectionSingle : List[str]
        OriginalObjectName : str
        BoundingBoxObject : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class CreateGapCover(PyCommand):
        """
        Command CreateGapCover.

        Parameters
        ----------
        GapCoverName : str
        SizingMethod : str
        GapSizeRatio : float
        GapSize : float
        SelectionType : str
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        ObjectSelectionList : List[str]
        GapCoverBetweenZones : str
        GapCoverRefineFactor : float
        RefineWrapperBeforeProjection : str
        AdvancedOptions : bool
        MaxIslandFaceForGapCover : int
        GapCoverFeatureImprint : str

        Returns
        -------
        bool
        """
        pass

    class CreateLocalRefinementRegions(PyCommand):
        """
        Command CreateLocalRefinementRegions.

        Parameters
        ----------
        RefinementRegionsName : str
        CreationMethod : str
        BOIMaxSize : float
        BOISizeName : str
        SelectionType : str
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        ObjectSelectionList : List[str]
        ZoneSelectionSingle : List[str]
        ObjectSelectionSingle : List[str]
        BoundingBoxObject : Dict[str, Any]
        OffsetObject : Dict[str, Any]
        CylinderObject : Dict[str, Any]
        VolumeFill : str

        Returns
        -------
        bool
        """
        pass

    class CreateOversetInterfaces(PyCommand):
        """
        Command CreateOversetInterfaces.

        Parameters
        ----------
        OversetInterfacesName : str
        ObjectSelectionList : List[str]

        Returns
        -------
        bool
        """
        pass

    class CreatePorousRegions(PyCommand):
        """
        Command CreatePorousRegions.

        Parameters
        ----------
        InputMethod : str
        PorousRegionName : str
        FileName : str
        Location : str
        CellSizeP1P2 : float
        CellSizeP1P3 : float
        CellSizeP1P4 : float
        BufferSizeRatio : float
        P1 : List[float]
        P2 : List[float]
        P3 : List[float]
        P4 : List[float]
        NonRectangularParameters : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class CreateRegions(PyCommand):
        """
        Command CreateRegions.

        Parameters
        ----------
        NumberOfFlowVolumes : int
        RetainDeadRegionName : str
        MeshObject : str

        Returns
        -------
        bool
        """
        pass

    class DefineLeakageThreshold(PyCommand):
        """
        Command DefineLeakageThreshold.

        Parameters
        ----------
        AddChild : str
        LeakageName : str
        SelectionType : str
        DeadRegionsList : List[str]
        RegionSelectionSingle : List[str]
        DeadRegionsSize : float
        PlaneClippingValue : int
        PlaneDirection : str
        FlipDirection : bool

        Returns
        -------
        bool
        """
        pass

    class DescribeGeometryAndFlow(PyCommand):
        """
        Command DescribeGeometryAndFlow.

        Parameters
        ----------
        FlowType : str
        GeometryOptions : bool
        AddEnclosure : str
        CloseCaps : str
        LocalRefinementRegions : str
        DescribeGeometryAndFlowOptions : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class DescribeOversetFeatures(PyCommand):
        """
        Command DescribeOversetFeatures.

        Parameters
        ----------
        AdvancedOptions : bool
        ComponentGrid : str
        CollarGrid : str
        BackgroundMesh : str
        OversetInterfaces : str

        Returns
        -------
        bool
        """
        pass

    class ExtractEdges(PyCommand):
        """
        Command ExtractEdges.

        Parameters
        ----------
        ExtractEdgesName : str
        ExtractMethodType : str
        SelectionType : str
        ObjectSelectionList : List[str]
        GeomObjectSelectionList : List[str]
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        FeatureAngleLocal : int
        IndividualCollective : str
        SharpAngle : int
        CompleteObjectSelectionList : List[str]
        CompleteGeomObjectSelectionList : List[str]
        NonExtractedObjects : List[str]

        Returns
        -------
        bool
        """
        pass

    class ExtrudeVolumeMesh(PyCommand):
        """
        Command ExtrudeVolumeMesh.

        Parameters
        ----------
        MExControlName : str
        Method : str
        ExternalBoundaryZoneList : List[str]
        TotalHeight : float
        FirstHeight : float
        NumberofLayers : int
        GrowthRate : float
        VMExtrudePreferences : Dict[str, Any]
        ZoneLocation : List[str]

        Returns
        -------
        bool
        """
        pass

    class GenerateInitialSurfaceMesh(PyCommand):
        """
        Command GenerateInitialSurfaceMesh.

        Parameters
        ----------
        MinSize : float
        MaxSize : float
        GrowthRate : float
        SizeFunctions : str
        CurvatureNormalAngle : float
        CellsPerGap : float
        PrimeMeshPreferences : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class GeneratePrisms(PyCommand):
        """
        Command GeneratePrisms.

        Parameters
        ----------
        GeneratePrismsOption : bool

        Returns
        -------
        bool
        """
        pass

    class GenerateTheMultiZoneMesh(PyCommand):
        """
        Command GenerateTheMultiZoneMesh.

        Parameters
        ----------
        OrthogonalQualityLimit : float
        RegionScope : List[str]
        NonConformal : str
        SizeFunctionScaleFactor : float
        CFDSurfaceMeshControls : Dict[str, Any]
        CompleteRegionScope : List[str]

        Returns
        -------
        bool
        """
        pass

    class GenerateTheSurfaceMeshFTM(PyCommand):
        """
        Command GenerateTheSurfaceMeshFTM.

        Parameters
        ----------
        SurfaceQuality : float
        SaveSurfaceMesh : bool
        AdvancedOptions : bool
        SaveIntermediateFiles : str
        IntermediateFileName : str
        SeparateSurface : str
        AutoPairing : str
        ParallelSerialOption : str
        NumberOfSessions : int
        MaxIslandFace : int
        SpikeRemovalAngle : float
        DihedralMinAngle : float
        ProjectOnGeometry : str
        AutoAssignZoneTypes : str
        AdvancedInnerWrap : str
        GapCoverZoneRecovery : str
        GlobalMin : float
        ShowSubTasks : str

        Returns
        -------
        bool
        """
        pass

    class GenerateTheSurfaceMeshWTM(PyCommand):
        """
        Command GenerateTheSurfaceMeshWTM.

        Parameters
        ----------
        CFDSurfaceMeshControls : Dict[str, Any]
        SeparationRequired : str
        SeparationAngle : float
        RemeshSelectionType : str
        RemeshZoneList : List[str]
        RemeshLabelList : List[str]
        SurfaceMeshPreferences : Dict[str, Any]
        ImportType : str
        AppendMesh : bool
        CadFacetingFileName : str
        Directory : str
        Pattern : str
        LengthUnit : str
        TesselationMethod : str
        OriginalZones : List[str]
        ExecuteShareTopology : str
        CADFacetingControls : Dict[str, Any]
        CadImportOptions : Dict[str, Any]
        ShareTopologyPreferences : Dict[str, Any]
        PreviewSizeToggle : bool

        Returns
        -------
        bool
        """
        pass

    class GenerateTheVolumeMeshFTM(PyCommand):
        """
        Command GenerateTheVolumeMeshFTM.

        Parameters
        ----------
        MeshQuality : float
        OrthogonalQuality : float
        EnableParallel : bool
        SaveVolumeMesh : bool
        EditVolumeSettings : bool
        RegionNameList : List[str]
        RegionVolumeFillList : List[str]
        RegionSizeList : List[str]
        OldRegionNameList : List[str]
        OldRegionVolumeFillList : List[str]
        OldRegionSizeList : List[str]
        AllRegionNameList : List[str]
        AllRegionVolumeFillList : List[str]
        AllRegionSizeList : List[str]
        AdvancedOptions : bool
        SpikeRemovalAngle : float
        DihedralMinAngle : float
        AvoidHangingNodes : str
        OctreePeelLayers : int
        FillWithSizeField : str
        OctreeBoundaryFaceSizeRatio : float
        GlobalBufferLayers : int
        TetPolyGrowthRate : float
        ConformalPrismSplit : str
        ShowSubTasks : str

        Returns
        -------
        bool
        """
        pass

    class GenerateTheVolumeMeshWTM(PyCommand):
        """
        Command GenerateTheVolumeMeshWTM.

        Parameters
        ----------
        Solver : str
        VolumeFill : str
        MeshFluidRegions : bool
        MeshSolidRegions : bool
        SizingMethod : str
        VolumeFillControls : Dict[str, Any]
        RegionBasedPreferences : bool
        ReMergeZones : str
        ParallelMeshing : bool
        VolumeMeshPreferences : Dict[str, Any]
        PrismPreferences : Dict[str, Any]
        InvokePrimsControl : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        TransitionRatio : float
        Rate : float
        FirstHeight : float
        MeshObject : str
        MeshDeadRegions : bool
        BodyLabelList : List[str]
        PrismLayers : bool
        QuadTetTransition : str
        MergeCellZones : bool
        FaceScope : Dict[str, Any]
        RegionTetNameList : List[str]
        RegionTetMaxCellLengthList : List[str]
        RegionTetGrowthRateList : List[str]
        RegionHexNameList : List[str]
        RegionHexMaxCellLengthList : List[str]
        OldRegionTetMaxCellLengthList : List[str]
        OldRegionTetGrowthRateList : List[str]
        OldRegionHexMaxCellLengthList : List[str]
        CFDSurfaceMeshControls : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class GeometrySetup(PyCommand):
        """
        Command GeometrySetup.

        Parameters
        ----------
        SetupType : str
        CappingRequired : str
        WallToInternal : str
        InvokeShareTopology : str
        NonConformal : str
        Multizone : str
        SetupInternals : List[str]
        SetupInternalTypes : List[str]
        OldZoneList : List[str]
        OldZoneTypeList : List[str]
        RegionList : List[str]
        EdgeLabels : List[str]
        SMImprovePreferences : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class IdentifyConstructionSurfaces(PyCommand):
        """
        Command IdentifyConstructionSurfaces.

        Parameters
        ----------
        MRFName : str
        CreationMethod : str
        SelectionType : str
        ObjectSelectionSingle : List[str]
        ZoneSelectionSingle : List[str]
        LabelSelectionSingle : List[str]
        ObjectSelectionList : List[str]
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        DefeaturingSize : float
        OffsetHeight : float
        Pivot : Dict[str, Any]
        Axis : Dict[str, Any]
        Rotation : Dict[str, Any]
        CylinderObject : Dict[str, Any]
        BoundingBoxObject : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class IdentifyDeviatedFaces(PyCommand):
        """
        Command IdentifyDeviatedFaces.

        Parameters
        ----------
        DisplayGridName : str
        SelectionType : str
        ObjectSelectionList : List[str]
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        AdvancedOptions : bool
        DeviationMinValue : float
        DeviationMaxValue : float
        Overlay : str
        IncludeGapCoverGeometry : str

        Returns
        -------
        bool
        """
        pass

    class IdentifyOrphans(PyCommand):
        """
        Command IdentifyOrphans.

        Parameters
        ----------
        NumberOfOrphans : str
        ObjectSelectionList : List[str]
        EnableGridPriority : bool
        DonorPriorityMethod : str
        OverlapBoundaries : str
        CheckOversetInterfaceIntersection : str
        RegionNameList : List[str]
        RegionSizeList : List[str]
        OldRegionNameList : List[str]
        OldRegionSizeList : List[str]

        Returns
        -------
        bool
        """
        pass

    class IdentifyRegions(PyCommand):
        """
        Command IdentifyRegions.

        Parameters
        ----------
        AddChild : str
        MaterialPointsName : str
        MptMethodType : str
        NewRegionType : str
        LinkConstruction : str
        SelectionType : str
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        LabelSelectionList : List[str]
        ObjectSelectionList : List[str]
        GraphicalSelection : bool
        ShowCoordinates : bool
        X : float
        Y : float
        Z : float
        OffsetX : float
        OffsetY : float
        OffsetZ : float

        Returns
        -------
        bool
        """
        pass

    class ImportBodyOfInfluenceGeometry(PyCommand):
        """
        Command ImportBodyOfInfluenceGeometry.

        Parameters
        ----------
        LengthUnit : str
        Type : str
        GeometryFileName : str
        MeshFileName : str
        ImportedObjects : List[str]
        CadImportOptions : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class ImportGeometry(PyCommand):
        """
        Command ImportGeometry.

        Parameters
        ----------
        FileFormat : str
        LengthUnit : str
        MeshUnit : str
        ImportCadPreferences : Dict[str, Any]
        FileName : str
        FileNames : str
        MeshFileName : str
        NumParts : float
        ImportType : str
        AppendMesh : bool
        Directory : str
        Pattern : str
        CadImportOptions : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class ImproveSurfaceMesh(PyCommand):
        """
        Command ImproveSurfaceMesh.

        Parameters
        ----------
        MeshObject : str
        FaceQualityLimit : float
        SQMinSize : float
        SMImprovePreferences : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class ImproveVolumeMesh(PyCommand):
        """
        Command ImproveVolumeMesh.

        Parameters
        ----------
        CellQualityLimit : float
        VMImprovePreferences : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class LinearMeshPattern(PyCommand):
        """
        Command LinearMeshPattern.

        Parameters
        ----------
        ChildName : str
        ObjectList : List[str]
        AutoPopulateVector : str
        PatternVector : Dict[str, Any]
        Pitch : float
        NumberOfUnits : int
        CheckOverlappingFaces : str
        BatteryModelingOptions : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class LoadCADGeometry(PyCommand):
        """
        Command LoadCADGeometry.

        Parameters
        ----------
        FileName : str
        LengthUnit : str
        Route : str
        CreateObjectPer : str
        NumParts : float
        2DRefaceting : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class LocalScopedSizingForPartReplacement(PyCommand):
        """
        Command LocalScopedSizingForPartReplacement.

        Parameters
        ----------
        LocalSettingsName : str
        SelectionType : str
        ObjectSelectionList : List[str]
        LabelSelectionList : List[str]
        ZoneSelectionList : List[str]
        ZoneLocation : List[str]
        EdgeSelectionList : List[str]
        LocalSizeControlParameters : Dict[str, Any]
        ValueChanged : str
        CompleteZoneSelectionList : List[str]
        CompleteLabelSelectionList : List[str]
        CompleteObjectSelectionList : List[str]
        CompleteEdgeSelectionList : List[str]

        Returns
        -------
        bool
        """
        pass

    class ManageZones(PyCommand):
        """
        Command ManageZones.

        Parameters
        ----------
        Type : str
        ZoneFilter : str
        SizeFilter : str
        Area : float
        Volume : float
        EqualRange : float
        ZoneOrLabel : str
        LabelList : List[str]
        ManageFaceZoneList : List[str]
        ManageCellZoneList : List[str]
        BodyLabelList : List[str]
        Operation : str
        OperationName : str
        MZChildName : str
        AddPrefixName : str
        FaceMerge : str
        Angle : float
        ZoneList : List[str]
        ZoneLocation : List[str]

        Returns
        -------
        bool
        """
        pass

    class MeshFluidDomain(PyCommand):
        """
        Command MeshFluidDomain.

        Parameters
        ----------
        MeshFluidDomainOption : bool

        Returns
        -------
        bool
        """
        pass

    class ModifyMeshRefinement(PyCommand):
        """
        Command ModifyMeshRefinement.

        Parameters
        ----------
        MeshObject : str
        RemeshExecution : str
        RemeshControlName : str
        LocalSize : float
        FaceZoneOrLabel : str
        RemeshFaceZoneList : List[str]
        RemeshFaceLabelList : List[str]
        SizingType : str
        LocalMinSize : float
        LocalMaxSize : float
        RemeshGrowthRate : float
        RemeshCurvatureNormalAngle : float
        RemeshCellsPerGap : float
        CFDSurfaceMeshControls : Dict[str, Any]
        RemeshPreferences : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class PartManagement(PyCommand):
        """
        Command PartManagement.

        Parameters
        ----------
        FileLoaded : str
        FMDFileName : str
        AppendFileName : str
        Append : bool
        LengthUnit : str
        CreateObjectPer : str
        FileLengthUnit : str
        FileLengthUnitAppend : str
        Route : str
        RouteAppend : str
        JtLOD : str
        JtLODAppend : str
        PartPerBody : bool
        PrefixParentName : bool
        RemoveEmptyParts : bool
        FeatureAngle : float
        OneZonePer : str
        Refaceting : Dict[str, Any]
        IgnoreSolidNames : bool
        IgnoreSolidNamesAppend : bool
        Options : Dict[str, Any]
        EdgeExtraction : str
        Context : int
        ObjectSetting : str

        Returns
        -------
        bool
        """
        pass

    class PartReplacementSettings(PyCommand):
        """
        Command PartReplacementSettings.

        Parameters
        ----------
        PartReplacementName : str
        ManagementMethod : str
        CreationMethod : str
        OldObjectSelectionList : List[str]
        NewObjectSelectionList : List[str]
        AdvancedOptions : bool
        ScalingFactor : float
        MptMethodType : str
        GraphicalSelection : bool
        ShowCoordinates : bool
        X : float
        Y : float
        Z : float

        Returns
        -------
        bool
        """
        pass

    class RemeshSurface(PyCommand):
        """
        Command RemeshSurface.

        Parameters
        ----------
        RemeshSurfaceOption : bool

        Returns
        -------
        bool
        """
        pass

    class RunCustomJournal(PyCommand):
        """
        Command RunCustomJournal.

        Parameters
        ----------
        JournalString : str

        Returns
        -------
        bool
        """
        pass

    class SeparateContacts(PyCommand):
        """
        Command SeparateContacts.

        Parameters
        ----------
        SeparateContactsOption : bool

        Returns
        -------
        bool
        """
        pass

    class SetUpPeriodicBoundaries(PyCommand):
        """
        Command SetUpPeriodicBoundaries.

        Parameters
        ----------
        MeshObject : str
        Type : str
        Method : str
        PeriodicityAngle : float
        LCSOrigin : Dict[str, Any]
        LCSVector : Dict[str, Any]
        TransShift : Dict[str, Any]
        SelectionType : str
        ZoneList : List[str]
        LabelList : List[str]
        RemeshBoundariesOption : str
        ZoneLocation : List[str]
        ListAllLabelToggle : bool

        Returns
        -------
        bool
        """
        pass

    class SetupBoundaryLayers(PyCommand):
        """
        Command SetupBoundaryLayers.

        Parameters
        ----------
        AddChild : str
        PrismsSettingsName : str
        AspectRatio : float
        GrowthRate : float
        OffsetMethodType : str
        LastRatioPercentage : float
        FirstHeight : float
        PrismLayers : int
        RegionSelectionList : List[str]

        Returns
        -------
        bool
        """
        pass

    class ShareTopology(PyCommand):
        """
        Command ShareTopology.

        Parameters
        ----------
        GapDistance : float
        GapDistanceConnect : float
        STMinSize : float
        InterfaceSelect : str
        ShareTopologyPreferences : Dict[str, Any]
        SMImprovePreferences : Dict[str, Any]
        SurfaceMeshPreferences : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class SizeControlsTable(PyCommand):
        """
        Command SizeControlsTable.

        Parameters
        ----------
        GlobalMin : float
        GlobalMax : float
        TargetGrowthRate : float
        DrawSizeControl : bool
        InitialSizeControl : bool
        TargetSizeControl : bool
        SizeControlInterval : float
        SizeControlParameters : Dict[str, Any]

        Returns
        -------
        bool
        """
        pass

    class TransformVolumeMesh(PyCommand):
        """
        Command TransformVolumeMesh.

        Parameters
        ----------
        MTControlName : str
        Type : str
        Method : str
        CellZoneList : List[str]
        LCSOrigin : Dict[str, Any]
        LCSVector : Dict[str, Any]
        TransShift : Dict[str, Any]
        Angle : float
        Copy : str
        NumOfCopies : int
        Merge : str
        Rename : str

        Returns
        -------
        bool
        """
        pass

    class UpdateBoundaries(PyCommand):
        """
        Command UpdateBoundaries.

        Parameters
        ----------
        MeshObject : str
        SelectionType : str
        BoundaryLabelList : List[str]
        BoundaryLabelTypeList : List[str]
        BoundaryZoneList : List[str]
        BoundaryZoneTypeList : List[str]
        OldBoundaryLabelList : List[str]
        OldBoundaryLabelTypeList : List[str]
        OldBoundaryZoneList : List[str]
        OldBoundaryZoneTypeList : List[str]
        OldLabelZoneList : List[str]
        ListAllBoundariesToggle : bool
        ZoneLocation : List[str]
        TopologyList : List[str]
        TopologyTypeList : List[str]
        OldTopologyList : List[str]
        OldTopologyTypeList : List[str]

        Returns
        -------
        bool
        """
        pass

    class UpdateRegionSettings(PyCommand):
        """
        Command UpdateRegionSettings.

        Parameters
        ----------
        MainFluidRegion : str
        FilterCategory : str
        RegionNameList : List[str]
        RegionMeshMethodList : List[str]
        RegionTypeList : List[str]
        RegionVolumeFillList : List[str]
        RegionLeakageSizeList : List[str]
        RegionOversetComponenList : List[str]
        OldRegionNameList : List[str]
        OldRegionMeshMethodList : List[str]
        OldRegionTypeList : List[str]
        OldRegionVolumeFillList : List[str]
        OldRegionLeakageSizeList : List[str]
        OldRegionOversetComponenList : List[str]
        AllRegionNameList : List[str]
        AllRegionMeshMethodList : List[str]
        AllRegionTypeList : List[str]
        AllRegionVolumeFillList : List[str]
        AllRegionLeakageSizeList : List[str]
        AllRegionOversetComponenList : List[str]
        AllRegionLinkedConstructionSurfaceList : List[str]
        AllRegionSourceList : List[str]
        AllRegionFilterCategories : List[str]

        Returns
        -------
        bool
        """
        pass

    class UpdateRegions(PyCommand):
        """
        Command UpdateRegions.

        Parameters
        ----------
        MeshObject : str
        RegionNameList : List[str]
        RegionTypeList : List[str]
        OldRegionNameList : List[str]
        OldRegionTypeList : List[str]
        RegionInternals : List[str]
        RegionInternalTypes : List[str]

        Returns
        -------
        bool
        """
        pass

    class UpdateTheVolumeMesh(PyCommand):
        """
        Command UpdateTheVolumeMesh.

        Parameters
        ----------
        EnableParallel : bool

        Returns
        -------
        bool
        """
        pass

    class WrapMain(PyCommand):
        """
        Command WrapMain.

        Parameters
        ----------
        WrapRegionsName : str

        Returns
        -------
        bool
        """
        pass

    class Write2dMesh(PyCommand):
        """
        Command Write2dMesh.

        Parameters
        ----------
        FileName : str

        Returns
        -------
        bool
        """
        pass

