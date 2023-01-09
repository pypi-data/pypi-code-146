from typing import Any, Tuple
import logging

import numpy as np

from sarus_data_spec.constants import PUBLIC, USER_COLUMN, WEIGHTS

from ..protection_utils import dp_transform, pandas_merge_pe

logger = logging.getLogger(__name__)

try:
    from sarus_statistics.ops.histograms import dataset_length
    from sarus_statistics.ops.max_multiplicity import max_multiplicity
except ModuleNotFoundError:
    logger.info(
        "`sarus_statistics` not installed. DP primitives not available."
    )

try:
    from sarus_differential_privacy.query import (
        ComposedQuery,
        EpsilonQuery,
        LaplaceQuery,
        PrivateQuery,
    )
except ModuleNotFoundError:
    logger.info(
        "`sarus_differential_privacy` not installed. "
        "DP primitives not available."
    )


@dp_transform([{"dataframe"}])
async def pd_shape_dp(
    dataframe: Any, budget: Any, seed: int, pe: Any
) -> Tuple[Any, PrivateQuery]:
    """Implementation of DP shape.

    A DP implementation receives additional arguments compared to a standard
    external implementation:
        - `budget`: a list of sp.Scalar.PrivacyParams.Point object containing
          each an epsilon and a delta values
        - `seed`: an integer used to parametrize random number generators
        - `pe`: the protected entity used by `sarus_statistics` primitives

    The DP implementation returns the private result an a PrivateQuery.
    """
    n_rows, n_cols = dataframe.shape

    if len(budget) != 1:
        raise NotImplementedError(
            "The PrivacyParams contains more than 1 point in the privacy "
            "profile."
        )

    epsilon = budget[0].epsilon
    if epsilon == 0.0:
        raise ValueError("`epsilon` should be greater than 0.")

    dataframe_with_pe = pandas_merge_pe(dataframe, pe).to_pandas()
    random_generator = np.random.default_rng(abs(seed))
    MAX_MAX_MULTIPLICITY = 50  # TODO infer proper max_max_multiplicity
    NOISE_USER_COUNT = 1.0  # TODO do with QB => use delta
    NOISE_MULTIPLICITY = 1.0  # TODO do with QB => use delta
    NOISE = 1.0 / epsilon

    # Compute DP value
    max_mul = max_multiplicity(
        data=dataframe_with_pe,
        epsilon_queries=epsilon,
        noise_user_count=NOISE_USER_COUNT,
        noise_multiplicity=NOISE_MULTIPLICITY,
        max_max_multiplicity=MAX_MAX_MULTIPLICITY,
        user_col=USER_COLUMN,
        private_col=PUBLIC,
        weight_col=WEIGHTS,
        random_generator=random_generator,
    )

    n_rows = dataset_length(
        data=dataframe_with_pe,
        max_multiplicity=max_mul,
        noise=NOISE,
        user_col=USER_COLUMN,
        private_col=PUBLIC,
        weight_col=WEIGHTS,
        random_generator=random_generator,
    )

    dp_shape = (n_rows, n_cols)

    # Compute private query
    # TODO we suppose that there is only 1 private table
    # we should use the schema to infer that instead
    N_TABLES = 1
    max_multiplicity_query = ComposedQuery(
        [
            EpsilonQuery(epsilon=1.0 / NOISE_USER_COUNT)
            for _ in range(2 * N_TABLES)
        ]
    )
    laplace_query = LaplaceQuery(noise=NOISE)
    private_query = ComposedQuery([max_multiplicity_query, laplace_query])

    return dp_shape, private_query
