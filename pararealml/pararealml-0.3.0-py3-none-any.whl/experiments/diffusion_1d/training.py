from mpi4py import MPI
from tensorflow import optimizers

from pararealml.utils.rand import set_random_seed, SEEDS
from pararealml.utils.time import time

from experiments.diffusion.ivp import *
from experiments.diffusion.operators import *

rank = MPI.COMM_WORLD.rank

mean_value = 1.

set_random_seed(SEEDS[rank])

don_data = time(f'rank {rank} don data generation')(coarse_don.generate_data)(
   ivp,
   coarse_fdm,
   2000,
   lambda t, y: (y - mean_value) * np.random.normal(1., t / 10.) + mean_value
)[0]

don_train_loss, don_test_loss = time(f'rank {rank} don model fitting')(
   coarse_don.fit_model
)(
   SKLearnKerasRegressor(
       don_model,
       optimizer=optimizers.Adam(
           learning_rate=optimizers.schedules.ExponentialDecay(
               5e-3, decay_steps=200, decay_rate=.98
           )
       ),
       batch_size=20000,
       epochs=5000,
       verbose=True
   ),
   don_data
)[0]
print(f'rank {rank} don train loss:', don_train_loss)
print(f'rank {rank} don test loss:', don_test_loss)
coarse_don.model.model.save_weights(f'weights/don_{rank}')

set_random_seed(SEEDS[rank])

fdm_sol = coarse_fdm.solve(ivp)
y_0_functions = [ic.y_0] * 20 + [
    DiscreteInitialCondition(
        cp,
        discrete_y,
        fdm_sol.vertex_oriented
    ).y_0 for discrete_y in fdm_sol.discrete_y(fdm_sol.vertex_oriented)
][:6580]
np.random.shuffle(y_0_functions)
training_y_0_functions = y_0_functions[:6000]
test_y_0_functions = y_0_functions[6000:]

pidon_train_loss_history, pidon_test_loss_history = time(
    f'rank {rank} pidon training'
)(coarse_pidon.train)(
    cp,
    (0., .25),
    training_data_args=DataArgs(
        y_0_functions=training_y_0_functions,
        n_domain_points=10000,
        n_boundary_points=2500,
        n_batches=6000,
        n_ic_repeats=100
    ),
    test_data_args=DataArgs(
        y_0_functions=test_y_0_functions,
        n_domain_points=1000,
        n_boundary_points=250,
        n_batches=60,
        n_ic_repeats=100
    ),
    model_args=ModelArgs(
        latent_output_size=50,
        branch_hidden_layer_sizes=[50] * 10,
        trunk_hidden_layer_sizes=[50] * 10,
        branch_initialization='he_uniform',
        branch_activation='relu',
    ),
    optimization_args=OptimizationArgs(
        optimizer=optimizers.Adam(
            learning_rate=optimizers.schedules.ExponentialDecay(
                5e-3, decay_steps=200, decay_rate=.98
            )
        ),
        epochs=20
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
