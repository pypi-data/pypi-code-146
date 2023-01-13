import os
import sys
sys.path.insert(0, os.getcwd())
# os.chdir("../..")

import pytest
import numpy as np
import pandas as pd
import dreamtools as dt
from PIL import Image

def test_plotting():
  """
  Plotting is difficult to unit test, but we can at least test that the functions run without errors.
  Visual inspection is required to verify that the plots are correct.
  """
  dt.REFERENCE_DATABASE = dt.Gdx("test.gdx")
  s = dt.Gdx("test.gdx")

  dt.time(2025, 20260)
  df1 = dt.DataFrame(
    [s.qC, s.qG, s.qI, s.qX, s.qM],
    names=["Privat forbrug (qC)", "Offentligt forbrug (qG)", "Investeringer (qI)", "Eksport (qX)", "Import (qM)"]
  )
  fig1 = df1.plot()
  assert fig1 == df1.plot()
  
  df2 = dt.DataFrame(
    [s.qC, s.qG, s.qI, s.qX, s.qM],
    "pq",
    names=["Privat forbrug (qC)", "Offentligt forbrug (qG)", "Investeringer (qI)", "Eksport (qX)", "Import (qM)"]
  )
  fig2 = df2.plot(small_figure=True)
  
  df3 = dt.DataFrame(s.qY[s.s], names=list(s.s.texts))
  fig3 = df3.plot()
  assert dt.plot(s.qY[s.s], names=list(s.s.texts)) == fig3

  dt.write_image(fig1, "test1.png", scale=1)
  dt.write_image(fig2, "test2.png", scale=1)
  dt.write_image(fig3, "test3.png", scale=1)

  assert round(Image.open("test1.png").width / 96 * 2.54, 1) == 15.5, "Large figure is not the correct width (pixels × DPI)"
  assert round(Image.open("test2.png").width / 96 * 2.54, 1) == 7.6, "Small figure is not the correct width (pixels × DPI)"
  
def test_yaxis_title():
  dt.REFERENCE_DATABASE = dt.Gdx("test.gdx")
  s = dt.Gdx("test.gdx")
  df = dt.DataFrame(s.qY, "m")
  assert df.plot().layout.yaxis.title.text == ""
  assert df.plot(layout=dict(yaxis_title="y-axis title")).layout.yaxis.title.text == ""
  assert df.plot(layout=dict(yaxis_title="y-axis title"), horizontal_yaxis_title=False).layout.yaxis.title.text == "y-axis title"
  