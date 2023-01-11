"""
This module contains the concrete implementation case of Driver for the
smartmesh dongle USB device.
Technical details about the device can be found in the following document:
https://tranxpert.atlassian.net/wiki/spaces/TD/pages/230817807/Tranxpert+MVP+Monitoring+Proposal#Several-Voyager-3-working-together.
"""

# ============================ imports =========================================
import queue
import time
import serial.tools.list_ports
from typing import Dict, Tuple, List

from IpMgrConnectorSerial.IpMgrConnectorSerial import IpMgrConnectorSerial
from IpMgrConnectorMux.IpMgrSubscribe import IpMgrSubscribe
from SmartMeshSDK import ApiException
from txp.devices.drivers.driver import DriverState
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# Voyager SmartMesh Manager Singleton
# ==============================================================================
class SmartMeshDongle(object):
    """The USB smartmesh dongle used as manager to handle smartmesh devices.

    This class is implemented following a singleton pattern.

    TODO: Custom Exception handling in the methods of the class.

    The main responsibility for this class is to communicate with the
    edge devices connected in the smartmesh network through the
    direct interaction with the smartmesh dongle device.
    """

    """
    Constant data configured values
    """
    Vcc = 3.3  # Supply Voltage
    V_perg_ref = 0.04  # V per g at reference voltage
    Vref = 1.8  # 1.8V reference voltage
    ADC_res = 16  # No of bits resolution
    ADC_offset = 2 ** (ADC_res - 1)
    V_per_LSB = Vcc / 2 ** ADC_res  # V per LSB resolution
    V_perg_Vcc = V_perg_ref * Vcc / Vref  # Volts per g at Vcc
    ADC_gain = V_per_LSB / V_perg_Vcc  # Gain of ADC
    f_adc = 6.5e6  # ADC clock frequency
    n_acq = 185  # Acq. time in clock periods

    def __init__(self, on_driver_state_change: callable):
        self.ID = 0
        self.connector = IpMgrConnectorSerial()
        self.mac = []
        """mac: The MAC address of the dongle device.
                Is this address returned in the connector call? 
                Probably some API to get it
        """
        self.operational_macs: List[Tuple] = []
        """operational_macs: A list of found operational devices MAC addresses."""
        self.drivers_packets_queues: Dict[Tuple, queue.PriorityQueue] = {}
        """edge_descriptors: A mapping of MAC address to Driver's packets queue."""
        self.num_motes: int = 0
        self.connected: bool = False
        self.net_config = None

        self.subscriber = None
        self.lights = []

        # Network Config Information
        self.netID = None
        self.max_drivers = None
        self.base_bw = None
        self.UDP_PORT_NUMBER = 61624

        # Default attributes for sampling parameters
        self.adc_num_samples = 512
        self.adc_param_len = 2

        self._port = None
        """_port: The connection port of the device."""

        #connection state change callable handler
        self.on_driver_state_change = on_driver_state_change

    def detect(self) -> bool:
        """This method looks for SmartMesh devices connected to the Gateway.

        TODO: Store the state of found ports. How to decide which port to use?

        Returns:
            True if the device was found. False otherwise.
        """
        devices = []
        ports = serial.tools.list_ports.comports()
        ports.sort(reverse=True)

        log.debug(
            f"SmartMesh manager. Ports to try connection: { [port.device for port in ports] }"
        )

        for port in ports:
            if (devices and port.vid == last_device) or not port.vid:
                continue
            try:
                log.debug(f"Trying to connect to path: {port.device} --- Device hwid: {port.hwid}")
                self.connector.connect({"port": str(port.device)})
                last_device = port.vid
                devices.append(str(port.device))
                self.connector.disconnect()
            except:
                pass
        # TODO: Selecting the first port found, based on example. Not final implementation.
        if devices:
            self._port = devices[0]
            return True

        return False

    def connect(self):
        """Connect the Manager to the SmartMesh network and the dongle device.

        If the Manager connects successfully, then it'll hold the list of operational
        edge devices by MAC addresses in self._operational_macs.

        Returns:
            None.
        """
        if self.connected:
            return
        if self._port is None:
            log.debug(
                "Trying to connect VoyagerSmartMeshManager but no connected device port was found"
            )
            raise RuntimeError(
                "Trying to connect VoyagerSmartMeshManager but no connected device port was found"
            )
        try:
            self.connector.connect({"port": self._port})
            log.info("Connected to SmartMeshNetwork")
            self.connected = True
        except:
            raise Exception("The SmartMesh manager device was not detected.")

        self.net_config = self.connector.dn_getNetworkConfig()
        self._get_motes()
        # Subscribe notification data callback
        self._subscribe_to_mote_data()

    def disconnect(self):
        """Disconnect the Manager from the SmartMesh network and dongle device.

        Returns:
             None.
        """
        if not self.connected:
            return

        self.connector.disconnect()
        self.operational_macs.clear()
        self.connected = False
        self.num_motes = 0
        log.info("SmartMesh manager was disconnected")

    def get_motes_connected(self):
        """Get the amount of motes currently connected to the manager.

        Returns:
            The amount of motes connected to the manager.
        """

        return self.num_motes

    def get_adc_number_of_samples(self):
        """Get the amount of samples taken by the ADC

        Returns:
            The amount of samples taken by the ADC
        """
        return self.adc_num_samples

    def get_adc_length(self):
        """Get the ADC length

        Returns:
            The the ADC length in bits
        """
        return self.adc_param_len

    def register_driver(
            self, mac_address: Tuple, driver_samples_queue: queue.PriorityQueue
    ):
        """Registers the Driver instance in the Manager.

        Right now, this means to provide the Manager with the priority queue
        of the driver. The manager will put received packages in the queues
        associated to the MAC address.
        """
        if mac_address in self.operational_macs:
            self.drivers_packets_queues[mac_address] = driver_samples_queue

    def unregister_device(self, mac_address: Tuple):
        """Unregister the Driver instance from the manager.

        This means to remove the driver packets queue from the manager.
        The driver will not register new packets received from the physical layer.
        """
        if mac_address in self.operational_macs:
            self.drivers_packets_queues.pop(mac_address)

    def send_to_mote(self, mac: Tuple, message: any):
        """Sends message to be received by mote device.
        # TODO: Raise exception on error or set state?
        Message can be read in mote module SmartMeshRFcog.c in RCV section.
        """
        try:
            rc = self.connector.dn_sendData(
                macAddress=mac,
                priority=0,

                srcPort=self.UDP_PORT_NUMBER,
                dstPort=self.UDP_PORT_NUMBER,
                options=0,
                data=[ord(i) for i in message],
            )
            if rc[0] == 0:
                log.info(f"Sent command to {self.pretty_mac(mac)} successfully")
            else:
                log.info(f"Unsuccessful command to {self.pretty_mac(mac)}")
        except:
            log.error(f"ERROR on send. Mote not connected. {self.pretty_mac(mac)}")

    def send_to_all_motes(self, message: any):
        """Sends message to all motes connected to the current network"""
        if self.num_motes > 0:
            log.info(f"Sending message to all motes: {message}")
            for mac in self.operational_macs:
                self.send_to_mote(mac, message)

    def _get_motes(self):
        """Asks for the connected edge devices in the network, and stores the operational
        MAC's
        """
        continueAsking = True
        currentMac = (0, 0, 0, 0, 0, 0, 0, 0)

        while continueAsking:  # While mote remains, add mote MAC to operational_macs
            try:
                res = self.connector.dn_getMoteConfig(currentMac, True)
            except ApiException.APIError:
                continueAsking = False
            else:
                if not res.isAP and res.state in [
                    4,
                ]:  # Not access point and in operational state
                    self.operational_macs.append(tuple(res.macAddress))
                currentMac = res.macAddress

        self.num_motes = len(self.operational_macs)

        for mac in self.operational_macs:
            log.info("Mote detected: {}".format(self.pretty_mac(mac)))
            self.on_driver_state_change(mac, DriverState.CONNECTED)

    def _subscribe_to_mote_data(self):
        """Subscribe the method to be called when notification data arrives from
        a mote.

        Returns:
            None
        """
        self.subscriber = IpMgrSubscribe(self.connector)
        self.subscriber.start()
        self.subscriber.subscribe(
            notifTypes=[
                IpMgrSubscribe.NOTIFDATA,  # Subscribe to notification data only
            ],
            fun=self._handle_notifdata,
            isRlbl=False,
        )

        self.subscriber.subscribe(
            notifTypes=[
                IpMgrSubscribe.NOTIFEVENT,
            ],
            fun=self._handle_notification_event,
            isRlbl=False,
        )

    def _handle_notification_event(self, notifName, notifParams):
        """Handle smartmesh manager events related to the status of the motes. Those messages can be used to manage
        the connection/disconnection events.

        Args:
            notifName: Notification ID sent by the smartmesh dongle:
            - eventMoteJoin: Mote attempting to join to the network.
            - eventMoteOperational: Mote has joined to the network.
            - eventMoteLost: Mote unreacheble or disconnected.
            notifParams: Structure holding smartmesh message metadata.
        Returns:
            None.
        """
        mac = tuple(notifParams.macAddress)
        pretty_address = self.pretty_mac(mac)
        if notifName == IpMgrSubscribe.EVENTMOTEOPERATIONAL:
            log.info("The Device with MAC {} was connected".format(pretty_address))
            self.on_driver_state_change(mac, DriverState.CONNECTED)
            if not self.operational_macs.__contains__(mac):
                self.operational_macs.append(mac)
                log.info("MAC {} has been added to list".format(pretty_address))



        if notifName == IpMgrSubscribe.EVENTMOTELOST:
            log.info("The Device with MAC {} was disconnected.".format(pretty_address))
            self.on_driver_state_change(mac, DriverState.DISCONNECTED)
            if self.operational_macs.__contains__(mac):
                self.operational_macs.remove(mac)
                log.info("MAC {} has been removed from list".format(pretty_address))


    def _handle_notifdata(self, notifName, notifParams):
        """Parses mote packet for timestamp and data. Finally, it pass
        the information to the Driver mote packets queue.

        Args:
            notifName: ID data from header of smartmesh packet, specifying type of data:
                Notification.
            notifParams: Structure holding smartmesh message data and metadata, time sent,
                and data.
        Returns:
            None.
        """
        mac_tuple = tuple(notifParams.macAddress)
        if mac_tuple not in self.drivers_packets_queues:
            return

        timestamp = notifParams.utcSecs + 1e-6 * notifParams.utcUsecs
        # Put the package in the driver priority queue, with the priority set to timestamp
        self.drivers_packets_queues[mac_tuple].put((timestamp, notifParams.data))

    @staticmethod
    def pretty_mac(mac):
        """Parses mote mac tuple into is corresponding string

        Args:
            mac: mac id tuple
        Returns:
            Mac string.
        """
        pMac = "-".join(["%02x" % b for b in mac])
        return pMac