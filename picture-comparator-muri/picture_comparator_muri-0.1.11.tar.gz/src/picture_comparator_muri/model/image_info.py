from __future__ import annotations

import os
from typing import Optional, Dict

import imagehash
import magic
from PIL import Image
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QImage
from wand.image import Image as WImage

from picture_comparator_muri.model.exceptions import ImageTooBigException
from picture_comparator_muri.model.file import FileInfo


class ImageQuality:
    def __init__(self, ext: str, lossless: bool, value: int):
        self.ext = ext
        self.value = value
        self.lossless = lossless

    def __gt__(self, other):
        if not isinstance(other, ImageQuality):
            raise TypeError(f"Cannot compare {ImageQuality.__name__} with {type(other)}")
        if self.lossless is None or other.lossless is None:
            return False
        return self.lossless and not other.lossless or self.ext == other.ext and self.value > other.value

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        if not isinstance(other, ImageQuality):
            raise TypeError(f"Cannot compare {ImageQuality.__name__} with {type(other)}")
        if self.lossless is None or other.lossless is None:
            return False
        return not self.lossless and other.lossless or self.ext == other.ext and self.value < other.value

    def __le__(self, other):
        return self < other or self == other

    def __eq__(self, other):
        if not isinstance(other, ImageQuality):
            raise TypeError(f"Cannot compare {ImageQuality.__name__} with {type(other)}")
        return self.lossless and other.lossless or\
               (self.ext is not None and other.ext is not None and self.ext == other.ext) and self.value == other.value

    @classmethod
    def from_wimage(cls, wimage: WImage) -> ImageQuality:
        format_map = {
            'PNG': ('png', True, 100),
            'JPEG': ('jpeg', False, wimage.compression_quality),
            'WEBP': ('webp', wimage.compression_quality == 100, 0)
        }
        return cls(*format_map.get(wimage.format, (None, None, None)))


class ImageInfo:
    SIZE_LIMIT = 0x2000000

    def __init__(self, path: str, realpath: str):
        self.path = path
        self.real_path = realpath
        self.index: Optional[int] = None  # Index in list of all found images
        self.identical_group: Optional[int] = None
        image = Image.open(path)
        if image.width * image.height >= self.SIZE_LIMIT:
            raise ImageTooBigException(path)
        # a_hash = imagehash.average_hash(image)
        hash = imagehash.whash(image)
        self.hash = []
        for h in hash.hash:
            self.hash.extend(h)
        self.hash = tuple(self.hash)
        self.selected: bool = False
        self.marked_for_deletion: bool = False
        self._file_size: int = 0
        self._quality: Optional[ImageQuality] = None
        self._qimage: Optional[QImage] = None
        self._catche = {}
        self._cache_width: Dict[int, int] = {}

    def __repr__(self):
        return f'{self.__class__.__name__}({self.path})'

    @property
    def file_size(self):
        if not self._file_size:
            self._file_size = os.path.getsize(self.path)
        return self._file_size

    @property
    def is_link(self) -> bool:
        return os.path.islink(self.path)

    @classmethod
    def from_path_if_image(cls, path: str) -> Optional[ImageInfo]:
        path: str = os.path.abspath(path)
        realpath: str = os.path.realpath(path)
        if not os.path.exists(realpath):
            return None
        mime = magic.from_file(realpath, mime=True)
        if not mime.startswith('image/'):
            return None
        return cls(path, realpath)

    def is_identical(self, other: ImageInfo) -> bool:
        if self.width() != other.width() or self.height() != other.height():
            return False
        return self.qimage().bits() == other.qimage().bits()  # TODO; check how time consuming it is

    def qimage(self, size: QSize = None):
        if self._qimage is None:
            self._qimage = QImage(self.path)
        if size is None:
            return self._qimage
        img = self._catche.get(size)
        if img is None:
            img = self._qimage.scaled(size, Qt.KeepAspectRatio)
            self._catche[size] = img
        return img

    def scaled_width(self, height: int) -> int:
        width = self._cache_width.get(height)
        if width is None:
            image = self.qimage()
            width = round(height * image.width() / image.height()) if image.height() else 0
        return width

    def height(self) -> int:
        return self.qimage().height()

    def width(self) -> int:
        return self.qimage().width()

    def size(self) -> QSize:
        return self.qimage().size()

    def ratio(self) -> float:
        return self.qimage().width() / self.qimage().height()

    @property
    def quality(self) -> ImageQuality:
        if self._quality is None:
            wimg = WImage(filename=self.path)
            self._quality = ImageQuality.from_wimage(wimg)
        return self._quality

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        if isinstance(other, FileInfo):
            return self.path == other.path
        if not isinstance(other, ImageInfo):
            return False
        return self.path == other.path
