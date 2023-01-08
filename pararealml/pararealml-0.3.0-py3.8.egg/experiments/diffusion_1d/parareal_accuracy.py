from mpi4py import MPI

from pararealml.utils.tf import use_cpu
from pararealml.utils.time import time

use_cpu()

from pararealml.operators.parareal import *

from experiments.diffusion.ivp import *
from experiments.diffusion.operators import *


comm = MPI.COMM_WORLD
rank = comm.rank

coarse_ar.model.model.load_weights('weights/ar_0')
# coarse_pidon.model.load_weights('weights/pidon_0')

fine_fdm_sol = time()(fine_fdm.solve)(ivp)[0]
coarse_fdm_sol = time()(coarse_fdm.solve)(ivp)[0]
coarse_ar_sol = time()(coarse_ar.solve)(ivp)[0]
# coarse_pidon_sol = coarse_pidon.solve(ivp)

for n_parareal_iterations in range(1, comm.size + 1):
    parareal_fdm = \
        PararealOperator(fine_fdm, coarse_fdm, 0., n_parareal_iterations)
    parareal_ar = \
        PararealOperator(fine_fdm, coarse_ar, 0., n_parareal_iterations)
    # parareal_pidon = \
    #     PararealOperator(fine_fdm, coarse_pidon, 0., n_parareal_iterations)

    parareal_fdm_sol = parareal_fdm.solve(ivp)
    parareal_ar_sol = parareal_ar.solve(ivp)
    # parareal_pidon_sol = parareal_pidon.solve(ivp)

    if rank == 0:
        diff = fine_fdm_sol.diff([
            coarse_fdm_sol,
            coarse_ar_sol,
            # coarse_pidon_sol,
            parareal_fdm_sol,
            parareal_ar_sol,
            # parareal_pidon_sol
        ])
        rss_diffs = np.sqrt(
            np.square(np.stack(diff.differences)).sum(axis=(2, 3))
        )
        print(
            f'Parareal iterations {n_parareal_iterations} - rank {rank} - '
            'RSS differences:', repr(rss_diffs)
        )
