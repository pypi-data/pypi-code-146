import sys
from typing import Optional, Sequence


# Buffer messages while printing, so that they can be logged once logging has been setup.
def print_and_buffer(buffer: Optional[Sequence[str]], message):
    print(message)
    if buffer is not None:
        buffer.append(message)


def handle_exception(logger, exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error(
        "Uncaught exception. (Exiting).",
        exc_info=(exc_type, exc_value, exc_traceback)
    )
