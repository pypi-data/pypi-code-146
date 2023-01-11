## $Id: interfaces.py 13089 2015-06-21 15:12:52Z henrik $
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
"""Interfaces for viewing components.
"""
from zope import schema
from zope.interface import Interface, Attribute
from waeup.kofa.interfaces import (
    IKofaObject, IUniversity, IUsersContainer, IDataCenter, validate_email)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.university.interfaces import (
    IFacultiesContainer, IFaculty, IDepartment,
    ICoursesContainer, ICourse, ICertificatesContainer,
    ICertificate, ICertificateCourse)

class IBreadcrumb(Interface):
    """Provide breadcrumbs.
    """
    title = Attribute("Context description")
    viewname = Attribute("The viewname, for which the breadcrumb is provided.")
    parent_viewname = Attribute("The viewname of the parent to use.")
    parent = Attribute("The parent object.")
    context = Attribute("The context of the breadcrumb.")
    target = Attribute("The link target.")

class IBreadcrumbIgnorable(Interface):
    """A marker interface for breadcrumbs that should be skipped in output.

    If a breadcrumb wants to be skipped in real output (for instance,
    because it is set on a layer in site hierarchy that should not be
    accessed by users), it can also provide this interface. The
    getBreadcrumbList() function defined here will exclude IIgnorables
    by default.
    """
    pass

class IBreadcrumbContainer(Interface):
    """A container of breadcrumbs.
    """
    def __iter__():
        """Allow iteration over the container.
        """

    def getList():
        """Get the list of breadcrumbs as real Python list.
        """
class ICaptchaRequest(Interface):
    """A set of data required to verify captcha solutions.

    To solve a captcha we need at least a solution. Many types of
    captchas might also need a challenge to compare whether the
    solution is correct.
    """
    solution = schema.TextLine(
        title = u'Solution string a user entered',
        default = None,
        )
    challenge = schema.TextLine(
        title = u'The challenge the solution might match',
        default = None,
        )

class ICaptchaResponse(Interface):
    """A formalized response for captcha solutions.
    """
    is_valid = schema.Bool(
        title = u'Indicates validity of entered captcha data.',
        default = False,
        )
    error_code = schema.TextLine(
        title = u'Error when trying to validate entered captcha data.',
        description = u'Error codes are not expected to be readable strings.',
        default = None,
        )

class ICaptcha(Interface):

    def verify(request):
        """Verify data entered in an HTTP request.

        Expects some IHTTPRequest object and returns an
        ICaptchaResponse indicating that the solution was correct or
        not.

        If the solution could not be verified (this might also happen
        because of technical reasons), the response might contain an
        error code.
        """

    def display(error_code=None):
        """Returns a piece of HTML code that displays the captcha.

        The generated HTML code might depend on any previous error
        code as returned from :meth:`verify`.

        The code is expected to appear inside a ``<form>``. It
        therefore should not contain a ``<form>`` nor any submit
        buttons.
        """

class ICaptchaConfig(Interface):
    """Any type of captcha might need some configuration data.

    By default we require no configuration data.
    """

class ICaptchaManager(Interface):
    """A chooser that collects available captchas.
    """
    def getAvailCaptchas():
        """Return a dict of available captchas with registered names as keys.
        """

    def getCaptcha():
        """Get captcha chosen for a certain site or default.
        """

class IPDFCreator(Interface):
    """A component that knows where logo graphics for PDFs are stored
    and can generate PDF documents.

    It is a utility (and not a simple function or class) to make these
    data customizable in derived packages.
    """
    header_logo_path = schema.TextLine(
        title = u'Path to header logo JPG')
    watermark_path = schema.TextLine(
        title = u'Path to watermark logo JPG')
    def paint_background(canvas, doc):
        """A callback function to render background of PDFs.
        """
    def create_pdf(data, headerline=None, title=None, author=None,
                   footer='', note=None, sigs_in_footer=[]):
        """Create a PDF.

        `data` is expected to be a list of reportlab flowables
        (paragraphs, images, tables, etc.), that will be rendered into
        some background.

        `headerline` will be displayed in page head and `title` under
        the top bar.

        `note` is optional HTML markup added at bottom of created
        document.

        `footer` is the text rendered in the bottom line next to the
        page numbers.

        `sigs_in_footer` is a set of translateable strings that will be
        rendered into signature boxes at bottom of each page.

        If no `headerline` is given, a default will be rendered (name
        of university).

        If no `title` is given, nothing will be rendered.
        """

class IChangePassword(IKofaObject):
    """Interface needed for change pasword page.

    """
    identifier = schema.TextLine(
        title = _(u'Unique Identifier'),
        description = _(
            u'User Name, Student or Applicant Id, Matriculation or '
            u'Registration Number'),
        required = True,
        readonly = False,
        )

    email = schema.ASCIILine(
        title = _(u'Email Address'),
        required = True,
        constraint=validate_email,
        )

class IStudentNavigationBase(IKofaObject):
    """Objects that provide student navigation should
       implement this interface.
    """
    student = Attribute('''Some student object that has a '''
                        ''' `display_fullname` attribute.''')
