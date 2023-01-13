#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import Column, Integer, String

__all__ = ["FeedBackStatus"]


class FeedBackStatus(DeferredReflection, Base):
	__tablename__ = "feedbackstatus"

	ID = Column(Integer, primary_key=True)
	Status = Column(String)