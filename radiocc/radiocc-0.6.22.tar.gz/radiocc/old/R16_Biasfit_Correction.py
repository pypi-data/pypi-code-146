#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 07:32:42 2020

@author: ananya
"""
import radiocc

import numpy as np
def Off_Cor2(Type, Doppler, Diff_doppler, ET, delET, N_data, distance):
    Doppler_debias2 = np.full(N_data, np.nan)
    Doppler_biasfit2 = np.full(N_data, np.nan)
    
        
    if Type == 'Linear':
        #p = np.polyfit(ET[i_integral:Corr_ind],Doppler[i_integral:Corr_ind],1)
        if radiocc.gui is not None:
            p0 = radiocc.gui.get_intercept()
            p1 = radiocc.gui.get_slope()
        else:
            p0 = float(input("Enter the new p[0], i.e; p[0] +dp[0] = " ))
            p1 = float(input("Enter the new p[1], i.e; p[1] +dp[1] = " ))
        for i in range(N_data):
            #Doppler_biasfit2[i] = p0 * (ET[i]) + p1
            Doppler_biasfit2[i] = p0 * (delET[i]) + p1
        p2 = None
            
            
    elif Type == 'Quadratic': 
        #p = np.polyfit(ET[i_integral:Corr_ind],Doppler[i_integral:Corr_ind],2)
        if radiocc.gui is not None:
            p0 = radiocc.gui.get_intercept()
            p1 = radiocc.gui.get_slope()
            p2 = radiocc.gui.get_quadratic()
        else:
            p0 = float(input("Enter the new p[0], i.e; p[0] +dp[0] = " ))
            p1 = float(input("Enter the new p[1], i.e; p[1] +dp[1] = " ))
            p2 = float(input("Enter the new p[2], i.e; p[2] +dp[2] = " ))
        for i in range(N_data):
            #Doppler_biasfit2[i] = p0 * (ET[i])**2 + p1*(ET[i]) + p2
            Doppler_biasfit2[i] = p0 * (delET[i])**2 + p1*(delET[i]) + p2
            
    else: 
        print('Type is not recognized')
        
    for i in range(N_data):
        Doppler_debias2[i]  = (Doppler[i]- Doppler_biasfit2[i])
        #print(ET[13542],Doppler[13542],Doppler_biasfit2[13542], Doppler_debias2[13542])    
    return Doppler_debias2, Doppler_biasfit2, p0, p1, p2
