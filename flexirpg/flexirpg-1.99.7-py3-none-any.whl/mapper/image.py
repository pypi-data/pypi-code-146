# FlexiRPG -- Images identified by IMGID
#
# Copyright (C) 2017 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import base64
import imghdr
import os.path

from orpg.tools.paths import Paths


class Image(object):
    def __init__(self, image_id, size = None):
        """Create an image with a IMAGE_ID and (optionally) size.

        """
        self.image_id = image_id
        self.size = size
        self.data = None
        self.data64 = None
        self._hooks = []
        self._mime_type = None

        self.images_dir = Paths.user("images")

    def set_image(self, data):
        assert not self.has_image()

        self.data = data
        self._detect_mime_type()

        # Save the image to the file system cache.
        try:
            if not os.path.exists(self.images_dir):
                os.mkdir(self.images_dir)
            cache_file = os.path.join(self.images_dir, self.cache_file_name)
            if not os.path.exists(cache_file):
                f = open(cache_file, "wb")
                f.write(data)
                f.close()
        except (OSError, IOError):
            # Silently ignore errors when updating the cache file
            pass

        self._set_image_done()

        for hook in self._hooks:
            hook(self)

    def _set_image_done(self):
        pass

    def has_image(self):
        return self.data != None

    def __get_width(self):
        return self.size[0]

    def __get_height(self):
        return self.size[1]

    width = property(__get_width)
    height = property(__get_height)

    def add_hook(self, hook):
        self._hooks.append(hook)

    def del_hook(self, hook):
        self._hooks.remove(hook)

    def base64(self):
        if not self.data64:
            self.data64 = base64.b64encode(self.data).decode("ascii")
        return self.data64

    def set_image_from_base64(self, b64):
        self.set_image(base64.b64decode(b64.encode("ascii")))

    @property
    def cache_file_name(self):
        if self.mime_type == "image/jpeg":
            ext = "jpg"
        elif self.mime_type == "image/png":
            ext = "png"
        else:
            ext = "bin"
        return "{}.{}".format(self.image_id, ext)

    @property
    def mime_type(self):
        return self._mime_type

    def _detect_mime_type(self):
        t = imghdr.what(None, self.data)
        if t == "jpeg":
            self._mime_type = "image/jpeg"
        elif t == "png":
            self._mime_type = "image/png"
        else:
            self._mime_type = "application/unknown"

class ServerImage(Image):
    """An image in the server -- it keeps track of who requested it so it
    can send IMAGEDATA messages to clients.

    """

    def __init__(self, image_id, size=None):
        Image.__init__(self, image_id, size)

        self.provider = None
        self.requesters = []

    def add_requester(self, provider, player_id):
        self.provider = provider
        self.requesters.append(player_id)

    def has_requesters(self):
        return self.requesters != []

    def _set_image_done(self):
        for player_id in self.requesters:
            self.provider.send_imagedata(player_id, self)
        self.requesters = []
