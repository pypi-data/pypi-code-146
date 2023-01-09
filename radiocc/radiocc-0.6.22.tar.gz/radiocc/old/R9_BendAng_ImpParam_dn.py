#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 10:56:32 2019

@author: ananya
"""

from typing import Optional

import numpy as np
from pudb import set_trace as bp

import radiocc

def Bend_dn(N_data, r_MEX, z_MEX, z_GS, vr_MEX, vz_MEX, vr_GS, vz_GS, gamma, beta_e, delta_s, Doppler_debias,Bande,fsup,c,DATA_TYPE: Optional[radiocc.model.RadioDataType]):
    a = np.stack((r_MEX, z_MEX, z_GS, vr_MEX, vz_MEX, vr_GS, vz_GS, gamma, beta_e, delta_s, Doppler_debias))
    # np.savetxt("/home/greg/code/oth/radio-occult/r9_dn_py.txt", a)

    delta_r_dn = np.zeros((N_data,))
    beta_r_dn= np.zeros((N_data,))


    #c = 3.0E8   #m s^-1
    if Bande == 'X':
        fs=(fsup)*(880./749.)  # downward X-band
    else :
        fs=(fsup)*(240./749.)  # downward S-band

    for i in range(N_data):

        vrs = vr_MEX[i]
        vzs = vz_MEX[i]

        vrt = vr_GS[i]
        vzt = vz_GS[i]

        rs = r_MEX[i]
        zs = z_MEX[i]
        zt = z_GS[i]

        gammarad = gamma[i]
        betaErad = beta_e[i]
        deltaSrad = delta_s[i]

        DeltaR=0.;
        BetaR=0.;

        #ABetaRall = np.array([np.nan for k in range(100)], dtype = float)
        #ADeltaRall = np.array([np.nan for k in range(100)], dtype = float)
        #DeltaR_loc = np.array([np.nan for k in range(100)], dtype = float)
        #BetaR_loc = np.array([np.nan for k in range(100)], dtype = float)
        epsilon = 999
        stock= 0
        while np.abs(epsilon)>1E-3:

            if DATA_TYPE is not None and DATA_TYPE == radiocc.model.RadioDataType.EGRESS:

                b11 = vzs*np.cos(betaErad-BetaR)+vrs*np.sin(betaErad-BetaR)

                b12 = vzt*np.sin(deltaSrad-DeltaR)+vrt*np.cos(deltaSrad-DeltaR)

                b21=(np.sqrt((rs**2)+(zs**2)))*np.cos(betaErad-gammarad-BetaR)

                b22=zt*np.cos(deltaSrad-DeltaR)

                k1= c*((Doppler_debias[i])/fs)-vrs*(np.cos(betaErad-BetaR)-np.cos(betaErad))\
                    +vzs*(np.sin(betaErad-BetaR)-np.sin(betaErad))\
                    +vrt*(np.sin(deltaSrad-DeltaR)-np.sin(deltaSrad))\
                    -vzt*(np.cos(deltaSrad-DeltaR)-np.cos(deltaSrad))

                k2=zt*np.sin(deltaSrad-DeltaR)+(np.sqrt(rs**(2)+zs**(2)))*np.sin(betaErad-gammarad-BetaR);
            else:

                b11 = vzs*np.cos(betaErad-BetaR)-vrs*np.sin(betaErad-BetaR)

                b12 = vzt*np.sin(deltaSrad-DeltaR)-vrt*np.cos(deltaSrad-DeltaR)

                b21=(np.sqrt((rs**2)+(zs**2)))*np.cos(betaErad-gammarad-BetaR)

                b22=zt*np.cos(deltaSrad-DeltaR)

                k1= c*((Doppler_debias[i])/fs)+vrs*(np.cos(betaErad-BetaR)-np.cos(betaErad))\
                    +vzs*(np.sin(betaErad-BetaR)-np.sin(betaErad))\
                    -vrt*(np.sin(deltaSrad-DeltaR)-np.sin(deltaSrad))\
                    -vzt*(np.cos(deltaSrad-DeltaR)-np.cos(deltaSrad))

                k2=zt*np.sin(deltaSrad-DeltaR)+(np.sqrt(rs**(2)+zs**(2)))*np.sin(betaErad-gammarad-BetaR);

            ABetaR=(k1-b12*k2/b22)/(b11-b21/b22*b12)

            ADeltaR=(k2-b21*ABetaR)/b22

            #ABetaRall[j] = ABetaR

            #ADeltaRall[j] = ADeltaR

            DeltaR=DeltaR+ADeltaR

            BetaR=BetaR+ABetaR

            epsilon = ADeltaR-stock
            stock= ADeltaR



            #DeltaR_loc[j] = DeltaR

            #BetaR_loc[j] = BetaR


        #print('final value: ' + str(DeltaR))
        delta_r_dn[i] = DeltaR
        #delta_r.append(DeltaR)
        #print('delta_r[i]: ' + str(delta_r[i]))

        beta_r_dn[i] = BetaR
        #beta_r.append(BetaR)


    bend_ang_dn = np.zeros((N_data,))

    imp_param_dn = np.zeros((N_data,))


    for i in range(N_data):

        alpha = delta_r_dn[i] + beta_r_dn[i]

        bend_ang_dn[i] = alpha

        a = (np.sqrt(r_MEX[i]**2 + z_MEX[i]**2)) * np.sin(beta_e[i] - beta_r_dn[i] - gamma[i])

        imp_param_dn[i] = a

    #print("Bending angle and Impact parameter: done")
    #print(fs)
    #print (Doppler_debias)
    print('\t BENDING ANGLE DN DONE ')
    #print('beta_r[0]: ' + str(beta_r[-1]))
    #print('delta_r[0]: ' + str(delta_r[-1]))
    #sys.exit()

    return imp_param_dn, bend_ang_dn, delta_r_dn, beta_r_dn
