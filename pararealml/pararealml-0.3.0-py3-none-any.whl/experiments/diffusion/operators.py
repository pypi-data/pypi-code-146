import numpy as np
import tensorflow as tf

from experiments.diffusion.ivp import cp
from pararealml.operators.fdm import (
    FDMOperator,
    ForwardEulerMethod,
    ThreePointCentralDifferenceMethod,
)
from pararealml.operators.ml.auto_regression import (
    AutoRegressionOperator,
    SKLearnKerasRegressor,
)
from pararealml.operators.ml.deeponet import DeepONet
from pararealml.operators.ml.pidon import (
    PIDeepONet,
    PIDONOperator,
    UniformRandomCollocationPointSampler,
)

fine_fdm = FDMOperator(
    ForwardEulerMethod(), ThreePointCentralDifferenceMethod(), 1e-4
)

coarse_fdm = FDMOperator(
    ForwardEulerMethod(), ThreePointCentralDifferenceMethod(), 1e-3
)

coarse_fast_fdm = FDMOperator(
    ForwardEulerMethod(), ThreePointCentralDifferenceMethod(), 2e-3
)

coarse_ar = AutoRegressionOperator(
    0.5, coarse_fdm.vertex_oriented, time_variant=False
)
ar_model = DeepONet(
    branch_net=tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(
                np.prod(cp.y_shape(coarse_ar.vertex_oriented)).item()
            )
        ]
        + [
            tf.keras.layers.Dense(
                50, kernel_initializer="he_uniform", activation="softplus"
            )
            for _ in range(5)
        ]
    ),
    trunk_net=tf.keras.Sequential(
        [tf.keras.layers.InputLayer(cp.differential_equation.x_dimension)]
        + [
            tf.keras.layers.Dense(
                50, kernel_initializer="he_uniform", activation="softplus"
            )
            for _ in range(5)
        ]
    ),
    combiner_net=tf.keras.Sequential(
        [tf.keras.layers.InputLayer(150)]
        + [tf.keras.layers.Dense(50, activation="tanh") for _ in range(5)]
        + [tf.keras.layers.Dense(cp.differential_equation.y_dimension)]
    ),
)
sklearn_ar_model = SKLearnKerasRegressor(lambda _: ar_model)
sklearn_ar_model.model = ar_model
coarse_ar.model = sklearn_ar_model

coarse_pidon = PIDONOperator(
    UniformRandomCollocationPointSampler(),
    0.5,
    coarse_fdm.vertex_oriented,
    auto_regression_mode=True,
)
coarse_pidon.model = PIDeepONet(
    branch_net=tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(
                np.prod(cp.y_shape(coarse_ar.vertex_oriented)).item()
            )
        ]
        + [
            tf.keras.layers.Dense(
                50,
                kernel_initializer="he_uniform",
                activation="softplus",
            )
            for _ in range(5)
        ]
    ),
    trunk_net=tf.keras.Sequential(
        [tf.keras.layers.InputLayer(cp.differential_equation.x_dimension + 1)]
        + [
            tf.keras.layers.Dense(
                50,
                kernel_initializer="he_uniform",
                activation="softplus",
            )
            for _ in range(5)
        ]
    ),
    combiner_net=tf.keras.Sequential(
        [tf.keras.layers.InputLayer(150)]
        + [
            tf.keras.layers.Dense(
                50,
                kernel_initializer="glorot_uniform",
                activation="tanh",
                activity_regularizer=tf.keras.regularizers.L2(l2=1e-3),
            )
            for _ in range(5)
        ]
        + [tf.keras.layers.Dense(cp.differential_equation.y_dimension)]
    ),
    cp=cp,
    vertex_oriented=coarse_pidon.vertex_oriented,
    ic_loss_weight=2.0,
)
