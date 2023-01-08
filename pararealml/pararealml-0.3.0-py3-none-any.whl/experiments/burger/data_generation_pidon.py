import numpy as np

from pararealml.utils.rand import SEEDS, set_random_seed
from pararealml.utils.tf import use_cpu
from pararealml.utils.time import time


def generate_initial_conditions():
    original_initial_condition = ivp.initial_condition.discrete_y_0(
        coarse_fdm.vertex_oriented
    )[np.newaxis]
    coarse_fdm_sol = np.concatenate(
        [
            original_initial_condition,
            coarse_fdm.solve(ivp).discrete_y(),
        ],
        axis=0,
    )
    coarse_fast_fdm_sol = np.concatenate(
        [
            original_initial_condition,
            coarse_fast_fdm.solve(ivp).discrete_y(),
        ],
        axis=0,
    )

    initial_conditions = np.empty(
        (5000,) + ivp.constrained_problem.y_shape(coarse_fdm.vertex_oriented)
    )
    n_sub_ivps = 4
    n_initial_conditions_per_sub_ivp = len(initial_conditions) // n_sub_ivps

    relative_ind_sd = 1.0 / 40.0
    coarse_fdm_sol_ind_sd = relative_ind_sd * len(coarse_fdm_sol)
    coarse_fast_fdm_sol_ind_sd = relative_ind_sd * len(coarse_fast_fdm_sol)

    for i in range(n_sub_ivps):
        coarse_fdm_sol_ind = i * (len(coarse_fdm_sol) - 1) // n_sub_ivps
        coarse_fast_fdm_sol_ind = (
            i * (len(coarse_fast_fdm_sol) - 1) // n_sub_ivps
        )

        base_y_0 = coarse_fdm_sol[coarse_fdm_sol_ind]

        for j in range(n_initial_conditions_per_sub_ivp):
            correction = (
                coarse_fdm_sol[
                    min(
                        len(coarse_fdm_sol) - 1,
                        max(
                            0,
                            int(
                                np.random.normal(
                                    coarse_fdm_sol_ind, coarse_fdm_sol_ind_sd
                                )
                            ),
                        ),
                    )
                ]
                - coarse_fast_fdm_sol[
                    min(
                        len(coarse_fast_fdm_sol) - 1,
                        max(
                            0,
                            int(
                                np.random.normal(
                                    coarse_fast_fdm_sol_ind,
                                    coarse_fast_fdm_sol_ind_sd,
                                )
                            ),
                        ),
                    )
                ]
                + np.random.normal(loc=0.0, scale=1e-6, size=base_y_0.shape)
            )

            initial_conditions[i * n_initial_conditions_per_sub_ivp + j] = (
                base_y_0 + np.random.rand() * correction
            )

    np.random.shuffle(initial_conditions)
    return initial_conditions


if __name__ == "__main__":
    use_cpu()

    set_random_seed(SEEDS[0])

    from experiments.burger.ivp import ivp
    from experiments.burger.operators import coarse_fast_fdm, coarse_fdm

    pidon_initial_conditions = time("pidon initial condition data generation")(
        generate_initial_conditions
    )()[0]
    np.save("data/pidon_initial_conditions", pidon_initial_conditions)
