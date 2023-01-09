#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 19:52:33 2020

@author: ananya
"""

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc
from pudb import set_trace as bp  # noqa

import radiocc


def PLOT_Dop1(distance, Doppler, Doppler_debias, Doppler_biasfit, ET, PLOT_DIR, N_data, DATA_TYPE: Optional[radiocc.model.RadioDataType]):
    import matplotlib

    if radiocc.gui is not None:
        figure = radiocc.gui.figure
        figure.clear()
    else:
        # matplotlib.use("TkAgg")
        figure = plt.figure(6)
        plt.ion()

    axis_left = figure.add_subplot(131)
    axis_middle = figure.add_subplot(132)
    axis_right = figure.add_subplot(133)
    #figure.suptitle("Radio Occultation")
    #figure.text(0.5, 0.04, "Doppler Frequency Residuals (Hz)", va="center", ha="center")
    #figure.text(
    #    0.04, 0.5, "Altitude (km)", va="center", ha="center", rotation="vertical"
    #)

    Doppler = np.array(Doppler)
    Doppler_debias = np.array(Doppler_debias)
    cond_dop = Doppler < 1
    cond_deb = Doppler_debias < 1

    axis_left.plot(
        Doppler, distance / 1000, ":", color="black", label="Raw L2 Data"
    )  # (1+880./749.)
    axis_left.plot(
        Doppler_debias,
        distance / 1000,
        ":",
        color="blue",
        label="Debias Raw L2 Data",
    )  # (1+880./749.)

    # FIXME:
    # + MEX enables lines below but not MAVEN, do we keep that?
    # + same for comment below 'xlim'
    #
    # Doppler = Doppler[cond_dop]
    # Doppler_debias = Doppler_debias[cond_deb]

    min_x1 = (
        np.nanmedian(Doppler_debias)
        - sc.median_abs_deviation(Doppler_debias, nan_policy="omit") * 5
    )
    min_x2 = (
        np.nanmedian(Doppler)
        - sc.median_abs_deviation(Doppler, nan_policy="omit") * 5
    )
    max_x1 = (
        np.nanmedian(Doppler_debias)
        + sc.median_abs_deviation(Doppler_debias, nan_policy="omit") * 5
    )
    max_x2 = (
        np.nanmedian(Doppler)
        + sc.median_abs_deviation(Doppler, nan_policy="omit") * 5
    )

    if np.isnan(min_x1) and np.isnan(max_x1):
        min_x = min_x2
        max_x = max_x2
    else:
        min_x = min([min_x1, min_x2])
        max_x = max([max_x1, max_x2])

    axis_left.set_ylim(3389, distance.max()/1e3)
    axis_left.set_xlim(min_x, max_x)
    axis_left.set_xlabel('frequency Res.')
    axis_left.set_ylabel('Altitude (km)')
    axis_left.grid(True)
    #axis_left.legend()
    axis_right.clear()
    delET = []  # np.full(N_data, np.nan)
    if DATA_TYPE is not None and DATA_TYPE == radiocc.model.RadioDataType.EGRESS:
        for i in range(N_data):
            delET.append(ET[i] - ET[-1])
  
        axis_right.plot(
            np.array(delET), np.negative(np.flip(Doppler)), "-", color="black", label="Raw L2 Data"
        )
    else:
        for i in range(N_data):
            delET.append(ET[i] - ET[0])
        axis_right.plot(
            np.array(delET), Doppler, "-", color="black", label="Raw L2 Data"
        )  # (1+880./749.)
    
    min_x1 = (
        np.nanmedian(Doppler_debias)
        - sc.median_abs_deviation(Doppler_debias, nan_policy="omit") * 5
    )
    min_x2 = (
        np.nanmedian(Doppler)
        - sc.median_abs_deviation(Doppler, nan_policy="omit") * 5
    )
    max_x1 = (
        np.nanmedian(Doppler_debias)
        + sc.median_abs_deviation(Doppler_debias, nan_policy="omit") * 5
    )
    max_x2 = (
        np.nanmedian(Doppler)
        + sc.median_abs_deviation(Doppler, nan_policy="omit") * 5
    )

    if np.isnan(min_x1) and np.isnan(max_x1):
        min_x = min_x2
        max_x = max_x2
    else:
        min_x = min([min_x1, min_x2])
        max_x = max([max_x1, max_x2])

    axis_right.set_ylim(min_x, max_x)
    #axis_right.set_xlim(0, 800)
    #axis_right.set_ylim(-0.3, 0.3)
    axis_right.set_ylabel('frequency Res.')
    axis_right.set_xlabel('time (sec)')
    axis_right.grid(True)
    axis_right.legend()
    
    
    axis_middle.clear()
    axis_middle.plot(
        np.array(delET), np.negative(np.flip(Doppler_debias)), "-", color="blue", label="Debiased L2 Data"
    )  # (1+880./749.)
  
    axis_middle.set_ylim(min_x, max_x)
    #axis_right.set_xlim(0, 800)
    #axis_right.set_ylim(-0.3, 0.3)
    axis_middle.set_ylabel('frequency Res.')
    axis_middle.set_xlabel('time (sec)')
    axis_middle.grid(True)
    axis_middle.legend()

    figure.savefig(PLOT_DIR + "/" + "Doppler_1.svg", dpi=100)
    if radiocc.gui is not None:
        radiocc.gui.draw()
    else:
        plt.draw()
        plt.pause(1.0)
        input("Press [enter] to continue.")
        plt.close()

    return
