#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from .base import Base
from sqlalchemy.ext.declarative import DeferredReflection

__all__ = ["DatabaseInformation"]


class DatabaseInformation(Base):
	__tablename__ = "databaseinformation"
	ID = Column(Integer, primary_key=True)
	DatabaseName = Column(String)
	Name = Column(String)
	Current = Column(Integer)