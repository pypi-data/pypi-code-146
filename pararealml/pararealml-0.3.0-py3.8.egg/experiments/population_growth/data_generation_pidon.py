import numpy as np

from pararealml.utils.rand import SEEDS, set_random_seed
from pararealml.utils.tf import use_cpu
from pararealml.utils.time import time


def generate_initial_conditions():
    coarse_fdm_sol = np.concatenate(
        [
            ivp.initial_condition.discrete_y_0()[np.newaxis],
            coarse_fdm.solve(ivp).discrete_y(),
        ],
        axis=0,
    )

    initial_conditions = np.empty((800,) + ivp.constrained_problem.y_shape())
    n_sub_ivps = 4
    for i in range(n_sub_ivps):
        coarse_fdm_sol_ind = i * (len(coarse_fdm_sol) - 1) // n_sub_ivps
        base_y_0 = coarse_fdm_sol[coarse_fdm_sol_ind]
        for j in range(len(initial_conditions) // n_sub_ivps):
            initial_conditions[
                i * len(initial_conditions) // n_sub_ivps + j
            ] = np.abs(base_y_0 + np.random.normal(0.0, 2.0, base_y_0.shape))

    np.random.shuffle(initial_conditions)
    return initial_conditions


if __name__ == "__main__":
    use_cpu()

    set_random_seed(SEEDS[0])

    from experiments.population_growth.ivp import ivp
    from experiments.population_growth.operators import coarse_fdm

    pidon_initial_conditions = time("pidon initial condition data generation")(
        generate_initial_conditions
    )()[0]
    np.save("data/pidon_initial_conditions", pidon_initial_conditions)
