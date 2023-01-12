class EloquaException(Exception):

    def __init__(self, reason, text):
        self.reason = reason
        self.text = text

    def __str__(self):
        return "Eloqua API Error: {}, reason: {}".format(
            self.text, self.reason)
