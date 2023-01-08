import numpy as np

from pararealml.utils.rand import SEEDS
from pararealml.utils.tf import use_cpu
from pararealml.utils.time import time


def perturbate_initial_conditions(_: float, y: np.ndarray):
    return np.abs(y + np.random.normal(0.0, 2.0, y.shape))


if __name__ == "__main__":
    use_cpu()

    from experiments.population_growth.ivp import ivp
    from experiments.population_growth.operators import coarse_ar, coarse_fdm

    n_jobs = 4
    ar_data = time("ar data generation")(coarse_ar.generate_data)(
        ivp,
        coarse_fdm,
        2500,
        perturbate_initial_conditions,
        isolate_perturbations=True,
        n_jobs=n_jobs,
        seeds=SEEDS[:n_jobs],
    )[0]
    np.save("data/ar_features", ar_data[0])
    np.save("data/ar_labels", ar_data[1])
