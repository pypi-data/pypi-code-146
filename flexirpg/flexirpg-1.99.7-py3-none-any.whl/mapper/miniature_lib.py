# FlexiRPG -- library of miniature templates.
#
# Copyright (C) 2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import codecs
import glob
import json
import math
import os
import pathlib
from string import *

import wx

from orpg.config import Paths
from orpg.lib.imageid import ImageId
from orpg.main import image_library

class MiniatureTemplate(object):
    def __init__(self, image_id, name, favourite):
        """Create a miniature template.

        image_id: ImageId for the miniature image.
        name: Name for the miniature.

        """
        self._image_id = image_id
        self._name = name
        self._favourite = favourite
        self._size = (20, 20) # HACK: assuming this size.
        self._serial = 0

    @property
    def image_id(self):
        return self._image_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val: str):
        self._name = val

    @property
    def favourite(self):
        return self._favourite

    @favourite.setter
    def favourite(self, val: bool):
        self._favourite = val

    @property
    def size(self):
        return self._size

    def new_label(self):
        self._serial += 1
        return "%s %d" % (self.name, self._serial)

    def image(self):
        return image_library.get(self._image_id).wximage

    def tool_bitmap(self, toolbar):
        """Return bitmap suitable for a toolbar icon.

        This returns a subset of the miniature image as a wx.Bitmap.

        """
        image = self.image()
        scale = min(toolbar.ToolBitmapSize.x / image.Width,
                    toolbar.ToolBitmapSize.y / image.Height)
        if scale < 1.0:
            image = image.Scale(math.ceil(image.Width * scale),
                                math.ceil(image.Height * scale),
                                wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

class MiniatureLib(object):
    def __init__(self):
        """Create a miniature template library.

        The library is populated from the configuration file
        ~/.flexirpg/miniatures.json
        """
        self._library = []
        self.favourites = MiniatureFavourites(self)

        self._config_file = Paths.user("miniatures.json")
        self._load()
        self.save()

    def _load(self):
        if not os.path.exists(self._config_file):
            return

        try:
            with codecs.open(self._config_file, "r", "utf-8") as f:
                d = json.load(f)
        except (OSError, IOError, ValueError):
            return

        for e in d:
            if "image-id" in e:
                mini = MiniatureTemplate(
                    ImageId(e["image-id"]),
                    e["name"],
                    e["favourite"] if "favourite" in e else True)
                self._library.append(mini)
            elif "uuid" in e:
                # Import old library that reference images using UUID.
                image = image_library.get_from_uuid(e["uuid"])
                if image:
                    self.add(e["name"], image)

    def save(self):
        d = []
        for mini in self._library:
            e = {}
            e["image-id"] = str(mini.image_id)
            e["name"] = mini.name
            e["favourite"] = mini.favourite
            d.append(e)

        with codecs.open(self._config_file, "w", "utf-8") as f:
            json.dump(d, f, indent=4)

        self.favourites.refresh()

    def add(self, name, image):
        mini = MiniatureTemplate(image.image_id, name, True)
        self._library.append(mini)
        return mini

    def remove(self, mini):
        self._library.remove(mini)

    def move_before(self, dest, mini):
        self._library.remove(mini)
        self._library.insert(self._library.index(dest), mini)

    def move_after(self, dest, mini):
        self._library.remove(mini)
        self._library.insert(self._library.index(dest) + 1, mini)

    def __getitem__(self, n):
        return self._library[n]

    def __iter__(self):
        for i in self._library:
            yield i

class MiniatureFavourites:
    def __init__(self, minis):
        self._minis = minis

    def refresh(self):
        self._favourites = [m for m in self._minis if m.favourite]

    def count(self):
        return len(self._favourites)

    def image(self, index):
        return self._favourites[index].image()

    def __contains__(self, mini):
        return mini in self._minis

    def __getitem__(self, n):
        if n < len(self._favourites):
            return self._favourites[n]
        return None
