"""MPLVideoApply is a lazy MPLVideo with a apply function applied for each frame"""
from functools import lru_cache
from .utils import build_video_write_fn

class MPLVideoApply:
    """Wrapper that applies a function on top of the getitem"""
    def __init__(self, base_video: "MPLVideo", apply_fn: "FrameApplyFn"):
        self.base_video = base_video
        self.apply_fn = apply_fn

    @lru_cache
    def __getitem__(self, key):
        item = self.base_video[key]
        applied_item = self.apply_fn(item, self, key)
        assert len(applied_item.shape) == 3 and applied_item.shape[-1] == 3
        assert applied_item.shape[0: 2] == self.base_video.frame_shape, \
            f"Apply functions changed the expected shape. {applied_item.shape[0: 2]} vs {self.base_video.frame_shape}"
        return applied_item

    @property
    def fps(self):
        """The frames per second of this mpl video"""
        return self.base_video.fps

    @property
    def shape(self):
        """The shape of this mpl video"""
        return self.base_video.shape

    @property
    def frame_shape(self):
        """The frame shape of this mpl video"""
        return self.base_video.frame_shape

    def write(self, path: str, video_lib: str = "imageio", **kwargs):
        """Write the video to disk"""
        f_write = build_video_write_fn(video_lib)
        f_write(self, path, **kwargs)

    def save(self, *args, **kwargs):
        """Write the video to disk"""
        self.write(*args, **kwargs)

    def __len__(self):
        return self.base_video.__len__()

    def apply(self, apply_fn):
        """Apply a new function on top of this applied video"""
        return MPLVideoApply(self, apply_fn)

    def __str__(self) -> str:
        f_str = str(self.base_video)
        f_str += f"\n -  Apply fn: {self.apply_fn}"
        return f_str
