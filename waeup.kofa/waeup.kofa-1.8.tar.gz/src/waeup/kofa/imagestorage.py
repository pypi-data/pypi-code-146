## $Id: imagestorage.py 11480 2014-03-08 06:08:04Z henrik $
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
"""A storage for image (and other) files.

A few words about storing files with ``waeup.kofa``. The need for this
feature arised initially from the need to store passport files for
applicants and students. These files are dynamic (can be changed
anytime), mean a lot of traffic and cost a lot of memory/disk space.

**Design Basics**

While one *can* store images and similar 'large binary objects' aka
blobs in the ZODB, this approach quickly becomes cumbersome and
difficult to understand. The worst approach here would be to store
images as regular byte-stream objects. ZODB supports this but
obviously access is slow (data must be looked up in the one
``Data.fs`` file, each file has to be sent to the ZEO server and back,
etc.).

A bit less worse is the approach to store images in the ZODB but as
Blobs. ZODB supports storing blobs in separate files in order to
accelerate lookup/retrieval of these files. The files, however, have
to be sent to the ZEO server (and back on lookups) which means a
bottleneck and will easily result in an increased number of
``ConflictErrors`` even on simple reads.

The advantage of both ZODB-geared approaches is, of course, complete
database consistency. ZODB will guarantee that your files are
available under some object name and can be handled as any other
Python object.

Another approach is to leave the ZODB behind and to store images and
other files in filesystem directly. This is faster (no ZEO contacts,
etc.), reduces probability of `ConflictErrors`, keeps the ZODB
smaller, and enables direct access (over filesystem) to the
files. Furthermore steps might be better understandable for
third-party developers. We opted for this last option.

**External File Store**

Our implementation for storing-files-API is defined in
:class:`ExtFileStore`. An instance of this file storage (which is also
able to store non-image files) is available at runtime as a global
utility implementing :class:`waeup.kofa.interfaces.IExtFileStore`.

The main task of this central component is to maintain a filesystem
root path for all files to be stored. It also provides methods to
store/get files under certain file ids which identify certain files
locally.

So, to store a file away, you can do something like this:

  >>> from StringIO import StringIO
  >>> from zope.component import getUtility
  >>> from waeup.kofa.interfaces import IExtFileStore
  >>> store = getUtility(IExtFileStore)
  >>> store.createFile('myfile.txt', StringIO('some file content'))

All you need is a filename and the file-like object containing the
real file data.

This will store the file somewhere (you shouldn't make too much
assumptions about the real filesystem path here).

Later, we can get the file back like this:

  >>> store.getFile('myfile')
  <open file ...>

Please note, that we ask for ``myfile`` instead of ``myfile.jpg`` as
the file id should not make a difference for different filename
extensions. The file id for ``sample.jpg`` thus could simply be
``sample``.

What we get back is a file or file-like object already opened for
reading:

  >>> store.getFile('myfile').read()
  'some file content'

**Handlers: Special Places for Special Files**

The file store supports special handling for certain files. For
example we want applicant images to be stored in a different directory
than student images, etc. Because the file store cannot know all
details about these special treatment of certain files, it looks up
helpers (handlers) to provide the information it needs for really
storing the files at the correct location.

That a file stored in filestore needs special handling can be
indicated by special filenames. These filenames start with a marker like
this::

  __<MARKER-STRING>__real-filename

Please note the double underscores before and after the marker
string. They indicate that all in between is a marker.

If you store a file in file store with such a filename (we call this a
`file_id` to distuingish it from real world filenames), the file store
will look up a handler for ``<MARKER-STRING>`` and pass it the file to
store. The handler then will return the internal path to store the
file and possibly do additional things as well like validating the
file or similar.

Examples for such a file store handler can be found in the
:mod:`waeup.kofa.applicants.applicant` module. Please see also the
:class:`DefaultFileStoreHandler` class below for more details.

The file store looks up handlers by utility lookups: it looks for a
named utiliy providing
:class:`waeup.kofa.interfaces.IFileStoreHandler` and named like the
marker string (without leading/trailing underscores) in lower
case. For example if the file id would be

  ``__IMG_USER__manfred``

then the looked up utility should be registered under name

  ``img_user``

and provide :class:`waeup.kofa.interfaces.IFileStoreHandler`. If no
such utility can be found, a default handler is used instead
(see :class:`DefaultFileStoreHandler`).

**About File IDs and Filenames**

In the waeup.kofa package we want to store documents like CVs,
photographs, and similar. Each of this documents might come into the
system with different filename extensions. This could be a problem as
the browser components might have to set different response headers
for different filetypes and we nevertheless want to make sure that
only one file is stored per document. For instance we don't want
``passport.jpg`` *and* ``passport.png`` but only one of them.

The default components like :class:`DefaultFileStoreHandler` take care
of this by searching the filesystem for already existing files with
same file id and eventually removing them.

Therefore file ids should never include filename extensions (except if
you only support exactly one filename extension for a certain
document). The only part where you should add an extension (and it is
important to do so) is when creating new files: when a file was
uploaded you can pass in the filename (including the filename
extension) and the file stored in external file store will (most
probably) have a different name but the same extension as the original
file.

When looking for the file, you however only have to give the file id
and the handlers should find the right file for you, regardless of the
filename extension it has.

**Context Adapters: Knowing Your Family**

Often the internal filename or file id of a file depends on a
context. For example when we store passport photographs of applicants,
then each image belongs to a certain applicant instance. It is not
difficult to maintain such a connection manually: Say every applicant
had an id, then we could put this id into the filename as well and
would build the filename to store/get the connected file by using that
filename. You then would create filenames of a format like this::

  __<MARKER-STRING>__applicant0001

where ``applicant0001`` would tell exactly which applicant you can see
on the photograph. You notice that the internal file id might have
nothing to do with once uploaded filenames. The id above could have
been uploaded with filename ``manfred.jpg`` but with the new file id
we are able to find the file again later.

Unfortunately it might soon get boring or cumbersome to retype this
building of filenames for a certain type of context, especially if
your filenames take more of the context into account than only a
simple id.

Therefore you can define filename building for a context as an adapter
that then could be looked up by other components simply by doing
something like:

  >>> from waeup.kofa.interfaces import IFileStoreNameChooser
  >>> file_id = IFileStoreNameChooser(my_context_obj)

If you later want to change the way file ids are created from a
certain context, you only have to change the adapter implementation
accordingly.

Note, that this is only a convenience component. You don't have to
define context adapters but it makes things easier for others if you
do, as you don't have to remember the exact file id creation method
all the time and can change things quick and in only one location if
you need to do so.

Please see the :class:`FileStoreNameChooser` default implementation
below for details.

"""
import glob
import grok
import os
import tempfile
from hurry.file import HurryFile
from hurry.file.interfaces import IFileRetrieval
from zope.component import queryUtility
from zope.interface import Interface
from waeup.kofa.interfaces import (
    IFileStoreNameChooser, IExtFileStore, IFileStoreHandler,)

class FileStoreNameChooser(grok.Adapter):
    """Default file store name chooser.

    File store name choosers pick a file id, a string, for a certain
    context object. They are normally registered as adapters for a
    certain content type and know how to build the file id for this
    special type of context.

    Provides the :class:`waeup.kofa.interfaces.IFileStoreNameChooser`
    interface.

    This default file name chosser accepts almost every name as long
    as it is a string or unicode object.
    """
    grok.context(Interface)
    grok.implements(IFileStoreNameChooser)

    def checkName(self, name, attr=None):
        """Check whether a given name (file id) is valid.

        Raises a user error if the name is not valid.

        For the default file store name chooser any name is valid as
        long as it is a string.

        The `attr` is not taken into account here.
        """
        if isinstance(name, basestring):
            return True
        return False

    def chooseName(self, name, attr=None):
        """Choose a unique valid file id for the object.

        The given name may be taken into account when choosing the
        name (file id).

        chooseName is expected to always choose a valid name (that
        would pass the checkName test) and never raise an error.

        For this default name chooser we return the given name if it
        is valid or ``unknown_file`` else. The `attr` param is not
        taken into account here.
        """
        if self.checkName(name):
            return name
        return u'unknown_file'

class ExtFileStore(object):
    """External file store.

    External file stores are meant to store files 'externally' of the
    ZODB, i.e. in filesystem.

    Most important attribute of the external file store is the `root`
    path which gives the path to the location where files will be
    stored within.

    By default `root` is a ``'media/'`` directory in the root of the
    datacenter root of a site.

    The `root` attribute is 'read-only' because you normally don't
    want to change this path -- it is dynamic. That means, if you call
    the file store from 'within' a site, the root path will be located
    inside this site (a :class:`waeup.kofa.University` instance). If
    you call it from 'outside' a site some temporary dir (always the
    same during lifetime of the file store instance) will be used. The
    term 'temporary' tells what you can expect from this path
    persistence-wise.

    If you insist, you can pass a root path on initialization to the
    constructor but when calling from within a site afterwards, the
    site will override your setting for security measures. This way
    you can safely use one file store for different sites in a Zope
    instance simultanously and files from one site won't show up in
    another.

    An ExtFileStore instance is available as a global utility
    implementing :class:`waeup.kofa.interfaces.IExtFileStore`.

    To add and retrieve files from the storage, use the appropriate
    methods below.
    """

    grok.implements(IExtFileStore)

    _root = None

    @property
    def root(self):
        """Root dir of this storage.

        The root dir is a readonly value determined dynamically. It
        holds media files for sites or other components.

        If a site is available we return a ``media/`` dir in the
        datacenter storage dir.

        Otherwise we create a temporary dir which will be remembered
        on next call.

        If a site exists and has a datacenter, it has always
        precedence over temporary dirs, also after a temporary
        directory was created.

        Please note that retrieving `root` is expensive. You might
        want to store a copy once retrieved in order to minimize the
        number of calls to `root`.

        """
        site = grok.getSite()
        if site is not None:
            root = os.path.join(site['datacenter'].storage, 'media')
            return root
        if self._root is None:
            self._root = tempfile.mkdtemp()
        return self._root

    def __init__(self, root=None):
        self._root = root
        return

    def _pathFromFileID(self, file_id):
        """Helper method to create filesystem path from FileID.

        Used class-internally. Do not rely on this method when working
        with an :class:`ExtFileStore` instance from other components.
        """
        marker, filename, base, ext = self.extractMarker(file_id)
        handler = queryUtility(IFileStoreHandler, name=marker,
                               default=DefaultFileStoreHandler())
        path = handler.pathFromFileID(self, self.root, file_id)
        return path

    def getFile(self, file_id):
        """Get a file stored under file ID `file_id`.

        Returns a file already opened for reading.

        If the file cannot be found ``None`` is returned.

        This methods takes into account registered handlers for any
        marker put into the file_id.

        .. seealso:: :class:`DefaultFileStoreHandler`
        """
        path = self._pathFromFileID(file_id)
        if not os.path.exists(path):
            return None
        fd = open(path, 'rb')
        return fd

    def getFileByContext(self, context, attr=None):
        """Get a file for given context.

        Returns a file already opened for reading.

        If the file cannot be found ``None`` is returned.

        This method takes into account registered handlers and file
        name choosers for context types to build an intermediate file
        id for the context and `attr` given.

        Both, `context` and `attr` are used to find (`context`)
        and feed (`attr`) an appropriate file name chooser.

        This is a convenience method that internally calls
        :meth:`getFile`.

        .. seealso:: :class:`FileStoreNameChooser`,
                     :class:`DefaultFileStoreHandler`.
        """
        file_id = IFileStoreNameChooser(context).chooseName(attr=attr)
        return self.getFile(file_id)

    def deleteFile(self, file_id):
        """Delete file stored under `file_id` in storage.

        The file is physically removed from filesystem.
        """
        path = self._pathFromFileID(file_id)
        if not os.path.exists(path) or not os.path.isfile(path):
            return
        os.unlink(path)
        return

    def deleteFileByContext(self, context, attr=None):
        """Remove file identified by `context` and `attr` if it exists.

        This method takes into account registered handlers and file
        name choosers for context types to build an intermediate file
        id for the context and `attr` given.

        Both, `context` and `attr` are used to find (`context`)
        and feed (`attr`) an appropriate file name chooser.

        This is a convenience method that internally calls
        :meth:`getFile`.

        .. seealso:: :class:`FileStoreNameChooser`,
                     :class:`DefaultFileStoreHandler`.

        """
        file_id = IFileStoreNameChooser(context).chooseName(attr=attr)
        return self.deleteFile(file_id)

    def createFile(self, filename, f):
        """Store a file.
        """
        root = self.root # Calls to self.root are expensive
        file_id = os.path.splitext(filename)[0]
        marker, filename, base, ext = self.extractMarker(filename)
        handler = queryUtility(IFileStoreHandler, name=marker,
                               default=DefaultFileStoreHandler())
        f, path, file_obj = handler.createFile(
            self, root, filename, file_id, f)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname, 0755)
        open(path, 'wb').write(f.read())
        return file_obj

    def extractMarker(self, file_id):
        """split filename into marker, filename, basename, and extension.

        A marker is a leading part of a string of form
        ``__MARKERNAME__`` followed by the real filename. This way we
        can put markers into a filename to request special processing.

        Returns a quadruple

          ``(marker, filename, basename, extension)``

        where ``marker`` is the marker in lowercase, filename is the
        complete trailing real filename, ``basename`` is the basename
        of the filename and ``extension`` the filename extension of
        the trailing filename. See examples below.

        Example:

           >>> extractMarker('__MaRkEr__sample.jpg')
           ('marker', 'sample.jpg', 'sample', '.jpg')

        If no marker is contained, we assume the whole string to be a
        real filename:

           >>> extractMarker('no-marker.txt')
           ('', 'no-marker.txt', 'no-marker', '.txt')

        Filenames without extension give an empty extension string:

           >>> extractMarker('no-marker')
           ('', 'no-marker', 'no-marker', '')

        """
        if not isinstance(file_id, basestring) or not file_id:
            return ('', '', '', '')
        parts = file_id.split('__', 2)
        marker = ''
        if len(parts) == 3 and parts[0] == '':
            marker = parts[1].lower()
            file_id = parts[2]
        basename, ext = os.path.splitext(file_id)
        return (marker, file_id, basename, ext)

grok.global_utility(ExtFileStore, provides=IExtFileStore)

class DefaultStorage(ExtFileStore):
    """Default storage for files.

    Registered globally as utility for
    :class:`hurry.file.interfaces.IFileRetrieval`.
    """
    grok.provides(IFileRetrieval)

grok.global_utility(DefaultStorage, provides=IFileRetrieval)

class DefaultFileStoreHandler(grok.GlobalUtility):
    """A default handler for external file store.

    This handler is the fallback called by external file stores when
    there is no or an unknown marker in the file id.

    Registered globally as utility for
    :class:`waeup.kofa.interfaces.IFileStoreHandler`.
    """
    grok.implements(IFileStoreHandler)

    def _searchInPath(self, path):
        """Get complete path of any existing file starting with `path`.

        If no such file can be found, return input path.

        If multiple such files exist, return the first one.

        **Example:**

        Looking for a `path`::

          '/tmp/myfile'

        will find any file like ``'/tmp/myfile.txt'``,
        ``'/tmp/myfile.jpg'`` but also ``'/tmp/myfile_any_attribute.pdf'``,
        if it exists. Therefore we must be careful. File attributes
        must come first: ``'/tmp/any_attribute_myfile.pdf'``
        """
        result = path
        if os.path.isdir(os.path.dirname(path)):
            file_iter = glob.iglob('%s*' % (path,))
            try:
                result = file_iter.next()
            except StopIteration:
                pass
        return result

    def pathFromFileID(self, store, root, file_id):
        """Return a path for getting/storing a file with given file id.

        If there is already a file stored for the given file id, the
        path to this file is returned.

        If no such file exists yet (or the the only file existing has
        no filename extension at all) a path to store the file but
        without any filename extension is returned.
        """
        path = os.path.join(root, file_id)
        return self._searchInPath(path)

    def createFile(self, store, root, filename, file_id, f):
        """Infos about what to store exactly and where.

        When a file should be handled by an external file storage, it
        looks up any handlers (like this one), passes runtime infos
        like the storage object, root path, filename, file_id, and the
        raw file object itself.

        The handler can then change the file, raise exceptions or
        whatever and return the result.

        This handler returns the input file as-is, a path returned by
        :meth:`pathFromFileID` and an instance of
        :class:`hurry.file.HurryFile` for further operations.

        Please note: although a handler has enough infos to store the
        file itself, it should leave that task to the calling file
        store.

        This method does, however, remove any existing files stored
        under the given file id.
        """
        ext = os.path.splitext(filename)[1]
        path = self.pathFromFileID(store, root, file_id)
        base, old_ext = os.path.splitext(path)
        if old_ext != ext:
            if os.path.exists(path):
                os.unlink(path)
            path = base + ext
        return f, path, HurryFile(filename, file_id + ext)
