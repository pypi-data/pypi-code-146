"""The Python SDK for Paloma."""

# Set default logging to avoid NoHandler warnings
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
