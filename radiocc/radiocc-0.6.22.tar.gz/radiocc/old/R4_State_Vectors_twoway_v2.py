#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:26:40 2019

@author: ananya
"""

import os

import numpy as np
import spiceypy as spy
from pudb import set_trace as bp  # noqa

from radiocc.model import ProcessType


def ephemerides(
    N_data, ET, SC, GS, Mars, DATA_DIR, Ref_frame, FOLDER_TYPE: ProcessType
):
    # os.chdir(DATA_DIR)
    # tB          = np.zeros((N_data,))
    tMEX = np.zeros((N_data,))
    tA = np.zeros((N_data,))
    t0_up = np.zeros((N_data,))
    t0_dn = np.zeros((N_data,))
    t0_upp = np.zeros((N_data,))

    #
    #
    #
    #
    #
    #
    #
    #
    #    GS(to_up) ---> t_Mex ----> G(to_dn)

    ET_MEX_Mars = np.zeros((N_data,))

    pos_GS_dn = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    vel_GS_dn = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    pos_MEX_dn = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    vel_MEX_dn = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    pos_GS_up = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    vel_GS_up = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    pos_MEX_up = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    vel_MEX_up = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    pos_GS_upp = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    vel_GS_upp = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    pos_MEX_upp = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)
    vel_MEX_upp = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    pos_MEX = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], float)
    vel_MEX = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], float)

    # This routine computes the transmit (or receive) time  of a signal at a specified target, given the receive  (or transmit) time at a specified observer. The elapsed   time between transmit and receive is also returned.
    #  Direction the signal travels ( "->" or "<-" )
    # etobs      I   Epoch of a signal at some observer
    # obs        I   NAIF ID of some observer
    # dir        I   Direction the signal travels ( "->" or "<-" )
    # targ       I   NAIF ID of the target object
    # ettarg     O   Epoch of the signal at the target
    # elapsd     O   Time between transmit and receipt of the signal

    # void ltime_c ( etobs, obs, ConstSpiceChar   * dir, SpiceInt           targ,
    #               output    * ettarg,
    #               output     * elapsd  )

    # spkezr Return the state (position and velocity) of a target body  relative to an observing body, optionally corrected for light   time (planetary aberration) and stellar aberration.
    # void spkezr_c (targ, et,  ref, abcorr, obs) output  starg[6],*lt        )

    # SUBROUTINE LTIME ( Epoch of a signal at some observer, NAIF-id of some observer, direction the signal travel, AIF-id of the target object,  Time between transmit and receipt of the signal )

    for i in range(N_data):
        # Downlink
        # tB = ET[i]
        [ET_MEX_GS, t_0] = spy.ltime(
            ET[i], int(GS), "<-", int(SC)
        )  #  Epoch of the signal at  MEX tdown
        tMEX[
            i
        ] = ET_MEX_GS  # time at which MEX send signal to mars via downlink = time at which MEX received signal from Mars via uplink

        #  [ET_Mars_GS, t_0] = spy.ltime(tMEX[i], int(Mars), '<-', int(SC)) #  Epoch of the signal at  Mars t down

        [ET_Mars_GS, t_0] = spy.ltime(
            tMEX[i], int(SC), "->", int(Mars)
        )  #  Epoch of the signal at  Mars t down
        t0_dn[i] = ET_Mars_GS  # The signal was transmitted at: t0_dn from Mars

        # [ET_Mars_GS, t_0] = spy.ltime(tMEX[i], int(Mars), '->', int(SC)) #  Epoch of the signal at  MARS tup
        [ET_Mars_GS, t_0] = spy.ltime(
            tMEX[i], int(SC), "<-", int(Mars)
        )  #  Epoch of the signal at  Mars tup
        t0_up[i] = ET_Mars_GS  # time at which Mars send signal to MEX uplink

        # [ states1, lt1 ] = spy.spkezr( 'DSS-65', t0_dn[i] , 'marsiau', "NONE", 'mars' )
        [states1, lt1] = spy.spkezr(
            GS, t0_dn[i], Ref_frame, "NONE", "mars"
        )  #  position of GS at  T_Mars wrt Mars
        pos_GS_dn[i] = states1[:3] * 1e3
        vel_GS_dn[i] = states1[3:] * 1e3

        [states2, lt2] = spy.spkezr(
            FOLDER_TYPE.name, t0_dn[i], Ref_frame, "NONE", "mars"
        )  #  position of MEX at  T_Mars wrt Mars
        pos_MEX_dn[i] = states2[:3] * 1e3
        vel_MEX_dn[i] = states2[3:] * 1e3

        # uplink

        [states3, lt3] = spy.spkezr(
            GS, t0_up[i], Ref_frame, "NONE", "mars"
        )  # position of  GS tup
        pos_GS_up[i] = states3[:3] * 1e3
        vel_GS_up[i] = states3[3:] * 1e3

        [states4, lt2] = spy.spkezr(
            FOLDER_TYPE.name, t0_up[i], Ref_frame, "NONE", "mars"
        )  # position of  MEX tup
        pos_MEX_up[i] = states4[:3] * 1e3
        vel_MEX_up[i] = states4[3:] * 1e3

        [ET_GS_SC, t_0] = spy.ltime(tMEX[i], int(SC), "<-", int(GS))
        tA[i] = ET_GS_SC

        # Used for routine R6, not in R9 !

        [ET_MEX_Marss, one_way_t_span] = spy.ltime(tMEX[i], int(Mars), "<-", int(SC))
        ET_MEX_Mars[i] = ET_MEX_Marss

        [states5, lt] = spy.spkezr(
            FOLDER_TYPE.name, ET_MEX_Mars[i], Ref_frame, "NONE", "mars"
        )
        pos_MEX[i] = states5[:3] * 1e3
        vel_MEX[i] = states5[3:] * 1e3

        [ET_GS_Mars, t_0] = spy.ltime(tA[i], int(Mars), "<-", int(GS))
        t0_upp[i] = ET_GS_Mars

        [states6, lt6] = spy.spkezr(GS, t0_upp[i], Ref_frame, "NONE", "mars")
        pos_GS_upp[i] = states6[:3] * 1e3
        vel_GS_upp[i] = states6[3:] * 1e3

        [states7, lt7] = spy.spkezr(
            FOLDER_TYPE.name, t0_upp[i], Ref_frame, "NONE", "mars"
        )
        pos_MEX_upp[i] = states7[:3] * 1e3
        vel_MEX_upp[i] = states7[3:] * 1e3

    # print('\tR5: Done')
    # print('')
    # print('')
    # print('')
    # print('')

    return (
        t0_up,
        pos_GS_up,
        vel_GS_up,
        pos_MEX_up,
        vel_MEX_up,
        tMEX,
        t0_dn,
        pos_GS_dn,
        vel_GS_dn,
        pos_MEX_dn,
        vel_MEX_dn,
        t0_upp,
        pos_GS_upp,
        vel_GS_upp,
        pos_MEX_upp,
        vel_MEX_upp,
        pos_MEX,
        vel_MEX,
        ET_MEX_Mars,
    )
