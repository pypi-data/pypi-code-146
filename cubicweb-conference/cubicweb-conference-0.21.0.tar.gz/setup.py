#!/usr/bin/env python
# pylint: disable=W0404,W0622,W0704,W0613
# copyright 2003-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr

from os.path import join, dirname
from setuptools import find_packages, setup


here = dirname(__file__)

# load metadata from the __pkginfo__.py file so there is no risk of conflict
# see https://packaging.python.org/en/latest/single_source_version.html
pkginfo = join(here, "cubicweb_conference", "__pkginfo__.py")
__pkginfo__ = {}
with open(pkginfo) as f:
    exec(f.read(), __pkginfo__)

# get required metadatas
distname = __pkginfo__["distname"]
version = __pkginfo__["version"]
license = __pkginfo__["license"]
description = __pkginfo__["description"]
web = __pkginfo__["web"]
author = __pkginfo__["author"]
author_email = __pkginfo__["author_email"]
classifiers = __pkginfo__["classifiers"]

with open(join(here, "README.rst")) as f:
    long_description = f.read()

# get optional metadatas
dependency_links = __pkginfo__.get("dependency_links", ())

requires = {}
for entry in ("__depends__",):  # "__recommends__"):
    requires.update(__pkginfo__.get(entry, {}))
install_requires = [
    "{} {}".format(d, v and v or "").strip() for d, v in requires.items()
]


setup(
    name=distname,
    version=version,
    license=license,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=web,
    classifiers=classifiers,
    packages=find_packages(exclude=["test"]),
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        "cubicweb.cubes": [
            "conference=cubicweb_conference",
        ],
        "cubicweb.i18ncube": [
            "conference=cubicweb_conference.i18n",
        ],
    },
    zip_safe=False,
    python_requires=">=3.7",
)
