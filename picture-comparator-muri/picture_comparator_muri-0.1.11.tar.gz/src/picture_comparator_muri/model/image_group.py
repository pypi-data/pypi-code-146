from __future__ import annotations
from typing import Iterable, List, Dict

from PySide6.QtCore import QFile

from picture_comparator_muri.model.image_info import ImageInfo


class ImageGroup:
    def __init__(self):
        self.images: List[ImageInfo] = []

    def add_images(self, images: Iterable[ImageInfo]):
        self.images.extend(images)
        self.images.sort(key=lambda a: a.path)

    def set_identical(self):
        groups: List[List[ImageInfo]] = []
        for image in self.images:
            found = False
            for group in groups:
                if image.is_identical(group[0]):
                    group.append(image)
                    found = True
                    break
            if not found:
                groups.append([image])
        id = 0
        for group in groups:
            if len(group) > 1:
                for image in group:
                    image.identical_group = id
                id += 1
            else:
                group[0].identical_group = None

    def reset_identical(self):
        """
        Should be run after removing image from group. Searches for markers and if there's only one of given id left,
        removes the marker.
        """
        groups: Dict[int: List[ImageInfo]] = {}
        for image in self.images:
            if image.identical_group is not None:
                group = groups.get(image.identical_group)
                if not group:
                    group = []
                    groups[image.identical_group] = group
                group.append(image)
        for group in groups.values():
            if len(group) == 1:
                group[0].identical_group = None

    def merge(self, other: ImageGroup):
        to_add = []
        for image in other:
            if image not in self.images:
                to_add.append(image)
        self.images.extend(to_add)
        self.images.sort(key=lambda a: a.path)

    def clear_markings(self):
        for image in self.images:
            image.selected = False
            image.marked_for_deletion = False

    def marked_for_deletion(self):
        return [i for i in self if i.marked_for_deletion]

    def has_marked(self) -> bool:
        return any(i.marked_for_deletion for i in self.images)

    def delete_marked(self) -> List[ImageInfo]:
        to_delete = self.marked_for_deletion()
        not_removed: List[ImageInfo] = []
        for image in to_delete:
            if QFile.moveToTrash(image.path):
                self.images.remove(image)
            else:
                not_removed.append(image)
        return not_removed

    def rename(self, renames: Dict[str, str]):
        for image in self.images:
            if image.path in renames:
                image.path = renames[image.path]
        self.images.sort(key=lambda a: a.path)

    def __iter__(self) -> Iterable[ImageInfo]:
        return iter(self.images)

    def __len__(self):
        return len(self.images)

    def __hash__(self):
        return hash(tuple(i.path for i in self.images))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(a == b for a, b in zip(self.images, other.images))
