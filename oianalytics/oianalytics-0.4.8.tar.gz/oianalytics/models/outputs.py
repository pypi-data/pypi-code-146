from typing import Union, Optional, List
import io
import time

import pandas as pd

from .. import api
from ._dtos import (
    get_default_model_execution,
    get_default_execution_report,
    ExecutionReport,
    CustomModelOutput,
)

__all__ = [
    "FileOutput",
    "TimeValuesOutput",
    "VectorTimeValuesOutput",
    "Delay",
    "BatchValuesOutput",
    "VectorBatchValuesOutput",
    "BatchFeaturesOutput",
    "CustomTextOutput",
    "CustomJsonOutput",
    "OIModelOutputs",
]


# Output classes
class FileOutput:
    def __init__(self, file_name: str, content: Union[io.StringIO, io.BytesIO]):
        self.output_type = "file"
        self.file_name = file_name
        self.content = content

    @classmethod
    def from_pandas(
        cls,
        data: Union[pd.Series, pd.DataFrame],
        file_name: str,
        file_type: str = "csv",
        writing_kwargs: Optional[dict] = None,
    ):
        # Init
        if writing_kwargs is None:
            writing_kwargs = {}

        bio = io.BytesIO()

        # Write data
        if file_type == "excel":
            data.to_excel(bio, **writing_kwargs)
        elif file_type == "csv":
            data.to_csv(bio, **writing_kwargs)
        else:
            raise NotImplementedError(f"Unsupported file_type: {file_type}")
        bio.seek(0)

        # Create object
        return cls(file_name=file_name, content=bio)

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # get execution report
        if execution_report is None:
            execution_report = get_default_execution_report()
        # update execution report
        execution_report.update(files_uploaded=1)

        return api.endpoints.files.upload_file(
            file_content=self.content,
            file_name=self.file_name,
            api_credentials=api_credentials,
        )


class TimeValuesOutput:
    def __init__(
        self,
        data: Union[pd.Series, pd.DataFrame],
        units: Optional[dict] = None,
        rename_data: bool = True,
        use_external_reference: bool = False,
        timestamp_index_name: str = "timestamp",
    ):
        self.output_type = "time_values"

        # Rename data if specified
        data_df = data.to_frame() if isinstance(data, pd.Series) else data

        if rename_data is True:
            model_exec = get_default_model_execution()
            if model_exec is None:
                raise ValueError(
                    "Data can't be renamed without a current model_exec set globally"
                )

            output_dict = model_exec.get_data_output_dict(
                data_type="any", values_type="scalar", mode="reference"
            )
            self.data = data_df.rename(columns=output_dict)
        else:
            self.data = data_df

        # Specify units
        if units is None:
            model_exec = get_default_model_execution()
            if model_exec is not None:
                self.units = {
                    output_data.reference: output_data.unit.label
                    for output_data in model_exec.get_data_output_dict(
                        data_type="any", values_type="scalar", mode="object"
                    ).values()
                }
            else:
                self.units = units
        else:
            self.units = units

        self.use_external_reference = use_external_reference

        self.timestamp_index_name = timestamp_index_name

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # send data
        response = api.insert_time_values(
            data=self.data,
            units=self.units,
            use_external_reference=self.use_external_reference,
            timestamp_index_name=self.timestamp_index_name,
            api_credentials=api_credentials,
        )
        # get execution report
        if execution_report is None:
            execution_report = get_default_execution_report()
        # update execution report
        execution_report.update(
            time_values_updated=response.get("numberOfValuesSuccessfullyInserted", 0),
            errors=len(response.get("errors", [])),
        )
        return response


class VectorTimeValuesOutput:
    def __init__(
        self,
        data: List[pd.DataFrame],
        data_reference: List[str],
        rename_data: bool = True,
        values_units: Optional[dict[str, str]] = None,
        index_units: Optional[dict[str, str]] = None,
        use_external_reference: bool = False,
        timestamp_index_name: str = "timestamp",
    ):
        self.output_type = "time_vector_values"

        if rename_data is True:
            model_exec = get_default_model_execution()
            if model_exec is None:
                raise ValueError(
                    "Data can't be renamed without a current model_exec set globally"
                )

            output_dict = model_exec.get_data_output_dict(
                data_type="time", values_type="vector", mode="reference"
            )
            data_reference = [
                output_dict[source_code_name] for source_code_name in data_reference
            ]

        self.data_reference = data_reference
        self.data = data

        # Specify values units
        if values_units is None:
            model_exec = get_default_model_execution()
            if model_exec is not None:
                self.values_units = {
                    output_data.reference: output_data.valueUnit.label
                    for output_data in model_exec.get_data_output_dict(
                        data_type="time", values_type="vector", mode="object"
                    ).values()
                    if output_data.reference in data_reference
                }
            else:
                self.values_units = values_units
        else:
            self.values_units = values_units

        # Specify index unit
        if index_units is None:
            model_exec = get_default_model_execution()
            if model_exec is not None:
                self.index_units = {
                    output_data.reference: output_data.indexUnit.label
                    for output_data in model_exec.get_data_output_dict(
                        data_type="time", values_type="vector", mode="object"
                    ).values()
                    if output_data.reference in data_reference
                }
            else:
                self.index_units = index_units
        else:
            self.index_units = index_units

        self.use_external_reference = use_external_reference

        self.timestamp_index_name = timestamp_index_name

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # send data
        response = api.insert_vector_time_values(
            data=self.data,
            data_reference=self.data_reference,
            index_units=self.index_units,
            values_units=self.values_units,
            use_external_reference=self.use_external_reference,
            timestamp_index_name=self.timestamp_index_name,
            api_credentials=api_credentials,
        )
        # get execution report
        if execution_report is None:
            execution_report = get_default_execution_report()
        # update execution report
        execution_report.update(
            errors=len(response.get("errors", [])),
            time_vector_values_updated=response.get(
                "numberOfValuesSuccessfullyInserted", 0
            ),
        )
        return response


class BatchValuesOutput:
    def __init__(
        self,
        batch_type_id: str,
        data: Union[pd.Series, pd.DataFrame],
        units: Optional[dict] = None,
        batch_id_index_name: str = "batch_id",
        rename_data: bool = True,
    ):
        self.output_type = "batch_values"
        self.batch_type_id = batch_type_id

        # Rename data if specified
        data_df = data.to_frame() if isinstance(data, pd.Series) else data

        if rename_data is True:
            model_exec = get_default_model_execution()
            if model_exec is None:
                raise ValueError(
                    "Data can't be renamed without a current model_exec set globally"
                )

            output_dict = model_exec.get_data_output_dict(
                data_type="batch", values_type="scalar", mode="id"
            )
            self.data = data_df.rename(columns=output_dict)
        else:
            self.data = data_df

        # Specify units
        if units is None:
            model_exec = get_default_model_execution()
            if model_exec is not None:
                self.units = {
                    output_data.reference: output_data.unit.id
                    for output_data in model_exec.get_data_output_dict(
                        data_type="batch", values_type="scalar", mode="object"
                    ).values()
                }
            else:
                self.units = None
        else:
            self.units = units

        self.batch_id_index_name = batch_id_index_name

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # get execution report
        if execution_report is None:
            execution_report = get_default_execution_report()
        try:
            # send data
            response = api.update_batch_features_and_values(
                batch_type_id=self.batch_type_id,
                data=self.data,
                unit_ids=self.units,
                batch_id_index_name=self.batch_id_index_name,
                api_credentials=api_credentials,
            )

            # update execution report
            execution_report.update(batch_values_updated=int(self.data.count().sum()))
            return response
        except Exception:
            execution_report.update(errors=1)


class VectorBatchValuesOutput:
    def __init__(
        self,
        data: List[pd.DataFrame],
        data_reference: List[str],
        values_units: Optional[dict[str, str]] = None,
        index_units: Optional[dict[str, str]] = None,
        batch_id_index_name: str = "batch_id",
        rename_data: bool = True,
    ):
        self.output_type = "batch_vector_values"

        if rename_data is True:
            model_exec = get_default_model_execution()
            if model_exec is None:
                raise ValueError(
                    "Data can't be renamed without a current model_exec set globally"
                )

            output_dict = model_exec.get_data_output_dict(
                data_type="batch", values_type="vector", mode="reference"
            )
            data_reference = [
                output_dict[source_code_name] for source_code_name in data_reference
            ]

        self.data_reference = data_reference
        self.data = data

        # Specify units
        if values_units is None:
            model_exec = get_default_model_execution()
            if model_exec is not None:
                self.values_units = {
                    output_data.reference: output_data.valueUnit.label
                    for output_data in model_exec.get_data_output_dict(
                        data_type="batch", values_type="vector", mode="object"
                    ).values()
                    if output_data.reference in data_reference
                }
        else:
            self.values_units = values_units

        # Specify units
        if index_units is None:
            model_exec = get_default_model_execution()
            if model_exec is not None:
                self.index_units = {
                    output_data.reference: output_data.indexUnit.label
                    for output_data in model_exec.get_data_output_dict(
                        data_type="batch", values_type="vector", mode="object"
                    ).values()
                    if output_data.reference in data_reference
                }
        else:
            self.index_units = index_units

        self.batch_id_index_name = batch_id_index_name

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # send data
        response = api.update_vector_batch_values(
            data=self.data,
            data_reference=self.data_reference,
            index_units=self.index_units,
            values_units=self.values_units,
            batch_id_index_name=self.batch_id_index_name,
            api_credentials=api_credentials,
        )
        # get execution report
        if execution_report is None:
            execution_report = get_default_execution_report()
        # update execution report
        execution_report.update(
            errors=len(response.get("errors", [])),
            batch_vector_values_updated=response.get(
                "numberOfValuesSuccessfullyInserted", 0
            ),
        )
        return response


class BatchFeaturesOutput:
    def __init__(
        self,
        batch_type_id: str,
        data: Union[pd.Series, pd.DataFrame],
        rename_features: bool = True,
        batch_id_index_name: str = "batch_id",
    ):
        self.output_type = "batch_features"
        self.batch_type_id = batch_type_id

        # Rename data if specified
        data_df = data.to_frame() if isinstance(data, pd.Series) else data

        if rename_features is True:
            model_exec = get_default_model_execution()
            if model_exec is None:
                raise ValueError(
                    "Features can't be renamed without a current model_exec set globally"
                )

            output_dict = model_exec.get_data_output_dict(
                data_type="batch", values_type="scalar", mode="id"
            )
            self.data = data_df.rename(columns=output_dict)
        else:
            self.data = data_df

        self.batch_id_index_name = batch_id_index_name

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # update execution report
        if execution_report is None:
            execution_report = get_default_execution_report()

        # send data
        try:
            response = api.update_batch_features_and_values(
                batch_type_id=self.batch_type_id,
                data=self.data,
                feature_columns=list(self.data.columns),
                batch_id_index_name=self.batch_id_index_name,
                api_credentials=api_credentials,
            )

            # update execution report
            execution_report.update(batch_tags_updated=int(self.data.count().sum()))
            return response
        except Exception:
            execution_report.update(errors=1)


class Delay:
    def __init__(self, duration=5):
        self.output_type = "delay"
        self.duration = duration

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # update execution report
        if execution_report is None:
            execution_report = get_default_execution_report()

        time.sleep(self.duration)


class CustomTextOutput:
    def __init__(self, content: str):
        self.type = "text"
        self.content = content

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # Get the default execution report if not provided
        if execution_report is None:
            execution_report = get_default_execution_report()

        # Update the execution report
        execution_report.customOutput = CustomModelOutput(
            type=self.type, content=self.content
        )


class CustomJsonOutput:
    def __init__(self, content):
        self.type = "json"
        self.content = content

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        # Get the default execution report if not provided
        if execution_report is None:
            execution_report = get_default_execution_report()

        # Update the execution report
        execution_report.customOutput = CustomModelOutput(
            type=self.type, content=self.content
        )


class OIModelOutputs:
    def __init__(self):
        self.output_type = "outputs_queue"
        self.model_outputs = []

    def add_output(
        self,
        output_object: Union[
            FileOutput,
            TimeValuesOutput,
            BatchValuesOutput,
            VectorTimeValuesOutput,
            VectorBatchValuesOutput,
            Delay,
            CustomTextOutput,
            CustomJsonOutput,
        ],
    ):
        self.model_outputs.append(output_object)

    def send_to_oianalytics(
        self,
        api_credentials: Optional[api.OIAnalyticsAPICredentials] = None,
        execution_report: Optional[ExecutionReport] = None,
    ):
        for model_output in self.model_outputs:
            model_output.send_to_oianalytics(
                api_credentials=api_credentials, execution_report=execution_report
            )
