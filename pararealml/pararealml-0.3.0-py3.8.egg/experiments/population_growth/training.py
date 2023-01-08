from mpi4py import MPI
import tensorflow as tf

from pararealml.utils.rand import set_random_seed, SEEDS
from pararealml.utils.time import time

from experiments.population_growth.ivp import *
from experiments.population_growth.operators import *


def perturbation_function(_: float, y: np.ndarray):
    return 60 * np.random.rand(*y.shape)


if __name__ == '__main__':
    rank = MPI.COMM_WORLD.rank

    set_random_seed(SEEDS[rank])

    data_generating_ivp = InitialValueProblem(
        cp,
        (0., coarse_ar.d_t),
        ivp.initial_condition
    )
    ar_data = time(f'rank {rank} ar data generation')(coarse_ar.generate_data)(
        data_generating_ivp,
        coarse_fdm,
        100000,
        perturbation_function,
        n_jobs=4
    )[0]

    ar_train_loss, ar_test_loss = time(f'rank {rank} ar model fitting')(
        coarse_ar.fit_model
    )(
        SKLearnKerasRegressor(
            ar_model,
            optimizer=tf.optimizers.Adam(
                learning_rate=tf.optimizers.schedules.ExponentialDecay(
                    1e-4, decay_steps=1000, decay_rate=.98
                )
            ),
            batch_size=4096,
            epochs=10000,
            verbose=True,
            validation_split=.2,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    min_delta=0,
                    patience=2000,
                    restore_best_weights=True,
                )
            ]
        ),
        ar_data
    )[0]
    print(f'rank {rank} ar train loss:', ar_train_loss)
    print(f'rank {rank} ar test loss:', ar_test_loss)
    coarse_ar.model.model.save_weights(f'weights/ar_{rank}')

    # set_random_seed(SEEDS[rank])
    #
    # fdm_sol = coarse_fdm.solve(ivp)
    # y_0_functions = [ic.y_0] * 25 + [
    #     lambda x, _y_0=y_0: _y_0
    #     for y_0 in fdm_sol.discrete_y(fdm_sol.vertex_oriented)[
    #         np.random.choice(40000, 10975, False)
    #     ]
    # ]
    # np.random.shuffle(y_0_functions)
    # training_y_0_functions = y_0_functions[:10000]
    # test_y_0_functions = y_0_functions[10000:]
    #
    # pidon_train_loss_history, pidon_test_loss_history = time(
    #     f'rank {rank} pidon training'
    # )(coarse_pidon.train)(
    #     cp,
    #     (0., 1.25),
    #     training_data_args=DataArgs(
    #         y_0_functions=training_y_0_functions,
    #         n_domain_points=5000,
    #         n_batches=5000,
    #         n_ic_repeats=1000
    #     ),
    #     test_data_args=DataArgs(
    #         y_0_functions=test_y_0_functions,
    #         n_domain_points=500,
    #         n_batches=50,
    #         n_ic_repeats=50
    #     ),
    #     model_args=ModelArgs(
    #         latent_output_size=50,
    #         branch_hidden_layer_sizes=[50] * 5,
    #         trunk_hidden_layer_sizes=[50] * 5,
    #     ),
    #     optimization_args=OptimizationArgs(
    #         optimizer=tf.optimizers.Adam(
    #             learning_rate=tf.optimizers.schedules.ExponentialDecay(
    #                 2.5e-3, decay_steps=2000, decay_rate=.98
    #             )
    #         ),
    #         epochs=120,
    #         diff_eq_loss_weight=10.
    #     )
    # )[0]
    # print(
    #     f'rank {rank} pidon train loss:',
    #     pidon_train_loss_history[-1].weighted_total_loss.numpy()
    # )
    # print(
    #     f'rank {rank} pidon test loss:',
    #     pidon_test_loss_history[-1].weighted_total_loss.numpy()
    # )
    # coarse_pidon.model.save_weights(f'weights/pidon_{rank}')
