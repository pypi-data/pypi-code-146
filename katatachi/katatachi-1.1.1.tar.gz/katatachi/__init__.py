import logging
import os

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
)

root_logger = logging.getLogger(__name__)
root_logger.propagate = False
root_logger.setLevel(
    logging.DEBUG if os.environ.get("LOGGING_DEBUG", "false") == "true" else logging.INFO
)
root_logger.addHandler(stream_handler)

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.ERROR)
