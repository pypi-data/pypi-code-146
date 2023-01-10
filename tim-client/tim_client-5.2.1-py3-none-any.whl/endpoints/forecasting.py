from array import array
from io import StringIO
import pandas as pd
from typing import Optional, List, Union
from tim.core.api import execute_request
from tim.core.credentials import Credentials
from tim.core.types import(
    ForecastingBuildModel,
    ForecastingUploadModel,
    ForecastingRebuildModel,
    ForecastingRetrainModel,
    ForecastingPredict,
    JobResponse,
    ForecastingJobMetaData,
    ExecuteResponse,
    JobLogs,
    StatusResponse,
    ErrorMeasures,
    ForecastModelResult,
    ForecastTableRequestPayload,
    Id,
    WhatIf,
    WhatIfPanel,
    CopyExperiment,
    ResultsProductionAccuraciesForecasting
    )

class Forecasting:
    def __init__(
        self,
        credentials: Credentials
        ):
        self.credentials = credentials
    
    def build_model(
        self,
        configuration: ForecastingBuildModel
        ) -> JobResponse:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path='/forecast-jobs/build-model',
            body=configuration
            ) 

    def upload_model(
        self,
        configuration: ForecastingUploadModel
        ) -> Id:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path='/forecast-jobs/upload-model',
            body=configuration
            ) 

    def rebuild_model(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingRebuildModel]
        ) -> JobResponse:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path=f'/forecast-jobs/{parent_job_id}/rebuild-model',
            body=configuration
            )

    def retrain_model(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingRetrainModel]
        ) -> JobResponse:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path=f'/forecast-jobs/{parent_job_id}/retrain-model',
            body=configuration
            )

    def predict(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingPredict]
        ) -> JobResponse:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path=f'/forecast-jobs/{parent_job_id}/predict',
            body=configuration
            )

    def rca(
        self,
        parent_job_id: str,
        ) -> Id:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path=f'/forecast-jobs/{parent_job_id}/rca',
            )

    def what_if(
        self,
        parent_job_id: str,
        configuration: Union[WhatIf,WhatIfPanel]
        ) -> JobResponse:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path=f'/forecast-jobs/{parent_job_id}/what-if',
            body=configuration
            )

    def job_list(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        experiment_id: Optional[str] = None,
        use_case_id: Optional[str] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        parent_id: Optional[str] = None,
        from_datetime: Optional[str] = None,
        to_datetime: Optional[str] = None,
        sort: Optional[str] = None,
        sequence_job_id: Optional[str] = None,
        ) -> List[ForecastingJobMetaData]:
        payload = {
            "offset": offset,
            "limit": limit,
            "experimentId": experiment_id,
            "useCaseId": use_case_id,
            "type": type,
            "status": status,
            "parentId": parent_id,
            "from": from_datetime,
            "to": to_datetime,
            "sort": sort,
            "sequenceJobId":sequence_job_id
            }
        return execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs',
            params=payload
            )

    def delete_job_list(
        self,
        experiment_id: Optional[str] = None,
        use_case_id: Optional[str] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        parent_id: Optional[str] = None,
        from_datetime: Optional[str] = None,
        to_datetime: Optional[str] = None,
        ) -> ExecuteResponse:
        payload = {
            "experimentId": experiment_id,
            "useCaseId": use_case_id,
            "type": type,
            "status": status,
            "parentId": parent_id,
            "from": from_datetime,
            "to": to_datetime
            }
        return execute_request(
            credentials=self.credentials,
            method="delete",
            path=f"/forecast-jobs",
            params=payload
            )

    def job_details(
        self,
        id: str
        ) -> ForecastingJobMetaData:
        return execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}'
            )

    def delete_job(
        self,
        id: str
        ) -> ExecuteResponse:
        return execute_request(
            credentials=self.credentials,
            method="delete",
            path=f"/forecast-jobs/{id}"
            )

    def copy_job(
        self,
        id: str,
        configuration: Optional[CopyExperiment] = None
        ) -> Id:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path=f'/forecast-jobs/{id}/copy',
            body=configuration
            )    

    def execute(
        self,
        id: str
        ) -> ExecuteResponse:
        return execute_request(
            credentials=self.credentials,
            method='post',
            path=f'/forecast-jobs/{id}/execute'
            )

    def job_logs(
        self,
        id: str
        ) -> List[JobLogs]:
        return execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}/log'
            )

    def status(
        self,
        id: str
        ) -> StatusResponse:
        return execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}/status'
            )

    def status_collect(
        self,
        id: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        ) -> List[StatusResponse]:
        payload = {
            "offset": offset,
            "limit": limit,
            "sort": sort
            }
        return execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}/status/collect',
            params=payload
            )

    def results_table(
        self,
        id: str,
        forecast_type: Optional[str] = None,
        model_index: Optional[int] = None
        ) -> pd.DataFrame:
        payload = ForecastTableRequestPayload(
            forecastType=forecast_type,
            modelIndex=model_index
            )
        response = execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}/results/table',
            params=payload
            )
        data_string = StringIO(response)
        return pd.read_csv(data_string)  # pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false

    def results_production_forecast(
        self,
        id: str,
        ) -> pd.DataFrame:
        response = execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}/results/production-forecast',
            )
        data_string = StringIO(response)
        return pd.read_csv(data_string) 

    def results_model(
        self,
        id: str
        ) -> ForecastModelResult:
        return execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}/results/model'
            )

    def results_accuracies(
        self,
        id: str
        ) -> ErrorMeasures:
        return execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}/results/accuracies'
            )

    def results_rca(
        self,
        id: str,
        index_of_model: int,
        timestamp: Optional[str] = None,
        radius: Optional[int] = None,
        ) -> pd.DataFrame:
        payload = {
        "indexOfModel": index_of_model,
        "timestamp": timestamp,
        "radius": radius
        }
        response = execute_request(
            credentials=self.credentials,
            method='get',
            path=f'/forecast-jobs/{id}/results/rca',
            params=payload
            )
        data_string = StringIO(response.replace("â\x89¤","<="))
        return pd.read_csv(data_string)

    def results_production_table(
        self,
        sequence_job_id : str,
        dataset_version_id: Optional[str] = None,
        type: Optional[array] = None,
        from_datetime: Optional[str] = None,
        to_datetime: Optional[str] = None,
        allow_overlapping: Optional[bool] = None,
        colocated_jobs: Optional[bool] = None,
        ) -> pd.DataFrame:
        payload = {
        "sequenceJobId": sequence_job_id,
        "datasetVersionId": dataset_version_id,
        "type": type,
        "from": from_datetime,
        "to": to_datetime,
        "allowOverlapping": allow_overlapping,
        "colocatedJobs": colocated_jobs
        }
        response = execute_request(
            credentials=self.credentials,
            method='get',
            path='/forecast-jobs/results/production-table',
            params=payload
            )
        data_string = StringIO(response)
        return pd.read_csv(data_string) 

    def results_production_accuracies(
        self,
        sequence_job_id : str,
        dataset_version_id: Optional[str] = None,
        type: Optional[array] = None,
        from_datetime: Optional[str] = None,
        to_datetime: Optional[str] = None,
        allow_overlapping: Optional[bool] = None,
        colocated_jobs: Optional[bool] = None,
        individual_accuracies: Optional[bool] = None,
        ) -> ResultsProductionAccuraciesForecasting:
        payload = {
        "sequenceJobId": sequence_job_id,
        "datasetVersionId": dataset_version_id,
        "type": type,
        "from": from_datetime,
        "to": to_datetime,
        "allowOverlapping": allow_overlapping,
        "colocatedJobs": colocated_jobs,
        "individualAccuracies": individual_accuracies
        }
        return execute_request(
            credentials=self.credentials,
            method='get',
            path='/forecast-jobs/results/production-accuracies',
            params=payload
            )