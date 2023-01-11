#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import DeferredReflection


__all__ = ["Code", "Message"]


class Message(DeferredReflection, Base):
    __tablename__ = "errormessage"

    errorCode = Column(Integer, primary_key=True)
    errorMessage = Column(String)

class Code(DeferredReflection, Base):
    __tablename__ = "errorcode"

    eventID = Column(Integer, ForeignKey("eventdescr.ID"), primary_key=True)
    error = relationship("Message", uselist=False)
    event = relationship("Event", uselist=False)
    message = association_proxy("error", "ErrorMessage")


