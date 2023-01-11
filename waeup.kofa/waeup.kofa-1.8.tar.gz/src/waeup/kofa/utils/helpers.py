## $Id: helpers.py 16818 2022-02-21 06:21:10Z henrik $
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
"""General helper functions for Kofa.
"""
import unicodecsv as csv  # XXX: csv ops should move to dedicated module.
import datetime
import imghdr
import logging
import os
import pytz
import re
import shutil
import tempfile
import transaction
import grok
from cStringIO import StringIO
from docutils.core import publish_string
from HTMLParser import HTMLParser
from zope.component import getUtility
from zope.component.interfaces import IFactory
from zope.interface import implementedBy
from zope.interface.interface import Method, Attribute
from zope.intid.interfaces import IIntIds
from zope.schema import getFieldNames
from zope.schema.fieldproperty import FieldProperty
from zope.security.interfaces import NoInteraction
from zope.security.management import getInteraction
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.formlib.widget import renderElement


BUFSIZE = 8 * 1024


def remove_file_or_directory(filepath):
    """Remove a file or directory.

    Different to :func:`shutil.rmtree` we also accept not existing
    paths (returning silently) and if a dir turns out to be a regular
    file, we remove that.
    """
    filepath = os.path.abspath(filepath)
    if not os.path.exists(filepath):
        return
    if os.path.isdir(filepath):
        shutil.rmtree(filepath)
    else:
        os.unlink(filepath)
    return


def copy_filesystem_tree(src, dst, overwrite=False, del_old=False):
    """Copy contents of directory src to directory dst.

    Both directories must exists.

    If `overwrite` is true, any same named objects will be
    overwritten. Otherwise these files will not be touched.

    If `del_old` is true, copied files and directories will be removed
    from the src directory.

    This functions returns a list of non-copied files.

    Unix hidden files and directories (starting with '.') are not
    processed by this function.
    """
    if not os.path.exists(src):
        raise ValueError('source path does not exist: %s' % src)
    if not os.path.exists(dst):
        raise ValueError('destination path does not exist: %s' % dst)
    if not os.path.isdir(src):
        raise ValueError('source path is not a directory: %s' % src)
    if not os.path.isdir(dst):
        raise ValueError('destination path is not a directory: %s' % dst)
    not_copied = []
    for item in os.listdir(src):
        if item.startswith('.'):
            continue  # We do not copy hidden stuff...
        itemsrc = os.path.join(src, item)
        itemdst = os.path.join(dst, item)

        if os.path.exists(itemdst):
            if overwrite is True:
                remove_file_or_directory(itemdst)
            else:
                not_copied.append(item)
                continue

        if os.path.isdir(itemsrc):
            shutil.copytree(itemsrc, itemdst)
        else:
            shutil.copy2(itemsrc, itemdst)
        if del_old:
            remove_file_or_directory(itemsrc)
    return not_copied


def get_inner_HTML_part(html_code):
    """Return the 'inner' part of a complete HTML snippet.

    If there is a form part, get this.

    If there is no form part, try to return the body part contents.

    If there is no body, return as-is.

    Let's see how that works. If we deliver some doc with form, we
    will get that form only:

       >>> doc = '<html><form>My Form</form>Outside the form</html>'
       >>> get_inner_HTML_part(doc)
       '<form>My Form</form>'

    No form? Then seek for a body part and get the contents:

       >>> doc = '<html><body>My Body</body>Trailing Trash</html>'
       >>> get_inner_HTML_part(doc)
       'My Body'

    If none of these is included, return what we got:

       >>> doc = '<html>without body nor form</html>'
       >>> get_inner_HTML_part(doc)
       '<html>without body nor form</html>'

    """

    try:
        result = re.match('^.+(<form[^\>]*>.*</form>).+$', html_code,
                          re.DOTALL).groups()[0]
        return result
    except AttributeError:
        # No <form> part included
        try:
            result = re.match('^.+<body[^\>]*>(.*)</body>.*$', html_code,
                              re.DOTALL).groups()[0]
            return result
        except AttributeError:
            # No <form> and no <body> tag...
            pass
    return html_code


class FactoryBase(grok.GlobalUtility):
    """A factory for things.

    This is a baseclass for easier creation of factories. Factories
    are utilities that are registered under a certain name and return
    instances of certain classes when called.

    In :mod:`waeup.kofa` we use factories extensively for
    batching. While processing a batch some processors looks up a
    factory to create real-world instances that then get filled with
    data from imported CSV files.

    To get rid of reimplementing the same stuff over and over again,
    most notably the methods defined here, we offer this base class
    (which will *not* be registered as a factory itself).

    Real factories can then be created like this:

       >>> import grok
       >>> from waeup.kofa.utils.helpers import FactoryBase
       >>> class MyObject(object):
       ...   # Some class we want to get instances of.
       ...   pass
       >>> class MyObjectFactory(FactoryBase):
       ...   # This is the factory for MyObject instances
       ...   grok.name(u'waeup.kofa.factory.MyObject')
       ...   factory = MyObject

    That's it. It is essential to set the ``factory`` attribute, which
    will determine the class of which instances should be created when
    called. The given name must even be unique amongst all utilities
    registered during runtime. While you can pick any name you like
    you might want to prepend ``waeup.kofa.factory.`` to the name
    string to make sure it does not clash with names of other
    utilities one day.

    Before all this works we have to grok the baseclass once and our
    freshly defined factory. This executes all the component
    registration stuff we don't want to do ourselves. In daily use
    this is done automatically on startup of a :mod:`waeup.kofa`
    system.

       >>> grok.testing.grok('waeup.kofa.utils.helpers')
       >>> grok.testing.grok_component(
       ...    'MyObjectFactory', MyObjectFactory
       ...  )
       True

    After grokking we (and processors) can create objects without
    knowing about the location of the real class definition, just by
    the factory name:

       >>> from zope.component import createObject
       >>> obj = createObject('waeup.kofa.factory.MyObject')
       >>> isinstance(obj, MyObject)
       True

    We can also use the regular utility lookups to find our new
    factory:

       >>> from zope.component import getUtility
       >>> from zope.component.interfaces import IFactory
       >>> factory = getUtility(
       ...   IFactory, name='waeup.kofa.factory.MyObject'
       ...   )
       >>> isinstance(factory, MyObjectFactory)
       True

    And this factory generates `MyObject` instances:

       >>> obj = factory()
       >>> isinstance(obj, MyObject)
       True

    """
    grok.baseclass()  # Do not grok this class, do not register us.
    grok.implements(IFactory)
    # You can override any of the following attributes in derived
    # classes. The `grok.name` setting *must* even be set to some
    # unique value.
    grok.name(u'waeup.Factory')
    title = u"Create instances of ``factory``.",
    description = u"This factory instantiates new applicant instances."
    factory = None

    def __call__(self, *args, **kw):
        """The main factory function.

        Returns an instance of the requested object.
        """
        return self.factory()

    def getInterfaces(self):
        # Required by IFactory
        return implementedBy(self.factory)


def ReST2HTML_w_warnings(source_string):
    """Convert a reStructuredText string to HTML preserving warnings.

    Returns a tuple ``(<HTML_CODE>, <WARNINGS>)``, both being
    strings. Where ``<HTML_CODE>`` is the HTML code generated from the
    source string (in unicode), ``<WARNINGS>`` is a string containing
    any warning messages or ``None``.

    Regular multi-line ReStructuredText strings will be returned as
    HTML code:

        >>> from waeup.kofa.utils.helpers import ReST2HTML
        >>> source = '''
        ... Headline
        ... ========
        ...
        ... - A list item
        ... - Another item
        ...
        ... Thanks for watching!
        ... '''
        >>> html, warnings = ReST2HTML_w_warnings(source)
        >>> print html
        <div class="document" id="headline">
        <h1 class="title">Headline</h1>
        <BLANKLINE>
        <ul class="simple">
        <li>A list item</li>
        <li>Another item</li>
        </ul>
        <p>Thanks for watching!</p>
        </div>

    Here no warnings happened, so the `warnings` are ``None``:

        >>> warnings is None
        True

    If warnings happen then they can be retrieved in the returned
    ``warnings``. We try to render an erraneous document:

        >>> source = '''
        ... Headline
        ... ======
        ...
        ... Thanks for watching!
        ... '''
        >>> html, warnings = ReST2HTML_w_warnings(source)
        >>> print html
        <div class="document" id="headline">
        <h1 class="title">Headline</h1>
        <BLANKLINE>
        <p>Thanks for watching!</p>
        </div>

        >>> print warnings
        <string>:3: (WARNING/2) Title underline too short.
        <BLANKLINE>
        Headline
        ======
        <BLANKLINE>

    As you can see, the warnings are not displayed inline the document
    but can be retrieved from the returned warnings, which is a string
    or ``None``.
    """
    warnings = StringIO()
    fulldoc = publish_string(
        source_string, writer_name='html4css1',
        settings_overrides={
            'report_level': 0,
            'warning_stream': warnings,
            })
    warnings.seek(0)
    warning_msgs = warnings.read()
    if warning_msgs:
        # Render again, this time with no warnings inline...
        fulldoc = publish_string(
        source_string, writer_name='html4css1',
        settings_overrides={
            'report_level': 10000,
            'halt_level': 10000,
            'warning_stream': warnings,
            })
    if warning_msgs == '':
        warning_msgs = None
    result = get_inner_HTML_part(fulldoc).strip()
    if not isinstance(result, unicode):
        result = result.decode('utf-8')
    return result, warning_msgs


def ReST2HTML(source_string):
    """Render a string containing ReStructuredText to HTML.

    Any warnings about too short headings, etc. are silently
    discarded. Use :func:`ReST2HTML_w_warnings` if you want to get any
    warnings.

    The returned string will be unicode.

    A regular document will be rendered like this:

        >>> source = '''
        ... Headline
        ... ========
        ...
        ... Thanks for watching!
        ... '''
        >>> html = ReST2HTML(source)
        >>> print html
        <div class="document" id="headline">
        <h1 class="title">Headline</h1>
        <BLANKLINE>
        <p>Thanks for watching!</p>
        </div>

    A document with markup problems (here: the underline is too short)
    will look similar:

        >>> source = '''
        ... Headline
        ... ======
        ...
        ... Thanks for watching!
        ... '''
        >>> html = ReST2HTML(source)
        >>> print html
        <div class="document" id="headline">
        <h1 class="title">Headline</h1>
        <BLANKLINE>
        <p>Thanks for watching!</p>
        </div>

    """
    html, warnings = ReST2HTML_w_warnings(source_string)
    return html


def attrs_to_fields(cls, omit=[]):
    """Set class attributes and bind them to the data definitions
    specified in the interface by turning the attributes into FieldProperty
    instances.

    With Python >= 2.6 we can even use this function as a class decorator.

    `omit` is a list of field names that should _not_ be turned into
    field properties. This is useful for properties and the like.
    """
    iface = list(implementedBy(cls))[0]
    for field_name in getFieldNames(iface):
        if field_name in omit:
            continue
        field_property = FieldProperty(iface[field_name])
        # Set proper docstring for the API docs.
        field_property.__doc__ = iface[field_name].title + ' (computed attribute)'
        setattr(cls, field_name, field_property)
    return cls


def get_current_principal():
    """Get the 'current' principal.

    This method works without a request. Examining a request is the
    regular (and recommended) way to get a principal involved
    'currently'.

    Use this method only if you really have no access to the current
    request.

    Returns ``None`` when no principal is involved (for instance
    during tests).
    """
    try:
        principal = getInteraction().participations[0].principal
    except NoInteraction:
        return None
    except IndexError:  # No participations present
        return None
    return principal


def cmp_files(file_descr1, file_descr2):
    """Compare two files by their file descriptors.

    Returns ``True`` if both are equal, ``False`` otherwise.
    """
    file_descr1.seek(0)
    file_descr2.seek(0)
    while True:
        b1 = file_descr1.read(BUFSIZE)
        b2 = file_descr2.read(BUFSIZE)
        if b1 != b2:
            return False
        if not b1:
            return True


def string_from_bytes(number):
    """Turn a number into some textual representation.

      Examples:

        >>> string_from_bytes(1)
        u'1 byte(s)'

        >>> string_from_bytes(1025)
        u'1 KB'

        >>> string_from_bytes(1.5 * 1024*1024)
        u'1.50 MB'

        >>> string_from_bytes(673.286 * 1024**3)
        u'673.29 GB'

    """
    if number < 1024:
        return u'%s byte(s)' % (str(number),)
    elif number < 1024 ** 2:
        return u'%s KB' % (number / 1024,)
    elif number < 1024 ** 3:
        return u'%.2f MB' % (number / 1024 ** 2,)
    return u'%.2f GB' % (number / 1024 ** 3,)


def file_size(file_like_obj):
    """Determine file size in most effective manner.

    Returns the number of bytes in a file. This function works for
    both, real files as well as file-like objects like cStringIO based
    'files'.

    Example:

      >>> from cStringIO import StringIO
      >>> file_size(StringIO('my file content'))
      15

    Please note that this function expects the file-like object passed
    in to be at first reading position (it does no seek(0)) and that
    when finished the file pointer might be at end of file.
    """
    if hasattr(file_like_obj, 'fileno'):
        return os.fstat(file_like_obj.fileno())[6]
    file_like_obj.seek(0, 2)  # seek to last position in file
    return file_like_obj.tell()


def get_user_account(request):
    """Return local user account.
    """
    principal_id = request.principal.id
    authenticator = getUtility(IAuthenticatorPlugin, name='users')
    account = authenticator.getAccount(principal_id)
    return account


def iface_names(iface, omit=[], exclude_attribs=True, exclude_methods=True):
    """Get all attribute names of an interface.

    Searches also base interfaces.

    Names of fields that are pure attributes
    (i.e. zope.interface.Attribute) or methods are excluded by
    default.

    Names of typical fields derived from zope.schema are included.

    The `omit` paramter can give a list of names to exclude.

    Returns an unsorted list of strings.
    """
    ifaces = set((iface,))
    # Collect all interfaces (also bases) recursively
    while True:
        ext_ifaces = set(ifaces)
        for iface in ext_ifaces:
            ext_ifaces = set.union(ext_ifaces, set(iface.getBases()))
        if ext_ifaces == ifaces:
            # No new interfaces found, list complete
            break
        ifaces = ext_ifaces
    # Collect (filtered) names of collected interfaces
    result = []
    for iface in ifaces:
        for name, descr in iface.namesAndDescriptions():
            if name in omit:
                continue
            if exclude_attribs and descr.__class__ is Attribute:
                continue
            if exclude_methods and isinstance(descr, Method):
                continue
            if name in result:
                continue
            result.append(name)
    return result


def get_sorted_preferred(tuples_iterable, preferred_list):
    """Get a list of tuples (<TITLE>,<TOKEN>) with values in
    `preferred_list` put in front.

    The rest of the tuples iterable is returned in orginal order. This
    is useful for putting default entries on top of (already sorted)
    lists of choice values, for instance when sorting countries and
    their code.

    Sample:

    We have a list of tuples with uppercase 'titles' and lowercase
    'tokens'. This list is already sorted but we want certain values
    of this list to show up before other values. For instance we want
    to see the 'C' entry to come first.

      >>> get_sorted_preferred([('A','a'), ('B','b'), ('C','c')],
      ...                       ['c'])
      (('C', 'c'), ('A', 'a'), ('B', 'b'))

    i.e. the entry with 'c' as second value moved to head of result.

    We can also require multiple entries at head of list:

      >>> get_sorted_preferred([('A','a'), ('B','b'), ('C','c')],
      ...                       ['b', 'c'])
      (('B', 'b'), ('C', 'c'), ('A', 'a'))

    We required the 'b' entry to come before the 'c' entry and then
    the rest of the input list. That's what we got.

    The result is returned as a tuple of tuples to keep order of values.
    """
    result = [None for x in preferred_list]
    for title, code in tuples_iterable:
        if code in preferred_list:
            index = preferred_list.index(code)
            result[index] = (title, code)
        else:
            result.append((title, code))
    return tuple(result)


def now(tz=None):
    """Get current datetime in timezone of `tz`.

    If `tz`, a `tzinfo` instance, is None, UTC time is returned.

    `tz` should be a timezone as defined in pytz.
    """
    return to_timezone(datetime.datetime.utcnow(), tz=tz)


def to_timezone(dt, tz=None):
    """Shift datetime into timezone `tz`.

    If datetime `dt` contains no `tzinfo` (i.e. it is 'naive'), it is
    assumed to be UTC.

    If no `tz` is given, shift to UTC is performed.

    If `dt` is not a datetime.datetime, the input value is returned
    unchanged.
    """
    if not isinstance(dt, datetime.datetime):
        return dt
    if tz is None:
        tz = pytz.utc
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return tz.normalize(dt.tzinfo.normalize(dt).astimezone(tz))


def imghdr_test_fpm(h, f):
    """FPM fileformat test.

    The `fpm` fileformat is the binary fingerprint data as created by
    `libfprint`.
    """
    if len(h) >= 3 and h[:3] == 'FP1':
        return 'fpm'


#: Add test function in stdlib's imghdr tests.
imghdr.tests.append(imghdr_test_fpm)


def get_fileformat(path, bytestream=None):
    """Try to determine the file format of a given media file.

    Although checks done here are not done very thoroughly, they make
    no assumptions about the filetype by looking at its filename
    extension or similar. Instead they check header data to comply
    with common known rules (Magic Words).

    If bytestream is not `None` the `path` is ignored.

    Returns filetype as string (something like ``'jpg'``) if
    file-format can be recognized, ``None`` else.

    Tested recognized filetypes currently are `jpg`, `png`, `fpm`, and
    `pdf`.

    More filetypes (though untested in waeup.kofa) are automatically
    recognized because we deploy the stdlib `imghdr` library. See this
    module's docs for a complete list of filetypes recognized.
    """
    if path is None and bytestream is None:
        return None

    img_type = None
    if bytestream is not None:
        img_type = imghdr.what(path, bytestream)
    else:
        img_type = imghdr.what(path)
    for name, replacement in (('jpeg', 'jpg'), ('tiff', 'tif')):
        if img_type == name:
            img_type = replacement
    return img_type


def check_pdf(bytestream, file):
    """Tell whether a file or bytestream is a PDF file.

    Works as a test/plugin for the stdlib `imghdr` library.
    """
    if file is not None:
        file.seek(0)
        bytestream = file.read(4)
        file.seek(0)

    if bytestream.startswith('%PDF'):
        return 'pdf'
    return None

# register check_pdf as header check function with `imghdr`
if check_pdf not in imghdr.tests:
    imghdr.tests.append(check_pdf)


def merge_csv_files(path1, path2):
    """Merge two CSV files into one (appending).

    CSV data from `path2` will be merged into `path1` csv file. This
    is a bit like 'appending' data from path2 to data from path1.

    The path of the resulting temporary file will be returned.

    In the result file data from `path2` will always come _after_ data
    from `path1`.

    **Caution**: It is the _callers_ responsibility to remove the
    result file (which is created by tempfile.mkstemp) after usage.

    This CSV file merging copes with different column orders in both
    CSV files and even with different column sets in both files.

    Also broken/empty CSV files can be handled.
    """
    # sniff the col names
    try:
        row10 = csv.DictReader(open(path1, 'rb')).next()
    except StopIteration:
        row10 = dict()
    try:
        row20 = csv.DictReader(open(path2, 'rb')).next()
    except StopIteration:
        row20 = dict()
    fieldnames = sorted(list(set(row10.keys() + row20.keys())))
    # now read/write the real data
    reader1 = csv.DictReader(open(path1, 'rb'))
    reader2 = csv.DictReader(open(path2, 'rb'))
    wp, tmp_path = tempfile.mkstemp()
    writer = csv.DictWriter(os.fdopen(wp, 'wb'), fieldnames)
    writer.writerow(dict((x, x) for x in fieldnames))  # header
    for row in reader1:
        writer.writerow(row)
    for row in reader2:
        writer.writerow(row)
    return tmp_path


def product(sequence, start=1):
    """Returns the product of a sequence of numbers (_not_ strings)
    multiplied by the parameter `start` (defaults to 1). If the
    sequence is empty, returns 0.
    """
    if not len(sequence):
        return 0
    result = start
    for item in sequence:
        result *= item
    return result


class NullHandler(logging.Handler):
    """A logging NullHandler.

    Does not log anything. Useful if you want to shut up a log.

    Defined here for backwards compatibility with Python < 2.7.
    """
    def emit(self, record):
        pass


def check_csv_charset(iterable):
    """Check contents of `iterable` regarding valid CSV encoding and
    trailing whitespaces in data.

    `iterable` is expected to be an iterable on _rows_ (not
    chars). This is true for instance for
    filehandlers. `zope.publisher.browser.FileUpload` instances are
    _not_ iterable, unfortunately.

    Returns line num of first illegal char or ``None``. Line nums
    start counting with 1 (not zero). Returns -1 if data contain
    trailing whitespaces (deactivated).
    """
    linenum = 1
    try:
        reader = csv.DictReader(iterable)
        for row in reader:
            linenum += 1
            #for value in row.values():
            #    if value.endswith(' '):
            #        return -1
    except UnicodeDecodeError:
        return linenum
    except:
        return linenum + 1
    return None


class MemInfo(dict):
    """A dict with access to its items like if they are attributes.
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def get_meminfo(src="/proc/meminfo"):
    """Get local memory info as provided in /proc/meminfo.

    Entries in /proc/meminfo are available as MemInfo attributes.

    By default we lookup a file /proc/meminfo. Another path can be
    lines = open(src, 'r').read()passed in as `src` parameter. In this
    case `src` must be a regular file and contain meminfo-style data.

    If the given `src` (or `/proc/meminfo`) are not available, `None`
    lines = open(src, 'r').read()is returned.
    """
    if not os.path.isfile(src):
        return None
    lines = open(src, 'r').read().splitlines()
    result = MemInfo()
    for line in lines:
        key, value = line.split(':', 1)
        value = int(value.split(' kB', 1)[0])
        result[key] = value
    return result

def html2dict(value=None,portal_language='en'):
    """Transforms a localized HTML text string into a dictionary.

    Different languages must be separated by ``>>xy<<`` whereas
    xy is the language code. Text parts without correct leading
    language separator - usually the first part has no language
    descriptor - are interpreted as texts in the portal's language.
    """
    try:
        parts = value.split('>>')
    except:
        return {}
    elements = {}
    lang = portal_language
    for part in parts:
        if part[2:4] == u'<<':
            lang = str(part[0:2].lower())
            text = part[4:]
            elements[lang] = renderElement(u'div id="html"',
                contents=text)
        else:
            text = part
            elements[lang] = renderElement(u'div id="html"',
                contents=text)
    return elements

def rest2dict(value=None,portal_language='en'):
    """Transforms a localized REST text string into a dictionary.

    Different languages must be separated by ``>>xy<<``` whereas
    xy is the language code. Text parts without correct leading
    language separator - usually the first part has no language
    descriptor - are interpreted as texts in the portal's language.
    """
    try:
        parts = value.split('>>')
    except:
        return {}
    elements = {}
    lang = portal_language
    for part in parts:
        if part[2:4] == u'<<':
            lang = str(part[0:2].lower())
            text = part[4:]
            elements[lang] = renderElement(u'div id="rest"',
                contents=ReST2HTML(text))
        else:
            text = part
            elements[lang] = renderElement(u'div id="rest"',
                contents=ReST2HTML(text))
    return elements



class FormVarParser(HTMLParser):
    """An HTML form parser that extracts keys and values.

       Fed with an HTML document, we parse all starttags and check for each,
       whether it provides a `name` and a `value` attribute. If so, the
       values of the respective attributes are stored in instance var
       `form_vars` as a dict entry.
    """

    def __init__(self):
        HTMLParser.__init__(self)  # old-style class - no super()
        self.form_vars = {}

    def handle_starttag(self, tag, attrs):
        tag_attrs = {}
        for key, val in attrs:
            tag_attrs[key] = val
        if 'name' in tag_attrs and 'value' in tag_attrs:
            self.form_vars[tag_attrs['name']] = unicode(tag_attrs['value'])


def extract_formvars(html_code):
    """Extract keys and values from an HTML form as dict.

       No text, no values::

         >>> extract_formvars("")
         {}

       Simple input tags normally provide name and value::

         >>> extract_formvars("<input type='text' name='foo' value='bar'>")
         {'foo': u'bar'}

       The sample doc we stored in tests is a bit more difficult::

         >>> html_path = os.path.join(os.path.dirname(__file__),
         ...                          'tests', 'sample_response.html')
         >>> html_code = open(html_path, 'r').read()
         >>> import pprint
         >>> pprint.pprint(extract_formvars(html_code))
         {'AMOUNT': u'100',
         ...
          'TRANS_NUM': u'01ESA20190916134824YA3YJ8'}

    """
    result = {}
    parser = FormVarParser()
    parser.feed(html_code)
    return parser.form_vars


def get_catalog_docids(cat):
    """Get all docids for a given catalog `cat`.

    Catalogs store the ids of objects they index. Get all of these object ids.
    This function works at least for catalogs that provide field- and text
    indexes only.
    """
    result = []
    for index in cat.values():
        try:
            # FieldIndexes
            result.extend(list(index._rev_index.keys()))
        except AttributeError:
            # TextIndexes
            result.extend(list(index.index._docwords.keys()))
    return set(result)


def reindex_cat(cat):
    """Reindex all objects stored in a catalog `cat`.

    Regular catalogs try to reindex all stored object ids of a ZODB when asked
    to reindex all contents. That can be overkill. This function reindexes only
    those objects, that were already stored in a catalog. It was tested for
    catalogs with at least 650000 objects.

    Please note, that reindexing catalgos, can take a considerable amount of
    time. 100.000 objects took about 12 minutes to reindex on a 16 GB machine.
    """
    d1 = datetime.datetime.now()
    print("Collecting doc ids...")
    uidutil = getUtility(IIntIds, context=cat)
    uids = get_catalog_docids(cat)
    print("Found %s entries..." % len(uids))
    for n, docid in enumerate(uids):
        ob = uidutil.getObject(docid)
        cat.index_doc(docid, ob)
        # indexes can become huge. commit changes every 5000th round to
        # keep the memory footprint of catalogs `updateIndex` manageable
        if not n % 5000:
            transaction.commit()
    d2 = datetime.datetime.now()
    print("Finished. %s" % (d2 - d1))
