from typing import List



class DintsError(Exception):
    """Base exception for all dints errors."""


class SubscriptionError(DintsError):
    """Raised when attempting to subscribe to a manager and the client was
    unable to subscribe to one or more subscriptions.
    """


class SubscriptionLimitError(DintsError):
    """Raised when attempting to subscribe to a manager with the maximum number
    of active subscribers.
    """
    def __init__(self, max_subscribers: int) -> None:
        self.max_subscribers = max_subscribers

    def __str__(self) -> str:
        return "Subscription limit reached ({})".format(self.max_subscribers)


class ClientSubscriptionError(DintsError):
    """Raised when attempting to subscribe to a manager and the client was
    unable to subscribe to one or more subscriptions. due to an unhandled exception.
    """
    def __init__(self, exc: BaseException) -> None:
        self.exc = exc

    def __str__(self) -> str:
        return "Unable to subscribe due to an unhandled exception in the client"


class FailedManager(DintsError):
    """Raised when attempting to subscribe to a manager instance that has failed
    due to an underlying exception in a background task.
    """
    def __init__(self, exc: List[BaseException]) -> None:
        self.exc = exc

    def __str__(self) -> str:
        return "Unable to subscribe due to an {} error(s) in manager".format(len(self.exc))