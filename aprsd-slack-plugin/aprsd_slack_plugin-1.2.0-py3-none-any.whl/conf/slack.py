from oslo_config import cfg


slack_group = cfg.OptGroup(
    name="aprsd_slack_plugin",
    title="APRSD Slack Plugin settings",
)

slack_opts = [
    cfg.StrOpt(
        "signing_secret",
        default=None,
        help="Your Slack account signing secret"
        "You have to create a slack bot account first.  "
        "https://api.slack.com/start/building/bolt-python",
    ),
    cfg.StrOpt(
        "bot_token",
        default=None,
        help="Your Slack bot's token",
    ),
    cfg.ListOpt(
        "channels",
        default=None,
        help="The channels you want messages sent to. This is a CSV list"
        "of slack channel names.",
    ),
]

ALL_OPTS = slack_opts


def register_opts(cfg):
    cfg.register_group(slack_group)
    cfg.register_opts(ALL_OPTS, group=slack_group)


def list_opts():
    return {
        slack_group.name: slack_opts,
    }
