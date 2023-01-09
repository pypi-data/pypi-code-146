#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 12:14:39 2020

@author: ananya
"""
from typing import Optional
from pudb import set_trace as bp  # noqa: F401

import radiocc

from radiocc.old import (
    R9_BendAng_ImpParam_dn,
    R9_BendAng_ImpParam_up,
    R10_Avg_BendAng_ImpParam,
    R11_Refractivity_and_Bending_Radius_v2,
    R12_Electron_Density,
    R13_Neutral_Number_Density,
    R13a_Pressure_and_Temperature,
    R14_Plot_check,
)


def run(
    Doppler,
    Doppler_debias,
    distance,
    Diff_doppler,
    item,
    i_integral,
    i_Surface,
    R_Planet,
    e,
    eps0,
    me,
    PLOT_DIR,
    Threshold_neut_upp,
    CC,
    kB,
    N_data,
    r_MEX_up,
    z_MEX_up,
    z_GS_up,
    vr_MEX_up,
    vz_MEX_up,
    vr_GS_up,
    vz_GS_up,
    gamma_up,
    beta_e_up,
    delta_s_up,
    r_MEX_dn,
    z_MEX_dn,
    z_GS_dn,
    vr_MEX_dn,
    vz_MEX_dn,
    vr_GS_dn,
    vz_GS_dn,
    gamma_dn,
    beta_e_dn,
    delta_s_dn,
    Bande,
    fsup,
    c,
    G,
    m_bar,
    M_Mars,
    T_BC_low,
    T_BC_med,
    T_BC_upp,
    DATA_TYPE: Optional[radiocc.model.RadioDataType]
):
    kx = 880.0 / 749.0
    ks = 240.0 / 749.0
    Doppler_debias_dn_iono_x = Doppler_debias / (1.0 + (kx * kx))
    Doppler_debias_up_iono_x = Doppler_debias / (kx + (1.0 / kx))

    Doppler_debias_dn_iono_s = Doppler_debias / (1.0 + (ks ** 2))
    Doppler_debias_up_iono_s = Doppler_debias_up_iono_x

    Doppler_debias_dn_atmo_x = Doppler_debias / 2.0
    Doppler_debias_up_atmo_x = Doppler_debias / (2.0 * kx)

    Doppler_debias_dn_atmo_s = Doppler_debias / 2.0
    Doppler_debias_up_atmo_s = Doppler_debias_up_atmo_x

    Diff_Doppler_debias_dn_iono_s = Diff_doppler / (1.0 - (9.0 / 121.0))

    if Bande == "X":

        if item == "IONO":

            # R8: bending angle & impact parameter up
            (
                imp_param_up,
                bend_ang_up,
                delta_r_up,
                beta_r_up,
            ) = R9_BendAng_ImpParam_up.Bend_up(
                N_data,
                r_MEX_up,
                z_MEX_up,
                z_GS_up,
                vr_MEX_up,
                vz_MEX_up,
                vr_GS_up,
                vz_GS_up,
                gamma_up,
                beta_e_up,
                delta_s_up,
                Doppler_debias_up_iono_x,
                fsup,
                c,
                DATA_TYPE,
            )

            # R8: bending angle & impact parameter down
            (
                imp_param_dn,
                bend_ang_dn,
                delta_r_dn,
                beta_r_dn,
            ) = R9_BendAng_ImpParam_dn.Bend_dn(
                N_data,
                r_MEX_dn,
                z_MEX_dn,
                z_GS_dn,
                vr_MEX_dn,
                vz_MEX_dn,
                vr_GS_dn,
                vz_GS_dn,
                gamma_dn,
                beta_e_dn,
                delta_s_dn,
                Doppler_debias_dn_iono_x,
                Bande,
                fsup,
                c,
                DATA_TYPE,
            )

            # R9: Average bending angle & impact parameter
            imp_param, bend_ang = R10_Avg_BendAng_ImpParam.Avg(
                imp_param_up, bend_ang_up, imp_param_dn, bend_ang_dn, Bande
            )

        if item == "ATMO":
            # R8: bending angle & impact parameter up
            (
                imp_param_up,
                bend_ang_up,
                delta_r_up,
                beta_r_up,
            ) = R9_BendAng_ImpParam_up.Bend_up(
                N_data,
                r_MEX_up,
                z_MEX_up,
                z_GS_up,
                vr_MEX_up,
                vz_MEX_up,
                vr_GS_up,
                vz_GS_up,
                gamma_up,
                beta_e_up,
                delta_s_up,
                Doppler_debias_up_atmo_x,
                fsup,
                c,
                DATA_TYPE,
            )

            # R8: bending angle & impact parameter down
            (
                imp_param_dn,
                bend_ang_dn,
                delta_r_dn,
                beta_r_dn,
            ) = R9_BendAng_ImpParam_dn.Bend_dn(
                N_data,
                r_MEX_dn,
                z_MEX_dn,
                z_GS_dn,
                vr_MEX_dn,
                vz_MEX_dn,
                vr_GS_dn,
                vz_GS_dn,
                gamma_dn,
                beta_e_dn,
                delta_s_dn,
                Doppler_debias_dn_atmo_x,
                Bande,
                fsup,
                c,
                DATA_TYPE,
            )

            # R9: Average bending angle & impact parameter
            imp_param, bend_ang = R10_Avg_BendAng_ImpParam.Avg(
                imp_param_up, bend_ang_up, imp_param_dn, bend_ang_dn, Bande
            )

    if Bande == "S":
        if item == "IONO":
            # R8: bending angle & impact parameter up
            (
                imp_param_up,
                bend_ang_up,
                delta_r_up,
                beta_r_up,
            ) = R9_BendAng_ImpParam_up.Bend_up(
                N_data,
                r_MEX_up,
                z_MEX_up,
                z_GS_up,
                vr_MEX_up,
                vz_MEX_up,
                vr_GS_up,
                vz_GS_up,
                gamma_up,
                beta_e_up,
                delta_s_up,
                Doppler_debias_up_iono_s,
                fsup,
                c,
                DATA_TYPE,
            )

            # R8: bending angle & impact parameter down
            (
                imp_param_dn,
                bend_ang_dn,
                delta_r_dn,
                beta_r_dn,
            ) = R9_BendAng_ImpParam_dn.Bend_dn(
                N_data,
                r_MEX_dn,
                z_MEX_dn,
                z_GS_dn,
                vr_MEX_dn,
                vz_MEX_dn,
                vr_GS_dn,
                vz_GS_dn,
                gamma_dn,
                beta_e_dn,
                delta_s_dn,
                Doppler_debias_dn_iono_s,
                Bande,
                fsup,
                c,
                DATA_TYPE,
            )

            # R9: Average bending angle & impact parameter
            imp_param, bend_ang = R10_Avg_BendAng_ImpParam.Avg(
                imp_param_up, bend_ang_up, imp_param_dn, bend_ang_dn, Bande
            )

        if item == "ATMO":
            # R8: bending angle & impact parameter up
            (
                imp_param_up,
                bend_ang_up,
                delta_r_up,
                beta_r_up,
            ) = R9_BendAng_ImpParam_up.Bend_up(
                N_data,
                r_MEX_up,
                z_MEX_up,
                z_GS_up,
                vr_MEX_up,
                vz_MEX_up,
                vr_GS_up,
                vz_GS_up,
                gamma_up,
                beta_e_up,
                delta_s_up,
                Doppler_debias_up_atmo_s,
                fsup,
                c,
                DATA_TYPE,
            )

            # R8: bending angle & impact parameter down
            (
                imp_param_dn,
                bend_ang_dn,
                delta_r_dn,
                beta_r_dn,
            ) = R9_BendAng_ImpParam_dn.Bend_dn(
                N_data,
                r_MEX_dn,
                z_MEX_dn,
                z_GS_dn,
                vr_MEX_dn,
                vz_MEX_dn,
                vr_GS_dn,
                vz_GS_dn,
                gamma_dn,
                beta_e_dn,
                delta_s_dn,
                Doppler_debias_dn_atmo_s,
                Bande,
                fsup,
                c,
                DATA_TYPE,
            )

            # R9: Average bending angle & impact parameter
            imp_param, bend_ang = R10_Avg_BendAng_ImpParam.Avg(
                imp_param_up, bend_ang_up, imp_param_dn, bend_ang_dn, Bande
            )

    if Bande == "Diff":

        if item == "IONO":

            # R8: bending angle & impact parameter down
            (
                imp_param,
                bend_ang,
                delta_r_diff,
                beta_r_diff,
            ) = R9_BendAng_ImpParam_dn.Bend_dn(
                N_data,
                r_MEX_dn,
                z_MEX_dn,
                z_GS_dn,
                vr_MEX_dn,
                vz_MEX_dn,
                vr_GS_dn,
                vz_GS_dn,
                gamma_dn,
                beta_e_dn,
                delta_s_dn,
                Diff_Doppler_debias_dn_iono_s,
                Bande,
                fsup,
                c,
                DATA_TYPE,
            )

        if item == "ATMO":

            # R8: bending angle & impact parameter down
            imp_param, bend_ang, delta_r_dn, beta_r_dn = R9_BendAng_ImpParam_dn.Bend_dn(
                N_data,
                r_MEX_dn,
                z_MEX_dn,
                z_GS_dn,
                vr_MEX_dn,
                vz_MEX_dn,
                vr_GS_dn,
                vz_GS_dn,
                gamma_dn,
                beta_e_dn,
                delta_s_dn,
                Doppler_debias_dn_atmo_s,
                Bande,
                fsup,
                c,
                DATA_TYPE,
            )  # NEED TO CHECK????

    # R11
    (
        ref_index,
        refractivity,
        bend_radius,
        Sum_tot,
    ) = R11_Refractivity_and_Bending_Radius_v2.Abel_Analytical(
        N_data, i_integral, i_Surface, imp_param, bend_ang, R_Planet
    )

    if item == "IONO":

        Ne = R12_Electron_Density.Elec(
            N_data, refractivity, e, eps0, me, Bande, fsup, c
        )
        TEC = R12_Electron_Density.TEC_Calc(
            N_data, Ne, i_integral, i_Surface, bend_radius, R_Planet
        )

        R14_Plot_check.PLOT1(
            distance, Doppler, Doppler_debias, refractivity, Ne, PLOT_DIR, item
        )
    if item == "ATMO":

        # R13: neutral density (Level 04)
        Nn, i_neut_upp = R13_Neutral_Number_Density.Neut(
            N_data, bend_radius, refractivity, Threshold_neut_upp, i_Surface, CC, kB
        )
        # R13a: pressure & temperature (Level 04)
        P_low, T_low = R13a_Pressure_and_Temperature.Temp_Pre(
            N_data,
            T_BC_low,
            Nn,
            bend_radius,
            i_neut_upp,
            i_Surface,
            kB,
            G,
            m_bar,
            M_Mars,
            refractivity,
        )
        P_med, T_med = R13a_Pressure_and_Temperature.Temp_Pre(
            N_data,
            T_BC_med,
            Nn,
            bend_radius,
            i_neut_upp,
            i_Surface,
            kB,
            G,
            m_bar,
            M_Mars,
            refractivity,
        )
        P_upp, T_upp = R13a_Pressure_and_Temperature.Temp_Pre(
            N_data,
            T_BC_upp,
            Nn,
            bend_radius,
            i_neut_upp,
            i_Surface,
            kB,
            G,
            m_bar,
            M_Mars,
            refractivity,
        )

        R14_Plot_check.PLOT2(
            distance, Doppler, Doppler_debias, refractivity, Nn, PLOT_DIR, item
        )

    if item == "IONO":
        return refractivity, Ne, TEC, bend_radius
    if item == "ATMO":
        return refractivity, Nn, i_neut_upp, P_low, P_med, P_upp, T_low, T_med, T_upp, bend_radius
