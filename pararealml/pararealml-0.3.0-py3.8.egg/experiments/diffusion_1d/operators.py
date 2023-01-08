import numpy as np

from pararealml.operators.fdm import *
from pararealml.operators.ml.auto_regression import *
from pararealml.operators.ml.fnn_regressor import FNNRegressor
from pararealml.operators.ml.pidon import *

from experiments.diffusion.ivp import cp

fine_fdm = FDMOperator(
    RK4(),
    ThreePointCentralDifferenceMethod(),
    5e-4
)

coarse_fdm = FDMOperator(
    ForwardEulerMethod(),
    ThreePointCentralDifferenceMethod(),
    1e-3
)

coarse_ar = AutoRegressionOperator(
    .5,
    coarse_fdm.vertex_oriented,
    time_variant=False
)
ar_model = FNNRegressor(
    [np.prod(cp.y_vertices_shape).item() + cp.mesh.dimensions] +
    [50] * 10 + [1],
    initialization='he_uniform',
    activation='softplus'
)
sklearn_ar_model = SKLearnKerasRegressor(ar_model)
sklearn_ar_model.model = ar_model
coarse_ar.model = sklearn_ar_model

coarse_pidon = PIDONOperator(
    UniformRandomCollocationPointSampler(),
    .5,
    coarse_fdm.vertex_oriented,
    auto_regression_mode=True
)
coarse_pidon.model = PIDeepONet(
    cp,
    latent_output_size=1,
    branch_hidden_layer_sizes=[50] * 10,
    trunk_hidden_layer_sizes=[50] * 10,
    vertex_oriented=coarse_fdm.vertex_oriented,
    branch_initialization='he_uniform',
    branch_activation='softplus',
    trunk_initialization='he_uniform',
    trunk_activation='softplus'
)
