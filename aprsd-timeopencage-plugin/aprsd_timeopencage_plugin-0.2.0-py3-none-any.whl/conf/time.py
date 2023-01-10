from oslo_config import cfg


ocd_group = cfg.OptGroup(
    name="aprsd_timeopencage_plugin",
    title="APRSD TimeOpenCage Plugin settings",
)

ocd_opts = [
    cfg.StrOpt(
        "apiKey",
        help="Your OpenCageData apiKey"
             "Information for creating your api keys is here:  "
             "https://opencagedata.com/api#quickstart",
    ),
]

ALL_OPTS = (
    ocd_opts
)


def register_opts(cfg):
    cfg.register_group(ocd_group)
    cfg.register_opts(ALL_OPTS, group=ocd_group)


def list_opts():
    return {
        ocd_group.name: ALL_OPTS,
    }
