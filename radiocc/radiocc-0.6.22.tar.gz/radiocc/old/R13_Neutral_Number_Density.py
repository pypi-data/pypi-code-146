import numpy as np
from pudb import set_trace as bp  # noqa:F401


# import matplotlib.pyplot as plt
def Neut(N_data, bend_radius, refractivity, d_neut_upp, i_Surface, C1, kB):

    i_neut_upp = np.where(bend_radius >= d_neut_upp)[0][-2]
    Nn = np.array([np.nan for i in range(N_data)], float)

    for i in range(i_neut_upp, i_Surface):

        Nn[i] = refractivity[i] / C1 * 1e-6
    # print(refractivity, Nn)
    # print('')
    print("\t NEUTRAL DENSITY DONE")
    # print('')
    # print('')

    return Nn, i_neut_upp
