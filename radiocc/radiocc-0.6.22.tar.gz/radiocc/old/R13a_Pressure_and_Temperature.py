import numpy as np
#import scipy as sc

def Temp_Pre(N_data, T_BC, Nn, bend_radius, i_neut_upp, i_Surface, kB, G, m_bar, M_Mars,refractivity):

    P = np.array([np.nan for i in range( N_data )], float)
    T = np.array([np.nan for i in range( N_data )], float)
    
    #T[i_neut_upp] = T_BC 
    P[i_neut_upp] = T_BC * Nn[i_neut_upp] * kB

    for i in range(i_neut_upp+1, i_Surface):
    
        gg = G * M_Mars / (bend_radius[i])**2
        #gg1 = G * M_Mars / (bend_radius[i-1])**2

        dz = (bend_radius[i-1] - bend_radius[i])

        P[i] = P[i-1] + 0.5 * (Nn[i] + Nn[i-1]) * gg * m_bar * dz
       # P[i] = P[i-1] + 0.5 * (Nn[i]*gg + Nn[i-1]*gg1) * m_bar * dz
       # T[i] = T[i-1]*refractivity[i_neut_upp]/refractivity[i-1] + T[i-1] +  0.5 * (Nn[i]*gg + Nn[i-1]*gg1) * m_bar * dz / ( Nn[i] * kB)
       # T[i] = T[i-1] + 0.5 * (Nn[i]*gg + Nn[i-1]*gg1) * m_bar * dz / ( Nn[i] * kB)

    for i in range(N_data):

        #P[i] = T[i] * ( Nn[i] * kB )
        T[i] = P[i] / ( Nn[i] * kB )
        
    return P, T


    #print('')
    #print('')
    print('\tR14: Done')
    #print('')
    #print('')
