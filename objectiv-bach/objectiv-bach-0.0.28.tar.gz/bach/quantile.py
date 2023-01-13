from typing import Union, List

import pandas

from bach import DataFrame, SeriesFloat64
from bach.partitioning import WindowFrameBoundary, Window, GroupBy
from bach.series import SeriesAbstractNumeric, SeriesTimedelta
from bach.expression import Expression, AggregateFunctionExpression
from bach.series.series import WrappedPartition
from sql_models.util import is_bigquery, is_postgres, is_athena

_QUANTILES_SERIES_NAME = 'quantile'


def _get_valid_series_for_calculation(df: DataFrame) -> List[str]:
    """
    Returns data series names that support quantile operation.
    Currently supporting only numeric and timedelta series dtypes.
    """
    return [
        num_series.name
        for num_series in df.data.values()
        if isinstance(num_series, (SeriesAbstractNumeric, SeriesTimedelta))
    ]


def _add_quantiles_as_series(df: DataFrame, q: Union[float, List[float]]) -> DataFrame:
    """
    Adds a new series to the provided DataFrame containing all quantile values to be calculated.
    """
    quantiles_df = df.copy()

    if isinstance(q, float):
        quantiles_df[_QUANTILES_SERIES_NAME] = q
    else:
        quantiles_to_calculate = DataFrame.from_pandas(
            engine=df.engine,
            df=pandas.DataFrame({_QUANTILES_SERIES_NAME: q})
        )
        quantiles_to_calculate = quantiles_to_calculate.reset_index(drop=True)

        quantiles_df = quantiles_df.merge(quantiles_to_calculate, how='cross')

    return quantiles_df


def _calculate_quantiles_with_percentile_cont(
    df: DataFrame, q: Union[float, List[float]], group_by: List[str],
) -> DataFrame:
    """
    Helper function in charge of calculating quantiles using SQL's PERCENTILE_CONT
    function (if engine supports it).

    Supported only for Postgres and BigQuery.
    """
    if not (is_postgres(df.engine) or is_bigquery(df.engine)):
        raise Exception('Can only calculate quantiles using PERCENTILE_CONT for Postgres and Bigquery only.')

    quantiles_df = df.copy()
    window = None
    if is_bigquery(df.engine):
        window = quantiles_df.groupby(by=group_by).window(
            start_boundary=None, end_boundary=None,
        ).group_by
    else:
        quantiles_df = df.groupby(group_by)

    quantiles = [q] if isinstance(q, float) else q
    series_to_calculate = _get_valid_series_for_calculation(df)

    q_results = {}
    for qt in quantiles:
        for series_name in series_to_calculate:
            q_series_name = f'__{series_name}_{qt}_quantile'
            series_to_agg = quantiles_df[series_name]

            agg_expr = AggregateFunctionExpression.construct(
                f'percentile_cont({qt}) within group (order by {{}})',
                series_to_agg,
            )
            if is_bigquery(df.engine):
                # mypy: help
                if window is None or not isinstance(window, Window):
                    raise Exception('Invalid window object.')

                if isinstance(series_to_agg, SeriesTimedelta):
                    series_to_agg = series_to_agg.dt.total_seconds

                agg_expr = window.get_window_expression(
                    AggregateFunctionExpression.construct(
                        f'percentile_cont({{}}, {qt})', series_to_agg,
                    )
                )

            q_results[q_series_name] = series_to_agg.copy_override(
                expression=agg_expr,
                name=q_series_name,
            )

    quantiles_df = quantiles_df.copy_override(series=q_results)
    quantiles_df = quantiles_df.materialize(distinct=True)
    quantiles_df = _add_quantiles_as_series(quantiles_df, q)

    final_series = []
    for series_name in series_to_calculate:
        q_series_name = f'{series_name}_quantile'
        quantiles_df[q_series_name] = None
        quantiles_df[q_series_name] = quantiles_df[q_series_name].astype(df[series_name].dtype)
        for qt in quantiles:
            curr_q_series_name = f'__{series_name}_{qt}_quantile'
            mask = quantiles_df[_QUANTILES_SERIES_NAME] == qt

            current_q_series = quantiles_df[curr_q_series_name]

            if is_bigquery(df.engine) and isinstance(df[series_name], SeriesTimedelta):
                # cast back to SeriesTimeDelta
                current_q_series = SeriesTimedelta.from_total_seconds(
                    total_seconds=current_q_series.copy_override_type(SeriesFloat64)
                )

            quantiles_df.loc[mask, q_series_name] = current_q_series

        final_series.append(q_series_name)

    quantiles_df = quantiles_df.set_index(_QUANTILES_SERIES_NAME, append=True)
    return quantiles_df[final_series].materialize(node_name='quantile_calculation')


def _calculate_quantiles_with_linear_interpolation(
    df: DataFrame, q: Union[float, List[float]], group_by: List[str],
) -> DataFrame:
    """
    Helper function that simulates quantile calculation using linear interpolation based
    on method 7 of Hyndman & Fan.
    https://www.amherst.edu/media/view/129116/original/Sample+Quantiles.pdf

    Main reason to use this method is because Numpy's `quantile` and SQL's `percentile_cont` functions are
    based on it. Therefore, the expression generated by this function MUST yield exact results.

    Formula:
    𝑄(𝑝)=(1−𝜸)∗𝑋𝑗+𝜸∗𝑋𝑗+1

    where:
        𝒋  denotes the index of the element in the lowest boundary of the percentile.
        It is the intergal part of the "virtual index" (estimation of the linear interpolation).
        Which is defined as:
            𝒗𝒊𝒓𝒕𝒖𝒂𝒍_𝒊𝒏𝒅𝒆𝒙=𝑝∗𝑁+𝛼+𝑝∗(1−𝛼−𝛽)
            where:
                * p: percentile
                * N: Size of the population
                * 𝛼 = 1 and 𝛽 = 1 (by default, for linear interpolation)

            So, we can simplify it and express it as:
                𝒗𝒊𝒓𝒕𝒖𝒂𝒍_𝒊𝒏𝒅𝒆𝒙 = 𝑝∗𝑁+1+𝑝∗(1−1−1)
                           = 𝑝∗𝑁+1−𝑝
                           = 𝑝∗(𝑁−1)+1
            therefore,
                𝑗 = 𝑓𝑙𝑜𝑜𝑟(𝒗𝒊𝒓𝒕𝒖𝒂𝒍_𝒊𝒏𝒅𝒆𝒙)

        𝜸  is the interpolation parameter. Expressed as the fractional part of the virtual_index:
            𝛾 = 𝒗𝒊𝒓𝒕𝒖𝒂𝒍_𝒊𝒏𝒅𝒆𝒙%1

        𝑋𝑗 : element at position j in the sorted population:
            𝑋={𝑋1,...𝑋𝑗,𝑋𝑗+1,...,𝑋𝑛}

        𝑋𝑗+1 : adjacent element to  𝑋𝑗


    Numpy's Source
    calculation of virtual_index
        https://github.com/numpy/numpy/blob/54c52f13713f3d21795926ca4dbb27e16fada171/numpy/lib/function_base.py#L110

    calculation of gamma,  𝑋𝑗 ,  𝑋𝑗+1
        https://github.com/numpy/numpy/blob/54c52f13713f3d21795926ca4dbb27e16fada171/numpy/lib/function_base.py#L4704-L4713

    calculation of linear interpolation
        https://github.com/numpy/numpy/blob/54c52f13713f3d21795926ca4dbb27e16fada171/numpy/lib/function_base.py#L4513

    Supported only for Athena
    """
    if not is_athena(df.engine):
        raise Exception('Can only calculate quantiles using linear interpolation for Athena only.')

    quantiles_df = df.set_index(group_by, drop=True)

    series_to_calculate = _get_valid_series_for_calculation(df)

    # Step 1. aggregate all values of the numeric series into a sorted ARRAY

    transformed_series = []
    for series_name in series_to_calculate:
        series_to_agg = quantiles_df[series_name]
        current_window = (
            quantiles_df.sort_values(by=series_name).groupby(group_by)
            .window(end_boundary=WindowFrameBoundary.FOLLOWING).group_by
        )

        # mypy: help
        if not isinstance(current_window, Window):
            raise Exception('Invalid window object.')

        agg_expr = current_window.get_window_expression(
            AggregateFunctionExpression.construct('array_agg({})', series_to_agg)
        )

        grouped_series_name = f'__grouped_array_{series_name}'
        size_series_name = f'__size_{series_name}'
        transformed_series += [grouped_series_name, size_series_name]

        quantiles_df[grouped_series_name] = series_to_agg.copy_override(expression=agg_expr)
        quantiles_df[size_series_name] = series_to_agg.count(partition=current_window)

    quantiles_df = quantiles_df[transformed_series]
    quantiles_df = quantiles_df.materialize(distinct=True)

    # Step 2. add quantiles to calculate as const values in df
    quantiles_df = _add_quantiles_as_series(quantiles_df, q)
    quantiles_df = quantiles_df.set_index(_QUANTILES_SERIES_NAME, append=True)

    # Step 3. Calculate quantile based in linear interpolation
    # https://github.com/numpy/numpy/blob/54c52f13713f3d21795926ca4dbb27e16fada171/numpy/lib/function_base.py#L105-L112
    calculated_quantiles = {}
    for series_name in series_to_calculate:
        array_series = quantiles_df[f'__grouped_array_{series_name}']

        n_population = quantiles_df[f'__size_{series_name}']
        # (size of population - 1) * quantile + 1
        virtual_index = (
            (n_population - 1) * quantiles_df.all_series[_QUANTILES_SERIES_NAME] + 1
        )

        # gamma is the fractional part of the virtual_index (virtual_index % 1)
        gamma_series = virtual_index % 1

        # X_j: element located at floor(virtual_index) in the agg array
        X_j_series = gamma_series.copy_override(
            expression=Expression.construct(
                "try({}[cast({} as bigint)])", array_series, virtual_index // 1,
            )
        ).fillna(0.)

        # X_j_next: element after X_j
        X_j_next_series = gamma_series.copy_override(
            expression=Expression.construct(
                "try({}[cast({} as bigint) + 1])", array_series, virtual_index // 1,
            )
        ).fillna(0.)

        # final result
        # X_j + gamma * (X_j_next - X_j)
        result_series = X_j_series + gamma_series * (X_j_next_series - X_j_series)

        q_series_name = f'{series_name}_quantile'
        calculated_quantiles[q_series_name] = result_series.copy_override(name=f'{series_name}_quantile')
        if isinstance(df[series_name], SeriesTimedelta):
            calculated_quantiles[q_series_name] = SeriesTimedelta.from_total_seconds(
                calculated_quantiles[q_series_name].copy_override_type(SeriesFloat64)
            )

    quantiles_df = quantiles_df.copy_override(series=calculated_quantiles)
    return quantiles_df.materialize(node_name='quantile_calculation')


def calculate_quantiles_df(
    df: DataFrame,
    partition: WrappedPartition = None,
    q: Union[float, List[float]] = 0.5,
) -> DataFrame:
    """
    Calculates each requested quantile per each numeric/timedelta series contained in the DataFrame.

    Supports only quantile calculation based on linear interpolation.
    """
    if not _get_valid_series_for_calculation(df):
        raise ValueError('Cannot calculate quantiles, DataFrame has no numeric or timedelta series.')

    partition = partition or df.group_by
    if partition and not isinstance(partition, GroupBy):
        raise ValueError("DataFrame or provided partition is not valid. Expected GroupBy instance.")

    gb = list(partition.index.keys()) if partition else []

    df_cp = df.copy()
    if not gb:
        df_cp = df_cp.reset_index(drop=True)

    # removing current DataFrame's group_by, this way we avoid conflicts with partitioning
    df_cp = df_cp.copy_override(
        series={
            series.name: series.copy_override(group_by=None)
            for series in df_cp.data.values()
        },
        group_by=None
    )
    if not is_athena(df.engine):
        return _calculate_quantiles_with_percentile_cont(df_cp, q, group_by=gb)

    return _calculate_quantiles_with_linear_interpolation(df_cp, q, group_by=gb)
