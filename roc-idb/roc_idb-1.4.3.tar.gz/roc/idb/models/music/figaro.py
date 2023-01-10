#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reference documentation
# ROC-GEN-SYS-NTT-00038-LES_Iss01_Rev02(Mission_Database_Description_Document)

from sqlalchemy.ext.declarative import DeferredReflection

from .base import Base

__all__ = [
    'Sequence',
    'Procedure',
    'TelecommandParameter',
    'Telecommand',
    'StepSeparator',
    'RpwStateDescription',
]


class RpwStateDescription(DeferredReflection, Base):
    """
    RpwStateDescription model
    """

    __tablename__ = 'figaro_rpwstatedescription'
    __table_args__ = {
        'schema': 'music',
    }


class Procedure(DeferredReflection, Base):
    """
    Procedure model
    """

    __tablename__ = 'figaro_procedure'
    __table_args__ = {
        'schema': 'music',
    }


class Sequence(DeferredReflection, Base):
    """
    Sequence model, related to :model:`figaro.Procedure`
    """

    __tablename__ = 'figaro_sequence'
    __table_args__ = {'schema': 'music'}


class Telecommand(DeferredReflection, Base):
    """
    Telecommand statement model, related to :model:`figaro.Sequence`
    """

    __tablename__ = 'figaro_telecommand'
    __table_args__ = {'schema': 'music'}


class TelecommandParameter(DeferredReflection, Base):
    """
    Telecommand parameter model, related to :model:`figaro.Telecommand`
    """

    __tablename__ = 'figaro_telecommandparameter'
    __table_args__ = {'schema': 'music'}


class StepSeparator(DeferredReflection, Base):
    """
    Step separator statement model, related to :model:`figaro.Sequence`
    """

    __tablename__ = 'figaro_stepseparator'
    __table_args__ = {'schema': 'music'}


class TelecommandDuration(DeferredReflection, Base):
    """
    Telecommand duration model, related to :model:`figaro.TelecommandDuration`
    """

    __tablename__ = 'figaro_telecommandduration'
    __table_args__ = {'schema': 'music'}
