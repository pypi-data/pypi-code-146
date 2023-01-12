"""Views for browsing all tracks."""
import datetime
from io import RawIOBase
from typing import List
from zipfile import ZIP_DEFLATED, ZipFile

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import func, or_, select
from sqlalchemy.orm import aliased

from .. import models, util
from ..models.track import TrackType, TrackWithMetadata


class Stream(RawIOBase):
    """A :class:`Stream` represents an in-memory buffered FIFO.

    This is useful for the zipfile module, as it needs a file-like object, but
    we do not want to create an actual temporary file.
    """

    def __init__(self):
        super().__init__()
        self.buffer = []

    def write(self, b):
        self.buffer.append(b)
        return len(b)

    def readall(self):
        buf = self.buffer
        self.buffer = []
        return b"".join(buf)


def _get_int(request, name):
    try:
        return int(request.params.get(name))
    except ValueError as exc:
        raise HTTPBadRequest(f"Invalid integer in {name!r}") from exc


def _get_date(request, name):
    try:
        return datetime.date.fromisoformat(request.params.get(name))
    except ValueError as exc:
        raise HTTPBadRequest(f"Invalid date in {name!r}") from exc


def _get_enum(enum, value):
    try:
        return enum[value]
    except KeyError as exc:
        raise HTTPBadRequest(f"Invalid enum value {value!r}") from exc


class Filter:
    """A class representing a filter that the user can apply to the track list."""

    def compile(self, query, track, track_cache):
        """Compile the filter into the SQL query.

        Returns the modified query.

        This method is optional, as a pure-Python filtering can be done via
        :meth:`apply`.

        :param query: The original query to be modified, selecting over all tracks.
        :param track: The track mapper.
        :param track_cache: The track cache mapper.
        :return: The modified query.
        """
        # pylint: disable=unused-argument
        return query

    def apply(self, track):
        """Check if the given track matches the filter.

        :param track: The track to check.
        :return: ``True`` if the track matches.
        """
        raise NotImplementedError


class LambdaFilter(Filter):
    """A :class:`Filter` that works by provided lambda functions."""

    def __init__(self, compiler, matcher):
        self.compiler = compiler
        self.matcher = matcher

    def compile(self, query, track, track_cache):
        return self.compiler(query, track, track_cache)

    def apply(self, track):
        return self.matcher(track)


class SearchFilter(Filter):
    """A :class:`Filter` that looks for the given search terms."""

    def __init__(self, search_terms):
        self.search_terms = search_terms

    def compile(self, query, track, track_cache):
        for term in self.search_terms:
            term = term.lower()
            query = query.where(func.lower(track.title).contains(term))
        return query

    def apply(self, track):
        return all(term.lower() in track.title.lower() for term in self.search_terms)


class TagFilter(Filter):
    """A :class:`Filter` that looks for the given tags."""

    def __init__(self, tags):
        self.tags = tags

    def compile(self, query, track, track_cache):
        lower_tags = [tag.lower() for tag in self.tags]
        for tag in lower_tags:
            exists_query = (
                select(models.Tag)
                .where(models.Tag.track_id == track.id)
                .where(func.lower(models.Tag.tag) == tag)
                .exists()
            )
            query = query.where(exists_query)
        return query

    def apply(self, track):
        lower_track_tags = {tag.lower() for tag in track.text_tags()}
        lower_tags = {tag.lower() for tag in self.tags}
        return all(tag in lower_track_tags for tag in lower_tags)


class PersonFilter(Filter):
    """A :class:`Filter` that looks for the given tagged people, based on their name."""

    def __init__(self, names):
        self.names = names

    def compile(self, query, track, track_cache):
        lower_names = [name.lower() for name in self.names]
        for name in lower_names:
            tpa = models.track.track_people_assoc
            exists_query = (
                select(tpa)
                .join(models.User, tpa.c.user_id == models.User.id)
                .where(tpa.c.track_id == track.id)
                .where(func.lower(models.User.name) == name)
                .exists()
            )
            is_owner = (
                select(models.User.id)
                .where(models.User.id == track.owner_id)
                .where(func.lower(models.User.name) == name)
                .exists()
            )
            query = query.where(or_(exists_query, is_owner))
        return query

    def apply(self, track):
        lower_names = {person.name.lower() for person in track.tagged_people}
        lower_names.add(track.owner.name.lower())
        return all(name.lower() in lower_names for name in self.names)


class UserTaggedFilter(Filter):
    """A :class:`Filter` that looks for a specific user to be tagged."""

    def __init__(self, user):
        self.user = user

    def compile(self, query, track, track_cache):
        tpa = models.track.track_people_assoc
        return query.where(
            or_(
                track.owner == self.user,
                (
                    select(tpa)
                    .where(tpa.c.track_id == track.id)
                    .where(tpa.c.user_id == self.user.id)
                    .exists()
                ),
            )
        )

    def apply(self, track):
        return track.owner == self.user or self.user in track.tagged_people


class FilterCollection(Filter):
    """A class that applies multiple :class:`Filter`."""

    def __init__(self, filters):
        self._filters = filters

    def __bool__(self):
        return bool(self._filters)

    def compile(self, query, track, track_cache):
        for filty in self._filters:
            query = filty.compile(query, track, track_cache)
        return query

    def apply(self, track):
        return all(filty.apply(track) for filty in self._filters)

    @classmethod
    def parse(cls, request):
        """Parse the filters from the given request.

        :raises HTTPBadRequest: If the filters are malformed.
        :param request: The request.
        :type request: pyramid.request.Request
        :return: The parsed filter.
        :rtype: FilterCollection
        """
        # pylint: disable=singleton-comparison
        filters: List[Filter] = []
        if request.params.get("search-terms"):
            term = request.params.get("search-terms").strip()
            filters.append(SearchFilter([term]))

        if request.params.get("tags"):
            tags = [tag.strip() for tag in request.params.get("tags").split("&&")]
            tags = list(filter(bool, tags))
            filters.append(TagFilter(tags))

        if request.params.get("tagged-person"):
            names = [name.strip() for name in request.params.get("tagged-person").split("&&")]
            names = list(filter(bool, names))
            filters.append(PersonFilter(names))

        if request.params.get("min-length"):
            # Value is given in km, so convert it to m
            min_length = _get_int(request, "min-length") * 1000
            filters.append(
                LambdaFilter(
                    lambda query, track, track_cache: query.where(
                        or_(
                            track_cache.length >= min_length,
                            track_cache.length == None,  # noqa: E711
                        )
                    ),
                    lambda track: track.length >= min_length,
                )
            )

        if request.params.get("max-length"):
            max_length = _get_int(request, "max-length") * 1000
            filters.append(
                LambdaFilter(
                    lambda query, track, track_cache: query.where(
                        or_(
                            track_cache.length <= max_length,
                            track_cache.length == None,  # noqa: E711
                        )
                    ),
                    lambda track: track.length <= max_length,
                )
            )

        if request.params.get("min-date"):
            min_date = _get_date(request, "min-date")
            min_date = datetime.datetime.combine(min_date, datetime.time.min)
            filters.append(
                LambdaFilter(
                    lambda query, track, track_cache: query.where(track.date_raw >= min_date),
                    lambda track: track.date.replace(tzinfo=None) >= min_date,
                )
            )

        if request.params.get("max-date"):
            max_date = _get_date(request, "max-date")
            max_date = datetime.datetime.combine(max_date, datetime.time.max)
            filters.append(
                LambdaFilter(
                    lambda query, track, track_cache: query.where(track.date_raw <= max_date),
                    lambda track: track.date.replace(tzinfo=None) <= max_date,
                )
            )

        if "mine" in request.params.getall("show-only[]"):
            filters.append(
                LambdaFilter(
                    lambda query, track, track_cache: query.where(track.owner == request.identity),
                    lambda track: track.owner == request.identity,
                )
            )

        if "friends" in request.params.getall("show-only[]") and request.identity:
            friend_ids = {friend.id for friend in request.identity.get_friends()}
            filters.append(
                LambdaFilter(
                    lambda query, track, track_cache: query.where(track.owner_id.in_(friend_ids)),
                    lambda track: track.owner in request.identity.get_friends(),
                )
            )

        if "user-tagged" in request.params.getall("show-only[]") and request.identity:
            filters.append(UserTaggedFilter(request.identity))

        if "type[]" in request.params:
            types = {_get_enum(TrackType, value) for value in request.params.getall("type[]")}
            filters.append(
                LambdaFilter(
                    lambda query, track, track_cache: query.where(track.type.in_(types)),
                    lambda track: track.type in types,
                )
            )

        return cls(filters)


@view_config(
    route_name="browse", renderer="fietsboek:templates/browse.jinja2", request_method="GET"
)
def browse(request):
    """Returns the page that lets a user browse all visible tracks.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    filters = FilterCollection.parse(request)
    track = aliased(models.Track, models.User.visible_tracks_query(request.identity).subquery())

    # Build our query
    query = select(track).join(models.TrackCache, isouter=True)
    query = filters.compile(query, track, models.TrackCache)
    query = query.order_by(track.date_raw.desc())

    tracks = request.dbsession.execute(query).scalars()
    tracks = (TrackWithMetadata(track, request.data_manager) for track in tracks)
    tracks = [track for track in tracks if filters.apply(track)]
    return {
        "tracks": tracks,
        "mps_to_kph": util.mps_to_kph,
        "used_filters": bool(filters),
    }


@view_config(route_name="track-archive", request_method="GET")
def archive(request):
    """Packs multiple tracks into a single archive.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    track_ids = set(map(int, request.params.getall("track_id[]")))
    tracks = (
        request.dbsession.execute(select(models.Track).filter(models.Track.id.in_(track_ids)))
        .scalars()
        .fetchall()
    )

    if len(tracks) != len(track_ids):
        return HTTPNotFound()

    for track in tracks:
        if not track.is_visible_to(request.identity):
            return HTTPForbidden()

    def generate():
        stream = Stream()
        with ZipFile(stream, "w", ZIP_DEFLATED) as zipfile:  # type: ignore
            for track_id in track_ids:
                data = request.data_manager.open(track_id).decompress_gpx()
                zipfile.writestr(f"track_{track_id}.gpx", data)
                yield stream.readall()
        yield stream.readall()

    return Response(
        app_iter=generate(),
        content_type="application/zip",
        content_disposition="attachment; filename=tracks.zip",
    )
