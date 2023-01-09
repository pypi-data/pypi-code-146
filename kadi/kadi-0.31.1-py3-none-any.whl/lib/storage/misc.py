# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import current_app
from PIL import Image

import kadi.lib.constants as const
from .local import LocalStorage


def create_misc_storage(max_size=None):
    """Create a local storage that can be used for miscellaneous uploads.

    Will use the local path set in ``MISC_UPLOADS_PATH`` in the application's
    configuration as root directory for the storage and two directories of length 2 for
    all generated file paths via :meth:`.LocalStorage.create_filepath`.

    :param max_size: (optional) See :class:`.BaseStorage`.
    :return: The storage.
    """
    return LocalStorage(
        root_directory=current_app.config["MISC_UPLOADS_PATH"],
        max_size=max_size,
        num_dirs=2,
    )


def save_as_thumbnail(image_identifier, file_object, max_resolution=(512, 512)):
    """Save an image file as JPEG thumbnail.

    Uses the local storage as returned by :func:`create_misc_storage` to store the
    thumbnails with a maximum size given by ``IMAGES_MAX_SIZE`` as defined in the
    application's configuration.

    :param image_identifier: An identifier of the image suitable for an actual file name
        using :meth:`.LocalStorage.create_filepath`.
    :param file_object: The binary image file object. The image must be of one of the
        image types specified in :const:`kadi.lib.constants.IMAGE_MIMETYPES`.
    :param max_resolution: (optional) The maximum resolution of the thumbnail in pixels.
    :return: ``True`` if the thumbnail was saved successfully, ``False`` otherwise. Note
        that the original image file may be saved regardless of whether the thumbnail
        could be generated from it or not.
    """
    storage = create_misc_storage(max_size=current_app.config["IMAGES_MAX_SIZE"])
    filepath = storage.create_filepath(image_identifier)

    if filepath is None:
        return False

    try:
        storage.save(filepath, file_object)
        mimetype = storage.get_mimetype(filepath)

        if mimetype not in const.IMAGE_MIMETYPES:
            return False

        with Image.open(filepath) as image:
            image = image.convert("RGBA")
            image.thumbnail(max_resolution)

            # Convert transparent background into white background.
            bg = Image.new("RGB", image.size, color=(255, 255, 255))
            bg.paste(image, mask=image.split()[-1])
            image = bg

            f = storage.open(filepath, mode="wb")
            image.save(f, format="JPEG", quality=95)
            storage.close(f)

        return True

    except Exception as e:
        current_app.logger.exception(e)

    return False


def delete_thumbnail(image_identifier):
    """Delete a thumbnail.

    This is the inverse operation of :func:`save_as_thumbnail`.

    :param image_identifier: See :func:`save_as_thumbnail`.
    :return: ``True`` if the thumbnail was deleted successfully, ``False`` otherwise.
    """
    storage = create_misc_storage()
    filepath = storage.create_filepath(image_identifier)

    if filepath is None:
        return False

    storage.delete(filepath)
    return True
