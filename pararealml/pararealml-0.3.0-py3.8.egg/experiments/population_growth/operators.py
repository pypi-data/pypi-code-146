import tensorflow as tf

from experiments.population_growth.ivp import cp
from pararealml.operators.fdm import (
    FDMOperator,
    ForwardEulerMethod,
    ThreePointCentralDifferenceMethod,
)
from pararealml.operators.ml.auto_regression import (
    AutoRegressionOperator,
    SKLearnKerasRegressor,
)
from pararealml.operators.ml.pidon import (
    PIDeepONet,
    PIDONOperator,
    UniformRandomCollocationPointSampler,
)

fine_fdm = FDMOperator(
    ForwardEulerMethod(), ThreePointCentralDifferenceMethod(), 2.5e-5
)

coarse_fdm = FDMOperator(
    ForwardEulerMethod(), ThreePointCentralDifferenceMethod(), 2.5e-4
)

coarse_fast_fdm = FDMOperator(
    ForwardEulerMethod(), ThreePointCentralDifferenceMethod(), 4e-4
)

coarse_ar = AutoRegressionOperator(
    1.25, coarse_fdm.vertex_oriented, time_variant=False
)
ar_model = tf.keras.Sequential(
    [
        tf.keras.layers.InputLayer(
            cp.differential_equation.y_dimension
            + cp.differential_equation.x_dimension
        )
    ]
    + [
        tf.keras.layers.Dense(
            50, kernel_initializer="he_uniform", activation="softplus"
        )
        for _ in range(3)
    ]
    + [
        tf.keras.layers.Dense(
            cp.differential_equation.y_dimension,
            kernel_initializer="he_uniform",
        )
    ]
)
sklearn_ar_model = SKLearnKerasRegressor(lambda _: ar_model)
sklearn_ar_model.model = ar_model
coarse_ar.model = sklearn_ar_model

coarse_pidon = PIDONOperator(
    UniformRandomCollocationPointSampler(),
    1.25,
    coarse_fdm.vertex_oriented,
    auto_regression_mode=True,
)
coarse_pidon.model = PIDeepONet(
    branch_net=tf.keras.Sequential(
        [tf.keras.layers.InputLayer(cp.differential_equation.y_dimension)]
        + [
            tf.keras.layers.Dense(
                50, kernel_initializer="he_uniform", activation="softplus"
            )
            for _ in range(3)
        ]
    ),
    trunk_net=tf.keras.Sequential(
        [tf.keras.layers.InputLayer(cp.differential_equation.x_dimension + 1)]
        + [
            tf.keras.layers.Dense(
                50, kernel_initializer="he_uniform", activation="softplus"
            )
            for _ in range(3)
        ]
    ),
    combiner_net=tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(150),
            tf.keras.layers.Dense(cp.differential_equation.y_dimension),
        ]
    ),
    cp=cp,
)
