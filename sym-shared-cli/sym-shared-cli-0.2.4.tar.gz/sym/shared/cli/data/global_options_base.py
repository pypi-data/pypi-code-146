import inspect
import logging
from dataclasses import dataclass, replace
from typing import Optional, Sequence


@dataclass
class GlobalOptionsBase:
    debug: bool = False
    log_dir: Optional[str] = None
    disable_analytics: bool = False

    def clone(self, **kwargs):
        return replace(self, **kwargs)

    def dprint(self, *s: Sequence[str], **kwargs):
        s = list(map(str, filter(None, s)))
        if (s or kwargs) and self.debug:
            message = " ".join(s)
            if kwargs:
                message += ": " + ",".join([f"{k}={v}" for k, v in kwargs.items()])
            mod = inspect.getmodule(inspect.stack()[1][0])
            logging.getLogger(mod.__name__ if mod else __name__).info(message)

    def to_dict(self):
        return {
            "debug": self.debug,
            "log_dir": self.log_dir,
            "disable_analytics": self.disable_analytics,
        }
