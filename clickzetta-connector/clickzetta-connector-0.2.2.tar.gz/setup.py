import io
import os

import setuptools

# Package metadata.

name = "clickzetta-connector"
description = "clickzetta python connector"

# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 3 - Alpha"
dependencies = [
    "proto-plus >= 1.22.0, <2.0.0dev",
    "packaging >= 14.3, <22.0.0dev",
    "protobuf>=3.19.5,<5.0.0dev,!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5",
    "python-dateutil >= 2.7.2, <3.0dev",
    "requests >= 2.21.0, < 3.0.0dev",
]
extras = {
    "pandas": ["pandas>=1.0.0", "db-dtypes>=0.3.0,<2.0.0dev"],
    "ipywidgets": ["ipywidgets==7.7.1"],
    "geopandas": ["geopandas>=0.9.0, <1.0dev", "Shapely>=1.6.0, <2.0dev"],
    "ipython": ["ipython>=7.0.1,!=8.1.0"],
    "tqdm": ["tqdm >= 4.7.4, <5.0.0dev"],
}

all_extras = []

for extra in extras:
    all_extras.extend(extras[extra])

extras["all"] = all_extras

# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(package_root, "clickzetta/version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

packages = ['clickzetta','clickzetta.dbapi']

setuptools.setup(
    name=name,
    version=version,
    description=description,
    url='https://www.zettadecision.com/',
    author="mocun",
    author_email="hanmiao.li@clickzetta.com",
    platforms="Posix; MacOS X;",
    packages=packages,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=3.7, <3.11",
    include_package_data=True,
    zip_safe=False,
)
