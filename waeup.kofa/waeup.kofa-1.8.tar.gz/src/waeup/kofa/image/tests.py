## $Id: tests.py 7196 2011-11-25 07:44:52Z henrik $
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
import unittest

from zope.testing import doctest
from zope.app.testing import placelesssetup
from zope import component

from hurry.file.file import IdFileRetrieval
from hurry.file.interfaces import IFileRetrieval

def fileSetUp(doctest):
    placelesssetup.setUp()
    component.provideUtility(IdFileRetrieval(), IFileRetrieval)

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt',
            setUp=fileSetUp, tearDown=placelesssetup.tearDown,
            ),
        ))
