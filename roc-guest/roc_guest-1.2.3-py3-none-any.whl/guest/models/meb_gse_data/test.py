#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Enum

__all__ = ["Descriptor"]

class Descriptor(Base):
	__tablename__ = "testdescriptor"

	ID = Column(Integer, primary_key=True)
	UUID = Column(String)
	TestName = Column(String)
	Status = Column('status', Enum('Running', 'Pending', 'Terminated', name='myenum'))
	Author = Column(String)
	Description = Column(String)
	CreationDate = Column(DateTime)
	OneShot = Column(Integer)
	Launched = Column(DateTime)
	TerminatedDate = Column(DateTime)
	RunningDPUIsNominal = Column(Integer)
	XML = Column(String)
	MainScript =  Column(Integer)
	HWVersion = Column(String)
	SWVersion = Column(String)
	OtherConfiguration = Column(String)
	Masked = Column(Integer)