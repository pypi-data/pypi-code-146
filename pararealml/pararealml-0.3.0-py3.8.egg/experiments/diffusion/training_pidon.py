import logging

import numpy as np
import tensorflow as tf

from pararealml import DiscreteInitialCondition
from pararealml.operators.ml.pidon import DataArgs, OptimizationArgs
from pararealml.utils.rand import SEEDS, set_random_seed
from pararealml.utils.time import time

if __name__ == "__main__":
    set_random_seed(SEEDS[0])

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    from experiments.diffusion.ivp import ivp
    from experiments.diffusion.operators import coarse_fdm, coarse_pidon

    y_0s = np.load("data/pidon_initial_conditions.npy")
    y_0_functions = [
        DiscreteInitialCondition(
            ivp.constrained_problem, y_0, coarse_fdm.vertex_oriented
        ).y_0
        for y_0 in y_0s
    ]
    training_y_0_functions = y_0_functions[:4000]
    test_y_0_functions = y_0_functions[4000:]

    training_results = time("pidon training")(coarse_pidon.train)(
        ivp.constrained_problem,
        (0.0, coarse_pidon.d_t),
        training_data_args=DataArgs(
            y_0_functions=training_y_0_functions,
            n_domain_points=16000,
            n_boundary_points=6000,
            n_batches=10000,
            n_ic_repeats=20,
        ),
        test_data_args=DataArgs(
            y_0_functions=test_y_0_functions,
            n_domain_points=16000,
            n_boundary_points=6000,
            n_batches=2500,
            n_ic_repeats=20,
            shuffle=False,
        ),
        optimization_args=OptimizationArgs(
            optimizer=tf.optimizers.Adam(
                learning_rate=tf.optimizers.schedules.ExponentialDecay(
                    1e-3, decay_steps=700000, decay_rate=0.1
                )
            ),
            epochs=200,
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
