from typing import Optional, Dict, Union

import numpy as np
from pandas import DataFrame

from lumipy.provider.metadata import ColumnMeta, ParamMeta, TableParam
from lumipy.provider.base_provider import BaseProvider
from lumipy.typing.sql_value_type import SqlValType


class UniformDistProvider(BaseProvider):
    """Provides a collection of values drawn from a uniform probability distribution.

    This provider uses numpy's numpy.random.uniform() function.
    """

    def __init__(self):

        columns = [ColumnMeta("Outcome", SqlValType.Double, "Outcome of draw from uniform distribution.", True)]
        params = [
            ParamMeta("UpperLim", SqlValType.Double, "Upper limit of uniform distribution", 1.0),
            ParamMeta("LowerLim", SqlValType.Double, "Lower limit of uniform distribution", 0.0),
            ParamMeta("Seed", SqlValType.Int, "Random seed to set in numpy.")
        ]

        super().__init__(
            "Numpy.Random.Uniform",
            columns,
            params,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        upper = params['UpperLim']
        lower = params['LowerLim']
        seed = params.get('Seed')

        if seed is not None:
            np.random.seed(seed)

        if limit is None:
            limit = 100

        return DataFrame({
            "Outcome": np.random.uniform(lower, upper, size=limit)
        })


class BernoulliDistProvider(BaseProvider):
    """Provides a collection of draws from a Bernoulli distribution with a given trial probability p.

    This provider uses numpy's numpy.random.binomial() function with n=1. The Bernoulli distribution is a special case
    of the Binomial distribution where the number of trials (n) is equal to 1.
    """

    def __init__(self):
        """Constructor for BernoulliProvider class.

        """
        columns = [ColumnMeta("Outcome", SqlValType.Boolean, "Outcome of a Bernoulli trial.", True)]
        parameters = [
            ParamMeta("Probability", SqlValType.Double, "Probability of success per-trial.", default_value=0.5),
            ParamMeta("Seed", SqlValType.Int, "Random seed to set in numpy.")
        ]

        super().__init__(
            "Numpy.Random.Bernoulli",
            columns,
            parameters,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        seed = params.get('Seed')
        if seed is not None:
            np.random.seed(seed)

        if limit is None:
            limit = 100

        return DataFrame({
            'Outcome': np.random.binomial(1, params['Probability'], size=limit).astype(bool)
        })


class GaussianDistProvider(BaseProvider):
    """Provides a collection of draws from a multivariate Gaussian distribution for a given covariance matrix and
    set of means.

    """

    def __init__(self, dimensions):

        self.dimensions = dimensions

        columns = [
            ColumnMeta(f"Dim{i}", SqlValType.Double, f"Value of random variable in dimension {i}")
            for i in range(self.dimensions)
        ]
        params = [
            ParamMeta("Seed", SqlValType.Int, "Random seed to set in numpy.")
        ]
        table_params = [
            TableParam(
                'Covariance',
                description="The covariance matrix of the distribution specified as a table."
            ),
            TableParam(
                'Means',
                columns=[ColumnMeta("Mean", SqlValType.Double)],
                description="The means of the distribution specified as a single-column table."
            )
        ]

        super().__init__(
            f"Numpy.Random.Gaussian{self.dimensions}D",
            columns=columns,
            parameters=params,
            table_parameters=table_params,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        covmat = params['Covariance']
        means = params['Means']
        if means.shape[1] != 1:
            raise ValueError("Means parameter must only have one column.")

        seed = params.get('Seed')
        if seed is not None:
            np.random.seed(seed)

        if limit is None:
            limit = 100

        res = np.random.multivariate_normal(means.values.flatten(), covmat.values, size=limit)
        return DataFrame(
            res,
            columns=[f'Dim{i}' for i in range(res.shape[1])]
        )
