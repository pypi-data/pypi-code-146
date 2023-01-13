#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import Column, Integer, String

__all__ = ["ParserCollection"]


class ParserCollection(Base):
    __tablename__ = "parsercollection"

    ID = Column(Integer, primary_key=True)
    CollectionName = Column(String)


