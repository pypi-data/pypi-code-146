import json
import logging
import sys
import threading
from datetime import datetime, timezone
from logging import Filter, Formatter, Logger, LogRecord
from typing import Any, Dict, Optional

import ulid

ContextDict = Dict[str, Any]
CONTEXT_KEY = "_thread_logging_context"

_thread_storage = threading.local()
_process_context: ContextDict = {}


class ContextLogger(Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._thread_storage = _thread_storage

    @property
    def context_id(self) -> Optional[str]:
        return self.context.get("context_id")

    # Process context

    @property
    def context(self) -> ContextDict:
        if not _process_context:
            self.reset_context()
        return {**_process_context, **self.thread_context}

    @classmethod
    def update_context(cls, **kwargs) -> ContextDict:
        _process_context.update(kwargs)
        return _process_context

    @classmethod
    def set_context(cls, context: Optional[ContextDict] = None, **kwargs) -> ContextDict:
        context = context or {}
        if "context_id" not in context:
            context = {"context_id": ulid.new().str, **context}  # Always keep context_id first.
        _process_context.clear()
        return cls.update_context(**context, **kwargs)

    @classmethod
    def reset_context(cls) -> ContextDict:
        return cls.set_context({})

    # Thread context

    @property
    def thread_context(self) -> ContextDict:
        current_context = getattr(self._thread_storage, CONTEXT_KEY, None)
        if current_context is None:
            return self.reset_thread_context()
        return current_context

    def update_thread_context(self, **kwargs) -> ContextDict:
        new_context = self.thread_context
        new_context.update(kwargs)
        return self.set_thread_context(new_context)

    def set_thread_context(self, context: ContextDict) -> ContextDict:
        setattr(self._thread_storage, CONTEXT_KEY, context)
        return context

    def reset_thread_context(self) -> ContextDict:
        return self.set_thread_context({})

    # Logging

    def _log(self, *args, **kwargs) -> None:
        extra = kwargs.get("extra")
        kwargs["extra"] = {"extra": extra, "context": self.context}
        super()._log(*args, **kwargs)  # noqa


class ContextFormatter(Formatter):
    def __init__(self, *args, log_extra: bool = True, log_context: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_extra = log_extra
        self.log_context = log_context

    def format(self, record: LogRecord) -> str:
        message = original_message = record.msg
        extra = getattr(record, "extra", None)
        context = getattr(record, "context", None)
        message = str(message)
        if extra and self.log_extra:
            message += f" | {extra}"
        if context and self.log_context:
            message += f" | {context}"
        record.msg = message
        result = super().format(record)
        record.msg = original_message
        return result


class JsonFormatter(Formatter):
    def __init__(self, *args, indented: bool = False, tz: Optional[timezone] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.indent = 2 if indented else None
        self.tz = tz or datetime.now().astimezone().tzinfo

    def format(self, record: LogRecord) -> str:
        record_data = {
            # Base
            "date_time": self._format_date_time(record.created),
            "level": record.levelname,
            "message": super().format(record),
            "extra": getattr(record, "extra", None),
            "context": getattr(record, "context", None),
            # Debug
            "func_name": record.funcName,
            "file_path": record.pathname,
            "line_number": record.lineno,
            # More
            "level_code": record.levelno,
            "timestamp": record.created,
            "logger": record.name,
            "thread_name": record.threadName,
        }
        try:
            return json.dumps(record_data, indent=self.indent, ensure_ascii=False)
        except Exception as e:  # noqa
            log.debug(f"Record serialization failed: {e}")
            return str(record_data)

    def _format_date_time(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, self.tz).isoformat(sep=" ", timespec="milliseconds")


class LevelRangeFilter(Filter):
    def __init__(self, low=0, high=100):
        Filter.__init__(self)
        self.low = low
        self.high = high

    def filter(self, record):
        if self.low <= record.levelno < self.high:
            return True
        return False


def get_logger(name: str) -> ContextLogger:
    return logging.getLogger(name)  # type: ignore


def wrap(o: object) -> str:
    return f"[{o}]"


def get_dict_config(
    *,
    std_formatter: str = "json",
    root_log_level: str = "DEBUG",
    indent_json: bool = False,
    extra_handlers: dict = None,
    extra_loggers: dict = None,
) -> dict:
    dict_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "()": "the_spymaster_util.logging.ContextFormatter",
                "format": "[%(asctime)s.%(msecs)03d] [%(levelname)-.4s]: %(message)s [%(name)s]",
                "datefmt": "%H:%M:%S",
                "log_context": False,
            },
            "debug": {
                "class": "the_spymaster_util.logging.ContextFormatter",
                "format": "[%(asctime)s.%(msecs)03d] [%(levelname)-.4s]: %(message)s @@@ "
                "[%(name)s:%(lineno)s] [%(threadName)s]",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "the_spymaster_util.logging.JsonFormatter",
                "indented": indent_json,
            },
        },
        "filters": {
            "std_filter": {"()": "the_spymaster_util.logging.LevelRangeFilter", "high": logging.WARNING},
            "err_filter": {"()": "the_spymaster_util.logging.LevelRangeFilter", "low": logging.WARNING},
        },
        "handlers": {
            "console_out": {
                "class": "logging.StreamHandler",
                "filters": ["std_filter"],
                "formatter": std_formatter,
                "stream": sys.stdout,
            },
            "console_err": {
                "class": "logging.StreamHandler",
                "filters": ["err_filter"],
                "formatter": std_formatter,
                "stream": sys.stderr,
            },
        },
        "root": {"handlers": ["console_out", "console_err"], "level": root_log_level},
        "loggers": {},
    }
    if extra_handlers:
        dict_config["handlers"].update(extra_handlers)  # type: ignore
    if extra_loggers:
        dict_config["loggers"].update(extra_loggers)  # type: ignore
    return dict_config


logging.setLoggerClass(ContextLogger)
log = get_logger(__name__)
