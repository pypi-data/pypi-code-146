"""GPX Track model definitions.

A freshly uploaded track is stored as a :class:`Upload`, until the user
finishes putting in the extra information. This is done so that we can parse
the GPX file on the server-side and pre-fill some of the fields (such as the
date) with GPX metadata.

Once the user has finished the upload, the track is saved as a :class:`Track`.
Each track can have an associated cache that caches the computed values. This
keeps the user's metadata and the computed information separate, and allows for
example all cached data to be re-computed without interfering with the other
meta information.
"""
import datetime
import enum
import gzip
import logging
from itertools import chain
from typing import TYPE_CHECKING, List, Optional, Set, Union

from babel.numbers import format_decimal
from markupsafe import Markup
from pyramid.authorization import (
    ALL_PERMISSIONS,
    ACLAllowed,
    ACLHelper,
    Allow,
    Authenticated,
    Everyone,
)
from pyramid.httpexceptions import HTTPNotFound
from pyramid.i18n import Localizer
from pyramid.i18n import TranslationString as _
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    Table,
    Text,
    select,
)
from sqlalchemy.orm import relationship

from .. import util
from .meta import Base

if TYPE_CHECKING:
    from .. import models


LOGGER = logging.getLogger(__name__)


class Tag(Base):
    """A tag is a single keyword associated with a track.

    :ivar track_id: ID of the track that this tag belongs to.
    :vartype track_id: int
    :ivar tag: Actual text of the tag.
    :vartype tag: str
    :ivar track: The track object that this tag belongs to.
    :vartype track: Track
    """

    # pylint: disable=too-few-public-methods
    __tablename__ = "tags"
    track_id = Column(Integer, ForeignKey("tracks.id"), primary_key=True)
    tag = Column(Text, primary_key=True)

    track = relationship("Track", back_populates="tags")


class Visibility(enum.Enum):
    """An enum that represents the visibility of tracks.

    Note that the track is always visible to tagged people and via the sharing
    link.
    """

    PRIVATE = enum.auto()
    """Only the owner of the track can see it."""
    FRIENDS = enum.auto()
    """Friends of the owner can see the track as well."""
    FRIENDS_TAGGED = enum.auto()
    """Friends of the owner or friends of tagged people can see the track."""
    LOGGED_IN = enum.auto()
    """Any logged in user can see the track."""
    PUBLIC = enum.auto()
    """Anyone can see the track."""


class TrackType(enum.Enum):
    """An enum that represents the type of a track."""

    ORGANIC = enum.auto()
    """An organic track that represents a recording of a user."""

    SYNTHETIC = enum.auto()
    """A planned track that represents a route, but not an actual recording.

    This is also called a "template".
    """


track_people_assoc = Table(
    "track_people_assoc",
    Base.metadata,
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


track_badge_assoc = Table(
    "track_badge_assoc",
    Base.metadata,
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
    Column("badge_id", ForeignKey("badges.id"), primary_key=True),
)

# Some words about timezone handling in saved tracks:
# https://www.youtube.com/watch?v=-5wpm-gesOY
#
# We usually want to store the times and dates in UTC, and then convert them
# later to the user's display timezone. However, this is not quite right for
# tracks, as the time of tracks is what JSR-310 would call a "LocalDateTime" -
# that is, a date and time in the calendar without timezone information. This
# makes sense: Imagine you go on vacation and cycle at 9:00 AM, you don't want
# that to be displayed as a different time once you return. Similarly, you
# would tell "We went on a tour at 9 in the morning", not convert that time to
# the local time of where you are telling the story.
#
# We therefore save the dates of tracks as a local time, but still try to guess
# the UTC offset so that *if needed*, we can get the UTC timestamp. This is
# done by having two fields, one for the "naive" local datetime and one for the
# UTC offset in minutes. In most cases, we don't care too much about the
# offset, as long as the displayed time is alright for the user.
#
# The issue then mainly consists of getting the local time from the GPX file,
# as some of them store timestamps as UTC time. The problem of finding some
# local timestamp is delegated to util.guess_gpx_timestamp().


class Track(Base):
    """A :class:`Track` represents a single GPX track.

    The :class:`Track` object only contains the attributes that we need to
    store. Attributes and metadata that is taken from the GPX file itself is
    not stored here. Instead, a :class:`Track` has an associated
    :class:`TrackCache` object, where the computed information can be stored.

    :ivar id: Database ID.
    :vartype id: int
    :ivar owner_id: ID of the track owner.
    :vartype owner_id: int
    :ivar title: Title of the track.
    :vartype title: str
    :ivar description: Textual description of the track.
    :vartype description: str
    :ivar date_raw: Set date of the track (naive :class:`~datetime.datetime`).
    :vartype date_raw: datetime.datetime
    :ivar date_tz: Timezone offset of the locale date in minutes.
    :vartype date_tz: int
    :ivar gpx: Compressed GPX data.
    :vartype gpx: bytes
    :ivar visibility: Visibility of the track.
    :vartype visibility: Visibility
    :ivar tags: Tags of the track.
    :vartype tags: list[Tag]
    :ivar link_secret: The secret string for the share link.
    :vartype link_secret: str
    :ivar type: Type of the track
    :vartype type: TrackType
    :ivar owner: Owner of the track.
    :vartype owner: fietsboek.models.user.User
    :ivar cache: Cache for the computed track metadata.
    :vartype cache: TrackCache
    :ivar tagged_people: List of people tagged in this track.
    :vartype tagged_people: list[fietsboek.models.user.User]
    :ivar badges: Badges associated with this track.
    :vartype badges: list[fietsboek.models.badge.Badge]
    :ivar comments: Comments left on this track.
    :vartype comments: list[fietsboek.models.comment.Comment]
    :ivar images: Metadata of the images saved for this track.
    :vartype images: list[fietsboek.models.image.ImageMetadata]
    """

    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(Text)
    description = Column(Text)
    date_raw = Column(DateTime)
    date_tz = Column(Integer)
    visibility = Column(Enum(Visibility))
    link_secret = Column(Text)
    type = Column(Enum(TrackType))

    owner = relationship("User", back_populates="tracks")
    cache = relationship(
        "TrackCache", back_populates="track", uselist=False, cascade="all, delete-orphan"
    )
    tagged_people = relationship(
        "User", secondary=track_people_assoc, back_populates="tagged_tracks"
    )
    badges = relationship("Badge", secondary=track_badge_assoc, back_populates="tracks")
    tags = relationship("Tag", back_populates="track", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="track", cascade="all, delete-orphan")
    images = relationship("ImageMetadata", back_populates="track", cascade="all, delete-orphan")

    @classmethod
    def factory(cls, request):
        """Factory method to pass to a route definition.

        This factory retrieves the track based on the ``track_id`` matched
        route parameter, and returns the track. If the track is not found,
        ``HTTPNotFound`` is raised.

        :raises pyramid.httpexception.NotFound: If the track is not found.
        :param request: The pyramid request.
        :type request: ~pyramid.request.Request
        :return: The track.
        :type: Track
        """
        track_id = request.matchdict["track_id"]
        query = select(cls).filter_by(id=track_id)
        track = request.dbsession.execute(query).scalar_one_or_none()
        if track is None:
            raise HTTPNotFound()
        return track

    def __acl__(self):
        # Basic ACL: Permissions for the admin, the owner and the share link
        acl = [
            (Allow, "group:admins", ALL_PERMISSIONS),
            (
                Allow,
                f"user:{self.owner_id}",
                ["track.view", "track.edit", "track.unshare", "track.comment", "track.delete"],
            ),
            (Allow, f"secret:{self.link_secret}", "track.view"),
        ]

        # Tagged people may always see the track
        for tagged in self.tagged_people:
            acl.append((Allow, f"user:{tagged.id}", ["track.view", "track.comment"]))

        if self.visibility == Visibility.PUBLIC:
            acl.append((Allow, Everyone, "track.view"))
            acl.append((Allow, Authenticated, "track.comment"))
        elif self.visibility == Visibility.LOGGED_IN:
            acl.append((Allow, Authenticated, ["track.view", "track.comment"]))
        elif self.visibility == Visibility.FRIENDS:
            acl.extend(
                (Allow, f"user:{friend.id}", ["track.view", "track.comment"])
                for friend in self.owner.get_friends()
            )
        elif self.visibility == Visibility.FRIENDS_TAGGED:
            all_friends = (
                friend
                for person in chain([self.owner], self.tagged_people)
                for friend in person.get_friends()
            )
            acl.extend(
                (Allow, f"user:{friend.id}", ["track.view", "track.comment"])
                for friend in all_friends
            )
        return acl

    @property
    def date(self):
        """The time-zone-aware date this track has set.

        This combines the :attr:`date_raw` and :attr:`date_tz` values to
        provide a timezone aware :class:`~datetime.datetime`.

        :return: The aware datetime.
        :rtype: datetime.datetime
        """
        if self.date_tz is None:
            timezone = datetime.timezone.utc
        else:
            timezone = datetime.timezone(datetime.timedelta(minutes=self.date_tz))
        return self.date_raw.replace(tzinfo=timezone)

    @date.setter
    def date(self, value):
        if value.tzinfo is None:
            LOGGER.debug(
                "Non-aware datetime passed (track_id=%d, value=%s), assuming offset=0",
                self.id or -1,
                value,
            )
            self.date_tz = 0
        else:
            self.date_tz = value.tzinfo.utcoffset(value).total_seconds() // 60
        self.date_raw = value.replace(tzinfo=None)

    def show_organic_data(self):
        """Determines whether the organic data should be shown.

        This includes average speed, maximum speed, record start time and record end time.

        For synthetic tracks, we only show the length, uphill and downhill values.

        :return: Whether the organic data should be shown.
        :rtype: bool
        """
        return self.type == TrackType.ORGANIC

    def is_visible_to(self, user):
        """Checks whether the track is visible to the given user.

        :param request: The user.
        :type request: fietsboek.models.User
        :return: Whether the track is visible to the current user.
        :rtype: bool
        """
        principals = [Everyone]
        if user:
            principals.append(Authenticated)
            principals.extend(user.principals())
        result = ACLHelper().permits(self, principals, "track.view")
        return isinstance(result, ACLAllowed)

    def ensure_cache(self, gpx_data: Union[str, bytes]):
        """Ensure that a cached version of this track's metadata exists.

        :param gpx_data: GPX data (uncompressed) from which to build the cache.
        """
        if self.cache is not None:
            return
        self.cache = TrackCache(track=self)
        meta = util.tour_metadata(gpx_data)
        self.cache.length = meta["length"]
        self.cache.uphill = meta["uphill"]
        self.cache.downhill = meta["downhill"]
        self.cache.moving_time = meta["moving_time"]
        self.cache.stopped_time = meta["stopped_time"]
        self.cache.max_speed = meta["max_speed"]
        self.cache.avg_speed = meta["avg_speed"]
        self.cache.start_time = meta["start_time"]
        self.cache.end_time = meta["end_time"]

    def text_tags(self):
        """Returns a set of textual tags.

        :return: The tags of the track, as a set of strings.
        :rtype: set[str]
        """
        return {tag.tag for tag in self.tags}

    def add_tag(self, text):
        """Add a tag with the given text.

        If a tag with the text already exists, does nothing.

        :param text: The text of the tag.
        :type text: str
        """
        for tag in self.tags:
            if tag.tag.lower() == text.lower():
                return
        self.tags.append(Tag(tag=text))

    def remove_tag(self, text):
        """Remove the tag with the given text.

        :param text: The text of the tag to remove.
        :type text: str
        """
        for i, tag in enumerate(self.tags):
            if tag.tag.lower() == text.lower():
                break
        else:
            return
        del self.tags[i]

    def sync_tags(self, tags):
        """Syncs the track's tags with a given set of wanted tags.

        This adds and removes tags from the track as needed.

        :param tags: The wanted tags.
        :type tags: set[str]
        """
        my_tags = {tag.tag.lower() for tag in self.tags}
        lower_tags = {tag.lower() for tag in tags}
        # We cannot use the set difference methods because we want to keep the
        # capitalization of the original tags when adding them, but use the
        # lower-case version when comparing them.
        for to_add in tags:
            if to_add.lower() not in my_tags:
                self.tags.append(Tag(tag=to_add))

        to_delete = []
        for (i, tag) in enumerate(self.tags):
            if tag.tag.lower() not in lower_tags:
                to_delete.append(i)
        for i in to_delete[::-1]:
            del self.tags[i]


class TrackWithMetadata:
    """A class to add metadata to a :class:`Track`.

    This basically caches the result of :func:`fietsboek.util.tour_metadata`,
    or uses the track's cache if possible.

    Loading of the metadata is lazy on first access. The track is accessible as
    ``track``, but most attributes are proxied read-only.
    """

    # pylint: disable=too-many-public-methods

    def __init__(self, track: Track, data_manager):
        self.track = track
        self.cache = track.cache
        self.data_manager = data_manager
        self._cached_meta: Optional[dict] = None

    def _meta(self):
        # Already loaded, we're done
        if self._cached_meta:
            return self._cached_meta

        data = self.data_manager.open(self.track.id).decompress_gpx()
        self._cached_meta = util.tour_metadata(data)
        return self._cached_meta

    @property
    def length(self) -> float:
        """Returns the length of the track..

        :return: Length of the track in meters.
        """
        if self.cache is None:
            return self._meta()["length"]
        return self.cache.length

    @property
    def downhill(self) -> float:
        """Returns the downhill of the track.

        :return: Downhill in meters.
        """
        if self.cache is None:
            return self._meta()["downhill"]
        return self.cache.downhill

    @property
    def uphill(self) -> float:
        """Returns the uphill of the track.

        :return: Uphill in meters.
        """
        if self.cache is None:
            return self._meta()["uphill"]
        return self.cache.uphill

    @property
    def moving_time(self) -> datetime.timedelta:
        """Returns the moving time.

        :return: Moving time in seconds.
        """
        if self.cache is None:
            value = self._meta()["moving_time"]
        else:
            value = self.cache.moving_time
        return datetime.timedelta(seconds=value)

    @property
    def stopped_time(self) -> datetime.timedelta:
        """Returns the stopped time.

        :return: Stopped time in seconds.
        """
        if self.cache is None:
            value = self._meta()["stopped_time"]
        else:
            value = self.cache.stopped_time
        return datetime.timedelta(seconds=value)

    @property
    def max_speed(self) -> float:
        """Returns the maximum speed.

        :return: Maximum speed in meters/second.
        """
        if self.cache is None:
            return self._meta()["max_speed"]
        return self.cache.max_speed

    @property
    def avg_speed(self) -> float:
        """Returns the average speed.

        :return: Average speed in meters/second.
        """
        if self.cache is None:
            return self._meta()["avg_speed"]
        return self.cache.avg_speed

    @property
    def start_time(self) -> datetime.datetime:
        """Returns the start time.

        This is the time embedded in the GPX file, not the time in the ``date`` column.

        :return: Start time.
        """
        if self.cache is None:
            return self._meta()["start_time"]
        return self.cache.start_time

    @property
    def end_time(self) -> datetime.datetime:
        """Returns the end time.

        This is the time embedded in the GPX file, not the time in the ``date`` column.

        :return: End time.
        """
        if self.cache is None:
            return self._meta()["end_time"]
        return self.cache.end_time

    def html_tooltip(self, localizer: Localizer) -> Markup:
        """Generate a quick summary of the track as a HTML element.

        This can be used in Bootstrap tooltips.

        :param localizer: The localizer used for localization.
        :return: The generated HTML.
        """

        def number(num):
            return format_decimal(num, locale=localizer.locale_name)

        rows = [
            (_("tooltip.table.length"), f"{number(round(self.length / 1000, 2))} km"),
            (_("tooltip.table.uphill"), f"{number(round(self.uphill, 2))} m"),
            (_("tooltip.table.downhill"), f"{number(round(self.downhill, 2))} m"),
            (_("tooltip.table.moving_time"), f"{self.moving_time}"),
            (_("tooltip.table.stopped_time"), f"{self.stopped_time}"),
            (
                _("tooltip.table.max_speed"),
                f"{number(round(util.mps_to_kph(self.max_speed), 2))} km/h",
            ),
            (
                _("tooltip.table.avg_speed"),
                f"{number(round(util.mps_to_kph(self.avg_speed), 2))} km/h",
            ),
        ]
        rows = [
            f"<tr><td>{localizer.translate(name)}</td><td>{value}</td></tr>"
            for (name, value) in rows
        ]
        return Markup(f'<table>{"".join(rows)}</table>')

    # Proxied properties
    @property
    def id(self) -> int:
        """ID of the underlying track."""
        return self.track.id

    @property
    def title(self) -> str:
        """Title of the underlying track."""
        return self.track.title

    @property
    def description(self) -> str:
        """Description of the underlying track."""
        return self.track.description

    @property
    def date(self) -> datetime.datetime:
        """Date of the underlying track."""
        return self.track.date

    @property
    def visibility(self) -> Visibility:
        """Visibility of the underlying track."""
        return self.track.visibility

    @property
    def link_secret(self) -> str:
        """Link secret of the underlying track."""
        return self.track.link_secret

    @property
    def type(self) -> TrackType:
        """Type of the underlying track."""
        return self.track.type

    @property
    def owner(self) -> "models.User":
        """Owner of the undlerying track."""
        return self.track.owner

    @property
    def tagged_people(self) -> List["models.User"]:
        """Tagged people of the underlying track."""
        return self.track.tagged_people[:]

    @property
    def badges(self) -> List["models.Badge"]:
        """Badges of the underlying track."""
        return self.track.badges[:]

    @property
    def tags(self) -> List["models.Tag"]:
        """Tags of the underlying track."""
        return self.track.tags[:]

    @property
    def comments(self) -> List["models.Comment"]:
        """Comments of the underlying track."""
        return self.track.comments[:]

    @property
    def images(self) -> List["models.ImageMetadata"]:
        """Images of the underlying track."""
        return self.track.images[:]

    def text_tags(self) -> Set[str]:
        """Returns a set of textual tags.

        :return: The tags of the track, as a set of strings.
        """
        return self.track.text_tags()

    def show_organic_data(self) -> bool:
        """Proxied method :meth:`Track.show_organic_data`.

        :return: Whether the organic data should be shown.
        """
        return self.track.show_organic_data()


class TrackCache(Base):
    """Cache for computed track metadata.

    In order to repeatedly compute the track metadata from GPX files, this
    information (such as length, uphill, downhill, ...) is stored in a
    :class:`TrackCache`.

    :ivar track_id: ID of the track this cache belongs to.
    :vartype track_id: int
    :ivar length: Length of the track, in meters.
    :vartype length: float
    :ivar uphill: Uphill amount, in meters.
    :vartype uphill: float
    :ivar downhill: Downhill amount, in meters.
    :vartype downhill: float
    :ivar moving_time: Time spent moving, in seconds.
    :vartype moving_time: float
    :ivar stopped_time: Time stopped, in seconds.
    :vartype stopped_time: float
    :ivar max_speed: Maximum speed, in meters/second.
    :vartype max_speed: float
    :ivar avg_speed: Average speed, in meters/second.
    :vartype avg_speed: float
    :ivar start_time_raw: Start time of the GPX recording.
    :vartype start_time_raw: datetime.datetime
    :ivar start_time_tz: Timezone offset of the start time in minutes.
    :vartype start_time_tz: int
    :ivar end_time_raw: End time of the GPX recording.
    :vartype end_time_raw: datetime.datetime
    :ivar end_time_tz: Timezone offset of the end time in minutes.
    :vartype end_time_tz: int
    :ivar track: The track that belongs to this cache entry.
    :vartype track: Track
    """

    # pylint: disable=too-many-instance-attributes,too-few-public-methods
    __tablename__ = "track_cache"
    track_id = Column(Integer, ForeignKey("tracks.id"), primary_key=True)
    length = Column(Float)
    uphill = Column(Float)
    downhill = Column(Float)
    moving_time = Column(Float)
    stopped_time = Column(Float)
    max_speed = Column(Float)
    avg_speed = Column(Float)
    start_time_raw = Column(DateTime)
    start_time_tz = Column(Integer)
    end_time_raw = Column(DateTime)
    end_time_tz = Column(Integer)

    track = relationship("Track", back_populates="cache")

    @property
    def start_time(self):
        """The time-zone-aware start time of this track.

        :return: The aware datetime.
        :rtype: datetime.datetime
        """
        if self.start_time_tz is None:
            timezone = datetime.timezone.utc
        else:
            timezone = datetime.timezone(datetime.timedelta(minutes=self.start_time_tz))
        return self.start_time_raw.replace(tzinfo=timezone)

    @start_time.setter
    def start_time(self, value):
        if value.tzinfo is None:
            LOGGER.debug(
                "Non-aware datetime passed (cache_id=%d, value=%s), assuming offset=0",
                self.id or -1,
                value,
            )
            self.start_time_tz = 0
        else:
            self.start_time_tz = value.tzinfo.utcoffset(value).total_seconds() // 60
        self.start_time_raw = value.replace(tzinfo=None)

    @property
    def end_time(self):
        """The time-zone-aware end time of this track.

        :return: The aware datetime.
        :rtype: datetime.datetime
        """
        if self.end_time_tz is None:
            timezone = datetime.timezone.utc
        else:
            timezone = datetime.timezone(datetime.timedelta(minutes=self.end_time_tz))
        return self.end_time_raw.replace(tzinfo=timezone)

    @end_time.setter
    def end_time(self, value):
        if value.tzinfo is None:
            LOGGER.debug(
                "Non-aware datetime passed (cache_id=%d, value=%s), assuming offset=0",
                self.id or -1,
                value,
            )
            self.end_time_tz = 0
        else:
            self.end_time_tz = value.tzinfo.utcoffset(value).total_seconds() // 60
        self.end_time_raw = value.replace(tzinfo=None)


class Upload(Base):
    """A track that is currently being uploaded.

    Once a upload is done, the :class:`Upload` item is removed and a proper
    :class:`Track` is created instead.

    :ivar id: Database ID.
    :vartype id: int
    :ivar uploaded_at: Date of the upload.
    :vartype uploaded_at: datetime.datetime
    :ivar owner_id: ID of the uploader.
    :vartype owner_id: int
    :ivar gpx: Compressed GPX data.
    :vartype gpx: bytes
    :ivar owner: Uploader of this track.
    :vartype owner: fietsboek.model.user.User
    """

    # pylint: disable=too-many-instance-attributes,too-few-public-methods
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True)
    uploaded_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    gpx = Column(LargeBinary)

    owner = relationship("User", back_populates="uploads")

    @classmethod
    def factory(cls, request):
        """Factory method to pass to a route definition.

        This factory retrieves the upload based on the ``upload_id`` matched
        route parameter, and returns the upload. If the upload is not found,
        ``HTTPNotFound`` is raised.

        :raises pyramid.httpexception.NotFound: If the upload is not found.
        :param request: The pyramid request.
        :type request: ~pyramid.request.Request
        :return: The upload.
        :type: Track
        """
        query = select(cls).filter_by(id=request.matchdict["upload_id"])
        upload = request.dbsession.execute(query).scalar_one_or_none()
        if upload is None:
            raise HTTPNotFound()
        return upload

    def __acl__(self):
        return [
            (Allow, "group:admins", ALL_PERMISSIONS),
            (Allow, f"user:{self.owner_id}", "upload.finish"),
        ]

    @property
    def gpx_data(self):
        """Access the decompressed gpx data."""
        return gzip.decompress(self.gpx)

    @gpx_data.setter
    def gpx_data(self, value):
        self.gpx = gzip.compress(value)
