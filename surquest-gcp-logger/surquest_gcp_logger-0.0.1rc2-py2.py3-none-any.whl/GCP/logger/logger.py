# import external packages
import os
import json
import inspect
from starlette.requests import Request
from surquest.GCP.tracer import Tracer

# import internal packages
from .json_encoder import encoder


class Logger(object):

    PROJECT = os.getenv("GCP_PROJECT_ID")
    DEFAULT_LEVEL = os.getenv("LOG_LEVEL", 200)
    LEVELS = {
        0: dict(
            name="DEFAULT",
            value=0,
            desc="The log entry has no assigned severity level.",
        ),
        100: dict(name="DEBUG", value=100, desc="Debug or trace information."),
        200: dict(
            name="INFO",
            value=200,
            desc="Routine information, such as ongoing status or performance.",
        ),
        300: dict(
            name="NOTICE",
            value=300,
            desc="Normal but significant events, such as start up, shut down, or a configuration change.",
        ),
        400: dict(
            name="WARNING",
            value=400,
            desc="Warning events might cause problems."
        ),
        500: dict(
            name="ERROR",
            value=500,
            desc="Error events are likely to cause problems."
        ),
        600: dict(
            name="CRITICAL",
            value=600,
            desc="Critical events cause more severe problems or outages.",
        ),
        700: dict(
            name="ALERT",
            value=700,
            desc="A person must take an action immediately."
        ),
        800: dict(
            name="EMERGENCY",
            value=800,
            desc="One or more systems are unusable."
        ),
    }

    def __init__(self, request: Request = None):

        self.tracer = Tracer(request=request)
        self._default_level = self.DEFAULT_LEVEL

        if os.getenv("ENVIRONMENT") in ["dev", "test"]:

            self._default_level = 0

    def log(self, severity, message: str, **context):

        severity = self.get_log_level(level=severity)

        if severity.get("value") >= self._default_level:

            entry = self._get_entry(severity=severity, message=message, **context)

            print(json.dumps(entry, sort_keys=False, default=encoder))
            return entry

    def __getattr__(self, method, message=None, context=None):

        severity = self.get_log_level(level=method).get("name")

        def temp_log(message=None, context=None):

            if context is None:
                return self.log(severity=severity, message=message, **{})
            else:
                return self.log(
                    severity=severity, message=message, context=context
                )

        return temp_log

    def _get_trace(self):

        return self.tracer.trace

    def _get_entry(self, severity, message: str, **context):

        entry = {"severity": severity.get("name"), "message": message}

        if context:
            entry["context"] = context
        if severity.get("value") >= 400:

            stack_trace = inspect.stack()

            entry["code"] = {
                "file": stack_trace[3][1],
                "lineno": stack_trace[3][2],
                "function": stack_trace[3][3],
            }
        trace = self._get_trace()
        if trace:
            entry["logging.googleapis.com/trace"] = trace
        return entry

    @classmethod
    def get_log_level_value(cls, level):
        """Method returns numeric value of given log level."""

        log_level = cls.get_log_level(level=level)

        if log_level:

            return log_level.get("value")

    @classmethod
    def raise_invalid_log_level(cls, level):
        """Method raises an error if log level is not valid value

        :param level: log level
        :type level: str

        :return: None
        :raises: ValueError
        """

        numeric_levels = list(cls.LEVELS.keys())
        alpha_levels = [cls.LEVELS.get(key).get("name") for key in numeric_levels]

        raise ValueError(
            """Invalid log level: `{level}`. Valid levels are:
            numeric values as: {numeric_levels}
            alpha values as: {alpha_levels}
        """.format(
                level=level,
                numeric_levels=", ".join([str(lvl) for lvl in numeric_levels]),
                alpha_levels=", ".join(alpha_levels),
            )
        )

    @classmethod
    def get_log_level(cls, level):
        """Method returns log level details.

        :param level: log level
        :type level: str

        :return: dictionary with log level details
        :rtype: dict
        """

        if isinstance(level, int):
            if level in list(cls.LEVELS.keys()):
                return cls.LEVELS.get(level)
        if isinstance(level, str):
            for key in cls.LEVELS.keys():
                if level.upper() == cls.LEVELS.get(key).get("name").upper():
                    return cls.LEVELS.get(key)
        cls.raise_invalid_log_level(level=level)
