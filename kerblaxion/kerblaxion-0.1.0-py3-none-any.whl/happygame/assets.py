
from os import PathLike
from pathlib import Path
from typing import Tuple, TypeVar, Union, Protocol

from importlib.abc import Traversable
from weakref import WeakValueDictionary

import pygame

PathCoercible = Union[PathLike, str]

T = TypeVar("T")

class AssetLoaderFunc(Protocol[T]):
  def __call__(self,
    k1: PathCoercible,
    *rest: PathCoercible,
  )-> T:
    ...


class SurfaceLoader(AssetLoaderFunc[pygame.surface.Surface]):
  def __init__(self, root: Traversable):
    self.root = root

  def __call__(self,
    k1: PathCoercible,
    *rest: PathCoercible,
  ) -> pygame.surface.Surface:
    target = self.root.joinpath(k1, *rest)
    with target.open("rb") as fin:
      return pygame.image.load(fin)


class SoundLoader(AssetLoaderFunc[pygame.mixer.Sound]):
  def __init__(self, root: Traversable):
    self.root = root

  def __call__(self,
    k1: PathCoercible,
    *rest: PathCoercible,
  ) -> pygame.mixer.Sound:
    target = self.root.joinpath(k1, *rest)
    with target.open("rb") as fin:
      return pygame.mixer.Sound(fin)


class CachingAssetLoader(AssetLoaderFunc[T]):
  def __init__(self, load_asset: AssetLoaderFunc[T]):
    self.__load_asset = load_asset
    self.__cache = WeakValueDictionary[Tuple[str], T]()

  @property
  def load_asset(self):
    return self.__load_asset

  @property
  def cache(self):
    return self.__cache

  def __call__(self,
    k1: PathCoercible,
    *rest: PathCoercible,
  ) -> T:
    key = Path(k1).joinpath(*rest).parts
    v = self.__cache.get(key)
    if v is None:
      v = self.__cache[key] = self.__load_asset(k1, *rest)

    return v
