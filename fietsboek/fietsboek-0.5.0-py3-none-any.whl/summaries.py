"""Module for a yearly/monthly track summary."""
from typing import Dict, List

from fietsboek.models.track import TrackWithMetadata


class Summary:
    """A summary of a user's tracks.

    :ivar years: Mapping of year to :class:`YearSummary`.
    :vartype years: dict[int, YearSummary]
    """

    def __init__(self):
        self.years: Dict[int, YearSummary] = {}

    def __iter__(self):
        items = list(self.years.values())
        items.sort(key=lambda y: y.year)
        return iter(items)

    def all_tracks(self) -> List[TrackWithMetadata]:
        """Returns all tracks of the summary.

        :return: All tracks.
        """
        return [track for year in self for month in year for track in month.all_tracks()]

    def add(self, track: TrackWithMetadata):
        """Add a track to the summary.

        This automatically inserts the track into the right yearly summary.

        :param track: The track to insert.
        :type track: fietsboek.model.track.Track
        """
        year = track.date.year
        self.years.setdefault(year, YearSummary(year)).add(track)

    @property
    def total_length(self) -> float:
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        """
        return sum(track.length for track in self.all_tracks())


class YearSummary:
    """A summary over a single year.

    :ivar year: Year number.
    :ivar months: Mapping of month to :class:`MonthSummary`.
    """

    def __init__(self, year):
        self.year: int = year
        self.months: Dict[int, MonthSummary] = {}

    def __iter__(self):
        items = list(self.months.values())
        items.sort(key=lambda x: x.month)
        return iter(items)

    def all_tracks(self) -> List[TrackWithMetadata]:
        """Returns all tracks of the summary.

        :return: All tracks.
        """
        return [track for month in self for track in month]

    def add(self, track: TrackWithMetadata):
        """Add a track to the summary.

        This automatically inserts the track into the right monthly summary.

        :param track: The track to insert.
        """
        month = track.date.month
        self.months.setdefault(month, MonthSummary(month)).add(track)

    @property
    def total_length(self) -> float:
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        """
        return sum(track.length for track in self.all_tracks())


class MonthSummary:
    """A summary over a single month.

    :ivar month: Month number (1-12).
    :ivar tracks: List of tracks in this month.
    """

    def __init__(self, month):
        self.month: int = month
        self.tracks: List[TrackWithMetadata] = []

    def __iter__(self):
        items = self.tracks[:]
        items.sort(key=lambda t: t.date)
        return iter(items)

    def all_tracks(self) -> List[TrackWithMetadata]:
        """Returns all tracks of the summary.

        :return: All tracks.
        """
        return self.tracks[:]

    def add(self, track: TrackWithMetadata):
        """Add a track to the summary.

        :param track: The track to insert.
        """
        self.tracks.append(track)

    @property
    def total_length(self) -> float:
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        """
        return sum(track.length for track in self.all_tracks())
