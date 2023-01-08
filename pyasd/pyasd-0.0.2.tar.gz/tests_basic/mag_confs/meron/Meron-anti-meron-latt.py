#!/usr/bin/env python

#==========================================================================
# this example demonstrate how to construct a vortex/anti-vortex lattice
#
# See Hayami et al. Phys. Rev. Lett. 121, 137202 (2018)
# for a spin model to realize such spin configurations
#
# See Yu et al. Nature 564, 95 (2018)
# for a material realization
#
# Shunhong Zhang, szhang2@ustc.edu.cn
#===========================================================================


# Important steps to create this lattice

# Build a suqare lattice
# Create a core-up anti-vortex at (0.5,0), phi0=180
# Create a core-up anti-vortex at (0,0.5), phi0=0
# Create a core-up vortex at (0,0)
# Create a core-dn vortex at (0.5,0.5)

# Build a honeycomb lattice
# Create a core-up anti-vortex at (0,0), winding = 2
# Create a core-up vortex at (1/3,2/3)
# Create a core-dn vortex at (2/3,1/3), phi0=180

# we create anti-vortice first so that the vortex can overwhelm them
# See codes in spin_configurations.py for details

from asd.core.spin_configurations import *

if __name__=='__main__':
    kwargs = dict(nx=15,ny=15,
    show=True,calc_Q=True,theta_power=0.3)
    build_square_meron_latt(**kwargs)
    build_honeycomb_meron_latt(**kwargs)
