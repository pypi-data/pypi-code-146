import logging

import numpy as np
import tensorflow as tf

from pararealml.operators.ml.pidon import DataArgs, OptimizationArgs
from pararealml.utils.rand import SEEDS, set_random_seed
from pararealml.utils.tf import use_deterministic_ops
from pararealml.utils.time import time

if __name__ == "__main__":
    set_random_seed(SEEDS[0])

    use_deterministic_ops()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    from experiments.population_growth.ivp import cp
    from experiments.population_growth.operators import coarse_pidon

    y_0s = np.load("data/pidon_initial_conditions.npy")
    y_0_functions = [lambda _, _y_0=y_0: _y_0 for y_0 in y_0s]
    training_y_0_functions = y_0_functions[:400]
    test_y_0_functions = y_0_functions[400:]

    training_results = time("pidon training")(coarse_pidon.train)(
        cp,
        (0.0, coarse_pidon.d_t),
        training_data_args=DataArgs(
            y_0_functions=training_y_0_functions,
            n_domain_points=200,
            n_batches=1,
            n_ic_repeats=1,
            shuffle=False,
        ),
        test_data_args=DataArgs(
            y_0_functions=test_y_0_functions,
            n_domain_points=200,
            n_batches=1,
            n_ic_repeats=1,
            shuffle=False,
        ),
        optimization_args=OptimizationArgs(
            optimizer=tf.optimizers.Adam(
                learning_rate=tf.optimizers.schedules.ExponentialDecay(
                    1e-3, decay_steps=20000, decay_rate=0.2
                )
            ),
            epochs=80000,
        ),
    )[0]
    print(
        "pidon train loss:",
        training_results.final_training_loss.weighted_total_loss.numpy(),
    )
    print(
        "pidon test loss:",
        training_results.final_test_loss.weighted_total_loss.numpy(),
    )
    coarse_pidon.model.save_weights("weights/pidon")
