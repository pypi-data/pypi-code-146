#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 20:17:48 2020

@author: ananya
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sc
import radiocc
from pudb import set_trace as bp #noqa: F401

def PLOT1( distance,Doppler,Doppler_debias,refractivity, Ne,PLOT_DIR,item):
    
    if radiocc.gui is not None:
        figure = radiocc.gui.figure
        figure.clear()
    else:
        figure = plt.figure(6)
        plt.ion()
        plt.show()

    Doppler=np.array(Doppler)
    Doppler_debias=np.array(Doppler_debias)
    cond_dop = Doppler<1 
    cond_deb = Doppler_debias<1

    axis_left = figure.add_subplot(131)
    axis_middle = figure.add_subplot(132)
    axis_right = figure.add_subplot(133)
    figure.tight_layout(pad=3.0)
    figure.suptitle("Radio Occultation")
    figure.text(0.04, 0.5, "Altitude (km)", va="center", ha="center", rotation="vertical")
    axis_left.plot(
        Doppler, distance / 1000, ":", color="black", label="Raw L2 Data"
    )  # (1+880./749.)
    axis_left.plot(
        Doppler_debias, distance / 1000, ":", color="blue", label="Debias Raw L2 Data"
    )  # (1+880./749.)

    
    Doppler = Doppler[cond_dop]
    Doppler_debias = Doppler_debias[cond_deb]
        
    min_x1 = np.nanmedian(Doppler_debias)- sc.median_absolute_deviation(Doppler_debias,nan_policy='omit')*5
    min_x2 = np.nanmedian(Doppler)- sc.median_absolute_deviation(Doppler,nan_policy='omit')*5
    max_x1 = np.nanmedian(Doppler_debias)+ sc.median_absolute_deviation(Doppler_debias,nan_policy='omit')*5
    max_x2 = np.nanmedian(Doppler)+ sc.median_absolute_deviation(Doppler,nan_policy='omit')*5    
    min_x = min([min_x1,min_x2])
    max_x = max([max_x1,max_x2])

    axis_left.set_xlabel("Doppler Frequency Residual (Hz)")
    axis_left.set_ylim(3400, 4000)
    axis_left.set_xlim(min_x, max_x)
    axis_left.grid(True)
    axis_left.legend()

    axis_middle.plot(
        np.array(refractivity),
        np.array(distance / 1000),
        ":",
        color="blue",
        label="after correction",
    )

    axis_middle.set_xlabel("Refractivity")
    axis_middle.set_ylim(3400, 4000)
    axis_middle.set_xlim(-0.05, 0.05)  # S band
    axis_middle.grid(True)

    axis_right.plot(
        np.array(Ne)* 1e-6 , np.array(distance / 1000), ":", color="blue", label="after correction"
    )
    axis_right.set_xlabel("Electron density (el/cm$^{3}$)")
    axis_right.set_xlim(-5.0e4, 5.0e4)
    axis_right.set_ylim(3400, 4000)
    axis_right.grid(True)

    figure.savefig(PLOT_DIR + "/" + "Ne_before-Corr.svg", dpi=100)

    if radiocc.gui is not None:
        radiocc.gui.draw()
    else:
        plt.pause(1.0)
        input("Press [enter] to continue.")
        plt.close()


    print('\t PLOT CHECK DONE')
    
    return 

def PLOT2( distance,Doppler,Doppler_debias,refractivity, Nn,PLOT_DIR,item):
    """
    Doppler=np.array(Doppler)
    Doppler_debias=np.array(Doppler_debias)
    cond_dop = Doppler<1 
    cond_deb = Doppler_debias<1

    fig6 = plt.figure(6) 
    plt.ion()
    plt.show()
    plt.plot(Doppler,distance/1000,':', color='black',label = 'Raw L2 Data')#(1+880./749.)
    plt.plot(Doppler_debias,distance/1000,':', color='blue', label = 'Debias Raw L2 Data')#(1+880./749.)
    
    Doppler = Doppler[cond_dop]
    Doppler_debias = Doppler_debias[cond_deb]
        
    min_x1 = np.nanmedian(Doppler_debias)- sc.median_absolute_deviation(Doppler_debias,nan_policy='omit')*5
    min_x2 = np.nanmedian(Doppler)- sc.median_absolute_deviation(Doppler,nan_policy='omit')*5
    max_x1 = np.nanmedian(Doppler_debias)+ sc.median_absolute_deviation(Doppler_debias,nan_policy='omit')*5
    max_x2 = np.nanmedian(Doppler)+ sc.median_absolute_deviation(Doppler,nan_policy='omit')*5    
    min_x = min([min_x1,min_x2])
    max_x = max([max_x1,max_x2])
    plt.xlabel('Doppler Frequency Residuals (Hz)')
    plt.ylabel('Altitude (km)')
    
    plt.ylim(3400, 4000)
    plt.xlim(min_x, max_x)
    plt.grid(True)
    plt.legend()
    fig6.set_size_inches(6, 10) #
    plt.savefig(PLOT_DIR+'/'+'Doppler-before-corr.png',dpi=600)
    plt.pause(1.0)
    input("Press [enter] to continue.")
    #plt.close()
    
    
    
    fig10 = plt.figure(10)    
    plt.ion()
    plt.show()            
    plt.plot(np.array(refractivity),np.array(distance/1000),':', color='blue', label ='after correction')
                     
    plt.xlabel('Refractivity')
    plt.ylabel('Altitude (km)')
        
    plt.ylim(3400,4000)
    plt.xlim(-0.05,0.05)# S band
    plt.grid(True)
    fig10.set_size_inches(6, 10) #Inch
    
    plt.savefig(PLOT_DIR+'/'+'refractivity-before-corr.png',dpi=600)
    plt.pause(1.0)    
    input("Press [enter] to continue.")
    #plt.close()
    """

    if radiocc.gui is not None:
        figure = radiocc.gui.figure
        figure.clear()
    else:
        figure = plt.figure(4)
        plt.ion()
        plt.show()

    axis = figure.add_subplot(111)
    figure.suptitle("Radio Occultation")

    axis.plot(np.array(Nn), np.array(distance / 1000), ":", color="blue", label="after correction")
    axis.set_xlabel("Neutral density (el/cm$^{3}$)")
    axis.set_ylabel("Altitude (km)")
    axis.grid(True)
    #axis.set_xlim(xmin=-1e22, xmax=3e23)
    # axis.ylim(3400, 4000)

    figure.savefig(PLOT_DIR + "/" + "Nn_before-Corr.svg", dpi=100)

    if radiocc.gui is not None:
        radiocc.gui.draw()
    else:
        plt.pause(1.0)
        input("Press [enter] to continue.")
        plt.close()

    
    print('\t PLOT CHECK DONE')
    
    return 
