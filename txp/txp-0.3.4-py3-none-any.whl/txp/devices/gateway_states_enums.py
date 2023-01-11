"""
This module defines the Gateway States-Status related enumerations.
"""
# ============================ imports =========================================
import enum


# ==============================================================================
# Definition of the custom Gateway States enumeration
# ==============================================================================
class GatewayStates(enum.Enum):
    def __str__(self):
        return self.name

    Uninitialized = 0
    """Uninitialized: Internal state to set and keep consistency while the states machine is being 
    programatically initialized"""

    Startup = 1
    """Startup: Receiving initial files and values from the user interaction with the Gateway Local 
    web page."""

    # TODO: Delete this.
    StartupError = 2
    """StartupError: Error from Startup state"""

    ConfigurationReception = 3
    """ConfigurationReception: State in which the cloud logical configuration is received"""

    # TODO: Delete this.
    ConfigurationReceptionError = 4
    """ConfigurationReceptionError: Error from ConfigurationReception state"""

    ConfigurationValidation = 5
    """ConfigurationValidation: State to process the received configuration and choose a path of execution"""

    PreparingDevices = 7
    """PreparingDevices: State to transition when the gateway needs to create the DriversHost and Drivers
    This state can be reached after production phase, or when a produced gateway is turned on.
    """

    DevicesPairing = 8
    """DevicesPairing: State to step into when an edge devices pairing is required"""

    DevicePairingError = 9
    """DevicePairingError: Error from DevicesPairing state"""

    Ready = 10
    """Ready: The Gateway instance is ready to operate"""

    Sampling = 11
    """Sampling: The gateway is currently sampling raw data from the edge devices"""

    Error = 12
    """Error: A General Error state to handle error cases."""


class StartupStatus(enum.Enum):
    RequestRequiredValues = 1
    """Request the required values from the user input."""
    RequiredValuesReceived = 2
    """The user has entered the required values. The Gateway will proceed to test those."""


class ConfigurationReceptionStatus(enum.Enum):
    EstablishCloudConnection = 1
    Idle = 2
    ListenGatewayConfiguration = 3
    ListenMachinesConfiguration = 4
    ListenEdgesConfiguration = 5


class ConfigurationValidationStatus(enum.Enum):
    CheckConfigurations = 1
    UserConfirmedSettings = 2


class PreparingDevicesStatus(enum.Enum):
    CreatingDriversHosts = 1
    CreatingDrivers = 2
    WaitingForDevicesToBeConnected = 3


class ConfigurationUpdateStatus(enum.Enum):
    UpdatePreviousConfiguration = 1


class DevicePairingStatus(enum.Enum):
    SelectDeviceToPair = 1
    PairingSelectedDevice = 2
    RequestConfirm = 3
    PairingConfirmed = 4
    PairingCancelled = 5
    PairingError = 6

    # Virtual Pairing Status
    RequestVirtualCameraConnection = 7
    VirtualCameraConnectionConfirmed = 8
    VirtualCameraProducedSuccessfully = 9
    VirtualCameraConnectionError = 10

    RequestVirtualThermocameraConnection = 11
    VirtualThermocameraConnectionConfirmed = 12
    VirtualThermocameraProducedSuccessfully = 13
    VirtualThermocameraConnectionError = 14

    VirtualRequestNextStepFromUser = 15  # Cameras already paired, the user selects what to do
    VirtualEnableTorque = 16
    VirtualDisableTorque = 17
    VirtualCapturePosition = 18
    VirtualRejectCapturedPosition = 19
    VirtualConfirmCapturedPosition = 20
    VirtualConfirmAllPositions = 21


class DevicePairingErrorStatus(enum.Enum):
    ErrorPairingDevice = 1


class ReadyStatus(enum.Enum):
    def __str__(self):
        return self.name
    Idle = 1
    SchedulingSampling = 2


class GatewaySamplingStatus(enum.Enum):
    def __str__(self):
        return self.name

    Sampling = 1
    CollectPackages = 2
    SendPackages = 3


# =========================== ERROR known error status ==============================
class GatewayErrorStatus(enum.Enum):
    ProductionNotCompleted = 1
