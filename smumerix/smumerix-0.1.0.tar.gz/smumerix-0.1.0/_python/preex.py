import smumerix
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def pt1ab():
    def analytical(t: int, alpha: float, k: float):
        return k * t**-alpha

    xs = np.arange(2, 100, dtype=int)

    cross_zero_pdf = smumerix.preex.one_a(1000)
    num_ys = cross_zero_pdf[2:100]
    (alpha, k), _ = curve_fit(analytical, xs, num_ys)

    plt.plot(num_ys)
    plt.plot(analytical(xs, alpha, k))
    plt.show()

    print(alpha, k)  # approx 1.6


def pt1cd():
    def analytical(t: int, alpha: float, k: float):
        return k * t**-alpha

    xs = np.arange(3, 300, dtype=int)

    level_cross_pdf = smumerix.preex.one_b(2, 1000)  # Looks like same form
    num_ys = level_cross_pdf[3:300]

    (alpha, k), _ = curve_fit(analytical, xs, num_ys)
    plt.plot(num_ys)
    plt.plot(analytical(xs, alpha, k))
    plt.show()

    print(alpha, k)  # approx 0.8


pt1ab()
pt1cd()
