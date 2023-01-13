import os
from typing import Optional
import tempfile
import subprocess

from solid2.core import scad_render, ObjectBase

__nothing__ = None

def _repr_png_(self):
    """
    Allow rich clients such as the IPython Notebook, to display the current
    OpenSCAD rendering of this object.
    """
    png_data = None
    tmp = tempfile.NamedTemporaryFile(suffix=".scad", delete=False)
    tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    try:
        scad_text = scad_render(self).encode("utf-8")
        tmp.write(scad_text)
        tmp.close()
        tmp_png.close()
        subprocess.Popen([
            "openscad",
            "--preview",
            "-o", tmp_png.name,
            tmp.name
        ]).communicate()

        with open(tmp_png.name, "rb") as png:
            png_data = png.read()
    finally:
        os.unlink(tmp.name)
        os.unlink(tmp_png.name)

    return png_data

ObjectBase._repr_png_ = _repr_png_

