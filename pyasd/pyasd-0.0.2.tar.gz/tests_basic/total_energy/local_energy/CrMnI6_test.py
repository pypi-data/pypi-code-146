#!/usr/bin/env python3

import os
import numpy as np
from asd.core.hamiltonian import *
from asd.data_base.exchange_for_CrMnI6_rect import *
from asd.core.spin_configurations import init_random


sp_lat = np.zeros((3,3,4,3))
sp_lat = init_random(sp_lat,verbosity=0)

site_idx = np.array([1,2,3])

e1 = ham0_rc_3NN.calc_local_energy(sp_lat,site_idx)
e2 = ham4_rc.calc_local_energy(sp_lat,site_idx)

print (e1,e2)

