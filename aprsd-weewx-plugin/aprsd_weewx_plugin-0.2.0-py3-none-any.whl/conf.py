from oslo_config import cfg

weewx_group = cfg.OptGroup(name="weewx-plugin",
                           title="APRSD Weewx Plugin settings")

weewx_opts = [
    cfg.FloatOpt(
        'latitude',
        default=None,
        help="Latitude of the station you want to report as"
    ),
    cfg.FloatOpt(
        'longitude',
        default=None,
        help="Longitude of the station you want to report as"
    ),
    cfg.IntOpt(
        'report_interval',
        default=60,
        help="How long (in seconds) in between weather reports"
    ),
]

weewx_mqtt_opts = [
    cfg.StrOpt(
        'mqtt_user',
        help="MQTT username"
    ),
    cfg.StrOpt(
        'mqtt_password',
        help="MQTT password"
    ),
    cfg.HostnameOpt(
        "mqtt_host",
        help="MQTT Hostname to connect to"
    ),
    cfg.PortOpt(
        "mqtt_port",
        help="MQTT Port"
    )
]


def register_opts(cfg):
    cfg.register_group(weewx_group)
    cfg.register_opts(weewx_opts, group=weewx_group)
    cfg.register_opts(weewx_mqtt_opts, group=weewx_group)


def list_opts():
    return [
        weewx_group.name: (
            weewx_opts +
            weewx_mqtt_opts
        )
    ]
