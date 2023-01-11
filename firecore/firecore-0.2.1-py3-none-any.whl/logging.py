import sys
import structlog
import logging.config
import logging

from typing import Optional


def init(filename: Optional[str] = None, level: str = "INFO"):
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.ExtraAdder(),
        timestamper
    ]

    handlers = {
        "default": {
            "level": level,
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    }

    if filename:
        handlers['file'] = {
            "level": level,
            "class": "logging.handlers.WatchedFileHandler",
            "filename": filename,
            "formatter": "json",
        }

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.processors.JSONRenderer(),
                ],
                "foreign_pre_chain": pre_chain,
            },
            "console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                ] + _get_console_output_processors(),
                "foreign_pre_chain": pre_chain,
            }
        },
        "handlers": handlers,
        "loggers": {
            "": {
                "handlers": ["default"] if not filename else ["default", "file"],
                "level": level,
                "propagate": True,
            }
        }
    })

    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def _get_console_output_processors():
    if sys.stderr.isatty():
        processors = [
            structlog.dev.ConsoleRenderer()
        ]
    else:
        processors = [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ]

    return processors


def get_logger(*args, **kwargs) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(*args, **kwargs)
