from typing import Optional, Dict, Union

import numpy as np
from cvxopt import matrix, solvers
from lumipy.provider.base_provider import BaseProvider
from lumipy.provider.metadata import ColumnMeta, ParamMeta, TableParam
from lumipy.typing.sql_value_type import SqlValType
from pandas import DataFrame, to_datetime


class QuadraticProgram(BaseProvider):
    """This provider calculates weights for a collection of securities given a table of returns data. It does this by
    solving the following quadratic program

        min_w  \lambda w^T \Sigma w - \mu w

    where \Sigma is the covariance matrix of the returns series, \mu is the mean returns vector, w is the weights
    vector.

    """

    def __init__(self):

        columns = [
            ColumnMeta('Id', SqlValType.Text, "Id that labels the security (i.e. a stock ticker)"),
            ColumnMeta('Weight', SqlValType.Double, "Weight assigned by the quadratic optimisation."),
        ]
        parameters = [
            ParamMeta(
                'Lam',
                SqlValType.Double,
                "Scaling parameter on the quadratic part of the objective. Sets the tradeoff between risk and returns "
                "(defaults to 1.0)",
                default_value=1.0,
            )
        ]
        table_parameters = [
            TableParam(
                'PriceData',
                columns=[
                    ColumnMeta('Id', SqlValType.Text),
                    ColumnMeta('Date', SqlValType.Date),
                    ColumnMeta('Price', SqlValType.Double),
                ],
                description='A table of returns data to use in the quadratic program.'
            )
        ]

        super().__init__(
            name='Tools.Index.Quadratic.Program',
            columns=columns,
            parameters=parameters,
            table_parameters=table_parameters,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        df = params.get('PriceData')
        lam = params.get('Lam')

        if df.shape[0] == 0:
            raise ValueError('Input table variable was empty.')

        df['Date'] = to_datetime(df.Date)
        df = df.sort_values(['Date']).set_index(['Date', 'Id'])

        rdf = np.log(df.unstack()).diff(axis=0).iloc[1:]

        cov_mat = rdf.cov().values
        avg_ret = rdf.mean(axis=0).values

        # Opt
        n = len(avg_ret)

        Q = matrix(lam * cov_mat)
        p = matrix(-avg_ret)

        G = matrix(np.vstack([np.diag([1.0] * n), np.diag([-1.0] * n)]))
        h = matrix([1.0] * n + [0.0] * n)

        A = matrix([1.0] * n, (1, n))
        b = matrix(1.0)

        sol = solvers.qp(Q, p, G, h, A, b)

        return DataFrame({
            'Id': [c[1] for c in rdf.columns],
            'Weight': np.array(sol['x']).flatten()
        }).sort_values(
            'Weight', ascending=False
        ).reset_index(drop=True)
