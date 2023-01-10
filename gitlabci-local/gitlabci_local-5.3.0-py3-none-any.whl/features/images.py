#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from typing import Any, Dict, List

# Components
from ..engines.engine import Engine
from ..types.lists import Lists

# ImagesFeature class
class ImagesFeature:

    # Members
    __engine: Engine
    __images: List[str]
    __options: Namespace

    # Constructor
    def __init__(self, jobs: Dict[str, Dict[str, Any]], options: Namespace) -> None:

        # Prepare jobs
        self.__jobs = jobs

        # Prepare options
        self.__options = options

        # Prepare engine
        self.__engine = Engine(self.__options)

        # Prepare images
        self.__images = []
        self.__prepare_images()

    # Filter
    def __filter(self, job: str) -> bool:

        # Filter jobs list
        if not self.__options.pipeline and self.__options.names and not Lists.match(
                self.__options.names, job, ignore_case=self.__options.ignore_case,
                no_regex=self.__options.no_regex):
            return False

        # Filter stages list, pylint: disable=duplicate-code
        if self.__options.pipeline and self.__options.names and not Lists.match(
                self.__options.names, self.__jobs[job]['stage'],
                ignore_case=self.__options.ignore_case, no_regex=self.__options.no_regex):
            return False

        # Result
        return True

    # Prepare images
    def __prepare_images(self) -> None:

        # Iterate through images
        for job in self.__jobs:

            # Filter jobs
            if not self.__filter(job):
                continue

            # Extract job image
            image = self.__jobs[job]['image']
            if image and not self.__jobs[job][
                    'options'].host and image not in self.__images:
                self.__images += [image]

            # Extract job services
            for service in self.__jobs[job]['services']:
                if service['image'] not in self.__images:
                    self.__images += [service['image']]

        # Sort images
        self.__images.sort()

    # Pull
    def pull(self) -> bool:

        # Pull images
        for image in self.__images:
            self.__engine.pull(image, self.__options.force)

        # Result
        return bool(self.__images)

    # Remove images
    def rmi(self) -> bool:

        # Remove images
        for image in self.__images:
            self.__engine.rmi(image)

        # Result
        return bool(self.__images)
