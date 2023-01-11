##
## tests.py
## Login : <uli@pu.smp.net>
## Started on  Mon Sep 13 10:38:33 2010 Uli Fouquet
## $Id: test_image.py 7137 2011-11-19 08:37:08Z henrik $
## 
## Copyright (C) 2010 Uli Fouquet
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
"""Tests for image files.
"""
import doctest
import unittest

from hurry.file.file import IdFileRetrieval
from hurry.file.interfaces import IFileRetrieval
from zope import component
from zope.app.testing import placelesssetup


def imageSetUp(doctest):
    placelesssetup.setUp()
    component.provideUtility(IdFileRetrieval(), IFileRetrieval)

def test_suite():
    return unittest.TestSuite(
        (
            doctest.DocFileSuite(
                'image.txt',
                setUp=imageSetUp,
                tearDown=placelesssetup.tearDown,
                optionflags=doctest.ELLIPSIS,
                ),
            )
        )
