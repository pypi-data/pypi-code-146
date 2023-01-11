class SmartmeterException(Exception):
    """General problem.
    Possible causes:
        - The byte stream is not as expected.
    """


class SmartmeterSerialException(SmartmeterException):
    """The com device does not respond.
    Possible causes:
        - port is empty or invalid.
        - port is already open.
        - wrong USB device.
    """


class SmartmeterTimeoutException(SmartmeterException):
    """The com device does not respond.
    Possible causes:
        - smartmeter cannot be reached.
        - smartmeter is off.
        - wrong USB device.
    """
