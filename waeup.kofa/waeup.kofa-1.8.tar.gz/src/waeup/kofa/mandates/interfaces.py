## $Id: interfaces.py 13959 2016-06-21 04:46:56Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
from zope.interface import Attribute
from zope import schema
from waeup.kofa.interfaces import IKofaObject

class IMandatesContainer(IKofaObject):
    """A container for all kind of mandate objects.

    """

    count = Attribute('Count active and expired mandates.')

    def addMandate(mandate):
        """Add mandate.
        """

    def removeExpired():
        """Remove all expired mandates and return the number
        of successfully removed mandates.
        """

class IMandate(IKofaObject):
    """A representation of all mandates.

    """
    mandate_id = Attribute('Mandate Identifier')
    expires = Attribute('Expiration Datetime')
    params = Attribute('Dictionary with mandate parameters')

    def execute():
        """Method which is performed by the mandate.
        """
