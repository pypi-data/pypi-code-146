import collections.abc
import importlib
import logging
import os.path

import yaml

CLASS_STORAGE_KEY = '~serialisedclass~'
TUPLE_STORAGE_KEY = '~serialisedtuple~'
SET_STORAGE_KEY = '~serialisedset~'
SERIALISED_STORAGE_KEY = '~serialisedobject~'

_logger = logging.getLogger(__name__)


class SendableMixin:
    """
    baseclass for a "sendable" object, providing methods for conversion to
    yaml format
    """

    def pack(self,
             uuid: str = None,
             file: str = None):
        """
        "packs" the object into a dict-format, ready for yaml-dump

        Args:
            uuid (str):
                optional uuid string to package this data inside
            file (str):
                package to file

        Returns:
            (dict):
                packaged Runner
        """
        # remove any attributes not to be packaged
        # these objects are either not needed, or can be re-created on the
        # recipient end
        never_package = ['_logger', '_logobj']

        do_not_package = {'Dataset': ['_database'],
                          'Runner': ['_serialiser', '_parent', '_database'],
                          'URL': ['_urlutils'],
                          'CMD': ['_subprocess'],
                          'Dependency': ['_network']}

        class_storage = get_class_storage(self)

        # if the object is a subclass, find the name of the parent by getting
        # the mro of the object, and extracting it from the set
        parent_class_names = get_mro_classnames(self)
        sub_block = set(do_not_package) & set(parent_class_names)

        name_to_block = None
        if class_storage['name'] in do_not_package:
            # classname has extra attrs to block
            name_to_block = class_storage['name']
        elif len(sub_block) != 0:
            # parent class has extra attrs to block
            name_to_block = list(sub_block)[0]

        if name_to_block:
            block = never_package + do_not_package[name_to_block]
        else:
            block = never_package

        payload = {}
        for k, v in self.__dict__.items():
            if k in block:
                payload[k] = {CLASS_STORAGE_KEY: {
                                  'mod': 'remotemanager.storage.sendablemixin',
                                  'name': 'Unloaded'}}
                continue

            payload[self.serialise(k)] = self.serialise(v)

        payload[CLASS_STORAGE_KEY] = class_storage

        if uuid:
            if '_uuid' in payload and payload['_uuid'] != uuid:
                raise ValueError('passed uuid and _uuid key in payload do'
                                 'not match!')

            payload['_uuid'] = uuid

            payload = {uuid: payload}

        if file is not None:
            print(f'dumping payload to {file}')
            with open(file, 'w+') as o:
                yaml.dump(payload, o)

            return None
        return payload

    @classmethod
    def unpack(cls,
               data: dict = None,
               file: str = None,
               limit: bool = True):
        """
        Re-create an object from a packaged payload coming from obj.pack

        .. note ::

            use this function to unpack from a payload _outside_ an object

        Args:
            data (dict):
                __dict__ payload from the object that was packaged
            file (str):
                filepath to unpack from, if data is not given
            limit (bool):
                disable to allow outside classes to be unserialised

        Returns:
            re-created object
        """

        if data is None:
            if file is None:
                raise ValueError('please provide a data payload or filepath '
                                 'to read from')
            elif not os.path.isfile(file):
                raise FileNotFoundError(f'could not find file {file}')

            with open(file, 'r') as o:
                data = yaml.safe_load(o)

        # if the data passed is a {uuid: {data}} format dict, search for a uuid
        # within and extract the {data}
        try:
            firstkey = list(data)[0]
            if isinstance(data[firstkey], dict) \
                    and '_uuid' in data[firstkey] \
                    and data[firstkey]['_uuid'] == firstkey:
                data = data[firstkey]
        except IndexError:
            # if there's no keys in data, then we definitely don't have a uuid
            pass

        # create a new instance of this class
        new = cls.__new__(cls)

        # update this object with the values extracted from the payload
        if isinstance(data, str):
            _logger.debug(f'importing from filename {data}')
            data = yaml.safe_load(data)

        # this is REQUIRED to be separate to the return call
        new.inject_payload(data, limit)

        return new

    def inject_payload(self,
                       payload: dict,
                       limit: bool = True):
        """
        inject payload into the __dict__, effectively re-creating the object

        .. note ::
            use this function to unpack _within_ an object

        Args:
            payload (dict):
                __dict__ payload from the object that was packaged
            limit (bool):
                enable or disable safeties
        """
        if isinstance(self, Unloaded):
            return

        if hasattr(self, '_logger'):
            self._logger.info(f'finalising unpacking of {type(self)}')

        # temporary attribute to check for a valid class
        self._unpack_validate = True

        if CLASS_STORAGE_KEY in payload:
            selfkey = get_class_storage(self)
            packkey = payload[CLASS_STORAGE_KEY]

            if selfkey != packkey:
                raise RuntimeError(f'attempting to unpack class '
                                   f'{packkey["name"]} as '
                                   f'{selfkey["name"]}')

            delattr(self, '_unpack_validate')

        for k, v in payload.items():
            self.__dict__[k] = self.unserialise(v, limit)

    def serialise(self,
                  obj):
        """
        Recurse over any iterable objects, or call the pack() method of any
        `SendableMixin` objects, for serialisation

        Args:
            obj:
                object to be packaged

        Returns (yaml-serialisable object):
            yaml-friendly object
        """

        if issubclass(type(obj), SendableMixin):
            payload = obj.pack()
            return payload

        elif isinstance(obj, collections.abc.Mapping):
            # dict type
            try:
                payload = {self.serialise(k):
                           self.serialise(v) for k, v in obj.items()}
                return payload
            except TypeError as e:
                raise ValueError("Possible dict-key. These cause "
                                 f"circular issues with YAML\nOriginal error: "
                                 f"{e}")

        elif isinstance(obj, list):
            # list-type
            return [self.serialise(v) for v in obj]

        elif isinstance(obj, tuple):
            # tuple-type
            return [TUPLE_STORAGE_KEY] + [self.serialise(v) for v in obj]

        elif isinstance(obj, set):
            # set-type
            return [SET_STORAGE_KEY] + [self.serialise(v) for v in obj]

        if basic_available(obj):
            return obj

        try:
            return [SERIALISED_STORAGE_KEY, self.serialiser.dumps(obj)]
        except AttributeError:
            pass

        raise RuntimeError(f'Failed to yaml dump {obj.__class__.__name__} '
                           f'object {obj}')

    def unserialise(self,
                    obj,
                    limit: bool = True):
        """
        Undo a serialised packaging, by importing the called object and calling
        its unpack() method

        Args:
            obj:
                payload to be unpacked
            limit (bool):
                exit if the object to be unpacked is not part of the
                remotemanager package

        Returns:
            object before packaging
        """
        try:
            unpackable = obj.get(CLASS_STORAGE_KEY)
        except AttributeError:
            unpackable = False

        if unpackable:
            # print(f'unserialising unpackable object {obj}')
            # extract the class to import
            source = obj.pop(CLASS_STORAGE_KEY)

            if '_conn' in obj:
                # disable protection for URLs
                limit = False

            # import the module
            modulename = source['mod']
            if limit and not modulename.startswith('remotemanager'):
                raise ValueError('module to import is not within the '
                                 'remotemanager package, exiting for safety')
            mod = importlib.import_module(modulename)

            # now get the actual class to import and unpack
            cls = getattr(mod, source['name'])

            return cls.unpack(obj)

        elif isinstance(obj, collections.abc.Mapping):
            # dict type
            return {self.unserialise(k):
                    self.unserialise(v) for k, v in obj.items()}

        # coming from the yaml file, output should _only_ be list
        elif isinstance(obj, list):
            try:
                if obj[0] == TUPLE_STORAGE_KEY:
                    return tuple(obj[1:])
                elif obj[0] == SET_STORAGE_KEY:
                    return set(obj[1:])
            except IndexError:
                return [self.unserialise(v) for v in obj]

        if basic_available(obj):
            return obj

        return obj

    def is_missing(self, objname: str) -> bool:
        """
        Determine if object with name objname is missing or uninitialised

        Args:
            objname (str): name of the object to look for

        Returns:
            (bool): object presence
        """

        if not hasattr(self, objname):
            return True

        obj = getattr(self, objname)
        if isinstance(obj, Unloaded):
            return True

        if obj is None:
            return True

        return False


class Unloaded(SendableMixin):

    def __init__(self):
        pass

    def __getattr__(self, item):
        pass


def get_class_storage(obj) -> dict:
    """
    Breaks down object into its module and classname.

    Args:
        obj:
            Python object to be broken down

    Returns (dict):
        module and classname dict
    """
    return {'mod': obj.__module__,
            'name': obj.__class__.__name__}


def get_mro_classnames(obj) -> list:
    return [subobj.__name__ for subobj in obj.__class__.__mro__]


def basic_available(obj):
    # attempt a serialisation, if it does not have a yaml constructor tag
    # we're probably safe to skip any further processing
    basic = yaml.dump(obj)
    if not basic.startswith('!!'):
        return True
    return False
