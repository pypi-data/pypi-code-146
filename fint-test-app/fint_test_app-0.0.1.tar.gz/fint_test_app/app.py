#  Copyright (c) 2023 actfint
#  Licensed under the BSD 3-Clause License
#  Created by @Wh1isper 2023/1/8
import logging

from fps.app import create_app as fps_create_app
from fps.logging import configure_loggers


def create_app():
    app = fps_create_app()
    configure_loggers(logging.root.manager.loggerDict.keys(), "warning")
    configure_loggers(
        (k for k in logging.root.manager.loggerDict.keys() if k.startswith("fint")), "debug"
    )
    return app
