from mpi4py import MPI
import tensorflow as tf

from pararealml import DiscreteInitialCondition, \
    VectorizedInitialConditionFunction
from pararealml.utils.rand import set_random_seed, SEEDS
from pararealml.utils.time import time

from experiments.diffusion.ivp import ivp
from experiments.diffusion.operators import *


coarse_fdm_sol = np.concatenate(
    [
        ivp.initial_condition.discrete_y_0(True)[np.newaxis],
        coarse_fdm.solve(ivp).discrete_y()
    ],
    axis=0
)


def y_0_function(t: float) -> VectorizedInitialConditionFunction:
    ind = int(
        t / (ivp.t_interval[1] - ivp.t_interval[0]) * len(coarse_fdm_sol)
    )
    y_0 = coarse_fdm_sol[ind] + \
        coarse_fdm_sol[max(0, int(np.random.normal(ind, 10)))] - \
        coarse_fdm_sol[max(0, int(np.random.normal(ind, 10)))]
    return DiscreteInitialCondition(cp, y_0, coarse_fdm.vertex_oriented).y_0


if __name__ == '__main__':
    rank = MPI.COMM_WORLD.rank

    set_random_seed(SEEDS[rank])

    y_0_functions = []
    for t_mean in [0., .5, 1., 1.5]:
        y_0_functions += [
            y_0_function(np.abs(np.random.normal(t_mean, .01)))
            for _ in range(10)
        ]
    np.random.shuffle(y_0_functions)
    training_y_0_functions = y_0_functions[:36]
    test_y_0_functions = y_0_functions[36:]

    pidon_train_loss_history, pidon_test_loss_history = time(
        f'rank {rank} pidon training'
    )(coarse_pidon.train)(
        cp,
        (0., coarse_pidon.d_t),
        training_data_args=DataArgs(
            y_0_functions=training_y_0_functions,
            n_domain_points=50,
            n_boundary_points=20,
            n_batches=1,
            n_ic_repeats=1,
            shuffle=False
        ),
        test_data_args=DataArgs(
            y_0_functions=test_y_0_functions,
            n_domain_points=50,
            n_boundary_points=20,
            n_batches=1,
            n_ic_repeats=1,
            shuffle=False
        ),
        optimization_args=OptimizationArgs(
            optimizer=tf.optimizers.Adam(1e-3),
            epochs=10000,
            diff_eq_loss_weight=0.,
            bc_loss_weight=0.
        )
    )[0]
    print(
        f'rank {rank} pidon train loss:',
        pidon_train_loss_history[-1].weighted_total_loss.numpy()
    )
    print(
        f'rank {rank} pidon test loss:',
        pidon_test_loss_history[-1].weighted_total_loss.numpy()
    )
    coarse_pidon.model.save_weights(f'weights/pidon_{rank}')
