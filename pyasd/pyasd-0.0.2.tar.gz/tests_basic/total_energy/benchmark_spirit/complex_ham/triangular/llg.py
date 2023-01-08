#!/usr/bin/env python

#===============================================
#
# Simulate the AFM spin lattice
# Shunhong Zhang <szhang2@ustc.edu.cn>
# Dec 27 2021
#
#================================================

from spirit import io,log,state,geometry,system,hamiltonian,simulation,parameters,configuration
import os

# in the convention of Spirit code
# negative for AFM, positive for FM
J1 = 1

# The DM intereaction strength
# if you use set_dmi, the DM vector
# always points along the bond, which
# favors Bloch-type skyrmions or other 
# chiral magnetic structures
DMI = 0.4

# for Single-ion anisotropy (SIA)
# negative (positive) favors in-plane (out-of-plane)
SIA = 0.2

temp=0.1
tag = 'T_{:.2f}'.format(temp)
nx=20
ny=20
n_iterations=50000
n_log_iterations = 1000

if __name__=='__main__':
    os.system('rm T* Log*')
    with state.State('input.cfg') as p_state:
        geometry.set_n_cells(p_state,[nx,ny,1])
        hamiltonian.set_boundary_conditions(p_state,[1,1,0])
        hamiltonian.set_exchange(p_state, 1, [J1])
        hamiltonian.set_dmi(p_state, 1, [DMI])

        configuration.random(p_state)
        parameters.llg.set_output_tag(p_state, tag)
        parameters.llg.set_output_folder(p_state, '.')
        parameters.llg.set_iterations(p_state, n_iterations, n_log_iterations)
        parameters.llg.set_output_configuration(p_state, 0, 1, 3)
        parameters.llg.set_output_energy(p_state, 0, 1)
        parameters.llg.set_output_general(p_state, 1, 0, 0)
        #parameters.llg.set_temperature(p_state, temp)
        parameters.llg.set_damping(p_state, 0.1)
        parameters.llg.set_timestep(p_state, 0.001)
        system.update_data(p_state)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_DEPONDT)
