#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy.ext.declarative import DeferredReflection

__all__ = ["Device"]


class Device(DeferredReflection, Base):
    __tablename__ = "device"

