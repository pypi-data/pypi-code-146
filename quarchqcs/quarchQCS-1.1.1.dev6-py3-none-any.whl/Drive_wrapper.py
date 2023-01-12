class DriveWrapper:
    """
    Allows drive to be parsed into object for use throughout Quarchpy

    """
    def __init__(self):
        """
                Constructor for quarchDevice, allowing the connection method of the device to be specified.

                Variables
                ----------
                identifier : str : REQUIRED

                    Identifier String: Different depending on drive type and OS being used

                    Examples:
                    05:00.0             - Standard PCIe identifier, Windows and Linux
                    \\.\PHYSICALDRIVE0  - An identifier for Windows
                    /dev/sda            - Standard smartctl drive identify - Windows and linux
                    ....

                drive_type : str : REQUIRED

                    Specifies the type of Drive in use

                    ### QCS1.09 - Test no longer determined by sas / PCIE ###

                description : str, REQUIRED

                    Description provided of Drive - Drive manufacturer / drive specific

                system_cmd : str, optional

                    Specifies the system command that was used to detect the drive
                    This is only currently used in detection

                serial_number : str, optional

                    Serial number of the DUT

                storage_capacity : str, optional

                    Storage capacity of the drive, QCS will report whatever string is assigned to this variable

                firmware_version : str, optional

                    Version of the firmware currently running of the DUT

                lane_width : str, optional

                    Specified only for PCIe Modules. Reports found Lane width stat of drive
                    Output of LSCPI -vv command.

                link_speed : str, optional

                    Specified only for PCIe Modules. Reports found link speed stat of drive
                    Output of LSCPI -vv command.

                fio_path : Str : Optional.

                    The FIO path used by FIO in order to start workloads on this drive.
                    windows:
                        \\.\PHYSICALDRIVEX
                    Linux:
                        /dev/sda
                        /dev/nvme0n1

                    Please check the FIO path is valid by running it against an FIO job.

                """

        self.identifier_str = ""
        self.drive_type = ""
        self.description = ""
        self.FIO_path = None


        # Optional extras
        self.drive_path = None
        self.link_speed = None
        self.lane_width = None
        self.system_cmd = ""
        self.serial_number = None
        self.storage_capacity = None
        self.firmware_version = None
        self.all_info = {}



