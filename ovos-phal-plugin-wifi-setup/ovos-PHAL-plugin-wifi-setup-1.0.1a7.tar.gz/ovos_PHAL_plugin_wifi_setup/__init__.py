import subprocess
import random
import uuid
from os.path import dirname, join
from time import sleep

from mycroft_bus_client.message import Message
from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils import create_daemon
from ovos_utils.device_input import can_use_touch_mouse
from ovos_utils.enclosure.api import EnclosureAPI
from ovos_utils.gui import (GUIInterface,
                            is_gui_running, is_gui_connected)
from ovos_utils.log import LOG
from ovos_utils.skills.settings import PrivateSettings
from ovos_utils.network_utils import is_connected

# Event Documentation
# ===================
# Registration:
# ----------------
# ovos.phal.wifi.plugin.register.client
# type: Request
# description: Register a client to the plugin (requested by the client)
#
# ovos.phal.wifi.plugin.deregister.client
# type: Request
# description: Deregister a client from the plugin (requested by the client)
#
# ovos.phal.wifi.plugin.client.registration.failure
# type: Response
# description: Registration failed
#
# ovos.phal.wifi.plugin.client.registered
# type: Response
# description: Registration successful
#
# ovos.phal.wifi.plugin.client.deregistered
# type: Response
# description: Deregistration successful
#
# Client Activation / Deactivation
# --------------------------------
# ovos.phal.wifi.plugin.set.active.client
# type: Request
# description: Activate a client (requested by the client)
#
# ovos.phal.wifi.plugin.remove.active.client
# type: Request
# description: Deactivate a client (requested by the client)
#
# ovos.phal.wifi.plugin.activate.{clientID}
# type: Response
# description: Inform the client that the activation was successful
#
# ovos.phal.wifi.plugin.deactivate.{clientID}
# type: Response
# description: Inform the client that the deactivation was successful
#
# Client Setup Running / Finished
# --------------------------------
# ovos.phal.wifi.plugin.client.setup.failure
# type: Request
# description: Inform the wifi plugin that the client setup failed
#
# Plugin VUI / GUI Interaction (Client Selection)
# --------------------------------------------
# ovos.phal.wifi.plugin.client.select
# type: Request
# description: Inform the wifi plugin that a client was selected
#
# ovos.phal.wifi.plugin.skip.setup
# type: Request
# description: Inform the wifi plugin that further setup is not needed
#
# ovos.phal.wifi.plugin.user.activated
# type: Request
# description: Inform the wifi plugin that the user has activated the client
#
# Generic Messages (Plugin Actions)
# ----------------
# mycroft.internet.connected
# type: Request
# description: Inform the wifi plugin that the internet is connected
#
# enclosure.notify.no_internet
# type: Response
# description: Notify watchdog detected internet disconnected
#
# ovos.phal.wifi.plugin.fully_offline
# type: Response
# description: Notify that the user has selected fully offline operation
#
# ovos.phal.wifi.plugin.alive
# type: Response
# description: Inform the wifi clients that the plugin is alive on startup
#
# ovos.phal.wifi.plugin.status
# type: Request
# description: Request the wifi plugin to send the status of the plugin
#
# ovos.phal.wifi.plugin.status.response
# type: Response
# description: Notify setup and watchdog status
#
# ovos.phal.wifi.plugin.stop.setup.event
# type: Response
# description: Inform the wifi clients to stop the setup event completely and clean up
#
# ovos.phal.wifi.plugin.setup.failed
# type: Response
# description: Inform the interested parties that the plugin itself failed


class WifiSetupPlugin(PHALPlugin):

    def __init__(self, bus=None, config=None):
        name = "ovos-PHAL-plugin-wifi-setup"
        super().__init__(bus=bus, name=name, config=config)
        self.monitoring = False
        self.in_setup = False
        self.client_in_setup = False

        # this is a XDG compliant jsonstorage object similar to self.settings in MycroftSkill
        # it can be used to keep state
        self.settings = PrivateSettings(name)

        # self.connected = False
        self.grace_period = 45
        self.time_between_checks = 30
        self.mycroft_ready = False
        self.stop_on_internet = False
        self.timeout_after_internet = 90
        self.active_client = None
        self.active_client_id = None
        self.registered_clients = []
        self.gui = GUIInterface(bus=self.bus, skill_id=self.name)

        # 0 = Normal Operation, 1 = Skipped (User selected to skip setup)
        # if the user selected to skip setup, we will not start the setup process or check for internet, etc.
        # until the user explicitly tells us to start the setup process again either through VUI or GUI interaction
        self.plugin_setup_mode = 0

        # Manage client registration, activation and deactivation
        # Multiple clients can be registered, but only one can be active at a time
        self.bus.on("ovos.phal.wifi.plugin.register.client", self.handle_register_client)
        self.bus.on("ovos.phal.wifi.plugin.deregister.client", self.handle_deregister_client)
        self.bus.on("ovos.phal.wifi.plugin.get.registered.clients", self.handle_get_registered_clients)
        self.bus.on("ovos.phal.wifi.plugin.set.active.client", self.handle_set_active_client)
        self.bus.on("ovos.phal.wifi.plugin.remove.active.client", self.handle_remove_active_client)

        # Manage when the client is in setup and out of setup
        self.bus.on("ovos.phal.wifi.plugin.client.setup.failure", self.handle_client_setup_failure)

        # GUI event to handle client selection
        # Client selection is presented to the user in the GUI if GUI and touch/mouse are available
        self.bus.on("ovos.phal.wifi.plugin.client.select", self.handle_client_select)
        self.bus.on("ovos.phal.wifi.plugin.skip.setup", self.handle_skip_setup)
        self.bus.on("ovos.phal.wifi.plugin.fully.offline", self.handle_fully_offline)
        self.bus.on("ovos.phal.wifi.plugin.client.select.page.removed", self.handle_setup_page_removed)

        # GUI event to handle user activation of plugin (user selected the plugin in the GUI)
        # or via voice command (user activated the plugin via voice command)
        self.bus.on("ovos.phal.wifi.plugin.user.activated", self.handle_user_activated)

        # Handle Internet Connected Event
        self.bus.on("mycroft.internet.connected", self.handle_internet_connected)

        # When the plugin comes online, we need to emit a message so clients can register
        self.bus.emit(Message("ovos.phal.wifi.plugin.alive"))
        # Also let the clients ask if the plugin is alive
        self.bus.on("ovos.phal.wifi.plugin.status", self.handle_status_request)

        # Check if internet is ready for mycroft_ready
        self.bus.on("mycroft.internet.is_ready", self.handle_ready_check)

        self.enclosure = EnclosureAPI(bus=self.bus, skill_id=self.name)
        self.start_internet_check()

    @property
    def first_boot(self):
        return self.settings.get("first_boot", True)

    @first_boot.setter
    def first_boot(self, val):
        self.settings["first_boot"] = bool(val)
        self.settings.store()

    @property
    def enable_watchdog(self):
        return self.settings.get("enable_watchdog", True)

    @enable_watchdog.setter
    def enable_watchdog(self, val):
        self.settings["enable_watchdog"] = bool(val)
        self.settings.store()

    # Generic Status Check
    ############################################################################

    def handle_status_request(self, message=None):
        # Check if the plugin is loaded and running
        if self.monitoring:
            self.bus.emit(Message("ovos.phal.wifi.plugin.alive"))
        message.response({"watchdog_active": self.enable_watchdog,
                          "in_setup": self.in_setup})

    # Client Registeration, De-Registration, Activation and Deactivation Section
    ############################################################################

    def handle_register_client(self, message=None):
        client_plugin_name = message.data.get("client", "")
        client_plugin_type = message.data.get("type", "")
        client_plugin_display_text = message.data.get("display_text", "")
        client_plugin_has_gui = message.data.get("has_gui", False)
        client_plugin_requires_input = message.data.get("requires_input", False)

        # Fist make sure the required parameters are present
        if not client_plugin_name or not client_plugin_type or not client_plugin_display_text:
            self.bus.emit(Message("ovos.phal.wifi.plugin.client.registration.failure", {"error": "Missing required parameters"}))
            return

        if not client_plugin_has_gui and not client_plugin_requires_input:
            self.bus.emit(Message("ovos.phal.wifi.plugin.client.registration.failure", {"error": "Missing required parameters"}))
            return

        # Use the client plugin id for activation and deactivation rather than depending on parameters in the message
        random_uuid = str(uuid.uuid4())
        client_plugin_id = client_plugin_name[-2:] + client_plugin_type[-2:] + str(
            random.randint(0, 9)) + str(random.randint(0, 9)) + random_uuid[-1:] + random_uuid[0]

        # First check if we already have this client registered, if not, add it
        if not any((client.get('client') == client_plugin_name
                    for client in self.registered_clients)):
            self.registered_clients.append({
                "client": client_plugin_name,
                "type": client_plugin_type,
                "display_text": client_plugin_display_text,
                "has_gui": client_plugin_has_gui,
                "requires_input": client_plugin_requires_input,
                "id": client_plugin_id
            })
            # Emit a message if the client has been registered
            self.bus.emit(Message("ovos.phal.wifi.plugin.client.registered", {
                "client": client_plugin_name,
                "type": client_plugin_type,
                "display_text": client_plugin_display_text,
                "has_gui": client_plugin_has_gui,
                "requires_input": client_plugin_requires_input,
                "id": client_plugin_id
            }))

            # Update the GUI so client selection has all options
            if self.gui.get('page_type') == "ModeChoose":
                LOG.info(f"Updating GUI with new clients: "
                         f"{self.registered_clients}")
                self.gui["clients_model"] = self.registered_clients
            else:
                LOG.debug(f"Not updating gui with clients: "
                          f"{self.gui.get('clients_model')}")
            LOG.info("Registered wifi client: " + client_plugin_name)

    def handle_deregister_client(self, message=None):
        client_plugin_name = message.data.get("client", "")

        for client in self.registered_clients:
            # If the client is found, remove the dictionary entry from the list
            # and emit a message to the client that it has been deregistered
            if client.get("client", "") == client_plugin_name:
                self.registered_clients.remove(client)
                self.bus.emit(Message("ovos.phal.wifi.plugin.client.deregistered", {
                    "client": client_plugin_name
                }))
                return

    def handle_get_registered_clients(self, message=None):
        self.bus.emit(Message("ovos.phal.wifi.plugin.registered.clients", {
            "clients": self.registered_clients
        }))

    def handle_set_active_client(self, message=None):
        set_client = message.data.get("client", "")
        set_client_id = message.data.get("id", "")

        # First make sure the client is registered
        for client in self.registered_clients:
            if client["client"] == set_client:
                self.active_client = set_client
                self.active_client_id = set_client_id
                # Tell the client that it is now active
                self.client_in_setup = True
                if set_client_id:
                    self.bus.emit(Message(f"ovos.phal.wifi.plugin.activate.{set_client_id}"))
                else:
                    LOG.error("No client id found to activate")

                # Release the gui once the client is set so client can take control of the gui
                self.gui.release()
                self.in_setup = False

    def handle_remove_active_client(self, message=None):
        if self.active_client is not None:
            self.active_client = None
        if self.active_client_id is not None:
            self.bus.emit(Message(f"ovos.phal.wifi.plugin.deactivate.{self.active_client_id}"))
            self.active_client_id = None
            if is_connected():
                self.bus.emit(Message("mycroft.internet.connected"))
        self.client_in_setup = False

    # Client Setup Control Section
    ############################################################################

    def handle_client_setup_failure(self, message=None):
        if self.active_client is not None:
            self.active_client = None
        if self.active_client_id is not None:
            self.bus.emit(Message(f"ovos.phal.wifi.plugin.deactivate.{self.active_client_id}"))
            self.active_client_id = None
        self.client_in_setup = False

    # Client Selection Section And GUI (Path only active if GUI and touch/mouse are available)
    ############################################################################

    def handle_client_select(self, message=None):
        # If the client is in setup, do not allow the user to select a client
        if self.client_in_setup:
            return

        # If the client is not in setup, and the client is not active, we can select a client
        if self.active_client is None:
            user_requested_client = message.data.get("client", "")
            user_requested_id = message.data.get("id", "")
            LOG.info("User requested client {0}".format(user_requested_client))

            for client in self.registered_clients:
                if client["client"] == user_requested_client:
                    self.handle_set_active_client(Message("ovos.phal.wifi.plugin.set.active.client", {
                        "client": user_requested_client,
                        "id": user_requested_id
                    }))
                    return
        self.in_setup = False

    def display_client_select(self, message=None):
        self.in_setup = True
        self.gui.clear()
        page = join(dirname(__file__), "ui", "WifiPluginClientLoader.qml")
        self.gui["page_type"] = "ModeChoose"
        self.gui["clients_model"] = self.registered_clients
        self.gui.show_page(page, override_idle=self.first_boot or None,
                           override_animations=True)
        
    def handle_skip_setup(self, message=None):
        self.in_setup = False
        self.client_in_setup = False
        self.active_client = None
        self.active_client_id = None

        # Deactivate the running watchdog daemon
        self.monitoring = False

        # set the plugin setup mode to 1 (skip setup)
        self.plugin_setup_mode = 1

        # Notify any listeners that we're in offline mode now
        message = message.forward("ovos.phal.wifi.plugin.fully_offline") or \
            Message("ovos.phal.wifi.plugin.fully_offline")
        self.bus.emit(message)
        self.gui.clear()

    def handle_fully_offline(self, message=None):
        self.in_setup = False
        self.client_in_setup = False
        self.active_client = None
        self.active_client_id = None
        self.monitoring = False
        self.enable_watchdog = False
        self.plugin_setup_mode = 1

        # First boot setup completed
        self.first_boot = False

        # Notify any listeners that we're in offline mode now
        message = message.forward("ovos.phal.wifi.plugin.fully_offline") or \
            Message("ovos.phal.wifi.plugin.fully_offline")
        self.bus.emit(message)
        self.gui.clear()

    def handle_user_activated(self, message=None):
        # enable the watchdog if user activated the service manually
        self.enable_watchdog = True
        
        # first check the plugin setup mode
        if self.plugin_setup_mode == 1:
            self.plugin_setup_mode = 0
            self.start_internet_check()
        else:
            # Assume the user wants to run the setup process manually
            self.launch_networking_setup()

    def handle_setup_page_removed(self, message=None):
        LOG.debug("Mode Select Page Removed")
        self.in_setup = False

    # Internet Check and Watchdog Section
    ############################################################################

    def start_internet_check(self):
        # Check the plugin setup mode to see if we should start the internet check
        if self.enable_watchdog:
            if self.plugin_setup_mode == 0:
                create_daemon(self._watchdog)
            else:
                LOG.info("Internet check disabled by user")
        else:  # User selected offline mode
            self.plugin_setup_mode = 1  # Advertise internet is ready
            LOG.info("Internet check disabled by skip network setup")
        
    def stop_internet_check(self):
        self.monitoring = False

    def _watchdog(self):
        try:
            self.monitoring = True
            LOG.info("Wifi watchdog started")
            output = subprocess.check_output("nmcli connection show",
                                             shell=True).decode("utf-8")
            active_output = subprocess.check_output("nmcli -f STATE,TYPE connection show --active",
                                                    shell=True).decode("utf-8")

            if "activated" in active_output:
                LOG.info("Network is active")
                self.handle_internet_connected()

            if "wifi" in output:
                LOG.info("Detected previously configured wifi, starting "
                         "grace period to allow it to connect")
                sleep(self.grace_period)

            while self.monitoring:
                if self.in_setup or self.client_in_setup:
                    sleep(1)  # let client and setup do it's thing
                    continue

                if not is_connected():
                    self.bus.emit(Message("enclosure.notify.no_internet"))
                    LOG.info("NO INTERNET")
                    if not self.is_connected_to_wifi():
                        LOG.info("LAUNCH SETUP")
                        try:
                            self.launch_networking_setup()  # non-blocking
                            if self.first_boot:
                                LOG.debug("First boot setup completed")
                                self.first_boot = False
                        except Exception as e:
                            LOG.exception(e)
                    else:
                        LOG.warning("CONNECTED TO WIFI, BUT NO INTERNET!!")
                sleep(self.time_between_checks)
        except Exception as e:
            LOG.error("Wifi watchdog crashed unexpectedly")
            LOG.exception(e)

    @staticmethod
    def get_wifi_ssid():
        SSID = None
        try:
            SSID = subprocess.check_output(["iwgetid", "-r"]).strip()
        except subprocess.CalledProcessError:
            # If there is no connection subprocess throws a 'CalledProcessError'
            pass
        return SSID

    @staticmethod
    def is_connected_to_wifi():
        return WifiSetupPlugin.get_wifi_ssid() is not None

    def launch_networking_setup(self):
        self.bus.emit(Message("ovos.phal.wifi.plugin.setup.launched"))

        try:
            if (is_gui_running() or is_gui_connected(self.bus)) and can_use_touch_mouse():
                LOG.debug("GUI / INPUT DETECTED LAUNCHING GUI")
                self.display_client_select()
            else:
                # First lets check if we have a client that can setup without requiring a physical input method
                # If we do find a registered client that has requires_input set to false, we can use it
                # example (balena-wifi-setup)
                LOG.debug("LAUNCHING NON INPUT INTERACTIVE SETUP")

                # First check if there are any clients registered at all
                if len(self.registered_clients) == 0:
                    LOG.error("No clients registered")

                # Check if there are any clients that do not require input
                for client in self.registered_clients:
                    if not client["requires_input"]:
                        self.handle_set_active_client(Message("ovos.phal.wifi.plugin.set.active.client", {
                            "client": client["client"],
                            "id": client["id"]
                        }))
                        return

        except Exception as e:
            LOG.exception(e)
            self.bus.emit(Message("ovos.phal.wifi.plugin.setup.failed", {"error": "Unknown error"}))

    def handle_internet_connected(self, message=None):
        """System came online later after booting."""
        message = message or Message("test")
        self.enclosure.mouth_reset()
        # sync clock as soon as we have internet
        self.bus.wait_for_response(message.forward("system.ntp.sync"),
                                   "system.ntp.sync.complete")
        # We don't know if the user has configured setup, so we'll just emit a message for setup skill
        self.bus.emit(message.forward("ovos.wifi.setup.completed"))
        # Make sure the GUI spinner is dismissed
        self.bus.emit(message.forward("ovos.shell.status.ok"))
        self.stop_setup()  # just in case

    def handle_ready_check(self, message=None):
        """ Check if internet is ready """
        status = self.plugin_setup_mode == 1 or is_connected()
        if self.client_in_setup:
            LOG.debug(f"Still in setup, wait for completion")
            status = False
        self.bus.emit(message.response({"status": status}))

    def stop_setup(self):
        self.gui.release()
        self.bus.emit(Message("ovos.phal.wifi.plugin.stop.setup.event"))
        self.in_setup = False

        # Disable first boot once setup is asked to stop
        self.first_boot = False

    def shutdown(self):
        self.monitoring = False
        self.bus.remove("mycroft.internet.connected",
                        self.handle_internet_connected)
        self.stop_setup()
        super().shutdown()
