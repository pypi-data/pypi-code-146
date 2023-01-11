import logging

from smb3_eh_manip.util import settings

FILE_FORMAT = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"


def initialize_logging(
    file_log_level=settings.get("file_log_level", fallback="INFO"),
    console_log_level=settings.get("console_log_level", fallback="INFO"),
    filename="smb3_eh_manip.log",
):
    # set up logging to file
    logging.basicConfig(
        filename=filename, level=file_log_level, format=FILE_FORMAT, datefmt="%H:%M:%S"
    )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(console_log_level)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger("").addHandler(console)
