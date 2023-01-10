import logging

from aprsd import packets, plugin
from oslo_config import cfg

import aprsd_slack_plugin
from aprsd_slack_plugin import base_plugin
from aprsd_slack_plugin import conf  # noqa


CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class SlackNotifyPlugin(
    base_plugin.SlackPluginBase,
    plugin.APRSDWatchListPluginBase,
):
    """SlackNotifyPlugin."""

    version = aprsd_slack_plugin.__version__

    def setup(self):
        config_set = self.setup_slack()
        if not config_set:
            self.enabled = False
        else:
            self.enabled = True

    def process(self, packet):
        LOG.info("SlackCommandPlugin")

        fromcall = packet.from_call
        # message = packet["message_text"]

        wl = packets.WatchList()
        if wl.is_old(fromcall):
            # get last location of a callsign, get descriptive name from weather service
            callsign_url = f"<http://aprs.fi/info/a/{fromcall}|{fromcall}>"

            message = {}
            message["username"] = "APRSD - Slack Notification Plugin"
            message["icon_emoji"] = ":satellite_antenna:"
            message["attachments"] = [{}]
            message["text"] = f"{callsign_url} - Is now on APRS"
            message["channel"] = "#hemna"

            LOG.debug(message)

            # self.swc.chat_postMessage(**message)
            for channel in self.slack_channels:
                message["channel"] = channel
                self.swc.chat_postMessage(**message)

        # Don't have aprsd try and send a reply
        return packets.NULL_MESSAGE
