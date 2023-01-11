"""This package contains everything regarding students.
"""
# Make this a package.
from waeup.kofa.students.student import (
    Student, StudentFactory
    )
from waeup.kofa.students.container import StudentsContainer
from waeup.kofa.students.studycourse import StudentStudyCourse
from waeup.kofa.students.payments import StudentPaymentsContainer
from waeup.kofa.students.accommodation import StudentAccommodation
from waeup.kofa.students.dynamicroles import StudentPrincipalRoleManager


__all__ = [
    'Student',
    'StudentFactory',
    'StudentsContainer',
    'StudentStudyCourse',
    'StudentPaymentsContainer',
    'StudentAccommodation',
    'StudentPrincipalRoleManager',
    ]
