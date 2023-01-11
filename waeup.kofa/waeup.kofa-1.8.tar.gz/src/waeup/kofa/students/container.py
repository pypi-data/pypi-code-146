## $Id: container.py 13165 2015-07-13 07:53:26Z henrik $
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
Containers for students.
"""
import grok
from thread import allocate_lock
from transaction import commit
from zope.component import getUtility
from waeup.kofa.students.interfaces import (
    IStudentsContainer, IStudent, IStudentsUtils)
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.utils.logger import Logger

lock = allocate_lock() # a lock object to lock threads.

class StudentsContainer(grok.Container, Logger):
    """
    The node containing the student models
    """

    grok.implements(IStudentsContainer)

    _curr_stud_id = 10 ** 6

    logger_name = 'waeup.kofa.${sitename}.students'
    logger_filename = 'students.log'

    @property
    def unique_student_id(self):
        """A unique student id.

        The student id returned is guaranteed to be unique. It
        consists of some prefix (normally a single letter) followed by
        a number with at least 7 digits.

        Once a student id was issued, it won't be issued again.

        Obtaining a student id is currently not thread-safe but can be
        made easily by enabling commented lines.
        """
        prefix = getUtility(IStudentsUtils).STUDENT_ID_PREFIX

        # lock.acquire() # lock data
        new_id = u'%s%s' % (prefix, self._curr_stud_id)
        self._curr_stud_id += 1
        # self._p_changed = True
        # commit()
        # lock.release() # end of lock
        return new_id

    def addStudent(self, student):
        """Add a student with subcontainers.
        """
        if not IStudent.providedBy(student):
            raise TypeError(
                'StudentsContainers contain only IStudent instances')
        self[student.student_id] = student
        return

StudentsContainer = attrs_to_fields(StudentsContainer)
