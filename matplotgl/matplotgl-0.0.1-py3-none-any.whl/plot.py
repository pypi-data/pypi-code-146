from .line import Line


def plot(ax, x, y, **kwargs):
    line = Line(ax=ax, x=x, y=y, **kwargs)
    ax.add_artist(line)
    ax.autoscale()
    return line
