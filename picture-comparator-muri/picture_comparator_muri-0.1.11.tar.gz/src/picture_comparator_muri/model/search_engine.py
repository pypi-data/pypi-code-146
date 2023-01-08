from __future__ import annotations

import os
from typing import Optional, Set, List, Dict

from PIL import UnidentifiedImageError
from PySide6.QtCore import QObject, QThread, Signal
from numpy import ndarray
from sklearn.neighbors import BallTree

from picture_comparator_muri.controller.settings import Settings
from picture_comparator_muri.model.exceptions import ImageTooBigException
from picture_comparator_muri.model.image_group import ImageGroup
from picture_comparator_muri.model.image_info import ImageInfo


class SearchThread(QThread):
    def __init__(self, search_engine: SearchEngine):
        super().__init__()
        self.search_engine = search_engine
        self.all_dirs: Set[str] = set()
        self.image_tree = None

    @property
    def settings(self) -> Settings:
        return self.search_engine.settings

    @property
    def images(self) -> List[ImageInfo]:
        return self.search_engine.images

    @property
    def images_hash_map(self):
        return self.search_engine.images_hash_map

    @property
    def raw_results(self):
        return self.search_engine.raw_results

    @raw_results.setter
    def raw_results(self, value):
        self.search_engine.raw_results = value

    @property
    def groups(self):
        return self.search_engine.groups

    @property
    def group_map(self):
        return self.search_engine.group_map

    def run(self) -> None:
        self._scan_files()
        self._find_results()
        self.images.clear()
        self.images_hash_map.clear()

    def _scan_files(self):
        for directory in self.settings.directories:
            self._add_directory(directory)

    def _add_directory(self, directory: str):
        self.all_dirs.add(directory)
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if os.path.isdir(path):
                if self.settings.scan_subdirectories and path not in self.all_dirs:
                    self._add_directory(path)
            else:
                try:
                    image = ImageInfo.from_path_if_image(path)
                except ImageTooBigException as e:
                    print(e.args[0])
                    self.search_engine.LoadingImageFailed.emit('Image too big', path)
                    continue
                except UnidentifiedImageError as e:
                    print(e.args[0])
                    self.search_engine.LoadingImageFailed.emit('Loading image failed', path)
                    continue
                if image:
                    self._add_image(image)
        self.search_engine.ImageSearchEnded.emit()

    def _add_image(self, image: ImageInfo):
        image.index = len(self.images)
        self.images.append(image)

        hash_arr = self.images_hash_map.get(image.hash)
        if not hash_arr:
            hash_arr = []
            self.images_hash_map[image.hash] = hash_arr
        hash_arr.append(image)

        self.search_engine.ImageFound.emit(image)

    def _find_results(self):
        X = [image.hash for image in self.images]
        if X:
            self.image_tree = BallTree(X)
            self.raw_results = self.image_tree.query_radius(X, 3)
            for result in self.raw_results:
                if len(result) < 2:
                    continue
                main_group = None  # group to which all other groups will be merged if there are multiple ones
                new_group = []  # indices for images that weren't part of any group previously

                for index in result:
                    group = self.group_map.get(index)
                    if not group:
                        new_group.append(index)
                    elif main_group is None:
                        main_group = group
                    elif main_group is not group:
                        for image in group:
                            self.group_map[image.index] = main_group
                        main_group.merge(group)
                        self.groups.remove(group)

                if main_group is None:
                    main_group = ImageGroup()
                    self.groups.append(main_group)

                images = [self.images[i] for i in new_group]
                main_group.add_images(images)
                for index in new_group:
                    self.group_map[index] = main_group

        self.search_engine.ResultsReady.emit(self.groups)
        self.image_tree = None


class SearchEngine(QObject):
    ImageFound = Signal(ImageInfo)
    LoadingImageFailed = Signal(str, str)
    ImageSearchEnded = Signal()
    ResultsReady = Signal(list)

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings: Settings = settings
        self.search_thread: Optional[SearchThread] = None

        self.images: List[ImageInfo] = []
        self.images_hash_map = {}
        self.raw_results: Optional[ndarray] = None
        self.groups: List[ImageGroup] = []
        self.group_map: Dict[int, ImageGroup] = {}

    def start_comparison(self):
        self.search_thread = SearchThread(self)
        self.search_thread.start()
