import logging
import requests

logger = logging.getLogger(__name__)


class Switch:
    """Represents a Shelly 1PM switch.
    Can be turned on or off using http put.

    """

    def __init__(self, setup: dict):
        """

        :type setup: dict
        """
        # Set default values
        self.on_url = 'http://192.168.50.128/relay/0?turn=on'
        self.off_url = 'http://192.168.50.128/relay/0?turn=off'
        self.ip_addr = '192.168.50.128'
        self.switch_timeout = '2'
        # Override defaults with setup values
        try:
            self.on_url = setup['switch_on_url']
            self.off_url = setup['switch_off_url']
            self.ip_addr = setup['switch_ip_addr']
            self.switch_timeout = setup['switch_timeout']
        except KeyError as ex:
            if ex.args[0] == 'switch_timeout':
                self.switch_timeout = 2
        finally:
            logger.debug(f'Switch on URL:      {self.on_url}')
            logger.debug(f'Switch off URL:     {self.off_url}')
            logger.debug(f'Switch IP address:  {self.ip_addr}')
            logger.debug(f'Switch timeout:     {self.switch_timeout}')

    def on(self):
        try:
            logger.info(f'Turning switch off.')
            requests.put(self.on_url, timeout=self.switch_timeout)
        except (requests.exceptions.ConnectTimeout, TimeoutError, ConnectionError) as ex:
            logger.error(f'Switch failed to turn on: {ex}')
            raise  # This is a failure that needs to bubble up.

    def off(self):
        try:
            logger.info(f'Turning switch off.')
            requests.put(self.off_url, timeout=self.switch_timeout)
        except (requests.exceptions.ConnectTimeout, TimeoutError, ConnectionError) as ex:
            logger.error(f'Switch failed to turn off: {ex}')
