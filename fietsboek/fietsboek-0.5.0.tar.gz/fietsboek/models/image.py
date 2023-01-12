"""Image metadata.

The actual image data is saved on disk, we only store the metadata such as an
image description here.
"""
from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint, select
from sqlalchemy.orm import relationship

from .meta import Base


class ImageMetadata(Base):
    """Represents metadata for an uploaded image.

    :ivar id: Database ID.
    :vartype id: int
    :ivar track_id: ID of the track that this image belongs to.
    :vartype track_id: int
    :ivar image_name: Name of the image file.
    :vartype image_name: str
    :ivar description: The description that should be shown.
    :vartype description: str
    :ivar track: The track that this image belongs to.
    :vartype track: fietsboek.models.track.Track
    """

    # pylint: disable=too-few-public-methods
    __tablename__ = "image_metadata"
    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    image_name = Column(Text, nullable=False)
    description = Column(Text)

    track = relationship("Track", back_populates="images")

    __table_args__ = (UniqueConstraint("track_id", "image_name"),)

    @classmethod
    def get_or_create(cls, dbsession, track, image_name):
        """Retrieves the image metadata for the given image, or creates a new
        one if it doesn't exist.

        :param dbsession: The database session.
        :type dbsession: sqlalchemy.orm.session.Session
        :param track: The track.
        :type track: fietsboek.models.track.Track
        :param image_name: The name of the image.
        :type image_name: str
        :return: The created/retrieved object.
        :rtype: ImageMetadata
        """
        query = select(cls).filter_by(track=track, image_name=image_name)
        result = dbsession.execute(query).scalar_one_or_none()
        if result:
            return result
        return cls(track=track, image_name=image_name)
