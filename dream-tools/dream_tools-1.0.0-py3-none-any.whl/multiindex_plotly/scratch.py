import os
import sys

sys.path.insert(0, os.getcwd())

import dreamtools as dt
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

# Dette er muligvis nødvendigt afhængingt af installationen
pd.options.plotting.backend = "plotly"
import plotly.io as pio
pio.renderers.default = "browser"

# Indlæs banker
r = dt.REFERENCE_DATABASE = dt.Gdx("C:/Users/B031441/Desktop/CommitOftere/Model/Gdx/dynamic_calibration2.gdx")

fig = lambda: dt.plot(r.qY[r.s], names=list(r.s.texts), xline=2017, layout={"yaxis_title": "Mia. kr."})
fig().show()
dt.small_figure(fig()).show()
# dt.large_figure(fig()).show()
dt.small_figure(fig()).write_image(r"C:\Users\B031441\Documents\Filkassen\Rapportering\1.png")
dt.small_figure(dt.age_figure_2d(r.qC_a, years=[2017], yaxis_title_text="Foobar")).write_image(r"C:\Users\B031441\Documents\Filkassen\Rapportering\2.png")
dt.small_figure(dt.plot([r.qX, r.qC, r.qG], xline=2017, layout={"yaxis_title": "Mia. kr."})).write_image(r"C:\Users\B031441\Documents\Filkassen\Rapportering\3.png")

pio.orca.shutdown_server()

pd.DataFrame({"a.uArv": a.uArv, "b.uArv": b.uArv, "c.uArv": c.uArv}).plot()

def age3d(series, t_start=2016, t_end=2099, a_start=0, a_end=100, title="", ztitle=""):
  age = list(range(a_start, a_end+1))
  time = list(range(t_start, t_end+1))
  value = series.loc[age, time].unstack().values
  surface = go.Surface(x=time, y=age, z=value)
  return go.Figure(
    surface,
    layout={
      "scene": {
        "xaxis": {"title": "År", "autorange": "reversed"},
        "yaxis": {"title": "Alder", "autorange": "reversed"},
        "zaxis": {"title": ztitle},
      },
      "title": {"text": title, 'x': 0.5, "y": 0.925}
    }
  )

figures = [
  age3d(c.vC_a, 2015, 2099, a_end=99, title="Forbrug (vC_a)", ztitle="Mio. kr. (vækst- og inflations-korrigeret)"),
  age3d(c.vHhx, 2015, 2099, a_end=99, title="Formue ekskl. pension, bolig og realkreditgæld (vHhx)", ztitle="Mio. kr. (vækst- og inflations-korrigeret)"),
  age3d(c.vBolig, 2015, 2099, a_end=99, title="Bolig-formue (vBolig)", ztitle="Mio. kr. (vækst- og inflations-korrigeret)"),
  age3d(c.vHh["Net"], 2015, 2099, a_end=99, title="Netto finansiel formue (vHh[Net])",
        ztitle="Mio. kr. (vækst- og inflations-korrigeret)"),
]
figures_to_html(figures, "aldersprofiler2.html")

v = "rDisk"
df = pd.DataFrame({
  # f"a.{v}": a[v].sort_index().loc[0:100, [2017, 2040]],
  f"b.{v}": b[v].sort_index().loc[0:100, [2017, 2065]],
  f"c.{v}": c[v].sort_index().loc[0:100, [2017, 2065]],
}).unstack()
df.columns = ["".join(str(i)) for i in df]
df.plot(title=v)

def debeta(beta):
  return 1/beta - 1 - 0.1

from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter, gauss_spline
from scipy.interpolate import UnivariateSpline

def spline(x, y, s=None, k=3, padding=1):
  if s is None:
    s = len(x) * np.std(y[1:]/y[:-1].values) ** 2
  padded = [*[x[0] for _ in range(padding)], *x, *[x[-1] for _ in range(padding)]]
  return pd.Series(UnivariateSpline(padded, y[padded], k=k, s=s)(x), x)

figs = []
b.rDisk_a = 1/(1+b.rDisk_a)
for var_name, a_start, smoothness in [
  ("rDisk_a", 18, 3),
  # ("uBolig_a", 18, 4),
  # #  ("uBoligHtM_a", 18, 0.3),
  # ("fProdHh_a", 15, 3),
  # ("ftBund", 15, 3),
  # ("ftKommune", 15, 3),
  # ("rTopSkatInd", 15, 3),
  # ("fvPersInd_a", 15, 2),
  # # ("cHh_a", 0, 4),
  # ("rRealKred2Bolig_a", 18, 2),
  # ("rvCLejeBolig", 18, 3),
  # ("uBoernFraHh_a", 0, 3),
]:
  x = np.array(range(a_start,101))
  df = {}
  for t in [2017]:
    y = 1/(1+b[var_name].sort_index().loc[a_start:100].loc[:,t])
    df[f"{var_name}[{t}]"] = y
    df[f"gaussian[{t}], sigma={smoothness}"] = pd.Series(gaussian_filter1d(y, smoothness, mode="nearest"), x)
    # df[f"savgol[{t}]"] = pd.Series(savgol_filter(y, 11, 2, mode="nearest"), x)
    # df[f"MA[{t}]"] = y.rolling(5, min_periods=0).mean()
    # df[f"UnivariateSpline[{t}], k=3, s={smoothness}"] = pd.Series(UnivariateSpline(x, y, k=3, s=smoothness)(x), x)
    # df[f"UnivariateSpline[{t}], k=5, s={smoothness}"] = pd.Series(UnivariateSpline(x, y, k=5, s=smoothness)(x), x)
    # df[f"Spline, s={smoothness}"] = spline(x, y, smoothness)
    # df["Spline, padding=0, k=3"] = spline(x, y, padding=0, k=3)
    # df["Spline, padding=0, k=5"] = spline(x, y, padding=0, k=5)
    # df["Spline, padding=1, k=3"] = spline(x, y, padding=1, k=3)
    # df["Spline, padding=10, k=3"] = spline(x, y, padding=10, k=3)
    # df["Spline, s=std*span"] = spline(x, y, padding=0)
    # df["gauss_spline"] = pd.Series(gauss_spline(y.values, 3), x)
  figs.append(px.line(df, title=var_name))
figures_to_html(figs)




def figures_to_html(figs, filename="dashboard.html"):
  dashboard = open(filename, 'w')
  dashboard.write("<html><head></head><body>" + "\n")
  for fig in figs:
    inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
    dashboard.write(inner_html)
  dashboard.write("</body></html>" + "\n")




figures = []
for i in ["Alder", "Kap", "Pens", "PensX"]:
  figures.append(age3d(a.nPop * a.vPensIndb.loc[i], title=f"Indbetaling, {i}"))
  figures.append(age3d(a.nPop * a.vPensUdb.loc[i], title=f"Udbetaling, {i}"))
figures_to_html(figures, "pensions.html")


r = b.rDisk_a[b.rDisk_a != 0][:,2017]
px.line({
  "gaussian": gaussian_filter1d(1/(1+r), 5, mode="nearest"),
  # "beta_first_s=3": gaussian_filter1d(1/(1+r), 3, mode="nearest"),
  "golsov": savgol_filter(1/(1+r), 21, 2, mode="nearest"),
  "smooth_first": (1/(1+gaussian_filter1d(r, 5, mode="nearest"))),
  "beta": 1/(1+r),
}).show()


from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter, wiener, medfilt
from scipy.ndimage import gaussian_filter1d, gaussian_laplace

figs = []
y = 1/(1+b.rDisk).loc[18:100].loc[:,2017]
x = b.rDisk.index.values
var_name="rDisk"
df = {
  var_name: 1/y - 1.1,
  # "s=0.005": UnivariateSpline(x, y, k=3, s=0.005)(x),
  # "s=0.01": UnivariateSpline(x, y, k=3, s=0.01)(x),
  # "s=0.1": UnivariateSpline(x, y, k=3, s=0.1)(x),
  # "s=1": UnivariateSpline(x, y, k=3, s=1)(x),
  # "s=100": UnivariateSpline(x, y, k=3, s=100)(x),
  # "s=std*span": UnivariateSpline(x, y, k=3, s=np.std(y)*(max(y)-min(y)))(x),
  # "savgol, 15": savgol_filter(y, 15, 3, mode="nearest"),
  # "gaussian 1": gaussian_filter1d(y, 1, mode="nearest"),
  # "gaussian 2": gaussian_filter1d(y, 2, mode="nearest"),
  "gaussian 3, nearest": 1/gaussian_filter1d(y, 3, mode="nearest")-1.1,
  "gaussian 3": 1/gaussian_filter1d(y, 3)-1.1,
  "gaussian 3, 19+": 1/(np.append(y.values[0], gaussian_filter1d(y.loc[19:], 3)))-1.1,
  # "gaussian 4": gaussian_filter1d(y, 4, mode="nearest"),
  # f"gaussian, sigma={smoothness}": gaussian_filter1d(y, smoothness, mode="nearest"),
  # "polynomial(deg=7)": np.polynomial.Polynomial.fit(x, y, 7).linspace(83)[1],
  # "lowess(frac=0.1)": lowess(y, x, frac=0.1, return_sorted=False),
}
figs.append(px.line(df, title=var_name))
figures_to_html(figs)

