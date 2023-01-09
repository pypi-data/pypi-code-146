#!/usr/bin/env python3
# mypy: ignore-errors

"""
Reconstruct.
"""

from collections.abc import Iterable
from pathlib import Path
from typing import Any  # noqa

import numpy
from pudb import set_trace as bp  # noqa

import radiocc
from radiocc import constants, old
from radiocc.model import (
    Export,
    L2Data,
    PressTemp,
    ProcessType,
    ResultsFolders,
    Scenario,
)
from radiocc.old import (
    R4_State_Vectors_twoway_v2,
    R5_Foot_Print,
    R6_Framework_Conversion,
    R7_Offset_Correction,
    R8_Plot_Doppler_1,
    R14_Plot_check,
    R15_Errors,
    R16_Biasfit_Correction,
    R17_Run_Routines1,
    R18_Occ_Info_MEX,
    R18_Occ_Info_MVN,
)


def run(  # noqa: C901
    scenario: Scenario,
    l2_data: L2Data,
) -> Export:
    # =================================================================================
    # Interface between new & old code
    # =================================================================================
    DATA = l2_data.DATA
    ET = DATA.ET
    N_data = ET.shape[0]
    Doppler = DATA.DOPPLER

    if l2_data.FOLDER_TYPE == ProcessType.MEX:
        Diff_doppler = DATA.DIFF_DOPPLER
        distance = DATA.DISTANCE
        i_Surface = numpy.where(DATA.SURFACES_CONDITIONS)[0]
        i_integral = numpy.where(DATA.INTEGRAL_CONDITIONS)[0]
        i_Surface = N_data - 1 if not i_Surface.size else i_Surface[0]
        i_integral = i_integral[0] if isinstance(i_Surface, Iterable) else 0
        fsup = DATA.FSUP
        error = DATA.ERROR
    else:
        # fsky = DATA.FSKY
        error = numpy.zeros(N_data)
        error_ref = numpy.zeros(N_data)
        error_elec = numpy.zeros(N_data)
        error_neut = numpy.zeros(N_data)
        Diff_doppler = numpy.zeros(N_data)
        fsup = 7.2e9
        i_integral = None

    NAIF_SC = str(l2_data.SPACECRAFT_NAIF_CODE)
    NAIF_GS = str(l2_data.dsn_station_naif_code)
    NAIF_P = str(l2_data.PLANET_NAIF_CODE)

    item = scenario.LAYER.name.upper()
    Bande = scenario.BAND.name.upper()
    RESULTS = scenario.results(radiocc.cfg.results)
    DATA_PRO = str(scenario.TO_PROCESS.parent)
    DATA_ID_i_profile = str(scenario.TO_PROCESS.resolve())
    CODE_DIR = str(Path(old.__file__).parent.resolve())
    # DATA_DIR = str(scenario.TO_PROCESS.parent.parent.resolve())
    PLOT_DIR = str((RESULTS / ResultsFolders.PLOTS.name).resolve())
    EPHE_DIR = str((RESULTS / ResultsFolders.EPHEMERIDS.name).resolve())
    DATA_FINAL_DIR = str((RESULTS / ResultsFolders.DATA.name).resolve())

    c = constants.c
    R_Planet = constants.R_Planet
    e = constants.e
    eps0 = constants.eps0
    me = constants.me
    CC = constants.CC
    kB = constants.kB
    V = constants.V
    Ref_frame = constants.Ref_frame
    B_Cor_Type = constants.B_Cor_Type
    Threshold_Cor = constants.Threshold_Cor
    Threshold_int = constants.Threshold_int
    Threshold_neut_upp = constants.Threshold_neut_upp
    Threshold_Surface = constants.Threshold_Surface
    G = constants.G
    m_bar = constants.m_bar
    M_Mars = constants.M_Planet
    T_BC_low = constants.T_BC_low
    T_BC_med = constants.T_BC_med
    T_BC_upp = constants.T_BC_upp
    # =================================================================================

    export = Export()

    if l2_data.FOLDER_TYPE == ProcessType.MAVEN:
        # R18 : Occ_info :
        distance, DATA_TYPE = R18_Occ_Info_MVN.occultation_info(
            NAIF_P,
            NAIF_GS,
            ET,
            Ref_frame,
            NAIF_SC,
            DATA_PRO,
            DATA_ID_i_profile,
            Threshold_Surface,
            EPHE_DIR,
        )

        i_Surface = numpy.where(numpy.array(distance) <= Threshold_Surface)[0]
        if i_Surface.size == 0:
            i_Surface = N_data - 1
        else:
            i_Surface = i_Surface[0]
        i_integral = numpy.where(numpy.array(distance) <= Threshold_int)[0]
        if i_integral.size == 0:
            i_integral = 0
        else:
            i_integral = i_integral[0]
    else:
        DATA_TYPE = None
        R18_Occ_Info_MEX.occultation_info(
            NAIF_P,
            NAIF_GS,
            ET,
            Ref_frame,
            NAIF_SC,
            DATA_PRO,
            DATA_ID_i_profile,
            Threshold_Surface,
            EPHE_DIR,
            distance,
        )
    if radiocc.cfg.quick_trace:
        return export

    # If egress, we reverse the matrices to have them from atmosphere to surface.
    if DATA_TYPE is not None and DATA_TYPE == radiocc.model.RadioDataType.EGRESS:
        distance = numpy.flip(distance)
        Doppler = numpy.flip(Doppler)
        ET = numpy.flip(ET)

    # R5: State_Vectors_twoway
    (
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
    ) = R4_State_Vectors_twoway_v2.ephemerides(
        N_data, ET, NAIF_SC, NAIF_GS, NAIF_P, DATA_PRO, Ref_frame, l2_data.FOLDER_TYPE
    )

    # R6: footprint
    (
        d_radius,
        d_lat,
        d_lon,
        dist_Mars_Sun,
        spclon_SC,
        spclat_SC,
        re,
        f,
    ) = R5_Foot_Print.long_lat(
        N_data, pos_MEX, vel_MEX, ET, ET_MEX_Mars, Ref_frame, l2_data.FOLDER_TYPE
    )

    # R7 coordinate frames
    (
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
    ) = R6_Framework_Conversion.Occ_Plane_Conversion(
        N_data, pos_MEX_up, vel_MEX_up, pos_GS_up, vel_GS_up
    )

    # R7 coordinate frames
    (
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
    ) = R6_Framework_Conversion.Occ_Plane_Conversion(
        N_data, pos_MEX_dn, vel_MEX_dn, pos_GS_dn, vel_GS_dn
    )

    if radiocc.cfg.skip_correction_guess:
        Doppler_debias = numpy.full_like(ET, numpy.nan)
        Doppler_biasfit = numpy.full_like(ET, numpy.nan)
        p0 = numpy.nan
        p1 = numpy.nan
        if B_Cor_Type:
            p2 = numpy.nan
        if radiocc.gui is not None:
            radiocc.gui.button_next.set_sensitive(False)

    else:
        if B_Cor_Type == "Linear":
            (
                ET,
                delET,
                Doppler_debias,
                Doppler_biasfit,
                Corr_ind,
                p0,
                p1,
            ) = R7_Offset_Correction.Off_Cor(
                B_Cor_Type,
                Threshold_Cor,
                Doppler,
                Diff_doppler,
                ET,
                N_data,
                distance,
                CODE_DIR,
                i_integral,
                # Threshold_Surface,
                # Threshold_int,
                # l2_data.FOLDER_TYPE,
            )
        if B_Cor_Type == "Quadratic":
            (
                i_Surface,
                ET,
                delET,
                Doppler_debias,
                Doppler_biasfit,
                Corr_ind,
                p0,
                p1,
                p2,
            ) = R7_Offset_Correction.Off_Cor(
                i_integral,
                i_Surface,
                ET,
                delET,
                B_Cor_Type,
                Threshold_Cor,
                Doppler,
                Diff_doppler,
                ET,
                N_data,
                distance,
                CODE_DIR,
                i_integral,
                # Threshold_Surface,
                # Threshold_int,
                # l2_data.FOLDER_TYPE,
            )

    # R5: Plot doppler after bias correction
    R8_Plot_Doppler_1.PLOT_Dop1(
        distance,
        Doppler,
        Doppler_debias,
        Doppler_biasfit,
        ET,
        PLOT_DIR,
        N_data,
        DATA_TYPE,
    )
    if radiocc.gui is not None:
        radiocc.gui.switch_order.set_sensitive(True)
        radiocc.gui.box_refractivity.hide()
        radiocc.gui.box_altitude.show()
        # Click on the button Next to exit this loop.
        radiocc.gui.go_next = False
        stay_while = not radiocc.gui.go_next
    else:
        if radiocc.cfg.skip_correction_guess:
            stay_while = True
        else:
            HAPPY_or_NOT = str(
                input("Enter 'YES' if the debias is good and 'NO' if bad: ")
            )
            stay_while = HAPPY_or_NOT == "NO"
    while stay_while:
        # Updating the regression order or altitude value triggers an update
        if radiocc.gui is not None:
            # Wait for the user to click on the button Compute to continue the loop.
            radiocc.gui.label_data.set_label(
                f"{scenario.TO_PROCESS.name} Band:{Bande} Layer:{item}"
                " is now interactive"
            )
            radiocc.gui.interactive()
            radiocc.gui.label_data.set_label(
                f"PROCESSING {scenario.TO_PROCESS.name} Band:{Bande} Layer:{item}..."
            )
            radiocc.gui.draw()
            NEW_B_Cor_Type = radiocc.gui.label_switch.get_label()
            NEW_Threshold_Cor = radiocc.gui.get_altitude()
        else:
            NEW_B_Cor_Type = str(input("Enter new type, Linear or Quadratic: "))
            NEW_Threshold_Cor = float(input("Enter new threshold altitude = "))
        if NEW_Threshold_Cor != Threshold_Cor or NEW_B_Cor_Type != B_Cor_Type:
            if radiocc.cfg.skip_correction_guess and radiocc.gui is not None:
                radiocc.gui.button_next.set_sensitive(True)
            if NEW_B_Cor_Type == "Linear":
                (
                    ET,
                    delET,
                    Doppler_debias,
                    Doppler_biasfit,
                    Corr_ind,
                    p0,
                    p1,
                ) = R7_Offset_Correction.Off_Cor(
                    NEW_B_Cor_Type,
                    NEW_Threshold_Cor,
                    Doppler,
                    Diff_doppler,
                    ET,
                    N_data,
                    distance,
                    CODE_DIR,
                    i_integral,
                    # Threshold_Surface,
                    # Threshold_int,
                    # l2_data.FOLDER_TYPE,
                )
            if NEW_B_Cor_Type == "Quadratic":
                (
                    ET,
                    delET,
                    Doppler_debias,
                    Doppler_biasfit,
                    Corr_ind,
                    p0,
                    p1,
                    p2,
                ) = R7_Offset_Correction.Off_Cor(
                    NEW_B_Cor_Type,
                    NEW_Threshold_Cor,
                    Doppler,
                    Diff_doppler,
                    ET,
                    N_data,
                    distance,
                    CODE_DIR,
                    i_integral,
                    # Threshold_Surface,
                    # Threshold_int,
                    # l2_data.FOLDER_TYPE,
                )

            R8_Plot_Doppler_1.PLOT_Dop1(
                distance,
                Doppler,
                Doppler_debias,
                Doppler_biasfit,
                ET,
                PLOT_DIR,
                N_data,
                DATA_TYPE,
            )
        B_Cor_Type = NEW_B_Cor_Type
        Threshold_Cor = NEW_Threshold_Cor

        if radiocc.gui is None:
            HAPPY_or_NOT = str(
                input("Enter 'YES' if the debias is good and 'NO' if bad: ")
            )
            stay_while = HAPPY_or_NOT == "NO"
        else:
            stay_while = not radiocc.gui.go_next

    if radiocc.cfg.skip_correction_guess:
        refractivity = numpy.full_like(distance, numpy.nan)
        if item == "IONO":
            Ne = numpy.full_like(distance, numpy.nan)
            R14_Plot_check.PLOT1(
                distance, Doppler, Doppler_debias, refractivity, Ne, PLOT_DIR, item
            )
        if item == "ATMO":
            Nn = numpy.full_like(distance, numpy.nan)
            R14_Plot_check.PLOT2(
                distance, Doppler, Doppler_debias, refractivity, Nn, PLOT_DIR, item
            )
        if radiocc.gui is not None:
            radiocc.gui.button_next.set_sensitive(False)
    else:
        if item == "IONO":
            refractivity, Ne, TEC, bend_radius = R17_Run_Routines1.run(
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
                DATA_TYPE,
            )
        if item == "ATMO":
            (
                refractivity,
                Nn,
                i_neut_upp,
                P_low,
                P_med,
                P_upp,
                T_low,
                T_med,
                T_upp,
                bend_radius,
            ) = R17_Run_Routines1.run(
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
                DATA_TYPE,
            )

    if radiocc.gui is not None:
        # Change interface in control panel
        radiocc.gui.switch_order.set_sensitive(False)
        radiocc.gui.box_altitude.hide()
        radiocc.gui.box_refractivity.show()
        radiocc.gui.set_intercept(p0)
        radiocc.gui.set_slope(p1)
        if radiocc.gui.label_switch.get_label() == "Linear":
            radiocc.gui.label_current_quadratic.hide()
            radiocc.gui.entry_quadratic.hide()
        else:
            radiocc.gui.set_quadratic(p2)
        # Click on the button Next to exit this loop.
        radiocc.gui.go_next = False
        stay_while = not radiocc.gui.go_next
    else:
        if radiocc.cfg.skip_correction_guess:
            stay_while = True
        else:
            RefCorr_GD_or_NOT = str(
                input(
                    "Enter 'YES' if the refractivity correction is good "
                    "and 'NO' if bad: "
                )
            )
            stay_while = RefCorr_GD_or_NOT == "NO"
    while stay_while:
        if radiocc.gui is not None:
            # Wait for the user to click on the button Compute to continue the loop.
            radiocc.gui.label_data.set_label(
                f"{scenario.TO_PROCESS.name} Band:{Bande} Layer:{item}"
                " is now interactive"
            )
            radiocc.gui.interactive()
            radiocc.gui.label_data.set_label(
                f"PROCESSING {scenario.TO_PROCESS.name} Band:{Bande} Layer:{item}..."
            )
            radiocc.gui.draw()
            NEW_p0 = radiocc.gui.get_intercept()
            NEW_p1 = radiocc.gui.get_slope()
            if B_Cor_Type == "Quadratic":
                NEW_p2 = radiocc.gui.get_quadratic()
        else:
            if B_Cor_Type == "Linear":
                print("\t p0 = ", p0)
                print("\t p1 = ", p1)

            if B_Cor_Type == "Quadratic":
                print("\t p0 = ", p0)
                print("\t p1 = ", p1)
                print("\t p2 = ", p2)

        (
            Doppler_debias2,
            Doppler_biasfit2,
            NEW_p0,
            NEW_p1,
            NEW_p2,
        ) = R16_Biasfit_Correction.Off_Cor2(
            B_Cor_Type, Doppler, Diff_doppler, ET, delET, N_data, distance
        )

        if NEW_p0 != p0 or NEW_p1 != p1 or (B_Cor_Type == "Quadratic" and NEW_p2 != p2):
            if radiocc.cfg.skip_correction_guess and radiocc.gui is not None:
                radiocc.gui.button_next.set_sensitive(True)
            if item == "IONO":
                refractivity, Ne, TEC, bend_radius = R17_Run_Routines1.run(
                    Doppler,
                    Doppler_debias2,
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
                    DATA_TYPE,
                )
            if item == "ATMO":
                (
                    refractivity,
                    Nn,
                    i_neut_upp,
                    P_low,
                    P_med,
                    P_upp,
                    T_low,
                    T_med,
                    T_upp,
                    bend_radius,
                ) = R17_Run_Routines1.run(
                    Doppler,
                    Doppler_debias2,
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
                    DATA_TYPE,
                )

            Doppler_debias = Doppler_debias2
            Doppler_biasfit = Doppler_biasfit2

        if radiocc.gui is None:
            RefCorr_GD_or_NOT = str(
                input(
                    "Enter 'YES' if the refractivity correction "
                    "is good and 'NO' if bad: "
                )
            )

            stay_while = RefCorr_GD_or_NOT == "NO"
        else:
            stay_while = not radiocc.gui.go_next
    error_ref, error_elec, error_neut = R15_Errors.ERRORS(
        N_data, fsup, error, c, distance, Threshold_neut_upp, V, e, eps0, me, Bande, CC
    )

    ALTITUDE = bend_radius - d_radius * 1e3

    # Return variables to be exported.

    export.DATA_PATH = Path(DATA_FINAL_DIR)
    export.PLOT_PATH = Path(PLOT_DIR)
    export.EPHE_PATH = Path(EPHE_DIR)
    export.ET = ET
    export.DOPPLER = Doppler
    export.DOPPLER_DEBIAS = Doppler_debias
    export.DOPPLER_BIAS_FIT = Doppler_biasfit
    export.DISTANCE = distance
    export.ALTITUDE = ALTITUDE
    export.REFRACTIVITY = refractivity
    export.ERROR = error
    export.ERROR_REFRAC = error_ref
    export.BEND_RADIUS = bend_radius

    if item == "IONO":
        export.NE = Ne
        export.ERROR_ELEC = error_elec
        export.TEC = TEC
    else:
        export.NE = Nn
        export.ERROR_ELEC = error_neut
        PT = PressTemp()
        PT.P_low = P_low
        PT.P_med = P_med
        PT.P_upp = P_upp
        PT.T_low = T_low
        PT.T_med = T_med
        PT.T_upp = T_upp
        export.PT = PT

    return export
