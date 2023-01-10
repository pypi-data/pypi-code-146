import logging
import re

from aprsd import packets
from oslo_config import cfg

import aprsd_slack_plugin
from aprsd_slack_plugin import base_plugin
from aprsd_slack_plugin import conf  # noqa


CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class SlackMessagePlugin(base_plugin.SlackPluginBase):
    """SlackMessagePlugin.

    This APRSD plugin looks for the slack msg command comming in
    to aprsd, then forwards the message to the configured slack channel.

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

        Edit your ~/.config/aprsd/aprsd.yml and add the section
        slack:
            signing_secret: <signing secret token here>
            bot_token: <Bot User OAuth Access Token here>
            channel: <channel name here>
    """

    version = aprsd_slack_plugin.__version__

    # matches any string starting with h or H
    command_regex = r"^([s]|[s]\s|slack)"
    command_name = "message-slack"

    def setup(self):
        config_set = self.setup_slack()
        if not config_set:
            self.enabled = False
        else:
            self.enabled = True

    def command(self, packet):
        message = packet.message_text
        fromcall = packet.from_call
        LOG.info(f"SlackMessagePlugin '{message}'")

        # optional second argument is a callsign to search
        a = re.search(r"^.*\s+(.*)", message)
        if a is not None:
            searchcall = a.group(1)
            searchcall = searchcall.upper()
        else:
            # if no second argument, search for calling station
            searchcall = fromcall

        slack_message = {}
        slack_message["username"] = "APRSD - Slack Message Plugin"
        slack_message["icon_emoji"] = ":satellite_antenna:"
        slack_message["text"] = f"{fromcall} says {message}"
        slack_message["channel"] = "#random"

        LOG.debug(slack_message)

        self.swc.chat_postMessage(**slack_message)
        # for channel in self.slack_channels:
        #    message["channel"] = channel
        #    self.swc.chat_postMessage(**message)

        # Don't have aprsd try and send a reply
        return packets.NULL_MESSAGE
