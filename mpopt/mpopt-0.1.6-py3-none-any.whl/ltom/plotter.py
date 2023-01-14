import yaml
import math
import numpy as np
from scipy import integrate
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

log_filename = "output.yaml"
track_filename = "scurve.yaml"


def lagrangeInterpolation(x, y, order=4):
    p = np.zeros((order + 1, order + 1))
    for i in range(order + 1):
        c = poly.polyfromroots([x[m] for m in range(order + 1) if m != i])
        p[i, :] = c / poly.polyval(x[i], c)
    return np.matmul(y, p)


def interpolate(x, y, xx, order=4):
    _x = np.reshape(x[:-1], (-1, order))
    _x = np.hstack((_x, np.vstack((_x[1:, 0:1], x[-1]))))
    _y = np.reshape(y[:-1], (-1, order))
    _y = np.hstack((_y, np.vstack((_y[1:, 0:1], y[-1]))))
    sections = _x.shape[0]
    # print(xx.shape, sections)
    _xx = np.reshape(xx[:-1], (sections, -1))
    _xx = np.hstack((_xx, np.vstack((_xx[1:, 0:1], xx[-1]))))

    _yy = np.array(
        [
            poly.polyval(_xx_, lagrangeInterpolation(_x_, _y_, order))
            for _x_, _y_, _xx_ in zip(_x, _y, _xx)
        ]
    )

    yy = np.zeros_like(xx)
    yy[-1] = _yy[-1, -1]
    yy[:-1] = [_ for _ in _yy[:, :-1].flat]

    return yy


def cubicBrezierCurve(s, P, breakpt):
    t = (s - breakpt[0]) / (breakpt[1] - breakpt[0])

    return (
        (1 - t) ** 3 * P[0]
        + 3 * (1 - t) ** 2 * t * P[1]
        + 3 * (1 - t) * t ** 2 * P[2]
        + t ** 3 * P[3]
    )


def getPath(track):
    s_start = track["d"]["breakpoints"][0]
    s_stop = track["goal"]

    s = np.arange(s_start, s_stop, 0.01)

    n_d = len(track["d"]["ctrlpoints"])
    n_theta = len(track["theta"]["ctrlpoints"])

    d = np.zeros_like(s)
    for i in range(n_d):
        d += cubicBrezierCurve(
            s, track["d"]["ctrlpoints"][i], track["d"]["breakpoints"][i : i + 2]
        ) * (
            np.heaviside(s - track["d"]["breakpoints"][i] + 1e-4, 0.5)
            - np.heaviside(s - track["d"]["breakpoints"][i + 1], 0.5)
        )

    theta = np.zeros_like(s)
    for i in range(n_theta):
        theta += cubicBrezierCurve(
            s, track["theta"]["ctrlpoints"][i], track["theta"]["breakpoints"][i : i + 2]
        ) * (
            np.heaviside(s - track["theta"]["breakpoints"][i] + 1e-4, 0.5)
            - np.heaviside(s - track["theta"]["breakpoints"][i + 1], 0.5)
        )

    x = integrate.cumtrapz(np.cos(theta), x=s, initial=0)
    y = integrate.cumtrapz(np.sin(theta), x=s, initial=0)

    x_l = x - d * np.sin(theta)
    y_l = y + d * np.cos(theta)

    x_r = x + d * np.sin(theta)
    y_r = y - d * np.cos(theta)

    return (x, y, x_l, y_l, x_r, y_r)


def drawTrack(track):
    (x, y, x_l, y_l, x_r, y_r) = getPath(track)

    plt.plot(x, y, linestyle="dashed", linewidth=3, color=(0.8500, 0.3250, 0.0980))
    plt.plot(x_l, y_l, linewidth=3, color=(0.3, 0.3, 0.3))
    plt.plot(x_r, y_r, linewidth=3, color=(0.3, 0.3, 0.3))


def drawPlot(
    x,
    y,
    theta,
    t=None,
    l=0.01,
    cmap="copper",
    xlim=None,
    ylim=None,
    with_arrow=False,
    title=None,
    order=4,
):
    if xlim is None:
        xlim = [min(x) - 1, max(x) + 1]
    if ylim is None:
        ylim = [min(y) - 1, max(y) + 1]

    # plt.xlim(xlim)
    # plt.ylim(ylim)

    if t is not None:
        sections = (len(x) - 1) / 4
        tt = np.linspace(t[0], t[-1], 100 * 64 + 1)
        x = interpolate(t, x, tt, order=order)
        y = interpolate(t, y, tt, order=order)

        plt.plot(x, y, linewidth=4, color=(0, 0.4470, 0.7410))
    else:
        # plt.scatter(x, y, cmap=cmap, c=-np.arange(len(x)), s=16)
        plt.plot(x, y, linewidth=1, color=(0, 0.4470, 0.7410))

        if with_arrow:
            plt.quiver(
                x,
                y,
                l * np.cos(theta),
                l * np.sin(theta),
                -np.arange(len(x)),
                cmap=cmap,
                angles="xy",
            )

    # if title is not None:
    #     plt.suptitle(title)


def drawStates(t, data, title="Open Loop States", order=4):
    t_max = max(t)

    fig, axs = plt.subplots(7, 1, sharex=True, num=title, figsize=(10, 8))

    labels = [
        "$X$ [$m$]",
        "$Y$ [$m$]",
        "$\\theta$ [$rad$]",
        "$\\delta$ [$rad$]",
        "$v_x$ [$m/s$]",
        "$v_y$ [$m/s$]",
        "$\\omega$ [$rad/s$]",
    ]

    for i in range(7):
        sections = (len(data[i]) - 1) / 4
        tt = np.linspace(t[0], t[-1], 100 * 64 + 1)
        x = interpolate(t, data[i], tt, order=order)

        axs[i].plot(tt, x, linewidth=2, color=(0.8500, 0.3250, 0.0980))
        axs[i].set_ylabel(labels[i])
    axs[i].set_xlabel("Time [s]")

    # plt.suptitle(title)
    plt.tight_layout()


def drawCtrl(t, data, title="Open Loop Control", order=4):
    t_max = max(t)

    fig, axs = plt.subplots(3, 1, sharex=True, num=title, figsize=(10, 8))

    labels = [
        "Front Driving Force [$N$]",
        "Rear Driving Force [$N$]",
        "Steering Angle Rate [$rad/s$]",
    ]

    for i in range(3):
        sections = (len(data[i]) - 1) / 4
        tt = np.linspace(t[0], t[-1], 100 * 64 + 1)
        x = interpolate(t, data[i], tt, order=order)

        axs[i].plot(tt, x, linewidth=2, color=(0.8500, 0.3250, 0.0980))
        axs[i].set_ylabel(labels[i])
    axs[i].set_xlabel("Time [s]")

    # plt.suptitle(title)
    plt.tight_layout()


if __name__ == "__main__":
    with open(log_filename, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    with open(track_filename, "r") as f:
        track = yaml.load(f, Loader=yaml.FullLoader)

    plt.figure("Open Loop")
    _data = zip(*data["OpenLoop"])
    drawTrack(track)
    drawPlot(
        _data[0], _data[1], _data[2], t=_data[-3], with_arrow=False, title="Open Loop"
    )
    plt.ylabel("Y [$m$]")
    plt.xlabel("X [$m$]")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

    drawStates(_data[-3], _data[:-3], title="Open Loop States")

    drawCtrl(_data[-3], zip(*data["OpenCtrl"]), title="Open Loop Control")

    plt.figure("Vehicle Motion in path coordinate frame")
    plt.plot(_data[-2], _data[-1])
    plt.ylim(-6.5, 6.5)
    plt.xlim(0, track["goal"])
    plt.ylabel("Distance from centerline [$m$]")
    plt.xlabel("Track Distance [$m$]")
    # plt.figure("Closed Loop")
    # _data = zip(*data["CloseLoop"])
    # drawPlot(_data[0], _data[1], _data[2],
    #         title="Closed Loop")

    # plt.figure("Closed Loop Control")
    # _data_ctrl = zip(*data["CloseCtrl"])
    # drawCtrl(_data[3][1:], _data_ctrl[0], np.rad2deg(_data_ctrl[1]),
    #          v_max=2,
    #          delta_max=50,
    #          title="Closed Loop Control")

    plt.show()
