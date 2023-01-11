#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.db.database import Database

__all__ = ["Base"]

# register the base for future use
Base = Database.bases_manager.get("MEB_DATA")
