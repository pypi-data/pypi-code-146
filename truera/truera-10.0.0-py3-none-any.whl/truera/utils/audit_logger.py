import datetime
import json
import logging

from prometheus_client import Counter


class AuditLogger(object):

    def __init__(
        self, service_name, log_file, emit_to_prometheus, labels
    ) -> None:
        self.service_name = service_name
        self.emit_to_prometheus = emit_to_prometheus
        if log_file:
            formatter = logging.Formatter('%(message)s')
            handler = logging.FileHandler(log_file)
            handler.setFormatter(formatter)
            self.logger = logging.getLogger(service_name)
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)
        if emit_to_prometheus:
            self.counter = Counter(
                f"audit_{service_name}",
                f"Audit events from {service_name} events.", labels
            )
            self.labels = set(labels)

    def log(self, event: dict) -> None:
        if not event:
            return
        if self.logger:
            event['service_name'] = self.service_name
            self.logger.debug(json.dumps(event))
        if self.emit_to_prometheus:
            label_values = {
                l: event[l] if l in event else "" for l in self.labels
            }
            self.counter.labels(**label_values).inc()
