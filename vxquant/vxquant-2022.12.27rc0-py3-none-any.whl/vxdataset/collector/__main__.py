"""数据采集器"""

import argparse
from pathlib import Path
from vxsched import vxengine, vxContext
from vxutils import logger

_default_config = {"settings": {"db": {}}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""trade agent server""")

    parser.add_argument(
        "-c",
        "--config",
        help="path to config json file",
        default="config.json",
        type=str,
    )
    parser.add_argument("-m", "--mod", help="模块存放目录", default="./mod", type=str)
    parser.add_argument(
        "-v", "--verbose", help="debug 模式", action="store_true", default=False
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel("DEBUG")

    configfile = Path(args.config)
    if configfile.exists():
        context = vxContext.load_json(configfile.as_posix(), _default_config)
    else:
        context = vxContext(_default_config)
    vxengine.initialize(context=context)

    vxengine.load_modules(args.mod)
    vxengine.serve_forever()
