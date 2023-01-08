import numpy as np

from pararealml.utils.rand import SEEDS
from pararealml.utils.tf import use_cpu
from pararealml.utils.time import time

use_cpu()

from experiments.diffusion.ivp import ivp  # noqa: E402
from experiments.diffusion.operators import coarse_ar, coarse_fdm  # noqa: E402

coarse_fdm_sol = np.concatenate(
    [
        ivp.initial_condition.discrete_y_0(coarse_fdm.vertex_oriented)[
            np.newaxis
        ],
        coarse_fdm.solve(ivp).discrete_y(),
    ],
    axis=0,
)


def perturbate_initial_conditions(t: float, y: np.ndarray) -> np.ndarray:
    ind = int(
        t / (ivp.t_interval[1] - ivp.t_interval[0]) * len(coarse_fdm_sol)
    )
    sd = len(coarse_fdm_sol) / 20.0
    return (
        y
        + coarse_fdm_sol[
            min(
                len(coarse_fdm_sol) - 1, max(0, int(np.random.normal(ind, sd)))
            )
        ]
        - coarse_fdm_sol[
            min(
                len(coarse_fdm_sol) - 1, max(0, int(np.random.normal(ind, sd)))
            )
        ]
    )


if __name__ == "__main__":
    n_jobs = 4
    ar_data = time("ar data generation")(coarse_ar.generate_data)(
        ivp,
        coarse_fdm,
        250,
        perturbate_initial_conditions,
        isolate_perturbations=True,
        n_jobs=n_jobs,
        seeds=SEEDS[:n_jobs],
    )[0]
    np.save("data/ar_features", ar_data[0])
    np.save("data/ar_labels", ar_data[1])
