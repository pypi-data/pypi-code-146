"""Comment model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .meta import Base


class Comment(Base):
    """Represents a comment on a track.

    :ivar id: Database ID.
    :vartype id: int
    :ivar author_id: ID of the comment's author.
    :vartype author_id: int
    :ivar track_id: ID of the track this comment belongs to.
    :vartype track_id: int
    :ivar date: Date on which the comment was made.
    :vartype date: datetime.datetime
    :ivar title: Title of the comment.
    :vartype title: str
    :ivar text: Text content of the comment.
    :vartype text: str
    :ivar author: Author of the comment.
    :vartype author: fietsboek.model.user.User
    :ivar track: Track that the comment belongs to.
    :vartype track: fietsboek.model.track.Track
    """

    # pylint: disable=too-few-public-methods
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    track_id = Column(Integer, ForeignKey("tracks.id"))
    date = Column(DateTime)
    title = Column(Text)
    text = Column(Text)

    author = relationship("User", back_populates="comments")
    track = relationship("Track", back_populates="comments")
