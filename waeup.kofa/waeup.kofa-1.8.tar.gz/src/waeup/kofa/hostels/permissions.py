## $Id: permissions.py 17253 2022-12-29 09:15:31Z henrik $
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
"""
Permissions for the accommdation section.
"""
import grok

# Accommodation section permissions

class ViewHostels(grok.Permission):
    """The ViewHostels permission is applied to all views of the
    Accommodation Section. Users with this permission can view but not edit
    data in the Accommodation Section.
    """
    grok.name('waeup.viewHostels')

class ManageHostels(grok.Permission):
    """The ManageHostels permission is applied to manage pages in the
    Accommodation Section.
    """
    grok.name('waeup.manageHostels')

class ExportAccommodationData(grok.Permission):
    """Accommodation Officers don't have the general exportData
    permission and are only allowed to export accommodation data
    (accommodation payment tickets and bed tickets).
    The ExportAccommodationData permission is only used to filter the
    respective exporters in the ExportJobContainerJobConfig view.
    """
    grok.name('waeup.exportAccommodationData')

# Site Roles
class AccommodationOfficer(grok.Role):
    """Accommodation Officers can view and manage hostels. They can also export
    student accommodation data (filtered payment tickets and bed tickets).
    They can't access the Data Center but see student data export buttons
    in the Academic Section.
    """
    grok.name('waeup.AccommodationOfficer')
    grok.title(u'Accommodation Officer')
    grok.permissions('waeup.viewHostels',
                     'waeup.manageHostels',
                     'waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportAccommodationData')

class AccommodationViewer(grok.Role):
    """Accommodation Viewers can view but not manage hostels. They can also export
    student accommodation data (filtered payment tickets and bed tickets).
    They can't access the Data Center but see student data export buttons
    in the Academic Section.
    """
    grok.name('waeup.AccommodationViewer')
    grok.title(u'Accommodation Viewer')
    grok.permissions('waeup.viewHostels',
                     'waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportAccommodationData')
