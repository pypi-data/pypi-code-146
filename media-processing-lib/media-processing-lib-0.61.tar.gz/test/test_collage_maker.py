import tempfile
import shutil
import numpy as np
from pathlib import Path
from media_processing_lib.image import image_write
from media_processing_lib.collage_maker import CollageMaker, collage_fn

def test_collage_maker_1():
    images = np.random.randint(0, 255, size=(3, 10, 30, 30, 3), dtype=np.uint8)
    tmpDir = Path(tempfile.mkdtemp())
    for i in range(images.shape[0]):
        (tmpDir / f"{i}").mkdir(exist_ok=True, parents=True)
        for j in range(images.shape[1]):
            image_write(images[i][j], f"{tmpDir}/{i}/{j}.png")

    files = [[f"{tmpDir}/{i}/{j}.png" for j in range(images.shape[1])] for i in range(images.shape[0])]
    plotFns = lambda x: x
    outputDir = tmpDir / "outputDir"
    maker = CollageMaker(files, plotFns, outputDir)
    maker.make_collage()
    shutil.rmtree(tmpDir)

def test_collage_fn_1():
    images = np.random.randint(0, 255, size=(3, 420, 420, 3), dtype=np.uint8)
    collage = collage_fn(images)
    assert collage.shape == (840, 840, 3)
