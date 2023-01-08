# FlexiRPG -- directory paths.
#
# Copyright (C) 2010-2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import os
import errno
import pkg_resources
import shutil

class _Paths:
    def __init__(self):
        self._paths = {}
        self._paths["image"] = pkg_resources.resource_filename("orpg", "images")
        self._paths["template"] = pkg_resources.resource_filename("orpg", "templates")

        #
        # Path to user files.
        #
        # Windows:
        #    %APPDATA%\OpenRPG\ = X:\Documents\<user>\Application Data\FlexiRPG\
            #
        # Linux:
        #   $HOME/.flexirpg/ = /home/<user>/.flexirpg/
        #
        if 'HOME' in os.environ:
            user_dir = os.environ['HOME'] + os.sep + ".flexirpg"
        elif 'APPDATA' in os.environ:
            user_dir = os.environ['APPDATA'] + os.sep + "FlexiRPG"
        else:
            # Neither Windows nor Linux?
            user_dir = os.path.dirname(__file__) + "myfiles"

        for d in (".", "runlogs", "logs"):
            try:
                os.makedirs(os.path.join(user_dir, d))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        self._paths["user"] = user_dir
        self._paths["log"] = os.path.join(self._paths["user"], "logs")

    def image(self, filename=None):
        """Get path for an included image."""
        return self._path("image", filename)

    def template(self, filename=None):
        """Get path for an included template file."""
        return self._path("template", filename)

    def user(self, filename=None):
        """Get path for a file in the per-user directory."""
        return self._path("user", filename)

    def log(self, filename=None):
        """"Get the path for a log file."""
        return self._path("log", filename)

    def config(self, user_file):
        """Get the path for a config file with fallback template."""
        template_file = "default_" + user_file
        template_path = self.template(template_file)
        user_path = self.user(user_file)

        # Check template file exists, raising FileNotFoundError otherwise.
        os.stat(template_path)

        # Need to copy template?
        if not os.path.exists(user_path):
            shutil.copyfile(template_path, user_path)
        return user_path

    def _path(self, path_type, filename):
        if filename is None:
            return self._paths[path_type]
        return os.path.join(self._paths[path_type], filename)

Paths = _Paths()
