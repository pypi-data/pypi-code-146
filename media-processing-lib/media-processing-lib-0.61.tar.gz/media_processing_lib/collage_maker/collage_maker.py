"""Collage maker module"""
from pathlib import Path
from multiprocessing import Pool
from typing import List, Callable, Tuple
import numpy as np
from tqdm import trange, tqdm

from .utils import get_closest_square, auto_load_fn, collage_fn
from ..image import image_write, image_resize
from ..logger import logger

class CollageMaker:
    """Collage maker class implementation"""
    def __init__(self, files: List[List[Path]], plot_fns: List[Callable], output_dir: Path, \
            load_fns: List[Callable] = None, names: List[str] = None, \
            rows_cols: Tuple[int, int] = None, resolution: Tuple[int, int] = None,
            n_cores: int = 0):
        assert isinstance(files, List)
        self.files = np.array([[Path(x) for x in y] for y in files])
        self.lens = [len(x) for x in self.files]
        self.output_dir = Path(output_dir)
        self.names = names
        self.rows_cols = get_closest_square(len(self.files)) if rows_cols is None else rows_cols
        self.n_cores = n_cores
        n_outputs = len(self.files)

        # Bravely assuming all items can be plotted the same
        if isinstance(plot_fns, Callable):
            plot_fns = n_outputs * [plot_fns]
        self.plot_fns = plot_fns
        # Bravely assuming we can infer the load fn based on suffixes
        if load_fns is None:
            load_fns = [auto_load_fn(x[0]) for x in self.files]
        # Bravely assuming all items can be loaded the same
        if isinstance(load_fns, Callable):
            load_fns = n_outputs * [load_fns]
        self.load_fns = load_fns

        assert np.std(self.lens) == 0, self.lens
        assert len(self.plot_fns) == n_outputs, f"{len(self.plot_fns)} vs. {n_outputs}"
        if self.names is not None:
            assert len(self.names) == n_outputs, f"{len(self.names)} vs {n_outputs}"
        if self.rows_cols is not None:
            assert self.rows_cols[0] * self.rows_cols[1] >= n_outputs, \
                f"Rows ({self.rows_cols[0]}) * Cols ({self.rows_cols[1]}) < Outputs ({n_outputs})"
        if resolution is None:
            resolution = self._get_resolution()
        self.resolution = resolution

    def _get_resolution(self):
        """Gets the resolution based on first iteration"""
        this_paths = self.files[:, 0]
        items = [load_fn(x) for load_fn, x in zip(self.load_fns, this_paths)]
        images = [plot_fn(x) for plot_fn, x in zip(self.plot_fns, items)]
        result = collage_fn(images, self.rows_cols, self.names)
        return tuple(result.shape[0: 2])

    @staticmethod
    def _do_one(items):
        in_paths, load_fns, plot_fns, out_path, rows_cols, names, resolution = items
        if Path(out_path).exists():
            logger.debug2(f"Out path '{out_path}' exists. Skipping.")
            return
        loaded_items = [load_fn(x) for load_fn, x in zip(load_fns, in_paths)]
        images = [plot_fn(x) for plot_fn, x in zip(plot_fns, loaded_items)]
        collage = collage_fn(images, rows_cols, names)
        collage_resized = image_resize(collage, height=resolution[0], width=resolution[1])
        image_write(collage_resized, out_path)

    def make_collage(self, start_ix: int = None, end_ix: int = None) -> np.ndarray:
        """Function that is called to create the collage"""
        start_ix = start_ix if not start_ix is None else 0
        end_ix = end_ix if not end_ix is None else len(self.files[0])
        assert start_ix < end_ix
        assert end_ix <= len(self.files[0]), f"{end_ix} vs {len(self.files[0])}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        items = []
        for i in range(start_ix, end_ix):
            in_paths = self.files[:, i]
            out_path = f"{self.output_dir}/{i}.png"
            item = [in_paths, self.load_fns, self.plot_fns, out_path, self.rows_cols, self.names, self.resolution]
            items.append(item)

        if self.n_cores == 0:
            _ = [CollageMaker._do_one(items[i]) for i in trange(len(items))]
        else:
            pool = Pool(min(self.n_cores, len(items)))
            pbar = tqdm(total=len(items))
            for _ in pool.imap(CollageMaker._do_one, items):
                pbar.update()

    def __call__(self, *args, **kwargs):
        return self.make_collage(*args, **kwargs)

    def __str__(self) -> str:
        f_str = "[Collage Maker]"
        f_str += f"\n - Num outputs: {len(self.files)}"
        f_str += f"\n - Rows x Cols: {self.rows_cols}"
        f_str += f"\n - Lens: {self.lens}"
        f_str += f"\n - Resolution: {self.resolution}"
        if self.names is not None:
            f_str += f"\n - Names: {self.names}"
        f_str += f"\n - Output dir: '{self.output_dir}'"
        f_str += f"\n - N cores: {self.n_cores}"
        return f_str
