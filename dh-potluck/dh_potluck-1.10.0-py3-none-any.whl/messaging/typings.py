from typing import Any, Dict

# See: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
# Cannot use a TypedDict easily here, see: https://github.com/python/mypy/issues/6462
ConsumerConfig = Dict[str, Any]
