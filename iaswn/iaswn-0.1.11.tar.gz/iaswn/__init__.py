"""
Text automatically generated from 'README.md' .

Iaswn project

Iaswn is a package for two-way conversions of complex Python objects and JSON strings. This is a GP
Lv3/Python 3.9+ project.

Maybe you should use more mature packages like jsonpickle or marshmallow.

Iaswn has weak points but also rare strong points: no dependencies, dict keys may be something else
 than a string, no eval(). A big drawback is that you have to derive your customed classes from the
 Iaswn class.

Selfreference are partly supported.

You may start with some documented examples. You may also read how to install this package or read
the project's roadmap and its license.

* see the classes' hierarchy
* see the dependencies
* see the external tools required to modify the project's code

-------------------------------------------------------------------------------

TABLE OF CONTENTS

- [0] the project in a few words
  - [0.1] What about the name ?
- [1] installation
  - [1.1] poetry and dependencies
- [2] how to use
  - [2.0] overview
  - [2.1] Python objects
  - [2.2] Class objects: simple case
  - [2.3] Class objects: add special methods to your class
  - [2.4] Selfreference
- [3] if you want to read/test/modify the code
  - [3.0] classes hierarchy
  - [3.1] checks and tests
    - [3.1.1] check_tools
    - [3.1.2] launch the tests
    - [3.1.3] check code quality
    - [3.1.4] check pip conflicts
    - [3.1.5] search all errors/warnings codes
    - [3.1.6] automatically generate the main __init__py file
  - [3.2] code quality
    - [3.2.1] code quality matters
      - [3.2.1.1] about pylint and pylintrc
    - [3.2.2] how to read and write documentation
      - [3.2.2.1] about markdown files
    - [3.2.3] before committing
  - [3.3] coding conventions
  - [3.4] errors and warnings
  - [3.5] git and poetry workflow
- [4] Iaswn JSON-string format
  - [4.1] how modify the string format ?
  - [4.2] Iaswn known types
- [5] Comparisons with other packages

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

[0] the project in a few words

You want to json-ize a Python object:


                  >----(encode)----->
    Python object                     JSON string
                  <----(decode)-----<

By default, you may encode a lot of Python objects that you may use directly in your class: int, fl
oat, complex, str, re.Pattern, ... (full list here).

By consequence if you want to jsonize a dict ({3: "three", "3": "(str)three"}), you can write:

  |
  | from iaswn.iaswn import encode, decode, IaswnError
  |
  | try:
  |     jsonstring = encode({3: "three", "3": "(str)three"})
  |     print(jsonstring)  # will print something like: {"|asωñ.i3": "three", "3": "(str)three"}
  |     obj = decode(jsonstring)
  |     print(obj)  # will print: {3: "three", "3": "(str)three"}
  | except IaswnError as error:
  |     print(error)
  |

Or, using your own class (named MyObject):

  |
  | from iaswn.iaswn import encode, decode, IaswnError, Iaswn
  |
  | class MyObject(Iaswn):
  |     def __init__(self, myattr=None):
  |         Iaswn.__init__(self)
  |         self.myattr = myattr
  |
  |     def __repr__(self):
  |         return f"(MyObject) self.myattr={self.myattr}"
  | try:
  |     MYOBJECT = MyObject(myattr="Hwæt! Wé Gárdena | in géardagum (Bēowulf.1)")
  |     MYOBJECT_JSONSTR = MYOBJECT.encode()
  |     print("Initial object is:", MYOBJECT)
  |     print("JSON-string of the initial object is:", MYOBJECT_JSONSTR)
  |     print("Recreated object is:", MYOBJECT.decode(MYOBJECT_JSONSTR))
  | except IaswnError as error:
  |     print(error)
  |

See here for more complex examples, especially if you use data types that Iaswn cannot handle.

[0.1] What about the name ?

Iaswn is the project's name; package name is iaswn for Python, pipy and Poetry.

Iaswn is a pun on JSON and Jason:

    JSON > J[a]son > Ἰάσων > Iaswn /j'aːsɔːn/

[1] installation

Normal way to install this package manually:

$ pip install iaswn

See this section to install from sources.

[1.1] poetry and dependencies

This package has been built and published thanks to poetry. Here is the result of the $ poetry show
 --tree command.

You may want to check pip conflicts: see this section.

[2] how to use

[2.0] overview

See example.py in the source code.

In general, you can use the encode() and decode() functions but your objects must either have a ias
wn-able type (full list here) either have their customed .encode() and .decode() methods to encode
and decode.
Default .encode() and .decode() are already written and you get these default methods by deriving y
our class from the Iaswn class.
It may happen that these default methods aren't sufficient and that you have to use another mechani
sm to help Iaswn.

If you want to check if an object may be handled by Iaswn, please use the diagnostic(obj) method de
fined in iaswn.py:

  |
  | import iaswn.iaswn
  | print(iaswn.iaswn.diagnostic({3: "3", 4: "4"}))  # will print "True"
  |

By default diagnostic() returns only (bool)success; if you want more details, use diagnostic(obj, d
etails=True)

[2.1] Python objects

You can encode a lot of native Python types that you may use directly in your class: int, float, st
r, re.Pattern, ... (full list here).

By consequence you can write:

  |
  | from iaswn.iaswn import encode, decode, IaswnError
  |
  | try:
  |     jsonstring = encode({3: "three", "3": "(str)three"})
  |     print(jsonstring)  # will print something like: {"|asωñ.i3": "three", "3": "(str)three"}
  |     obj = decode(jsonstring)
  |     print(obj)  # will print: {3: "three", "3": "(str)three"}
  | except IaswnError as error:
  |     print(error)
  |

[2.2] Class objects: simple case

You class must be derived from the Iaswn class; if this class uses only types that Iaswn can handle
 (full list here) you have nothing more to do:

  |
  | from iaswn.iaswn import encode, decode, IaswnError, Iaswn
  |
  | class MyObject(Iaswn):
  |     def __init__(self, myattr=None):
  |         Iaswn.__init__(self)
  |         self.myattr = myattr
  |
  |     def __repr__(self):
  |         return f"(MyObject) self.myattr={self.myattr}"
  |
  | try:
  |     MYOBJECT = MyObject(myattr="Hwæt! Wé Gárdena | in géardagum (Bēowulf.1)")
  |     MYOBJECT_JSONSTR = MYOBJECT.encode()
  |     print("Initial object is:", MYOBJECT)
  |     print("JSON-string of the initial object is:", MYOBJECT_JSONSTR)
  |     print("Recreated object is:", MYOBJECT.decode(MYOBJECT_JSONSTR))
  | except IaswnError as error:
  |     print(error)
  |

If MyObject is initialized with an object Iaswn can't handle, more work is required.

[2.3] Class objects: add special methods to your class

Let's say you have a class that uses an object Iaswn can't natively handle, e.g. a Quaternion objec
t:

  |
  | class Quaternion:
  |     def __init__(self, a=0, b=0, c=0, d=0):
  |         self.a = a
  |         self.b = b
  |         self.c = c
  |         self.d = d
  |
  | THIS CODE CAN'T WORK: by default, Iaswn doesn't know
  | how to handle Quaternion objects.
  | class MyObject(Iaswn):
  |     def __init__(self, quaternion):
  |         Iaswn.__init__(self)
  |         self.quaternion = quaternion
  |

How iaswn-ize a MyObject instance ? There are two solutions:

* if you can modify Quaternion, derive Quaternion from Iaswn: class Quaternion(Iaswn). Nothing more
 is required.
* if you can't modify Quaternion, you have to add two methods to MyObject, namely iaswn_preprocessi
ng and iaswn_postprocessing.

  |
  | class MyObject(Iaswn):
  |     def __init__(self, quaternion):
  |         Iaswn.__init__(self)
  |         self.quaternion = quaternion
  |
  |     def iaswn_postprocessing(self):
  |         # ---- every customed .iaswn_postprocessing() method should begin ----
  |         # ---- with the following lines:
  |         if self._iaswn_has_the_postprocessing_been_done():
  |             # the job has already been done, nothing to do:
  |             return
  |         # ---- if this attribute is set to its default value    ----
  |         # ---- (see __init__()), nothing to do, it's not a real ----
  |         # ---- initialization.                                  ----
  |         if self.quaternion is None:
  |             return
  |
  |         # ---- real work starts here ----
  |         self.quaternion = Quaternion(self.quaternion[0],
  |                                  self.quaternion[1],
  |                                  self.quaternion[2],
  |                                  self.quaternion[3])
  |
  |         # ---- Don't forget to signal that the work is finished. ----
  |         self._iaswn_postprocessing_has_been_done()
  |
  |     def iaswn_preprocessing(self,
  |                             classattributes=True,
  |                             inheritedlist=False,
  |                             inheriteddict=False):
  |         res = Iaswn.iaswn_preprocessing(self,
  |                                         classattributes=False)
  |         # remember: list-s are cheaper than tuple-s to encode/decode,
  |         # hence the list created for res["quaternion"].
  |         res["quaternion"] = [self.quaternion.a,
  |                              self.quaternion.b,
  |                              self.quaternion.c,
  |                              self.quaternion.d]
  |
  |         return res
  |

[2.4] Selfreference

Selfreference (i.e. an object containing a reference to itself) is only partly supported by Iaswn.
Iaswn knows how to handle selfreference for class attributes.

You may write:
  |
  | class MyObject(Iaswn):
  |     def __init__(self):
  |         self.value = self
  |

But you cannot write:
  |
  | class MyObject(Iaswn):
  |     def __init__(self):
  |         self.value = [self,]
  |

[3] if you want to read/test/modify the code

If you want to read or modify or test the code:

$ git clone https://github.com/suizokukan/iaswn.git

You may want to launch documented examples : see example.py.

[3.0] classes hierarchy

See this file to see all classes hierarchy.

[3.1] checks and tests

[3.1.1] check_tools

Use check_tools to check that all external tools are installed:

$ ./check_tools

[3.1.2] launch the tests

$ ./tests.sh

[3.1.3] check code quality

$ ./code_quality.sh

See 3.2 code quality section.

[3.1.4] check pip conflicts

$ ./pip_conflicts.sh

...if you don't see the package name (namely iaswn) in the output, everything is alright.

[3.1.5] search all errors/warnings codes

Only one exception should be raised by the code, namely IaswnError defined in iaswn.py.

[3.1.6] automatically generate the main __init__py file.

README.md > __init__.py with the help of the readmemd2txt command:

  |
  | $ readmemd2txt --pyinitfile --linemaxlength=99 > iaswn/__init__.py
  |

[3.2] code quality

[3.2.1] code quality matters

This project focuses on documentation and easy-to-read code.

Please use the code_quality.sh script to check the
quality of the code. Pytlint's note should be equal to 10/10.

$ ./code_quality.sh

[3.2.1.1] about pylint and pylintrc

The original pylintrc file has been modified for this project.
At least one warning has been disabled:

  |
  | disable=..................
  |         duplicate-code,
  |

* About disable=duplicate-code
This warning cannot be disabled with "# pylint: disable=duplicate-code". This message is therefore
unusable.

[3.2.2] how to read and write documentation

Use codesearch.py to search a string in the project: try codesearch.py.sh --help or go to the relev
ant section of the documentation.

[3.2.2.1] about markdown files

You may use a dedicated online editor.

[3.2.3] before committing

Please respect the following steps before committing:

  |
  | $ ./code_quality.sh
  |

Don't forget to update the main __init__.py; the documentation of this file should be generated by:

  |
  | $ readmemd2txt --pyinitfile --linemaxlength=99 > iaswn/__init__.py
  |

And if you want to publish:

  |
  | $ poetry build
  | $ poetry publish
  |

[3.3] coding conventions

    (01) Each method, each function deserves a good doc.
    (02) 10/10 with pylint is an interesting target.
    (03) every .py file begins with:
         - a shebang (namely #!/usr/bin/env python3)
         - the file encoding (namely # -*- coding: utf-8 -*-)
         - the licence
         - a doc.

         Every .py script in the main directory has at least the following arguments:
         --help, -h, --version, -v
     (04) in the root directory of all MusaMusa packages the following files
         are expected:
         _ .gitignore
         - check_tools.sh
         - classes.md
         - code_quality.sh
         - codesearch.py
         - example.py
         - LICENSE
         - pip_conflicts.sh
         - poetry_show_tree.md
         - poetry_show_tree.sh
         - propagate_versionnumber.py
         - pylintrc
         - pyproject.toml
         - README.md
         - ROADMAP.md
         - tests.sh
    (05) All examples in the documentation should be executable immediately
         after being copied and pasted. No extra import required !

[3.4] errors and warnings

If an error occurs, an IaswnError exception is raised.

[3.5] git and poetry workflow

Go to the dev branch; get the last task number (see ROADMAP.md
or check the log with git log).

Create from the dev branch a X.Y.2 branch, then create a task-XXX branch:

$ git checkout -b X.Y.Z
$ git checkout -b task-999

Edit ROADMAP.md and add what this branch is about.

Write some code, check and test it, commit and merge with
the X.Y.Z then with the dev branch.

On the dev branch you may want to publish:
  |
  | $ poetry build
  | $ poetry publish
  |

[4] Iaswn JSON-string format

[4.1] how modify the string format ?

* (encoding only)

You may modify the values stored in iaswn.iaswn.DEFAULT_JSONARGS_ENCODER. See Python documentation
since these values are those of the json package.

    DEFAULT_JSONARGS_ENCODER = {
        "skipkeys": False,
        "ensure_ascii": False,
        "check_circular": True,
        "allow_nan": True,
        "indent": None,
        "separators": None,
        "sort_keys": False,
        }

* (encoding and decoding)

You may modify the value of iaswn.iaswn.SPECIALATTRIBUTE_PREFIX

  |
  | (pimydoc)SPECIALATTRIBUTE_PREFIX
  | ⋅ This prefix is used to generate special keywords like "|asωñ.t" for
  | ⋅ a tuple.
  | ⋅
  | ⋅ By default SPEIALATTRIBUTE_PREFIX is set to '|asωñ' but you may hange
  | ⋅ this value whih don't have to be a valid Python identifier.
  | ⋅
  | ⋅ Tests have shown that there is little point in shortening this string in
  | ⋅ order to redue the length of the json-strings.
  | ⋅ It is more interesting to introdue exoticharacters to prevent collision with
  | ⋅ the strings stored in the input objets, the lasse names or the attributes
  | ⋅ names.
  | ⋅ The default string, "|asωñ", voluntarily starts with a harater that can't be
  | ⋅ used as a Python identifier in order to protect against collisions.
  | ⋅
  | ⋅ This string an't be set to :
  | ⋅ * "" (empty string)
  | ⋅ * "_"
  | ⋅ * "objet"
  | ⋅ * "at"
  | ⋅   ... or anything that might appear in a string like:
  | ⋅      "<mymodule.myfilename.Mylass objet at 0x7f71c9a6e1f0>"
  | ⋅   Confer DOCDEF001 in iaswn.py to understand why.
  | ⋅
  | ⋅ This string shouldn't be set to :
  | ⋅ * "iaswn", "Iaswn" or similar strings: you have to prevent collisions with
  | ⋅   similar strings given in the input objets.
  |

[4.2] Iaswn known types

Here are the keywords used by Iaswn to encode different types. Therefore, the following list gives
the list of all types recognized by Iaswn. If you use another data type, you have to define yoursel
f how to encode it.

The memoryview data type is not supported. Therefore it is used in the example file to show how use
 a data type that Iaswn doesn't know how to handle. If you decide to  modify Iaswn to handle the me
moryview data type, please update the example file.

If you modify/add/remove such types, BE CAREFUL WHEN CHOOSING ENCODING NAME:
the code may be tricky: e.g. try not to use strings having the same characters
at their beginning (like '.c', '.co' and '.col').

Iaswn doesn't known how to handle a function having '<locals'> in its __qualname__ (e.g. a nested f
unction).

Iaswn does know how to handle class objects, even if the class is derived from dict or list.

In what follows, we assume that the SPECIALATTRIBUTE_PREFIX has been set to "|asωñ".

    Data type                    encoded as
    ==================================================================================
    any class object(*)          '|asωñ.o' + IaswnEncoder().encode(obj)
    ==================================================================================
    bool:False                   false (NOT 'false') or '|asωñ.0' if a dict key
    ----------------------------------------------------------------------------------
    bool:True                    true  (NOT 'true') or '|asωñ.1' if a dict key
    ----------------------------------------------------------------------------------
    self/self reference (*)    '|asωñ.selfref'
    ----------------------------------------------------------------------------------
    bytes                        '|asωñ.b' + base64.b64encode(BYTES).decode("ascii")
    ----------------------------------------------------------------------------------
    complex                      ['|asωñ.C', real, imag]
    ----------------------------------------------------------------------------------
    callable()                 ['|asωñ.c',
                                  obj.__module__,
                                  obj.__qualname__,
                                  inspect.ismethod(obj)]
    ----------------------------------------------------------------------------------
    collections.defaultdict      ['|asωñ.dd',
                                  obj.default_factory,
                                  tuple(obj.items())]
    ----------------------------------------------------------------------------------
    datetime.datetime            ['|asωñ.dt', isoformat_string]

                                 tzinfo is supported as a part of the isoformat string.
                                 See examples in the test file(s) and see
                                 https://docs.python.org/3/library/datetime.html#datetime.datetime.
isoformat
    ----------------------------------------------------------------------------------
    datetime.date                ['|asωñ.dtd',
                                  obj.year,
                                  obj.month,
                                  obj.day]
    ----------------------------------------------------------------------------------
    datetime.timedelta           ['|asωñ.dtD',
                                  obj.days,
                                  obj.seconds,
                                  obj.microseconds]
    ----------------------------------------------------------------------------------
    Decimal                      '|asωñ.D' + "0.3333333333"

                                 please note that Decimal('NaN') is not supported
                                    https://stackoverflow.com/questions/10034149
                                    https://docs.python.org/3/library/stdtypes.html,
                                        see "Numeric Types — int, float, complex" section
    ----------------------------------------------------------------------------------
    empty frozenset              '|asωñ.f0'
    ----------------------------------------------------------------------------------
    empty inherited-dict content '|asωñ.d0'
    ----------------------------------------------------------------------------------
    empty inherited-list content '|asωñ.l0'
    ----------------------------------------------------------------------------------
    empty set                    '|asωñ.s0'
    ----------------------------------------------------------------------------------
    empty tuple                  '|asωñ.t0'
    ----------------------------------------------------------------------------------
    float                        by example 3.3 or '|asωñ.F'+str(floatnumber)
                                 if a dict key.
    ----------------------------------------------------------------------------------
    frozenset                    ('|asωñ.f'
                                  list(item for item in obj))
                                 If the frozenset is empty, confer
                                 "empty frozenset"
    ----------------------------------------------------------------------------------
    inherited-dict content       {'|asωñ.d':
                                  [[key, value] for key, value in obj.items()]}
                                 this dict is added to the dict which encodes the
                                 source object.
                                 If the dict is empty, confer
                                 "empty inherited-dict content"
    ----------------------------------------------------------------------------------
    inherited-list content       {'|asωñ.l':
                                  list(item for item in self)}
                                 this dict is added to the dict which encodes the
                                 source object.
                                 If the list is empty, confer
                                 "empty inherited-list content"
    ----------------------------------------------------------------------------------
    int                          e.g. 3 or '|asωñ.i'+str(integer) if a dict key
    ----------------------------------------------------------------------------------
    list                         e.g. [3, 4, 5] (nothing special about lists)
    ----------------------------------------------------------------------------------
    None                         null (not 'null') or '|asωñ.n' if a dict key
    ----------------------------------------------------------------------------------
    NotImplemented               '|asωñ.no'
    ----------------------------------------------------------------------------------
    range                        ['|asωñ.r',
                                  (int)start, (int)stop, (int)step]
    ----------------------------------------------------------------------------------
    set                          ['|asωñ.s'
                                  list(item for item in obj)]
                                 If the set is empty, confer
                                 "empty set"
    ----------------------------------------------------------------------------------
    tuple                        ['|asωñ.t'
                                  list(item for item in obj)]
                                 If the tuple is empty, confer
                                 "empty tuple"
    ----------------------------------------------------------------------------------
    type                         ['|asωñ.ty',
                                  obj.__module__,
                                  obj.__qualname__]
    ----------------------------------------------------------------------------------
    re.Pattern; source is str    ('|asωñ.p',
                                  obj.pattern,
                                  obj.flags)
    ----------------------------------------------------------------------------------
    re.Pattern; source is bytes  ('|asωñ.P',
                                  obj.pattern,
                                  obj.flags)
    ----------------------------------------------------------------------------------

    (*) Iaswn does know how to handle class objects, even if the class is derived from dict or list
.

    () A function having '<locals'> in its __qualname__ (e.g. a nested function) can't be encoded b
y Iaswn.

    (*) Selfreference: when <self> contains a reference to <self>.


[5] Comparisons with other packages

  |
  | $ wisteria --cmp="iaswn vs all(all)" --exportreport="md"
  |

  |
  | (B1b) Full Details: Serializers
  | ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━
━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
  | ┃ Serializer                   ┃ Encod. Ok ? ┃ Σ Encoded   ┃ Σ Encoded     ┃ Decod. Ok ? ┃ Σ De
coded   ┃ Reversibility ?  ┃ Σ memory     ┃
  | ┃                              ┃ (Max=116)   ┃ Time        ┃ Str. Length   ┃ (Max=116)   ┃ Time
        ┃ (Max=116)        ┃              ┃
  | ┃                              ┃             ┃ (seconds)   ┃ (characters)  ┃             ┃ (sec
onds)   ┃                  ┃              ┃
  | ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━
━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
  | │ Iaswn                        │ 51 (43.97%) │ (no data)   │ (no data)     │ 51 (43.97%) │ (no
data)   │ 49 (42.24%)      │ (no data)    │
  | │ json                         │ 33 (28.45%) │ (no data)   │ (no data)     │ 33 (28.45%) │ (no
data)   │ 20 (17.24%)      │ (no data)    │
  | │ jsonpickle                   │ (no data)   │ (no data)   │ (no data)     │ (no data)   │ (no
data)   │ (no data)        │ (no data)    │
  | │ jsonpickle(keys=True)        │ (no data)   │ (no data)   │ (no data)     │ (no data)   │ (no
data)   │ (no data)        │ (no data)    │
  | │ marshal                      │ 61 (52.59%) │ (no data)   │ (no data)     │ 61 (52.59%) │ (no
data)   │ 33 (28.45%)      │ (no data)    │
  | │ pickle                       │ 106         │ (no data)   │ (no data)     │ 106         │ (no
data)   │ 99 (85.34%)      │ (no data)    │
  | │                              │ (91.38%)    │             │               │ (91.38%)    │
        │                  │              │
  | │ pyyaml                       │ (no data)   │ (no data)   │ (no data)     │ (no data)   │ (no
data)   │ (no data)        │ (no data)    │
  | │ Amazon Ion Python            │ 33 (28.45%) │ (no data)   │ (no data)     │ 33 (28.45%) │ (no
data)   │ 24 (20.69%)      │ (no data)    │
  | │ yajl                         │ (no data)   │ (no data)   │ (no data)     │ (no data)   │ (no
data)   │ (no data)        │ (no data)    │
  | └──────────────────────────────┴─────────────┴─────────────┴───────────────┴─────────────┴─────
────────┴──────────────────┴──────────────┘
  |
  | (C1a) Conclusion: Data Objects Handled by the Serializer(s)
  |
  | Iaswn: According to the tests carried out on all data, Iaswn can handle 49 data objects among 1
16 (42.24%), namely bool/false, bool/true, bytes, bytes(empty), complex,
  | demonstration_dataobj_a5, dict(keys/bool), dict(keys/float), dict(keys/int), dict(keys/str), di
ct(keys/str+subdicts), float, frozenset, frozenset(empty), function,
  | function(python), imported module(class), imported module(function), int, io.string(empty), lis
t(+sublists), list(empty), metaclass, none, numbers(complex),
  | numbers(integral), numbers(real), pythonexception typeerror, re.pattern(bytes), re.pattern(str)
, regularclass(async_method), regularclass(class_method),
  | regularclass(generator), regularclass(method), regularclass(static_method), set, set(empty), st
r, str(empty), str(long), str(non ascii characters), time(time.time),
  | tuple, tuple(+subtuples), tuple(empty), type(str), type(type(str)), cwc:pgnreader.cwc_iaswn.Che
ssGames and cwc:simple.cwc_iaswn.SimpleClass .
  |
  | Other serializers:
  | json: According to the tests carried out on all data, json can handle 20 data objects among 116
 (17.24%), namely bool/false, bool/true, collections.counter(empty),
  | collections.defaultdict(empty), collections.ordereddict(empty), demonstration_dataobj_a5, dict(
keys/str), dict(keys/str+subdicts), float, int, io.string(empty),
  | list(+sublists), list(empty), metaclass, none, str, str(empty), str(long), str(non ascii charac
ters) and time(time.time) .
  | jsonpickle: According to the tests carried out on all data, jsonpickle can handle 90 data objec
ts among 116 (77.59%), namely array(b), array(b/empty),
  | array(b_unsigned), array(b_unsigned/empty), array(d), array(d/empty), array(f/empty), array(h),
 array(h/empty), array(h_unsigned), array(h_unsigned/empty), array(i),
  | array(i/empty), array(i_unsigned), array(i_unsigned/empty), array(l), array(l/empty), array(l_u
nsigned), array(l_unsigned/empty), array(q), array(q/empty),
  | array(q_unsigned), array(q_unsigned/empty), array(u), array(u/empty), bool/false, bool/true, by
tearray, bytearray(empty), bytes, bytes(empty),
  | collections.chainmap(empty), collections.counter(empty), collections.defaultdict(empty), collec
tions.deque, collections.deque(empty), collections.ordereddict,
  | collections.ordereddict(empty), complex, datetime(datetime.datetime), datetime(datetime.timedel
ta), dateutil(parser.parse), decimal(+infinity), decimal(-infinity),
  | decimal(0.5), decimal(1/7), demonstration_dataobj_a5, dict(keys/str), dict(keys/str+subdicts),
float, frozenset, frozenset(empty), function, function(python), imported
  | module, imported module(class), imported module(function), int, io.string(empty), list(+sublist
s), list(empty), metaclass, none, numbers(complex), numbers(integral),
  | numbers(real), pythonexception typeerror, range, range(empty), re.pattern(bytes), regularclass,
 regularclass(async_method), regularclass(generator),
  | regularclass(method), regularclass(static_method), regularclassinheriteddict, regularclassinher
itedlist, set, set(empty), str, str(empty), str(long), str(non ascii
  | characters), time(time.time), tuple, tuple(+subtuples), tuple(empty), type(str), type(type(str)
) and cwc:simple.cwc_default.SimpleClass .
  | jsonpickle(keys=True): According to the tests carried out on all data, jsonpickle(keys=True) ca
n handle 97 data objects among 116 (83.62%), namely array(b),
  | array(b/empty), array(b_unsigned), array(b_unsigned/empty), array(d), array(d/empty), array(f/e
mpty), array(h), array(h/empty), array(h_unsigned),
  | array(h_unsigned/empty), array(i), array(i/empty), array(i_unsigned), array(i_unsigned/empty),
array(l), array(l/empty), array(l_unsigned), array(l_unsigned/empty),
  | array(q), array(q/empty), array(q_unsigned), array(q_unsigned/empty), array(u), array(u/empty),
 bool/false, bool/true, bytearray, bytearray(empty), bytes, bytes(empty),
  | collections.chainmap, collections.chainmap(empty), collections.counter, collections.counter(emp
ty), collections.defaultdict, collections.defaultdict(empty),
  | collections.deque, collections.deque(empty), collections.ordereddict, collections.ordereddict(e
mpty), complex, datetime(datetime.datetime),
  | datetime(datetime.timedelta), dateutil(parser.parse), decimal(+infinity), decimal(-infinity), d
ecimal(0.5), decimal(1/7), demonstration_dataobj_a5, dict(keys/bool),
  | dict(keys/float), dict(keys/int), dict(keys/str), dict(keys/str+subdicts), float, frozenset, fr
ozenset(empty), function, function(python), imported module, imported
  | module(class), imported module(function), int, io.string(empty), list(+sublists), list(empty),
metaclass, none, numbers(complex), numbers(integral), numbers(real),
  | pythonexception typeerror, range, range(empty), re.pattern(bytes), regularclass, regularclass(a
sync_method), regularclass(generator), regularclass(method),
  | regularclass(static_method), regularclassinheriteddict, regularclassinheritedlist, set, set(emp
ty), str, str(empty), str(long), str(non ascii characters),
  | time(time.time), tuple, tuple(+subtuples), tuple(empty), type(str), type(type(str)), cwc:pgnrea
der.cwc_default.ChessGames and cwc:simple.cwc_default.SimpleClass .
  | marshal: According to the tests carried out on all data, marshal can handle 33 data objects amo
ng 116 (28.45%), namely bool/false, bool/true, bytearray,
  | bytearray(empty), bytes, bytes(empty), complex, demonstration_dataobj_a5, dict(keys/bool), dict
(keys/float), dict(keys/int), dict(keys/str), dict(keys/str+subdicts),
  | float, frozenset, frozenset(empty), int, io.string(empty), list(+sublists), list(empty), memory
view, metaclass, none, set, set(empty), str, str(empty), str(long),
  | str(non ascii characters), time(time.time), tuple, tuple(+subtuples) and tuple(empty) .
  | pickle: According to the tests carried out on all data, pickle can handle 99 data objects among
 116 (85.34%), namely array(b), array(b/empty), array(b_unsigned),
  | array(b_unsigned/empty), array(d), array(d/empty), array(f/empty), array(h), array(h/empty), ar
ray(h_unsigned), array(h_unsigned/empty), array(i), array(i/empty),
  | array(i_unsigned), array(i_unsigned/empty), array(l), array(l/empty), array(l_unsigned), array(
l_unsigned/empty), array(q), array(q/empty), array(q_unsigned),
  | array(q_unsigned/empty), array(u), array(u/empty), bool/false, bool/true, bytearray, bytearray(
empty), bytes, bytes(empty), collections.chainmap,
  | collections.chainmap(empty), collections.counter, collections.counter(empty), collections.defau
ltdict, collections.defaultdict(empty), collections.deque,
  | collections.deque(empty), collections.ordereddict, collections.ordereddict(empty), complex, dat
etime(datetime.datetime), datetime(datetime.timedelta),
  | dateutil(parser.parse), decimal(+infinity), decimal(-infinity), decimal(0.5), decimal(1/7), dem
onstration_dataobj_a5, dict(keys/bool), dict(keys/float), dict(keys/int),
  | dict(keys/str), dict(keys/str+subdicts), float, frozenset, frozenset(empty), function, function
(python), imported module(class), imported module(function), int,
  | io.string(empty), list(+sublists), list(empty), metaclass, none, notimplemented, numbers(comple
x), numbers(integral), numbers(real), pythonexception typeerror, range,
  | range(empty), re.pattern(bytes), re.pattern(str), regularclass, regularclass(async_method), reg
ularclass(class_method), regularclass(generator), regularclass(method),
  | regularclass(static_method), regularclassinheriteddict, regularclassinheritedlist, set, set(emp
ty), str, str(empty), str(long), str(non ascii characters),
  | time(time.time), tuple, tuple(+subtuples), tuple(empty), type(str), type(type(str)), cwc:pgnrea
der.cwc_default.ChessGames and cwc:simple.cwc_default.SimpleClass .
  | pyyaml: According to the tests carried out on all data, pyyaml can handle 92 data objects among
 116 (79.31%), namely array(b), array(b/empty), array(b_unsigned),
  | array(b_unsigned/empty), array(d), array(d/empty), array(f/empty), array(h), array(h/empty), ar
ray(h_unsigned), array(h_unsigned/empty), array(i), array(i/empty),
  | array(i_unsigned), array(i_unsigned/empty), array(l), array(l/empty), array(l_unsigned), array(
l_unsigned/empty), array(q), array(q/empty), array(q_unsigned),
  | array(q_unsigned/empty), array(u), array(u/empty), bool/false, bool/true, bytearray, bytearray(
empty), bytes, bytes(empty), collections.chainmap,
  | collections.chainmap(empty), collections.counter, collections.counter(empty), collections.defau
ltdict, collections.defaultdict(empty), collections.deque,
  | collections.deque(empty), collections.ordereddict, collections.ordereddict(empty), complex, dat
etime(datetime.datetime), datetime(datetime.timedelta),
  | dateutil(parser.parse), decimal(+infinity), decimal(-infinity), decimal(0.5), decimal(1/7), dem
onstration_dataobj_a5, dict(keys/bool), dict(keys/float), dict(keys/int),
  | dict(keys/str), dict(keys/str+subdicts), float, frozenset, frozenset(empty), function, function
(python), imported module, imported module(class), imported
  | module(function), int, io.string(empty), list(+sublists), list(empty), metaclass, none, pythone
xception typeerror, range, range(empty), re.pattern(bytes),
  | re.pattern(str), regularclass, regularclass(class_method), regularclassinheriteddict, regularcl
assinheritedlist, set, set(empty), str, str(empty), str(long), str(non
  | ascii characters), time(time.time), tuple, tuple(+subtuples), tuple(empty), type(str), type(typ
e(str)), cwc:pgnreader.cwc_default.ChessGames and
  | cwc:simple.cwc_default.SimpleClass .
  | Amazon Ion Python: According to the tests carried out on all data, Amazon Ion Python can handle
 24 data objects among 116 (20.69%), namely bool/false, bool/true, bytes,
  | bytes(empty), collections.counter(empty), collections.defaultdict(empty), collections.ordereddi
ct(empty), datetime(datetime.datetime), dateutil(parser.parse),
  | decimal(0.5), decimal(1/7), demonstration_dataobj_a5, dict(keys/str), dict(keys/str+subdicts),
float, int, io.string(empty), list(+sublists), list(empty), str,
  | str(empty), str(long), str(non ascii characters) and time(time.time) .
  | yajl: According to the tests carried out on all data, yajl can handle 15 data objects among 116
 (12.93%), namely bool/false, bool/true, collections.counter(empty),
  | collections.defaultdict(empty), collections.ordereddict(empty), demonstration_dataobj_a5, dict(
keys/str), dict(keys/str+subdicts), list(+sublists), list(empty),
  | metaclass, none, str, str(empty) and str(long) .
  |
  | (C1b) Conclusion: Data Objects NOT Handled by the Serializer(s)
  |
  | Iaswn: According to the tests carried out on all data, Iaswn can't handle 67 data objects among
 116 (57.76%), namely array(b), array(b/empty), array(b_unsigned),
  | array(b_unsigned/empty), array(d), array(d/empty), array(f), array(f/empty), array(h), array(h/
empty), array(h_unsigned), array(h_unsigned/empty), array(i),
  | array(i/empty), array(i_unsigned), array(i_unsigned/empty), array(l), array(l/empty), array(l_u
nsigned), array(l_unsigned/empty), array(q), array(q/empty),
  | array(q_unsigned), array(q_unsigned/empty), array(u), array(u/empty), bytearray, bytearray(empt
y), calendar(calendar(3)), collections.chainmap,
  | collections.chainmap(empty), collections.counter, collections.counter(empty), collections.defau
ltdict, collections.defaultdict(empty), collections.deque,
  | collections.deque(empty), collections.ordereddict, collections.ordereddict(empty), datetime(dat
etime.datetime), datetime(datetime.timedelta), dateutil(parser.parse),
  | decimal(+infinity), decimal(-infinity), decimal(0.5), decimal(1/7), decimal(nan), file descript
or, float(nan), hashlib(hashlib.sha1), hashlib(hashlib.sha224),
  | hashlib(hashlib.sha256), hashlib(hashlib.sha384), hashlib(hashlib.sha512), imported module, io.
string, list, memoryview, notimplemented, numbers(numbers), range,
  | range(empty), re.match, re.match(+flags), regularclass, regularclassinheriteddict and regularcl
assinheritedlist .
  |
  | Other serializers:
  | json: According to the tests carried out on all data, json can't handle 96 data objects among 1
16 (82.76%), namely array(b), array(b/empty), array(b_unsigned),
  | array(b_unsigned/empty), array(d), array(d/empty), array(f), array(f/empty), array(h), array(h/
empty), array(h_unsigned), array(h_unsigned/empty), array(i),
  | array(i/empty), array(i_unsigned), array(i_unsigned/empty), array(l), array(l/empty), array(l_u
nsigned), array(l_unsigned/empty), array(q), array(q/empty),
  | array(q_unsigned), array(q_unsigned/empty), array(u), array(u/empty), bytearray, bytearray(empt
y), bytes, bytes(empty), calendar(calendar(3)), collections.chainmap,
  | collections.chainmap(empty), collections.counter, collections.defaultdict, collections.deque, c
ollections.deque(empty), collections.ordereddict, complex,
  | datetime(datetime.datetime), datetime(datetime.timedelta), dateutil(parser.parse), decimal(+inf
inity), decimal(-infinity), decimal(0.5), decimal(1/7), decimal(nan),
  | dict(keys/bool), dict(keys/float), dict(keys/int), file descriptor, float(nan), frozenset, froz
enset(empty), function, function(python), hashlib(hashlib.sha1),
  | hashlib(hashlib.sha224), hashlib(hashlib.sha256), hashlib(hashlib.sha384), hashlib(hashlib.sha5
12), imported module, imported module(class), imported module(function),
  | io.string, list, memoryview, notimplemented, numbers(complex), numbers(integral), numbers(numbe
rs), numbers(real), pythonexception typeerror, range, range(empty),
  | re.match, re.match(+flags), re.pattern(bytes), re.pattern(str), regularclass, regularclass(asyn
c_method), regularclass(class_method), regularclass(generator),
  | regularclass(method), regularclass(static_method), regularclassinheriteddict, regularclassinher
itedlist, set, set(empty), tuple, tuple(+subtuples), tuple(empty),
  | type(str), type(type(str)), cwc:pgnreader.cwc_default.ChessGames and cwc:simple.cwc_default.Sim
pleClass .
  | jsonpickle: According to the tests carried out on all data, jsonpickle can't handle 25 data obj
ects among 116 (21.55%), namely array(f), calendar(calendar(3)),
  | collections.chainmap, collections.counter, collections.defaultdict, decimal(nan), dict(keys/boo
l), dict(keys/float), dict(keys/int), file descriptor, float(nan),
  | hashlib(hashlib.sha1), hashlib(hashlib.sha224), hashlib(hashlib.sha256), hashlib(hashlib.sha384
), hashlib(hashlib.sha512), io.string, list, memoryview, notimplemented,
  | re.match, re.match(+flags), re.pattern(str), regularclass(class_method) and cwc:pgnreader.cwc_d
efault.ChessGames .
  | jsonpickle(keys=True): According to the tests carried out on all data, jsonpickle(keys=True) ca
n't handle 18 data objects among 116 (15.52%), namely array(f),
  | calendar(calendar(3)), decimal(nan), file descriptor, float(nan), hashlib(hashlib.sha1), hashli
b(hashlib.sha224), hashlib(hashlib.sha256), hashlib(hashlib.sha384),
  | hashlib(hashlib.sha512), io.string, list, memoryview, notimplemented, re.match, re.match(+flags
), re.pattern(str) and regularclass(class_method) .
  | marshal: According to the tests carried out on all data, marshal can't handle 83 data objects a
mong 116 (71.55%), namely array(b), array(b/empty), array(b_unsigned),
  | array(b_unsigned/empty), array(d), array(d/empty), array(f), array(f/empty), array(h), array(h/
empty), array(h_unsigned), array(h_unsigned/empty), array(i),
  | array(i/empty), array(i_unsigned), array(i_unsigned/empty), array(l), array(l/empty), array(l_u
nsigned), array(l_unsigned/empty), array(q), array(q/empty),
  | array(q_unsigned), array(q_unsigned/empty), array(u), array(u/empty), calendar(calendar(3)), co
llections.chainmap, collections.chainmap(empty), collections.counter,
  | collections.counter(empty), collections.defaultdict, collections.defaultdict(empty), collection
s.deque, collections.deque(empty), collections.ordereddict,
  | collections.ordereddict(empty), datetime(datetime.datetime), datetime(datetime.timedelta), date
util(parser.parse), decimal(+infinity), decimal(-infinity), decimal(0.5),
  | decimal(1/7), decimal(nan), file descriptor, float(nan), function, function(python), hashlib(ha
shlib.sha1), hashlib(hashlib.sha224), hashlib(hashlib.sha256),
  | hashlib(hashlib.sha384), hashlib(hashlib.sha512), imported module, imported module(class), impo
rted module(function), io.string, list, notimplemented, numbers(complex),
  | numbers(integral), numbers(numbers), numbers(real), pythonexception typeerror, range, range(emp
ty), re.match, re.match(+flags), re.pattern(bytes), re.pattern(str),
  | regularclass, regularclass(async_method), regularclass(class_method), regularclass(generator),
regularclass(method), regularclass(static_method),
  | regularclassinheriteddict, regularclassinheritedlist, type(str), type(type(str)), cwc:pgnreader
.cwc_default.ChessGames and cwc:simple.cwc_default.SimpleClass .
  | pickle: According to the tests carried out on all data, pickle can't handle 17 data objects amo
ng 116 (14.66%), namely array(f), calendar(calendar(3)), decimal(nan),
  | file descriptor, float(nan), hashlib(hashlib.sha1), hashlib(hashlib.sha224), hashlib(hashlib.sh
a256), hashlib(hashlib.sha384), hashlib(hashlib.sha512), imported module,
  | io.string, list, memoryview, numbers(numbers), re.match and re.match(+flags) .
  | pyyaml: According to the tests carried out on all data, pyyaml can't handle 20 data objects amo
ng 116 (17.24%), namely array(f), calendar(calendar(3)), decimal(nan),
  | file descriptor, float(nan), hashlib(hashlib.sha1), hashlib(hashlib.sha224), hashlib(hashlib.sh
a256), hashlib(hashlib.sha384), hashlib(hashlib.sha512), io.string, list,
  | memoryview, notimplemented, numbers(complex), numbers(integral), numbers(numbers), numbers(real
), re.match and re.match(+flags) .
  | Amazon Ion Python: According to the tests carried out on all data, Amazon Ion Python can't hand
le 92 data objects among 116 (79.31%), namely array(b), array(b/empty),
  | array(b_unsigned), array(b_unsigned/empty), array(d), array(d/empty), array(f), array(f/empty),
 array(h), array(h/empty), array(h_unsigned), array(h_unsigned/empty),
  | array(i), array(i/empty), array(i_unsigned), array(i_unsigned/empty), array(l), array(l/empty),
 array(l_unsigned), array(l_unsigned/empty), array(q), array(q/empty),
  | array(q_unsigned), array(q_unsigned/empty), array(u), array(u/empty), bytearray, bytearray(empt
y), calendar(calendar(3)), collections.chainmap,
  | collections.chainmap(empty), collections.counter, collections.defaultdict, collections.deque, c
ollections.deque(empty), collections.ordereddict, complex,
  | datetime(datetime.timedelta), decimal(+infinity), decimal(-infinity), decimal(nan), dict(keys/b
ool), dict(keys/float), dict(keys/int), file descriptor, float(nan),
  | frozenset, frozenset(empty), function, function(python), hashlib(hashlib.sha1), hashlib(hashlib
.sha224), hashlib(hashlib.sha256), hashlib(hashlib.sha384),
  | hashlib(hashlib.sha512), imported module, imported module(class), imported module(function), io
.string, list, memoryview, metaclass, none, notimplemented,
  | numbers(complex), numbers(integral), numbers(numbers), numbers(real), pythonexception typeerror
, range, range(empty), re.match, re.match(+flags), re.pattern(bytes),
  | re.pattern(str), regularclass, regularclass(async_method), regularclass(class_method), regularc
lass(generator), regularclass(method), regularclass(static_method),
  | regularclassinheriteddict, regularclassinheritedlist, set, set(empty), tuple, tuple(+subtuples)
, tuple(empty), type(str), type(type(str)),
  | cwc:pgnreader.cwc_default.ChessGames and cwc:simple.cwc_default.SimpleClass .
  | yajl: According to the tests carried out on all data, yajl can't handle 97 data objects among 1
16 (83.62%), namely array(b), array(b/empty), array(b_unsigned),
  | array(b_unsigned/empty), array(d), array(d/empty), array(f), array(f/empty), array(h), array(h/
empty), array(h_unsigned), array(h_unsigned/empty), array(i),
  | array(i/empty), array(i_unsigned), array(i_unsigned/empty), array(l), array(l/empty), array(l_u
nsigned), array(l_unsigned/empty), array(q), array(q/empty),
  | array(q_unsigned), array(q_unsigned/empty), array(u), array(u/empty), bytearray, bytearray(empt
y), bytes, bytes(empty), calendar(calendar(3)), collections.chainmap,
  | collections.chainmap(empty), collections.counter, collections.defaultdict, collections.deque, c
ollections.deque(empty), collections.ordereddict, complex,
  | datetime(datetime.datetime), datetime(datetime.timedelta), dateutil(parser.parse), decimal(+inf
inity), decimal(-infinity), decimal(0.5), decimal(1/7), decimal(nan),
  | dict(keys/bool), dict(keys/float), dict(keys/int), file descriptor, float(nan), frozenset, froz
enset(empty), function, function(python), hashlib(hashlib.sha1),
  | hashlib(hashlib.sha224), hashlib(hashlib.sha256), hashlib(hashlib.sha384), hashlib(hashlib.sha5
12), imported module, imported module(class), imported module(function),
  | io.string, list, memoryview, notimplemented, numbers(complex), numbers(integral), numbers(numbe
rs), numbers(real), pythonexception typeerror, range, range(empty),
  | re.match, re.match(+flags), re.pattern(bytes), re.pattern(str), regularclass, regularclass(asyn
c_method), regularclass(class_method), regularclass(generator),
  | regularclass(method), regularclass(static_method), regularclassinheriteddict, regularclassinher
itedlist, set, set(empty), str(non ascii characters), tuple,
  | tuple(+subtuples), tuple(empty), type(str), type(type(str)), cwc:pgnreader.cwc_default.ChessGam
es and cwc:simple.cwc_default.SimpleClass .
  |
  | (C2a) Conclusion: Serializers (Not Sorted)
  | ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━
━━━━━┓
  | ┃ Serializer                ┃ Σ Encoded Str.   ┃ Σ Encod.+Decod.  ┃ Reversibility    ┃ Memory
     ┃
  | ┃                           ┃ Length           ┃ Time (seconds)   ┃ (Coverage Rate)  ┃
     ┃
  | ┃                           ┃ (characters)     ┃                  ┃ (Max=116)        ┃
     ┃
  | ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━
━━━━━┩
  | │ Iaswn                     │ (no data)        │ None             │ 49 (42.24%)      │ (no data
)    │
  | │ -                         │ -                │ -                │ -                │
     │
  | │ json                      │ (no data)        │ None             │ 20 (17.24%)      │ (no data
)    │
  | │ jsonpickle                │ (no data)        │ None             │ (no data)        │ (no data
)    │
  | │ jsonpickle(keys=True)     │ (no data)        │ None             │ (no data)        │ (no data
)    │
  | │ marshal                   │ (no data)        │ None             │ 33 (28.45%)      │ (no data
)    │
  | │ pickle                    │ (no data)        │ None             │ 99 (85.34%)      │ (no data
)    │
  | │ pyyaml                    │ (no data)        │ None             │ (no data)        │ (no data
)    │
  | │ Amazon Ion Python         │ (no data)        │ None             │ 24 (20.69%)      │ (no data
)    │
  | │ yajl                      │ (no data)        │ None             │ (no data)        │ (no data
)    │
  | └───────────────────────────┴──────────────────┴──────────────────┴──────────────────┴─────────
─────┘
  |
  | (C2b) Conclusion: Overall Score Based on 4 Comparisons Points (Σ Encoded Str. Length/Σ Encod.+D
ecod. Time/Coverage Rate/Σ memory)
  | ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
  | ┃ Serializer                ┃ Overall Score ┃
  | ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
  | │ Iaswn                     │ 36            │
  | │ -                         │ -             │
  | │ json                      │ 32            │
  | │ jsonpickle                │ 28            │
  | │ jsonpickle(keys=True)     │ 24            │
  | │ marshal                   │ 20            │
  | │ pickle                    │ 16            │
  | │ pyyaml                    │ 12            │
  | │ Amazon Ion Python         │ 8             │
  | │ yajl                      │ 4             │
  | └───────────────────────────┴───────────────┘
  |
  | (C2c) Conclusion
  | According to the tests carried out on all data, Iaswn is ranked #1 among 9 serializers (¹). The
re are 8 serializers, namely json, jsonpickle, jsonpickle(keys=True),
  | marshal, pickle, pyyaml, Amazon Ion Python and yajl that produce longer strings than Iaswn and
there's no serializer that produces shorter strings than Iaswn. There are
  | 8 serializers, namely json, jsonpickle, jsonpickle(keys=True), marshal, pickle, pyyaml, Amazon
Ion Python and yajl that are slower than Iaswn and there's no serializer
  | that is faster than Iaswn. There are 8 serializers, namely json, jsonpickle, jsonpickle(keys=Tr
ue), marshal, pickle, pyyaml, Amazon Ion Python and yajl that are worse
  | than Iaswn when it comes to data coverage and there's no serializer better than Iaswn when it c
omes to data coverage. There are 8 serializers, namely json, jsonpickle,
  | jsonpickle(keys=True), marshal, pickle, pyyaml, Amazon Ion Python and yajl that consume more me
mory than Iaswn and there's no serializer that consumes less memory than
  | Iaswn.
  |
  | - notes -
  | [¹] a rank based on 4 comparisons points: Σ jsonstr.len./Σ encod.+decod. time/Coverage Rate/Σ m
emory
  |
  | Can't create graph 'report1.png' for attribute 'encoding_time' since data are not fully availab
le for all serializers.
  | Can't create graph 'report2.png' for attribute 'mem_usage' since data are not fully available f
or all serializers.
  | Can't create graph 'report3.png' for attribute 'encoding_strlen' since data are not fully avail
able for all serializers.
  | Can't create graph 'report4.png' for attribute 'reversibility' since data are not fully availab
le for all serializers.
  | About to delete ancient 'report4.png' graph (/home/proguser/report4.png).
  |
"""
from iaswn.iaswn import Iaswn, IaswnError, IaswnEncoder, IaswnDecoder, encode, decode, diagnostic
from iaswn.iaswn import to_jsonstr, from_jsonstr
from iaswn.iaswn import serialize, deserialize
from iaswn.aboutproject import __version__
