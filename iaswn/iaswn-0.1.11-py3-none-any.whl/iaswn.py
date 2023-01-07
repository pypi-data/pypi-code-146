#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Iaswn Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Iaswn.
#    Iaswn is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Iaswn is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Iaswn.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   Iaswn project : iaswn/iaswn.py

   Main file of the project.

   For the user of this project, the most import class in Iaswn which must be
   the mother class of all JSON-able classes.
   Use encode() to encode and decode() to decode.

   ____________________________________________________________________________

   o  DEFAULT_JSONARGS_ENCODER

   o  class IaswnError
   o  class IaswnDecoder
   o  class IaswnEncoder
   o  class Iaswn

   o  decode(jsonstring)
   o  encode(obj, json_args=None)
   o  diagnostic(obj, details=False)
"""
# We need to verify the type of various objects in this file.
# Therefore we can't use isinstance() which is too broad.
# pylint: disable=unidiomatic-typecheck

# I have chosen not to reduce the length of some of the methods
# in favor of readability and speed.
# pylint: disable=too-many-branches

import base64
import collections
import datetime
import decimal
import importlib
import inspect
import json
import re
import types

# default paramaters given to Iaswn encoder:
# see README.md for more details.
DEFAULT_JSONARGS_ENCODER = {
    "skipkeys": False,
    "ensure_ascii": False,
    "check_circular": True,
    "allow_nan": True,
    "indent": None,
    "separators": None,
    "sort_keys": False,
    }


# (pimydoc)SPECIALATTRIBUTE_PREFIX
# ⋅ This prefix is used to generate special keywords like "|asωñ.t" for
# ⋅ a tuple.
# ⋅
# ⋅ By default SPEIALATTRIBUTE_PREFIX is set to '|asωñ' but you may hange
# ⋅ this value whih don't have to be a valid Python identifier.
# ⋅
# ⋅ Tests have shown that there is little point in shortening this string in
# ⋅ order to redue the length of the json-strings.
# ⋅ It is more interesting to introdue exoticharacters to prevent collision with
# ⋅ the strings stored in the input objets, the lasse names or the attributes
# ⋅ names.
# ⋅ The default string, "|asωñ", voluntarily starts with a harater that can't be
# ⋅ used as a Python identifier in order to protect against collisions.
# ⋅
# ⋅ This string an't be set to :
# ⋅ * "" (empty string)
# ⋅ * "_"
# ⋅ * "objet"
# ⋅ * "at"
# ⋅   ... or anything that might appear in a string like:
# ⋅      "<mymodule.myfilename.Mylass objet at 0x7f71c9a6e1f0>"
# ⋅   Confer DOCDEF001 in iaswn.py to understand why.
# ⋅
# ⋅ This string shouldn't be set to :
# ⋅ * "iaswn", "Iaswn" or similar strings: you have to prevent collisions with
# ⋅   similar strings given in the input objets.
SPECIALATTRIBUTE_PREFIX = "|asωñ"


class IaswnError(Exception):
    """
        IaswnError class

        This exception is raised when Iaswn catches the following exceptions:
        - TypeError
        - json.decoder.JSONDecodeError

        To simplify the errors gestion, these three errors are merged into
        IaswnError.
    """


class IaswnDecoder(json.JSONDecoder):
    """
        IaswnDecoder : json string > object

        _______________________________________________________________________

        Methods:
        o  __init__(self, *args, **kwargs)
        o  _decode(jsonstring)
        o  _decode_bytes(obj)
        o  _decode_dictkey(obj)
        o  _decode_str(obj)
        o  _decode_list(obj)
        o  customed_object_hook(obj)
    """
    def __init__(self,
                 *args,
                 **kwargs):
        """
            IaswnDecoder.__init__()
        """
        json.JSONDecoder.__init__(self,
                                  object_hook=self.customed_object_hook,
                                  *args, **kwargs)

    @staticmethod
    def _decode(jsonstring):
        """
            IaswnDecoder._decode()

            Decode <jsonstring> by calling json.JSONDecoder().decode over it.

            ___________________________________________________________________

            ARGUMENT: the (str)json string to be decoded.

            RETURNED VALUE: the corresponding object.
        """
        return json.JSONDecoder().decode(jsonstring.removeprefix(SPECIALATTRIBUTE_PREFIX+".o"))

    @staticmethod
    def _decode_bytes(obj):
        """
            IaswnDecoder._decode_bytes()

            Transform the bytes <obj> in a string

            ___________________________________________________________________

            ARGUMENT: (bytes) <obj>, the bytes to be transformed.

            RETURNED VALUE: (str) the corresponding string.
        """
        return base64.b64decode(obj)

    @staticmethod
    def _decode_dictkey(obj):
        """
            IaswnDecoder._decode_dictkey()

            Decode dict key <obj> and create the corresponding object.
            Sub-method used by customed_object_hook().

            Please notice that <obj> may be OR NOT a string.

            Confer IaswnEncoder._encode_dictkey().

            ___________________________________________________________________

            ARGUMENT: obj, the dict key to be decoded.

            RETURNED VALUE: the corresponding object.
        """
        if type(obj) is str:
            return IaswnDecoder._decode_str(obj)

        # anything but a string:
        return obj

    @staticmethod
    def _decode_list(obj):
        """
            IaswnDecoder._decode_list()

            Transform the list <obj> in the corresponding object.

            ___________________________________________________________________

            ARGUMENT: (list) <obj>, the list to be transformed.

            RETURNED VALUE: the corresponding object.
        """
        if len(obj) == 0:
            # empty list, we catch this case since we check infra obj[0].
            res = []
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".t":
            res = tuple(IaswnDecoder.customed_object_hook(item) for item in obj[1])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".s":
            res = set(IaswnDecoder.customed_object_hook(item) for item in obj[1])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".f":
            res = frozenset(IaswnDecoder.customed_object_hook(item) for item in obj[1])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".c":
            # obj: e.g. [PREFIX+'.c', 'tests.tests', 'IaswnTests.method', False]
            target = obj[2].split(".")
            target_len = len(target)

            _module = importlib.import_module(obj[1])  # easy part: the module

            # the not so easy part: the name

            # <res> will be e.g. 'tests.tests' then 'tests.tests.IaswnTests'
            #       then 'tests.tests.IaswnTests.method'
            res = _module
            # <_res> is <res> without the last iteration, which will be skipped.
            # So <_res> will be e.g. 'tests.tests' then 'tests.tests.IaswnTests'.
            _res = _module

            for item_index, item in enumerate(target):
                last_item = (item_index == target_len-1)

                if item == "<locals>":
                    # Up to now, functions having "<locals>" in their __qualname__
                    # can't be decoded. Such functions are (among others ?) nested functions
                    raise TypeError(
                        f"Can't decode '{obj}': "
                        "Iaswn doesn't know how to handle functions having "
                        "'<locals'> in their __qualname__, e.g. nested functions.")
                res = res.__dict__[item]
                if not last_item:
                    _res = res
                # If <res> is a static method, it has got a __func__ attribute.
                # In this case, res.__func__ is the information to be stored, not <res> alone.
                #   see https://stackoverflow.com/questions/41921255
                if hasattr(res, "__func__"):
                    res = res.__func__
            # for class methods only:
            if obj[3]:
                # https://stackoverflow.com/questions/46897417/
                res = types.MethodType(res, _res)
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".C":
            res = complex(obj[1], obj[2])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".ty":
            _module = importlib.import_module(obj[1])
            res = getattr(_module, obj[2])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".p":
            res = re.compile(obj[1], flags=obj[2])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".P":
            res = re.compile(
                IaswnDecoder._decode_bytes(obj[1]), flags=obj[2])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".r":
            res = range(obj[1], obj[2], obj[3])  # start, stop, step
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".dd":
            res = collections.defaultdict(IaswnDecoder.customed_object_hook(obj[1]),
                                          IaswnDecoder.customed_object_hook(obj[2]))
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".dt":
            res = datetime.datetime.fromisoformat(obj[1])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".dtD":
            res = datetime.timedelta(days=obj[1], seconds=obj[2], microseconds=obj[3])
        elif obj[0] == SPECIALATTRIBUTE_PREFIX+".dtd":
            res = datetime.date(year=obj[1], month=obj[2], day=obj[3])
        else:
            # a regular list with at least 1 item.
            # <obj> is something like [item1, item2, ...]
            res = list(IaswnDecoder.customed_object_hook(item) for item in obj)

        return res

    @staticmethod
    def _decode_str(obj):
        """
            IaswnDecoder._decode_str()

            Transform the string <obj> in the corresponding object.

            ___________________________________________________________________

            ARGUMENT: (str) <obj>, the str[ing] to be transformed.

            RETURNED VALUE: the corresponding object.
        """
        if obj == SPECIALATTRIBUTE_PREFIX+".n":
            res = None
        elif obj == SPECIALATTRIBUTE_PREFIX+".1":
            res = True
        elif obj == SPECIALATTRIBUTE_PREFIX+".0":
            res = False
        elif obj == SPECIALATTRIBUTE_PREFIX+".t0":
            res = tuple()
        elif obj == SPECIALATTRIBUTE_PREFIX+".s0":
            res = set()
        elif obj == SPECIALATTRIBUTE_PREFIX+".f0":
            res = frozenset()
        elif obj.startswith(SPECIALATTRIBUTE_PREFIX+".i"):
            res = int(obj.removeprefix(SPECIALATTRIBUTE_PREFIX+".i"))
        elif obj.startswith(SPECIALATTRIBUTE_PREFIX+".F"):
            res = float(obj.removeprefix(SPECIALATTRIBUTE_PREFIX+".F"))
        elif obj.startswith(SPECIALATTRIBUTE_PREFIX+".o"):
            # Some very special cases:
            res = IaswnDecoder.customed_object_hook(IaswnDecoder._decode(obj))
            if type(res) is tuple and len(res) > 0:
                # Strictly speaking this "if" isn't mandatory but it avoids the following problem:
                # | if res[0] is a class object, the following checks, like:
                # |     if res[0] == SPECIALATTRIBUTE_PREFIX+".p"
                # | will call the __eq__() method of this class object. Some class objects
                # | have no __eq__() method, so let's avoid this situation.
                if type(res[0]) is str:
                    #  re.Pattern is encoded as "|asωñ.o[\"|asωñ.t\", [\"|asωñ.p\", \".*\", 32]]"
                    # the IaswnDecoder.customed_object_hook(IaswnDecoder._decode() line above gives:
                    #  res = ("|asωñ.t", ["|asωñ.p", ".*", 32])
                    # We need to decode this tuple, hence the following lines:
                    if res[0] == SPECIALATTRIBUTE_PREFIX+".p":
                        res = re.compile(
                            res[1],
                            flags=res[2])
                    elif res[0] == SPECIALATTRIBUTE_PREFIX+".P":
                        res = re.compile(
                            IaswnDecoder._decode_bytes(res[1]),
                            flags=res[2])
                    #  frozenset() is encoded as "|asωñ.o["|asωñ.t", ["|asωñ.f", [1, 2]]]"
                    # the IaswnDecoder.customed_object_hook(IaswnDecoder._decode() line above gives:
                    #  res = ('|asωñ.f', [1, 2])
                    # We need to decode this tuple, hence the following lines:
                    elif res[0] == SPECIALATTRIBUTE_PREFIX+".f":
                        res = frozenset(res[1])
                    elif res[0] == SPECIALATTRIBUTE_PREFIX+".C":
                        res = complex(res[1], res[2])
                    elif res[0] == SPECIALATTRIBUTE_PREFIX+".r":
                        res = range(res[1], res[2], res[3])
                    elif res[0] == SPECIALATTRIBUTE_PREFIX+".dt":
                        res = datetime.datetime.fromisoformat(res[1])
                    elif res[0] == SPECIALATTRIBUTE_PREFIX+".dtD":
                        res = datetime.timedelta(res[1], res[2], res[3])
                    elif res[0] == SPECIALATTRIBUTE_PREFIX+".dtd":
                        res = datetime.date(res[1], res[2], res[3])
                    else:
                        # Something wrong happened: this line should never be reached.
                        raise TypeError(f"Ill-formed serialized Iaswn object; obj={obj}; res={res}")

            # -----------------------------------------------
            # - PLEASE DO NOT REMOVE THE FOLLOWING COMMENTS -
            # -----------------------------------------------
            #
            #     else:
            #         # simple case: we have to decode a simple tuple like
            #         #  obj == "|asωñ.o["|asωñ.t", [0, 123]]"
            #         #  res == (0, 123)
            #         pass
            # else:
            #     # simple case: we have to decode a class-object like
            #     #    obj == |asωñ.o{"|asωñ": {"name": ["myclass", "MyObject"]}, "xvalue": null}
            #     #    res == MyObject(.xvalue=None)
            #     pass

        elif obj.startswith(SPECIALATTRIBUTE_PREFIX+".b"):
            res = IaswnDecoder._decode_bytes(obj.removeprefix(SPECIALATTRIBUTE_PREFIX+".b"))
        elif obj == SPECIALATTRIBUTE_PREFIX+".no":
            res = NotImplemented
        elif obj.startswith(SPECIALATTRIBUTE_PREFIX+".D"):
            res = decimal.Decimal(obj.removeprefix(SPECIALATTRIBUTE_PREFIX+".D"))
        else:
            res = obj
        return res

    @staticmethod
    def customed_object_hook(obj):
        """
            IaswnDecoder.customed_object_hook()

            Method given as object hook to json.JSONDecoder() : see .__init__().

            ___________________________________________________________________

            ARGUMENT: <obj> may be any object read by ._decode() : int, dict, ...

            RETURNED VALUE: the corresponding object.
        """
        # By default, res = obj and <res> will not be modified.
        # It happens for basic types, e.g. if <obj> is a str[ing].
        res = obj

        # (A.1) The following cases (inside the first if statement) deal with objects
        #       <obj> which are attributes of an object; they don't deal with objects
        #       <obj> which are contained within such an attribute.
        if isinstance(obj, dict) and SPECIALATTRIBUTE_PREFIX in obj:
            # Creation of the class object <res> from data stored in
            # obj[SPECIALATTRIBUTE_PREFIX]['name']

            # Why _type.__new__(_type) and not _type() ?
            # see task-65 in ROADMAP.md
            #
            #    _type() will call __init__() and we don't wan't to call this method:
            #    * we don't want to call __init__() twice (at the creation of the object
            #      and at its re-creation, which may lead to conflicts
            #    * we don't want to add a constraint; indeed, if we call __init__(),
            #      all __init__() arguments must have a default value.
            #
            # cf https://stackoverflow.com/questions/2168964
            _type = getattr(
                importlib.import_module(
                    obj[SPECIALATTRIBUTE_PREFIX]['name'][0]),
                obj[SPECIALATTRIBUTE_PREFIX]['name'][1])
            res = _type.__new__(_type)

            # Let's add class attributes:
            for key, value in obj.items():
                # _setattr:
                # By default, the <key, value> values will be setattr(res, key, new_value)
                # because they correspond to an attribute to be added to the <obj> object.
                # In some cases it is necessary to proceed differently, for example if <key, value>
                # give the list of elements of the internal list of a class derived from the list
                # type.
                _setattr = True  # True if a <new_value> must be setattr()

                # DOC#2: How are inherited-list objects encoded into a json-string ?
                if key == SPECIALATTRIBUTE_PREFIX+".l":
                    _setattr = False
                    for item in value:
                        res.append(IaswnDecoder.customed_object_hook(item))
                elif key == SPECIALATTRIBUTE_PREFIX+".l0":
                    new_value = []
                # DOC#3: How are inherited-dict objects encoded into a json-string ?
                elif key == SPECIALATTRIBUTE_PREFIX+".d":
                    _setattr = False
                    for _key, _value in value:
                        res[IaswnDecoder._decode_dictkey(_key)] = \
                            IaswnDecoder.customed_object_hook(_value)
                elif key == SPECIALATTRIBUTE_PREFIX+".d0":
                    new_value = {}
                elif key == SPECIALATTRIBUTE_PREFIX+".t0":
                    new_value = tuple()
                elif key == SPECIALATTRIBUTE_PREFIX+".s0":
                    new_value = set()
                elif key == SPECIALATTRIBUTE_PREFIX+".f0":
                    new_value = frozenset()

                # ======================================================
                # === <key> has nothing special, let's check <value> ===
                # ======================================================
                else:
                    # ---------------------------------------------------------
                    # <value> is a str and may be:
                    # - either a true str like "my string"
                    # - either a str describing a special object (Iaswn-obj,type, byte)
                    if type(value) is str:
                        new_value = IaswnDecoder._decode_str(value)
                    # ---------------------------------------------------------
                    # <value> is a dict: its keys have to be decoded with the
                    # special method _decode_dictkey().
                    elif type(value) is dict:
                        new_value = {}
                        for valuekey, valuevalue in value.items():
                            new_value[IaswnDecoder._decode_dictkey(valuekey)] = \
                                IaswnDecoder.customed_object_hook(valuevalue)
                    # ---------------------------------------------------------
                    # <value> is a list and may be:
                    # - either a true list like [1, 2]
                    # - either a list describing a special object (tuple, set)
                    #   like ['|asωñ.p', '.*', 32] or
                    #   ['|asωñ.c', 'tests.tests', 'IaswnTests.method'].
                    elif type(value) is list:
                        new_value = IaswnDecoder._decode_list(value)
                    else:
                        #
                        # neither <key> neither <value> are special.
                        #
                        new_value = value

                if _setattr:
                    setattr(res,
                            key,
                            new_value)

            # post-processing ?
            #
            # _iaswn_has_the_postprocessing_been_done() is not really a
            # "protected" member, even if Pylint thinks otherwise.
            # pylint: disable=protected-access
            if not res._iaswn_has_the_postprocessing_been_done():
                res.iaswn_postprocessing()

        # (A.2) The following cases involve <obj> objects that are not directly
        # attributes of an object but are contained within such an attribute.
        elif type(obj) is list:
            res = IaswnDecoder._decode_list(obj)
        elif type(obj) == str:
            res = IaswnDecoder._decode_str(obj)
        elif type(obj) is dict:
            res = {}
            for _objkey, _objvalue in obj.items():
                res[IaswnDecoder._decode_dictkey(_objkey)] = \
                    IaswnDecoder.customed_object_hook(_objvalue)
        # PLEASE DO NOT REMOVE THE FOLLOWING COMMENTS
        # else:
        #     # basic type like str, int, function, ...
        #     pass

        return res


class IaswnEncoder(json.JSONEncoder):
    """
        IaswnEncoder : object -> json string

        _______________________________________________________________________

        Methods:
        o  _encode_dictkey(obj)
        o  _encode(obj)
        o  default(obj)
    """
    @staticmethod
    def _encode_bytes(_string):
        """
            IaswnEncoder._encode_bytes()

            Transform the str <_string> into bytes.

            ___________________________________________________________________

            ARGUMENT: (str) <_string>, the string to be transformed.

            RETURNED VALUE: (bytes) the corresponding bytes.
        """
        return base64.b64encode(_string).decode("ascii")

    @staticmethod
    def _encode_dictkey(obj):
        """
            IaswnEncoder._encode_dictkey()

            Encode dict key object <obj> and create the corresponding json string.

            Cf IaswnDecoder._decode_dictkey().

            ___________________________________________________________________

            ARGUMENT: <obj>, the dict key object to be encoded.

            RETURNED VALUE: (str)the corresponding json string.
        """
        if hasattr(obj, "__dict__"):
            res = IaswnEncoder._encode(obj)
        elif type(obj) is int:
            res = SPECIALATTRIBUTE_PREFIX+".i"+str(obj)
        elif type(obj) is str:
            res = obj
        elif type(obj) is float:
            res = SPECIALATTRIBUTE_PREFIX+".F"+str(obj)
        elif obj is None:
            res = SPECIALATTRIBUTE_PREFIX+".n"
        elif obj is True:
            res = SPECIALATTRIBUTE_PREFIX+".1"
        elif obj is False:
            res = SPECIALATTRIBUTE_PREFIX+".0"
        elif type(obj) is complex:
            # Beware ! This type CAN'T BE ENCODED as a list (we use indeed
            # a tuple, see infra) since this type may be used as a dict key.
            res = IaswnEncoder.default((SPECIALATTRIBUTE_PREFIX+".C",
                                        obj.real,
                                        obj.imag))
        elif type(obj) is re.Pattern:
            # Beware ! This type CAN'T BE ENCODED as a list (we use indeed
            # a tuple, see infra) since this type may be used as a dict key.
            if type(obj.pattern) is str:
                res = IaswnEncoder.default((SPECIALATTRIBUTE_PREFIX+".p",
                                            obj.pattern,
                                            obj.flags))
            else:
                res = IaswnEncoder.default((SPECIALATTRIBUTE_PREFIX+".P",
                                            IaswnEncoder._encode_bytes(obj.pattern),
                                            obj.flags))
        elif type(obj) is frozenset:
            if len(obj) == 0:
                res = SPECIALATTRIBUTE_PREFIX+".f0"
            else:
                # Beware ! This type CAN'T BE ENCODED as a list (we use indeed
                # a tuple, see infra) since this type may be used as a dict key.
                res = IaswnEncoder.default((SPECIALATTRIBUTE_PREFIX+".f",
                                            list(IaswnEncoder.default(item) for item in obj)))
        elif type(obj) is range:
            res = IaswnEncoder.default((SPECIALATTRIBUTE_PREFIX+".r",
                                        obj.start, obj.stop, obj.step))
        elif type(obj) is decimal.Decimal:
            res = SPECIALATTRIBUTE_PREFIX+".D"+str(obj)
        elif type(obj) is datetime.datetime:
            res = IaswnEncoder.default((SPECIALATTRIBUTE_PREFIX+".dt",
                                        obj.isoformat(timespec='microseconds')))
        elif type(obj) is datetime.timedelta:
            res = IaswnEncoder.default((SPECIALATTRIBUTE_PREFIX+".dtD",
                                        obj.days,
                                        obj.seconds,
                                        obj.microseconds))
        elif type(obj) is datetime.date:
            res = IaswnEncoder.default((SPECIALATTRIBUTE_PREFIX+".dtd",
                                        obj.year,
                                        obj.month,
                                        obj.day))
        else:
            res = IaswnEncoder.default(obj)
        return res

    @staticmethod
    def _encode(obj):
        """
            IaswnEncoder._encode()

            Encode <obj> by calling IaswnEncoder().encode() over it.

            ___________________________________________________________________

            ARGUMENT: the <obj> to be encoded.

            RETURNED VALUE: (str)the corresponding string.
        """
        return SPECIALATTRIBUTE_PREFIX+".o" + IaswnEncoder().encode(obj)

    # Original signature: def default(self, o)
    # Since 'o' isn't a valid name, we use <obj> instead.
    # pylint: disable=method-hidden
    # pylint: disable=arguments-differ
    #
    # pylint: disable=too-many-statements
    @staticmethod
    def default(obj):
        """
            IaswnEncoder.default()

            Flatten <obj>, i.e. transform <obj> into something that json.JSONEncoder()
            knows how to encode.

            Method called by json.JSONEncoder(), by IaswnEncoder._encode_dictkey(),
            by Iaswn.iaswn_preprocessing() and recursively by IaswnEncoder.default()
            itself.

            ___________________________________________________________________

            ARGUMENT: <obj> may be any object read while encoding : int, dict, ...

            RETURNED VALUE: the corresponding object.
        """
        if type(obj) is not type and hasattr(obj, "iaswn_preprocessing"):
            obj = obj.iaswn_preprocessing()

        if obj is None:
            res = obj
        elif type(obj) is str:
            res = obj
        elif type(obj) is bool:
            res = obj
        elif type(obj) is int:
            res = obj
        elif type(obj) is float:
            res = obj
        elif type(obj) is dict:
            res = {}
            for key, value in obj.items():
                res[IaswnEncoder._encode_dictkey(key)] = IaswnEncoder.default(value)
        elif type(obj) is set:
            if len(obj) == 0:
                res = SPECIALATTRIBUTE_PREFIX+".s0"
            else:
                res = [SPECIALATTRIBUTE_PREFIX+".s",
                       list(IaswnEncoder.default(item) for item in obj)]
        elif type(obj) is frozenset:
            if len(obj) == 0:
                res = SPECIALATTRIBUTE_PREFIX+".f0"
            else:
                res = [SPECIALATTRIBUTE_PREFIX+".f",
                       list(IaswnEncoder.default(item) for item in obj)]
        elif type(obj) is list:
            res = list(IaswnEncoder.default(item) for item in obj)
        elif type(obj) is re.Pattern:
            if type(obj.pattern) is str:
                res = [SPECIALATTRIBUTE_PREFIX+".p",
                       obj.pattern,
                       obj.flags]
            else:
                res = [SPECIALATTRIBUTE_PREFIX+".P",
                       IaswnEncoder._encode_bytes(obj.pattern),
                       obj.flags]
        elif type(obj) is type:
            # !!  int/float/... has a __dict__ attribute too, please insert this if before the
            #    "elif asattr(obj, "__dict__")" test.
            res = [SPECIALATTRIBUTE_PREFIX+".ty", obj.__module__, obj.__name__]
        elif type(obj) is tuple:
            if len(obj) == 0:
                res = SPECIALATTRIBUTE_PREFIX+".t0"
            else:
                res = IaswnEncoder._encode([SPECIALATTRIBUTE_PREFIX+".t",
                                            list(IaswnEncoder.default(item) for item in obj)])
        elif callable(obj):
            res = [SPECIALATTRIBUTE_PREFIX+".c",
                   obj.__module__,
                   obj.__qualname__,
                   inspect.ismethod(obj)]
        elif type(obj) is bytes:
            res = SPECIALATTRIBUTE_PREFIX+".b"+IaswnEncoder._encode_bytes(obj)
        elif type(obj) is complex:
            res = [SPECIALATTRIBUTE_PREFIX+".C",
                   obj.real,
                   obj.imag]
        elif obj is NotImplemented:
            res = SPECIALATTRIBUTE_PREFIX+".no"
        elif type(obj) is range:
            res = [SPECIALATTRIBUTE_PREFIX+".r",
                   obj.start,
                   obj.stop,
                   obj.step]
        elif type(obj) is decimal.Decimal:
            if obj.is_nan():
                # NaN is a special case:
                #  https://stackoverflow.com/questions/10034149
                #  https://docs.python.org/3/library/stdtypes.html,
                #    see "Numeric Types — int, float, complex" section
                raise TypeError(f"Can't encode a NaN number; {obj=}")
            res = SPECIALATTRIBUTE_PREFIX+".D"+str(obj)
        elif type(obj) is collections.defaultdict:
            res = [SPECIALATTRIBUTE_PREFIX+".dd",
                   IaswnEncoder.default(obj.default_factory),
                   IaswnEncoder.default(dict(obj.items()))]
        elif type(obj) is datetime.datetime:
            res = [SPECIALATTRIBUTE_PREFIX+".dt",
                   obj.isoformat(timespec='microseconds')]
        elif type(obj) is datetime.timedelta:
            res = [SPECIALATTRIBUTE_PREFIX+".dtD",
                   obj.days,
                   obj.seconds,
                   obj.microseconds]
        elif type(obj) is datetime.date:
            res = [SPECIALATTRIBUTE_PREFIX+".dtd",
                   obj.year,
                   obj.month,
                   obj.day]
        else:
            # This code is reached when <obj> is of a type that .default() does not know how to
            # convert to a json-string.
            # This can happen when encoding a customed object that does not use the pre/post-process
            # mechanism to encode/decode an unknown type.
            raise TypeError("Can't encode using .default() method "
                            f"the object (type={type(obj)}) '{obj}'. ")

        return res


class Iaswn:
    """
        Iaswn class

        Mother class of the classes using the Iaswn utilities.

        _______________________________________________________________________

        Methods:
        o  _iaswn_has_the_postprocessing_been_done(self)
        o  _iaswn_postprocessing_has_been_done(self)
        o  decode(cls, jsonstring)
        o  encode(self, json_args=None)
        o  iaswn_preprocessing(classattributes=True, inheritedlist=True, inheriteddict=True)
        o  iaswn_postprocessing(self)
        o  to_jsonstr(self, json_args=None)

        o  "from_jsonstr", defined as "decode"
        o  "to_jsonstr", defined as "encode"
    """
    def _iaswn_has_the_postprocessing_been_done(self):
        # access to the special attribute (by default, .|asωñ):
        return "postprocessing:done" in self.__dict__[SPECIALATTRIBUTE_PREFIX]

    def _iaswn_postprocessing_has_been_done(self):
        # access to the special attribute (by default, .|asωñ):
        self.__dict__[SPECIALATTRIBUTE_PREFIX]["postprocessing:done"] = True

    @classmethod
    def decode(cls,
               jsonstring):
        """
            Iaswn.decode()

            Read a <jsonstring> and return the corresponding object.

            ___________________________________________________________________

            ARGUMENT: (str)jsonstring, the string to be decoded.

            RETURNED VALUE: the decoded object.
        """
        try:
            return IaswnDecoder().decode(jsonstring)
        except (TypeError, json.decoder.JSONDecodeError) as exception:
            raise IaswnError(exception) from exception

    def encode(self,
               json_args=None):
        """
            Iaswn.encode()

            Transform <self> into a (str)json string that may be read by .decode()

            ___________________________________________________________________

            ARGUMENT: (None or a dict)json_args, the options relative to the encoding.
                      If None, all keys/values will be read from DEFAULT_JSONARGS_ENCODER
                      see DEFAULT_JSONARGS_ENCODER
                      You may give only a subset of DEFAULT_JSONARGS_ENCODER, the other
                      keys/values will be read from DEFAULT_JSONARGS_ENCODER.

            RETURNED VALUE: (str)the encoded object
        """
        _json_args = DEFAULT_JSONARGS_ENCODER
        if json_args:
            _json_args.update(json_args)

        try:
            res = self.iaswn_preprocessing()
            return IaswnEncoder(**_json_args).encode(res)
        except TypeError as exception:
            raise IaswnError(exception) from exception

    def iaswn_postprocessing(self):
        """
            Iaswn.iaswn_postprocessing()

            about iaswn_[post|pre]processing() methods:
              If an error occured, please catch it and raise a TypeError with a
              message describing the error.

            ___________________________________________________________________

            no RETURNED VALUE, the object is modified in place.
        """
        to_be_modified = []
        for key, value in self.__dict__.items():
            # selfreference:
            if value == SPECIALATTRIBUTE_PREFIX+".selfref":
                to_be_modified.append((key, self))

        for key, new_value in to_be_modified:
            self.__dict__[key] = new_value

    def iaswn_preprocessing(self,
                            classattributes=True,
                            inheritedlist=True,
                            inheriteddict=True):
        """
            Iaswn.iaswn_preprocessing()

            Default .iaswn_preprocessing() method.

            about iaswn_[post|pre]processing() methods:
              If an error occured, please catch it and raise a TypeError with a
              message describing the error.

            ___________________________________________________________________

            ARGUMENTS:
            o  classattributes  : (bool) True if this methods deals with class attributes.
            o  inheritedlist    : (bool) True if this methods deals with inherited list content.
            o  inheriteddict    : (bool) True if this methods deals with inherited dict content.

            RETURNED VALUE: the minimal dict required to json-ize an object.
        """
        res = {SPECIALATTRIBUTE_PREFIX: {"name": [self.__module__,
                                                  self.__class__.__name__, ], }}

        # class attributes:
        if classattributes:
            _res = {}
            for key, value in self.__dict__.items():
                if id(self) == id(value):
                    # selfreference:
                    _res[key] = SPECIALATTRIBUTE_PREFIX+".selfref"
                else:
                    _res[key] = value
            res = res | IaswnEncoder.default(_res)

        # inherited list content:
        # In this case, <self> is an iterable even if Pylint disagrees.
        # pylint: disable=not-an-iterable
        if inheritedlist:
            if type(self) is not list and isinstance(self, list):
                if len(self) == 0:
                    res = res | \
                        {SPECIALATTRIBUTE_PREFIX+".l0": None}
                else:
                    res = res | \
                        {SPECIALATTRIBUTE_PREFIX+".l":
                         list(IaswnEncoder.default(item) for item in self)}

        # inherited dict content:
        # In this case, <self> does have an .items() member even if
        # Pylint disagrees.
        # pylint: disable=no-member
        if inheriteddict:
            if type(self) is not dict and isinstance(self, dict):
                if len(self) == 0:
                    res = res | \
                        {SPECIALATTRIBUTE_PREFIX+".d0": None}
                else:
                    res = res | \
                        {SPECIALATTRIBUTE_PREFIX+".d":
                         [[IaswnEncoder.default(_key),
                           IaswnEncoder.default(_value)] for _key, _value in self.items()]}

        return res

    from_jsonstr = decode
    to_jsonstr = encode


def decode(jsonstring):
    """
        decode()

        Read a <jsonstring> and return the corresponding object.

        _______________________________________________________________________

        ARGUMENT: (str)jsonstring, the string to be decoded.

        RETURNED VALUE: the decoded object
                        a IaswnError exception is raised if an error occurs while
                        decoding.
    """
    try:
        res = IaswnDecoder().decode(jsonstring)
        stop = False
        while not stop:
            stop = True

            # <res> may be a string or any other type.
            #
            # definition of DOCDEF001
            #  str(res) may be equal (if <res> is a class instance and if
            #  no __str()__/__repr__() have been defined for this class) to:
            #      "<mymodule.myfilename.MyClass object at 0x7f71c9a6e1f0>"
            if SPECIALATTRIBUTE_PREFIX in str(res):
                res = IaswnDecoder.customed_object_hook(res)
                stop = False

        return res
    except (TypeError,
            json.decoder.JSONDecodeError) as exception:
        raise IaswnError(exception) from exception


def diagnostic(obj,
               details=False):
    """
        diagnostic()

        Try to encode/decode <obj>.

        _______________________________________________________________________

        ARGUMENTS:
        o  <obj> the object to be checked
        o  (bool)<details> if True, return ((bool)success, (str)explanations)

        RETURNED VALUE:
        if <details> is False: (bool)success
        if <details> is True:  (bool)success, (str)explanations
    """
    res = True
    _details = None

    # access through .encode()/.decode() methods:
    #  why isinstance(obj, iaswn.iaswn.Iaswn) ?
    #  In this method <obj> may be a string and strings have a native
    #  .encode() which has nothing to do with iaswn.iaswn.Iaswn.encode().
    #
    # Pylint doesn't know how to handle "iaswn.iaswn.Iaswn":
    # pylint: disable=undefined-variable
    if hasattr(obj, "encode") and isinstance(obj, iaswn.iaswn.Iaswn):
        try:
            jsonstr = obj.encode()
            if not isinstance(jsonstr, str):
                _details = "(.encode/decode methods) " \
                    f"Can't encode; jsonstr(obj) isn't a string but a {type(jsonstr)} object."
                res = False
        except IaswnError as exception:
            _details = "(.encode/decode methods) " \
                f"Can't encode: error message is '{str(exception)}'."
            res = False

        if res:
            try:
                obj2 = type(obj).decode(jsonstr)
                if not obj.__eq__(obj2):
                    _details = "(.encode/decode methods) " \
                        f"Can't decode; original obj. != re-created obj.; {obj=}; {obj2=};"
                    res = False
            except IaswnError as exception:
                _details = "(.encode/decode methods) " \
                    f"Can't decode: error message is '{str(exception)}'."
                res = False

    # access through encode()/decode() functions:
    try:
        jsonstr = encode(obj)
        if not isinstance(jsonstr, str):
            _details = "(.encode/decode functions) " \
                f"Can't encode; jsonstr(obj) isn't a string but a {type(jsonstr)} object."
            res = False
    except IaswnError as exception:
        _details = "(.encode/decode functions) " \
            f"Can't encode: error message is '{str(exception)}'."
        res = False

    if res:
        try:
            obj2 = decode(jsonstr)
            if obj != obj2:
                _details = "(.encode/decode functions) " \
                    f"Can't decode; original obj. != re-created obj.; {obj=}; {obj2=};"
                res = False
        except IaswnError as exception:
            _details = "(.encode/decode functions) " \
                f"Can't decode: error message is '{str(exception)}'."
            res = False

    if not details:
        return res

    return res, _details


def encode(obj,
           json_args=None):
    """
        encode()

        Transform <self> into a (str)json string that may be read by .decode() .

        _______________________________________________________________________

        ARGUMENTS:
        o  obj, the object to be encoded into a json str.
        o  json_args(None or a dict)json_args, the options relative to the encoding.
           If None, all keys/values will be read from DEFAULT_JSONARGS_ENCODER
           see DEFAULT_JSONARGS_ENCODER
           You may give only a subset of DEFAULT_JSONARGS_ENCODER, the other
           keys/values will be read from DEFAULT_JSONARGS_ENCODER.

        RETURNED VALUE: (str)the encoded object
                        a IaswnError exception is raised if an error occurs
                        while encoding.
    """
    _json_args = DEFAULT_JSONARGS_ENCODER
    if json_args:
        _json_args.update(json_args)

    try:
        if type(obj) is not dict and isinstance(obj, dict):
            # if <obj> is a tests.fake_classes.CustomedInheritedDict instance:
            #    <obj>: - self.quaternionvalue=<tests.fake_classes.Quaternion object>;
            #           - dictcontent=((1, 2),)
            #
            # then IaswnEncoder(**_json_args).default(obj) will be a DICT:
            #    {'|asωñ': {'name': ['tests.fake_classes', 'CustomedInheritedDict']},
            #     '|asωñ.d': [[1, 2]],
            #     'quaternionvalue': '|asωñ.o["|asωñ.t", [0, 1, 2, 3]]'
            #    }
            # and IaswnEncoder(**_json_args).encode(IaswnEncoder(**_json_args).default(obj))
            # will be the (str)jsonstring.
            return IaswnEncoder(**_json_args).encode(IaswnEncoder(**_json_args).default(obj))
        if type(obj) is not list and isinstance(obj, list):
            # if <obj> a CustomInheritedList instance:
            #    <obj>: - self.quaternionvalue=<tests.fake_classes.Quaternion object>;
            #           - listcontent=({3: 4, '3': 5},)
            #
            # then IaswnEncoder(**_json_args).default(obj) will be a DICT:
            #     {'|asωñ': {'name': ['tests.fake_classes', 'CustomedInheritedList']},
            #                 '|asωñ.l': [{'|asωñ.i3': 4, '3': 5}],
            #                 'quaternionvalue': '|asωñ.o["|asωñ.t", [0, 1, 2, 5]]'}
            #
            # and IaswnEncoder(**_json_args).encode(IaswnEncoder(**_json_args).default(obj))
            # will be the (str)jsonstring.
            return IaswnEncoder(**_json_args).encode(IaswnEncoder(**_json_args).default(obj))
        if hasattr(obj, "encode"):
            # if <obj> is a RegularObject instance:
            #    <obj>: - self.xvalue={3: <function randomfunction};
            #
            # then IaswnEncoder(**_json_args).encode(obj) will be a STR, the expected jsonstring.
            return IaswnEncoder(**_json_args).encode(obj)

        # <obj> is not class instance: it may be an int, a str, a tuple...
        return IaswnEncoder(**_json_args).encode(IaswnEncoder(**_json_args).default(obj))

    except TypeError as exception:
        raise IaswnError(exception) from exception


# We need these names written in lower case.
to_jsonstr = encode  # pylint: disable=invalid-name
from_jsonstr = decode  # pylint: disable=invalid-name

serialize = encode  # pylint: disable=invalid-name
deserialize = decode  # pylint: disable=invalid-name
