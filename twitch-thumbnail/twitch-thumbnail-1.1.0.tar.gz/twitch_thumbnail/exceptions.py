class NoStreamError(Exception):
    def __init__(self, channel: str):
        self.channel = channel

    def __str__(self):
        return f"Channel {self.channel} has no stream."


class AttemptsExceededError(Exception):
    def __init__(self, attempts: int):
        self.attempts = attempts

    def __str__(self):
        return f"Exceeded {self.attempts} attempts."


class AuthError(Exception):
    pass
