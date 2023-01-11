#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import Column, Integer, String

__all__ = ["PacketType"]

class PacketType(Base):
	__tablename__ = "packettype"

	ID = Column(Integer, primary_key=True)
	Type = Column(String)
	IsInput = Column(Integer)