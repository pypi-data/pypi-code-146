# Product name and version.
#
# Copyright (C) 2011-2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from importlib_metadata import version, PackageNotFoundError

try:
    v = version("flexirpg")
except PackageNotFoundError:
    v = "0.0.0"
vers = v.split(".", 4)

PRODUCT = "FlexiRPG"
VERSION_MAJOR = int(vers[0])
VERSION_MINOR = int(vers[1])
VERSION_MICRO = int( vers[2])
VERSION_EXTRA = f".{vers[3]}" if len(vers) > 4 else ""

SERVER_MIN_CLIENT_VERSION = "1.99.0"

# This version is for network capability.
PROTOCOL_VERSION = "2.2"

VERSION = "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_MICRO)

CLIENT_STRING = "%s %s%s" % (PRODUCT, VERSION, VERSION_EXTRA)

if __name__ == "__main__":
    print(VERSION + VERSION_EXTRA)
