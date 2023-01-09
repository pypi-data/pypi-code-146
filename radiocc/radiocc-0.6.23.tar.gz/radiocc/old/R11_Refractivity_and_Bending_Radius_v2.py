import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
import scipy.integrate as sci
from pudb import set_trace as bp  # noqa: F401


def Abel_num(N_data, Corr_ind, i_Surface, imp_param, bend_ang, R_Mars):

    def integrand(x, alpha, aj):

        return alpha / np.sqrt(x**2 - aj**2)

    ref_index    = np.full(N_data, np.nan) #np.array([np.nan for i in range(N_data)], float)
    bend_radius  = np.full(N_data, np.nan)#np.array([np.nan for i in range(N_data)], float)
    refractivity = np.full(N_data, np.nan)#np.array([np.nan for i in range(N_data)], float)
    Sum_tot      = np.full(N_data, np.nan)#np.array([np.nan for i in range(N_data)], float)

    for i in range(Corr_ind, i_Surface):

        aj = imp_param[i]
        alpha_0 = bend_ang[0]
        aj_0 = imp_param[0]
        I0 = (1./np.pi) * sci.quad(integrand, aj_0, np.inf, args=(alpha_0, aj))[0]

        Sum = I0
        for j in range(Corr_ind,i+1):
            alpha = (bend_ang[j] + bend_ang[j-1])/2.0
            Sum += -(1./np.pi) * sci.quad(integrand, imp_param[j], imp_param[j-1], args=(alpha, aj))[0]

        Sum_tot[i] = Sum
        ref_index[i] = np.exp(Sum)
        bend_radius[i] = aj/np.exp(Sum)
        refractivity[i] = (np.exp(Sum) - 1.0)*1E6


    #print(I0, Sum)
    print('\tR11: Done')
    #print('')
    #print('')

    return ref_index, refractivity,bend_radius, Sum_tot



def Abel_Analytical(N_data, Corr_ind, i_Surface, imp_param, bend_ang, R_Mars):

    Sum_tot      = np.full(N_data, np.nan)
    refractivity = np.array([np.nan for i in range(N_data)], float)
    bend_radius  = np.array([np.nan for i in range(N_data)], float)

    A = np.array([np.nan for i in range(N_data)], float)
    B = np.array([np.nan for i in range(N_data)], float)

    for i in range(0,N_data):
        alpha_loc  = bend_ang[i:i+2]
        a_loc      = imp_param[i:i+2]
        A[i], B[i] = np.polyfit(a_loc, alpha_loc, 1)

    ref_index = None

    for j in range(Corr_ind, i_Surface):

        Sum_1 = 0
        for k in range(Corr_ind, j):
            Sum_1 += A[k] * (np.sqrt(imp_param[k+1]**2 - imp_param[j]**2) - \
                      np.sqrt(imp_param[k]**2 - imp_param[j]**2))\
                      + B[k] * np.log(np.abs((imp_param[k+1] +\
                      np.sqrt(imp_param[k+1]**2 - imp_param[j]**2))/(imp_param[k] +\
                             np.sqrt(imp_param[k]**2 - imp_param[j]**2))))

        refractivity[j] = (np.exp((1./sc.pi) * Sum_1) - 1.0)*1.0e6
        bend_radius[j]  = imp_param[j] / np.exp(Sum_1 / sc.pi)
        ref_index=bend_radius

    #print(Corr_ind)
    #print('')
    print('\t REFRACTIVITY AND BENDING RADIUS DONE')
    #print('')
    #print('')
    #plt.plot(refractivity)
    return ref_index,refractivity, bend_radius, Sum_tot



