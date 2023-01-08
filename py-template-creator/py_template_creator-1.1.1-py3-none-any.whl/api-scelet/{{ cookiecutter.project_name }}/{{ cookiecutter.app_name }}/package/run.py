from mrkutil.logging import get_logging_config

from uvicorn import run
import os
import logging
import logging.config


log_level = os.getenv("LOG_LEVEL", "DEBUG")
develop = bool('true' == str(os.getenv("DEVELOP", 'false')).lower())
json_format = bool('true' == str(os.getenv("JSON_FORMAT", 'false')).lower())

logging_config = get_logging_config(log_level, json_format, True)
logger = logging.getLogger("main")


def dev():
    run("package.app.start:app", host="0.0.0.0", port=8080, reload=True, log_level=log_level.lower(), log_config=logging_config)


def prod():
    run(
        "package.app.start:app",
        headers=[
            ("server", "Apache"),
            ("X-Frame-Options", "SAMEORIGIN"),
            ("X-XSS-Protection", "1; mode=block"),
            ("X-Content-Type-Options", "nosniff"),
            ("Strict-Transport-Security", "max-age=15768000; includeSubDomains"),
            ("Referrer-Policy", "no-referrer-when-downgrade"),
            ("Content-Security-Policy", "frame-ancestors 'self'"),
        ],
        host="0.0.0.0",
        port=80,
        log_level=log_level.lower(),
        log_config=logging_config,
        forwarded_allow_ips="*"
    )


if __name__ == "__main__":
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    dev()
