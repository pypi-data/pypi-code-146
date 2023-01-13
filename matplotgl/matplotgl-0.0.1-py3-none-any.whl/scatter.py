from .points import Points


def scatter(ax, x, y, **kwargs):
    pts = Points(ax=ax, x=x, y=y, **kwargs)
    ax.add_artist(pts)
    ax.autoscale()
    return pts
