#!/usr/bin/env python3

"""
Physical constants.
"""

c = 299792458.0  # m s^-1
kB = 1.38064852e-23  # m^2 kg s^-2 K^-1
G = 6.673e-11  # m^3 kg^-1 s^-2
e = 1.6e-19  # A s
eps0 = 8.854e-12
me = 9.109e-31  # kg
C1 = 1.3077e-6  # m kg^-1 s^2 K  "Hinson et al. (1999)"
CC = C1 * kB  # m^3            "K. L. Cahoy(2005)" Refractive Volume
m_bar = 7.221e-26  # kg                "S.Tellmann (2013)"
V = 3.4e3  # m.s^-1
# radius thresholds
Threshold_Cor = 3.95e6  # 4.0e6  # 4.2E6 #4128432         # Wang et al. (2018) ??
B_Cor_Type = "Linear"  # 'Linear' #'Quadratic'        # 'Linear' or 'Quadratic'
Threshold_neut_upp = 3466000  # M.Patzold et al.(2014) + Peter et al.(2014) ==> 80 km
Threshold_Surface = 3386000  # K. L. Cahoy (2005)
Threshold_int = Threshold_Surface + 1e6
# for refracitivity correction
# neutral_upp = 3.45E6
# iono_low = 3.46E6
# temperature boundary condition
T_BC_low = 130  # Ref: Patzol data processing files
T_BC_med = 165  # Ref : Patzol data processing files
T_BC_upp = 200  # Ref : Patzol data processing files

SC = "MEX"  # '-41'
Planet = "MARS"  # '499'

R_Planet = 3.3866e6
M_Planet = 6.4185e23
Ref_frame = "J2000"

Ref_frame_FP = "marsiau"
# Ref_frame = 'IAU_MARS'
