# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['einspect',
 'einspect.protocols',
 'einspect.structs',
 'einspect.structs.include',
 'einspect.views']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'einspect',
    'version': '0.4.0',
    'description': 'Extended Inspect - view and modify memory structs of runtime objects.',
    'long_description': '# einspect\n\n[![Build](https://github.com/ionite34/einspect/actions/workflows/build.yml/badge.svg)](https://github.com/ionite34/einspect/actions/workflows/build.yml)\n[![codecov](https://codecov.io/gh/ionite34/einspect/branch/main/graph/badge.svg?token=v71SdG5Bo6)](https://codecov.io/gh/ionite34/einspect)\n[![security](https://snyk-widget.herokuapp.com/badge/pip/einspect/badge.svg)](https://security.snyk.io/package/pip/einspect)\n\n[![PyPI](https://img.shields.io/pypi/v/einspect)][pypi]\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/einspect)][pypi]\n\n[pypi]: https://pypi.org/project/einspect/\n\n> Extended Inspections for CPython\n\n### [Documentation](https://docs.ionite.io/einspect)\n\n- [View and modify memory structures of live objects.](#check-detailed-states-of-built-in-objects)\n- [Able to mutate immutable objects like tuples and ints.](#mutate-tuples-strings-ints-or-other-immutable-types)\n- [Modify slot functions or attributes of built-in types.](#modify-attributes-on-built-in-types)\n- [Fully typed, extensible framework in pure Python.](#move-objects-in-memory)\n\n### Check detailed states of built-in objects\n```python\nfrom einspect import view\n\nls = [1, 2, 3]\nv = view(ls)\nprint(v.info())\n```\n```python\nPyListObject(at 0x2833738):\n   ob_refcnt: Py_ssize_t = 5\n   ob_type: *PyTypeObject = &[list]\n   ob_item: **PyObject = &[&[1], &[2], &[3]]\n   allocated: Py_ssize_t = 4\n```\n\n### Mutate tuples, strings, ints, or other immutable types\n```python\nfrom einspect import view\n\nt = ("A", "B")\nview(t)[1] = 10\nprint(t)\n```\n```python\n("A", 10)\n```\n\n```python\nfrom einspect import view\n\na = "hello"\nb = 100\n\nview(a).buffer[:] = b"world"\nview(b).value = 5\n\nprint("hello", 100)\n```\n```python\nworld 5\n```\n\n### Modify attributes of built-in types\n```python\nfrom einspect import view\n\nv = view(int)\nv["__iter__"] = lambda self: iter(range(self))\nv["__str__"] = lambda self: "custom: " + repr(self)\n\nfor i in 3:\n    print(i)\n```\n```python\ncustom: 0\ncustom: 1\ncustom: 2\n```\n\n### Move objects in memory\n```python\nfrom einspect import view\n\ns = "meaning of life"\n\nv = view(s)\nwith v.unsafe():\n    v <<= 42\n\nprint("meaning of life")\nprint("meaning of life" == 42)\n```\n```python\n42\nTrue\n```\n\n### Fully typed interface\n<img width="551" alt="image" src="https://user-images.githubusercontent.com/13956642/211129165-38a1c405-9d54-413c-962e-6917f1f3c2a1.png">\n\n## Table of Contents\n- [Views](#views)\n  - [Using the `einspect.view` constructor](#using-the-einspectview-constructor)\n  - [Inspecting struct attributes](#inspecting-struct-attributes)\n\n## Views\n\n### Using the `einspect.view` constructor\n\nThis is the recommended and simplest way to create a `View` onto an object. Equivalent to constructing a specific `View` subtype from `einspect.views`, except the choice of subtype is automatic based on object type.\n\n```python\nfrom einspect import view\n\nprint(view(1))\nprint(view("hello"))\nprint(view([1, 2]))\nprint(view((1, 2)))\n```\n> ```\n> IntView(<PyLongObject at 0x102058920>)\n> StrView(<PyUnicodeObject at 0x100f12ab0>)\n> ListView(<PyListObject at 0x10124f800>)\n> TupleView(<PyTupleObject at 0x100f19a00>)\n> ```\n\n### Inspecting struct attributes\n\nAttributes of the underlying C Struct of objects can be accessed through the view\'s properties.\n```python\nfrom einspect import view\n\nls = [1, 2]\nv = view(ls)\n\n# Inherited from PyObject\nprint(v.ref_count)  # ob_refcnt\nprint(v.type)       # ob_type\n# Inherited from PyVarObject\nprint(v.size)       # ob_size\n# From PyListObject\nprint(v.item)       # ob_item\nprint(v.allocated)  # allocated\n```\n> ```\n> 4\n> <class \'tuple\'>\n> 3\n> <einspect.structs.c_long_Array_3 object at 0x105038ed0>\n> ```\n\n## 2. Writing to view attributes\n\nWriting to these attributes will affect the underlying object of the view.\n\nNote that most memory-unsafe attribute modifications require entering an unsafe context manager with `View.unsafe()`\n```python\nwith v.unsafe():\n    v.size -= 1\n\nprint(obj)\n```\n> `(1, 2)`\n\nSince `items` is an array of integer pointers to python objects, they can be replaced by `id()` addresses to modify\nindex items in the tuple.\n```python\nfrom einspect import view\n\ntup = (100, 200)\n\nwith view(tup).unsafe() as v:\n    s = "dog"\n    v.item[0] = id(s)\n\nprint(tup)\n```\n> ```\n> (\'dog\', 200)\n>\n> >> Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)\n> ```\n\nSo here we did set the item at index 0 with our new item, the string `"dog"`, but this also caused a segmentation fault.\nNote that the act of setting an item in containers like tuples and lists "steals" a reference to the object, even\nif we only supplied the address pointer.\n\nTo make this safe, we will have to manually increment a ref-count before the new item is assigned. To do this we can\neither create a `view` of our new item, and increment its `ref_count += 1`, or use the apis from `einspect.api`, which\nare pre-typed implementations of `ctypes.pythonapi` methods.\n```python\nfrom einspect import view\nfrom einspect.api import Py\n\ntup = (100, 200)\n\nwith view(tup).unsafe() as v:\n    a = "bird"\n    Py.IncRef(a)\n    v.item[0] = id(a)\n\n    b = "kitten"\n    Py.IncRef(b)\n    v.item[1] = id(b)\n\nprint(tup)\n```\n> `(\'bird\', \'kitten\')`\n\n🎉 No more seg-faults, and we just successfully set both items in an otherwise immutable tuple.\n\nTo make the above routine easier, you can access an abstraction by simply indexing the view.\n\n```python\nfrom einspect import view\n\ntup = ("a", "b", "c")\n\nv = view(tup)\nv[0] = 123\nv[1] = "hm"\nv[2] = "🤔"\n\nprint(tup)\n```\n> `(123, \'hm\', \'🤔\')`\n',
    'author': 'ionite34',
    'author_email': 'dev@ionite.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ionite34/einspect',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
