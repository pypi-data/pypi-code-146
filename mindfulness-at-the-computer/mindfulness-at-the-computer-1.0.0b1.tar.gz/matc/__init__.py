import logging

# These logging lines must be here otherwise no logging will be shown. Unknown why.
# We have to use DEBUG as the logging level, but if we start the application in normal mode
# (rather than -X dev mode) only INFO messages will be shown. Again unknown why.
logging_format_str = "%(levelname)s: %(message)s"
logging.basicConfig(format=logging_format_str, level=logging.DEBUG)
