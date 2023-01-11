## $Id: interfaces.py 9266 2012-10-02 06:43:52Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Interfaces of access code related components.
"""
from zope import schema
from zope.interface import Interface
from waeup.kofa.interfaces import IKofaObject
from waeup.kofa.interfaces import MessageFactory as _

class IAccessCode(IKofaObject):
    """An access code.
    """
    batch_serial = schema.Int(
        title = _(u'Serial number inside batch'),
        )
    batch_prefix = schema.TextLine(
        title = _(u'Prefix inside batch'),
        )
    batch_num = schema.Int(
        title = _(u'Batch number'),
        )
    random_num = schema.TextLine(
        title = _(u'Random part of access code'),
        )
    cost = schema.Float(
        title = _(u'Cost of access code'),
        )
    state = schema.TextLine(
        title = _(u'Workflow state'),
        required = False,
        )
    representation = schema.TextLine(
        title = _(u'Complete title of access code'),
        )
    owner = schema.TextLine(
        title = _(u'Purchaser'),
        required = False,
        )
    history = schema.Text(
        title = _(u'The history of access code as lines'),
        default = u'',
        readonly = True,
        required = False,
       )

class IAccessCodeBatch(Interface):
    """A factory for batches of access codes.
    """
    creation_date = schema.Datetime(
        title = _(u'Creation date'),
        )
    creator = schema.TextLine(
        title = _(u'Batch creator'),
        )
    prefix = schema.TextLine(
        title = _(u'Batch prefix'),
        )
    num = schema.Int(
        title = _(u'Batch number (1-3 digits)'),
        min = 0, max = 999,
        )
    entry_num = schema.Int(
        title = _(u'Number of access codes'),
        default = 1000, min = 0,
        )
    cost = schema.Float(
        title = _(u'Cost of access code'),
        default = 0.0, min = 0.0,
        )
    disabled_num = schema.Int(
        title = _(u'Number of disabled access codes inside the batch'),
        default = 0,
        readonly = True,
        )
    used_num = schema.Int(
        title = _(u'Number of used access codes inside the batch'),
        default = 0,
        readonly = True,
        )

class IAccessCodeBatchContainer(IKofaObject):
    """A container for access code batches.
    """

    def addBatch(batch):
        """Add a batch.
        """
