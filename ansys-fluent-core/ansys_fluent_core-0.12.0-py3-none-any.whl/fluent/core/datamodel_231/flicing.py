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
        self.Case = self.__class__.Case(service, rules, path + [("Case", "")])
        super().__init__(service, rules, path)

    class Case(PyMenu):
        """
        Singleton Case.
        """
        def __init__(self, service, rules, path):
            self.App = self.__class__.App(service, rules, path + [("App", "")])
            self.AppLocal = self.__class__.AppLocal(service, rules, path + [("AppLocal", "")])
            self.AuxiliaryInfo = self.__class__.AuxiliaryInfo(service, rules, path + [("AuxiliaryInfo", "")])
            self.CaseInfo = self.__class__.CaseInfo(service, rules, path + [("CaseInfo", "")])
            self.MeshInfo = self.__class__.MeshInfo(service, rules, path + [("MeshInfo", "")])
            self.Results = self.__class__.Results(service, rules, path + [("Results", "")])
            self.ResultsInfo = self.__class__.ResultsInfo(service, rules, path + [("ResultsInfo", "")])
            self.Setup = self.__class__.Setup(service, rules, path + [("Setup", "")])
            self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
            self.Streaming = self.__class__.Streaming(service, rules, path + [("Streaming", "")])
            self.AppName = self.__class__.AppName(service, rules, path + [("AppName", "")])
            self.ClearDatamodel = self.__class__.ClearDatamodel(service, rules, "ClearDatamodel", path)
            self.ReadCase = self.__class__.ReadCase(service, rules, "ReadCase", path)
            self.ReadCaseAndData = self.__class__.ReadCaseAndData(service, rules, "ReadCaseAndData", path)
            self.ReadData = self.__class__.ReadData(service, rules, "ReadData", path)
            self.SendCommand = self.__class__.SendCommand(service, rules, "SendCommand", path)
            self.WriteCase = self.__class__.WriteCase(service, rules, "WriteCase", path)
            self.WriteCaseAndData = self.__class__.WriteCaseAndData(service, rules, "WriteCaseAndData", path)
            self.WriteData = self.__class__.WriteData(service, rules, "WriteData", path)
            super().__init__(service, rules, path)

        class App(PyMenu):
            """
            Singleton App.
            """
            def __init__(self, service, rules, path):
                self.BC = self.__class__.BC(service, rules, path + [("BC", "")])
                self.Adaptation = self.__class__.Adaptation(service, rules, path + [("Adaptation", "")])
                self.Airflow = self.__class__.Airflow(service, rules, path + [("Airflow", "")])
                self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
                self.Ice = self.__class__.Ice(service, rules, path + [("Ice", "")])
                self.Particles = self.__class__.Particles(service, rules, path + [("Particles", "")])
                self.RunType = self.__class__.RunType(service, rules, path + [("RunType", "")])
                self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
                self.InProgress = self.__class__.InProgress(service, rules, path + [("InProgress", "")])
                self.IsBusy = self.__class__.IsBusy(service, rules, path + [("IsBusy", "")])
                self.SetupErrors = self.__class__.SetupErrors(service, rules, path + [("SetupErrors", "")])
                self.SetupWarnings = self.__class__.SetupWarnings(service, rules, path + [("SetupWarnings", "")])
                self.CheckSetup = self.__class__.CheckSetup(service, rules, "CheckSetup", path)
                self.IcingImportCase = self.__class__.IcingImportCase(service, rules, "IcingImportCase", path)
                self.IcingImportMesh = self.__class__.IcingImportMesh(service, rules, "IcingImportMesh", path)
                self.ImportCase = self.__class__.ImportCase(service, rules, "ImportCase", path)
                self.ImportMesh = self.__class__.ImportMesh(service, rules, "ImportMesh", path)
                self.InitAddOn = self.__class__.InitAddOn(service, rules, "InitAddOn", path)
                self.InitAddOnAero = self.__class__.InitAddOnAero(service, rules, "InitAddOnAero", path)
                self.InitDM = self.__class__.InitDM(service, rules, "InitDM", path)
                self.LoadCase = self.__class__.LoadCase(service, rules, "LoadCase", path)
                self.LoadCaseAndData = self.__class__.LoadCaseAndData(service, rules, "LoadCaseAndData", path)
                self.ReloadCase = self.__class__.ReloadCase(service, rules, "ReloadCase", path)
                self.ReloadDomain = self.__class__.ReloadDomain(service, rules, "ReloadDomain", path)
                self.SaveCase = self.__class__.SaveCase(service, rules, "SaveCase", path)
                self.SaveCaseAndData = self.__class__.SaveCaseAndData(service, rules, "SaveCaseAndData", path)
                self.SaveCaseAs = self.__class__.SaveCaseAs(service, rules, "SaveCaseAs", path)
                self.SaveData = self.__class__.SaveData(service, rules, "SaveData", path)
                self.SavePostCaseAndData = self.__class__.SavePostCaseAndData(service, rules, "SavePostCaseAndData", path)
                self.SendCommandQuiet = self.__class__.SendCommandQuiet(service, rules, "SendCommandQuiet", path)
                self.SyncDM = self.__class__.SyncDM(service, rules, "SyncDM", path)
                self.WriteAll = self.__class__.WriteAll(service, rules, "WriteAll", path)
                super().__init__(service, rules, path)

            class BC(PyNamedObjectContainer):
                """
                .
                """
                class _BC(PyMenu):
                    """
                    Singleton _BC.
                    """
                    def __init__(self, service, rules, path):
                        self.AirflowMassFlowInlet = self.__class__.AirflowMassFlowInlet(service, rules, path + [("AirflowMassFlowInlet", "")])
                        self.AirflowMassFlowOutlet = self.__class__.AirflowMassFlowOutlet(service, rules, path + [("AirflowMassFlowOutlet", "")])
                        self.AirflowPressureOutlet = self.__class__.AirflowPressureOutlet(service, rules, path + [("AirflowPressureOutlet", "")])
                        self.AirflowVelocityInlet = self.__class__.AirflowVelocityInlet(service, rules, path + [("AirflowVelocityInlet", "")])
                        self.AirflowWall = self.__class__.AirflowWall(service, rules, path + [("AirflowWall", "")])
                        self.Common = self.__class__.Common(service, rules, path + [("Common", "")])
                        self.IceWall = self.__class__.IceWall(service, rules, path + [("IceWall", "")])
                        self.ParticlesInlet = self.__class__.ParticlesInlet(service, rules, path + [("ParticlesInlet", "")])
                        self.ParticlesWall = self.__class__.ParticlesWall(service, rules, path + [("ParticlesWall", "")])
                        self.BCType = self.__class__.BCType(service, rules, path + [("BCType", "")])
                        self.IsExit = self.__class__.IsExit(service, rules, path + [("IsExit", "")])
                        self.IsInlet = self.__class__.IsInlet(service, rules, path + [("IsInlet", "")])
                        self.IsWall = self.__class__.IsWall(service, rules, path + [("IsWall", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.CopyToBCs = self.__class__.CopyToBCs(service, rules, "CopyToBCs", path)
                        self.CopyWallAdiabaticP10 = self.__class__.CopyWallAdiabaticP10(service, rules, "CopyWallAdiabaticP10", path)
                        self.Display = self.__class__.Display(service, rules, "Display", path)
                        self.ImportConditions = self.__class__.ImportConditions(service, rules, "ImportConditions", path)
                        self.RefreshBCs = self.__class__.RefreshBCs(service, rules, "RefreshBCs", path)
                        self.RenameBC = self.__class__.RenameBC(service, rules, "RenameBC", path)
                        self.ResetToCustom = self.__class__.ResetToCustom(service, rules, "ResetToCustom", path)
                        super().__init__(service, rules, path)

                    class AirflowMassFlowInlet(PyMenu):
                        """
                        Singleton AirflowMassFlowInlet.
                        """
                        def __init__(self, service, rules, path):
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.DirectionMode = self.__class__.DirectionMode(service, rules, path + [("DirectionMode", "")])
                            self.FlowX = self.__class__.FlowX(service, rules, path + [("FlowX", "")])
                            self.FlowY = self.__class__.FlowY(service, rules, path + [("FlowY", "")])
                            self.FlowZ = self.__class__.FlowZ(service, rules, path + [("FlowZ", "")])
                            self.MassFlow = self.__class__.MassFlow(service, rules, path + [("MassFlow", "")])
                            self.MassFlowMode = self.__class__.MassFlowMode(service, rules, path + [("MassFlowMode", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            self.ReferenceFrame = self.__class__.ReferenceFrame(service, rules, path + [("ReferenceFrame", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.TurbIntensity = self.__class__.TurbIntensity(service, rules, path + [("TurbIntensity", "")])
                            self.TurbIntermittency = self.__class__.TurbIntermittency(service, rules, path + [("TurbIntermittency", "")])
                            self.TurbLengthScale = self.__class__.TurbLengthScale(service, rules, path + [("TurbLengthScale", "")])
                            self.TurbSpecification = self.__class__.TurbSpecification(service, rules, path + [("TurbSpecification", "")])
                            self.TurbViscRatio = self.__class__.TurbViscRatio(service, rules, path + [("TurbViscRatio", "")])
                            super().__init__(service, rules, path)

                        class AbsolutePressure(PyNumerical):
                            """
                            Parameter AbsolutePressure of value type float.
                            """
                            pass

                        class BCSync(PyTextual):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class DirectionMode(PyTextual):
                            """
                            Parameter DirectionMode of value type str.
                            """
                            pass

                        class FlowX(PyNumerical):
                            """
                            Parameter FlowX of value type float.
                            """
                            pass

                        class FlowY(PyNumerical):
                            """
                            Parameter FlowY of value type float.
                            """
                            pass

                        class FlowZ(PyNumerical):
                            """
                            Parameter FlowZ of value type float.
                            """
                            pass

                        class MassFlow(PyNumerical):
                            """
                            Parameter MassFlow of value type float.
                            """
                            pass

                        class MassFlowMode(PyTextual):
                            """
                            Parameter MassFlowMode of value type str.
                            """
                            pass

                        class Pressure(PyNumerical):
                            """
                            Parameter Pressure of value type float.
                            """
                            pass

                        class ReferenceFrame(PyTextual):
                            """
                            Parameter ReferenceFrame of value type str.
                            """
                            pass

                        class SettingsEditable(PyParameter):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                        class SettingsVisible(PyParameter):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class Temperature(PyNumerical):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class TurbIntensity(PyNumerical):
                            """
                            Parameter TurbIntensity of value type float.
                            """
                            pass

                        class TurbIntermittency(PyNumerical):
                            """
                            Parameter TurbIntermittency of value type float.
                            """
                            pass

                        class TurbLengthScale(PyNumerical):
                            """
                            Parameter TurbLengthScale of value type float.
                            """
                            pass

                        class TurbSpecification(PyTextual):
                            """
                            Parameter TurbSpecification of value type str.
                            """
                            pass

                        class TurbViscRatio(PyNumerical):
                            """
                            Parameter TurbViscRatio of value type float.
                            """
                            pass

                    class AirflowMassFlowOutlet(PyMenu):
                        """
                        Singleton AirflowMassFlowOutlet.
                        """
                        def __init__(self, service, rules, path):
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.MassFlow = self.__class__.MassFlow(service, rules, path + [("MassFlow", "")])
                            self.MassFlowMode = self.__class__.MassFlowMode(service, rules, path + [("MassFlowMode", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            super().__init__(service, rules, path)

                        class BCSync(PyTextual):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class MassFlow(PyNumerical):
                            """
                            Parameter MassFlow of value type float.
                            """
                            pass

                        class MassFlowMode(PyTextual):
                            """
                            Parameter MassFlowMode of value type str.
                            """
                            pass

                        class SettingsEditable(PyParameter):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                        class SettingsVisible(PyParameter):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                    class AirflowPressureOutlet(PyMenu):
                        """
                        Singleton AirflowPressureOutlet.
                        """
                        def __init__(self, service, rules, path):
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            self.ReferenceFrame = self.__class__.ReferenceFrame(service, rules, path + [("ReferenceFrame", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            super().__init__(service, rules, path)

                        class AbsolutePressure(PyNumerical):
                            """
                            Parameter AbsolutePressure of value type float.
                            """
                            pass

                        class BCSync(PyTextual):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class Pressure(PyNumerical):
                            """
                            Parameter Pressure of value type float.
                            """
                            pass

                        class ReferenceFrame(PyTextual):
                            """
                            Parameter ReferenceFrame of value type str.
                            """
                            pass

                        class SettingsEditable(PyParameter):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                        class SettingsVisible(PyParameter):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class Temperature(PyNumerical):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                    class AirflowVelocityInlet(PyMenu):
                        """
                        Singleton AirflowVelocityInlet.
                        """
                        def __init__(self, service, rules, path):
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.AbsoluteSupersonicPressure = self.__class__.AbsoluteSupersonicPressure(service, rules, path + [("AbsoluteSupersonicPressure", "")])
                            self.AngleAlpha = self.__class__.AngleAlpha(service, rules, path + [("AngleAlpha", "")])
                            self.AngleBeta = self.__class__.AngleBeta(service, rules, path + [("AngleBeta", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.FlowDirection = self.__class__.FlowDirection(service, rules, path + [("FlowDirection", "")])
                            self.FlowMagnitude = self.__class__.FlowMagnitude(service, rules, path + [("FlowMagnitude", "")])
                            self.FlowMagnitudeComputed = self.__class__.FlowMagnitudeComputed(service, rules, path + [("FlowMagnitudeComputed", "")])
                            self.FlowX = self.__class__.FlowX(service, rules, path + [("FlowX", "")])
                            self.FlowXComputed = self.__class__.FlowXComputed(service, rules, path + [("FlowXComputed", "")])
                            self.FlowY = self.__class__.FlowY(service, rules, path + [("FlowY", "")])
                            self.FlowYComputed = self.__class__.FlowYComputed(service, rules, path + [("FlowYComputed", "")])
                            self.FlowZ = self.__class__.FlowZ(service, rules, path + [("FlowZ", "")])
                            self.FlowZComputed = self.__class__.FlowZComputed(service, rules, path + [("FlowZComputed", "")])
                            self.Mach = self.__class__.Mach(service, rules, path + [("Mach", "")])
                            self.MachComputed = self.__class__.MachComputed(service, rules, path + [("MachComputed", "")])
                            self.NormalToBoundary = self.__class__.NormalToBoundary(service, rules, path + [("NormalToBoundary", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            self.ReferenceFrame = self.__class__.ReferenceFrame(service, rules, path + [("ReferenceFrame", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.SupersonicPressure = self.__class__.SupersonicPressure(service, rules, path + [("SupersonicPressure", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.TurbIntensity = self.__class__.TurbIntensity(service, rules, path + [("TurbIntensity", "")])
                            self.TurbIntermittency = self.__class__.TurbIntermittency(service, rules, path + [("TurbIntermittency", "")])
                            self.TurbLengthScale = self.__class__.TurbLengthScale(service, rules, path + [("TurbLengthScale", "")])
                            self.TurbSpecification = self.__class__.TurbSpecification(service, rules, path + [("TurbSpecification", "")])
                            self.TurbViscRatio = self.__class__.TurbViscRatio(service, rules, path + [("TurbViscRatio", "")])
                            self.VelocityMode = self.__class__.VelocityMode(service, rules, path + [("VelocityMode", "")])
                            super().__init__(service, rules, path)

                        class AbsolutePressure(PyNumerical):
                            """
                            Parameter AbsolutePressure of value type float.
                            """
                            pass

                        class AbsoluteSupersonicPressure(PyNumerical):
                            """
                            Parameter AbsoluteSupersonicPressure of value type float.
                            """
                            pass

                        class AngleAlpha(PyNumerical):
                            """
                            Parameter AngleAlpha of value type float.
                            """
                            pass

                        class AngleBeta(PyNumerical):
                            """
                            Parameter AngleBeta of value type float.
                            """
                            pass

                        class BCSync(PyTextual):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class FlowDirection(PyTextual):
                            """
                            Parameter FlowDirection of value type str.
                            """
                            pass

                        class FlowMagnitude(PyNumerical):
                            """
                            Parameter FlowMagnitude of value type float.
                            """
                            pass

                        class FlowMagnitudeComputed(PyNumerical):
                            """
                            Parameter FlowMagnitudeComputed of value type float.
                            """
                            pass

                        class FlowX(PyNumerical):
                            """
                            Parameter FlowX of value type float.
                            """
                            pass

                        class FlowXComputed(PyNumerical):
                            """
                            Parameter FlowXComputed of value type float.
                            """
                            pass

                        class FlowY(PyNumerical):
                            """
                            Parameter FlowY of value type float.
                            """
                            pass

                        class FlowYComputed(PyNumerical):
                            """
                            Parameter FlowYComputed of value type float.
                            """
                            pass

                        class FlowZ(PyNumerical):
                            """
                            Parameter FlowZ of value type float.
                            """
                            pass

                        class FlowZComputed(PyNumerical):
                            """
                            Parameter FlowZComputed of value type float.
                            """
                            pass

                        class Mach(PyNumerical):
                            """
                            Parameter Mach of value type float.
                            """
                            pass

                        class MachComputed(PyNumerical):
                            """
                            Parameter MachComputed of value type float.
                            """
                            pass

                        class NormalToBoundary(PyParameter):
                            """
                            Parameter NormalToBoundary of value type bool.
                            """
                            pass

                        class Pressure(PyNumerical):
                            """
                            Parameter Pressure of value type float.
                            """
                            pass

                        class ReferenceFrame(PyTextual):
                            """
                            Parameter ReferenceFrame of value type str.
                            """
                            pass

                        class SettingsEditable(PyParameter):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                        class SettingsVisible(PyParameter):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class SupersonicPressure(PyNumerical):
                            """
                            Parameter SupersonicPressure of value type float.
                            """
                            pass

                        class Temperature(PyNumerical):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class TurbIntensity(PyNumerical):
                            """
                            Parameter TurbIntensity of value type float.
                            """
                            pass

                        class TurbIntermittency(PyNumerical):
                            """
                            Parameter TurbIntermittency of value type float.
                            """
                            pass

                        class TurbLengthScale(PyNumerical):
                            """
                            Parameter TurbLengthScale of value type float.
                            """
                            pass

                        class TurbSpecification(PyTextual):
                            """
                            Parameter TurbSpecification of value type str.
                            """
                            pass

                        class TurbViscRatio(PyNumerical):
                            """
                            Parameter TurbViscRatio of value type float.
                            """
                            pass

                        class VelocityMode(PyTextual):
                            """
                            Parameter VelocityMode of value type str.
                            """
                            pass

                    class AirflowWall(PyMenu):
                        """
                        Singleton AirflowWall.
                        """
                        def __init__(self, service, rules, path):
                            self.AxisCenterX = self.__class__.AxisCenterX(service, rules, path + [("AxisCenterX", "")])
                            self.AxisCenterY = self.__class__.AxisCenterY(service, rules, path + [("AxisCenterY", "")])
                            self.AxisCenterZ = self.__class__.AxisCenterZ(service, rules, path + [("AxisCenterZ", "")])
                            self.AxisDirectionX = self.__class__.AxisDirectionX(service, rules, path + [("AxisDirectionX", "")])
                            self.AxisDirectionY = self.__class__.AxisDirectionY(service, rules, path + [("AxisDirectionY", "")])
                            self.AxisDirectionZ = self.__class__.AxisDirectionZ(service, rules, path + [("AxisDirectionZ", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.HighRoughnessHeight = self.__class__.HighRoughnessHeight(service, rules, path + [("HighRoughnessHeight", "")])
                            self.ReferenceFrame = self.__class__.ReferenceFrame(service, rules, path + [("ReferenceFrame", "")])
                            self.RotationSpeed = self.__class__.RotationSpeed(service, rules, path + [("RotationSpeed", "")])
                            self.Roughness = self.__class__.Roughness(service, rules, path + [("Roughness", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.ThermalCondition = self.__class__.ThermalCondition(service, rules, path + [("ThermalCondition", "")])
                            self.isRotating = self.__class__.isRotating(service, rules, path + [("isRotating", "")])
                            super().__init__(service, rules, path)

                        class AxisCenterX(PyNumerical):
                            """
                            Parameter AxisCenterX of value type float.
                            """
                            pass

                        class AxisCenterY(PyNumerical):
                            """
                            Parameter AxisCenterY of value type float.
                            """
                            pass

                        class AxisCenterZ(PyNumerical):
                            """
                            Parameter AxisCenterZ of value type float.
                            """
                            pass

                        class AxisDirectionX(PyNumerical):
                            """
                            Parameter AxisDirectionX of value type float.
                            """
                            pass

                        class AxisDirectionY(PyNumerical):
                            """
                            Parameter AxisDirectionY of value type float.
                            """
                            pass

                        class AxisDirectionZ(PyNumerical):
                            """
                            Parameter AxisDirectionZ of value type float.
                            """
                            pass

                        class BCSync(PyTextual):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class HeatFlux(PyNumerical):
                            """
                            Parameter HeatFlux of value type float.
                            """
                            pass

                        class HighRoughnessHeight(PyNumerical):
                            """
                            Parameter HighRoughnessHeight of value type float.
                            """
                            pass

                        class ReferenceFrame(PyTextual):
                            """
                            Parameter ReferenceFrame of value type str.
                            """
                            pass

                        class RotationSpeed(PyNumerical):
                            """
                            Parameter RotationSpeed of value type float.
                            """
                            pass

                        class Roughness(PyTextual):
                            """
                            Parameter Roughness of value type str.
                            """
                            pass

                        class Temperature(PyNumerical):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class ThermalCondition(PyTextual):
                            """
                            Parameter ThermalCondition of value type str.
                            """
                            pass

                        class isRotating(PyParameter):
                            """
                            Parameter isRotating of value type bool.
                            """
                            pass

                    class Common(PyMenu):
                        """
                        Singleton Common.
                        """
                        def __init__(self, service, rules, path):
                            self.DisplayThread = self.__class__.DisplayThread(service, rules, path + [("DisplayThread", "")])
                            self.Group = self.__class__.Group(service, rules, path + [("Group", "")])
                            self.Hidden = self.__class__.Hidden(service, rules, path + [("Hidden", "")])
                            super().__init__(service, rules, path)

                        class DisplayThread(PyTextual):
                            """
                            Parameter DisplayThread of value type str.
                            """
                            pass

                        class Group(PyTextual):
                            """
                            Parameter Group of value type str.
                            """
                            pass

                        class Hidden(PyParameter):
                            """
                            Parameter Hidden of value type bool.
                            """
                            pass

                    class IceWall(PyMenu):
                        """
                        Singleton IceWall.
                        """
                        def __init__(self, service, rules, path):
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.HeatFluxFlag = self.__class__.HeatFluxFlag(service, rules, path + [("HeatFluxFlag", "")])
                            self.Icing = self.__class__.Icing(service, rules, path + [("Icing", "")])
                            super().__init__(service, rules, path)

                        class HeatFlux(PyNumerical):
                            """
                            Parameter HeatFlux of value type float.
                            """
                            pass

                        class HeatFluxFlag(PyParameter):
                            """
                            Parameter HeatFluxFlag of value type bool.
                            """
                            pass

                        class Icing(PyTextual):
                            """
                            Parameter Icing of value type str.
                            """
                            pass

                    class ParticlesInlet(PyMenu):
                        """
                        Singleton ParticlesInlet.
                        """
                        def __init__(self, service, rules, path):
                            self.AutoBC = self.__class__.AutoBC(service, rules, path + [("AutoBC", "")])
                            self.CrystalICC = self.__class__.CrystalICC(service, rules, path + [("CrystalICC", "")])
                            self.CrystalTemperature = self.__class__.CrystalTemperature(service, rules, path + [("CrystalTemperature", "")])
                            self.CrystalVelX = self.__class__.CrystalVelX(service, rules, path + [("CrystalVelX", "")])
                            self.CrystalVelY = self.__class__.CrystalVelY(service, rules, path + [("CrystalVelY", "")])
                            self.CrystalVelZ = self.__class__.CrystalVelZ(service, rules, path + [("CrystalVelZ", "")])
                            self.CrystalVelocityFlag = self.__class__.CrystalVelocityFlag(service, rules, path + [("CrystalVelocityFlag", "")])
                            self.DpmInjFlag = self.__class__.DpmInjFlag(service, rules, path + [("DpmInjFlag", "")])
                            self.DpmNstream = self.__class__.DpmNstream(service, rules, path + [("DpmNstream", "")])
                            self.DropletDiameter = self.__class__.DropletDiameter(service, rules, path + [("DropletDiameter", "")])
                            self.DropletLWC = self.__class__.DropletLWC(service, rules, path + [("DropletLWC", "")])
                            self.DropletTemperature = self.__class__.DropletTemperature(service, rules, path + [("DropletTemperature", "")])
                            self.DropletVelX = self.__class__.DropletVelX(service, rules, path + [("DropletVelX", "")])
                            self.DropletVelY = self.__class__.DropletVelY(service, rules, path + [("DropletVelY", "")])
                            self.DropletVelZ = self.__class__.DropletVelZ(service, rules, path + [("DropletVelZ", "")])
                            self.DropletVelocityFlag = self.__class__.DropletVelocityFlag(service, rules, path + [("DropletVelocityFlag", "")])
                            self.VaporConcentration = self.__class__.VaporConcentration(service, rules, path + [("VaporConcentration", "")])
                            self.VaporMode = self.__class__.VaporMode(service, rules, path + [("VaporMode", "")])
                            self.VaporRH = self.__class__.VaporRH(service, rules, path + [("VaporRH", "")])
                            super().__init__(service, rules, path)

                        class AutoBC(PyParameter):
                            """
                            Parameter AutoBC of value type bool.
                            """
                            pass

                        class CrystalICC(PyNumerical):
                            """
                            Parameter CrystalICC of value type float.
                            """
                            pass

                        class CrystalTemperature(PyNumerical):
                            """
                            Parameter CrystalTemperature of value type float.
                            """
                            pass

                        class CrystalVelX(PyNumerical):
                            """
                            Parameter CrystalVelX of value type float.
                            """
                            pass

                        class CrystalVelY(PyNumerical):
                            """
                            Parameter CrystalVelY of value type float.
                            """
                            pass

                        class CrystalVelZ(PyNumerical):
                            """
                            Parameter CrystalVelZ of value type float.
                            """
                            pass

                        class CrystalVelocityFlag(PyParameter):
                            """
                            Parameter CrystalVelocityFlag of value type bool.
                            """
                            pass

                        class DpmInjFlag(PyParameter):
                            """
                            Parameter DpmInjFlag of value type bool.
                            """
                            pass

                        class DpmNstream(PyNumerical):
                            """
                            Parameter DpmNstream of value type int.
                            """
                            pass

                        class DropletDiameter(PyNumerical):
                            """
                            Parameter DropletDiameter of value type float.
                            """
                            pass

                        class DropletLWC(PyNumerical):
                            """
                            Parameter DropletLWC of value type float.
                            """
                            pass

                        class DropletTemperature(PyNumerical):
                            """
                            Parameter DropletTemperature of value type float.
                            """
                            pass

                        class DropletVelX(PyNumerical):
                            """
                            Parameter DropletVelX of value type float.
                            """
                            pass

                        class DropletVelY(PyNumerical):
                            """
                            Parameter DropletVelY of value type float.
                            """
                            pass

                        class DropletVelZ(PyNumerical):
                            """
                            Parameter DropletVelZ of value type float.
                            """
                            pass

                        class DropletVelocityFlag(PyParameter):
                            """
                            Parameter DropletVelocityFlag of value type bool.
                            """
                            pass

                        class VaporConcentration(PyNumerical):
                            """
                            Parameter VaporConcentration of value type float.
                            """
                            pass

                        class VaporMode(PyTextual):
                            """
                            Parameter VaporMode of value type str.
                            """
                            pass

                        class VaporRH(PyNumerical):
                            """
                            Parameter VaporRH of value type float.
                            """
                            pass

                    class ParticlesWall(PyMenu):
                        """
                        Singleton ParticlesWall.
                        """
                        def __init__(self, service, rules, path):
                            self.VaporWetWall = self.__class__.VaporWetWall(service, rules, path + [("VaporWetWall", "")])
                            super().__init__(service, rules, path)

                        class VaporWetWall(PyParameter):
                            """
                            Parameter VaporWetWall of value type bool.
                            """
                            pass

                    class BCType(PyTextual):
                        """
                        Parameter BCType of value type str.
                        """
                        pass

                    class IsExit(PyParameter):
                        """
                        Parameter IsExit of value type bool.
                        """
                        pass

                    class IsInlet(PyParameter):
                        """
                        Parameter IsInlet of value type bool.
                        """
                        pass

                    class IsWall(PyParameter):
                        """
                        Parameter IsWall of value type bool.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class CopyToBCs(PyCommand):
                        """
                        Command CopyToBCs.

                        Parameters
                        ----------
                        BCName : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class CopyWallAdiabaticP10(PyCommand):
                        """
                        Command CopyWallAdiabaticP10.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Display(PyCommand):
                        """
                        Command Display.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class ImportConditions(PyCommand):
                        """
                        Command ImportConditions.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class RefreshBCs(PyCommand):
                        """
                        Command RefreshBCs.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class RenameBC(PyCommand):
                        """
                        Command RenameBC.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class ResetToCustom(PyCommand):
                        """
                        Command ResetToCustom.


                        Returns
                        -------
                        bool
                        """
                        pass

                def __getitem__(self, key: str) -> _BC:
                    return super().__getitem__(key)

            class Adaptation(PyMenu):
                """
                Singleton Adaptation.
                """
                def __init__(self, service, rules, path):
                    self.Boundaries = self.__class__.Boundaries(service, rules, path + [("Boundaries", "")])
                    self.Constraints = self.__class__.Constraints(service, rules, path + [("Constraints", "")])
                    self.Input = self.__class__.Input(service, rules, path + [("Input", "")])
                    self.State = self.__class__.State(service, rules, path + [("State", "")])
                    self.EditCAD = self.__class__.EditCAD(service, rules, "EditCAD", path)
                    self.GenerateCAD = self.__class__.GenerateCAD(service, rules, "GenerateCAD", path)
                    self.ResetCAD = self.__class__.ResetCAD(service, rules, "ResetCAD", path)
                    super().__init__(service, rules, path)

                class Boundaries(PyMenu):
                    """
                    Singleton Boundaries.
                    """
                    def __init__(self, service, rules, path):
                        self.DeadZones = self.__class__.DeadZones(service, rules, path + [("DeadZones", "")])
                        self.YFamilies = self.__class__.YFamilies(service, rules, path + [("YFamilies", "")])
                        super().__init__(service, rules, path)

                    class DeadZones(PyTextual):
                        """
                        Parameter DeadZones of value type List[str].
                        """
                        pass

                    class YFamilies(PyTextual):
                        """
                        Parameter YFamilies of value type List[str].
                        """
                        pass

                class Constraints(PyMenu):
                    """
                    Singleton Constraints.
                    """
                    def __init__(self, service, rules, path):
                        self.DegAnisotropy = self.__class__.DegAnisotropy(service, rules, path + [("DegAnisotropy", "")])
                        self.DihedralAngle = self.__class__.DihedralAngle(service, rules, path + [("DihedralAngle", "")])
                        self.FaceAngle = self.__class__.FaceAngle(service, rules, path + [("FaceAngle", "")])
                        self.HasHexa = self.__class__.HasHexa(service, rules, path + [("HasHexa", "")])
                        self.HasPrism = self.__class__.HasPrism(service, rules, path + [("HasPrism", "")])
                        self.HasPyra = self.__class__.HasPyra(service, rules, path + [("HasPyra", "")])
                        self.HasTetra = self.__class__.HasTetra(service, rules, path + [("HasTetra", "")])
                        self.HexaDeterminant = self.__class__.HexaDeterminant(service, rules, path + [("HexaDeterminant", "")])
                        self.HexaWarpage = self.__class__.HexaWarpage(service, rules, path + [("HexaWarpage", "")])
                        self.MaxCoarseningCurvature = self.__class__.MaxCoarseningCurvature(service, rules, path + [("MaxCoarseningCurvature", "")])
                        self.MaxEdge = self.__class__.MaxEdge(service, rules, path + [("MaxEdge", "")])
                        self.MaxEdgeRef = self.__class__.MaxEdgeRef(service, rules, path + [("MaxEdgeRef", "")])
                        self.MinEdge = self.__class__.MinEdge(service, rules, path + [("MinEdge", "")])
                        self.MinEdgeRef = self.__class__.MinEdgeRef(service, rules, path + [("MinEdgeRef", "")])
                        self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                        self.PrismAspectRatio = self.__class__.PrismAspectRatio(service, rules, path + [("PrismAspectRatio", "")])
                        self.PrismWarpage = self.__class__.PrismWarpage(service, rules, path + [("PrismWarpage", "")])
                        self.TetraAspectRatio = self.__class__.TetraAspectRatio(service, rules, path + [("TetraAspectRatio", "")])
                        super().__init__(service, rules, path)

                    class DegAnisotropy(PyNumerical):
                        """
                        Parameter DegAnisotropy of value type float.
                        """
                        pass

                    class DihedralAngle(PyNumerical):
                        """
                        Parameter DihedralAngle of value type float.
                        """
                        pass

                    class FaceAngle(PyNumerical):
                        """
                        Parameter FaceAngle of value type float.
                        """
                        pass

                    class HasHexa(PyParameter):
                        """
                        Parameter HasHexa of value type bool.
                        """
                        pass

                    class HasPrism(PyParameter):
                        """
                        Parameter HasPrism of value type bool.
                        """
                        pass

                    class HasPyra(PyParameter):
                        """
                        Parameter HasPyra of value type bool.
                        """
                        pass

                    class HasTetra(PyParameter):
                        """
                        Parameter HasTetra of value type bool.
                        """
                        pass

                    class HexaDeterminant(PyNumerical):
                        """
                        Parameter HexaDeterminant of value type float.
                        """
                        pass

                    class HexaWarpage(PyNumerical):
                        """
                        Parameter HexaWarpage of value type float.
                        """
                        pass

                    class MaxCoarseningCurvature(PyNumerical):
                        """
                        Parameter MaxCoarseningCurvature of value type float.
                        """
                        pass

                    class MaxEdge(PyNumerical):
                        """
                        Parameter MaxEdge of value type float.
                        """
                        pass

                    class MaxEdgeRef(PyNumerical):
                        """
                        Parameter MaxEdgeRef of value type float.
                        """
                        pass

                    class MinEdge(PyNumerical):
                        """
                        Parameter MinEdge of value type float.
                        """
                        pass

                    class MinEdgeRef(PyNumerical):
                        """
                        Parameter MinEdgeRef of value type float.
                        """
                        pass

                    class Mode(PyTextual):
                        """
                        Parameter Mode of value type str.
                        """
                        pass

                    class PrismAspectRatio(PyNumerical):
                        """
                        Parameter PrismAspectRatio of value type float.
                        """
                        pass

                    class PrismWarpage(PyNumerical):
                        """
                        Parameter PrismWarpage of value type float.
                        """
                        pass

                    class TetraAspectRatio(PyNumerical):
                        """
                        Parameter TetraAspectRatio of value type float.
                        """
                        pass

                class Input(PyMenu):
                    """
                    Singleton Input.
                    """
                    def __init__(self, service, rules, path):
                        self.VarList = self.__class__.VarList(service, rules, path + [("VarList", "")])
                        self.CADFile = self.__class__.CADFile(service, rules, path + [("CADFile", "")])
                        self.Convolution = self.__class__.Convolution(service, rules, path + [("Convolution", "")])
                        self.Deconvolution = self.__class__.Deconvolution(service, rules, path + [("Deconvolution", "")])
                        self.Expression = self.__class__.Expression(service, rules, path + [("Expression", "")])
                        self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                        self.PostDeconvolution = self.__class__.PostDeconvolution(service, rules, path + [("PostDeconvolution", "")])
                        self.ScalarVariable = self.__class__.ScalarVariable(service, rules, path + [("ScalarVariable", "")])
                        self.ScalarVariableList = self.__class__.ScalarVariableList(service, rules, path + [("ScalarVariableList", "")])
                        self.ScalarVariableSelect = self.__class__.ScalarVariableSelect(service, rules, path + [("ScalarVariableSelect", "")])
                        self.ScalarVariableTranslation = self.__class__.ScalarVariableTranslation(service, rules, path + [("ScalarVariableTranslation", "")])
                        self.Smoothing = self.__class__.Smoothing(service, rules, path + [("Smoothing", "")])
                        self.Variables = self.__class__.Variables(service, rules, path + [("Variables", "")])
                        self.VariablesPost = self.__class__.VariablesPost(service, rules, path + [("VariablesPost", "")])
                        super().__init__(service, rules, path)

                    class VarList(PyMenu):
                        """
                        Singleton VarList.
                        """
                        def __init__(self, service, rules, path):
                            self.Var = self.__class__.Var(service, rules, path + [("Var", "")])
                            super().__init__(service, rules, path)

                        class Var(PyNamedObjectContainer):
                            """
                            .
                            """
                            class _Var(PyMenu):
                                """
                                Singleton _Var.
                                """
                                def __init__(self, service, rules, path):
                                    self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                                    self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                    super().__init__(service, rules, path)

                                class Name(PyTextual):
                                    """
                                    Parameter Name of value type str.
                                    """
                                    pass

                                class _name_(PyTextual):
                                    """
                                    Parameter _name_ of value type str.
                                    """
                                    pass

                            def __getitem__(self, key: str) -> _Var:
                                return super().__getitem__(key)

                    class CADFile(PyTextual):
                        """
                        Parameter CADFile of value type str.
                        """
                        pass

                    class Convolution(PyNumerical):
                        """
                        Parameter Convolution of value type int.
                        """
                        pass

                    class Deconvolution(PyNumerical):
                        """
                        Parameter Deconvolution of value type int.
                        """
                        pass

                    class Expression(PyTextual):
                        """
                        Parameter Expression of value type str.
                        """
                        pass

                    class Mode(PyTextual):
                        """
                        Parameter Mode of value type str.
                        """
                        pass

                    class PostDeconvolution(PyNumerical):
                        """
                        Parameter PostDeconvolution of value type int.
                        """
                        pass

                    class ScalarVariable(PyTextual):
                        """
                        Parameter ScalarVariable of value type str.
                        """
                        pass

                    class ScalarVariableList(PyTextual):
                        """
                        Parameter ScalarVariableList of value type str.
                        """
                        pass

                    class ScalarVariableSelect(PyTextual):
                        """
                        Parameter ScalarVariableSelect of value type str.
                        """
                        pass

                    class ScalarVariableTranslation(PyTextual):
                        """
                        Parameter ScalarVariableTranslation of value type str.
                        """
                        pass

                    class Smoothing(PyTextual):
                        """
                        Parameter Smoothing of value type str.
                        """
                        pass

                    class Variables(PyTextual):
                        """
                        Parameter Variables of value type List[str].
                        """
                        pass

                    class VariablesPost(PyTextual):
                        """
                        Parameter VariablesPost of value type List[str].
                        """
                        pass

                class State(PyMenu):
                    """
                    Singleton State.
                    """
                    def __init__(self, service, rules, path):
                        self.CADLoaded = self.__class__.CADLoaded(service, rules, path + [("CADLoaded", "")])
                        super().__init__(service, rules, path)

                    class CADLoaded(PyParameter):
                        """
                        Parameter CADLoaded of value type bool.
                        """
                        pass

                class EditCAD(PyCommand):
                    """
                    Command EditCAD.


                    Returns
                    -------
                    bool
                    """
                    pass

                class GenerateCAD(PyCommand):
                    """
                    Command GenerateCAD.


                    Returns
                    -------
                    bool
                    """
                    pass

                class ResetCAD(PyCommand):
                    """
                    Command ResetCAD.


                    Returns
                    -------
                    bool
                    """
                    pass

            class Airflow(PyMenu):
                """
                Singleton Airflow.
                """
                def __init__(self, service, rules, path):
                    self.AirDirection = self.__class__.AirDirection(service, rules, path + [("AirDirection", "")])
                    self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                    self.Fensap = self.__class__.Fensap(service, rules, path + [("Fensap", "")])
                    self.Fluent = self.__class__.Fluent(service, rules, path + [("Fluent", "")])
                    self.General = self.__class__.General(service, rules, path + [("General", "")])
                    self.Refresh = self.__class__.Refresh(service, rules, "Refresh", path)
                    super().__init__(service, rules, path)

                class AirDirection(PyMenu):
                    """
                    Singleton AirDirection.
                    """
                    def __init__(self, service, rules, path):
                        self.Alpha = self.__class__.Alpha(service, rules, path + [("Alpha", "")])
                        self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                        self.DragDir = self.__class__.DragDir(service, rules, path + [("DragDir", "")])
                        self.LiftDir = self.__class__.LiftDir(service, rules, path + [("LiftDir", "")])
                        self.Magnitude = self.__class__.Magnitude(service, rules, path + [("Magnitude", "")])
                        self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                        self.VelocityX = self.__class__.VelocityX(service, rules, path + [("VelocityX", "")])
                        self.VelocityY = self.__class__.VelocityY(service, rules, path + [("VelocityY", "")])
                        self.VelocityZ = self.__class__.VelocityZ(service, rules, path + [("VelocityZ", "")])
                        self.SetAirDirection = self.__class__.SetAirDirection(service, rules, "SetAirDirection", path)
                        super().__init__(service, rules, path)

                    class Alpha(PyNumerical):
                        """
                        Parameter Alpha of value type float.
                        """
                        pass

                    class Beta(PyNumerical):
                        """
                        Parameter Beta of value type float.
                        """
                        pass

                    class DragDir(PyTextual):
                        """
                        Parameter DragDir of value type str.
                        """
                        pass

                    class LiftDir(PyTextual):
                        """
                        Parameter LiftDir of value type str.
                        """
                        pass

                    class Magnitude(PyNumerical):
                        """
                        Parameter Magnitude of value type float.
                        """
                        pass

                    class Mode(PyTextual):
                        """
                        Parameter Mode of value type str.
                        """
                        pass

                    class VelocityX(PyNumerical):
                        """
                        Parameter VelocityX of value type float.
                        """
                        pass

                    class VelocityY(PyNumerical):
                        """
                        Parameter VelocityY of value type float.
                        """
                        pass

                    class VelocityZ(PyNumerical):
                        """
                        Parameter VelocityZ of value type float.
                        """
                        pass

                    class SetAirDirection(PyCommand):
                        """
                        Command SetAirDirection.

                        Parameters
                        ----------
                        aoa : float
                        aos : float
                        mag : float
                        lift : str
                        drag : str

                        Returns
                        -------
                        bool
                        """
                        pass

                class Conditions(PyMenu):
                    """
                    Singleton Conditions.
                    """
                    def __init__(self, service, rules, path):
                        self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                        self.AdiabaticStagnationTemperature = self.__class__.AdiabaticStagnationTemperature(service, rules, path + [("AdiabaticStagnationTemperature", "")])
                        self.CharLen = self.__class__.CharLen(service, rules, path + [("CharLen", "")])
                        self.Mach = self.__class__.Mach(service, rules, path + [("Mach", "")])
                        self.OperatingPressure = self.__class__.OperatingPressure(service, rules, path + [("OperatingPressure", "")])
                        self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                        self.Reynolds = self.__class__.Reynolds(service, rules, path + [("Reynolds", "")])
                        self.SyncFluent = self.__class__.SyncFluent(service, rules, path + [("SyncFluent", "")])
                        self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                        self.Velocity = self.__class__.Velocity(service, rules, path + [("Velocity", "")])
                        super().__init__(service, rules, path)

                    class AbsolutePressure(PyNumerical):
                        """
                        Parameter AbsolutePressure of value type float.
                        """
                        pass

                    class AdiabaticStagnationTemperature(PyNumerical):
                        """
                        Parameter AdiabaticStagnationTemperature of value type float.
                        """
                        pass

                    class CharLen(PyNumerical):
                        """
                        Parameter CharLen of value type float.
                        """
                        pass

                    class Mach(PyNumerical):
                        """
                        Parameter Mach of value type float.
                        """
                        pass

                    class OperatingPressure(PyNumerical):
                        """
                        Parameter OperatingPressure of value type float.
                        """
                        pass

                    class Pressure(PyNumerical):
                        """
                        Parameter Pressure of value type float.
                        """
                        pass

                    class Reynolds(PyNumerical):
                        """
                        Parameter Reynolds of value type float.
                        """
                        pass

                    class SyncFluent(PyParameter):
                        """
                        Parameter SyncFluent of value type bool.
                        """
                        pass

                    class Temperature(PyNumerical):
                        """
                        Parameter Temperature of value type float.
                        """
                        pass

                    class Velocity(PyNumerical):
                        """
                        Parameter Velocity of value type float.
                        """
                        pass

                class Fensap(PyMenu):
                    """
                    Singleton Fensap.
                    """
                    def __init__(self, service, rules, path):
                        self.AV = self.__class__.AV(service, rules, path + [("AV", "")])
                        self.Advanced = self.__class__.Advanced(service, rules, path + [("Advanced", "")])
                        self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                        self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                        super().__init__(service, rules, path)

                    class AV(PyMenu):
                        """
                        Singleton AV.
                        """
                        def __init__(self, service, rules, path):
                            self.CW = self.__class__.CW(service, rules, path + [("CW", "")])
                            self.Option = self.__class__.Option(service, rules, path + [("Option", "")])
                            self.Order = self.__class__.Order(service, rules, path + [("Order", "")])
                            super().__init__(service, rules, path)

                        class CW(PyNumerical):
                            """
                            Parameter CW of value type float.
                            """
                            pass

                        class Option(PyTextual):
                            """
                            Parameter Option of value type str.
                            """
                            pass

                        class Order(PyNumerical):
                            """
                            Parameter Order of value type float.
                            """
                            pass

                    class Advanced(PyMenu):
                        """
                        Singleton Advanced.
                        """
                        def __init__(self, service, rules, path):
                            self.SolverParameters = self.__class__.SolverParameters(service, rules, path + [("SolverParameters", "")])
                            super().__init__(service, rules, path)

                        class SolverParameters(PyTextual):
                            """
                            Parameter SolverParameters of value type str.
                            """
                            pass

                    class Model(PyMenu):
                        """
                        Singleton Model.
                        """
                        def __init__(self, service, rules, path):
                            self.CoupledFlag = self.__class__.CoupledFlag(service, rules, path + [("CoupledFlag", "")])
                            self.EnergyConservativeFlag = self.__class__.EnergyConservativeFlag(service, rules, path + [("EnergyConservativeFlag", "")])
                            self.EnergyEquation = self.__class__.EnergyEquation(service, rules, path + [("EnergyEquation", "")])
                            super().__init__(service, rules, path)

                        class CoupledFlag(PyParameter):
                            """
                            Parameter CoupledFlag of value type bool.
                            """
                            pass

                        class EnergyConservativeFlag(PyParameter):
                            """
                            Parameter EnergyConservativeFlag of value type bool.
                            """
                            pass

                        class EnergyEquation(PyTextual):
                            """
                            Parameter EnergyEquation of value type str.
                            """
                            pass

                    class Turbulence(PyMenu):
                        """
                        Singleton Turbulence.
                        """
                        def __init__(self, service, rules, path):
                            self.CustomFlag = self.__class__.CustomFlag(service, rules, path + [("CustomFlag", "")])
                            self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                            self.TransitionSA = self.__class__.TransitionSA(service, rules, path + [("TransitionSA", "")])
                            self.TransitionSST = self.__class__.TransitionSST(service, rules, path + [("TransitionSST", "")])
                            super().__init__(service, rules, path)

                        class CustomFlag(PyParameter):
                            """
                            Parameter CustomFlag of value type bool.
                            """
                            pass

                        class Model(PyTextual):
                            """
                            Parameter Model of value type str.
                            """
                            pass

                        class TransitionSA(PyTextual):
                            """
                            Parameter TransitionSA of value type str.
                            """
                            pass

                        class TransitionSST(PyTextual):
                            """
                            Parameter TransitionSST of value type str.
                            """
                            pass

                class Fluent(PyMenu):
                    """
                    Singleton Fluent.
                    """
                    def __init__(self, service, rules, path):
                        self.DiscretizationSchemes = self.__class__.DiscretizationSchemes(service, rules, path + [("DiscretizationSchemes", "")])
                        self.Materials = self.__class__.Materials(service, rules, path + [("Materials", "")])
                        self.Models = self.__class__.Models(service, rules, path + [("Models", "")])
                        self.Solver = self.__class__.Solver(service, rules, path + [("Solver", "")])
                        self.Refresh = self.__class__.Refresh(service, rules, "Refresh", path)
                        self.SetAir = self.__class__.SetAir(service, rules, "SetAir", path)
                        self.SetModel = self.__class__.SetModel(service, rules, "SetModel", path)
                        super().__init__(service, rules, path)

                    class DiscretizationSchemes(PyNamedObjectContainer):
                        """
                        .
                        """
                        class _DiscretizationSchemes(PyMenu):
                            """
                            Singleton _DiscretizationSchemes.
                            """
                            def __init__(self, service, rules, path):
                                self.AllowedValues = self.__class__.AllowedValues(service, rules, path + [("AllowedValues", "")])
                                self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                                self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                                self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                super().__init__(service, rules, path)

                            class AllowedValues(PyTextual):
                                """
                                Parameter AllowedValues of value type List[str].
                                """
                                pass

                            class DomainId(PyNumerical):
                                """
                                Parameter DomainId of value type int.
                                """
                                pass

                            class InternalName(PyTextual):
                                """
                                Parameter InternalName of value type str.
                                """
                                pass

                            class Value(PyTextual):
                                """
                                Parameter Value of value type str.
                                """
                                pass

                            class _name_(PyTextual):
                                """
                                Parameter _name_ of value type str.
                                """
                                pass

                        def __getitem__(self, key: str) -> _DiscretizationSchemes:
                            return super().__getitem__(key)

                    class Materials(PyMenu):
                        """
                        Singleton Materials.
                        """
                        def __init__(self, service, rules, path):
                            self.AirCp = self.__class__.AirCp(service, rules, path + [("AirCp", "")])
                            self.AirCpConstant = self.__class__.AirCpConstant(service, rules, path + [("AirCpConstant", "")])
                            self.AirDensity = self.__class__.AirDensity(service, rules, path + [("AirDensity", "")])
                            self.AirDensityConstant = self.__class__.AirDensityConstant(service, rules, path + [("AirDensityConstant", "")])
                            self.AirThermalConductivity = self.__class__.AirThermalConductivity(service, rules, path + [("AirThermalConductivity", "")])
                            self.AirThermalConductivityConstant = self.__class__.AirThermalConductivityConstant(service, rules, path + [("AirThermalConductivityConstant", "")])
                            self.AirViscosity = self.__class__.AirViscosity(service, rules, path + [("AirViscosity", "")])
                            self.AirViscosityConstant = self.__class__.AirViscosityConstant(service, rules, path + [("AirViscosityConstant", "")])
                            self.SettingsSync = self.__class__.SettingsSync(service, rules, path + [("SettingsSync", "")])
                            super().__init__(service, rules, path)

                        class AirCp(PyTextual):
                            """
                            Parameter AirCp of value type str.
                            """
                            pass

                        class AirCpConstant(PyNumerical):
                            """
                            Parameter AirCpConstant of value type float.
                            """
                            pass

                        class AirDensity(PyTextual):
                            """
                            Parameter AirDensity of value type str.
                            """
                            pass

                        class AirDensityConstant(PyNumerical):
                            """
                            Parameter AirDensityConstant of value type float.
                            """
                            pass

                        class AirThermalConductivity(PyTextual):
                            """
                            Parameter AirThermalConductivity of value type str.
                            """
                            pass

                        class AirThermalConductivityConstant(PyNumerical):
                            """
                            Parameter AirThermalConductivityConstant of value type float.
                            """
                            pass

                        class AirViscosity(PyTextual):
                            """
                            Parameter AirViscosity of value type str.
                            """
                            pass

                        class AirViscosityConstant(PyNumerical):
                            """
                            Parameter AirViscosityConstant of value type float.
                            """
                            pass

                        class SettingsSync(PyTextual):
                            """
                            Parameter SettingsSync of value type str.
                            """
                            pass

                    class Models(PyMenu):
                        """
                        Singleton Models.
                        """
                        def __init__(self, service, rules, path):
                            self.Energy = self.__class__.Energy(service, rules, path + [("Energy", "")])
                            self.KwModel = self.__class__.KwModel(service, rules, path + [("KwModel", "")])
                            self.ProductionLimiter = self.__class__.ProductionLimiter(service, rules, path + [("ProductionLimiter", "")])
                            self.TransitionSSTRoughnessConstant = self.__class__.TransitionSSTRoughnessConstant(service, rules, path + [("TransitionSSTRoughnessConstant", "")])
                            self.TransitionSSTRoughnessCorrelation = self.__class__.TransitionSSTRoughnessCorrelation(service, rules, path + [("TransitionSSTRoughnessCorrelation", "")])
                            self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                            self.ViscousHeating = self.__class__.ViscousHeating(service, rules, path + [("ViscousHeating", "")])
                            super().__init__(service, rules, path)

                        class Energy(PyParameter):
                            """
                            Parameter Energy of value type bool.
                            """
                            pass

                        class KwModel(PyTextual):
                            """
                            Parameter KwModel of value type str.
                            """
                            pass

                        class ProductionLimiter(PyParameter):
                            """
                            Parameter ProductionLimiter of value type bool.
                            """
                            pass

                        class TransitionSSTRoughnessConstant(PyNumerical):
                            """
                            Parameter TransitionSSTRoughnessConstant of value type float.
                            """
                            pass

                        class TransitionSSTRoughnessCorrelation(PyParameter):
                            """
                            Parameter TransitionSSTRoughnessCorrelation of value type bool.
                            """
                            pass

                        class Turbulence(PyTextual):
                            """
                            Parameter Turbulence of value type str.
                            """
                            pass

                        class ViscousHeating(PyParameter):
                            """
                            Parameter ViscousHeating of value type bool.
                            """
                            pass

                    class Solver(PyMenu):
                        """
                        Singleton Solver.
                        """
                        def __init__(self, service, rules, path):
                            self.SolverType = self.__class__.SolverType(service, rules, path + [("SolverType", "")])
                            super().__init__(service, rules, path)

                        class SolverType(PyTextual):
                            """
                            Parameter SolverType of value type str.
                            """
                            pass

                    class Refresh(PyCommand):
                        """
                        Command Refresh.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class SetAir(PyCommand):
                        """
                        Command SetAir.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class SetModel(PyCommand):
                        """
                        Command SetModel.


                        Returns
                        -------
                        bool
                        """
                        pass

                class General(PyMenu):
                    """
                    Singleton General.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverType = self.__class__.SolverType(service, rules, path + [("SolverType", "")])
                        super().__init__(service, rules, path)

                    class SolverType(PyTextual):
                        """
                        Parameter SolverType of value type str.
                        """
                        pass

                class Refresh(PyCommand):
                    """
                    Command Refresh.


                    Returns
                    -------
                    bool
                    """
                    pass

            class Domain(PyMenu):
                """
                Singleton Domain.
                """
                def __init__(self, service, rules, path):
                    self.AxisDirectionX = self.__class__.AxisDirectionX(service, rules, path + [("AxisDirectionX", "")])
                    self.AxisDirectionY = self.__class__.AxisDirectionY(service, rules, path + [("AxisDirectionY", "")])
                    self.AxisDirectionZ = self.__class__.AxisDirectionZ(service, rules, path + [("AxisDirectionZ", "")])
                    self.Filter = self.__class__.Filter(service, rules, path + [("Filter", "")])
                    self.Frame = self.__class__.Frame(service, rules, path + [("Frame", "")])
                    self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                    self.NodeOrderId = self.__class__.NodeOrderId(service, rules, path + [("NodeOrderId", "")])
                    self.RotationSpeed = self.__class__.RotationSpeed(service, rules, path + [("RotationSpeed", "")])
                    self.SingleDomain = self.__class__.SingleDomain(service, rules, path + [("SingleDomain", "")])
                    super().__init__(service, rules, path)

                class AxisDirectionX(PyNumerical):
                    """
                    Parameter AxisDirectionX of value type float.
                    """
                    pass

                class AxisDirectionY(PyNumerical):
                    """
                    Parameter AxisDirectionY of value type float.
                    """
                    pass

                class AxisDirectionZ(PyNumerical):
                    """
                    Parameter AxisDirectionZ of value type float.
                    """
                    pass

                class Filter(PyTextual):
                    """
                    Parameter Filter of value type str.
                    """
                    pass

                class Frame(PyTextual):
                    """
                    Parameter Frame of value type str.
                    """
                    pass

                class Mode(PyTextual):
                    """
                    Parameter Mode of value type str.
                    """
                    pass

                class NodeOrderId(PyTextual):
                    """
                    Parameter NodeOrderId of value type str.
                    """
                    pass

                class RotationSpeed(PyNumerical):
                    """
                    Parameter RotationSpeed of value type float.
                    """
                    pass

                class SingleDomain(PyParameter):
                    """
                    Parameter SingleDomain of value type bool.
                    """
                    pass

            class GlobalSettings(PyMenu):
                """
                Singleton GlobalSettings.
                """
                def __init__(self, service, rules, path):
                    self.AdvancedFlag = self.__class__.AdvancedFlag(service, rules, path + [("AdvancedFlag", "")])
                    self.BetaFlag = self.__class__.BetaFlag(service, rules, path + [("BetaFlag", "")])
                    self.BetaOrAdvancedFlag = self.__class__.BetaOrAdvancedFlag(service, rules, path + [("BetaOrAdvancedFlag", "")])
                    self.CFFOutput = self.__class__.CFFOutput(service, rules, path + [("CFFOutput", "")])
                    self.PlotInterval = self.__class__.PlotInterval(service, rules, path + [("PlotInterval", "")])
                    super().__init__(service, rules, path)

                class AdvancedFlag(PyParameter):
                    """
                    Parameter AdvancedFlag of value type bool.
                    """
                    pass

                class BetaFlag(PyParameter):
                    """
                    Parameter BetaFlag of value type bool.
                    """
                    pass

                class BetaOrAdvancedFlag(PyParameter):
                    """
                    Parameter BetaOrAdvancedFlag of value type bool.
                    """
                    pass

                class CFFOutput(PyParameter):
                    """
                    Parameter CFFOutput of value type bool.
                    """
                    pass

                class PlotInterval(PyNumerical):
                    """
                    Parameter PlotInterval of value type int.
                    """
                    pass

            class Ice(PyMenu):
                """
                Singleton Ice.
                """
                def __init__(self, service, rules, path):
                    self.Advanced = self.__class__.Advanced(service, rules, path + [("Advanced", "")])
                    self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                    self.Crystals = self.__class__.Crystals(service, rules, path + [("Crystals", "")])
                    self.IceConditions = self.__class__.IceConditions(service, rules, path + [("IceConditions", "")])
                    self.IcingModel = self.__class__.IcingModel(service, rules, path + [("IcingModel", "")])
                    super().__init__(service, rules, path)

                class Advanced(PyMenu):
                    """
                    Singleton Advanced.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverParameters = self.__class__.SolverParameters(service, rules, path + [("SolverParameters", "")])
                        super().__init__(service, rules, path)

                    class SolverParameters(PyTextual):
                        """
                        Parameter SolverParameters of value type str.
                        """
                        pass

                class Conditions(PyMenu):
                    """
                    Singleton Conditions.
                    """
                    def __init__(self, service, rules, path):
                        self.CrackDetectionCriteria = self.__class__.CrackDetectionCriteria(service, rules, path + [("CrackDetectionCriteria", "")])
                        self.FractureToughness = self.__class__.FractureToughness(service, rules, path + [("FractureToughness", "")])
                        self.IceConstantDensity = self.__class__.IceConstantDensity(service, rules, path + [("IceConstantDensity", "")])
                        self.IceDensityType = self.__class__.IceDensityType(service, rules, path + [("IceDensityType", "")])
                        self.IceEmissivity = self.__class__.IceEmissivity(service, rules, path + [("IceEmissivity", "")])
                        self.IceJonesLEDiameter = self.__class__.IceJonesLEDiameter(service, rules, path + [("IceJonesLEDiameter", "")])
                        self.PoissonRatio = self.__class__.PoissonRatio(service, rules, path + [("PoissonRatio", "")])
                        self.PrincipalStrength = self.__class__.PrincipalStrength(service, rules, path + [("PrincipalStrength", "")])
                        self.SurfaceInterface = self.__class__.SurfaceInterface(service, rules, path + [("SurfaceInterface", "")])
                        self.YoungModulus = self.__class__.YoungModulus(service, rules, path + [("YoungModulus", "")])
                        super().__init__(service, rules, path)

                    class CrackDetectionCriteria(PyTextual):
                        """
                        Parameter CrackDetectionCriteria of value type str.
                        """
                        pass

                    class FractureToughness(PyNumerical):
                        """
                        Parameter FractureToughness of value type float.
                        """
                        pass

                    class IceConstantDensity(PyNumerical):
                        """
                        Parameter IceConstantDensity of value type float.
                        """
                        pass

                    class IceDensityType(PyTextual):
                        """
                        Parameter IceDensityType of value type str.
                        """
                        pass

                    class IceEmissivity(PyNumerical):
                        """
                        Parameter IceEmissivity of value type float.
                        """
                        pass

                    class IceJonesLEDiameter(PyNumerical):
                        """
                        Parameter IceJonesLEDiameter of value type float.
                        """
                        pass

                    class PoissonRatio(PyNumerical):
                        """
                        Parameter PoissonRatio of value type float.
                        """
                        pass

                    class PrincipalStrength(PyNumerical):
                        """
                        Parameter PrincipalStrength of value type float.
                        """
                        pass

                    class SurfaceInterface(PyTextual):
                        """
                        Parameter SurfaceInterface of value type str.
                        """
                        pass

                    class YoungModulus(PyNumerical):
                        """
                        Parameter YoungModulus of value type float.
                        """
                        pass

                class Crystals(PyMenu):
                    """
                    Singleton Crystals.
                    """
                    def __init__(self, service, rules, path):
                        self.BouncingModel = self.__class__.BouncingModel(service, rules, path + [("BouncingModel", "")])
                        self.Erosion = self.__class__.Erosion(service, rules, path + [("Erosion", "")])
                        super().__init__(service, rules, path)

                    class BouncingModel(PyTextual):
                        """
                        Parameter BouncingModel of value type str.
                        """
                        pass

                    class Erosion(PyParameter):
                        """
                        Parameter Erosion of value type bool.
                        """
                        pass

                class IceConditions(PyMenu):
                    """
                    Singleton IceConditions.
                    """
                    def __init__(self, service, rules, path):
                        self.IcingAirTemperature = self.__class__.IcingAirTemperature(service, rules, path + [("IcingAirTemperature", "")])
                        self.IcingAirTemperatureFlag = self.__class__.IcingAirTemperatureFlag(service, rules, path + [("IcingAirTemperatureFlag", "")])
                        self.RecoveryFactor = self.__class__.RecoveryFactor(service, rules, path + [("RecoveryFactor", "")])
                        self.RelativeHumidity = self.__class__.RelativeHumidity(service, rules, path + [("RelativeHumidity", "")])
                        super().__init__(service, rules, path)

                    class IcingAirTemperature(PyNumerical):
                        """
                        Parameter IcingAirTemperature of value type float.
                        """
                        pass

                    class IcingAirTemperatureFlag(PyParameter):
                        """
                        Parameter IcingAirTemperatureFlag of value type bool.
                        """
                        pass

                    class RecoveryFactor(PyNumerical):
                        """
                        Parameter RecoveryFactor of value type float.
                        """
                        pass

                    class RelativeHumidity(PyNumerical):
                        """
                        Parameter RelativeHumidity of value type float.
                        """
                        pass

                class IcingModel(PyMenu):
                    """
                    Singleton IcingModel.
                    """
                    def __init__(self, service, rules, path):
                        self.Beading = self.__class__.Beading(service, rules, path + [("Beading", "")])
                        self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                        self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                        self.SheddingFlag = self.__class__.SheddingFlag(service, rules, path + [("SheddingFlag", "")])
                        super().__init__(service, rules, path)

                    class Beading(PyParameter):
                        """
                        Parameter Beading of value type bool.
                        """
                        pass

                    class HeatFlux(PyTextual):
                        """
                        Parameter HeatFlux of value type str.
                        """
                        pass

                    class Model(PyTextual):
                        """
                        Parameter Model of value type str.
                        """
                        pass

                    class SheddingFlag(PyTextual):
                        """
                        Parameter SheddingFlag of value type str.
                        """
                        pass

            class Particles(PyMenu):
                """
                Singleton Particles.
                """
                def __init__(self, service, rules, path):
                    self.Advanced = self.__class__.Advanced(service, rules, path + [("Advanced", "")])
                    self.Crystals = self.__class__.Crystals(service, rules, path + [("Crystals", "")])
                    self.Droplets = self.__class__.Droplets(service, rules, path + [("Droplets", "")])
                    self.General = self.__class__.General(service, rules, path + [("General", "")])
                    self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                    self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                    self.Vapor = self.__class__.Vapor(service, rules, path + [("Vapor", "")])
                    super().__init__(service, rules, path)

                class Advanced(PyMenu):
                    """
                    Singleton Advanced.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverParameters = self.__class__.SolverParameters(service, rules, path + [("SolverParameters", "")])
                        super().__init__(service, rules, path)

                    class SolverParameters(PyTextual):
                        """
                        Parameter SolverParameters of value type str.
                        """
                        pass

                class Crystals(PyMenu):
                    """
                    Singleton Crystals.
                    """
                    def __init__(self, service, rules, path):
                        self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                        self.ParticlesDistribution = self.__class__.ParticlesDistribution(service, rules, path + [("ParticlesDistribution", "")])
                        super().__init__(service, rules, path)

                    class Conditions(PyMenu):
                        """
                        Singleton Conditions.
                        """
                        def __init__(self, service, rules, path):
                            self.AR = self.__class__.AR(service, rules, path + [("AR", "")])
                            self.Appendix = self.__class__.Appendix(service, rules, path + [("Appendix", "")])
                            self.AppendixLWCPriorityMode = self.__class__.AppendixLWCPriorityMode(service, rules, path + [("AppendixLWCPriorityMode", "")])
                            self.AppendixTWCFactor = self.__class__.AppendixTWCFactor(service, rules, path + [("AppendixTWCFactor", "")])
                            self.Density = self.__class__.Density(service, rules, path + [("Density", "")])
                            self.Diameter = self.__class__.Diameter(service, rules, path + [("Diameter", "")])
                            self.ICC = self.__class__.ICC(service, rules, path + [("ICC", "")])
                            self.CheckAppendixD = self.__class__.CheckAppendixD(service, rules, "CheckAppendixD", path)
                            self.ViewAppendix = self.__class__.ViewAppendix(service, rules, "ViewAppendix", path)
                            super().__init__(service, rules, path)

                        class AR(PyNumerical):
                            """
                            Parameter AR of value type float.
                            """
                            pass

                        class Appendix(PyTextual):
                            """
                            Parameter Appendix of value type str.
                            """
                            pass

                        class AppendixLWCPriorityMode(PyParameter):
                            """
                            Parameter AppendixLWCPriorityMode of value type bool.
                            """
                            pass

                        class AppendixTWCFactor(PyParameter):
                            """
                            Parameter AppendixTWCFactor of value type bool.
                            """
                            pass

                        class Density(PyNumerical):
                            """
                            Parameter Density of value type float.
                            """
                            pass

                        class Diameter(PyNumerical):
                            """
                            Parameter Diameter of value type float.
                            """
                            pass

                        class ICC(PyNumerical):
                            """
                            Parameter ICC of value type float.
                            """
                            pass

                        class CheckAppendixD(PyCommand):
                            """
                            Command CheckAppendixD.

                            Parameters
                            ----------
                            UpdateTWC : bool

                            Returns
                            -------
                            bool
                            """
                            pass

                        class ViewAppendix(PyCommand):
                            """
                            Command ViewAppendix.

                            Parameters
                            ----------
                            Target : str

                            Returns
                            -------
                            bool
                            """
                            pass

                    class ParticlesDistribution(PyMenu):
                        """
                        Singleton ParticlesDistribution.
                        """
                        def __init__(self, service, rules, path):
                            self.CrystalAspectRatios = self.__class__.CrystalAspectRatios(service, rules, path + [("CrystalAspectRatios", "")])
                            self.CrystalDiameters = self.__class__.CrystalDiameters(service, rules, path + [("CrystalDiameters", "")])
                            self.CrystalDistribution = self.__class__.CrystalDistribution(service, rules, path + [("CrystalDistribution", "")])
                            self.ExportDistribution = self.__class__.ExportDistribution(service, rules, "ExportDistribution", path)
                            self.ImportDistribution = self.__class__.ImportDistribution(service, rules, "ImportDistribution", path)
                            self.ViewDistribution = self.__class__.ViewDistribution(service, rules, "ViewDistribution", path)
                            super().__init__(service, rules, path)

                        class CrystalAspectRatios(PyTextual):
                            """
                            Parameter CrystalAspectRatios of value type str.
                            """
                            pass

                        class CrystalDiameters(PyTextual):
                            """
                            Parameter CrystalDiameters of value type str.
                            """
                            pass

                        class CrystalDistribution(PyTextual):
                            """
                            Parameter CrystalDistribution of value type str.
                            """
                            pass

                        class ExportDistribution(PyCommand):
                            """
                            Command ExportDistribution.

                            Parameters
                            ----------
                            Filename : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class ImportDistribution(PyCommand):
                            """
                            Command ImportDistribution.

                            Parameters
                            ----------
                            Filename : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class ViewDistribution(PyCommand):
                            """
                            Command ViewDistribution.

                            Parameters
                            ----------
                            Target : str

                            Returns
                            -------
                            bool
                            """
                            pass

                class Droplets(PyMenu):
                    """
                    Singleton Droplets.
                    """
                    def __init__(self, service, rules, path):
                        self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                        self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                        self.ParticlesDistribution = self.__class__.ParticlesDistribution(service, rules, path + [("ParticlesDistribution", "")])
                        super().__init__(service, rules, path)

                    class Conditions(PyMenu):
                        """
                        Singleton Conditions.
                        """
                        def __init__(self, service, rules, path):
                            self.Appendix = self.__class__.Appendix(service, rules, path + [("Appendix", "")])
                            self.AppendixEnvironment = self.__class__.AppendixEnvironment(service, rules, path + [("AppendixEnvironment", "")])
                            self.AppendixLWCFactor = self.__class__.AppendixLWCFactor(service, rules, path + [("AppendixLWCFactor", "")])
                            self.AppendixODiameter = self.__class__.AppendixODiameter(service, rules, path + [("AppendixODiameter", "")])
                            self.AppendixOEnvironment = self.__class__.AppendixOEnvironment(service, rules, path + [("AppendixOEnvironment", "")])
                            self.AppendixOLWCFactor = self.__class__.AppendixOLWCFactor(service, rules, path + [("AppendixOLWCFactor", "")])
                            self.Diameter = self.__class__.Diameter(service, rules, path + [("Diameter", "")])
                            self.LWC = self.__class__.LWC(service, rules, path + [("LWC", "")])
                            self.SLDFlag = self.__class__.SLDFlag(service, rules, path + [("SLDFlag", "")])
                            self.WaterDensity = self.__class__.WaterDensity(service, rules, path + [("WaterDensity", "")])
                            self.CheckAppendixC = self.__class__.CheckAppendixC(service, rules, "CheckAppendixC", path)
                            self.CheckAppendixO = self.__class__.CheckAppendixO(service, rules, "CheckAppendixO", path)
                            self.ViewAppendix = self.__class__.ViewAppendix(service, rules, "ViewAppendix", path)
                            super().__init__(service, rules, path)

                        class Appendix(PyTextual):
                            """
                            Parameter Appendix of value type str.
                            """
                            pass

                        class AppendixEnvironment(PyNumerical):
                            """
                            Parameter AppendixEnvironment of value type int.
                            """
                            pass

                        class AppendixLWCFactor(PyParameter):
                            """
                            Parameter AppendixLWCFactor of value type bool.
                            """
                            pass

                        class AppendixODiameter(PyNumerical):
                            """
                            Parameter AppendixODiameter of value type int.
                            """
                            pass

                        class AppendixOEnvironment(PyNumerical):
                            """
                            Parameter AppendixOEnvironment of value type int.
                            """
                            pass

                        class AppendixOLWCFactor(PyParameter):
                            """
                            Parameter AppendixOLWCFactor of value type bool.
                            """
                            pass

                        class Diameter(PyNumerical):
                            """
                            Parameter Diameter of value type float.
                            """
                            pass

                        class LWC(PyNumerical):
                            """
                            Parameter LWC of value type float.
                            """
                            pass

                        class SLDFlag(PyParameter):
                            """
                            Parameter SLDFlag of value type bool.
                            """
                            pass

                        class WaterDensity(PyNumerical):
                            """
                            Parameter WaterDensity of value type float.
                            """
                            pass

                        class CheckAppendixC(PyCommand):
                            """
                            Command CheckAppendixC.

                            Parameters
                            ----------
                            UpdateLWC : bool

                            Returns
                            -------
                            bool
                            """
                            pass

                        class CheckAppendixO(PyCommand):
                            """
                            Command CheckAppendixO.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class ViewAppendix(PyCommand):
                            """
                            Command ViewAppendix.

                            Parameters
                            ----------
                            Target : str

                            Returns
                            -------
                            bool
                            """
                            pass

                    class Model(PyMenu):
                        """
                        Singleton Model.
                        """
                        def __init__(self, service, rules, path):
                            self.BreakupModel = self.__class__.BreakupModel(service, rules, path + [("BreakupModel", "")])
                            self.DpmDragModel = self.__class__.DpmDragModel(service, rules, path + [("DpmDragModel", "")])
                            self.DragCunninghamCorrection = self.__class__.DragCunninghamCorrection(service, rules, path + [("DragCunninghamCorrection", "")])
                            self.DragModel = self.__class__.DragModel(service, rules, path + [("DragModel", "")])
                            self.DragShapeFactor = self.__class__.DragShapeFactor(service, rules, path + [("DragShapeFactor", "")])
                            self.NTries = self.__class__.NTries(service, rules, path + [("NTries", "")])
                            self.Splashing = self.__class__.Splashing(service, rules, path + [("Splashing", "")])
                            self.SplashingActivationTrigger = self.__class__.SplashingActivationTrigger(service, rules, path + [("SplashingActivationTrigger", "")])
                            self.SplashingDelay = self.__class__.SplashingDelay(service, rules, path + [("SplashingDelay", "")])
                            self.SplashingModel = self.__class__.SplashingModel(service, rules, path + [("SplashingModel", "")])
                            self.TerminalVelocity = self.__class__.TerminalVelocity(service, rules, path + [("TerminalVelocity", "")])
                            self.TurbulentDispersion = self.__class__.TurbulentDispersion(service, rules, path + [("TurbulentDispersion", "")])
                            self.UDFDrag = self.__class__.UDFDrag(service, rules, path + [("UDFDrag", "")])
                            self.RefreshNames = self.__class__.RefreshNames(service, rules, "RefreshNames", path)
                            super().__init__(service, rules, path)

                        class BreakupModel(PyTextual):
                            """
                            Parameter BreakupModel of value type str.
                            """
                            pass

                        class DpmDragModel(PyTextual):
                            """
                            Parameter DpmDragModel of value type str.
                            """
                            pass

                        class DragCunninghamCorrection(PyNumerical):
                            """
                            Parameter DragCunninghamCorrection of value type float.
                            """
                            pass

                        class DragModel(PyTextual):
                            """
                            Parameter DragModel of value type str.
                            """
                            pass

                        class DragShapeFactor(PyNumerical):
                            """
                            Parameter DragShapeFactor of value type float.
                            """
                            pass

                        class NTries(PyNumerical):
                            """
                            Parameter NTries of value type int.
                            """
                            pass

                        class Splashing(PyTextual):
                            """
                            Parameter Splashing of value type str.
                            """
                            pass

                        class SplashingActivationTrigger(PyNumerical):
                            """
                            Parameter SplashingActivationTrigger of value type float.
                            """
                            pass

                        class SplashingDelay(PyNumerical):
                            """
                            Parameter SplashingDelay of value type int.
                            """
                            pass

                        class SplashingModel(PyTextual):
                            """
                            Parameter SplashingModel of value type str.
                            """
                            pass

                        class TerminalVelocity(PyTextual):
                            """
                            Parameter TerminalVelocity of value type str.
                            """
                            pass

                        class TurbulentDispersion(PyParameter):
                            """
                            Parameter TurbulentDispersion of value type bool.
                            """
                            pass

                        class UDFDrag(PyTextual):
                            """
                            Parameter UDFDrag of value type str.
                            """
                            pass

                        class RefreshNames(PyCommand):
                            """
                            Command RefreshNames.

                            Parameters
                            ----------
                            Target : str

                            Returns
                            -------
                            bool
                            """
                            pass

                    class ParticlesDistribution(PyMenu):
                        """
                        Singleton ParticlesDistribution.
                        """
                        def __init__(self, service, rules, path):
                            self.AppODistribution = self.__class__.AppODistribution(service, rules, path + [("AppODistribution", "")])
                            self.DPMDropletDistribution = self.__class__.DPMDropletDistribution(service, rules, path + [("DPMDropletDistribution", "")])
                            self.DropletDiameters = self.__class__.DropletDiameters(service, rules, path + [("DropletDiameters", "")])
                            self.DropletDistribution = self.__class__.DropletDistribution(service, rules, path + [("DropletDistribution", "")])
                            self.Weights = self.__class__.Weights(service, rules, path + [("Weights", "")])
                            self.ExportDistribution = self.__class__.ExportDistribution(service, rules, "ExportDistribution", path)
                            self.ImportDistribution = self.__class__.ImportDistribution(service, rules, "ImportDistribution", path)
                            self.ViewDistribution = self.__class__.ViewDistribution(service, rules, "ViewDistribution", path)
                            super().__init__(service, rules, path)

                        class AppODistribution(PyTextual):
                            """
                            Parameter AppODistribution of value type str.
                            """
                            pass

                        class DPMDropletDistribution(PyTextual):
                            """
                            Parameter DPMDropletDistribution of value type str.
                            """
                            pass

                        class DropletDiameters(PyTextual):
                            """
                            Parameter DropletDiameters of value type str.
                            """
                            pass

                        class DropletDistribution(PyTextual):
                            """
                            Parameter DropletDistribution of value type str.
                            """
                            pass

                        class Weights(PyTextual):
                            """
                            Parameter Weights of value type str.
                            """
                            pass

                        class ExportDistribution(PyCommand):
                            """
                            Command ExportDistribution.

                            Parameters
                            ----------
                            Filename : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class ImportDistribution(PyCommand):
                            """
                            Command ImportDistribution.

                            Parameters
                            ----------
                            Filename : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class ViewDistribution(PyCommand):
                            """
                            Command ViewDistribution.

                            Parameters
                            ----------
                            Target : str

                            Returns
                            -------
                            bool
                            """
                            pass

                class General(PyMenu):
                    """
                    Singleton General.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverType = self.__class__.SolverType(service, rules, path + [("SolverType", "")])
                        self.UseCaseInjection = self.__class__.UseCaseInjection(service, rules, path + [("UseCaseInjection", "")])
                        super().__init__(service, rules, path)

                    class SolverType(PyTextual):
                        """
                        Parameter SolverType of value type str.
                        """
                        pass

                    class UseCaseInjection(PyTextual):
                        """
                        Parameter UseCaseInjection of value type str.
                        """
                        pass

                class Model(PyMenu):
                    """
                    Singleton Model.
                    """
                    def __init__(self, service, rules, path):
                        self.ThermalEquation = self.__class__.ThermalEquation(service, rules, path + [("ThermalEquation", "")])
                        super().__init__(service, rules, path)

                    class ThermalEquation(PyParameter):
                        """
                        Parameter ThermalEquation of value type bool.
                        """
                        pass

                class Type(PyMenu):
                    """
                    Singleton Type.
                    """
                    def __init__(self, service, rules, path):
                        self.CrystalsFlag = self.__class__.CrystalsFlag(service, rules, path + [("CrystalsFlag", "")])
                        self.DropletsFlag = self.__class__.DropletsFlag(service, rules, path + [("DropletsFlag", "")])
                        self.VaporFlag = self.__class__.VaporFlag(service, rules, path + [("VaporFlag", "")])
                        super().__init__(service, rules, path)

                    class CrystalsFlag(PyParameter):
                        """
                        Parameter CrystalsFlag of value type bool.
                        """
                        pass

                    class DropletsFlag(PyParameter):
                        """
                        Parameter DropletsFlag of value type bool.
                        """
                        pass

                    class VaporFlag(PyParameter):
                        """
                        Parameter VaporFlag of value type bool.
                        """
                        pass

                class Vapor(PyMenu):
                    """
                    Singleton Vapor.
                    """
                    def __init__(self, service, rules, path):
                        self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                        self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                        super().__init__(service, rules, path)

                    class Conditions(PyMenu):
                        """
                        Singleton Conditions.
                        """
                        def __init__(self, service, rules, path):
                            self.VaporConcentration = self.__class__.VaporConcentration(service, rules, path + [("VaporConcentration", "")])
                            self.VaporInitialMode = self.__class__.VaporInitialMode(service, rules, path + [("VaporInitialMode", "")])
                            self.VaporRH = self.__class__.VaporRH(service, rules, path + [("VaporRH", "")])
                            super().__init__(service, rules, path)

                        class VaporConcentration(PyNumerical):
                            """
                            Parameter VaporConcentration of value type float.
                            """
                            pass

                        class VaporInitialMode(PyTextual):
                            """
                            Parameter VaporInitialMode of value type str.
                            """
                            pass

                        class VaporRH(PyNumerical):
                            """
                            Parameter VaporRH of value type float.
                            """
                            pass

                    class Model(PyMenu):
                        """
                        Singleton Model.
                        """
                        def __init__(self, service, rules, path):
                            self.TurbSchmidtNumber = self.__class__.TurbSchmidtNumber(service, rules, path + [("TurbSchmidtNumber", "")])
                            super().__init__(service, rules, path)

                        class TurbSchmidtNumber(PyNumerical):
                            """
                            Parameter TurbSchmidtNumber of value type float.
                            """
                            pass

            class RunType(PyMenu):
                """
                Singleton RunType.
                """
                def __init__(self, service, rules, path):
                    self.Adapt = self.__class__.Adapt(service, rules, path + [("Adapt", "")])
                    self.Airflow = self.__class__.Airflow(service, rules, path + [("Airflow", "")])
                    self.CHT = self.__class__.CHT(service, rules, path + [("CHT", "")])
                    self.Ice = self.__class__.Ice(service, rules, path + [("Ice", "")])
                    self.Particles = self.__class__.Particles(service, rules, path + [("Particles", "")])
                    super().__init__(service, rules, path)

                class Adapt(PyParameter):
                    """
                    Parameter Adapt of value type bool.
                    """
                    pass

                class Airflow(PyParameter):
                    """
                    Parameter Airflow of value type bool.
                    """
                    pass

                class CHT(PyParameter):
                    """
                    Parameter CHT of value type bool.
                    """
                    pass

                class Ice(PyParameter):
                    """
                    Parameter Ice of value type bool.
                    """
                    pass

                class Particles(PyParameter):
                    """
                    Parameter Particles of value type bool.
                    """
                    pass

            class Solution(PyMenu):
                """
                Singleton Solution.
                """
                def __init__(self, service, rules, path):
                    self.AdaptationGlobalSettings = self.__class__.AdaptationGlobalSettings(service, rules, path + [("AdaptationGlobalSettings", "")])
                    self.AdaptationRun = self.__class__.AdaptationRun(service, rules, path + [("AdaptationRun", "")])
                    self.AirflowRun = self.__class__.AirflowRun(service, rules, path + [("AirflowRun", "")])
                    self.CHT = self.__class__.CHT(service, rules, path + [("CHT", "")])
                    self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
                    self.IceRun = self.__class__.IceRun(service, rules, path + [("IceRun", "")])
                    self.MultishotRun = self.__class__.MultishotRun(service, rules, path + [("MultishotRun", "")])
                    self.ParticlesRun = self.__class__.ParticlesRun(service, rules, path + [("ParticlesRun", "")])
                    self.RunState = self.__class__.RunState(service, rules, path + [("RunState", "")])
                    self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                    self.CalculateOG = self.__class__.CalculateOG(service, rules, "CalculateOG", path)
                    self.ConfigureShots = self.__class__.ConfigureShots(service, rules, "ConfigureShots", path)
                    self.FensapGridSave = self.__class__.FensapGridSave(service, rules, "FensapGridSave", path)
                    self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                    self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                    self.ResetMultishot = self.__class__.ResetMultishot(service, rules, "ResetMultishot", path)
                    super().__init__(service, rules, path)

                class AdaptationGlobalSettings(PyMenu):
                    """
                    Singleton AdaptationGlobalSettings.
                    """
                    def __init__(self, service, rules, path):
                        self.NumberLoops = self.__class__.NumberLoops(service, rules, path + [("NumberLoops", "")])
                        self.RunSolver = self.__class__.RunSolver(service, rules, path + [("RunSolver", "")])
                        self.SolutionRestart = self.__class__.SolutionRestart(service, rules, path + [("SolutionRestart", "")])
                        super().__init__(service, rules, path)

                    class NumberLoops(PyNumerical):
                        """
                        Parameter NumberLoops of value type int.
                        """
                        pass

                    class RunSolver(PyParameter):
                        """
                        Parameter RunSolver of value type bool.
                        """
                        pass

                    class SolutionRestart(PyTextual):
                        """
                        Parameter SolutionRestart of value type str.
                        """
                        pass

                class AdaptationRun(PyMenu):
                    """
                    Singleton AdaptationRun.
                    """
                    def __init__(self, service, rules, path):
                        self.Operations = self.__class__.Operations(service, rules, path + [("Operations", "")])
                        self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                        self.OutputCase = self.__class__.OutputCase(service, rules, path + [("OutputCase", "")])
                        self.State = self.__class__.State(service, rules, path + [("State", "")])
                        self.Target = self.__class__.Target(service, rules, path + [("Target", "")])
                        self.ComputeCarpet = self.__class__.ComputeCarpet(service, rules, "ComputeCarpet", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        self.RunOG = self.__class__.RunOG(service, rules, "RunOG", path)
                        self.UpdateMesh = self.__class__.UpdateMesh(service, rules, "UpdateMesh", path)
                        self.ViewMesh = self.__class__.ViewMesh(service, rules, "ViewMesh", path)
                        super().__init__(service, rules, path)

                    class Operations(PyMenu):
                        """
                        Singleton Operations.
                        """
                        def __init__(self, service, rules, path):
                            self.AdaptCurv = self.__class__.AdaptCurv(service, rules, path + [("AdaptCurv", "")])
                            self.AdjustY = self.__class__.AdjustY(service, rules, path + [("AdjustY", "")])
                            self.ComputeError = self.__class__.ComputeError(service, rules, path + [("ComputeError", "")])
                            self.MainIter = self.__class__.MainIter(service, rules, path + [("MainIter", "")])
                            self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                            self.NMPost = self.__class__.NMPost(service, rules, path + [("NMPost", "")])
                            self.NMPre = self.__class__.NMPre(service, rules, path + [("NMPre", "")])
                            self.Swap = self.__class__.Swap(service, rules, path + [("Swap", "")])
                            self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                            super().__init__(service, rules, path)

                        class AdaptCurv(PyParameter):
                            """
                            Parameter AdaptCurv of value type bool.
                            """
                            pass

                        class AdjustY(PyTextual):
                            """
                            Parameter AdjustY of value type str.
                            """
                            pass

                        class ComputeError(PyParameter):
                            """
                            Parameter ComputeError of value type bool.
                            """
                            pass

                        class MainIter(PyNumerical):
                            """
                            Parameter MainIter of value type int.
                            """
                            pass

                        class Mode(PyTextual):
                            """
                            Parameter Mode of value type str.
                            """
                            pass

                        class NMPost(PyNumerical):
                            """
                            Parameter NMPost of value type int.
                            """
                            pass

                        class NMPre(PyNumerical):
                            """
                            Parameter NMPre of value type int.
                            """
                            pass

                        class Swap(PyNumerical):
                            """
                            Parameter Swap of value type int.
                            """
                            pass

                        class Type(PyTextual):
                            """
                            Parameter Type of value type str.
                            """
                            pass

                    class Options(PyMenu):
                        """
                        Singleton Options.
                        """
                        def __init__(self, service, rules, path):
                            self.NumberCPUs = self.__class__.NumberCPUs(service, rules, path + [("NumberCPUs", "")])
                            self.SpecifyCPUs = self.__class__.SpecifyCPUs(service, rules, path + [("SpecifyCPUs", "")])
                            super().__init__(service, rules, path)

                        class NumberCPUs(PyNumerical):
                            """
                            Parameter NumberCPUs of value type int.
                            """
                            pass

                        class SpecifyCPUs(PyParameter):
                            """
                            Parameter SpecifyCPUs of value type bool.
                            """
                            pass

                    class OutputCase(PyMenu):
                        """
                        Singleton OutputCase.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.FilenameDat = self.__class__.FilenameDat(service, rules, path + [("FilenameDat", "")])
                            self.FilenameIp = self.__class__.FilenameIp(service, rules, path + [("FilenameIp", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyTextual):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class FilenameDat(PyTextual):
                            """
                            Parameter FilenameDat of value type str.
                            """
                            pass

                        class FilenameIp(PyTextual):
                            """
                            Parameter FilenameIp of value type str.
                            """
                            pass

                    class State(PyMenu):
                        """
                        Singleton State.
                        """
                        def __init__(self, service, rules, path):
                            self.MeshAdapted = self.__class__.MeshAdapted(service, rules, path + [("MeshAdapted", "")])
                            super().__init__(service, rules, path)

                        class MeshAdapted(PyParameter):
                            """
                            Parameter MeshAdapted of value type bool.
                            """
                            pass

                    class Target(PyMenu):
                        """
                        Singleton Target.
                        """
                        def __init__(self, service, rules, path):
                            self.ErrorValue = self.__class__.ErrorValue(service, rules, path + [("ErrorValue", "")])
                            self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                            self.NumCells = self.__class__.NumCells(service, rules, path + [("NumCells", "")])
                            self.NumCellsChange = self.__class__.NumCellsChange(service, rules, path + [("NumCellsChange", "")])
                            self.NumCellsMax = self.__class__.NumCellsMax(service, rules, path + [("NumCellsMax", "")])
                            self.NumCellsRef = self.__class__.NumCellsRef(service, rules, path + [("NumCellsRef", "")])
                            self.NumNodes = self.__class__.NumNodes(service, rules, path + [("NumNodes", "")])
                            self.NumNodesChange = self.__class__.NumNodesChange(service, rules, path + [("NumNodesChange", "")])
                            self.NumNodesMax = self.__class__.NumNodesMax(service, rules, path + [("NumNodesMax", "")])
                            self.NumNodesRef = self.__class__.NumNodesRef(service, rules, path + [("NumNodesRef", "")])
                            super().__init__(service, rules, path)

                        class ErrorValue(PyNumerical):
                            """
                            Parameter ErrorValue of value type float.
                            """
                            pass

                        class Mode(PyTextual):
                            """
                            Parameter Mode of value type str.
                            """
                            pass

                        class NumCells(PyNumerical):
                            """
                            Parameter NumCells of value type int.
                            """
                            pass

                        class NumCellsChange(PyNumerical):
                            """
                            Parameter NumCellsChange of value type int.
                            """
                            pass

                        class NumCellsMax(PyNumerical):
                            """
                            Parameter NumCellsMax of value type int.
                            """
                            pass

                        class NumCellsRef(PyNumerical):
                            """
                            Parameter NumCellsRef of value type int.
                            """
                            pass

                        class NumNodes(PyNumerical):
                            """
                            Parameter NumNodes of value type int.
                            """
                            pass

                        class NumNodesChange(PyNumerical):
                            """
                            Parameter NumNodesChange of value type int.
                            """
                            pass

                        class NumNodesMax(PyNumerical):
                            """
                            Parameter NumNodesMax of value type int.
                            """
                            pass

                        class NumNodesRef(PyNumerical):
                            """
                            Parameter NumNodesRef of value type int.
                            """
                            pass

                    class ComputeCarpet(PyCommand):
                        """
                        Command ComputeCarpet.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Command Interrupt.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Command Reset.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class RunOG(PyCommand):
                        """
                        Command RunOG.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class UpdateMesh(PyCommand):
                        """
                        Command UpdateMesh.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class ViewMesh(PyCommand):
                        """
                        Command ViewMesh.


                        Returns
                        -------
                        bool
                        """
                        pass

                class AirflowRun(PyMenu):
                    """
                    Singleton AirflowRun.
                    """
                    def __init__(self, service, rules, path):
                        self.AirflowFENSAPOutputSolution = self.__class__.AirflowFENSAPOutputSolution(service, rules, path + [("AirflowFENSAPOutputSolution", "")])
                        self.AirflowFluentOutputSolution = self.__class__.AirflowFluentOutputSolution(service, rules, path + [("AirflowFluentOutputSolution", "")])
                        self.AirflowInput = self.__class__.AirflowInput(service, rules, path + [("AirflowInput", "")])
                        self.FensapOutput = self.__class__.FensapOutput(service, rules, path + [("FensapOutput", "")])
                        self.FensapTimeIntegration = self.__class__.FensapTimeIntegration(service, rules, path + [("FensapTimeIntegration", "")])
                        self.FluentCFFPost = self.__class__.FluentCFFPost(service, rules, path + [("FluentCFFPost", "")])
                        self.FluentInitSettings = self.__class__.FluentInitSettings(service, rules, path + [("FluentInitSettings", "")])
                        self.FluentTimeIntegration = self.__class__.FluentTimeIntegration(service, rules, path + [("FluentTimeIntegration", "")])
                        self.ConvergenceAvailable = self.__class__.ConvergenceAvailable(service, rules, path + [("ConvergenceAvailable", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Load = self.__class__.Load(service, rules, "Load", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        self.Save = self.__class__.Save(service, rules, "Save", path)
                        self.SaveAs = self.__class__.SaveAs(service, rules, "SaveAs", path)
                        super().__init__(service, rules, path)

                    class AirflowFENSAPOutputSolution(PyMenu):
                        """
                        Singleton AirflowFENSAPOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.HasHFlux = self.__class__.HasHFlux(service, rules, path + [("HasHFlux", "")])
                            self.HasShear = self.__class__.HasShear(service, rules, path + [("HasShear", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyTextual):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class HasHFlux(PyParameter):
                            """
                            Parameter HasHFlux of value type bool.
                            """
                            pass

                        class HasShear(PyParameter):
                            """
                            Parameter HasShear of value type bool.
                            """
                            pass

                        class Loaded(PyParameter):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class AirflowFluentOutputSolution(PyMenu):
                        """
                        Singleton AirflowFluentOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyTextual):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class Loaded(PyParameter):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class AirflowInput(PyMenu):
                        """
                        Singleton AirflowInput.
                        """
                        def __init__(self, service, rules, path):
                            self.RoughnessInput = self.__class__.RoughnessInput(service, rules, path + [("RoughnessInput", "")])
                            super().__init__(service, rules, path)

                        class RoughnessInput(PyParameter):
                            """
                            Parameter RoughnessInput of value type bool.
                            """
                            pass

                    class FensapOutput(PyMenu):
                        """
                        Singleton FensapOutput.
                        """
                        def __init__(self, service, rules, path):
                            self.DragX = self.__class__.DragX(service, rules, path + [("DragX", "")])
                            self.DragY = self.__class__.DragY(service, rules, path + [("DragY", "")])
                            self.DragZ = self.__class__.DragZ(service, rules, path + [("DragZ", "")])
                            self.FensapOutputEID = self.__class__.FensapOutputEID(service, rules, path + [("FensapOutputEID", "")])
                            self.FensapOutputForces = self.__class__.FensapOutputForces(service, rules, path + [("FensapOutputForces", "")])
                            self.LiftAxis = self.__class__.LiftAxis(service, rules, path + [("LiftAxis", "")])
                            self.MomentX = self.__class__.MomentX(service, rules, path + [("MomentX", "")])
                            self.MomentY = self.__class__.MomentY(service, rules, path + [("MomentY", "")])
                            self.MomentZ = self.__class__.MomentZ(service, rules, path + [("MomentZ", "")])
                            self.MonitorH = self.__class__.MonitorH(service, rules, path + [("MonitorH", "")])
                            self.MonitorMass = self.__class__.MonitorMass(service, rules, path + [("MonitorMass", "")])
                            self.MonitorTotalHeat = self.__class__.MonitorTotalHeat(service, rules, path + [("MonitorTotalHeat", "")])
                            self.NumberedOutput = self.__class__.NumberedOutput(service, rules, path + [("NumberedOutput", "")])
                            self.RefArea = self.__class__.RefArea(service, rules, path + [("RefArea", "")])
                            self.SaveDelay = self.__class__.SaveDelay(service, rules, path + [("SaveDelay", "")])
                            super().__init__(service, rules, path)

                        class DragX(PyNumerical):
                            """
                            Parameter DragX of value type float.
                            """
                            pass

                        class DragY(PyNumerical):
                            """
                            Parameter DragY of value type float.
                            """
                            pass

                        class DragZ(PyNumerical):
                            """
                            Parameter DragZ of value type float.
                            """
                            pass

                        class FensapOutputEID(PyParameter):
                            """
                            Parameter FensapOutputEID of value type bool.
                            """
                            pass

                        class FensapOutputForces(PyTextual):
                            """
                            Parameter FensapOutputForces of value type str.
                            """
                            pass

                        class LiftAxis(PyTextual):
                            """
                            Parameter LiftAxis of value type str.
                            """
                            pass

                        class MomentX(PyNumerical):
                            """
                            Parameter MomentX of value type float.
                            """
                            pass

                        class MomentY(PyNumerical):
                            """
                            Parameter MomentY of value type float.
                            """
                            pass

                        class MomentZ(PyNumerical):
                            """
                            Parameter MomentZ of value type float.
                            """
                            pass

                        class MonitorH(PyParameter):
                            """
                            Parameter MonitorH of value type bool.
                            """
                            pass

                        class MonitorMass(PyParameter):
                            """
                            Parameter MonitorMass of value type bool.
                            """
                            pass

                        class MonitorTotalHeat(PyParameter):
                            """
                            Parameter MonitorTotalHeat of value type bool.
                            """
                            pass

                        class NumberedOutput(PyParameter):
                            """
                            Parameter NumberedOutput of value type bool.
                            """
                            pass

                        class RefArea(PyNumerical):
                            """
                            Parameter RefArea of value type float.
                            """
                            pass

                        class SaveDelay(PyNumerical):
                            """
                            Parameter SaveDelay of value type int.
                            """
                            pass

                    class FensapTimeIntegration(PyMenu):
                        """
                        Singleton FensapTimeIntegration.
                        """
                        def __init__(self, service, rules, path):
                            self.CFL = self.__class__.CFL(service, rules, path + [("CFL", "")])
                            self.NumIterations = self.__class__.NumIterations(service, rules, path + [("NumIterations", "")])
                            self.RlxIter = self.__class__.RlxIter(service, rules, path + [("RlxIter", "")])
                            self.TimeOrder = self.__class__.TimeOrder(service, rules, path + [("TimeOrder", "")])
                            self.TimeStep = self.__class__.TimeStep(service, rules, path + [("TimeStep", "")])
                            self.TimeTotal = self.__class__.TimeTotal(service, rules, path + [("TimeTotal", "")])
                            self.VariableRelaxation = self.__class__.VariableRelaxation(service, rules, path + [("VariableRelaxation", "")])
                            super().__init__(service, rules, path)

                        class CFL(PyNumerical):
                            """
                            Parameter CFL of value type float.
                            """
                            pass

                        class NumIterations(PyNumerical):
                            """
                            Parameter NumIterations of value type int.
                            """
                            pass

                        class RlxIter(PyNumerical):
                            """
                            Parameter RlxIter of value type int.
                            """
                            pass

                        class TimeOrder(PyTextual):
                            """
                            Parameter TimeOrder of value type str.
                            """
                            pass

                        class TimeStep(PyNumerical):
                            """
                            Parameter TimeStep of value type float.
                            """
                            pass

                        class TimeTotal(PyNumerical):
                            """
                            Parameter TimeTotal of value type float.
                            """
                            pass

                        class VariableRelaxation(PyParameter):
                            """
                            Parameter VariableRelaxation of value type bool.
                            """
                            pass

                    class FluentCFFPost(PyMenu):
                        """
                        Singleton FluentCFFPost.
                        """
                        def __init__(self, service, rules, path):
                            self.Fields = self.__class__.Fields(service, rules, path + [("Fields", "")])
                            self.ReadOnly = self.__class__.ReadOnly(service, rules, path + [("ReadOnly", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.WriteLevel = self.__class__.WriteLevel(service, rules, path + [("WriteLevel", "")])
                            self.WriteMode = self.__class__.WriteMode(service, rules, path + [("WriteMode", "")])
                            self.ZoneType = self.__class__.ZoneType(service, rules, path + [("ZoneType", "")])
                            super().__init__(service, rules, path)

                        class Fields(PyTextual):
                            """
                            Parameter Fields of value type List[str].
                            """
                            pass

                        class ReadOnly(PyParameter):
                            """
                            Parameter ReadOnly of value type bool.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class WriteLevel(PyTextual):
                            """
                            Parameter WriteLevel of value type str.
                            """
                            pass

                        class WriteMode(PyTextual):
                            """
                            Parameter WriteMode of value type str.
                            """
                            pass

                        class ZoneType(PyTextual):
                            """
                            Parameter ZoneType of value type str.
                            """
                            pass

                    class FluentInitSettings(PyMenu):
                        """
                        Singleton FluentInitSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Boundaries = self.__class__.Boundaries(service, rules, path + [("Boundaries", "")])
                            self.FMGCourantNumber = self.__class__.FMGCourantNumber(service, rules, path + [("FMGCourantNumber", "")])
                            self.InitialPressure = self.__class__.InitialPressure(service, rules, path + [("InitialPressure", "")])
                            self.InitialTemperature = self.__class__.InitialTemperature(service, rules, path + [("InitialTemperature", "")])
                            self.InitialTurbIntensity = self.__class__.InitialTurbIntensity(service, rules, path + [("InitialTurbIntensity", "")])
                            self.InitialTurbViscRatio = self.__class__.InitialTurbViscRatio(service, rules, path + [("InitialTurbViscRatio", "")])
                            self.InitialVelocityX = self.__class__.InitialVelocityX(service, rules, path + [("InitialVelocityX", "")])
                            self.InitialVelocityY = self.__class__.InitialVelocityY(service, rules, path + [("InitialVelocityY", "")])
                            self.InitialVelocityZ = self.__class__.InitialVelocityZ(service, rules, path + [("InitialVelocityZ", "")])
                            self.InitializationMethod = self.__class__.InitializationMethod(service, rules, path + [("InitializationMethod", "")])
                            self.StandardInitSync = self.__class__.StandardInitSync(service, rules, path + [("StandardInitSync", "")])
                            super().__init__(service, rules, path)

                        class Boundaries(PyTextual):
                            """
                            Parameter Boundaries of value type List[str].
                            """
                            pass

                        class FMGCourantNumber(PyNumerical):
                            """
                            Parameter FMGCourantNumber of value type float.
                            """
                            pass

                        class InitialPressure(PyNumerical):
                            """
                            Parameter InitialPressure of value type float.
                            """
                            pass

                        class InitialTemperature(PyNumerical):
                            """
                            Parameter InitialTemperature of value type float.
                            """
                            pass

                        class InitialTurbIntensity(PyNumerical):
                            """
                            Parameter InitialTurbIntensity of value type float.
                            """
                            pass

                        class InitialTurbViscRatio(PyNumerical):
                            """
                            Parameter InitialTurbViscRatio of value type float.
                            """
                            pass

                        class InitialVelocityX(PyNumerical):
                            """
                            Parameter InitialVelocityX of value type float.
                            """
                            pass

                        class InitialVelocityY(PyNumerical):
                            """
                            Parameter InitialVelocityY of value type float.
                            """
                            pass

                        class InitialVelocityZ(PyNumerical):
                            """
                            Parameter InitialVelocityZ of value type float.
                            """
                            pass

                        class InitializationMethod(PyTextual):
                            """
                            Parameter InitializationMethod of value type str.
                            """
                            pass

                        class StandardInitSync(PyTextual):
                            """
                            Parameter StandardInitSync of value type str.
                            """
                            pass

                    class FluentTimeIntegration(PyMenu):
                        """
                        Singleton FluentTimeIntegration.
                        """
                        def __init__(self, service, rules, path):
                            self.CourantNumber = self.__class__.CourantNumber(service, rules, path + [("CourantNumber", "")])
                            self.NumIterations = self.__class__.NumIterations(service, rules, path + [("NumIterations", "")])
                            self.SolutionControl = self.__class__.SolutionControl(service, rules, path + [("SolutionControl", "")])
                            self.SteeringBlending = self.__class__.SteeringBlending(service, rules, path + [("SteeringBlending", "")])
                            self.SteeringCourantNumberInitial = self.__class__.SteeringCourantNumberInitial(service, rules, path + [("SteeringCourantNumberInitial", "")])
                            self.SteeringCourantNumberMax = self.__class__.SteeringCourantNumberMax(service, rules, path + [("SteeringCourantNumberMax", "")])
                            self.SteeringRelaxation = self.__class__.SteeringRelaxation(service, rules, path + [("SteeringRelaxation", "")])
                            self.TimeOrder = self.__class__.TimeOrder(service, rules, path + [("TimeOrder", "")])
                            self.TimeScaleFactor = self.__class__.TimeScaleFactor(service, rules, path + [("TimeScaleFactor", "")])
                            self.TimeStep = self.__class__.TimeStep(service, rules, path + [("TimeStep", "")])
                            self.TimeTotal = self.__class__.TimeTotal(service, rules, path + [("TimeTotal", "")])
                            super().__init__(service, rules, path)

                        class CourantNumber(PyNumerical):
                            """
                            Parameter CourantNumber of value type float.
                            """
                            pass

                        class NumIterations(PyNumerical):
                            """
                            Parameter NumIterations of value type int.
                            """
                            pass

                        class SolutionControl(PyTextual):
                            """
                            Parameter SolutionControl of value type str.
                            """
                            pass

                        class SteeringBlending(PyNumerical):
                            """
                            Parameter SteeringBlending of value type float.
                            """
                            pass

                        class SteeringCourantNumberInitial(PyNumerical):
                            """
                            Parameter SteeringCourantNumberInitial of value type float.
                            """
                            pass

                        class SteeringCourantNumberMax(PyNumerical):
                            """
                            Parameter SteeringCourantNumberMax of value type float.
                            """
                            pass

                        class SteeringRelaxation(PyNumerical):
                            """
                            Parameter SteeringRelaxation of value type float.
                            """
                            pass

                        class TimeOrder(PyTextual):
                            """
                            Parameter TimeOrder of value type str.
                            """
                            pass

                        class TimeScaleFactor(PyNumerical):
                            """
                            Parameter TimeScaleFactor of value type float.
                            """
                            pass

                        class TimeStep(PyNumerical):
                            """
                            Parameter TimeStep of value type float.
                            """
                            pass

                        class TimeTotal(PyNumerical):
                            """
                            Parameter TimeTotal of value type float.
                            """
                            pass

                    class ConvergenceAvailable(PyParameter):
                        """
                        Parameter ConvergenceAvailable of value type bool.
                        """
                        pass

                    class SolutionAvailable(PyParameter):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Command Calculate.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Initialize(PyCommand):
                        """
                        Command Initialize.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Command Interrupt.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Load(PyCommand):
                        """
                        Command Load.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Command Reset.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Save(PyCommand):
                        """
                        Command Save.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class SaveAs(PyCommand):
                        """
                        Command SaveAs.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                class CHT(PyMenu):
                    """
                    Singleton CHT.
                    """
                    def __init__(self, service, rules, path):
                        self.CHTOutputSolution = self.__class__.CHTOutputSolution(service, rules, path + [("CHTOutputSolution", "")])
                        self.NumberLoops = self.__class__.NumberLoops(service, rules, path + [("NumberLoops", "")])
                        self.SaveInterval = self.__class__.SaveInterval(service, rules, path + [("SaveInterval", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.SolverIterations = self.__class__.SolverIterations(service, rules, path + [("SolverIterations", "")])
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        self.CalculateICE = self.__class__.CalculateICE(service, rules, "CalculateICE", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Load = self.__class__.Load(service, rules, "Load", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        super().__init__(service, rules, path)

                    class CHTOutputSolution(PyMenu):
                        """
                        Singleton CHTOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Loaded(PyParameter):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class NumberLoops(PyNumerical):
                        """
                        Parameter NumberLoops of value type int.
                        """
                        pass

                    class SaveInterval(PyNumerical):
                        """
                        Parameter SaveInterval of value type int.
                        """
                        pass

                    class SolutionAvailable(PyParameter):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class SolverIterations(PyNumerical):
                        """
                        Parameter SolverIterations of value type int.
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Command Calculate.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class CalculateICE(PyCommand):
                        """
                        Command CalculateICE.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Command Interrupt.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Load(PyCommand):
                        """
                        Command Load.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Command Reset.


                        Returns
                        -------
                        bool
                        """
                        pass

                class GlobalSettings(PyMenu):
                    """
                    Singleton GlobalSettings.
                    """
                    def __init__(self, service, rules, path):
                        self.AutoSave = self.__class__.AutoSave(service, rules, path + [("AutoSave", "")])
                        self.MonitorMode = self.__class__.MonitorMode(service, rules, path + [("MonitorMode", "")])
                        self.PlotInterval = self.__class__.PlotInterval(service, rules, path + [("PlotInterval", "")])
                        self.SaveConverg = self.__class__.SaveConverg(service, rules, path + [("SaveConverg", "")])
                        self.SaveGMRES = self.__class__.SaveGMRES(service, rules, path + [("SaveGMRES", "")])
                        self.Verbosity = self.__class__.Verbosity(service, rules, path + [("Verbosity", "")])
                        super().__init__(service, rules, path)

                    class AutoSave(PyParameter):
                        """
                        Parameter AutoSave of value type bool.
                        """
                        pass

                    class MonitorMode(PyTextual):
                        """
                        Parameter MonitorMode of value type str.
                        """
                        pass

                    class PlotInterval(PyNumerical):
                        """
                        Parameter PlotInterval of value type int.
                        """
                        pass

                    class SaveConverg(PyParameter):
                        """
                        Parameter SaveConverg of value type bool.
                        """
                        pass

                    class SaveGMRES(PyParameter):
                        """
                        Parameter SaveGMRES of value type bool.
                        """
                        pass

                    class Verbosity(PyTextual):
                        """
                        Parameter Verbosity of value type str.
                        """
                        pass

                class IceRun(PyMenu):
                    """
                    Singleton IceRun.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplacementOutputSolution = self.__class__.DisplacementOutputSolution(service, rules, path + [("DisplacementOutputSolution", "")])
                        self.IceAdvanced = self.__class__.IceAdvanced(service, rules, path + [("IceAdvanced", "")])
                        self.IceInit = self.__class__.IceInit(service, rules, path + [("IceInit", "")])
                        self.IceOutput = self.__class__.IceOutput(service, rules, path + [("IceOutput", "")])
                        self.IceOutputSolution = self.__class__.IceOutputSolution(service, rules, path + [("IceOutputSolution", "")])
                        self.IceRemeshing = self.__class__.IceRemeshing(service, rules, path + [("IceRemeshing", "")])
                        self.IceTime = self.__class__.IceTime(service, rules, path + [("IceTime", "")])
                        self.SheddingOutput = self.__class__.SheddingOutput(service, rules, path + [("SheddingOutput", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Load = self.__class__.Load(service, rules, "Load", path)
                        self.MeshMorph = self.__class__.MeshMorph(service, rules, "MeshMorph", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        self.Save = self.__class__.Save(service, rules, "Save", path)
                        self.SaveAs = self.__class__.SaveAs(service, rules, "SaveAs", path)
                        self.SetupRemeshing = self.__class__.SetupRemeshing(service, rules, "SetupRemeshing", path)
                        super().__init__(service, rules, path)

                    class DisplacementOutputSolution(PyMenu):
                        """
                        Singleton DisplacementOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Loaded(PyParameter):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class IceAdvanced(PyMenu):
                        """
                        Singleton IceAdvanced.
                        """
                        def __init__(self, service, rules, path):
                            self.EIDDisable = self.__class__.EIDDisable(service, rules, path + [("EIDDisable", "")])
                            super().__init__(service, rules, path)

                        class EIDDisable(PyParameter):
                            """
                            Parameter EIDDisable of value type bool.
                            """
                            pass

                    class IceInit(PyMenu):
                        """
                        Singleton IceInit.
                        """
                        def __init__(self, service, rules, path):
                            self.Restart = self.__class__.Restart(service, rules, path + [("Restart", "")])
                            super().__init__(service, rules, path)

                        class Restart(PyParameter):
                            """
                            Parameter Restart of value type bool.
                            """
                            pass

                    class IceOutput(PyMenu):
                        """
                        Singleton IceOutput.
                        """
                        def __init__(self, service, rules, path):
                            self.HybridRemeshing = self.__class__.HybridRemeshing(service, rules, path + [("HybridRemeshing", "")])
                            self.RemeshingDelay = self.__class__.RemeshingDelay(service, rules, path + [("RemeshingDelay", "")])
                            self.RemeshingMode = self.__class__.RemeshingMode(service, rules, path + [("RemeshingMode", "")])
                            self.RemeshingSetup = self.__class__.RemeshingSetup(service, rules, path + [("RemeshingSetup", "")])
                            super().__init__(service, rules, path)

                        class HybridRemeshing(PyParameter):
                            """
                            Parameter HybridRemeshing of value type bool.
                            """
                            pass

                        class RemeshingDelay(PyNumerical):
                            """
                            Parameter RemeshingDelay of value type int.
                            """
                            pass

                        class RemeshingMode(PyTextual):
                            """
                            Parameter RemeshingMode of value type str.
                            """
                            pass

                        class RemeshingSetup(PyParameter):
                            """
                            Parameter RemeshingSetup of value type bool.
                            """
                            pass

                    class IceOutputSolution(PyMenu):
                        """
                        Singleton IceOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            self.Roughness = self.__class__.Roughness(service, rules, path + [("Roughness", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyTextual):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class Loaded(PyParameter):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                        class Roughness(PyParameter):
                            """
                            Parameter Roughness of value type bool.
                            """
                            pass

                    class IceRemeshing(PyMenu):
                        """
                        Singleton IceRemeshing.
                        """
                        def __init__(self, service, rules, path):
                            self.Advanced = self.__class__.Advanced(service, rules, path + [("Advanced", "")])
                            self.CellSizingGrowthRate = self.__class__.CellSizingGrowthRate(service, rules, path + [("CellSizingGrowthRate", "")])
                            self.CellSizingType = self.__class__.CellSizingType(service, rules, path + [("CellSizingType", "")])
                            self.CurvGrowthRate = self.__class__.CurvGrowthRate(service, rules, path + [("CurvGrowthRate", "")])
                            self.CurvNormalAngle = self.__class__.CurvNormalAngle(service, rules, path + [("CurvNormalAngle", "")])
                            self.CurvRange = self.__class__.CurvRange(service, rules, path + [("CurvRange", "")])
                            self.Dimension = self.__class__.Dimension(service, rules, path + [("Dimension", "")])
                            self.GlobGrowthRate = self.__class__.GlobGrowthRate(service, rules, path + [("GlobGrowthRate", "")])
                            self.GlobMaxGeoMinSpan3D = self.__class__.GlobMaxGeoMinSpan3D(service, rules, path + [("GlobMaxGeoMinSpan3D", "")])
                            self.GlobRange = self.__class__.GlobRange(service, rules, path + [("GlobRange", "")])
                            self.MaterialPoint = self.__class__.MaterialPoint(service, rules, path + [("MaterialPoint", "")])
                            self.PrismFirstCellAR = self.__class__.PrismFirstCellAR(service, rules, path + [("PrismFirstCellAR", "")])
                            self.PrismGrowthRate = self.__class__.PrismGrowthRate(service, rules, path + [("PrismGrowthRate", "")])
                            self.PrismNLayers = self.__class__.PrismNLayers(service, rules, path + [("PrismNLayers", "")])
                            self.ProxGrowthRate = self.__class__.ProxGrowthRate(service, rules, path + [("ProxGrowthRate", "")])
                            self.ProxMin = self.__class__.ProxMin(service, rules, path + [("ProxMin", "")])
                            self.ProxNCellGap = self.__class__.ProxNCellGap(service, rules, path + [("ProxNCellGap", "")])
                            self.RotPeriodicAngle = self.__class__.RotPeriodicAngle(service, rules, path + [("RotPeriodicAngle", "")])
                            self.RotPeriodicAxis = self.__class__.RotPeriodicAxis(service, rules, path + [("RotPeriodicAxis", "")])
                            self.RotPeriodicCenter = self.__class__.RotPeriodicCenter(service, rules, path + [("RotPeriodicCenter", "")])
                            self.RotPeriodicZones = self.__class__.RotPeriodicZones(service, rules, path + [("RotPeriodicZones", "")])
                            self.RotationalPeriodic = self.__class__.RotationalPeriodic(service, rules, path + [("RotationalPeriodic", "")])
                            self.TransPeriodic = self.__class__.TransPeriodic(service, rules, path + [("TransPeriodic", "")])
                            self.TransPeriodicZones = self.__class__.TransPeriodicZones(service, rules, path + [("TransPeriodicZones", "")])
                            self.TranslationalPeriodic = self.__class__.TranslationalPeriodic(service, rules, path + [("TranslationalPeriodic", "")])
                            self.WrapResolutionFactor = self.__class__.WrapResolutionFactor(service, rules, path + [("WrapResolutionFactor", "")])
                            self.ZSpan = self.__class__.ZSpan(service, rules, path + [("ZSpan", "")])
                            super().__init__(service, rules, path)

                        class Advanced(PyParameter):
                            """
                            Parameter Advanced of value type bool.
                            """
                            pass

                        class CellSizingGrowthRate(PyNumerical):
                            """
                            Parameter CellSizingGrowthRate of value type float.
                            """
                            pass

                        class CellSizingType(PyTextual):
                            """
                            Parameter CellSizingType of value type str.
                            """
                            pass

                        class CurvGrowthRate(PyNumerical):
                            """
                            Parameter CurvGrowthRate of value type float.
                            """
                            pass

                        class CurvNormalAngle(PyNumerical):
                            """
                            Parameter CurvNormalAngle of value type float.
                            """
                            pass

                        class CurvRange(PyParameter):
                            """
                            Parameter CurvRange of value type List[float].
                            """
                            pass

                        class Dimension(PyTextual):
                            """
                            Parameter Dimension of value type str.
                            """
                            pass

                        class GlobGrowthRate(PyNumerical):
                            """
                            Parameter GlobGrowthRate of value type float.
                            """
                            pass

                        class GlobMaxGeoMinSpan3D(PyNumerical):
                            """
                            Parameter GlobMaxGeoMinSpan3D of value type float.
                            """
                            pass

                        class GlobRange(PyParameter):
                            """
                            Parameter GlobRange of value type List[float].
                            """
                            pass

                        class MaterialPoint(PyParameter):
                            """
                            Parameter MaterialPoint of value type List[float].
                            """
                            pass

                        class PrismFirstCellAR(PyNumerical):
                            """
                            Parameter PrismFirstCellAR of value type float.
                            """
                            pass

                        class PrismGrowthRate(PyNumerical):
                            """
                            Parameter PrismGrowthRate of value type float.
                            """
                            pass

                        class PrismNLayers(PyNumerical):
                            """
                            Parameter PrismNLayers of value type int.
                            """
                            pass

                        class ProxGrowthRate(PyNumerical):
                            """
                            Parameter ProxGrowthRate of value type float.
                            """
                            pass

                        class ProxMin(PyNumerical):
                            """
                            Parameter ProxMin of value type float.
                            """
                            pass

                        class ProxNCellGap(PyNumerical):
                            """
                            Parameter ProxNCellGap of value type int.
                            """
                            pass

                        class RotPeriodicAngle(PyNumerical):
                            """
                            Parameter RotPeriodicAngle of value type float.
                            """
                            pass

                        class RotPeriodicAxis(PyParameter):
                            """
                            Parameter RotPeriodicAxis of value type List[float].
                            """
                            pass

                        class RotPeriodicCenter(PyParameter):
                            """
                            Parameter RotPeriodicCenter of value type List[float].
                            """
                            pass

                        class RotPeriodicZones(PyTextual):
                            """
                            Parameter RotPeriodicZones of value type str.
                            """
                            pass

                        class RotationalPeriodic(PyParameter):
                            """
                            Parameter RotationalPeriodic of value type bool.
                            """
                            pass

                        class TransPeriodic(PyParameter):
                            """
                            Parameter TransPeriodic of value type List[float].
                            """
                            pass

                        class TransPeriodicZones(PyTextual):
                            """
                            Parameter TransPeriodicZones of value type str.
                            """
                            pass

                        class TranslationalPeriodic(PyParameter):
                            """
                            Parameter TranslationalPeriodic of value type bool.
                            """
                            pass

                        class WrapResolutionFactor(PyNumerical):
                            """
                            Parameter WrapResolutionFactor of value type float.
                            """
                            pass

                        class ZSpan(PyNumerical):
                            """
                            Parameter ZSpan of value type float.
                            """
                            pass

                    class IceTime(PyMenu):
                        """
                        Singleton IceTime.
                        """
                        def __init__(self, service, rules, path):
                            self.AutoTimeStep = self.__class__.AutoTimeStep(service, rules, path + [("AutoTimeStep", "")])
                            self.TimeStep = self.__class__.TimeStep(service, rules, path + [("TimeStep", "")])
                            self.TotalTime = self.__class__.TotalTime(service, rules, path + [("TotalTime", "")])
                            super().__init__(service, rules, path)

                        class AutoTimeStep(PyParameter):
                            """
                            Parameter AutoTimeStep of value type bool.
                            """
                            pass

                        class TimeStep(PyNumerical):
                            """
                            Parameter TimeStep of value type float.
                            """
                            pass

                        class TotalTime(PyNumerical):
                            """
                            Parameter TotalTime of value type float.
                            """
                            pass

                    class SheddingOutput(PyMenu):
                        """
                        Singleton SheddingOutput.
                        """
                        def __init__(self, service, rules, path):
                            self.OutputFiles = self.__class__.OutputFiles(service, rules, path + [("OutputFiles", "")])
                            self.SheddingInterval = self.__class__.SheddingInterval(service, rules, path + [("SheddingInterval", "")])
                            super().__init__(service, rules, path)

                        class OutputFiles(PyTextual):
                            """
                            Parameter OutputFiles of value type str.
                            """
                            pass

                        class SheddingInterval(PyNumerical):
                            """
                            Parameter SheddingInterval of value type float.
                            """
                            pass

                    class SolutionAvailable(PyParameter):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Command Calculate.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Command Interrupt.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Load(PyCommand):
                        """
                        Command Load.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class MeshMorph(PyCommand):
                        """
                        Command MeshMorph.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Command Reset.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Save(PyCommand):
                        """
                        Command Save.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class SaveAs(PyCommand):
                        """
                        Command SaveAs.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class SetupRemeshing(PyCommand):
                        """
                        Command SetupRemeshing.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                class MultishotRun(PyMenu):
                    """
                    Singleton MultishotRun.
                    """
                    def __init__(self, service, rules, path):
                        self.AirflowRestart = self.__class__.AirflowRestart(service, rules, path + [("AirflowRestart", "")])
                        self.FirstShotAirflowIterations = self.__class__.FirstShotAirflowIterations(service, rules, path + [("FirstShotAirflowIterations", "")])
                        self.FirstShotParticlesIterations = self.__class__.FirstShotParticlesIterations(service, rules, path + [("FirstShotParticlesIterations", "")])
                        self.IterationSettings = self.__class__.IterationSettings(service, rules, path + [("IterationSettings", "")])
                        self.NumberShots = self.__class__.NumberShots(service, rules, path + [("NumberShots", "")])
                        self.RootFilename = self.__class__.RootFilename(service, rules, path + [("RootFilename", "")])
                        self.SaveFiles = self.__class__.SaveFiles(service, rules, path + [("SaveFiles", "")])
                        self.SettingsMode = self.__class__.SettingsMode(service, rules, path + [("SettingsMode", "")])
                        self.ShotRestart = self.__class__.ShotRestart(service, rules, path + [("ShotRestart", "")])
                        self.ShotRestartStep = self.__class__.ShotRestartStep(service, rules, path + [("ShotRestartStep", "")])
                        self.ShotRestartTime = self.__class__.ShotRestartTime(service, rules, path + [("ShotRestartTime", "")])
                        self.TotalTime = self.__class__.TotalTime(service, rules, path + [("TotalTime", "")])
                        super().__init__(service, rules, path)

                    class AirflowRestart(PyTextual):
                        """
                        Parameter AirflowRestart of value type str.
                        """
                        pass

                    class FirstShotAirflowIterations(PyNumerical):
                        """
                        Parameter FirstShotAirflowIterations of value type int.
                        """
                        pass

                    class FirstShotParticlesIterations(PyNumerical):
                        """
                        Parameter FirstShotParticlesIterations of value type int.
                        """
                        pass

                    class IterationSettings(PyTextual):
                        """
                        Parameter IterationSettings of value type str.
                        """
                        pass

                    class NumberShots(PyNumerical):
                        """
                        Parameter NumberShots of value type int.
                        """
                        pass

                    class RootFilename(PyTextual):
                        """
                        Parameter RootFilename of value type str.
                        """
                        pass

                    class SaveFiles(PyParameter):
                        """
                        Parameter SaveFiles of value type bool.
                        """
                        pass

                    class SettingsMode(PyTextual):
                        """
                        Parameter SettingsMode of value type str.
                        """
                        pass

                    class ShotRestart(PyNumerical):
                        """
                        Parameter ShotRestart of value type int.
                        """
                        pass

                    class ShotRestartStep(PyTextual):
                        """
                        Parameter ShotRestartStep of value type str.
                        """
                        pass

                    class ShotRestartTime(PyNumerical):
                        """
                        Parameter ShotRestartTime of value type float.
                        """
                        pass

                    class TotalTime(PyNumerical):
                        """
                        Parameter TotalTime of value type float.
                        """
                        pass

                class ParticlesRun(PyMenu):
                    """
                    Singleton ParticlesRun.
                    """
                    def __init__(self, service, rules, path):
                        self.CrystalOutputSolution = self.__class__.CrystalOutputSolution(service, rules, path + [("CrystalOutputSolution", "")])
                        self.DropletOutputSolution = self.__class__.DropletOutputSolution(service, rules, path + [("DropletOutputSolution", "")])
                        self.InitConditions = self.__class__.InitConditions(service, rules, path + [("InitConditions", "")])
                        self.Monitors = self.__class__.Monitors(service, rules, path + [("Monitors", "")])
                        self.Output = self.__class__.Output(service, rules, path + [("Output", "")])
                        self.RunSettings = self.__class__.RunSettings(service, rules, path + [("RunSettings", "")])
                        self.SolutionInfo = self.__class__.SolutionInfo(service, rules, path + [("SolutionInfo", "")])
                        self.Solver = self.__class__.Solver(service, rules, path + [("Solver", "")])
                        self.VaporOutputSolution = self.__class__.VaporOutputSolution(service, rules, path + [("VaporOutputSolution", "")])
                        self.ConvergenceAvailable = self.__class__.ConvergenceAvailable(service, rules, path + [("ConvergenceAvailable", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.LoadCrystals = self.__class__.LoadCrystals(service, rules, "LoadCrystals", path)
                        self.LoadDroplets = self.__class__.LoadDroplets(service, rules, "LoadDroplets", path)
                        self.LoadParticles = self.__class__.LoadParticles(service, rules, "LoadParticles", path)
                        self.LoadVapor = self.__class__.LoadVapor(service, rules, "LoadVapor", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        self.Save = self.__class__.Save(service, rules, "Save", path)
                        self.SaveAs = self.__class__.SaveAs(service, rules, "SaveAs", path)
                        self.SaveCrystals = self.__class__.SaveCrystals(service, rules, "SaveCrystals", path)
                        self.SaveDroplets = self.__class__.SaveDroplets(service, rules, "SaveDroplets", path)
                        self.SaveVapor = self.__class__.SaveVapor(service, rules, "SaveVapor", path)
                        super().__init__(service, rules, path)

                    class CrystalOutputSolution(PyMenu):
                        """
                        Singleton CrystalOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyTextual):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class Loaded(PyParameter):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class DropletOutputSolution(PyMenu):
                        """
                        Singleton DropletOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyTextual):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class Loaded(PyParameter):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class InitConditions(PyMenu):
                        """
                        Singleton InitConditions.
                        """
                        def __init__(self, service, rules, path):
                            self.Alpha = self.__class__.Alpha(service, rules, path + [("Alpha", "")])
                            self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                            self.DryInit = self.__class__.DryInit(service, rules, path + [("DryInit", "")])
                            self.InitMode = self.__class__.InitMode(service, rules, path + [("InitMode", "")])
                            self.Magnitude = self.__class__.Magnitude(service, rules, path + [("Magnitude", "")])
                            self.VelocityFlag = self.__class__.VelocityFlag(service, rules, path + [("VelocityFlag", "")])
                            self.VelocityX = self.__class__.VelocityX(service, rules, path + [("VelocityX", "")])
                            self.VelocityY = self.__class__.VelocityY(service, rules, path + [("VelocityY", "")])
                            self.VelocityZ = self.__class__.VelocityZ(service, rules, path + [("VelocityZ", "")])
                            super().__init__(service, rules, path)

                        class Alpha(PyNumerical):
                            """
                            Parameter Alpha of value type float.
                            """
                            pass

                        class Beta(PyNumerical):
                            """
                            Parameter Beta of value type float.
                            """
                            pass

                        class DryInit(PyParameter):
                            """
                            Parameter DryInit of value type bool.
                            """
                            pass

                        class InitMode(PyTextual):
                            """
                            Parameter InitMode of value type str.
                            """
                            pass

                        class Magnitude(PyNumerical):
                            """
                            Parameter Magnitude of value type float.
                            """
                            pass

                        class VelocityFlag(PyParameter):
                            """
                            Parameter VelocityFlag of value type bool.
                            """
                            pass

                        class VelocityX(PyNumerical):
                            """
                            Parameter VelocityX of value type float.
                            """
                            pass

                        class VelocityY(PyNumerical):
                            """
                            Parameter VelocityY of value type float.
                            """
                            pass

                        class VelocityZ(PyNumerical):
                            """
                            Parameter VelocityZ of value type float.
                            """
                            pass

                    class Monitors(PyMenu):
                        """
                        Singleton Monitors.
                        """
                        def __init__(self, service, rules, path):
                            self.ChangeBeta = self.__class__.ChangeBeta(service, rules, path + [("ChangeBeta", "")])
                            self.MassDeficit = self.__class__.MassDeficit(service, rules, path + [("MassDeficit", "")])
                            self.TotalBeta = self.__class__.TotalBeta(service, rules, path + [("TotalBeta", "")])
                            self.VaporCondensation = self.__class__.VaporCondensation(service, rules, path + [("VaporCondensation", "")])
                            super().__init__(service, rules, path)

                        class ChangeBeta(PyParameter):
                            """
                            Parameter ChangeBeta of value type bool.
                            """
                            pass

                        class MassDeficit(PyParameter):
                            """
                            Parameter MassDeficit of value type bool.
                            """
                            pass

                        class TotalBeta(PyParameter):
                            """
                            Parameter TotalBeta of value type bool.
                            """
                            pass

                        class VaporCondensation(PyParameter):
                            """
                            Parameter VaporCondensation of value type bool.
                            """
                            pass

                    class Output(PyMenu):
                        """
                        Singleton Output.
                        """
                        def __init__(self, service, rules, path):
                            self.AutoSaveDistribution = self.__class__.AutoSaveDistribution(service, rules, path + [("AutoSaveDistribution", "")])
                            self.DistributionRestart = self.__class__.DistributionRestart(service, rules, path + [("DistributionRestart", "")])
                            self.NumberedOutput = self.__class__.NumberedOutput(service, rules, path + [("NumberedOutput", "")])
                            self.SaveDelay = self.__class__.SaveDelay(service, rules, path + [("SaveDelay", "")])
                            super().__init__(service, rules, path)

                        class AutoSaveDistribution(PyParameter):
                            """
                            Parameter AutoSaveDistribution of value type bool.
                            """
                            pass

                        class DistributionRestart(PyTextual):
                            """
                            Parameter DistributionRestart of value type str.
                            """
                            pass

                        class NumberedOutput(PyParameter):
                            """
                            Parameter NumberedOutput of value type bool.
                            """
                            pass

                        class SaveDelay(PyNumerical):
                            """
                            Parameter SaveDelay of value type int.
                            """
                            pass

                    class RunSettings(PyMenu):
                        """
                        Singleton RunSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.HighResTrack = self.__class__.HighResTrack(service, rules, path + [("HighResTrack", "")])
                            self.MaxStepNumber = self.__class__.MaxStepNumber(service, rules, path + [("MaxStepNumber", "")])
                            self.NumIterations = self.__class__.NumIterations(service, rules, path + [("NumIterations", "")])
                            self.StepLengthFactor = self.__class__.StepLengthFactor(service, rules, path + [("StepLengthFactor", "")])
                            self.StepLengthScale = self.__class__.StepLengthScale(service, rules, path + [("StepLengthScale", "")])
                            self.UseStepLengthScale = self.__class__.UseStepLengthScale(service, rules, path + [("UseStepLengthScale", "")])
                            super().__init__(service, rules, path)

                        class HighResTrack(PyParameter):
                            """
                            Parameter HighResTrack of value type bool.
                            """
                            pass

                        class MaxStepNumber(PyNumerical):
                            """
                            Parameter MaxStepNumber of value type int.
                            """
                            pass

                        class NumIterations(PyNumerical):
                            """
                            Parameter NumIterations of value type int.
                            """
                            pass

                        class StepLengthFactor(PyNumerical):
                            """
                            Parameter StepLengthFactor of value type int.
                            """
                            pass

                        class StepLengthScale(PyNumerical):
                            """
                            Parameter StepLengthScale of value type float.
                            """
                            pass

                        class UseStepLengthScale(PyParameter):
                            """
                            Parameter UseStepLengthScale of value type bool.
                            """
                            pass

                    class SolutionInfo(PyMenu):
                        """
                        Singleton SolutionInfo.
                        """
                        def __init__(self, service, rules, path):
                            self.InputSolutionType = self.__class__.InputSolutionType(service, rules, path + [("InputSolutionType", "")])
                            super().__init__(service, rules, path)

                        class InputSolutionType(PyTextual):
                            """
                            Parameter InputSolutionType of value type str.
                            """
                            pass

                    class Solver(PyMenu):
                        """
                        Singleton Solver.
                        """
                        def __init__(self, service, rules, path):
                            self.AVCoefficient = self.__class__.AVCoefficient(service, rules, path + [("AVCoefficient", "")])
                            self.CFL = self.__class__.CFL(service, rules, path + [("CFL", "")])
                            self.ConvergenceBeta = self.__class__.ConvergenceBeta(service, rules, path + [("ConvergenceBeta", "")])
                            self.ResidualCutoff = self.__class__.ResidualCutoff(service, rules, path + [("ResidualCutoff", "")])
                            super().__init__(service, rules, path)

                        class AVCoefficient(PyNumerical):
                            """
                            Parameter AVCoefficient of value type float.
                            """
                            pass

                        class CFL(PyNumerical):
                            """
                            Parameter CFL of value type float.
                            """
                            pass

                        class ConvergenceBeta(PyNumerical):
                            """
                            Parameter ConvergenceBeta of value type float.
                            """
                            pass

                        class ResidualCutoff(PyNumerical):
                            """
                            Parameter ResidualCutoff of value type float.
                            """
                            pass

                    class VaporOutputSolution(PyMenu):
                        """
                        Singleton VaporOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyTextual):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class Loaded(PyParameter):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class ConvergenceAvailable(PyParameter):
                        """
                        Parameter ConvergenceAvailable of value type bool.
                        """
                        pass

                    class SolutionAvailable(PyParameter):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Command Calculate.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Initialize(PyCommand):
                        """
                        Command Initialize.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Command Interrupt.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class LoadCrystals(PyCommand):
                        """
                        Command LoadCrystals.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class LoadDroplets(PyCommand):
                        """
                        Command LoadDroplets.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class LoadParticles(PyCommand):
                        """
                        Command LoadParticles.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class LoadVapor(PyCommand):
                        """
                        Command LoadVapor.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Command Reset.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class Save(PyCommand):
                        """
                        Command Save.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class SaveAs(PyCommand):
                        """
                        Command SaveAs.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class SaveCrystals(PyCommand):
                        """
                        Command SaveCrystals.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class SaveDroplets(PyCommand):
                        """
                        Command SaveDroplets.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                    class SaveVapor(PyCommand):
                        """
                        Command SaveVapor.

                        Parameters
                        ----------
                        Filename : str

                        Returns
                        -------
                        bool
                        """
                        pass

                class RunState(PyMenu):
                    """
                    Singleton RunState.
                    """
                    def __init__(self, service, rules, path):
                        self.ClientProcessRunning = self.__class__.ClientProcessRunning(service, rules, path + [("ClientProcessRunning", "")])
                        self.CurrentStep = self.__class__.CurrentStep(service, rules, path + [("CurrentStep", "")])
                        self.MultishotState = self.__class__.MultishotState(service, rules, path + [("MultishotState", "")])
                        self.ProjectRunIterator = self.__class__.ProjectRunIterator(service, rules, path + [("ProjectRunIterator", "")])
                        self.RunMode = self.__class__.RunMode(service, rules, path + [("RunMode", "")])
                        self.ShotID = self.__class__.ShotID(service, rules, path + [("ShotID", "")])
                        self.SubStepID = self.__class__.SubStepID(service, rules, path + [("SubStepID", "")])
                        super().__init__(service, rules, path)

                    class ClientProcessRunning(PyParameter):
                        """
                        Parameter ClientProcessRunning of value type bool.
                        """
                        pass

                    class CurrentStep(PyTextual):
                        """
                        Parameter CurrentStep of value type str.
                        """
                        pass

                    class MultishotState(PyTextual):
                        """
                        Parameter MultishotState of value type str.
                        """
                        pass

                    class ProjectRunIterator(PyNumerical):
                        """
                        Parameter ProjectRunIterator of value type int.
                        """
                        pass

                    class RunMode(PyTextual):
                        """
                        Parameter RunMode of value type str.
                        """
                        pass

                    class ShotID(PyNumerical):
                        """
                        Parameter ShotID of value type int.
                        """
                        pass

                    class SubStepID(PyNumerical):
                        """
                        Parameter SubStepID of value type int.
                        """
                        pass

                class Calculate(PyCommand):
                    """
                    Command Calculate.


                    Returns
                    -------
                    bool
                    """
                    pass

                class CalculateOG(PyCommand):
                    """
                    Command CalculateOG.


                    Returns
                    -------
                    bool
                    """
                    pass

                class ConfigureShots(PyCommand):
                    """
                    Command ConfigureShots.


                    Returns
                    -------
                    bool
                    """
                    pass

                class FensapGridSave(PyCommand):
                    """
                    Command FensapGridSave.

                    Parameters
                    ----------
                    Filename : str

                    Returns
                    -------
                    bool
                    """
                    pass

                class Interrupt(PyCommand):
                    """
                    Command Interrupt.


                    Returns
                    -------
                    bool
                    """
                    pass

                class Reset(PyCommand):
                    """
                    Command Reset.


                    Returns
                    -------
                    bool
                    """
                    pass

                class ResetMultishot(PyCommand):
                    """
                    Command ResetMultishot.


                    Returns
                    -------
                    bool
                    """
                    pass

            class InProgress(PyParameter):
                """
                Parameter InProgress of value type bool.
                """
                pass

            class IsBusy(PyParameter):
                """
                Parameter IsBusy of value type bool.
                """
                pass

            class SetupErrors(PyTextual):
                """
                Parameter SetupErrors of value type str.
                """
                pass

            class SetupWarnings(PyTextual):
                """
                Parameter SetupWarnings of value type str.
                """
                pass

            class CheckSetup(PyCommand):
                """
                Command CheckSetup.


                Returns
                -------
                str
                """
                pass

            class IcingImportCase(PyCommand):
                """
                Command IcingImportCase.

                Parameters
                ----------
                Filename : str

                Returns
                -------
                bool
                """
                pass

            class IcingImportMesh(PyCommand):
                """
                Command IcingImportMesh.

                Parameters
                ----------
                Filename : str

                Returns
                -------
                bool
                """
                pass

            class ImportCase(PyCommand):
                """
                Command ImportCase.

                Parameters
                ----------
                Filename : str

                Returns
                -------
                bool
                """
                pass

            class ImportMesh(PyCommand):
                """
                Command ImportMesh.

                Parameters
                ----------
                Filename : str

                Returns
                -------
                bool
                """
                pass

            class InitAddOn(PyCommand):
                """
                Command InitAddOn.


                Returns
                -------
                bool
                """
                pass

            class InitAddOnAero(PyCommand):
                """
                Command InitAddOnAero.


                Returns
                -------
                bool
                """
                pass

            class InitDM(PyCommand):
                """
                Command InitDM.


                Returns
                -------
                bool
                """
                pass

            class LoadCase(PyCommand):
                """
                Command LoadCase.

                Parameters
                ----------
                FileName : str

                Returns
                -------
                bool
                """
                pass

            class LoadCaseAndData(PyCommand):
                """
                Command LoadCaseAndData.

                Parameters
                ----------
                FileName : str

                Returns
                -------
                bool
                """
                pass

            class ReloadCase(PyCommand):
                """
                Command ReloadCase.

                Parameters
                ----------
                Filename : str

                Returns
                -------
                bool
                """
                pass

            class ReloadDomain(PyCommand):
                """
                Command ReloadDomain.

                Parameters
                ----------
                CheckNodeOrder : bool

                Returns
                -------
                bool
                """
                pass

            class SaveCase(PyCommand):
                """
                Command SaveCase.

                Parameters
                ----------
                FileName : str

                Returns
                -------
                bool
                """
                pass

            class SaveCaseAndData(PyCommand):
                """
                Command SaveCaseAndData.

                Parameters
                ----------
                FileName : str

                Returns
                -------
                bool
                """
                pass

            class SaveCaseAs(PyCommand):
                """
                Command SaveCaseAs.

                Parameters
                ----------
                FileName : str

                Returns
                -------
                bool
                """
                pass

            class SaveData(PyCommand):
                """
                Command SaveData.

                Parameters
                ----------
                FileName : str

                Returns
                -------
                bool
                """
                pass

            class SavePostCaseAndData(PyCommand):
                """
                Command SavePostCaseAndData.

                Parameters
                ----------
                FileName : str

                Returns
                -------
                bool
                """
                pass

            class SendCommandQuiet(PyCommand):
                """
                Command SendCommandQuiet.

                Parameters
                ----------
                Command : str

                Returns
                -------
                bool
                """
                pass

            class SyncDM(PyCommand):
                """
                Command SyncDM.


                Returns
                -------
                bool
                """
                pass

            class WriteAll(PyCommand):
                """
                Command WriteAll.

                Parameters
                ----------
                FileName : str

                Returns
                -------
                bool
                """
                pass

        class AppLocal(PyMenu):
            """
            Singleton AppLocal.
            """
            def __init__(self, service, rules, path):
                super().__init__(service, rules, path)

        class AuxiliaryInfo(PyMenu):
            """
            Singleton AuxiliaryInfo.
            """
            def __init__(self, service, rules, path):
                self.DefaultField = self.__class__.DefaultField(service, rules, path + [("DefaultField", "")])
                self.DefaultVectorField = self.__class__.DefaultVectorField(service, rules, path + [("DefaultVectorField", "")])
                self.FluentBoundaryZones = self.__class__.FluentBoundaryZones(service, rules, path + [("FluentBoundaryZones", "")])
                self.IsCourantNumberActive = self.__class__.IsCourantNumberActive(service, rules, path + [("IsCourantNumberActive", "")])
                self.IsDPMWallFilmBC = self.__class__.IsDPMWallFilmBC(service, rules, path + [("IsDPMWallFilmBC", "")])
                self.IsOversetReadOnly = self.__class__.IsOversetReadOnly(service, rules, path + [("IsOversetReadOnly", "")])
                self.IsPVCouplingActive = self.__class__.IsPVCouplingActive(service, rules, path + [("IsPVCouplingActive", "")])
                self.IsSgPDFTransport = self.__class__.IsSgPDFTransport(service, rules, path + [("IsSgPDFTransport", "")])
                self.IsUnsteadyParticleTracking = self.__class__.IsUnsteadyParticleTracking(service, rules, path + [("IsUnsteadyParticleTracking", "")])
                self.MultiPhaseDomainList = self.__class__.MultiPhaseDomainList(service, rules, path + [("MultiPhaseDomainList", "")])
                self.MultiPhaseModel = self.__class__.MultiPhaseModel(service, rules, path + [("MultiPhaseModel", "")])
                self.TimeStepSpecification = self.__class__.TimeStepSpecification(service, rules, path + [("TimeStepSpecification", "")])
                super().__init__(service, rules, path)

            class DefaultField(PyTextual):
                """
                Parameter DefaultField of value type str.
                """
                pass

            class DefaultVectorField(PyTextual):
                """
                Parameter DefaultVectorField of value type str.
                """
                pass

            class FluentBoundaryZones(PyTextual):
                """
                Parameter FluentBoundaryZones of value type List[str].
                """
                pass

            class IsCourantNumberActive(PyParameter):
                """
                Parameter IsCourantNumberActive of value type bool.
                """
                pass

            class IsDPMWallFilmBC(PyParameter):
                """
                Parameter IsDPMWallFilmBC of value type bool.
                """
                pass

            class IsOversetReadOnly(PyParameter):
                """
                Parameter IsOversetReadOnly of value type bool.
                """
                pass

            class IsPVCouplingActive(PyParameter):
                """
                Parameter IsPVCouplingActive of value type bool.
                """
                pass

            class IsSgPDFTransport(PyParameter):
                """
                Parameter IsSgPDFTransport of value type bool.
                """
                pass

            class IsUnsteadyParticleTracking(PyParameter):
                """
                Parameter IsUnsteadyParticleTracking of value type bool.
                """
                pass

            class MultiPhaseDomainList(PyTextual):
                """
                Parameter MultiPhaseDomainList of value type List[str].
                """
                pass

            class MultiPhaseModel(PyTextual):
                """
                Parameter MultiPhaseModel of value type str.
                """
                pass

            class TimeStepSpecification(PyParameter):
                """
                Parameter TimeStepSpecification of value type bool.
                """
                pass

        class CaseInfo(PyMenu):
            """
            Singleton CaseInfo.
            """
            def __init__(self, service, rules, path):
                self.CaseFileName = self.__class__.CaseFileName(service, rules, path + [("CaseFileName", "")])
                self.CaseFileNameDirStripped = self.__class__.CaseFileNameDirStripped(service, rules, path + [("CaseFileNameDirStripped", "")])
                self.Configuration = self.__class__.Configuration(service, rules, path + [("Configuration", "")])
                self.Dimension = self.__class__.Dimension(service, rules, path + [("Dimension", "")])
                self.HostName = self.__class__.HostName(service, rules, path + [("HostName", "")])
                self.IsEduOnlyLogo = self.__class__.IsEduOnlyLogo(service, rules, path + [("IsEduOnlyLogo", "")])
                self.IsStudentOnly = self.__class__.IsStudentOnly(service, rules, path + [("IsStudentOnly", "")])
                self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                super().__init__(service, rules, path)

            class CaseFileName(PyTextual):
                """
                Parameter CaseFileName of value type str.
                """
                pass

            class CaseFileNameDirStripped(PyTextual):
                """
                Parameter CaseFileNameDirStripped of value type str.
                """
                pass

            class Configuration(PyTextual):
                """
                Parameter Configuration of value type str.
                """
                pass

            class Dimension(PyTextual):
                """
                Parameter Dimension of value type str.
                """
                pass

            class HostName(PyTextual):
                """
                Parameter HostName of value type str.
                """
                pass

            class IsEduOnlyLogo(PyParameter):
                """
                Parameter IsEduOnlyLogo of value type bool.
                """
                pass

            class IsStudentOnly(PyParameter):
                """
                Parameter IsStudentOnly of value type bool.
                """
                pass

            class SolverName(PyTextual):
                """
                Parameter SolverName of value type str.
                """
                pass

        class MeshInfo(PyMenu):
            """
            Singleton MeshInfo.
            """
            def __init__(self, service, rules, path):
                self.MeshExtents = self.__class__.MeshExtents(service, rules, path + [("MeshExtents", "")])
                super().__init__(service, rules, path)

            class MeshExtents(PyMenu):
                """
                Singleton MeshExtents.
                """
                def __init__(self, service, rules, path):
                    self.XMax = self.__class__.XMax(service, rules, path + [("XMax", "")])
                    self.XMin = self.__class__.XMin(service, rules, path + [("XMin", "")])
                    self.YMax = self.__class__.YMax(service, rules, path + [("YMax", "")])
                    self.YMin = self.__class__.YMin(service, rules, path + [("YMin", "")])
                    self.ZMax = self.__class__.ZMax(service, rules, path + [("ZMax", "")])
                    self.ZMin = self.__class__.ZMin(service, rules, path + [("ZMin", "")])
                    super().__init__(service, rules, path)

                class XMax(PyNumerical):
                    """
                    Parameter XMax of value type float.
                    """
                    pass

                class XMin(PyNumerical):
                    """
                    Parameter XMin of value type float.
                    """
                    pass

                class YMax(PyNumerical):
                    """
                    Parameter YMax of value type float.
                    """
                    pass

                class YMin(PyNumerical):
                    """
                    Parameter YMin of value type float.
                    """
                    pass

                class ZMax(PyNumerical):
                    """
                    Parameter ZMax of value type float.
                    """
                    pass

                class ZMin(PyNumerical):
                    """
                    Parameter ZMin of value type float.
                    """
                    pass

        class Results(PyMenu):
            """
            Singleton Results.
            """
            def __init__(self, service, rules, path):
                self.Reports = self.__class__.Reports(service, rules, path + [("Reports", "")])
                self.SurfaceDefs = self.__class__.SurfaceDefs(service, rules, path + [("SurfaceDefs", "")])
                self.View = self.__class__.View(service, rules, path + [("View", "")])
                self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
                self.Plots = self.__class__.Plots(service, rules, path + [("Plots", "")])
                self.ResultsExternalInfo = self.__class__.ResultsExternalInfo(service, rules, path + [("ResultsExternalInfo", "")])
                self.CreateCellZoneSurfaces = self.__class__.CreateCellZoneSurfaces(service, rules, "CreateCellZoneSurfaces", path)
                self.CreateMultipleIsosurfaces = self.__class__.CreateMultipleIsosurfaces(service, rules, "CreateMultipleIsosurfaces", path)
                self.CreateMultiplePlanes = self.__class__.CreateMultiplePlanes(service, rules, "CreateMultiplePlanes", path)
                self.GetFieldMinMax = self.__class__.GetFieldMinMax(service, rules, "GetFieldMinMax", path)
                self.GetXYData = self.__class__.GetXYData(service, rules, "GetXYData", path)
                super().__init__(service, rules, path)

            class Reports(PyNamedObjectContainer):
                """
                .
                """
                class _Reports(PyMenu):
                    """
                    Singleton _Reports.
                    """
                    def __init__(self, service, rules, path):
                        self.DensityConstant = self.__class__.DensityConstant(service, rules, path + [("DensityConstant", "")])
                        self.DensityField = self.__class__.DensityField(service, rules, path + [("DensityField", "")])
                        self.DensitySpecification = self.__class__.DensitySpecification(service, rules, path + [("DensitySpecification", "")])
                        self.Expression = self.__class__.Expression(service, rules, path + [("Expression", "")])
                        self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                        self.ForEach = self.__class__.ForEach(service, rules, path + [("ForEach", "")])
                        self.Quantity = self.__class__.Quantity(service, rules, path + [("Quantity", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                        self.VelocityField = self.__class__.VelocityField(service, rules, path + [("VelocityField", "")])
                        self.VolumeFractionField = self.__class__.VolumeFractionField(service, rules, path + [("VolumeFractionField", "")])
                        self.Volumes = self.__class__.Volumes(service, rules, path + [("Volumes", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.GetReport = self.__class__.GetReport(service, rules, "GetReport", path)
                        self.PlotReport = self.__class__.PlotReport(service, rules, "PlotReport", path)
                        self.PrintReport = self.__class__.PrintReport(service, rules, "PrintReport", path)
                        self.SaveReport = self.__class__.SaveReport(service, rules, "SaveReport", path)
                        super().__init__(service, rules, path)

                    class DensityConstant(PyNumerical):
                        """
                        Parameter DensityConstant of value type float.
                        """
                        pass

                    class DensityField(PyTextual):
                        """
                        Parameter DensityField of value type str.
                        """
                        pass

                    class DensitySpecification(PyTextual):
                        """
                        Parameter DensitySpecification of value type str.
                        """
                        pass

                    class Expression(PyTextual):
                        """
                        Parameter Expression of value type str.
                        """
                        pass

                    class Field(PyTextual):
                        """
                        Parameter Field of value type str.
                        """
                        pass

                    class ForEach(PyParameter):
                        """
                        Parameter ForEach of value type bool.
                        """
                        pass

                    class Quantity(PyTextual):
                        """
                        Parameter Quantity of value type str.
                        """
                        pass

                    class Surfaces(PyTextual):
                        """
                        Parameter Surfaces of value type List[str].
                        """
                        pass

                    class Type(PyTextual):
                        """
                        Parameter Type of value type str.
                        """
                        pass

                    class VelocityField(PyTextual):
                        """
                        Parameter VelocityField of value type str.
                        """
                        pass

                    class VolumeFractionField(PyTextual):
                        """
                        Parameter VolumeFractionField of value type str.
                        """
                        pass

                    class Volumes(PyTextual):
                        """
                        Parameter Volumes of value type List[str].
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class GetReport(PyCommand):
                        """
                        Command GetReport.

                        Parameters
                        ----------
                        TimestepSelection : Dict[str, Any]

                        Returns
                        -------
                        List[float]
                        """
                        pass

                    class PlotReport(PyCommand):
                        """
                        Command PlotReport.

                        Parameters
                        ----------
                        TimestepSelection : Dict[str, Any]
                        Title : str
                        XAxis : str
                        XAxisLabel : str
                        YAxisLabel : str

                        Returns
                        -------
                        None
                        """
                        pass

                    class PrintReport(PyCommand):
                        """
                        Command PrintReport.

                        Parameters
                        ----------
                        TimestepSelection : Dict[str, Any]

                        Returns
                        -------
                        None
                        """
                        pass

                    class SaveReport(PyCommand):
                        """
                        Command SaveReport.

                        Parameters
                        ----------
                        Filename : str
                        TimestepSelection : Dict[str, Any]

                        Returns
                        -------
                        None
                        """
                        pass

                def __getitem__(self, key: str) -> _Reports:
                    return super().__getitem__(key)

            class SurfaceDefs(PyNamedObjectContainer):
                """
                .
                """
                class _SurfaceDefs(PyMenu):
                    """
                    Singleton _SurfaceDefs.
                    """
                    def __init__(self, service, rules, path):
                        self.IsoClipSettings = self.__class__.IsoClipSettings(service, rules, path + [("IsoClipSettings", "")])
                        self.IsosurfaceSettings = self.__class__.IsosurfaceSettings(service, rules, path + [("IsosurfaceSettings", "")])
                        self.LineSettings = self.__class__.LineSettings(service, rules, path + [("LineSettings", "")])
                        self.PlaneSettings = self.__class__.PlaneSettings(service, rules, path + [("PlaneSettings", "")])
                        self.PointSettings = self.__class__.PointSettings(service, rules, path + [("PointSettings", "")])
                        self.RakeSettings = self.__class__.RakeSettings(service, rules, path + [("RakeSettings", "")])
                        self.ZoneSettings = self.__class__.ZoneSettings(service, rules, path + [("ZoneSettings", "")])
                        self.GroupName = self.__class__.GroupName(service, rules, path + [("GroupName", "")])
                        self.SurfaceDim = self.__class__.SurfaceDim(service, rules, path + [("SurfaceDim", "")])
                        self.SurfaceId = self.__class__.SurfaceId(service, rules, path + [("SurfaceId", "")])
                        self.SurfaceType = self.__class__.SurfaceType(service, rules, path + [("SurfaceType", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.Display = self.__class__.Display(service, rules, "Display", path)
                        self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                        self.Ungroup = self.__class__.Ungroup(service, rules, "Ungroup", path)
                        super().__init__(service, rules, path)

                    class IsoClipSettings(PyMenu):
                        """
                        Singleton IsoClipSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                            self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class Maximum(PyNumerical):
                            """
                            Parameter Maximum of value type float.
                            """
                            pass

                        class Minimum(PyNumerical):
                            """
                            Parameter Minimum of value type float.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            Command UpdateMinMax.


                            Returns
                            -------
                            None
                            """
                            pass

                    class IsosurfaceSettings(PyMenu):
                        """
                        Singleton IsosurfaceSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.IsoValue = self.__class__.IsoValue(service, rules, path + [("IsoValue", "")])
                            self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                            self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                            self.RestrictToSpecificSurfaces = self.__class__.RestrictToSpecificSurfaces(service, rules, path + [("RestrictToSpecificSurfaces", "")])
                            self.RestrictToSpecificZones = self.__class__.RestrictToSpecificZones(service, rules, path + [("RestrictToSpecificZones", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.Zones = self.__class__.Zones(service, rules, path + [("Zones", "")])
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class IsoValue(PyNumerical):
                            """
                            Parameter IsoValue of value type float.
                            """
                            pass

                        class Maximum(PyNumerical):
                            """
                            Parameter Maximum of value type float.
                            """
                            pass

                        class Minimum(PyNumerical):
                            """
                            Parameter Minimum of value type float.
                            """
                            pass

                        class RestrictToSpecificSurfaces(PyParameter):
                            """
                            Parameter RestrictToSpecificSurfaces of value type bool.
                            """
                            pass

                        class RestrictToSpecificZones(PyParameter):
                            """
                            Parameter RestrictToSpecificZones of value type bool.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class Zones(PyTextual):
                            """
                            Parameter Zones of value type List[str].
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            Command UpdateMinMax.


                            Returns
                            -------
                            None
                            """
                            pass

                    class LineSettings(PyMenu):
                        """
                        Singleton LineSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.EndPoint = self.__class__.EndPoint(service, rules, path + [("EndPoint", "")])
                            self.StartPoint = self.__class__.StartPoint(service, rules, path + [("StartPoint", "")])
                            super().__init__(service, rules, path)

                        class EndPoint(PyMenu):
                            """
                            Singleton EndPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class StartPoint(PyMenu):
                            """
                            Singleton StartPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                    class PlaneSettings(PyMenu):
                        """
                        Singleton PlaneSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.FirstPoint = self.__class__.FirstPoint(service, rules, path + [("FirstPoint", "")])
                            self.Normal = self.__class__.Normal(service, rules, path + [("Normal", "")])
                            self.SecondPoint = self.__class__.SecondPoint(service, rules, path + [("SecondPoint", "")])
                            self.ThirdPoint = self.__class__.ThirdPoint(service, rules, path + [("ThirdPoint", "")])
                            self.Bounded = self.__class__.Bounded(service, rules, path + [("Bounded", "")])
                            self.CreationMode = self.__class__.CreationMode(service, rules, path + [("CreationMode", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            super().__init__(service, rules, path)

                        class FirstPoint(PyMenu):
                            """
                            Singleton FirstPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class Normal(PyMenu):
                            """
                            Singleton Normal.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class SecondPoint(PyMenu):
                            """
                            Singleton SecondPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class ThirdPoint(PyMenu):
                            """
                            Singleton ThirdPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class Bounded(PyParameter):
                            """
                            Parameter Bounded of value type bool.
                            """
                            pass

                        class CreationMode(PyTextual):
                            """
                            Parameter CreationMode of value type str.
                            """
                            pass

                        class X(PyNumerical):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyNumerical):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyNumerical):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                    class PointSettings(PyMenu):
                        """
                        Singleton PointSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.LbClipping = self.__class__.LbClipping(service, rules, path + [("LbClipping", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            super().__init__(service, rules, path)

                        class LbClipping(PyParameter):
                            """
                            Parameter LbClipping of value type bool.
                            """
                            pass

                        class X(PyNumerical):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyNumerical):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyNumerical):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                    class RakeSettings(PyMenu):
                        """
                        Singleton RakeSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.EndPoint = self.__class__.EndPoint(service, rules, path + [("EndPoint", "")])
                            self.StartPoint = self.__class__.StartPoint(service, rules, path + [("StartPoint", "")])
                            self.NumberOfPoints = self.__class__.NumberOfPoints(service, rules, path + [("NumberOfPoints", "")])
                            super().__init__(service, rules, path)

                        class EndPoint(PyMenu):
                            """
                            Singleton EndPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class StartPoint(PyMenu):
                            """
                            Singleton StartPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class NumberOfPoints(PyNumerical):
                            """
                            Parameter NumberOfPoints of value type int.
                            """
                            pass

                    class ZoneSettings(PyMenu):
                        """
                        Singleton ZoneSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.IdList = self.__class__.IdList(service, rules, path + [("IdList", "")])
                            self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                            self.ZId = self.__class__.ZId(service, rules, path + [("ZId", "")])
                            self.ZType = self.__class__.ZType(service, rules, path + [("ZType", "")])
                            super().__init__(service, rules, path)

                        class IdList(PyParameter):
                            """
                            Parameter IdList of value type List[int].
                            """
                            pass

                        class Type(PyTextual):
                            """
                            Parameter Type of value type str.
                            """
                            pass

                        class ZId(PyNumerical):
                            """
                            Parameter ZId of value type int.
                            """
                            pass

                        class ZType(PyTextual):
                            """
                            Parameter ZType of value type str.
                            """
                            pass

                    class GroupName(PyTextual):
                        """
                        Parameter GroupName of value type str.
                        """
                        pass

                    class SurfaceDim(PyTextual):
                        """
                        Parameter SurfaceDim of value type List[str].
                        """
                        pass

                    class SurfaceId(PyNumerical):
                        """
                        Parameter SurfaceId of value type int.
                        """
                        pass

                    class SurfaceType(PyTextual):
                        """
                        Parameter SurfaceType of value type str.
                        """
                        pass

                    class Surfaces(PyTextual):
                        """
                        Parameter Surfaces of value type List[str].
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class Display(PyCommand):
                        """
                        Command Display.


                        Returns
                        -------
                        bool
                        """
                        pass

                    class SaveImage(PyCommand):
                        """
                        Command SaveImage.

                        Parameters
                        ----------
                        FileName : str
                        Format : str
                        FileType : str
                        Coloring : str
                        Orientation : str
                        UseWhiteBackground : bool
                        Resolution : Dict[str, Any]

                        Returns
                        -------
                        bool
                        """
                        pass

                    class Ungroup(PyCommand):
                        """
                        Command Ungroup.


                        Returns
                        -------
                        bool
                        """
                        pass

                def __getitem__(self, key: str) -> _SurfaceDefs:
                    return super().__getitem__(key)

            class View(PyNamedObjectContainer):
                """
                .
                """
                class _View(PyMenu):
                    """
                    Singleton _View.
                    """
                    def __init__(self, service, rules, path):
                        self.Camera = self.__class__.Camera(service, rules, path + [("Camera", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.RestoreView = self.__class__.RestoreView(service, rules, "RestoreView", path)
                        super().__init__(service, rules, path)

                    class Camera(PyMenu):
                        """
                        Singleton Camera.
                        """
                        def __init__(self, service, rules, path):
                            self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                            self.Target = self.__class__.Target(service, rules, path + [("Target", "")])
                            self.UpVector = self.__class__.UpVector(service, rules, path + [("UpVector", "")])
                            self.Height = self.__class__.Height(service, rules, path + [("Height", "")])
                            self.Projection = self.__class__.Projection(service, rules, path + [("Projection", "")])
                            self.Width = self.__class__.Width(service, rules, path + [("Width", "")])
                            super().__init__(service, rules, path)

                        class Position(PyMenu):
                            """
                            Singleton Position.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyNumerical):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyNumerical):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyNumerical):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class Target(PyMenu):
                            """
                            Singleton Target.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyNumerical):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyNumerical):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyNumerical):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class UpVector(PyMenu):
                            """
                            Singleton UpVector.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyNumerical):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyNumerical):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyNumerical):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class Height(PyNumerical):
                            """
                            Parameter Height of value type float.
                            """
                            pass

                        class Projection(PyTextual):
                            """
                            Parameter Projection of value type str.
                            """
                            pass

                        class Width(PyNumerical):
                            """
                            Parameter Width of value type float.
                            """
                            pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class RestoreView(PyCommand):
                        """
                        Command RestoreView.


                        Returns
                        -------
                        bool
                        """
                        pass

                def __getitem__(self, key: str) -> _View:
                    return super().__getitem__(key)

            class Graphics(PyMenu):
                """
                Singleton Graphics.
                """
                def __init__(self, service, rules, path):
                    self.Contour = self.__class__.Contour(service, rules, path + [("Contour", "")])
                    self.LIC = self.__class__.LIC(service, rules, path + [("LIC", "")])
                    self.Mesh = self.__class__.Mesh(service, rules, path + [("Mesh", "")])
                    self.ParticleTracks = self.__class__.ParticleTracks(service, rules, path + [("ParticleTracks", "")])
                    self.Pathlines = self.__class__.Pathlines(service, rules, path + [("Pathlines", "")])
                    self.Scene = self.__class__.Scene(service, rules, path + [("Scene", "")])
                    self.Vector = self.__class__.Vector(service, rules, path + [("Vector", "")])
                    self.XYPlot = self.__class__.XYPlot(service, rules, path + [("XYPlot", "")])
                    self.CameraSettings = self.__class__.CameraSettings(service, rules, path + [("CameraSettings", "")])
                    self.GridColors = self.__class__.GridColors(service, rules, path + [("GridColors", "")])
                    self.GraphicsCreationCount = self.__class__.GraphicsCreationCount(service, rules, path + [("GraphicsCreationCount", "")])
                    self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                    super().__init__(service, rules, path)

                class Contour(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Contour(PyMenu):
                        """
                        Singleton _Contour.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.BoundaryValues = self.__class__.BoundaryValues(service, rules, path + [("BoundaryValues", "")])
                            self.Coloring = self.__class__.Coloring(service, rules, path + [("Coloring", "")])
                            self.ContourLines = self.__class__.ContourLines(service, rules, path + [("ContourLines", "")])
                            self.DisplayLIC = self.__class__.DisplayLIC(service, rules, path + [("DisplayLIC", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Filled = self.__class__.Filled(service, rules, path + [("Filled", "")])
                            self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyParameter):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                            class GlobalRange(PyParameter):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class BoundaryValues(PyParameter):
                            """
                            Parameter BoundaryValues of value type bool.
                            """
                            pass

                        class Coloring(PyTextual):
                            """
                            Parameter Coloring of value type str.
                            """
                            pass

                        class ContourLines(PyParameter):
                            """
                            Parameter ContourLines of value type bool.
                            """
                            pass

                        class DisplayLIC(PyParameter):
                            """
                            Parameter DisplayLIC of value type bool.
                            """
                            pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class Filled(PyParameter):
                            """
                            Parameter Filled of value type bool.
                            """
                            pass

                        class NodeValues(PyParameter):
                            """
                            Parameter NodeValues of value type bool.
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            Command AddToViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class DisplayInViewport(PyCommand):
                            """
                            Command DisplayInViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            Command UpdateMinMax.


                            Returns
                            -------
                            None
                            """
                            pass

                    def __getitem__(self, key: str) -> _Contour:
                        return super().__getitem__(key)

                class LIC(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _LIC(PyMenu):
                        """
                        Singleton _LIC.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.FastLic = self.__class__.FastLic(service, rules, path + [("FastLic", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.GrayScale = self.__class__.GrayScale(service, rules, path + [("GrayScale", "")])
                            self.ImageFilter = self.__class__.ImageFilter(service, rules, path + [("ImageFilter", "")])
                            self.ImageToDisplay = self.__class__.ImageToDisplay(service, rules, path + [("ImageToDisplay", "")])
                            self.IntensityAlpha = self.__class__.IntensityAlpha(service, rules, path + [("IntensityAlpha", "")])
                            self.IntensityFactor = self.__class__.IntensityFactor(service, rules, path + [("IntensityFactor", "")])
                            self.LicColor = self.__class__.LicColor(service, rules, path + [("LicColor", "")])
                            self.LicColorByField = self.__class__.LicColorByField(service, rules, path + [("LicColorByField", "")])
                            self.LicMaxSteps = self.__class__.LicMaxSteps(service, rules, path + [("LicMaxSteps", "")])
                            self.LicNormalize = self.__class__.LicNormalize(service, rules, path + [("LicNormalize", "")])
                            self.LicPixelInterp = self.__class__.LicPixelInterp(service, rules, path + [("LicPixelInterp", "")])
                            self.OrientedLic = self.__class__.OrientedLic(service, rules, path + [("OrientedLic", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.TextureSize = self.__class__.TextureSize(service, rules, path + [("TextureSize", "")])
                            self.TextureSpacing = self.__class__.TextureSpacing(service, rules, path + [("TextureSpacing", "")])
                            self.VectorField = self.__class__.VectorField(service, rules, path + [("VectorField", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyParameter):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                            class GlobalRange(PyParameter):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class FastLic(PyParameter):
                            """
                            Parameter FastLic of value type bool.
                            """
                            pass

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class GrayScale(PyParameter):
                            """
                            Parameter GrayScale of value type bool.
                            """
                            pass

                        class ImageFilter(PyTextual):
                            """
                            Parameter ImageFilter of value type str.
                            """
                            pass

                        class ImageToDisplay(PyTextual):
                            """
                            Parameter ImageToDisplay of value type str.
                            """
                            pass

                        class IntensityAlpha(PyParameter):
                            """
                            Parameter IntensityAlpha of value type bool.
                            """
                            pass

                        class IntensityFactor(PyNumerical):
                            """
                            Parameter IntensityFactor of value type int.
                            """
                            pass

                        class LicColor(PyTextual):
                            """
                            Parameter LicColor of value type str.
                            """
                            pass

                        class LicColorByField(PyParameter):
                            """
                            Parameter LicColorByField of value type bool.
                            """
                            pass

                        class LicMaxSteps(PyNumerical):
                            """
                            Parameter LicMaxSteps of value type int.
                            """
                            pass

                        class LicNormalize(PyParameter):
                            """
                            Parameter LicNormalize of value type bool.
                            """
                            pass

                        class LicPixelInterp(PyParameter):
                            """
                            Parameter LicPixelInterp of value type bool.
                            """
                            pass

                        class OrientedLic(PyParameter):
                            """
                            Parameter OrientedLic of value type bool.
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class TextureSize(PyNumerical):
                            """
                            Parameter TextureSize of value type int.
                            """
                            pass

                        class TextureSpacing(PyNumerical):
                            """
                            Parameter TextureSpacing of value type int.
                            """
                            pass

                        class VectorField(PyTextual):
                            """
                            Parameter VectorField of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _LIC:
                        return super().__getitem__(key)

                class Mesh(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Mesh(PyMenu):
                        """
                        Singleton _Mesh.
                        """
                        def __init__(self, service, rules, path):
                            self.EdgeOptions = self.__class__.EdgeOptions(service, rules, path + [("EdgeOptions", "")])
                            self.MeshColoring = self.__class__.MeshColoring(service, rules, path + [("MeshColoring", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.DisplayLIC = self.__class__.DisplayLIC(service, rules, path + [("DisplayLIC", "")])
                            self.ShrinkFactor = self.__class__.ShrinkFactor(service, rules, path + [("ShrinkFactor", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class EdgeOptions(PyMenu):
                            """
                            Singleton EdgeOptions.
                            """
                            def __init__(self, service, rules, path):
                                self.FeatureAngle = self.__class__.FeatureAngle(service, rules, path + [("FeatureAngle", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                super().__init__(service, rules, path)

                            class FeatureAngle(PyNumerical):
                                """
                                Parameter FeatureAngle of value type float.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                        class MeshColoring(PyMenu):
                            """
                            Singleton MeshColoring.
                            """
                            def __init__(self, service, rules, path):
                                self.Automatic = self.__class__.Automatic(service, rules, path + [("Automatic", "")])
                                self.ColorBy = self.__class__.ColorBy(service, rules, path + [("ColorBy", "")])
                                self.ColorEdgesBy = self.__class__.ColorEdgesBy(service, rules, path + [("ColorEdgesBy", "")])
                                self.ColorFacesBy = self.__class__.ColorFacesBy(service, rules, path + [("ColorFacesBy", "")])
                                self.ColorNodesBy = self.__class__.ColorNodesBy(service, rules, path + [("ColorNodesBy", "")])
                                super().__init__(service, rules, path)

                            class Automatic(PyParameter):
                                """
                                Parameter Automatic of value type bool.
                                """
                                pass

                            class ColorBy(PyTextual):
                                """
                                Parameter ColorBy of value type str.
                                """
                                pass

                            class ColorEdgesBy(PyTextual):
                                """
                                Parameter ColorEdgesBy of value type str.
                                """
                                pass

                            class ColorFacesBy(PyTextual):
                                """
                                Parameter ColorFacesBy of value type str.
                                """
                                pass

                            class ColorNodesBy(PyTextual):
                                """
                                Parameter ColorNodesBy of value type str.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.Edges = self.__class__.Edges(service, rules, path + [("Edges", "")])
                                self.Faces = self.__class__.Faces(service, rules, path + [("Faces", "")])
                                self.Nodes = self.__class__.Nodes(service, rules, path + [("Nodes", "")])
                                self.Overset = self.__class__.Overset(service, rules, path + [("Overset", "")])
                                self.Partitions = self.__class__.Partitions(service, rules, path + [("Partitions", "")])
                                super().__init__(service, rules, path)

                            class Edges(PyParameter):
                                """
                                Parameter Edges of value type bool.
                                """
                                pass

                            class Faces(PyParameter):
                                """
                                Parameter Faces of value type bool.
                                """
                                pass

                            class Nodes(PyParameter):
                                """
                                Parameter Nodes of value type bool.
                                """
                                pass

                            class Overset(PyParameter):
                                """
                                Parameter Overset of value type bool.
                                """
                                pass

                            class Partitions(PyParameter):
                                """
                                Parameter Partitions of value type bool.
                                """
                                pass

                        class DisplayLIC(PyParameter):
                            """
                            Parameter DisplayLIC of value type bool.
                            """
                            pass

                        class ShrinkFactor(PyNumerical):
                            """
                            Parameter ShrinkFactor of value type float.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            Command AddToViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class DisplayInViewport(PyCommand):
                            """
                            Command DisplayInViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Mesh:
                        return super().__getitem__(key)

                class ParticleTracks(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _ParticleTracks(PyMenu):
                        """
                        Singleton _ParticleTracks.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Filter = self.__class__.Filter(service, rules, path + [("Filter", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.Plot = self.__class__.Plot(service, rules, path + [("Plot", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.TrackSingleParticleStream = self.__class__.TrackSingleParticleStream(service, rules, path + [("TrackSingleParticleStream", "")])
                            self.VectorStyle = self.__class__.VectorStyle(service, rules, path + [("VectorStyle", "")])
                            self.Coarsen = self.__class__.Coarsen(service, rules, path + [("Coarsen", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.FreeStreamParticles = self.__class__.FreeStreamParticles(service, rules, path + [("FreeStreamParticles", "")])
                            self.Injections = self.__class__.Injections(service, rules, path + [("Injections", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.ParticleTracksField = self.__class__.ParticleTracksField(service, rules, path + [("ParticleTracksField", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.TrackPDFParticles = self.__class__.TrackPDFParticles(service, rules, path + [("TrackPDFParticles", "")])
                            self.WallFilmParticles = self.__class__.WallFilmParticles(service, rules, path + [("WallFilmParticles", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Filter(PyMenu):
                            """
                            Singleton Filter.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.FilterField = self.__class__.FilterField(service, rules, path + [("FilterField", "")])
                                self.Inside = self.__class__.Inside(service, rules, path + [("Inside", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyParameter):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class FilterField(PyTextual):
                                """
                                Parameter FilterField of value type str.
                                """
                                pass

                            class Inside(PyParameter):
                                """
                                Parameter Inside of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyParameter):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                        class Plot(PyMenu):
                            """
                            Singleton Plot.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyParameter):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class XAxisFunction(PyTextual):
                                """
                                Parameter XAxisFunction of value type str.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Style(PyMenu):
                            """
                            Singleton Style.
                            """
                            def __init__(self, service, rules, path):
                                self.Ribbon = self.__class__.Ribbon(service, rules, path + [("Ribbon", "")])
                                self.Sphere = self.__class__.Sphere(service, rules, path + [("Sphere", "")])
                                self.ArrowScale = self.__class__.ArrowScale(service, rules, path + [("ArrowScale", "")])
                                self.ArrowSpace = self.__class__.ArrowSpace(service, rules, path + [("ArrowSpace", "")])
                                self.LineWidth = self.__class__.LineWidth(service, rules, path + [("LineWidth", "")])
                                self.MarkerSize = self.__class__.MarkerSize(service, rules, path + [("MarkerSize", "")])
                                self.Radius = self.__class__.Radius(service, rules, path + [("Radius", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                super().__init__(service, rules, path)

                            class Ribbon(PyMenu):
                                """
                                Singleton Ribbon.
                                """
                                def __init__(self, service, rules, path):
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    super().__init__(service, rules, path)

                                class Field(PyTextual):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class ScaleFactor(PyNumerical):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                            class Sphere(PyMenu):
                                """
                                Singleton Sphere.
                                """
                                def __init__(self, service, rules, path):
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    self.SphereField = self.__class__.SphereField(service, rules, path + [("SphereField", "")])
                                    self.SphereLod = self.__class__.SphereLod(service, rules, path + [("SphereLod", "")])
                                    self.SphereSize = self.__class__.SphereSize(service, rules, path + [("SphereSize", "")])
                                    self.VariableSize = self.__class__.VariableSize(service, rules, path + [("VariableSize", "")])
                                    super().__init__(service, rules, path)

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                        self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                        super().__init__(service, rules, path)

                                    class AutoRange(PyParameter):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class MaxValue(PyNumerical):
                                        """
                                        Parameter MaxValue of value type float.
                                        """
                                        pass

                                    class MinValue(PyNumerical):
                                        """
                                        Parameter MinValue of value type float.
                                        """
                                        pass

                                class ScaleFactor(PyNumerical):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                                class SphereField(PyTextual):
                                    """
                                    Parameter SphereField of value type str.
                                    """
                                    pass

                                class SphereLod(PyNumerical):
                                    """
                                    Parameter SphereLod of value type int.
                                    """
                                    pass

                                class SphereSize(PyNumerical):
                                    """
                                    Parameter SphereSize of value type float.
                                    """
                                    pass

                                class VariableSize(PyParameter):
                                    """
                                    Parameter VariableSize of value type bool.
                                    """
                                    pass

                            class ArrowScale(PyNumerical):
                                """
                                Parameter ArrowScale of value type float.
                                """
                                pass

                            class ArrowSpace(PyNumerical):
                                """
                                Parameter ArrowSpace of value type float.
                                """
                                pass

                            class LineWidth(PyNumerical):
                                """
                                Parameter LineWidth of value type float.
                                """
                                pass

                            class MarkerSize(PyNumerical):
                                """
                                Parameter MarkerSize of value type float.
                                """
                                pass

                            class Radius(PyNumerical):
                                """
                                Parameter Radius of value type float.
                                """
                                pass

                            class Style(PyTextual):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                        class TrackSingleParticleStream(PyMenu):
                            """
                            Singleton TrackSingleParticleStream.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.StreamId = self.__class__.StreamId(service, rules, path + [("StreamId", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyParameter):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class StreamId(PyNumerical):
                                """
                                Parameter StreamId of value type int.
                                """
                                pass

                        class VectorStyle(PyMenu):
                            """
                            Singleton VectorStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.VectorAttribute = self.__class__.VectorAttribute(service, rules, path + [("VectorAttribute", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                super().__init__(service, rules, path)

                            class VectorAttribute(PyMenu):
                                """
                                Singleton VectorAttribute.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.ConstantColor = self.__class__.ConstantColor(service, rules, path + [("ConstantColor", "")])
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.Length = self.__class__.Length(service, rules, path + [("Length", "")])
                                    self.LengthToHeadRatio = self.__class__.LengthToHeadRatio(service, rules, path + [("LengthToHeadRatio", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    self.VariableLength = self.__class__.VariableLength(service, rules, path + [("VariableLength", "")])
                                    self.VectorsOf = self.__class__.VectorsOf(service, rules, path + [("VectorsOf", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class ConstantColor(PyParameter):
                                    """
                                    Parameter ConstantColor of value type bool.
                                    """
                                    pass

                                class Field(PyTextual):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class Length(PyNumerical):
                                    """
                                    Parameter Length of value type float.
                                    """
                                    pass

                                class LengthToHeadRatio(PyNumerical):
                                    """
                                    Parameter LengthToHeadRatio of value type float.
                                    """
                                    pass

                                class ScaleFactor(PyNumerical):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                                class VariableLength(PyParameter):
                                    """
                                    Parameter VariableLength of value type bool.
                                    """
                                    pass

                                class VectorsOf(PyTextual):
                                    """
                                    Parameter VectorsOf of value type str.
                                    """
                                    pass

                            class Style(PyTextual):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                        class Coarsen(PyNumerical):
                            """
                            Parameter Coarsen of value type int.
                            """
                            pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class FreeStreamParticles(PyParameter):
                            """
                            Parameter FreeStreamParticles of value type bool.
                            """
                            pass

                        class Injections(PyTextual):
                            """
                            Parameter Injections of value type List[str].
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class ParticleTracksField(PyTextual):
                            """
                            Parameter ParticleTracksField of value type str.
                            """
                            pass

                        class Skip(PyNumerical):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class TrackPDFParticles(PyParameter):
                            """
                            Parameter TrackPDFParticles of value type bool.
                            """
                            pass

                        class WallFilmParticles(PyParameter):
                            """
                            Parameter WallFilmParticles of value type bool.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _ParticleTracks:
                        return super().__getitem__(key)

                class Pathlines(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Pathlines(PyMenu):
                        """
                        Singleton _Pathlines.
                        """
                        def __init__(self, service, rules, path):
                            self.AccuracyControl = self.__class__.AccuracyControl(service, rules, path + [("AccuracyControl", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.Plot = self.__class__.Plot(service, rules, path + [("Plot", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.Coarsen = self.__class__.Coarsen(service, rules, path + [("Coarsen", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.OnZone = self.__class__.OnZone(service, rules, path + [("OnZone", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.PathlinesField = self.__class__.PathlinesField(service, rules, path + [("PathlinesField", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.Step = self.__class__.Step(service, rules, path + [("Step", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.UID = self.__class__.UID(service, rules, path + [("UID", "")])
                            self.VelocityDomain = self.__class__.VelocityDomain(service, rules, path + [("VelocityDomain", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class AccuracyControl(PyMenu):
                            """
                            Singleton AccuracyControl.
                            """
                            def __init__(self, service, rules, path):
                                self.AccuracyControlOn = self.__class__.AccuracyControlOn(service, rules, path + [("AccuracyControlOn", "")])
                                self.StepSize = self.__class__.StepSize(service, rules, path + [("StepSize", "")])
                                self.Tolerance = self.__class__.Tolerance(service, rules, path + [("Tolerance", "")])
                                super().__init__(service, rules, path)

                            class AccuracyControlOn(PyParameter):
                                """
                                Parameter AccuracyControlOn of value type bool.
                                """
                                pass

                            class StepSize(PyNumerical):
                                """
                                Parameter StepSize of value type float.
                                """
                                pass

                            class Tolerance(PyNumerical):
                                """
                                Parameter Tolerance of value type float.
                                """
                                pass

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                self.OilFlow = self.__class__.OilFlow(service, rules, path + [("OilFlow", "")])
                                self.Relative = self.__class__.Relative(service, rules, path + [("Relative", "")])
                                self.Reverse = self.__class__.Reverse(service, rules, path + [("Reverse", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyParameter):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                            class OilFlow(PyParameter):
                                """
                                Parameter OilFlow of value type bool.
                                """
                                pass

                            class Relative(PyParameter):
                                """
                                Parameter Relative of value type bool.
                                """
                                pass

                            class Reverse(PyParameter):
                                """
                                Parameter Reverse of value type bool.
                                """
                                pass

                        class Plot(PyMenu):
                            """
                            Singleton Plot.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyParameter):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class XAxisFunction(PyTextual):
                                """
                                Parameter XAxisFunction of value type str.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Style(PyMenu):
                            """
                            Singleton Style.
                            """
                            def __init__(self, service, rules, path):
                                self.Ribbon = self.__class__.Ribbon(service, rules, path + [("Ribbon", "")])
                                self.ArrowScale = self.__class__.ArrowScale(service, rules, path + [("ArrowScale", "")])
                                self.ArrowSpace = self.__class__.ArrowSpace(service, rules, path + [("ArrowSpace", "")])
                                self.LineWidth = self.__class__.LineWidth(service, rules, path + [("LineWidth", "")])
                                self.MarkerSize = self.__class__.MarkerSize(service, rules, path + [("MarkerSize", "")])
                                self.Radius = self.__class__.Radius(service, rules, path + [("Radius", "")])
                                self.SphereLod = self.__class__.SphereLod(service, rules, path + [("SphereLod", "")])
                                self.SphereSize = self.__class__.SphereSize(service, rules, path + [("SphereSize", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                super().__init__(service, rules, path)

                            class Ribbon(PyMenu):
                                """
                                Singleton Ribbon.
                                """
                                def __init__(self, service, rules, path):
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    super().__init__(service, rules, path)

                                class Field(PyTextual):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class ScaleFactor(PyNumerical):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                            class ArrowScale(PyNumerical):
                                """
                                Parameter ArrowScale of value type float.
                                """
                                pass

                            class ArrowSpace(PyNumerical):
                                """
                                Parameter ArrowSpace of value type float.
                                """
                                pass

                            class LineWidth(PyNumerical):
                                """
                                Parameter LineWidth of value type float.
                                """
                                pass

                            class MarkerSize(PyNumerical):
                                """
                                Parameter MarkerSize of value type float.
                                """
                                pass

                            class Radius(PyNumerical):
                                """
                                Parameter Radius of value type float.
                                """
                                pass

                            class SphereLod(PyNumerical):
                                """
                                Parameter SphereLod of value type int.
                                """
                                pass

                            class SphereSize(PyNumerical):
                                """
                                Parameter SphereSize of value type float.
                                """
                                pass

                            class Style(PyTextual):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                        class Coarsen(PyNumerical):
                            """
                            Parameter Coarsen of value type int.
                            """
                            pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class OnZone(PyTextual):
                            """
                            Parameter OnZone of value type List[str].
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class PathlinesField(PyTextual):
                            """
                            Parameter PathlinesField of value type str.
                            """
                            pass

                        class Skip(PyNumerical):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class Step(PyNumerical):
                            """
                            Parameter Step of value type int.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class UID(PyTextual):
                            """
                            Parameter UID of value type str.
                            """
                            pass

                        class VelocityDomain(PyTextual):
                            """
                            Parameter VelocityDomain of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Pathlines:
                        return super().__getitem__(key)

                class Scene(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Scene(PyMenu):
                        """
                        Singleton _Scene.
                        """
                        def __init__(self, service, rules, path):
                            self.GraphicsObjects = self.__class__.GraphicsObjects(service, rules, path + [("GraphicsObjects", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class GraphicsObjects(PyDictionary):
                            """
                            Parameter GraphicsObjects of value type Dict[str, Any].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Scene:
                        return super().__getitem__(key)

                class Vector(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Vector(PyMenu):
                        """
                        Singleton _Vector.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Scale = self.__class__.Scale(service, rules, path + [("Scale", "")])
                            self.VectorOptions = self.__class__.VectorOptions(service, rules, path + [("VectorOptions", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.VectorField = self.__class__.VectorField(service, rules, path + [("VectorField", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyParameter):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                            class GlobalRange(PyParameter):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Scale(PyMenu):
                            """
                            Singleton Scale.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoScale = self.__class__.AutoScale(service, rules, path + [("AutoScale", "")])
                                self.Scale = self.__class__.Scale(service, rules, path + [("Scale", "")])
                                super().__init__(service, rules, path)

                            class AutoScale(PyParameter):
                                """
                                Parameter AutoScale of value type bool.
                                """
                                pass

                            class Scale(PyNumerical):
                                """
                                Parameter Scale of value type float.
                                """
                                pass

                        class VectorOptions(PyMenu):
                            """
                            Singleton VectorOptions.
                            """
                            def __init__(self, service, rules, path):
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.FixedLength = self.__class__.FixedLength(service, rules, path + [("FixedLength", "")])
                                self.HeadScale = self.__class__.HeadScale(service, rules, path + [("HeadScale", "")])
                                self.InPlane = self.__class__.InPlane(service, rules, path + [("InPlane", "")])
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class Color(PyTextual):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class FixedLength(PyParameter):
                                """
                                Parameter FixedLength of value type bool.
                                """
                                pass

                            class HeadScale(PyNumerical):
                                """
                                Parameter HeadScale of value type float.
                                """
                                pass

                            class InPlane(PyParameter):
                                """
                                Parameter InPlane of value type bool.
                                """
                                pass

                            class XComponent(PyParameter):
                                """
                                Parameter XComponent of value type bool.
                                """
                                pass

                            class YComponent(PyParameter):
                                """
                                Parameter YComponent of value type bool.
                                """
                                pass

                            class ZComponent(PyParameter):
                                """
                                Parameter ZComponent of value type bool.
                                """
                                pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Skip(PyNumerical):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class Style(PyTextual):
                            """
                            Parameter Style of value type str.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class VectorField(PyTextual):
                            """
                            Parameter VectorField of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            Command AddToViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class DisplayInViewport(PyCommand):
                            """
                            Command DisplayInViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            Command UpdateMinMax.


                            Returns
                            -------
                            None
                            """
                            pass

                    def __getitem__(self, key: str) -> _Vector:
                        return super().__getitem__(key)

                class XYPlot(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _XYPlot(PyMenu):
                        """
                        Singleton _XYPlot.
                        """
                        def __init__(self, service, rules, path):
                            self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                            self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                            self.DirectionVectorInternal = self.__class__.DirectionVectorInternal(service, rules, path + [("DirectionVectorInternal", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                            self.YAxisFunction = self.__class__.YAxisFunction(service, rules, path + [("YAxisFunction", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.UID = self.__class__.UID(service, rules, path + [("UID", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.ExportData = self.__class__.ExportData(service, rules, "ExportData", path)
                            self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class Axes(PyMenu):
                            """
                            Singleton Axes.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Singleton X.
                                """
                                def __init__(self, service, rules, path):
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

                                class MajorRules(PyMenu):
                                    """
                                    Singleton MajorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyTextual):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyNumerical):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class MinorRules(PyMenu):
                                    """
                                    Singleton MinorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyTextual):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyNumerical):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class NumberFormat(PyMenu):
                                    """
                                    Singleton NumberFormat.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                        super().__init__(service, rules, path)

                                    class Precision(PyNumerical):
                                        """
                                        Parameter Precision of value type int.
                                        """
                                        pass

                                    class Type(PyTextual):
                                        """
                                        Parameter Type of value type str.
                                        """
                                        pass

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        super().__init__(service, rules, path)

                                    class AutoRange(PyParameter):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class Log(PyParameter):
                                        """
                                        Parameter Log of value type bool.
                                        """
                                        pass

                                    class MajorRules(PyParameter):
                                        """
                                        Parameter MajorRules of value type bool.
                                        """
                                        pass

                                    class MinorRules(PyParameter):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                        self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                        super().__init__(service, rules, path)

                                    class Maximum(PyNumerical):
                                        """
                                        Parameter Maximum of value type float.
                                        """
                                        pass

                                    class Minimum(PyNumerical):
                                        """
                                        Parameter Minimum of value type float.
                                        """
                                        pass

                                class Label(PyTextual):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                            class Y(PyMenu):
                                """
                                Singleton Y.
                                """
                                def __init__(self, service, rules, path):
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

                                class MajorRules(PyMenu):
                                    """
                                    Singleton MajorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyTextual):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyNumerical):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class MinorRules(PyMenu):
                                    """
                                    Singleton MinorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyTextual):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyNumerical):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class NumberFormat(PyMenu):
                                    """
                                    Singleton NumberFormat.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                        super().__init__(service, rules, path)

                                    class Precision(PyNumerical):
                                        """
                                        Parameter Precision of value type int.
                                        """
                                        pass

                                    class Type(PyTextual):
                                        """
                                        Parameter Type of value type str.
                                        """
                                        pass

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        super().__init__(service, rules, path)

                                    class AutoRange(PyParameter):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class Log(PyParameter):
                                        """
                                        Parameter Log of value type bool.
                                        """
                                        pass

                                    class MajorRules(PyParameter):
                                        """
                                        Parameter MajorRules of value type bool.
                                        """
                                        pass

                                    class MinorRules(PyParameter):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                        self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                        super().__init__(service, rules, path)

                                    class Maximum(PyNumerical):
                                        """
                                        Parameter Maximum of value type float.
                                        """
                                        pass

                                    class Minimum(PyNumerical):
                                        """
                                        Parameter Minimum of value type float.
                                        """
                                        pass

                                class Label(PyTextual):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                        class Curves(PyMenu):
                            """
                            Singleton Curves.
                            """
                            def __init__(self, service, rules, path):
                                self.LineStyle = self.__class__.LineStyle(service, rules, path + [("LineStyle", "")])
                                self.MarkerStyle = self.__class__.MarkerStyle(service, rules, path + [("MarkerStyle", "")])
                                super().__init__(service, rules, path)

                            class LineStyle(PyMenu):
                                """
                                Singleton LineStyle.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Pattern = self.__class__.Pattern(service, rules, path + [("Pattern", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Pattern(PyTextual):
                                    """
                                    Parameter Pattern of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class MarkerStyle(PyMenu):
                                """
                                Singleton MarkerStyle.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                    self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Size(PyNumerical):
                                    """
                                    Parameter Size of value type float.
                                    """
                                    pass

                                class Symbol(PyTextual):
                                    """
                                    Parameter Symbol of value type str.
                                    """
                                    pass

                        class DirectionVectorInternal(PyMenu):
                            """
                            Singleton DirectionVectorInternal.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyNumerical):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyNumerical):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyNumerical):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyParameter):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                        class XAxisFunction(PyMenu):
                            """
                            Singleton XAxisFunction.
                            """
                            def __init__(self, service, rules, path):
                                self.DirectionVector = self.__class__.DirectionVector(service, rules, path + [("DirectionVector", "")])
                                self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                self.PositionOnCurrentAxis = self.__class__.PositionOnCurrentAxis(service, rules, path + [("PositionOnCurrentAxis", "")])
                                self.XAxisFunctionInternal = self.__class__.XAxisFunctionInternal(service, rules, path + [("XAxisFunctionInternal", "")])
                                super().__init__(service, rules, path)

                            class DirectionVector(PyMenu):
                                """
                                Singleton DirectionVector.
                                """
                                def __init__(self, service, rules, path):
                                    self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                    self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                    self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                    super().__init__(service, rules, path)

                                class XComponent(PyNumerical):
                                    """
                                    Parameter XComponent of value type float.
                                    """
                                    pass

                                class YComponent(PyNumerical):
                                    """
                                    Parameter YComponent of value type float.
                                    """
                                    pass

                                class ZComponent(PyNumerical):
                                    """
                                    Parameter ZComponent of value type float.
                                    """
                                    pass

                            class Field(PyTextual):
                                """
                                Parameter Field of value type str.
                                """
                                pass

                            class PositionOnCurrentAxis(PyParameter):
                                """
                                Parameter PositionOnCurrentAxis of value type bool.
                                """
                                pass

                            class XAxisFunctionInternal(PyTextual):
                                """
                                Parameter XAxisFunctionInternal of value type str.
                                """
                                pass

                        class YAxisFunction(PyMenu):
                            """
                            Singleton YAxisFunction.
                            """
                            def __init__(self, service, rules, path):
                                self.DirectionVector = self.__class__.DirectionVector(service, rules, path + [("DirectionVector", "")])
                                self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                self.PositionOnCurrentAxis = self.__class__.PositionOnCurrentAxis(service, rules, path + [("PositionOnCurrentAxis", "")])
                                self.YAxisFunctionInternal = self.__class__.YAxisFunctionInternal(service, rules, path + [("YAxisFunctionInternal", "")])
                                super().__init__(service, rules, path)

                            class DirectionVector(PyMenu):
                                """
                                Singleton DirectionVector.
                                """
                                def __init__(self, service, rules, path):
                                    self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                    self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                    self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                    super().__init__(service, rules, path)

                                class XComponent(PyNumerical):
                                    """
                                    Parameter XComponent of value type float.
                                    """
                                    pass

                                class YComponent(PyNumerical):
                                    """
                                    Parameter YComponent of value type float.
                                    """
                                    pass

                                class ZComponent(PyNumerical):
                                    """
                                    Parameter ZComponent of value type float.
                                    """
                                    pass

                            class Field(PyTextual):
                                """
                                Parameter Field of value type str.
                                """
                                pass

                            class PositionOnCurrentAxis(PyParameter):
                                """
                                Parameter PositionOnCurrentAxis of value type bool.
                                """
                                pass

                            class YAxisFunctionInternal(PyTextual):
                                """
                                Parameter YAxisFunctionInternal of value type str.
                                """
                                pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class UID(PyTextual):
                            """
                            Parameter UID of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class ExportData(PyCommand):
                            """
                            Command ExportData.

                            Parameters
                            ----------
                            FileName : str

                            Returns
                            -------
                            bool
                            """
                            pass

                        class Plot(PyCommand):
                            """
                            Command Plot.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : Dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _XYPlot:
                        return super().__getitem__(key)

                class CameraSettings(PyMenu):
                    """
                    Singleton CameraSettings.
                    """
                    def __init__(self, service, rules, path):
                        self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                        self.Target = self.__class__.Target(service, rules, path + [("Target", "")])
                        super().__init__(service, rules, path)

                    class Position(PyMenu):
                        """
                        Singleton Position.
                        """
                        def __init__(self, service, rules, path):
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            super().__init__(service, rules, path)

                        class X(PyNumerical):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyNumerical):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyNumerical):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                    class Target(PyMenu):
                        """
                        Singleton Target.
                        """
                        def __init__(self, service, rules, path):
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            super().__init__(service, rules, path)

                        class X(PyNumerical):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyNumerical):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyNumerical):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                class GridColors(PyMenu):
                    """
                    Singleton GridColors.
                    """
                    def __init__(self, service, rules, path):
                        self.ColorGridAxis = self.__class__.ColorGridAxis(service, rules, path + [("ColorGridAxis", "")])
                        self.ColorGridFar = self.__class__.ColorGridFar(service, rules, path + [("ColorGridFar", "")])
                        self.ColorGridFreeSurface = self.__class__.ColorGridFreeSurface(service, rules, path + [("ColorGridFreeSurface", "")])
                        self.ColorGridInlet = self.__class__.ColorGridInlet(service, rules, path + [("ColorGridInlet", "")])
                        self.ColorGridInterior = self.__class__.ColorGridInterior(service, rules, path + [("ColorGridInterior", "")])
                        self.ColorGridInternal = self.__class__.ColorGridInternal(service, rules, path + [("ColorGridInternal", "")])
                        self.ColorGridOutlet = self.__class__.ColorGridOutlet(service, rules, path + [("ColorGridOutlet", "")])
                        self.ColorGridOverset = self.__class__.ColorGridOverset(service, rules, path + [("ColorGridOverset", "")])
                        self.ColorGridPeriodic = self.__class__.ColorGridPeriodic(service, rules, path + [("ColorGridPeriodic", "")])
                        self.ColorGridRansLesInterface = self.__class__.ColorGridRansLesInterface(service, rules, path + [("ColorGridRansLesInterface", "")])
                        self.ColorGridSymmetry = self.__class__.ColorGridSymmetry(service, rules, path + [("ColorGridSymmetry", "")])
                        self.ColorGridTraction = self.__class__.ColorGridTraction(service, rules, path + [("ColorGridTraction", "")])
                        self.ColorGridWall = self.__class__.ColorGridWall(service, rules, path + [("ColorGridWall", "")])
                        self.ColorInterface = self.__class__.ColorInterface(service, rules, path + [("ColorInterface", "")])
                        self.ColorSurface = self.__class__.ColorSurface(service, rules, path + [("ColorSurface", "")])
                        super().__init__(service, rules, path)

                    class ColorGridAxis(PyTextual):
                        """
                        Parameter ColorGridAxis of value type str.
                        """
                        pass

                    class ColorGridFar(PyTextual):
                        """
                        Parameter ColorGridFar of value type str.
                        """
                        pass

                    class ColorGridFreeSurface(PyTextual):
                        """
                        Parameter ColorGridFreeSurface of value type str.
                        """
                        pass

                    class ColorGridInlet(PyTextual):
                        """
                        Parameter ColorGridInlet of value type str.
                        """
                        pass

                    class ColorGridInterior(PyTextual):
                        """
                        Parameter ColorGridInterior of value type str.
                        """
                        pass

                    class ColorGridInternal(PyTextual):
                        """
                        Parameter ColorGridInternal of value type str.
                        """
                        pass

                    class ColorGridOutlet(PyTextual):
                        """
                        Parameter ColorGridOutlet of value type str.
                        """
                        pass

                    class ColorGridOverset(PyTextual):
                        """
                        Parameter ColorGridOverset of value type str.
                        """
                        pass

                    class ColorGridPeriodic(PyTextual):
                        """
                        Parameter ColorGridPeriodic of value type str.
                        """
                        pass

                    class ColorGridRansLesInterface(PyTextual):
                        """
                        Parameter ColorGridRansLesInterface of value type str.
                        """
                        pass

                    class ColorGridSymmetry(PyTextual):
                        """
                        Parameter ColorGridSymmetry of value type str.
                        """
                        pass

                    class ColorGridTraction(PyTextual):
                        """
                        Parameter ColorGridTraction of value type str.
                        """
                        pass

                    class ColorGridWall(PyTextual):
                        """
                        Parameter ColorGridWall of value type str.
                        """
                        pass

                    class ColorInterface(PyTextual):
                        """
                        Parameter ColorInterface of value type str.
                        """
                        pass

                    class ColorSurface(PyTextual):
                        """
                        Parameter ColorSurface of value type str.
                        """
                        pass

                class GraphicsCreationCount(PyNumerical):
                    """
                    Parameter GraphicsCreationCount of value type int.
                    """
                    pass

                class SaveImage(PyCommand):
                    """
                    Command SaveImage.

                    Parameters
                    ----------
                    FileName : str
                    Format : str
                    FileType : str
                    Coloring : str
                    Orientation : str
                    UseWhiteBackground : bool
                    Resolution : Dict[str, Any]

                    Returns
                    -------
                    bool
                    """
                    pass

            class Plots(PyMenu):
                """
                Singleton Plots.
                """
                def __init__(self, service, rules, path):
                    self.PlotFromFile = self.__class__.PlotFromFile(service, rules, path + [("PlotFromFile", "")])
                    super().__init__(service, rules, path)

                class PlotFromFile(PyMenu):
                    """
                    Singleton PlotFromFile.
                    """
                    def __init__(self, service, rules, path):
                        self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                        self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                        self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                        self.YAxisFunction = self.__class__.YAxisFunction(service, rules, path + [("YAxisFunction", "")])
                        self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                        self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                        super().__init__(service, rules, path)

                    class Axes(PyMenu):
                        """
                        Singleton Axes.
                        """
                        def __init__(self, service, rules, path):
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            super().__init__(service, rules, path)

                        class X(PyMenu):
                            """
                            Singleton X.
                            """
                            def __init__(self, service, rules, path):
                                self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                super().__init__(service, rules, path)

                            class MajorRules(PyMenu):
                                """
                                Singleton MajorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class MinorRules(PyMenu):
                                """
                                Singleton MinorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class NumberFormat(PyMenu):
                                """
                                Singleton NumberFormat.
                                """
                                def __init__(self, service, rules, path):
                                    self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                    self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                    super().__init__(service, rules, path)

                                class Precision(PyNumerical):
                                    """
                                    Parameter Precision of value type int.
                                    """
                                    pass

                                class Type(PyTextual):
                                    """
                                    Parameter Type of value type str.
                                    """
                                    pass

                            class Options(PyMenu):
                                """
                                Singleton Options.
                                """
                                def __init__(self, service, rules, path):
                                    self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                    self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    super().__init__(service, rules, path)

                                class AutoRange(PyParameter):
                                    """
                                    Parameter AutoRange of value type bool.
                                    """
                                    pass

                                class Log(PyParameter):
                                    """
                                    Parameter Log of value type bool.
                                    """
                                    pass

                                class MajorRules(PyParameter):
                                    """
                                    Parameter MajorRules of value type bool.
                                    """
                                    pass

                                class MinorRules(PyParameter):
                                    """
                                    Parameter MinorRules of value type bool.
                                    """
                                    pass

                            class Range(PyMenu):
                                """
                                Singleton Range.
                                """
                                def __init__(self, service, rules, path):
                                    self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                    self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                    super().__init__(service, rules, path)

                                class Maximum(PyNumerical):
                                    """
                                    Parameter Maximum of value type float.
                                    """
                                    pass

                                class Minimum(PyNumerical):
                                    """
                                    Parameter Minimum of value type float.
                                    """
                                    pass

                            class Label(PyTextual):
                                """
                                Parameter Label of value type str.
                                """
                                pass

                        class Y(PyMenu):
                            """
                            Singleton Y.
                            """
                            def __init__(self, service, rules, path):
                                self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                super().__init__(service, rules, path)

                            class MajorRules(PyMenu):
                                """
                                Singleton MajorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class MinorRules(PyMenu):
                                """
                                Singleton MinorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class NumberFormat(PyMenu):
                                """
                                Singleton NumberFormat.
                                """
                                def __init__(self, service, rules, path):
                                    self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                    self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                    super().__init__(service, rules, path)

                                class Precision(PyNumerical):
                                    """
                                    Parameter Precision of value type int.
                                    """
                                    pass

                                class Type(PyTextual):
                                    """
                                    Parameter Type of value type str.
                                    """
                                    pass

                            class Options(PyMenu):
                                """
                                Singleton Options.
                                """
                                def __init__(self, service, rules, path):
                                    self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                    self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    super().__init__(service, rules, path)

                                class AutoRange(PyParameter):
                                    """
                                    Parameter AutoRange of value type bool.
                                    """
                                    pass

                                class Log(PyParameter):
                                    """
                                    Parameter Log of value type bool.
                                    """
                                    pass

                                class MajorRules(PyParameter):
                                    """
                                    Parameter MajorRules of value type bool.
                                    """
                                    pass

                                class MinorRules(PyParameter):
                                    """
                                    Parameter MinorRules of value type bool.
                                    """
                                    pass

                            class Range(PyMenu):
                                """
                                Singleton Range.
                                """
                                def __init__(self, service, rules, path):
                                    self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                    self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                    super().__init__(service, rules, path)

                                class Maximum(PyNumerical):
                                    """
                                    Parameter Maximum of value type float.
                                    """
                                    pass

                                class Minimum(PyNumerical):
                                    """
                                    Parameter Minimum of value type float.
                                    """
                                    pass

                            class Label(PyTextual):
                                """
                                Parameter Label of value type str.
                                """
                                pass

                    class Curves(PyMenu):
                        """
                        Singleton Curves.
                        """
                        def __init__(self, service, rules, path):
                            self.LineStyle = self.__class__.LineStyle(service, rules, path + [("LineStyle", "")])
                            self.MarkerStyle = self.__class__.MarkerStyle(service, rules, path + [("MarkerStyle", "")])
                            super().__init__(service, rules, path)

                        class LineStyle(PyMenu):
                            """
                            Singleton LineStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.Pattern = self.__class__.Pattern(service, rules, path + [("Pattern", "")])
                                self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                super().__init__(service, rules, path)

                            class Color(PyTextual):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class Pattern(PyTextual):
                                """
                                Parameter Pattern of value type str.
                                """
                                pass

                            class Weight(PyNumerical):
                                """
                                Parameter Weight of value type float.
                                """
                                pass

                        class MarkerStyle(PyMenu):
                            """
                            Singleton MarkerStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                super().__init__(service, rules, path)

                            class Color(PyTextual):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type float.
                                """
                                pass

                            class Symbol(PyTextual):
                                """
                                Parameter Symbol of value type str.
                                """
                                pass

                    class XAxisFunction(PyMenu):
                        """
                        Singleton XAxisFunction.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            super().__init__(service, rules, path)

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                    class YAxisFunction(PyMenu):
                        """
                        Singleton YAxisFunction.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            super().__init__(service, rules, path)

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                    class Filename(PyTextual):
                        """
                        Parameter Filename of value type str.
                        """
                        pass

                    class Plot(PyCommand):
                        """
                        Command Plot.


                        Returns
                        -------
                        None
                        """
                        pass

            class ResultsExternalInfo(PyMenu):
                """
                Singleton ResultsExternalInfo.
                """
                def __init__(self, service, rules, path):
                    super().__init__(service, rules, path)

            class CreateCellZoneSurfaces(PyCommand):
                """
                Command CreateCellZoneSurfaces.


                Returns
                -------
                List[int]
                """
                pass

            class CreateMultipleIsosurfaces(PyCommand):
                """
                Command CreateMultipleIsosurfaces.

                Parameters
                ----------
                NameFormat : str
                Field : str
                SpecifyBy : str
                FirstValue : float
                Increment : float
                Steps : int
                LastValue : float

                Returns
                -------
                None
                """
                pass

            class CreateMultiplePlanes(PyCommand):
                """
                Command CreateMultiplePlanes.

                Parameters
                ----------
                NameFormat : str
                NumberOfPlanes : int
                Option : str
                NormalSpecification : str
                NormalVector : Dict[str, Any]
                StartPoint : Dict[str, Any]
                EndPoint : Dict[str, Any]
                Spacing : float

                Returns
                -------
                None
                """
                pass

            class GetFieldMinMax(PyCommand):
                """
                Command GetFieldMinMax.

                Parameters
                ----------
                Field : str
                Surfaces : List[str]

                Returns
                -------
                List[float]
                """
                pass

            class GetXYData(PyCommand):
                """
                Command GetXYData.

                Parameters
                ----------
                Surfaces : List[str]
                Fields : List[str]

                Returns
                -------
                None
                """
                pass

        class ResultsInfo(PyMenu):
            """
            Singleton ResultsInfo.
            """
            def __init__(self, service, rules, path):
                self.DPMInjections = self.__class__.DPMInjections(service, rules, path + [("DPMInjections", "")])
                self.DPMParticleVectorFields = self.__class__.DPMParticleVectorFields(service, rules, path + [("DPMParticleVectorFields", "")])
                self.Fields = self.__class__.Fields(service, rules, path + [("Fields", "")])
                self.ParticleTracksFields = self.__class__.ParticleTracksFields(service, rules, path + [("ParticleTracksFields", "")])
                self.ParticleVariables = self.__class__.ParticleVariables(service, rules, path + [("ParticleVariables", "")])
                self.PathlinesFields = self.__class__.PathlinesFields(service, rules, path + [("PathlinesFields", "")])
                self.VectorFields = self.__class__.VectorFields(service, rules, path + [("VectorFields", "")])
                super().__init__(service, rules, path)

            class DPMInjections(PyNamedObjectContainer):
                """
                .
                """
                class _DPMInjections(PyMenu):
                    """
                    Singleton _DPMInjections.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _DPMInjections:
                    return super().__getitem__(key)

            class DPMParticleVectorFields(PyNamedObjectContainer):
                """
                .
                """
                class _DPMParticleVectorFields(PyMenu):
                    """
                    Singleton _DPMParticleVectorFields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _DPMParticleVectorFields:
                    return super().__getitem__(key)

            class Fields(PyNamedObjectContainer):
                """
                .
                """
                class _Fields(PyMenu):
                    """
                    Singleton _Fields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Rank = self.__class__.Rank(service, rules, path + [("Rank", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self.UnitQuantity = self.__class__.UnitQuantity(service, rules, path + [("UnitQuantity", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Domain(PyTextual):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Rank(PyNumerical):
                        """
                        Parameter Rank of value type int.
                        """
                        pass

                    class Section(PyTextual):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class UnitQuantity(PyTextual):
                        """
                        Parameter UnitQuantity of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _Fields:
                    return super().__getitem__(key)

            class ParticleTracksFields(PyNamedObjectContainer):
                """
                .
                """
                class _ParticleTracksFields(PyMenu):
                    """
                    Singleton _ParticleTracksFields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Domain(PyTextual):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Section(PyTextual):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _ParticleTracksFields:
                    return super().__getitem__(key)

            class ParticleVariables(PyNamedObjectContainer):
                """
                .
                """
                class _ParticleVariables(PyMenu):
                    """
                    Singleton _ParticleVariables.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Domain(PyTextual):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Section(PyTextual):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _ParticleVariables:
                    return super().__getitem__(key)

            class PathlinesFields(PyNamedObjectContainer):
                """
                .
                """
                class _PathlinesFields(PyMenu):
                    """
                    Singleton _PathlinesFields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Rank = self.__class__.Rank(service, rules, path + [("Rank", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Domain(PyTextual):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Rank(PyNumerical):
                        """
                        Parameter Rank of value type int.
                        """
                        pass

                    class Section(PyTextual):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _PathlinesFields:
                    return super().__getitem__(key)

            class VectorFields(PyNamedObjectContainer):
                """
                .
                """
                class _VectorFields(PyMenu):
                    """
                    Singleton _VectorFields.
                    """
                    def __init__(self, service, rules, path):
                        self.IsCustomVector = self.__class__.IsCustomVector(service, rules, path + [("IsCustomVector", "")])
                        self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                        self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                        self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class IsCustomVector(PyParameter):
                        """
                        Parameter IsCustomVector of value type bool.
                        """
                        pass

                    class XComponent(PyTextual):
                        """
                        Parameter XComponent of value type str.
                        """
                        pass

                    class YComponent(PyTextual):
                        """
                        Parameter YComponent of value type str.
                        """
                        pass

                    class ZComponent(PyTextual):
                        """
                        Parameter ZComponent of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _VectorFields:
                    return super().__getitem__(key)

        class Setup(PyMenu):
            """
            Singleton Setup.
            """
            def __init__(self, service, rules, path):
                self.Boundary = self.__class__.Boundary(service, rules, path + [("Boundary", "")])
                self.CellZone = self.__class__.CellZone(service, rules, path + [("CellZone", "")])
                self.Material = self.__class__.Material(service, rules, path + [("Material", "")])
                self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                super().__init__(service, rules, path)

            class Boundary(PyNamedObjectContainer):
                """
                .
                """
                class _Boundary(PyMenu):
                    """
                    Singleton _Boundary.
                    """
                    def __init__(self, service, rules, path):
                        self.Flow = self.__class__.Flow(service, rules, path + [("Flow", "")])
                        self.Thermal = self.__class__.Thermal(service, rules, path + [("Thermal", "")])
                        self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                        self.BoundaryId = self.__class__.BoundaryId(service, rules, path + [("BoundaryId", "")])
                        self.BoundaryType = self.__class__.BoundaryType(service, rules, path + [("BoundaryType", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class Flow(PyMenu):
                        """
                        Singleton Flow.
                        """
                        def __init__(self, service, rules, path):
                            self.Direction = self.__class__.Direction(service, rules, path + [("Direction", "")])
                            self.FlowDirection = self.__class__.FlowDirection(service, rules, path + [("FlowDirection", "")])
                            self.RotationAxisDirection = self.__class__.RotationAxisDirection(service, rules, path + [("RotationAxisDirection", "")])
                            self.RotationAxisOrigin = self.__class__.RotationAxisOrigin(service, rules, path + [("RotationAxisOrigin", "")])
                            self.TranslationalDirection = self.__class__.TranslationalDirection(service, rules, path + [("TranslationalDirection", "")])
                            self.TranslationalVelocityComponents = self.__class__.TranslationalVelocityComponents(service, rules, path + [("TranslationalVelocityComponents", "")])
                            self.VelocityCartesianComponents = self.__class__.VelocityCartesianComponents(service, rules, path + [("VelocityCartesianComponents", "")])
                            self.AverageMassFlux = self.__class__.AverageMassFlux(service, rules, path + [("AverageMassFlux", "")])
                            self.DirectionSpecificationMethod = self.__class__.DirectionSpecificationMethod(service, rules, path + [("DirectionSpecificationMethod", "")])
                            self.GaugePressure = self.__class__.GaugePressure(service, rules, path + [("GaugePressure", "")])
                            self.GaugeTotalPressure = self.__class__.GaugeTotalPressure(service, rules, path + [("GaugeTotalPressure", "")])
                            self.IsMotionBC = self.__class__.IsMotionBC(service, rules, path + [("IsMotionBC", "")])
                            self.IsRotating = self.__class__.IsRotating(service, rules, path + [("IsRotating", "")])
                            self.MachNumber = self.__class__.MachNumber(service, rules, path + [("MachNumber", "")])
                            self.MassFlowRate = self.__class__.MassFlowRate(service, rules, path + [("MassFlowRate", "")])
                            self.MassFlowSpecificationMethod = self.__class__.MassFlowSpecificationMethod(service, rules, path + [("MassFlowSpecificationMethod", "")])
                            self.MassFlux = self.__class__.MassFlux(service, rules, path + [("MassFlux", "")])
                            self.RotationalSpeed = self.__class__.RotationalSpeed(service, rules, path + [("RotationalSpeed", "")])
                            self.SupersonicOrInitialGaugePressure = self.__class__.SupersonicOrInitialGaugePressure(service, rules, path + [("SupersonicOrInitialGaugePressure", "")])
                            self.TranslationalVelocityMagnitude = self.__class__.TranslationalVelocityMagnitude(service, rules, path + [("TranslationalVelocityMagnitude", "")])
                            self.TranslationalVelocitySpecification = self.__class__.TranslationalVelocitySpecification(service, rules, path + [("TranslationalVelocitySpecification", "")])
                            self.VelocityMagnitude = self.__class__.VelocityMagnitude(service, rules, path + [("VelocityMagnitude", "")])
                            self.VelocitySpecification = self.__class__.VelocitySpecification(service, rules, path + [("VelocitySpecification", "")])
                            self.WallVelocitySpecification = self.__class__.WallVelocitySpecification(service, rules, path + [("WallVelocitySpecification", "")])
                            super().__init__(service, rules, path)

                        class Direction(PyMenu):
                            """
                            Singleton Direction.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class FlowDirection(PyMenu):
                            """
                            Singleton FlowDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class RotationAxisDirection(PyMenu):
                            """
                            Singleton RotationAxisDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class RotationAxisOrigin(PyMenu):
                            """
                            Singleton RotationAxisOrigin.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class TranslationalDirection(PyMenu):
                            """
                            Singleton TranslationalDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class TranslationalVelocityComponents(PyMenu):
                            """
                            Singleton TranslationalVelocityComponents.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class VelocityCartesianComponents(PyMenu):
                            """
                            Singleton VelocityCartesianComponents.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class AverageMassFlux(PyNumerical):
                            """
                            Parameter AverageMassFlux of value type float.
                            """
                            pass

                        class DirectionSpecificationMethod(PyTextual):
                            """
                            Parameter DirectionSpecificationMethod of value type str.
                            """
                            pass

                        class GaugePressure(PyNumerical):
                            """
                            Parameter GaugePressure of value type float.
                            """
                            pass

                        class GaugeTotalPressure(PyNumerical):
                            """
                            Parameter GaugeTotalPressure of value type float.
                            """
                            pass

                        class IsMotionBC(PyNumerical):
                            """
                            Parameter IsMotionBC of value type int.
                            """
                            pass

                        class IsRotating(PyParameter):
                            """
                            Parameter IsRotating of value type bool.
                            """
                            pass

                        class MachNumber(PyNumerical):
                            """
                            Parameter MachNumber of value type float.
                            """
                            pass

                        class MassFlowRate(PyNumerical):
                            """
                            Parameter MassFlowRate of value type float.
                            """
                            pass

                        class MassFlowSpecificationMethod(PyTextual):
                            """
                            Parameter MassFlowSpecificationMethod of value type str.
                            """
                            pass

                        class MassFlux(PyNumerical):
                            """
                            Parameter MassFlux of value type float.
                            """
                            pass

                        class RotationalSpeed(PyNumerical):
                            """
                            Parameter RotationalSpeed of value type float.
                            """
                            pass

                        class SupersonicOrInitialGaugePressure(PyNumerical):
                            """
                            Parameter SupersonicOrInitialGaugePressure of value type float.
                            """
                            pass

                        class TranslationalVelocityMagnitude(PyNumerical):
                            """
                            Parameter TranslationalVelocityMagnitude of value type float.
                            """
                            pass

                        class TranslationalVelocitySpecification(PyTextual):
                            """
                            Parameter TranslationalVelocitySpecification of value type str.
                            """
                            pass

                        class VelocityMagnitude(PyNumerical):
                            """
                            Parameter VelocityMagnitude of value type float.
                            """
                            pass

                        class VelocitySpecification(PyTextual):
                            """
                            Parameter VelocitySpecification of value type str.
                            """
                            pass

                        class WallVelocitySpecification(PyTextual):
                            """
                            Parameter WallVelocitySpecification of value type str.
                            """
                            pass

                    class Thermal(PyMenu):
                        """
                        Singleton Thermal.
                        """
                        def __init__(self, service, rules, path):
                            self.ExternalEmissivity = self.__class__.ExternalEmissivity(service, rules, path + [("ExternalEmissivity", "")])
                            self.ExternalRadiationTemperature = self.__class__.ExternalRadiationTemperature(service, rules, path + [("ExternalRadiationTemperature", "")])
                            self.FreeStreamTemperature = self.__class__.FreeStreamTemperature(service, rules, path + [("FreeStreamTemperature", "")])
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.HeatGenerationRate = self.__class__.HeatGenerationRate(service, rules, path + [("HeatGenerationRate", "")])
                            self.HeatTransferCoefficient = self.__class__.HeatTransferCoefficient(service, rules, path + [("HeatTransferCoefficient", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.ThermalConditions = self.__class__.ThermalConditions(service, rules, path + [("ThermalConditions", "")])
                            self.TotalTemperature = self.__class__.TotalTemperature(service, rules, path + [("TotalTemperature", "")])
                            self.WallThickness = self.__class__.WallThickness(service, rules, path + [("WallThickness", "")])
                            super().__init__(service, rules, path)

                        class ExternalEmissivity(PyNumerical):
                            """
                            Parameter ExternalEmissivity of value type float.
                            """
                            pass

                        class ExternalRadiationTemperature(PyNumerical):
                            """
                            Parameter ExternalRadiationTemperature of value type float.
                            """
                            pass

                        class FreeStreamTemperature(PyNumerical):
                            """
                            Parameter FreeStreamTemperature of value type float.
                            """
                            pass

                        class HeatFlux(PyNumerical):
                            """
                            Parameter HeatFlux of value type float.
                            """
                            pass

                        class HeatGenerationRate(PyNumerical):
                            """
                            Parameter HeatGenerationRate of value type float.
                            """
                            pass

                        class HeatTransferCoefficient(PyNumerical):
                            """
                            Parameter HeatTransferCoefficient of value type float.
                            """
                            pass

                        class Temperature(PyNumerical):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class ThermalConditions(PyTextual):
                            """
                            Parameter ThermalConditions of value type str.
                            """
                            pass

                        class TotalTemperature(PyNumerical):
                            """
                            Parameter TotalTemperature of value type float.
                            """
                            pass

                        class WallThickness(PyNumerical):
                            """
                            Parameter WallThickness of value type float.
                            """
                            pass

                    class Turbulence(PyMenu):
                        """
                        Singleton Turbulence.
                        """
                        def __init__(self, service, rules, path):
                            self.HydraulicDiameter = self.__class__.HydraulicDiameter(service, rules, path + [("HydraulicDiameter", "")])
                            self.SpecificationMethod = self.__class__.SpecificationMethod(service, rules, path + [("SpecificationMethod", "")])
                            self.TurbulentIntensity = self.__class__.TurbulentIntensity(service, rules, path + [("TurbulentIntensity", "")])
                            self.TurbulentLengthScale = self.__class__.TurbulentLengthScale(service, rules, path + [("TurbulentLengthScale", "")])
                            self.TurbulentViscosityRatio = self.__class__.TurbulentViscosityRatio(service, rules, path + [("TurbulentViscosityRatio", "")])
                            super().__init__(service, rules, path)

                        class HydraulicDiameter(PyNumerical):
                            """
                            Parameter HydraulicDiameter of value type float.
                            """
                            pass

                        class SpecificationMethod(PyTextual):
                            """
                            Parameter SpecificationMethod of value type str.
                            """
                            pass

                        class TurbulentIntensity(PyNumerical):
                            """
                            Parameter TurbulentIntensity of value type float.
                            """
                            pass

                        class TurbulentLengthScale(PyNumerical):
                            """
                            Parameter TurbulentLengthScale of value type float.
                            """
                            pass

                        class TurbulentViscosityRatio(PyNumerical):
                            """
                            Parameter TurbulentViscosityRatio of value type float.
                            """
                            pass

                    class BoundaryId(PyNumerical):
                        """
                        Parameter BoundaryId of value type int.
                        """
                        pass

                    class BoundaryType(PyTextual):
                        """
                        Parameter BoundaryType of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _Boundary:
                    return super().__getitem__(key)

            class CellZone(PyNamedObjectContainer):
                """
                .
                """
                class _CellZone(PyMenu):
                    """
                    Singleton _CellZone.
                    """
                    def __init__(self, service, rules, path):
                        self.CellZoneId = self.__class__.CellZoneId(service, rules, path + [("CellZoneId", "")])
                        self.Material = self.__class__.Material(service, rules, path + [("Material", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class CellZoneId(PyNumerical):
                        """
                        Parameter CellZoneId of value type int.
                        """
                        pass

                    class Material(PyTextual):
                        """
                        Parameter Material of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _CellZone:
                    return super().__getitem__(key)

            class Material(PyNamedObjectContainer):
                """
                .
                """
                class _Material(PyMenu):
                    """
                    Singleton _Material.
                    """
                    def __init__(self, service, rules, path):
                        self.CpSpecificHeat = self.__class__.CpSpecificHeat(service, rules, path + [("CpSpecificHeat", "")])
                        self.Density = self.__class__.Density(service, rules, path + [("Density", "")])
                        self.MolecularWeight = self.__class__.MolecularWeight(service, rules, path + [("MolecularWeight", "")])
                        self.ThermalConductivity = self.__class__.ThermalConductivity(service, rules, path + [("ThermalConductivity", "")])
                        self.ThermalExpansionCoefficient = self.__class__.ThermalExpansionCoefficient(service, rules, path + [("ThermalExpansionCoefficient", "")])
                        self.Viscosity = self.__class__.Viscosity(service, rules, path + [("Viscosity", "")])
                        self.FluentName = self.__class__.FluentName(service, rules, path + [("FluentName", "")])
                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.LoadFromDatabase = self.__class__.LoadFromDatabase(service, rules, "LoadFromDatabase", path)
                        super().__init__(service, rules, path)

                    class CpSpecificHeat(PyMenu):
                        """
                        Singleton CpSpecificHeat.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class Density(PyMenu):
                        """
                        Singleton Density.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class MolecularWeight(PyMenu):
                        """
                        Singleton MolecularWeight.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class ThermalConductivity(PyMenu):
                        """
                        Singleton ThermalConductivity.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class ThermalExpansionCoefficient(PyMenu):
                        """
                        Singleton ThermalExpansionCoefficient.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class Viscosity(PyMenu):
                        """
                        Singleton Viscosity.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class FluentName(PyTextual):
                        """
                        Parameter FluentName of value type str.
                        """
                        pass

                    class Type(PyTextual):
                        """
                        Parameter Type of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class LoadFromDatabase(PyCommand):
                        """
                        Command LoadFromDatabase.

                        Parameters
                        ----------
                        MaterialName : str

                        Returns
                        -------
                        None
                        """
                        pass

                def __getitem__(self, key: str) -> _Material:
                    return super().__getitem__(key)

            class Beta(PyParameter):
                """
                Parameter Beta of value type bool.
                """
                pass

        class Solution(PyMenu):
            """
            Singleton Solution.
            """
            def __init__(self, service, rules, path):
                self.Calculation = self.__class__.Calculation(service, rules, path + [("Calculation", "")])
                self.CalculationActivities = self.__class__.CalculationActivities(service, rules, path + [("CalculationActivities", "")])
                self.Controls = self.__class__.Controls(service, rules, path + [("Controls", "")])
                self.Methods = self.__class__.Methods(service, rules, path + [("Methods", "")])
                self.Monitors = self.__class__.Monitors(service, rules, path + [("Monitors", "")])
                self.State = self.__class__.State(service, rules, path + [("State", "")])
                super().__init__(service, rules, path)

            class Calculation(PyMenu):
                """
                Singleton Calculation.
                """
                def __init__(self, service, rules, path):
                    self.AnalysisType = self.__class__.AnalysisType(service, rules, path + [("AnalysisType", "")])
                    self.MaxIterationsPerTimeStep = self.__class__.MaxIterationsPerTimeStep(service, rules, path + [("MaxIterationsPerTimeStep", "")])
                    self.NumberOfIterations = self.__class__.NumberOfIterations(service, rules, path + [("NumberOfIterations", "")])
                    self.NumberOfTimeSteps = self.__class__.NumberOfTimeSteps(service, rules, path + [("NumberOfTimeSteps", "")])
                    self.TimeStepSize = self.__class__.TimeStepSize(service, rules, path + [("TimeStepSize", "")])
                    self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                    self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                    self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                    self.Pause = self.__class__.Pause(service, rules, "Pause", path)
                    self.Resume = self.__class__.Resume(service, rules, "Resume", path)
                    super().__init__(service, rules, path)

                class AnalysisType(PyTextual):
                    """
                    Parameter AnalysisType of value type str.
                    """
                    pass

                class MaxIterationsPerTimeStep(PyNumerical):
                    """
                    Parameter MaxIterationsPerTimeStep of value type int.
                    """
                    pass

                class NumberOfIterations(PyNumerical):
                    """
                    Parameter NumberOfIterations of value type int.
                    """
                    pass

                class NumberOfTimeSteps(PyNumerical):
                    """
                    Parameter NumberOfTimeSteps of value type int.
                    """
                    pass

                class TimeStepSize(PyNumerical):
                    """
                    Parameter TimeStepSize of value type float.
                    """
                    pass

                class Calculate(PyCommand):
                    """
                    Command Calculate.


                    Returns
                    -------
                    bool
                    """
                    pass

                class Initialize(PyCommand):
                    """
                    Command Initialize.


                    Returns
                    -------
                    bool
                    """
                    pass

                class Interrupt(PyCommand):
                    """
                    Command Interrupt.


                    Returns
                    -------
                    bool
                    """
                    pass

                class Pause(PyCommand):
                    """
                    Command Pause.


                    Returns
                    -------
                    bool
                    """
                    pass

                class Resume(PyCommand):
                    """
                    Command Resume.


                    Returns
                    -------
                    bool
                    """
                    pass

            class CalculationActivities(PyMenu):
                """
                Singleton CalculationActivities.
                """
                def __init__(self, service, rules, path):
                    self.SolutionAnimations = self.__class__.SolutionAnimations(service, rules, path + [("SolutionAnimations", "")])
                    super().__init__(service, rules, path)

                class SolutionAnimations(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _SolutionAnimations(PyMenu):
                        """
                        Singleton _SolutionAnimations.
                        """
                        def __init__(self, service, rules, path):
                            self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
                            self.IntegerIndex = self.__class__.IntegerIndex(service, rules, path + [("IntegerIndex", "")])
                            self.Projection = self.__class__.Projection(service, rules, path + [("Projection", "")])
                            self.RealIndex = self.__class__.RealIndex(service, rules, path + [("RealIndex", "")])
                            self.RecordAfter = self.__class__.RecordAfter(service, rules, path + [("RecordAfter", "")])
                            self.Sequence = self.__class__.Sequence(service, rules, path + [("Sequence", "")])
                            self.StorageDirectory = self.__class__.StorageDirectory(service, rules, path + [("StorageDirectory", "")])
                            self.StorageType = self.__class__.StorageType(service, rules, path + [("StorageType", "")])
                            self.View = self.__class__.View(service, rules, path + [("View", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                            self.Delete = self.__class__.Delete(service, rules, "Delete", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.PlayBack = self.__class__.PlayBack(service, rules, "PlayBack", path)
                            super().__init__(service, rules, path)

                        class Graphics(PyTextual):
                            """
                            Parameter Graphics of value type str.
                            """
                            pass

                        class IntegerIndex(PyNumerical):
                            """
                            Parameter IntegerIndex of value type int.
                            """
                            pass

                        class Projection(PyTextual):
                            """
                            Parameter Projection of value type str.
                            """
                            pass

                        class RealIndex(PyNumerical):
                            """
                            Parameter RealIndex of value type float.
                            """
                            pass

                        class RecordAfter(PyTextual):
                            """
                            Parameter RecordAfter of value type str.
                            """
                            pass

                        class Sequence(PyNumerical):
                            """
                            Parameter Sequence of value type int.
                            """
                            pass

                        class StorageDirectory(PyTextual):
                            """
                            Parameter StorageDirectory of value type str.
                            """
                            pass

                        class StorageType(PyTextual):
                            """
                            Parameter StorageType of value type str.
                            """
                            pass

                        class View(PyTextual):
                            """
                            Parameter View of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Apply(PyCommand):
                            """
                            Command Apply.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Delete(PyCommand):
                            """
                            Command Delete.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            pass

                        class PlayBack(PyCommand):
                            """
                            Command PlayBack.


                            Returns
                            -------
                            bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _SolutionAnimations:
                        return super().__getitem__(key)

            class Controls(PyMenu):
                """
                Singleton Controls.
                """
                def __init__(self, service, rules, path):
                    self.UnderRelaxationFactors = self.__class__.UnderRelaxationFactors(service, rules, path + [("UnderRelaxationFactors", "")])
                    self.CourantNumber = self.__class__.CourantNumber(service, rules, path + [("CourantNumber", "")])
                    super().__init__(service, rules, path)

                class UnderRelaxationFactors(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _UnderRelaxationFactors(PyMenu):
                        """
                        Singleton _UnderRelaxationFactors.
                        """
                        def __init__(self, service, rules, path):
                            self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                            self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            super().__init__(service, rules, path)

                        class DomainId(PyNumerical):
                            """
                            Parameter DomainId of value type int.
                            """
                            pass

                        class InternalName(PyTextual):
                            """
                            Parameter InternalName of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                    def __getitem__(self, key: str) -> _UnderRelaxationFactors:
                        return super().__getitem__(key)

                class CourantNumber(PyNumerical):
                    """
                    Parameter CourantNumber of value type float.
                    """
                    pass

            class Methods(PyMenu):
                """
                Singleton Methods.
                """
                def __init__(self, service, rules, path):
                    self.DiscretizationSchemes = self.__class__.DiscretizationSchemes(service, rules, path + [("DiscretizationSchemes", "")])
                    self.PVCouplingScheme = self.__class__.PVCouplingScheme(service, rules, path + [("PVCouplingScheme", "")])
                    self.PVCouplingSchemeAllowedValues = self.__class__.PVCouplingSchemeAllowedValues(service, rules, path + [("PVCouplingSchemeAllowedValues", "")])
                    super().__init__(service, rules, path)

                class DiscretizationSchemes(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _DiscretizationSchemes(PyMenu):
                        """
                        Singleton _DiscretizationSchemes.
                        """
                        def __init__(self, service, rules, path):
                            self.AllowedValues = self.__class__.AllowedValues(service, rules, path + [("AllowedValues", "")])
                            self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                            self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            super().__init__(service, rules, path)

                        class AllowedValues(PyTextual):
                            """
                            Parameter AllowedValues of value type List[str].
                            """
                            pass

                        class DomainId(PyNumerical):
                            """
                            Parameter DomainId of value type int.
                            """
                            pass

                        class InternalName(PyTextual):
                            """
                            Parameter InternalName of value type str.
                            """
                            pass

                        class Value(PyTextual):
                            """
                            Parameter Value of value type str.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                    def __getitem__(self, key: str) -> _DiscretizationSchemes:
                        return super().__getitem__(key)

                class PVCouplingScheme(PyTextual):
                    """
                    Parameter PVCouplingScheme of value type str.
                    """
                    pass

                class PVCouplingSchemeAllowedValues(PyTextual):
                    """
                    Parameter PVCouplingSchemeAllowedValues of value type List[str].
                    """
                    pass

            class Monitors(PyMenu):
                """
                Singleton Monitors.
                """
                def __init__(self, service, rules, path):
                    self.ReportPlots = self.__class__.ReportPlots(service, rules, path + [("ReportPlots", "")])
                    self.Residuals = self.__class__.Residuals(service, rules, path + [("Residuals", "")])
                    super().__init__(service, rules, path)

                class ReportPlots(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _ReportPlots(PyMenu):
                        """
                        Singleton _ReportPlots.
                        """
                        def __init__(self, service, rules, path):
                            self.Active = self.__class__.Active(service, rules, path + [("Active", "")])
                            self.Frequency = self.__class__.Frequency(service, rules, path + [("Frequency", "")])
                            self.FrequencyOf = self.__class__.FrequencyOf(service, rules, path + [("FrequencyOf", "")])
                            self.IsValid = self.__class__.IsValid(service, rules, path + [("IsValid", "")])
                            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                            self.Print = self.__class__.Print(service, rules, path + [("Print", "")])
                            self.ReportDefinitions = self.__class__.ReportDefinitions(service, rules, path + [("ReportDefinitions", "")])
                            self.Title = self.__class__.Title(service, rules, path + [("Title", "")])
                            self.UnitInfo = self.__class__.UnitInfo(service, rules, path + [("UnitInfo", "")])
                            self.XLabel = self.__class__.XLabel(service, rules, path + [("XLabel", "")])
                            self.YLabel = self.__class__.YLabel(service, rules, path + [("YLabel", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            super().__init__(service, rules, path)

                        class Active(PyParameter):
                            """
                            Parameter Active of value type bool.
                            """
                            pass

                        class Frequency(PyNumerical):
                            """
                            Parameter Frequency of value type int.
                            """
                            pass

                        class FrequencyOf(PyTextual):
                            """
                            Parameter FrequencyOf of value type str.
                            """
                            pass

                        class IsValid(PyParameter):
                            """
                            Parameter IsValid of value type bool.
                            """
                            pass

                        class Name(PyTextual):
                            """
                            Parameter Name of value type str.
                            """
                            pass

                        class Print(PyParameter):
                            """
                            Parameter Print of value type bool.
                            """
                            pass

                        class ReportDefinitions(PyTextual):
                            """
                            Parameter ReportDefinitions of value type List[str].
                            """
                            pass

                        class Title(PyTextual):
                            """
                            Parameter Title of value type str.
                            """
                            pass

                        class UnitInfo(PyTextual):
                            """
                            Parameter UnitInfo of value type str.
                            """
                            pass

                        class XLabel(PyTextual):
                            """
                            Parameter XLabel of value type str.
                            """
                            pass

                        class YLabel(PyTextual):
                            """
                            Parameter YLabel of value type str.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                    def __getitem__(self, key: str) -> _ReportPlots:
                        return super().__getitem__(key)

                class Residuals(PyMenu):
                    """
                    Singleton Residuals.
                    """
                    def __init__(self, service, rules, path):
                        self.Equation = self.__class__.Equation(service, rules, path + [("Equation", "")])
                        self.ConvergenceCriterionType = self.__class__.ConvergenceCriterionType(service, rules, path + [("ConvergenceCriterionType", "")])
                        super().__init__(service, rules, path)

                    class Equation(PyNamedObjectContainer):
                        """
                        .
                        """
                        class _Equation(PyMenu):
                            """
                            Singleton _Equation.
                            """
                            def __init__(self, service, rules, path):
                                self.AbsoluteCriterion = self.__class__.AbsoluteCriterion(service, rules, path + [("AbsoluteCriterion", "")])
                                self.CheckConvergence = self.__class__.CheckConvergence(service, rules, path + [("CheckConvergence", "")])
                                self.IsMonitored = self.__class__.IsMonitored(service, rules, path + [("IsMonitored", "")])
                                self.RelativeCriterion = self.__class__.RelativeCriterion(service, rules, path + [("RelativeCriterion", "")])
                                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                super().__init__(service, rules, path)

                            class AbsoluteCriterion(PyNumerical):
                                """
                                Parameter AbsoluteCriterion of value type float.
                                """
                                pass

                            class CheckConvergence(PyParameter):
                                """
                                Parameter CheckConvergence of value type bool.
                                """
                                pass

                            class IsMonitored(PyParameter):
                                """
                                Parameter IsMonitored of value type bool.
                                """
                                pass

                            class RelativeCriterion(PyNumerical):
                                """
                                Parameter RelativeCriterion of value type float.
                                """
                                pass

                            class _name_(PyTextual):
                                """
                                Parameter _name_ of value type str.
                                """
                                pass

                        def __getitem__(self, key: str) -> _Equation:
                            return super().__getitem__(key)

                    class ConvergenceCriterionType(PyTextual):
                        """
                        Parameter ConvergenceCriterionType of value type str.
                        """
                        pass

            class State(PyMenu):
                """
                Singleton State.
                """
                def __init__(self, service, rules, path):
                    self.AeroOn = self.__class__.AeroOn(service, rules, path + [("AeroOn", "")])
                    self.CaseFileName = self.__class__.CaseFileName(service, rules, path + [("CaseFileName", "")])
                    self.CaseId = self.__class__.CaseId(service, rules, path + [("CaseId", "")])
                    self.CaseValid = self.__class__.CaseValid(service, rules, path + [("CaseValid", "")])
                    self.DataId = self.__class__.DataId(service, rules, path + [("DataId", "")])
                    self.DataValid = self.__class__.DataValid(service, rules, path + [("DataValid", "")])
                    self.GridId = self.__class__.GridId(service, rules, path + [("GridId", "")])
                    self.IcingOn = self.__class__.IcingOn(service, rules, path + [("IcingOn", "")])
                    super().__init__(service, rules, path)

                class AeroOn(PyParameter):
                    """
                    Parameter AeroOn of value type bool.
                    """
                    pass

                class CaseFileName(PyTextual):
                    """
                    Parameter CaseFileName of value type str.
                    """
                    pass

                class CaseId(PyNumerical):
                    """
                    Parameter CaseId of value type int.
                    """
                    pass

                class CaseValid(PyParameter):
                    """
                    Parameter CaseValid of value type bool.
                    """
                    pass

                class DataId(PyNumerical):
                    """
                    Parameter DataId of value type int.
                    """
                    pass

                class DataValid(PyParameter):
                    """
                    Parameter DataValid of value type bool.
                    """
                    pass

                class GridId(PyNumerical):
                    """
                    Parameter GridId of value type int.
                    """
                    pass

                class IcingOn(PyParameter):
                    """
                    Parameter IcingOn of value type bool.
                    """
                    pass

        class Streaming(PyMenu):
            """
            Singleton Streaming.
            """
            def __init__(self, service, rules, path):
                self.Ack = self.__class__.Ack(service, rules, path + [("Ack", "")])
                super().__init__(service, rules, path)

            class Ack(PyParameter):
                """
                Parameter Ack of value type bool.
                """
                pass

        class AppName(PyTextual):
            """
            Parameter AppName of value type str.
            """
            pass

        class ClearDatamodel(PyCommand):
            """
            Command ClearDatamodel.


            Returns
            -------
            None
            """
            pass

        class ReadCase(PyCommand):
            """
            Command ReadCase.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            bool
            """
            pass

        class ReadCaseAndData(PyCommand):
            """
            Command ReadCaseAndData.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            bool
            """
            pass

        class ReadData(PyCommand):
            """
            Command ReadData.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            bool
            """
            pass

        class SendCommand(PyCommand):
            """
            Command SendCommand.

            Parameters
            ----------
            Command : str

            Returns
            -------
            bool
            """
            pass

        class WriteCase(PyCommand):
            """
            Command WriteCase.

            Parameters
            ----------
            FileName : str
            Binary : bool
            Overwrite : bool

            Returns
            -------
            bool
            """
            pass

        class WriteCaseAndData(PyCommand):
            """
            Command WriteCaseAndData.

            Parameters
            ----------
            FileName : str
            Binary : bool
            Overwrite : bool

            Returns
            -------
            bool
            """
            pass

        class WriteData(PyCommand):
            """
            Command WriteData.

            Parameters
            ----------
            FileName : str
            Binary : bool
            Overwrite : bool

            Returns
            -------
            bool
            """
            pass

