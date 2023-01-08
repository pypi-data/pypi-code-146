from typing import Sequence

from mpi4py import MPI

from pararealml.operators.parareal import *
from pararealml.utils.time import time, mpi_time

from experiments.diffusion.ivp import *
from experiments.diffusion.operators import *


comm = MPI.COMM_WORLD
rank = comm.rank


def print_execution_time_stats(execution_times: Sequence[float], name: str):
    print(
        f'rank {rank} {name} execution time - '
        f'mean: {np.mean(execution_times)}s; sd: {np.std(execution_times)}'
    )


coarse_ar.model.model.load_weights(f'weights/ar_{rank}')
coarse_pidon.model.load_weights(f'weights/pidon_{rank}')

parareal_tol = 1e-2
parareal_fdm = PararealOperator(fine_fdm, coarse_fdm, parareal_tol)
parareal_ar = PararealOperator(fine_fdm, coarse_ar, parareal_tol)
parareal_pidon = PararealOperator(fine_fdm, coarse_pidon, parareal_tol)

n_warmup_runs = 2
n_real_runs = 20

fine_fdm_sol = None
coarse_fdm_sol = None
coarse_ar_sol = None
coarse_pidon_sol = None
parareal_fdm_sol = None
parareal_ar_sol = None
parareal_pidon_sol = None

fine_fdm_times = []
coarse_fdm_times = []
coarse_ar_times = []
coarse_pidon_times = []
parareal_fdm_times = []

for run_ind in range(n_warmup_runs + n_real_runs):
    fine_fdm_sol, fine_fdm_time = \
        time(f'rank {rank} fine fdm')(fine_fdm.solve)(ivp)
    coarse_fdm_sol, coarse_fdm_time = \
        time(f'rank {rank} coarse fdm')(coarse_fdm.solve)(ivp)
    coarse_ar_sol, coarse_ar_time = \
        time(f'rank {rank} coarse ar')(coarse_ar.solve)(ivp)
    coarse_pidon_sol, coarse_pidon_time = \
        time(f'rank {rank} coarse pidon')(coarse_pidon.solve)(ivp)
    parareal_fdm_sol, parareal_fdm_time = \
        mpi_time(f'parareal fdm')(parareal_fdm.solve)(ivp)

    if run_ind >= n_warmup_runs:
        fine_fdm_times.append(fine_fdm_time)
        coarse_fdm_times.append(coarse_fdm_time)
        coarse_ar_times.append(coarse_ar_time)
        coarse_pidon_times.append(coarse_pidon_time)
        parareal_fdm_times.append(parareal_fdm_time)

for model_ind in range(comm.size):
    coarse_ar.model.model.load_weights(f'weights/ar_{model_ind}')
    coarse_pidon.model.load_weights(f'weights/pidon_{model_ind}')

    parareal_ar_times = []
    parareal_pidon_times = []

    for run_ind in range(n_real_runs):
        parareal_ar_sol, parareal_ar_time = \
            mpi_time(f'parareal ar')(parareal_ar.solve)(ivp)
        parareal_pidon_sol, parareal_pidon_time = \
            mpi_time(f'parareal pidon')(parareal_pidon.solve)(ivp)

        parareal_ar_times.append(parareal_ar_time)
        parareal_pidon_times.append(parareal_pidon_time)

    if rank == model_ind:
        print_execution_time_stats(fine_fdm_times, 'fine fdm')
        print_execution_time_stats(coarse_fdm_times, 'coarse fdm')
        print_execution_time_stats(coarse_ar_times, 'coarse ar')
        print_execution_time_stats(coarse_pidon_times, 'coarse pidon')
        print_execution_time_stats(parareal_fdm_times, 'parareal fdm')
        print_execution_time_stats(parareal_ar_times, 'parareal ar')
        print_execution_time_stats(parareal_pidon_times, 'parareal pidon')

        diff = fine_fdm_sol.diff([
            coarse_fdm_sol,
            coarse_ar_sol,
            coarse_pidon_sol,
            parareal_fdm_sol,
            parareal_ar_sol,
            parareal_pidon_sol
        ])
        rss_diffs = np.sqrt(np.square(np.stack(diff.differences)).sum(axis=2))
        print(f'rank {rank} - RSS differences:', repr(rss_diffs))
        print(
            f'rank {rank} - max RSS differences:',
            rss_diffs.max(axis=-1, keepdims=True)
        )
        print(
            f'rank {rank} - mean RSS differences:',
            rss_diffs.mean(axis=-1, keepdims=True)
        )
