from oslo_config import cfg

from aprsd_slack_plugin.conf import slack


CONF = cfg.CONF
slack.register_opts(CONF)
