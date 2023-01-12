"""The Badge model."""
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import Column, Integer, LargeBinary, Text, select
from sqlalchemy.orm import relationship

from .meta import Base


class Badge(Base):
    """Represents a badge.

    Badges have a title and an image and can be defined by the admin.

    :ivar id: Database ID.
    :vartype id: int
    :ivar title: Title of the badge.
    :vartype title: str
    :ivar image: Image of the badge.
    :vartype image: bytes
    :ivar tracks: Tracks associated with this badge.
    :vartype tracks: list[fietsboek.models.track.Track]
    """

    # pylint: disable=too-few-public-methods
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    image = Column(LargeBinary)

    tracks = relationship("Track", secondary="track_badge_assoc", back_populates="badges")

    @classmethod
    def factory(cls, request):
        """Factory method to pass to a route definition.

        This factory retrieves the badge based on the ``badge_id`` matched
        route parameter, and returns the badge. If the badge is not found,
        ``HTTPNotFound`` is raised.

        :raises pyramid.httpexception.NotFound: If the badge is not found.
        :param request: The pyramid request.
        :type request: ~pyramid.request.Request
        :return: The badge.
        :type: Badge
        """
        query = select(cls).filter_by(id=request.matchdict["badge_id"])
        badge_object = request.dbsession.execute(query).scalar_one_or_none()
        if badge_object is None:
            raise HTTPNotFound()
        return badge_object
