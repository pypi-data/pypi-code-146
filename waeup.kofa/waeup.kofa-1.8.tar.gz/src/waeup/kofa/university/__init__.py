# Make this a package.
from waeup.kofa.university.course import Course
from waeup.kofa.university.coursescontainer import CoursesContainer
from waeup.kofa.university.certificate import Certificate
from waeup.kofa.university.certificatescontainer import CertificatesContainer
from waeup.kofa.university.faculty import Faculty
from waeup.kofa.university.department import Department
from waeup.kofa.university.facultiescontainer import FacultiesContainer
__all__ = (
    'Course', 'CoursesContainer',
    'Certificate', 'CertificatesContainer',
    'Faculty', 'FacultiesContainer', 'Department')
