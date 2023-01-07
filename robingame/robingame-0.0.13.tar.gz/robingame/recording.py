import logging
import functools
import glob
import multiprocessing
import os
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

import pygame
from pygame import Surface
from robingame.objects import Game

logger = logging.getLogger(__file__)


def clean_empty_recordings_dir(output_dir: Path):
    try:
        os.mkdir(output_dir.as_posix())
    except FileExistsError:
        pass

    # clear old files
    files = glob.glob((output_dir / "*").as_posix())
    for file in files:
        os.remove(file)


def save_image_async(filename, img_string: bytes, size: tuple[int, int], output_dir: Path):
    image = pygame.image.fromstring(img_string, size, "RGBA")
    pygame.image.save(image, str(output_dir / f"{filename}.png"))


def save_images_async(images: list[Surface], output_dir: Path, processes: int):
    stringified = (
        (
            pygame.image.tostring(image, "RGBA"),
            image.get_size(),
        )
        for image in images
    )
    with multiprocessing.Pool(processes=processes) as pool:
        result = pool.starmap(
            func=save_image_async,
            iterable=(
                (ii, string, size, output_dir) for ii, (string, size) in enumerate(stringified)
            ),
        )
    return result


def create_videos(output_dir: Path, filename: str):
    mp4_file = output_dir / f"{filename}.mp4"
    gif_file = output_dir / f"{filename}.gif"
    subprocess.run(
        [
            "ffmpeg",
            "-r",
            "60",
            "-i",
            str(output_dir / "%d.png"),
            "-r",
            "60",
            str(mp4_file),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    print(f"Created {mp4_file}")
    subprocess.run(
        [
            "ffmpeg",
            "-r",
            "60",
            "-i",
            str(output_dir / "%d.png"),
            "-filter_complex",
            # credit: https://superuser.com/questions/1049606/reduce-generated-gif-size-using-ffmpeg
            (
                "fps=30,"
                "scale=1080:-1:flags=lanczos,"
                "split[s0][s1];[s0]"
                "palettegen=max_colors=32[p];[s1][p]"
                "paletteuse=dither=bayer"
            ),
            str(gif_file),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    print(f"Created {gif_file}")


def decorate_draw(func, screenshots):
    @functools.wraps(func)
    def wrapped(self, surface: Surface, debug: bool = False):
        # normal _draw call
        func(self, surface, debug)

        # also do _draw onto a new screenshot surface which we store
        screenshot = Surface(surface.get_size()).convert_alpha()
        func(self, screenshot, debug)
        screenshots.append(screenshot)

    return wrapped


def decorate_main(func, screenshots: deque, output_dir: Path, filename: str, processes: int):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        """Run the game as normal, but intercept the quit signal and save all the screenshots to
        file."""
        try:
            func(*args, **kwargs)
        except SystemExit:
            print("Deleting old images/videos...")
            clean_empty_recordings_dir(output_dir)
            print(f"Saving {len(screenshots)} images...")
            t1 = time.perf_counter()
            save_images_async(screenshots, output_dir, processes=processes)
            t2 = time.perf_counter()
            print(f"Images saved in {t2-t1}s")
            print("Creating videos...")
            create_videos(output_dir, filename)
        pygame.quit()
        sys.exit()

    return wrapped


def record(
    cls: Game = None,
    *,
    n_frames: int,
    output_dir: Path,
    filename="out",
    processes=4,
):
    """
    Patch the Game's ._draw() and .main() methods so that we keep a screenshot of every frame,
    which we later stitch into videos.
    """
    output_dir = output_dir or Path(__file__).parent / "recordings"
    screenshots = deque(maxlen=n_frames)

    def decorate(cls):
        cls._draw = decorate_draw(cls._draw, screenshots=screenshots)
        cls.main = decorate_main(
            cls.main,
            screenshots=screenshots,
            output_dir=output_dir,
            filename=filename,
            processes=processes,
        )
        return cls

    return decorate(cls) if cls else decorate
