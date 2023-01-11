# Copyright 2022 Rockabox Media Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

AUTH = ["google-cloud-firestore>=2.3,<3"]
MANIFEST = ["boto3<2", "opencv-python-headless==4.4.0.46"]
MAPS = [
    "googlemaps>=4.4.2,<5",
]
NOTIFICATIONS = [
    "google-cloud-pubsub>=2.9,<3",
]
QUEUES = [
    "redis>3.5,<4.2",
    "hiredis==2.0.0",
    "rq==1.10.1",
    "rq-scheduler==0.11.0",
]
STORAGE = ["google-cloud-storage>=2.1,<3"]
TASKS = ["google-cloud-tasks>=2.7,<3"]


setup(
    name="rbx",
    version="3.0.3",
    license="Apache 2.0",
    description="Scoota Platform utilities",
    long_description="A collection of common tools for Scoota services.",
    url="http://scoota.com/",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet",
    ],
    author="The Scoota Engineering Team",
    author_email="engineering@scoota.com",
    python_requires=">=3.7",
    install_requires=[
        "arrow>=1,<2",
        "cachetools>=4.2.4,<6",
        "Click<9",
        "colorama",
        "PyYAML>=5.4.1",
        "requests>=1.21.1",
    ],
    extras_require={
        # These are requirement bundles required for specific feature sets.
        "auth": AUTH,
        "buildtools": [
            "bumpversion==0.5.3",
            "check-manifest",
            "fabric~=2.5.0",
            "twine",
        ],
        "geo": MAPS,
        "manifest": MANIFEST,
        "notifications": NOTIFICATIONS,
        "platform": AUTH + MANIFEST + MAPS + NOTIFICATIONS + QUEUES,
        "queues": QUEUES,
        "storage": STORAGE,
        "tasks": TASKS,
        # Include them all for the test suite.
        "test": AUTH + MANIFEST + MAPS + NOTIFICATIONS + QUEUES + STORAGE + TASKS,
    },
    entry_points={
        "console_scripts": [
            "buildtools = rbx.buildtools.cli:program.run [buildtools]",
            "buildcreative = rbx.manifest.cli:build_creative [manifest]",
            "geocode = rbx.geo.cli:geocode [geo]",
            "reverse_geocode = rbx.geo.cli:reverse_geocode [geo]",
            "unpack = rbx.geo.cli:unpack [geo]",
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["*.md", "*.yaml"],
    },
)
