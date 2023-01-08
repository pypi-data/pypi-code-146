from mpi4py import MPI
import tensorflow as tf

from pararealml.utils.rand import set_random_seed, SEEDS
from pararealml.utils.time import time

from experiments.diffusion.operators import *


if __name__ == '__main__':
    rank = MPI.COMM_WORLD.rank

    set_random_seed(SEEDS[rank])

    ar_data = (
        np.load(f'data/ar_features_{rank}.npy'),
        np.load(f'data/ar_labels_{rank}.npy')
    )
    ar_train_loss, ar_test_loss = time(f'rank {rank} ar model fitting')(
        coarse_ar.fit_model
    )(
        SKLearnKerasRegressor(
            ar_model,
            optimizer=tf.optimizers.Adam(
                learning_rate=tf.optimizers.schedules.ExponentialDecay(
                    1e-3, decay_steps=75000, decay_rate=.0001
                )
            ),
            batch_size=94080,
            epochs=25000,
            verbose=True,
            validation_split=.2,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    min_delta=0,
                    patience=1000,
                    restore_best_weights=True,
                )
            ]
        ),
        ar_data,
        test_size=.2
    )[0]
    print(f'rank {rank} ar train loss:', ar_train_loss)
    print(f'rank {rank} ar test loss:', ar_test_loss)
    coarse_ar.model.model.save_weights(f'weights/ar_{rank}')
