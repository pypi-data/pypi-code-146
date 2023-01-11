#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeferredReflection

__all__ = ["Event"]


class Event(DeferredReflection, Base):
    __tablename__ = "eventdescr"

    device = relationship("Device")
    collection = relationship("ParserCollection")
    test = relationship("Descriptor")
    packet_type = relationship("PacketType")