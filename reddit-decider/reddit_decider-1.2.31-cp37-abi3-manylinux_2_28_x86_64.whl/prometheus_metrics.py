from prometheus_client import Counter

decider_client_counter = Counter(
    "decider_client_total",
    "Count of successful/failed Decider operations (with error_type) in reddit-decider package",
    ["operation", "success", "error_type", "pkg_version"],
)
