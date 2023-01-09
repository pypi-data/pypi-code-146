import os


import numpy as np
from pudb import set_trace as bp  # noqa
from scipy import signal as sg

import radiocc


#Type = "Quadratic" or "Linear", threshold [m]
def Off_Cor(Type, threshold, Doppler, Diff_doppler, ET, N_data, distance, CODE_DIR,i_integral):
    
    Doppler_debias = np.full(N_data, np.nan)
    Doppler_biasfit = np.full(N_data, np.nan)
    delET = np.full(N_data, np.nan)

    # altitude threshold for fit
    Corr_ind = 0
    for i in range(len(distance)):
        if distance[i] > threshold:  
            Corr_ind += 1
    if Corr_ind == len(distance):
        Corr_ind = Corr_ind-1
    # Search for maximum
    
    if len(Doppler)%2==1 :
        taille = len(Doppler)
    else:
        taille = len(Doppler)-1
        
    Smoothed_Doppler = sg.savgol_filter(Doppler,taille,40)
    deriv = np.gradient(Smoothed_Doppler)

    good=np.logical_and(deriv[np.array(np.where(deriv[:-1]<1E-5))-1]<0,\
                                       deriv[np.array(np.where(deriv[:-1]<1E-5))+1]>0)
    
    
    targ=np.where(deriv[:-1]<1E-5)
    index = targ[0][good[0]]
    good_one = index[-1]

    # FIT
    if Type == 'Fit':
        p = np.polyfit(np.append(ET[:Corr_ind],ET[good_one])\
                         ,np.append(Doppler[:Corr_ind],Doppler[good_one]),2)
        
        for i in range(i_integral,N_data):
            Doppler_biasfit[i] = p[0] * ET[i]**2 + p[1]*ET[i] + p[2]
            
###########################################################################################
    for i in range(N_data):
        delET[i]= ET[i]-ET[0]
      
    # bias fit
    if Type == 'Linear':
        p = np.polyfit(delET[i_integral:Corr_ind],Doppler[i_integral:Corr_ind],1)
        p0 = p[0]
        p1 = p[1]
        for i in range(N_data):
            Doppler_biasfit[i] = p[0] * (delET[i]) + p[1]
            
    elif Type == 'Quadratic': 
        p = np.polyfit(delET[i_integral:Corr_ind],Doppler[i_integral:Corr_ind],2)
        p0 = p[0]
        p1 = p[1]
        p2 = p[2]
        for i in range(N_data):
            Doppler_biasfit[i] = p[0] * (delET[i])**2 + p[1]*(delET[i]) + p[2]
            
    else: 
        print('Type is not recognized')
    
    # subtract bias and scale residual
    for i in range(N_data):
        Doppler_debias[i]  = (Doppler[i]- Doppler_biasfit[i])
    #print(ET[13542],Doppler[13542],Doppler_biasfit[13542], Doppler_debias[13542])
    # back to code directory (why in this subroutine?)   
    # os.chdir(CODE_DIR)
    if Type == 'Linear':
      return ET, delET, Doppler_debias, Doppler_biasfit, Corr_ind, p0, p1
    
    if Type == 'Quadratic':
      return ET, delET, Doppler_debias, Doppler_biasfit, Corr_ind, p0, p1,p2



