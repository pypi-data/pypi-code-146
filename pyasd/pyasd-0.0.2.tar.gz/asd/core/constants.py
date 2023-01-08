#!/usr/bin/env python

# physical constants for spin dynamics simulations
# Shunhong Zhang
# May 19, 2021
# Data from wikipedia

import numpy as np

mu_0 = 2.0133545e2      # vacuum permeability, in T^2*Angstrom^3/meV
e_chg = 1.6021766e-19   # elementary charge in Coulomb
kB = 8.617333262145e-2  # Boltzmann constant, in meV/K
gamma_e = 0.1760859644  # electron gyromagnetic ratio, in rad/T/ps
muB = 0.057883817555    # Bohr Magnetom, in utit of meV/T
PlanckConstant = 4.13566733e-15  # [eV s]
Hbar = PlanckConstant/(2*np.pi)  # [eV s]
