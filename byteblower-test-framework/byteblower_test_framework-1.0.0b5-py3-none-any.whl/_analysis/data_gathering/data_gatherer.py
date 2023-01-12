"""Containing the data gathering interface definition."""


class DataGatherer(object):
    """Data gathering interface definition."""

    __slots__ = ()

    def __init__(self) -> None:
        """Make a new data gatherer."""
        pass

    def prepare(self) -> None:
        """
        Prepare the receivers to process expected data.

        .. note::
           Virtual method.
        """
        pass

    def process(self) -> None:
        """
        .. note::
           Virtual method.
        """
        pass

    def updatestats(self) -> None:
        """
        .. note::
           Virtual method.
        """
        pass

    def summarize(self) -> None:
        """
        Store the final results.

        This can contain totals, summary, ...

        .. note::
           Virtual method.
        """
        pass
