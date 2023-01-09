#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:46:27 2019

@author: ananya
"""

import numpy as np

def Elec(N_data, refractivity, e, eps0, me,Bande,fsup,c):

    if Bande == 'X':
        f_TX=(fsup)*(880./749.)  # downward X-band
    if Bande == 'S':
        f_TX=(fsup)*(240./749.)  # downward S-band
    if Bande == 'Diff':
        f_TX=(fsup)*(240./749.)  # downward S-band


    Ne = np.full(N_data,np.nan)#np.array([np.nan for i in range( N_data )], float)

    for i in range(N_data):

        Ne[i] = - (refractivity[i]*1E-6)/40.31*f_TX**2
        #Ne_dn[i] = -2*np.pi*(refractivity[i]*1E-6)/(2.818E-15*(c/f_TX)**2)

        #Ne_dn[i] = - refractivity[i]*(8*np.pi**2*me*eps0*f_TX**2)/(e**2)*1E-6
    #print(f_TX)
    #print(Ne[1600])
    return Ne


def TEC_Calc(N_data, Ne, Corr_ind, i_Surface, bend_radius, R_Mars):

    TEC = np.full(N_data,np.nan)#np.array([np.nan for i in range( N_data )], float)
    TEC_loc = 0.
    for i in range(Corr_ind+1, i_Surface):

        if Ne[i] > 0:

            TEC_loc += Ne[i] * ((bend_radius[i-1]-bend_radius[i])) / 1.0e16
            TEC[i] = TEC_loc

    #print np.shape(TEC)
    #print('')
    #print('')
    print('\t ELECTRON DENSITY DONE')
    #print('')
    #print('')

    return TEC
