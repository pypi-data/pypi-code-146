from mpi4py import MPI

from pararealml.utils.rand import set_random_seed, SEEDS
from pararealml.utils.tf import use_cpu
from pararealml.utils.time import time

use_cpu()

from experiments.diffusion.ivp import *
from experiments.diffusion.operators import *


coarse_fdm_sol = np.concatenate(
    [
        ivp.initial_condition.discrete_y_0(True)[np.newaxis],
        coarse_fdm.solve(ivp).discrete_y()
    ],
    axis=0
)


def perturbation_function(t: float, y: np.ndarray) -> np.ndarray:
    ind = int(
        t / (ivp.t_interval[1] - ivp.t_interval[0]) * len(coarse_fdm_sol)
    )
    return y + \
        coarse_fdm_sol[max(0, int(np.random.normal(ind, 10)))] - \
        coarse_fdm_sol[max(0, int(np.random.normal(ind, 10)))]


if __name__ == '__main__':
    rank = MPI.COMM_WORLD.rank

    set_random_seed(SEEDS[rank])

    ar_data = time(f'rank {rank} ar data generation')(coarse_ar.generate_data)(
        ivp,
        coarse_fdm,
        250,
        perturbation_function,
        isolate_perturbations=True,
        n_jobs=4
    )[0]
    np.save(f'data/ar_features_{rank}', ar_data[0])
    np.save(f'data/ar_labels_{rank}', ar_data[1])
