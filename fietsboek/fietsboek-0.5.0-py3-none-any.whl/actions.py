"""High-level actions.

This module implements the basic logic for high level intents such as "add a
track", "delete a track", ... It combines the low-level APIs of the ORM and the
data manager, and provides functions that can be used by the views, the API and
the test functions.
"""
import datetime
import logging
import re
from typing import List

from pyramid.request import Request
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from fietsboek import models, util
from fietsboek.data import DataManager
from fietsboek.models.track import TrackType, Visibility

LOGGER = logging.getLogger(__name__)


def add_track(
    dbsession: Session,
    data_manager: DataManager,
    owner: models.User,
    title: str,
    date: datetime.datetime,
    visibility: Visibility,
    track_type: TrackType,
    description: str,
    badges: List[models.Badge],
    tagged_people: List[models.User],
    tags: List[str],
    gpx_data: bytes,
) -> models.Track:
    """Adds a track to the database.

    Note that this function does not do any authorization checking, and as
    such, expects the caller to ensure that everything is in order.

    Most of the parameters correspond to the attributes of
    :class:`~fietsboek.models.track.Track` objects.

    :param dbsession: The database session.
    :param data_manager: The data manager.
    :param owner: The owner of the track.
    :param title: Title of the track.
    :param date: Date of the track, should be timezone-aware.
    :param visibility: Track visibility.
    :param track_type: Type of the track.
    :param description: Track description.
    :param badges: Badges to attach to the track.
    :param tagged_people: List of people to tag.
    :param tags: List of text tags for the track.
    :param gpx_data: Actual GPX data (uncompressed, straight from the source).
    :return: The track object that has been inserted into the database. Useful
        for its ``id`` attribute.
    """
    # pylint: disable=too-many-arguments
    LOGGER.debug("Inserting new track...")
    track = models.Track(
        owner=owner,
        title=title,
        visibility=visibility,
        type=track_type,
        description=description,
        badges=badges,
        link_secret=util.random_link_secret(),
        tagged_people=tagged_people,
    )
    track.date = date
    track.sync_tags(tags)
    dbsession.add(track)
    dbsession.flush()

    # Best time to build the cache is right after the upload
    track.ensure_cache(gpx_data)
    dbsession.add(track.cache)

    # Save the GPX data
    LOGGER.debug("Creating a new data folder for %d", track.id)
    manager = data_manager.initialize(track.id)
    LOGGER.debug("Saving GPX to %s", manager.gpx_path())
    manager.compress_gpx(gpx_data)
    manager.backup()

    manager.engrave_metadata(
        title=track.title,
        description=track.description,
        author_name=track.owner.name,
        time=track.date,
    )

    return track


def edit_images(request: Request, track: models.Track):
    """Edit the images according to the given request.

    This deletes and adds images and image descriptions as needed, based on the
    ``image[...]`` and ``image-description[...]`` fields.

    :param request: The request.
    :param track: The track to edit.
    """
    LOGGER.debug("Editing images for %d", track.id)
    manager = request.data_manager.open(track.id)

    # Delete requested images
    for image in request.params.getall("delete-image[]"):
        manager.delete_image(image)
        image_meta = request.dbsession.execute(
            select(models.ImageMetadata).filter_by(track_id=track.id, image_name=image)
        ).scalar_one_or_none()
        LOGGER.debug("Deleted image %s %s (metadata: %s)", track.id, image, image_meta)
        if image_meta:
            request.dbsession.delete(image_meta)

    # Add new images
    set_descriptions = set()
    for param_name, image in request.params.items():
        match = re.match("image\\[(\\d+)\\]$", param_name)
        if not match:
            continue
        # Sent for the multi input
        if image == b"":
            continue

        upload_id = match.group(1)
        image_name = manager.add_image(image.file, image.filename)
        image_meta = models.ImageMetadata(track=track, image_name=image_name)
        image_meta.description = request.params.get(f"image-description[{upload_id}]", "")
        request.dbsession.add(image_meta)
        LOGGER.debug("Uploaded image %s %s", track.id, image_name)
        set_descriptions.add(upload_id)

    images = manager.images()
    # Set image descriptions
    for param_name, description in request.params.items():
        match = re.match("image-description\\[(.+)\\]$", param_name)
        if not match:
            continue
        image_id = match.group(1)
        # Descriptions that we already set while adding new images can be
        # ignored
        if image_id in set_descriptions:
            continue
        # Did someone give us a wrong ID?!
        if image_id not in images:
            LOGGER.info("Got a ghost image description for track %s: %s", track.id, image_id)
            continue
        image_meta = models.ImageMetadata.get_or_create(request.dbsession, track, image_id)
        image_meta.description = description
        request.dbsession.add(image_meta)
