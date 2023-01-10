import logging
import re

import pytz
from aprsd import conf  # noqa
from aprsd import plugin, plugin_utils
from aprsd.plugins import time
from opencage.geocoder import OpenCageGeocode
from oslo_config import cfg

import aprsd_timeopencage_plugin
from aprsd_timeopencage_plugin import conf  # noqa


CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class TimeOpenCagePlugin(time.TimePlugin, plugin.APRSFIKEYMixin):

    version = aprsd_timeopencage_plugin.__version__
    # Change this regex to match for your plugin's command
    # Tutorial on regex here: https://regexone.com/
    # Look for any command that starts with w or W
    command_regex = r"^([t]|[t]\s|time)"
    # the command is for ?
    # Change this value to a 1 word description of the plugin
    # this string is used for help
    command_name = "time"

    enabled = False

    def setup(self):
        """Allows the plugin to do some 'setup' type checks in here.

        If the setup checks fail, set the self.enabled = False.  This
        will prevent the plugin from being called when packets are
        received."""
        # Do some checks here?
        self.ensure_aprs_fi_key()
        if not CONF.aprsd_timeopencage_plugin.apiKey:
            LOG.error("Failed to find config aprsd_timeopencage_plugin.apiKey")
            self.enabled = False

    def process(self, packet):
        fromcall = packet.from_call
        message = packet.message_text
        # ack = packet.get("msgNo", "0")

        api_key = CONF.aprs_fi.apiKey

        # optional second argument is a callsign to search
        a = re.search(r"^.*\s+(.*)", message)
        if a is not None:
            searchcall = a.group(1)
            searchcall = searchcall.upper()
        else:
            # if no second argument, search for calling station
            searchcall = fromcall

        try:
            aprs_data = plugin_utils.get_aprs_fi(api_key, searchcall)
        except Exception as ex:
            LOG.error(f"Failed to fetch aprs.fi data {ex}")
            return "Failed to fetch location"

        # LOG.debug("LocationPlugin: aprs_data = {}".format(aprs_data))
        if not len(aprs_data["entries"]):
            LOG.error("Didn't get any entries from aprs.fi")
            return "Failed to fetch aprs.fi location"

        lat = aprs_data["entries"][0]["lat"]
        lon = aprs_data["entries"][0]["lng"]

        opencage_key = CONF.aprsd_timeopencage_plugin.apiKey
        try:
            geocoder = OpenCageGeocode(opencage_key)
            results = geocoder.reverse_geocode(lat, lon)
        except Exception as ex:
            LOG.error(f"Couldn't fetch opencagedata api '{ex}'")
            # Default to UTC instead
            localzone = pytz.timezone("UTC")
        else:
            tzone = results[0]["annotations"]["timezone"]["name"]
            localzone = pytz.timezone(tzone)

        return self.build_date_str(localzone)
