import atexit
import base64
import importlib.abc
from importlib.machinery import (
    ModuleSpec,
    ExtensionFileLoader,
    SourceFileLoader,
    SourcelessFileLoader,
    SOURCE_SUFFIXES,
    BYTECODE_SUFFIXES,
    EXTENSION_SUFFIXES,
)
from importlib.util import spec_from_file_location
import os
import shutil
import sys
import tempfile
from typing import List
import warnings

from cryptography.hazmat.primitives.ciphers.aead import AESOCB3
from cryptography.exceptions import InvalidTag
import requests

from .models import (
    ChannelEvent,
    EventAction,
)


HOLOGRAPH_MAGIC_PATH_ENTRY = "HOLOGAPH_REMOTE_LOCATION"
TEMP_MAGIC_PATH = "/Users/max.taggart/Developer/Holograph/magic_location"

def tune_in(url: str, channel: str, key: str):
    """
    This function is the entrypoint on the consuming-side of a holograph transmission.
    i.e. users call this function where they wish to consume the code that they are
    writing in a more authoring-friendly environment.
    It hooks into the native python import logic to enable imports from the
    Holograph server.
    """
    key_bytes = base64.b64decode(key.encode())
    # Instantiate the same file loaders that are used by the built-in FileFinder
    extensions = (ExtensionFileLoader, EXTENSION_SUFFIXES)
    source = (SourceFileLoader, SOURCE_SUFFIXES)
    bytecode = (SourcelessFileLoader, BYTECODE_SUFFIXES)
    loader_details = [extensions, source, bytecode]
    # Create the temporary directory where we can store the remote files, this allows
    # us to re-use a lot of the existing logic from the standard FileFinder around
    # caching file contents.
    temp_dir = tempfile.mkdtemp(prefix="holograph-")
    print(f"Temp Dir: {temp_dir}")
    atexit.register(lambda: shutil.rmtree(temp_dir))
    # Add the HolographicFileFinder to the list of path_hooks so that the PathFinder knows about it.
    sys.path_hooks.append(HolographicFileFinder.path_hook(url, channel, key_bytes, temp_dir, *loader_details))
    # Add the HOLOGRAPH_MAGIC_PATH_ENTRY to sys.path. Our HolographicFileFinder will only be asked to
    # find modules if there is an entry in sys.path which is not actually a directory. Otherwise, if the
    # entry in sys.path is a real directory PathFinder will just create a new instance of the regular 
    # FileFinder to handle it, which of course won't know how to communicate with the Holograph server. 
    # But, since HolographicFileFinder knows to look for the HOLOGRAPH_MAGIC_PATH_ENTRY in the module's path
    # its `path_hook` classmethod will return an instance of HolographicFileFinder when it sees the magic 
    # path, that finder will be added to the `sys.path_importer_cache` for the path starting with
    # `HOLOGRAPH_MAGIC_PATH_ENTRY`, and we will have successfully hooked into the existing PathFinder logic.
    sys.path.append(HOLOGRAPH_MAGIC_PATH_ENTRY)
    
class DataIntegrityError(Exception):
    """
    Raised when we encounter an invalid signature for data coming from the holograph server.
    """
    pass

class HolographicFileFinder(importlib.abc.PathEntryFinder):

    """
    This class is a modified version of the native imporlib.machinery.FileFinder which
    knows how to ask the Holograph server for updates before determining whether or not
    it can find the requested module. It also knows to look for module paths that start
    with the `HOLOGRAPH_MAGIC_PATH_ENTRY` and manipulates the module path in the 
    ModuleSpec to start with `HOLOGRAPH_MAGIC_PATH_ENTRY` so that sub-modules are also
    imported using an instance of this class.
    """

    def __init__(self, path: str, url, channel, key, temp_dir, *loader_details):
        """Initialize with the path to search on and a variable number of
        2-tuples containing the loader and the file suffixes the loader
        recognizes."""
        loaders = []
        for loader, suffixes in loader_details:
            loaders.extend((suffix, loader) for suffix in suffixes)
        self._loaders = loaders
        # The `path` variable passed to us will start with `HOLOGRAPH_MAGIC_PATH_ENTRY`, 
        # but we need to convert that into an actual path that starts with `temp_dir`.
        path_end = path.replace(HOLOGRAPH_MAGIC_PATH_ENTRY, "")
        # Note that if path_end starts with a "/" then os.path.join will just return path_end
        # since it interprets it as an absolute path.
        if len(path_end) > 0 and path_end[0] == "/":
            path_end = path_end[1:]
        self.path = os.path.join(temp_dir, path_end)
        self._path_mtime = -1
        self._path_cache = set()
        self._relaxed_path_cache = set()
        self._url = url
        self._channel = channel
        self._decryptor = AESOCB3(key)
        self._temp_dir = temp_dir

    def invalidate_caches(self):
        """Invalidate the directory mtime."""
        self._path_mtime = -1

    def find_module(self, fullname):
        """Try to find a loader for the specified module by delegating to
        self.find_loader().

        This method is deprecated in favor of finder.find_spec().

        """
        warnings.warn("find_module() is deprecated and "
                    "slated for removal in Python 3.12; use find_spec() instead",
                    DeprecationWarning)
        # Call find_loader(). If it returns a string (indicating this
        # is a namespace package portion), generate a warning and
        # return None.
        loader, portions = self.find_loader(fullname)
        if loader is None and len(portions):
            msg = 'Not importing directory {}: missing __init__'
            warnings.warn(msg.format(portions[0]), ImportWarning)
        return loader

    def find_loader(self, fullname):
        """Try to find a loader for the specified module, or the namespace
        package portions. Returns (loader, list-of-portions).

        This method is deprecated.  Use find_spec() instead.

        """
        warnings.warn("FileFinder.find_loader() is deprecated and "
                       "slated for removal in Python 3.12; use find_spec() instead",
                       DeprecationWarning)
        spec = self.find_spec(fullname)
        if spec is None:
            return None, []
        return spec.loader, spec.submodule_search_locations or []

    def _get_spec(self, loader_class, fullname, path, smsl, target):
        loader = loader_class(fullname, path)
        module_spec = spec_from_file_location(fullname, path, loader=loader,
                                       submodule_search_locations=smsl)
        if module_spec is None:
            return None
        # If we found the module then make sure to overwrite its __path__ so that it starts
        # with our magic path entry, otherwise if this module is really a package then any
        # sub-packages will be imported using the actual path, which will cause the MetaPathFinder
        # to use a regular FileFinder, which will be able to find the file, but won't trigger
        # a call to the server to update the local filesystem with remote changes.
        # According to the importlib documentation for ModuleSpecs
        # (https://docs.python.org/3/library/importlib.html#importlib.machinery.ModuleSpec) 
        # the `submodule_search_locations` attribute is what is used for the module's __path__
        # attribute, which is what is passed to the MetaPathFinder when importing a sub-module
        # from a package. Quoting the docs, this attribute is
        # 
        # "The list of locations where the package’s submodules will be found. Most of the time this 
        # is a single directory. The finder should set this attribute to a list, even an empty one, 
        # to indicate to the import system that the module is a package. It should be set to None 
        # for non-package modules. It is set automatically later to a special object for namespace 
        # packages.""
        # 
        # So if it is already set to None we will just leave it as is, but if it is a list then we
        # know that the module is actually a package, in which case we need to overwrite the entries
        # in the list so they start with our magic location.
        if module_spec.submodule_search_locations is None:
            return module_spec
        # Make sure the temp_dir does not end in a slash so that when we replace the temp_dir
        # name with our magic path entry we don't pull out the slash that we need to separate 
        # the magic path entry from the first actual filename or directory.
        temp_dir = self._temp_dir
        if temp_dir[-1] == "/":
            temp_dir = temp_dir[:-1]
        for i, location in enumerate(module_spec.submodule_search_locations):
            if self._temp_dir in location:
                module_spec.submodule_search_locations[i] = location.replace(self._temp_dir, HOLOGRAPH_MAGIC_PATH_ENTRY)
        return module_spec

    def find_spec(self, fullname, target=None):
        """Try to find a spec for the specified module.

        Returns the matching spec, or None if not found.
        """
        self._apply_remote_updates()
        is_namespace = False
        tail_module = fullname.rpartition('.')[2]
        try:
            mtime = os.stat(self.path or os.getcwd()).st_mtime
        except OSError:
            mtime = -1
        if mtime != self._path_mtime:
            self._fill_cache()
            self._path_mtime = mtime
        # # tail_module keeps the original casing, for __file__ and friends
        # if _relax_case():
        #     cache = self._relaxed_path_cache
        #     cache_module = tail_module.lower()
        # else:
        #     cache = self._path_cache
        #     cache_module = tail_module
        
        cache = self._path_cache
        cache_module = tail_module
        # Check if the module is the name of a directory (and thus a package).
        # This line is here to help keep the typechecker happy
        base_path = ""
        if cache_module in cache:
            base_path = os.path.join(self.path, tail_module)
            for suffix, loader_class in self._loaders:
                init_filename = '__init__' + suffix
                full_path = os.path.join(base_path, init_filename)
                if os.path.isfile(full_path):
                    return self._get_spec(loader_class, fullname, full_path, [base_path], target)
            else:
                # If a namespace package, return the path if we don't
                #  find a module in the next section.
                is_namespace = os.path.isdir(base_path)
        # Check for a file w/ a proper suffix exists.
        for suffix, loader_class in self._loaders:
            try:
                full_path = os.path.join(self.path, tail_module + suffix)
            except ValueError:
                return None
            # _verbose_message('trying {}', full_path, verbosity=2)
            if cache_module + suffix in cache:
                if os.path.isfile(full_path):
                    return self._get_spec(loader_class, fullname, full_path,
                                          None, target)
        if is_namespace:
            # _verbose_message('possible namespace for {}', base_path)
            spec = ModuleSpec(fullname, None)
            spec.submodule_search_locations = [base_path]
            return spec
        return None

    def _fill_cache(self):
        """Fill the cache of potential modules and packages for this directory."""
        path = self.path
        try:
            contents = os.listdir(path or os.getcwd())
        except (FileNotFoundError, PermissionError, NotADirectoryError):
            # Directory has either been removed, turned into a file, or made
            # unreadable.
            contents = []
        # We store two cached versions, to handle runtime changes of the
        # PYTHONCASEOK environment variable.
        if not sys.platform.startswith('win'):
            self._path_cache = set(contents)
        else:
            # Windows users can import modules with case-insensitive file
            # suffixes (for legacy reasons). Make the suffix lowercase here
            # so it's done once instead of for every import. This is safe as
            # the specified suffixes to check against are always specified in a
            # case-sensitive manner.
            lower_suffix_contents = set()
            for item in contents:
                name, dot, suffix = item.partition('.')
                if dot:
                    new_name = '{}.{}'.format(name, suffix.lower())
                else:
                    new_name = name
                lower_suffix_contents.add(new_name)
            self._path_cache = lower_suffix_contents
        # if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):
        #     self._relaxed_path_cache = {fn.lower() for fn in contents}

    def _apply_remote_updates(self):
        """
        Get any updates for this channel from the Holograph server, including
        decrypting and checking the signature of the updates.
        """
        url = f"{self._url}/channel/{self._channel}/updates"
        response = requests.get(url)
        response.raise_for_status()
        body_json: List[dict] = response.json()
        for d in body_json:
            event = ChannelEvent.from_dict(d)
            # Make sure the signature is valid
            try:
                file_contents = self._decryptor.decrypt(event.nonce, event.contents, event.filepath.encode())
            except InvalidTag:
                # Either the cyphertext or the path changed
                raise DataIntegrityError(
                    "One of the source files retrieved from the Holograph server has been "
                    "altered en-route after leaving the source filesystem. "
                    "Please open a new channel and re-initialize your Holograph connection."
                    f"(Suspicious file: {event.filepath})"
                )
            filepath = os.path.join(self._temp_dir, event.filepath)
            if event.action in [EventAction.CREATE, EventAction.UPDATE]:
                # We handle CREATE and UPDATE events the same because the server will send as an UPDATE event
                # for a file we have never seen before if that file was both created and updated since the last
                # time we asked for udpates (similar to the case where a file is both created and deleted in 
                # between udpates as explained below).
                # Make sure the intermediate directories exist first
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                # Then write the file
                with open(filepath, 'wb') as h:
                    h.write(file_contents)
            elif event.action == EventAction.DELETE:
                # The Holograph server does not keep track of the state of the filesystem on the consuming end.
                # This means that if a file on the producing end was both created and deleted since we last asked 
                # for updates from the server then the server will send us a "DELETE" event for that file, even
                # though the file was never present on the consuming filesystem. So we simply need to check for
                # the existence of the file before asking the operating system to delete it in case we are in
                # this situation.
                if os.path.exists(filepath):
                    os.remove(filepath)




    @classmethod
    def path_hook(cls, url, channel, key, temp_dir, *loader_details):
        """A class method which returns a closure to use on sys.path_hook
        which will return an instance using the specified loaders and the path
        called on the closure.

        If the path called on the closure is not a directory, ImportError is
        raised.

        """
        def path_hook_for_HolographicFileFinder(path: str):
            """Path hook for for the file finder used by Holograph."""
            # We hook into the import machinery by adding a dummy path to sys.path
            # which we look for here. The first time the import machinery looks
            # for a module that is at the top-level of our remote package it will 
            # pass `path == HOLOGRAPHIC_MAGIC_PATH_ENTRY`, which will be our queue
            # to return an instance of this class which knows how to look for modules
            # that are coming from the Holograph server. For child modules the path
            # will start with `HOLOGRAPHIC_MAGIC_PATH_ENTRY`.
            if not path.startswith(HOLOGRAPH_MAGIC_PATH_ENTRY):
                raise ImportError(f'the HolographicFileFinder only handles modules at the magic "{HOLOGRAPH_MAGIC_PATH_ENTRY}" path.')
            return cls(path, url, channel, key, temp_dir, *loader_details)

        return path_hook_for_HolographicFileFinder

    def __repr__(self):
        return 'HolographicFileFinder({!r})'.format(self.path)


# # Taken from Lib/importlib/_bootstrap_external.py:54 (branch 3.10)
# _CASE_INSENSITIVE_PLATFORMS_STR_KEY = 'win',
# _CASE_INSENSITIVE_PLATFORMS_BYTES_KEY = 'cygwin', 'darwin'
# _CASE_INSENSITIVE_PLATFORMS =  (_CASE_INSENSITIVE_PLATFORMS_BYTES_KEY
#                                 + _CASE_INSENSITIVE_PLATFORMS_STR_KEY)
# def _make_relax_case():
#     if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):
#         if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS_STR_KEY):
#             key = 'PYTHONCASEOK'
#         else:
#             key = b'PYTHONCASEOK'

#         def _relax_case():
#             """True if filenames must be checked case-insensitively and ignore environment flags are not set."""
#             return not sys.flags.ignore_environment and key in os.environ
#     else:
#         def _relax_case():
#             """True if filenames must be checked case-insensitively."""
#             return False
#     return _relax_case

# _relax_case = _make_relax_case()

# # Taken from Lib/importlib/_bootstrap.py:244 (branch 3.10)
# def _verbose_message(message, *args, verbosity=1):
#     """Print the message to stderr if -v/PYTHONVERBOSE is turned on."""
#     if sys.flags.verbose >= verbosity:
#         if not message.startswith(('#', 'import ')):
#             message = '# ' + message
#         print(message.format(*args), file=sys.stderr)