# Goal: express errors returned from the SpikeSafe error queue as Python exceptions

class SpikeSafeError(Exception):
    """Exception raised for SpikeSafe errors returned by the SYSTem:ERRor? query

    Attributes:
        code  : int
            numerical code representing the specific SpikeSafe error
        message : string
            explanation of the SpikeSafe error
        channel_list : int[]
            a list of channels affected by a given error (if applicable)
        full_error
            the full error query response text
    """
    code = 0

    message = None

    channel_list = []

    full_error = None

    def __init__(self, code, message, channel_list = [], full_error = None):
        self.code = code
        self.message = message
        self.channel_list = channel_list
        self.full_error = full_error

    def __str__(self):
        if self.full_error:
            return "SpikeSafe Error: {}".format(self.full_error)
        else:
            return "SpikeSafe Error: {}".format(self.message)