# FlexiRPG -- Image ID (hash)
#
# Copyright (C) 2021 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import hashlib

class ImageId:
    """A globally unique identifier for an image.

    Images are identified using a SHA-256 hash.
    """

    def __init__(self, image_id_str: str):
        self._image_id = image_id_str

    @classmethod
    def from_data(self, data: bytes):
        return ImageId(hashlib.sha256(data).hexdigest())

    def __str__(self):
        return self._image_id

    def __repr__(self):
        return f"ImageId <{self._image_id}>"

    def __eq__(self, other: "ImageId"):
        return self._image_id == other._image_id

    def __hash__(self):
        return hash(self._image_id)
