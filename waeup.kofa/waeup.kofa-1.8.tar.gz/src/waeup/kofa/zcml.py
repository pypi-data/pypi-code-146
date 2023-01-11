## $Id: zcml.py 8057 2012-04-06 21:56:22Z henrik $
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
from zope.component.zcml import handler
from waeup.kofa.interfaces import IDataCenterConfig

def data_center_conf(context, path):
    """Handler for ZCML ``datacenter`` directive.

    Registers a global utility under IDataCenterConfig and containing
    a dictionary with (currently) only one entry: `path`.

    The directive can be put into site.zcml like this:

    - Add to the header:
        ``xmlns:kofa="http://namespaces.waeup.org/kofa"``

    - Then, after including waeup.kofa:
        ``<kofa:datacenter path="some/existing/file/path" />``

    In a running instance (where some directive like above was
    processed during startup), one can then ask for the
    IDataCenterConfig utility:

      >>> from waeup.kofa.interfaces import IDataCenterConfig
      >>> from zope.component import getUtility
      >>> getUtility(IDataCenterConfig)
      {'path': 'some/existing/file/path'}

    """
    context.action(
        discriminator = ('utility', IDataCenterConfig, ''),
        callable = handler,
        args = ('registerUtility',
                {'path':path}, IDataCenterConfig, '')
        )
