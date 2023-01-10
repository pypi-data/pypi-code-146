import logging

from oslo_config import cfg
from slack_sdk import WebClient

import aprsd_slack_plugin


CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class SlackPluginBase:
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

        Edit your ~/.config/aprsd/aprsd.yml and add the section
        slack:
            signing_secret: <signing secret token here>
            bot_token: <Bot User OAuth Access Token here>
            channel: <channel name here>
    """

    version = aprsd_slack_plugin.__version__
    swc = None
    slack_channels = None

    def setup_slack(self):
        """Create the slack require client from config."""

        if not CONF.aprsd_slack_plugin.signing_secret:
            LOG.error("Failed to find config aprsd_slack_plugin.signing_secret")
            return "No slack signing_secret found"

        if not CONF.aprsd_slack_plugin.bot_token:
            LOG.error(
                "APRSD config is missing aprsd_slack_plugin.bot_token. "
                "Please install the slack app and get the "
                "Bot User OAth Access Token.",
            )
            return False

        if not CONF.aprsd_slack_plugin.channels:
            LOG.error("aprsd_slack_plugin.channels is missing")
            return False

        self.swc = WebClient(token=CONF.aprsd_slack_plugin.bot_token)
        self.slack_channels = CONF.aprsd_slack_plugin.channels

        return True
