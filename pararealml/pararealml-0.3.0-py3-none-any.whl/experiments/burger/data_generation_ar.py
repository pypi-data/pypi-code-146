import numpy as np

from pararealml.utils.rand import SEEDS
from pararealml.utils.tf import use_cpu
from pararealml.utils.time import time

use_cpu()

from experiments.burger.ivp import ivp  # noqa: E402
from experiments.burger.operators import (  # noqa: E402
    coarse_ar,
    coarse_fast_fdm,
    coarse_fdm,
)

initial_condition = ivp.initial_condition.discrete_y_0(
    coarse_fdm.vertex_oriented
)[np.newaxis]
coarse_fdm_sol = np.concatenate(
    [
        initial_condition,
        coarse_fdm.solve(ivp).discrete_y(),
    ],
    axis=0,
)
coarse_fast_fdm_sol = np.concatenate(
    [
        initial_condition,
        coarse_fast_fdm.solve(ivp).discrete_y(),
    ],
    axis=0,
)


def perturbate_initial_conditions(t: float, y: np.ndarray) -> np.ndarray:
    relative_ind_sd = 1.0 / 40.0
    relative_t = t / (ivp.t_interval[1] - ivp.t_interval[0])
    coarse_fdm_sol_ind = int(relative_t * len(coarse_fdm_sol))
    coarse_fast_fdm_sol_ind = int(relative_t * len(coarse_fast_fdm_sol))
    coarse_fdm_sol_ind_sd = relative_ind_sd * len(coarse_fdm_sol)
    coarse_fast_fdm_sol_ind_sd = relative_ind_sd * len(coarse_fast_fdm_sol)

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
                            coarse_fast_fdm_sol_ind, coarse_fast_fdm_sol_ind_sd
                        )
                    ),
                ),
            )
        ]
        + np.random.normal(loc=0.0, scale=1e-6, size=y.shape)
    )

    return y + np.random.rand() * correction


if __name__ == "__main__":
    n_jobs = 4
    ar_data = time("ar data generation")(coarse_ar.generate_data)(
        ivp,
        coarse_fdm,
        300,
        perturbate_initial_conditions,
        isolate_perturbations=True,
        n_jobs=n_jobs,
        seeds=SEEDS[:n_jobs],
    )[0]
    np.save("data/ar_features", ar_data[0])
    np.save("data/ar_labels", ar_data[1])
