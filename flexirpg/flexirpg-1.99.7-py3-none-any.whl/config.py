# FlexiRPG -- Configuration (paths and settings)
#
# Copyright (C) 2010-2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from orpg.tools.paths import Paths
import orpg.tools.settings

Settings = orpg.tools.settings.SettingCollection(Paths.user("settings.dat"))
