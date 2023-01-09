
from importlib import resources

from arclia.happygame.assets import (
  CachingAssetLoader,
  SoundLoader,
  SurfaceLoader,
)

ASSETS_PATH = resources.files(__name__)

GRAPHICS_PATH = ASSETS_PATH / "graphics"
MUSIC_PATH = ASSETS_PATH / "music"
SFX_PATH = ASSETS_PATH / "sfx"

load_surface = SurfaceLoader(GRAPHICS_PATH)
get_surface = CachingAssetLoader(load_surface)

load_sound = SoundLoader(SFX_PATH)
get_sound = CachingAssetLoader(load_sound)
