# FlexiRPG -- Library of images identified by their hashes.
#
# Copyright (C) 2017,2021 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import os

from orpg.config import Paths
from orpg.lib.imageid import ImageId

class ImageLibrary(object):
    def __init__(self, image_class):
        """Create an empty image library.

        """

        self.image_class = image_class
        self.providers = []
        self.images = {}

    def register_provider(self, provider):
        self.providers.append(provider)

    def unregister_provider(self, provider):
        assert provider in self.providers

        providers.remove(providers)

    def add(self, image):
        self.images[image.image_id] = image
        if not image.has_image():
            self._fetch(image)

    def get(self, image_id, size=None):
        """Get an images from the cache by its hash.

        The image data will be requested but may not be immediately
        available (e.g., if it needs to be fetched from a client or
        server.).

        """

        assert isinstance(image_id, ImageId)

        if image_id in self.images:
            return self.images[image_id]
        new_image = self.image_class(image_id=image_id, size=size)
        self.add(new_image)
        return new_image

    def get_local(self, image_id):
        """Get an image from the library, iff it exists locally.

        If the image exists locally, the image data will be
        immediately available, otherwise None is returned.

        """
        if image_id in self.images:
            image = self.images[image_id]
            if image.has_image():
                return image
        else:
            image = self.image_class(image_id)
            if self._fetch_local(image):
                self.images[image.image_id] = image
                return image
        return None

    def _fetch(self, image):
        for provider in self.providers:
            if provider.fetch(image):
                return True
        return False

    def _fetch_local(self, image):
        for provider in self.providers:
            if provider.fetch_local(image):
                return True
        return False

    def get_from_data(self, data):
        image = self.image_class(ImageId.from_data(data))
        image.set_image(data)
        self.add(image)
        return image

    def get_from_file(self, path):
        f = open(path, "rb")
        data = f.read()
        f.close()
        return self.get_from_data(data)

    def get_from_uuid(self, uuid: str):
        for ext in ["png", "jpg"]:
            old_image_path = os.path.join(Paths.user("images"), f"{uuid}.{ext}")
            if os.path.exists(old_image_path):
                return self.get_from_file(old_image_path)
        return None
