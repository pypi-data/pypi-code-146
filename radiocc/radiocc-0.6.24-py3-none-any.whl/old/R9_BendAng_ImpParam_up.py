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

def Bend_up(N_data, r_MEX, z_MEX, z_GS, vr_MEX, vz_MEX, vr_GS, vz_GS, gamma, beta_e, delta_s, Doppler_debias,fsup,c, DATA_TYPE: Optional[radiocc.model.RadioDataType]):
    a = np.stack((r_MEX, z_MEX, z_GS, vr_MEX, vz_MEX, vr_GS, vz_GS, gamma, beta_e, delta_s, Doppler_debias))
    # np.savetxt("/home/greg/code/oth/radio-occult/r9_up_py.txt", a)


    delta_r_up = np.zeros((N_data,))
    beta_r_up = np.zeros((N_data,))


    #c = 299792458 # 3.0E8  # m s^-1
    fs= fsup  # upward X-band signal

    for i in range(N_data):

        vrs = vr_MEX[i]    # velocity of the spacecraft  along the r axes in the occultation plane coordinate system
        vzs = vz_MEX[i]    # velocity of the spacecraft  along the z axes in the occultation plane coordinate system

        vrt = vr_GS[i]     # velocity of the G/S  along the r axes in the occultation plane coordinate system
        vzt = vz_GS[i]     # velocity of the G/S  along the z axes in the occultation plane coordinate system

        rs = r_MEX[i]      # position of the spacecraft  along the r axes in the occultation plane coordinate system
        zs = z_MEX[i]      # position of the spacecraft  along the z axes in the occultation plane coordinate system
        zt = z_GS[i]       # position of the G/S  along the z axes in the occultation plane coordinate system

        gammarad = gamma[i]
        betaErad = beta_e[i]
        deltaSrad = delta_s[i]

        DeltaR=0.;
        BetaR=0.;

        #cABetaRall = np.array([np.nan for k in range(100)], dtype = float)
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
        delta_r_up[i] = DeltaR
        #delta_r_up.append(DeltaR)
        #print('delta_r_up[i]: ' + str(delta_r_up[i]))

        beta_r_up[i] = BetaR
        #beta_r.append(BetaR)


    bend_ang_up = np.zeros((N_data,))

    imp_param_up = np.zeros((N_data,))


    for i in range(N_data):

        alpha = delta_r_up[i] + beta_r_up[i]

        bend_ang_up[i] = alpha

        a = (np.sqrt(r_MEX[i]**2 + z_MEX[i]**2)) * np.sin(beta_e[i] - beta_r_up[i] - gamma[i])

        imp_param_up[i] = a

    #print("Bending angle and Impact parameter: done")
    #print(fs)
    #print (Doppler_debias)
    print('\t BENDING ANGLE UP DONE')
    #print('beta_r[0]: ' + str(beta_r[-1]))
    #print('delta_r_up[0]: ' + str(delta_r_up[-1]))
    #sys.exit()

    return imp_param_up, bend_ang_up, delta_r_up, beta_r_up
