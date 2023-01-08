from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import datadog
import statsd


class Exporter(ABC):
    @abstractmethod
    def send(self, key: str, **extras) -> None:
        raise NotImplementedError("Provide implementation")

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError("Provide implementation")


class StatsdExporter(Exporter):
    def __init__(
        self,
        *,
        metric: Optional[str] = None,
        options,
    ):
        # TODO: use default options if not provided
        self.metric = metric
        self.statsd = statsd.StatsClient(
            host=options["statsd_host"],
            port=options["statsd_port"],
            prefix=self.metric,
        )

    def send(self, key, **extras):
        self.statsd.incr(key)

    def flush(self):
        self.statsd.close()


class DatadogExporter(Exporter):

    _DEFAULT_OPTIONS = {
        "statsd_host": "127.0.0.1",
        "statsd_port": 8125,
    }

    def __init__(
        self,
        *,
        options: Optional[Dict[str, Any]] = None,
        metric: Optional[str] = None,
        group: bool = True,
        extra_tags: Optional[List[str]] = None,
    ):
        self.options = options or self._DEFAULT_OPTIONS
        self.metric = metric
        self.group = group
        self.tags = extra_tags or []
        datadog.initialize(**self.options)
        self.statsd = datadog.statsd

    def send(self, key, **extras):
        metric = self.metric
        if not self.group:
            # NOTE: send each method as a separate metirc
            metric = f"{self.metric}.{key}"
        tags = [f"method:{key}", *self.tags]
        self.statsd.increment(metric=metric, tags=tags)

    def flush(self):
        self.statsd.flush()
