from typing import Optional

import pandas as pd

from ... import api
from .. import _dtos
from .. import utils

__all__ = ["get_single_obs_time_data", "get_single_obs_batch_data"]


def get_single_obs_time_data(
    model_execution: Optional[_dtos.ModelExecution] = None,
    rename_data_to_source_code_name: bool = True,
    api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
):
    # Get model execution from environment if not specified
    if model_execution is None:
        model_execution = _dtos.get_default_model_execution()
        if model_execution.pythonModelInstance.dataExchangeMode != "SINGLE_OBSERVATION":
            raise ValueError("The execution has to be in single observation mode")
        if model_execution.pythonModelInstance.singleObservationContext.type != "time":
            raise ValueError(
                "The execution has to be in single observation mode on time data"
            )

    # Start date
    start_date = (
        model_execution.lastSuccessfulExecutionInstant
        - model_execution.pythonModelInstance.singleObservationContext.overlappingPeriod
    )

    # End date
    end_date = model_execution.currentExecutionInstant

    # Aggregation
    if (
        model_execution.pythonModelInstance.singleObservationContext.aggregationPeriod
        == "PT0S"
    ):
        aggregation = "RAW_VALUES"
    else:
        aggregation = "TIME"

    # Aggregation period
    if aggregation == "RAW_VALUES":
        aggregation_period = None
    else:
        aggregation_period = (
            model_execution.pythonModelInstance.singleObservationContext.aggregationPeriod
        )

    # Aggregation function
    if aggregation == "RAW_VALUES":
        aggregation_function = None
    else:
        aggregation_function = [
            input_data.aggregationFunction
            for input_data in model_execution.get_data_input_dict(
                data_type="any", mode="object"
            ).values()
        ]

    # Get data references' dict(sourceCode: ref) for all data
    input_data_references = model_execution.get_data_input_dict(
        data_type="any", mode="reference"
    )

    # renaming dict(ref: sourceCode) for all data
    input_renaming_dict = utils.reverse_dict(input_data_references)

    # Get data references' dict(sourceCode: ref) of scalar data
    input_scalar_data_references = model_execution.get_data_input_dict(
        data_type="any", values_type="scalar", mode="reference"
    )

    # Get units of scalar data
    scalar_input_unit_ids = [
        input_data.unit.id
        for input_data in model_execution.get_data_input_dict(
            data_type="any", values_type="scalar", mode="object"
        ).values()
    ]

    # Query endpoint
    data = api.get_multiple_data_values(
        start_date=start_date,
        end_date=end_date,
        aggregation=aggregation,
        data_id=None,
        data_reference=input_scalar_data_references.values(),
        number_of_values=None,
        aggregation_period=aggregation_period,
        aggregation_function=aggregation_function,
        unit_id=scalar_input_unit_ids,
        unit_label=None,
        name_data_from="reference",
        append_unit_to_description=False,
        join_series_on="timestamp",
        api_credentials=api_credentials,
    )

    # initialise list of DataFrames and Series to be concatenated
    dfs_list = [data]

    for input_data in model_execution.get_data_input_dict(
        data_type="time", values_type="vector", mode="object"
    ).values():
        vector_data = api.get_vector_time_values(
            vector_data_id=input_data.id,
            start_date=start_date,
            end_date=end_date,
            aggregation=aggregation,
            index_aggregation="RAW_VALUES",
            aggregation_period=aggregation_period,
            max_number_of_points=None,
            aggregation_function=aggregation_function,
            index_aggregation_function=None,
            index_aggregation_step_type=None,
            index_aggregation_step_value=None,
            min_index=None,
            max_index=None,
            index_unit_id=input_data.indexUnit.id,
            value_unit_id=input_data.valueUnit.id,
        )
        # vector data is converted to a list of series
        ser_list = [
            pd.Series(data=vector_data.loc[index]) for index in vector_data.index
        ]
        # list of series is converted to a series
        ser_vector_data = pd.Series(
            data=ser_list, index=vector_data.index, name=input_data.reference,
        )
        # Series of Series in added to the list of DataFrames for a later concatenation
        dfs_list.append(ser_vector_data)

    # list containing DataFrame and Series is concatenated
    data = pd.concat(dfs_list, axis=1)

    # Rename data
    if rename_data_to_source_code_name is True:
        data = data.rename(columns=input_renaming_dict)

    # Output
    return data


def get_single_obs_batch_data(
    model_execution: Optional[_dtos.ModelExecution] = None,
    rename_data_to_source_code_name: bool = True,
    api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
):
    # Get variables from environment if not specified
    if model_execution is None:
        model_execution = _dtos.get_default_model_execution()
        if model_execution.pythonModelInstance.dataExchangeMode != "SINGLE_OBSERVATION":
            raise ValueError("The execution has to be in single observation mode")
        if model_execution.pythonModelInstance.singleObservationContext.type != "batch":
            raise ValueError(
                "The execution has to be in single observation mode on batches"
            )

    # Start date
    start_date = (
        model_execution.lastSuccessfulExecutionInstant
        - model_execution.pythonModelInstance.singleObservationContext.overlappingPeriod
    )

    # End date
    end_date = model_execution.currentExecutionInstant

    # Batch type
    batch_type_id = (
        model_execution.pythonModelInstance.singleObservationContext.batchPredicate.batchType.id
    )

    # Batch feature filters
    features_value_ids = [
        feature.id
        for feature in model_execution.pythonModelInstance.singleObservationContext.batchPredicate.featureFilters
    ]

    # Get data references' dict(sourceCode: ref) for batch data (scalar and vector)
    input_data_references = model_execution.get_data_input_dict(
        data_type="batch", mode="reference"
    )

    # renaming dict(ref: sourceCode) for batch data (scalar and vector)
    input_renaming_dict = utils.reverse_dict(input_data_references)

    # Get data references' dict(sourceCode: ref) for batch scalar data
    input_scalar_data_references = model_execution.get_data_input_dict(
        data_type="batch", values_type="scalar", mode="reference"
    )

    # Get units of batch scalar data
    scalar_input_unit_ids = [
        input_data.unit.id
        for input_data in model_execution.get_data_input_dict(
            data_type="batch", values_type="scalar", mode="object"
        ).values()
    ]

    # Query endpoint for data
    data = None

    if len(model_execution.get_data_input_dict()) > 0:
        data = api.get_multiple_data_values(
            start_date=start_date,
            end_date=end_date,
            aggregation="RAW_VALUES",
            data_reference=input_scalar_data_references.values(),
            unit_id=scalar_input_unit_ids,
            name_data_from="reference",
            append_unit_to_description=False,
            join_series_on="index",
            api_credentials=api_credentials,
        )

    # Query endpoint for features & batch predicate
    features = api.get_batches(
        batch_type_id=batch_type_id,
        start_date=start_date,
        end_date=end_date,
        features_value_ids=features_value_ids,
        api_credentials=api_credentials,
    )[1]

    # Rename features
    features_renaming_dict = utils.reverse_dict(
        model_execution.get_input_dict(input_types=["BATCH_TAG_KEY"], mode="reference")
    )

    features = features[
        [col for col in features.columns if col in features_renaming_dict.keys()]
    ]

    if rename_data_to_source_code_name is True:
        features = features.rename(columns=features_renaming_dict)

    if data is None:
        data = features
    else:
        data = data.join(features, how="right")

    # initialise list of DataFrames and Series to be concatenated
    dfs_list = [data]

    for input_data in model_execution.get_data_input_dict(
        data_type="batch", values_type="vector", mode="object"
    ).values():
        vector_data = api.get_vector_batch_values(
            vector_data_id=input_data.id,
            start_date=start_date,
            end_date=end_date,
            index_unit_id=input_data.indexUnit.id,
            value_unit_id=input_data.valueUnit.id,
            aggregation="RAW_VALUES",
            index_aggregation="RAW_VALUES",
            aggregation_period="PT0S",
            max_number_of_points=None,
            aggregation_function=None,
            index_aggregation_function=None,
            index_aggregation_step_type=None,
            index_aggregation_step_value=None,
            min_index=None,
            max_index=None,
            batch_ids=None,
        )
        # vector data is converted to a list of series
        ser_list = [
            pd.Series(data=vector_data.loc[index]) for index in vector_data.index
        ]
        # list of series is converted to a series
        ser_vector_data = pd.Series(
            data=ser_list, index=vector_data.index, name=input_data.reference,
        )
        # series of series in added to the list of DataFrames for a later concatenation
        dfs_list.append(ser_vector_data)

    # list containing 'data' with scalar values and the series with vector values is concatenated
    data = pd.concat(dfs_list, axis=1)

    # Rename data
    if rename_data_to_source_code_name is True:
        data = data.rename(columns=input_renaming_dict)

    # Output
    return data
