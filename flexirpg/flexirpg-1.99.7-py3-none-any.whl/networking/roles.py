# Player roles (GM, player, or lurker).
#
# Copyright (C) 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

ROLE_GM = "GM"
ROLE_PLAYER = "Player"
ROLE_LURKER = "Lurker"

def role_from_string(s):
    s = s.upper()
    if s == "GM":
        return ROLE_GM
    elif s == "PLAYER":
        return ROLE_PLAYER
    else:
        return ROLE_LURKER
