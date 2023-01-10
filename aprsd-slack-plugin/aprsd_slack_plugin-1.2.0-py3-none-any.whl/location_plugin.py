import logging
import re
import time

from aprsd import packets, plugin, plugin_utils
from oslo_config import cfg

import aprsd_slack_plugin
from aprsd_slack_plugin import base_plugin
from aprsd_slack_plugin import conf  # noqa


CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class SlackLocationPlugin(
    base_plugin.SlackPluginBase,
    plugin.APRSDRegexCommandPluginBase,
    plugin.APRSFIKEYMixin,
):
    """SlackCommandPlugin.

    This APRSD plugin looks for the location command comming in
    to aprsd, then fetches the caller's location, and then reports
    that location string to the configured slack channel.

    To use this:
        Create a slack bot for your workspace at api.slack.com.
        A good source of information on how to create the app
        and the tokens and permissions and install the app in your
        workspace is here:

            https://api.slack.com/start/building/bolt-python


        You will need the signing secret from the
        Basic Information -> App Credentials form.
        You will also need the Bot User OAuth Access Token from
        OAuth & Permissions -> OAuth Tokens for Your Team ->
        Bot User OAuth Access Token.

        Install the app/bot into your workspace.

        Edit your ~/.config/aprsd/aprsd.conf and add the section
        slack:
            signing_secret: <signing secret token here>
            bot_token: <Bot User OAuth Access Token here>
            channel: <channel name here>
    """

    version = aprsd_slack_plugin.__version__

    # matches any string starting with h or H
    command_regex = "^[lL]"
    command_name = "location-slack"

    def setup(self):
        self.ensure_aprs_fi_key()
        if self.enabled:
            config_set = self.setup_slack()
            if not config_set:
                self.enabled = False

    def process(self, packet):
        LOG.info("SlackCommandPlugin")

        fromcall = packet.from_call
        message = packet.message_text

        # get last location of a callsign, get descriptive name from weather service
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
            LOG.error(f"Failed to fetch aprs.fi '{ex}'")
            return "Failed to fetch aprs.fi location"

        LOG.debug(f"LocationPlugin: aprs_data = {aprs_data}")
        if not len(aprs_data["entries"]):
            LOG.error("Didn't get any entries from aprs.fi")
            return "Failed to fetch aprs.fi location"

        lat = aprs_data["entries"][0]["lat"]
        lon = aprs_data["entries"][0]["lng"]
        try:  # altitude not always provided
            alt = float(aprs_data["entries"][0]["altitude"])
        except Exception:
            alt = 0
        altfeet = int(alt * 3.28084)
        aprs_lasttime_seconds = aprs_data["entries"][0]["lasttime"]
        delta_seconds = time.time() - int(aprs_lasttime_seconds)
        delta_hours = delta_seconds / 60 / 60

        wx_data = None
        try:
            wx_data = plugin_utils.get_weather_gov_for_gps(lat, lon)
        except Exception:
            LOG.warning("Couldn't fetch forecast.weather.gov")

        callsign_url = f"<http://aprs.fi/info/a/{searchcall}|{searchcall}>"

        aprs_url = "<http://aprs.fi/#!mt=roadmap&z=15&lat={}&lng={}|" " http://aprs.fi/>".format(
            lat,
            lon,
        )

        message = {}
        message["username"] = "APRSD - Slack Location Plugin"
        message["icon_emoji"] = ":satellite_antenna:"
        message["attachments"] = [{}]
        message["text"] = f"{callsign_url} - Location"
        message["channel"] = "#random"

        attachment = message["attachments"][0]
        attachment["fallback"] = message["text"]
        attachment["fields"] = []

        # if the coordinates are outside of the US, we don't get this
        # aread description
        if wx_data and "location" in wx_data and "areaDescription" in wx_data["location"]:
            attachment["fields"].append(
                {
                    "title": "Location",
                    "value": wx_data["location"]["areaDescription"],
                    "short": True,
                },
            )

        attachment["fields"].append(
            {"title": "Map Location", "value": aprs_url, "short": True},
        )
        attachment["fields"].append(
            {
                "title": "Altitude",
                "value": altfeet,
                "short": True,
                "fallback": f"Altitude - {altfeet}",
            },
        )
        attachment["fields"].append(
            {
                "title": "Time",
                "value": f"{round(delta_hours, 1)} h ago",
                "short": True,
                "fallback": f"Time {round(delta_hours, 1)} h ago",
            },
        )

        LOG.debug(message)

        # self.swc.chat_postMessage(**message)
        for channel in self.slack_channels:
            message["channel"] = channel
            self.swc.chat_postMessage(**message)

        # Don't have aprsd try and send a reply
        return packets.NULL_MESSAGE
