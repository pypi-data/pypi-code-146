#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.db.database import Database
from poppy.core.conf import settings

__all__ = ['Base']

# register the base for future use
Base = Database.bases_manager.get(settings.MUSIC_DATABASE)
