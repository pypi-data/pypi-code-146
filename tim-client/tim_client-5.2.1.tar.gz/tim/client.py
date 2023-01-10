from time import sleep
from typing import Union, Callable, Optional, List
from pandas import DataFrame
from datetime import datetime
from tim.core.server import server
from tim.core.credentials import Credentials
from tim.core.helper import postProcess
from tim.endpoints import (
  Licenses,
  UserGroups,
  Workspaces,
  UseCases,
  Experiments,
  Datasets,
  Forecasting,
  Detection,
  Telemetry,
)
from tim.core.types import (
  UploadDatasetConfiguration,
  DatasetStatusResponse,
  DatasetCreated,
  UploadDatasetResponse,
  Status,
  UpdateDatasetConfiguration,
  DatasetVersion,
  DatasetOutputs,
  StatusResponse,
  ForecastingBuildModel,
  JobExecuteResponse,
  JobResponse,
  ForecastingResultsOptions,
  ForecastingResultsOutputs,
  Id,
  UseCasePost,
  ForecastingRebuildModel,
  ForecastingRetrainModel,
  ForecastingPredict,
  ForecastingResultsRCAOptions,
  RCAResults,
  ForecastingRCAOutput,
  WhatIf,
  WhatIfPanel,
  QuickForecast,
  DetectionResultsOptions,
  DetectionResultsOutputs,
  DetectionBuildKPIModel,
  DetectionBuildSystemModel,
  DetectionRebuildKPIModel,
  DetectionDetect,
  DetectionResultsRCAOptions,
  DetectionRCAOutput
)

class Tim:

  def __init__(
      self,
      email: str,
      password: str,
      server: str = server,
      client_name: str = "Python Client",
  ):
    self.__credentials = Credentials(email, password, server, client_name)
    self.licenses = Licenses(self.__credentials)
    self.user_groups = UserGroups(self.__credentials)
    self.workspaces = Workspaces(self.__credentials)
    self.use_cases = UseCases(self.__credentials)
    self.experiments = Experiments(self.__credentials)
    self.datasets = Datasets(self.__credentials)
    self.forecasting = Forecasting(self.__credentials)
    self.detection = Detection(self.__credentials)
    self.telemetry = Telemetry(self.__credentials)
    self.post_process = postProcess()

    
# -------------------------------- Datasets --------------------------------

  def poll_dataset_version_status(
    self,
    id: str,
    version_id: str,
    status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
    tries_left: int = 300
    ) -> DatasetStatusResponse:
    """Poll for the status and progress of the dataset upload or dataset version update.

    Parameters
    ----------
    id : str
      The ID of a dataset in the TIM repository.
    version_id : str
      The ID of a dataset version in the TIM repository of the dataset above.
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the dataset version.
    tries_left : int
      Number of iterations the function will loop to fetch the dataset version status before sending a timeout error.

    Returns
    -------
    status : Dict
      Available keys: createdAt (str), status (str) and progress (int)
    """
    if tries_left < 1:
        raise ValueError("Timeout error.")
    response = self.datasets.status_dataset_version(id, version_id)
    if status_poll: status_poll(response)
    if Status(response['status']).value == Status.FAILED.value:  # pyright: reportUnnecessaryComparison=false
      return response
    if Status(response['status']).value != Status.FINISHED.value and Status(response['status']).value != Status.FINISHED_WITH_WARNING.value:
      sleep(2)
      return Tim.poll_dataset_version_status(
        self,
        id,
        version_id,
        status_poll,
        tries_left - 1
        )
    return response

  def upload_dataset(
    self,
    dataset: DataFrame,
    configuration: UploadDatasetConfiguration = UploadDatasetConfiguration(),
    wait_to_finish: bool = True,
    outputs: List[DatasetOutputs] = [
      'response',
      'logs',
      'details',
    ],
    status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
    tries_left: int = 300
    ) -> Union[DatasetCreated, UploadDatasetResponse]:
    """Upload a dataset to the TIM repository.

      Parameters
      ----------
      dataset : DataFrame
        The dataset containing time-series data.
      configuration : Dict, Optional
        Metadata of the dataset
        Available keys are: 
        timestampFormat, timestampColumn, decimalSeparator, csvSeparator, timeZone,
        timeZoneName, groupKeys, name, description, samplingPeriod and workspace.
        The value of samplingPeriod is a Dict containing the keys baseUnit and value.
      wait_to_finish : bool, Optional
        Wait for the dataset to be uploaded before returning.
        If set to False, the function will return once the dataset upload process has started.
      status_poll : Callable, Optional
        A callback function to poll for the status and progress of the dataset upload.
      tries_left : int
        Number of iterations the function will loop to fetch the dataset version status before sending a timeout error.

      Returns
      -------
      response : Dict
      details : Dict | None
        Dict when successful; None when unsuccessful
      logs : list of Dict
      """
    response = self.datasets.upload_dataset(dataset, configuration)
    if wait_to_finish is False: return response
    dataset_id = response['id']
    version_id = response['version']['id']
    status_result = Tim.poll_dataset_version_status(
        self,
        id=dataset_id,
        version_id=version_id,
        status_poll=status_poll,
        tries_left=tries_left
        )
    if Status(status_result['status']).value != Status.FAILED.value:
      details = self.datasets.details_dataset(dataset_id) if 'details' in outputs else None
    else:
      details = None
    logs = self.datasets.dataset_logs(dataset_id) if 'logs' in outputs else None
    return UploadDatasetResponse(response,details,logs)

  def update_dataset(
    self,
    dataset_id: str,
    dataset_version: DataFrame,
    configuration: UpdateDatasetConfiguration = UpdateDatasetConfiguration(),
    wait_to_finish: bool = True,
    outputs: List[DatasetOutputs] = [
    'response',
    'logs',
    'details',
    ],
    status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
    tries_left: int = 300
    ) -> Union[DatasetVersion, UploadDatasetResponse]:
    """Update a dataset in the TIM repository.

      Parameters
      ----------
      dataset_id : str
        The ID of a dataset in the TIM repository.
      dataset : DataFrame
        The dataset containing time-series data.
      configuration : Dict, Optional
        Metadata of the dataset version
        Available keys are: 
        timestampFormat, timestampColumn, decimalSeparator, csvSeparator.
      wait_to_finish : bool, Optional
        Wait for the dataset to be updated before returning.
        If set to False, the function will return once the dataset update process has started.
      status_poll : Callable, Optional
        A callback function to poll for the status and progress of the dataset update.
      tries_left : int
        Number of iterations the function will loop to fetch the dataset version status before sending a timeout error.

      Returns
      -------
      response : Dict
      details : Dict | None
        Dict when successful; None when unsuccessful
      logs : list of Dict
      """
    response = self.datasets.update_dataset(dataset_id,dataset_version,configuration)
    if wait_to_finish is False: return response
    status_result = Tim.poll_dataset_version_status(
        self,
        id=dataset_id,
        version_id=response['version']['id'],
        status_poll=status_poll,
        tries_left=tries_left
        )
    if Status(status_result['status']).value != Status.FAILED.value:
      details = self.datasets.details_dataset(dataset_id) if 'details' in outputs else None
    else:
      details = None
    details = self.datasets.details_dataset(dataset_id) if 'details' in outputs else None
    logs = self.datasets.dataset_logs(dataset_id) if 'logs' in outputs else None
    return UploadDatasetResponse(response,details,logs)

# -------------------------------- Forecasting --------------------------------
  
  def poll_forecast_status(
    self,
    id: str,
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    ) -> StatusResponse:
    """Poll for the status and progress of a forecasting job.

    Parameters
    ----------
    id : str
      The ID of a forecasting job in the TIM repository.
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the job.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    status : Dict
      Available keys: createdAt (str), status (str), progress (float), memory (int) and CPU (int).
    """
    if tries_left < 1:
      raise ValueError("Timeout error.")
    response = self.forecasting.status(id)
    if status_poll: status_poll(response)
    if Status(response['status']).value == Status.FAILED.value:
      return response
    if Status(response['status']).value != Status.FINISHED.value and Status(response['status']).value != Status.FINISHED_WITH_WARNING.value:
      sleep(2)
      return Tim.poll_forecast_status(
        self,
        id,
        status_poll,
        tries_left - 1
        )
    return response

  def forecasting_job_results(
    self,
    id: str,
    outputs: List[ForecastingResultsOptions] = [
      'id',
      'details',
      'logs',
      'status',
      'table',
      'production_forecast',
      'model',
      'accuracies',
      'production_table',
      'production_accuracies'
      ]
    ) -> ForecastingResultsOutputs:
    """Retrieve the results of a forecast job. You can choose which outputs you want to return by specifying the outputs.
       By default all possible outputs are returned.

    Parameters
    ----------
    id : str
      The ID of a forecast job.
    outputs : array | 
      Possible outputs are ['id','details','logs','status','table','production_forecast'
                            ,'model','accuracies','production_table','production_accuracies']
    Returns
    -------
    id : str | None
      The ID of a forecast job for tracing.
    details : Dict | None
      Metadata of the forecasting job.
    logs : list of Dict | None
      Log messages of the forecasting job.
    status : Dict | None
      Final status of the forecasting job.
    table : DataFrame | None
      Table result containing all predicted values.
    production_forecast : DataFrame | None
      Table result containing only the production forecast.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
    production_table : DataFrame | None
      Table result containing the predicted values of a sequence.
    production_accuracies : Dict | None
      Accuracy metrics calculated by TIM on predicted values of a sequence.
    """
    details = self.forecasting.job_details(id) if 'details' in outputs else None
    logs = self.forecasting.job_logs(id) if 'logs' in outputs else None
    status = self.forecasting.status(id) if 'status' in outputs else None
    table = self.forecasting.results_table(id) if 'table' in outputs else None
    production_forecast = self.forecasting.results_production_forecast(id) if 'production_forecast' in outputs else None
    if 'model' in outputs:
      model = self.forecasting.results_model(id) 
      if model == {}:
        job_details = self.forecasting.job_details(id)
        parent_job_id = job_details['parentJob']['id']
        model = self.forecasting.results_model(parent_job_id) 
    else:
      model = None
    accuracies = self.forecasting.results_accuracies(id) if 'accuracies' in outputs else None
    production_table = self.forecasting.results_production_table(id) if 'production_table' in outputs else None
    production_accuracies = self.forecasting.results_production_accuracies(id) if 'production_accuracies' in outputs else None
    return ForecastingResultsOutputs(
      id = id,
      details = details,
      logs = logs,
      status = status,
      table = table,
      production_forecast = production_forecast,
      model = model,
      accuracies = accuracies,
      production_table = production_table,
      production_accuracies = production_accuracies
    )

  def execute_forecast_job(
    self,
    id: str,
    wait_to_finish: bool = True,
    outputs: List[ForecastingResultsOptions] = None,
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    ) -> Union[JobExecuteResponse,ForecastingResultsOutputs]:
    """Execute a forecast job. You can choose which outputs you want to return by specifying the outputs.
       By default none are returned.

    Parameters
    ----------
    id : str
      The ID of a forecast job to execute.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning.
      If set to False, the function will return once the job has started the execution process.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','production_forecast'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    ForecastingResultsOutputs ->
    id : str | None
      The ID of a forecast job for tracing.
    details : Dict | None
      Metadata of the forecasting job.
    logs : list of Dict | None
      Log messages of the forecasting job.
    status : Dict | None
      Final status of the forecasting job.
    table : DataFrame | None
      Table result containing all predicted values.
    production_forecast : DataFrame | None
      Table result containing only the production forecast.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
    production_table : DataFrame | None
      Table result containing the predicted values of a sequence.
    production_accuracies : Dict | None
      Accuracy metrics calculated by TIM on predicted values of a sequence.
    """
    response = self.forecasting.execute(id)
    if wait_to_finish is False: 
      return JobExecuteResponse(
        id=id,
        response=response,
        status='Queued'
        )
    status = Tim.poll_forecast_status(
      self,
      id=id,
      status_poll=status_poll,
      tries_left=tries_left
      )
    if outputs is None: 
      return JobExecuteResponse(
        id=id,
        response=response,
        status=status
        )
    return Tim.forecasting_job_results(
      self,
      id=id,
      outputs=outputs
      )

  def forecasting_build_model(
    self,
    configuration: ForecastingBuildModel,
    dataset_id: str = None,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[ForecastingResultsOptions] = [
      'id',
      'logs',
      'status',
      'table',
      'model',
      'accuracies',
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None, 
    tries_left: int = 300
    ) -> Union[JobResponse,JobExecuteResponse,ForecastingResultsOutputs]:
    """ Register, execute and collect results of a forecasting build model job.
        The build model job makes a new forecasting model based on a dataset id and configuration.
        You can choose to only register the job and return a forecasting job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','logs','status','table','model','accuracies']

    Parameters
    ----------
    configuration : ForecastingBuildModel
      TIM Engine model building and forecasting configuration.
    dataset_id : str
      The ID of a dataset in the TIM repository.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','production_forecast'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    ForecastingResultsOutputs ->
    id : str | None
      The ID of a forecast job.
    details : Dict | None
      Metadata of the forecasting job.
    logs : list of Dict | None
      Log messages of the forecasting job.
    status : Dict | None
      Final status of the forecasting job.
    table : DataFrame | None
      Table result containing all predicted values.
    production_forecast : DataFrame | None
      Table result containing only the production forecast.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
    production_table : DataFrame | None
      Table result containing the predicted values of a sequence.
    production_accuracies : Dict | None
      Accuracy metrics calculated by TIM on predicted values of a sequence.
    """
    try:
      configuration['useCase']['id']
      job_configuration = ForecastingBuildModel(**configuration)
    except:
      if dataset_id is None: raise ValueError("'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'")
      try:
        use_case_name = configuration['name']
      except:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        use_case_name = f'Quick Forecast - {dt_string}'
      dataset_details = self.datasets.details_dataset(dataset_id)
      workspace_id = dataset_details['workspace']['id']
      create_use_case_configuration = UseCasePost(
        name = use_case_name,
        dataset = Id(id=dataset_id),
        workspace = Id(id=workspace_id)
        )
      useCase = self.use_cases.create_use_case(create_use_case_configuration)
      job_configuration = ForecastingBuildModel(**configuration,useCase=useCase)
    response = self.forecasting.build_model(job_configuration)
    if execute is False: return response
    id = response['id']
    return Tim.execute_forecast_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )

  def forecasting_predict(
    self,
    parent_job_id: str,
    configuration: Optional[ForecastingPredict] = None,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[ForecastingResultsOptions] = [
      'id',
      'logs',
      'status',
      'table',
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    )-> Union[JobResponse,JobExecuteResponse,ForecastingResultsOutputs]:
    """ Register, execute and collect results of a forecasting predict job.
        The predict job makes a prediction based on an existing model job in the TIM repository.
        You can choose to only register the job and return a forecasting job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','logs','status','table']

    Parameters
    ----------
    parent_job_id : str
      The ID of a forecasting model job in the TIM repository.
    configuration : ForecastingPredict
      TIM Engine forecasting prediction configuration.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','production_forecast'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    ForecastingResultsOutputs ->
    id : str | None
      The ID of a forecast job.
    details : Dict | None
      Metadata of the forecasting job.
    logs : list of Dict | None
      Log messages of the forecasting job.
    status : Dict | None
      Final status of the forecasting job.
    table : DataFrame | None
      Table result containing all predicted values.
    production_forecast : DataFrame | None
      Table result containing only the production forecast.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
    production_table : DataFrame | None
      Table result containing the predicted values of a sequence.
    production_accuracies : Dict | None
      Accuracy metrics calculated by TIM on predicted values of a sequence.
    """
    response = self.forecasting.predict(
      parent_job_id=parent_job_id,
      configuration=configuration
      )
    if execute is False: return response
    id = response['id']
    return Tim.execute_forecast_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )

  def forecasting_rebuild_model(
    self,
    parent_job_id: str,
    configuration: Optional[ForecastingRebuildModel] = None,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[ForecastingResultsOptions] = [
      'id',
      'logs',
      'status',
      'table',
      'model',
      'accuracies',
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    ) -> Union[JobResponse,JobExecuteResponse,ForecastingResultsOutputs]:
    """ Register, execute and collect results of a forecasting rebuild model job.
        The rebuild model job updates and extends an existing model in the TIM repository.
        You can choose to only register the job and return a forecasting job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','logs','status','table','model','accuracies']

    Parameters
    ----------
    parent_job_id : str
      The ID of a forecasting model job in the TIM repository.
    configuration : ForecastingRebuildModel
      TIM Engine forecasting rebuild configuration.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','production_forecast'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    ForecastingResultsOutputs ->
    id : str | None
      The ID of a forecast job.
    details : Dict | None
      Metadata of the forecasting job.
    logs : list of Dict | None
      Log messages of the forecasting job.
    status : Dict | None
      Final status of the forecasting job.
    table : DataFrame | None
      Table result containing all predicted values.
    production_forecast : DataFrame | None
      Table result containing only the production forecast.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
    production_table : DataFrame | None
      Table result containing the predicted values of a sequence.
    production_accuracies : Dict | None
      Accuracy metrics calculated by TIM on predicted values of a sequence.
    """
    response = self.forecasting.rebuild_model(
      parent_job_id=parent_job_id,
      configuration=configuration
      )
    if execute is False: return response
    id = response['id']
    return Tim.execute_forecast_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )

  def forecasting_retrain_model(
    self,
    parent_job_id: str,
    configuration: Optional[ForecastingRetrainModel] = None,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[ForecastingResultsOptions] = [
      'id',
      'logs',
      'status',
      'table',
      'model',
      'accuracies',
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    ) -> Union[JobResponse,JobExecuteResponse,ForecastingResultsOutputs]:
    """ Register, execute and collect results of a forecasting retrain model job.
        The retrain model job updates the coefficients of an existing model in the TIM repository.
        You can choose to only register the job and return a forecasting job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','logs','status','table','model','accuracies']

    Parameters
    ----------
    parent_job_id : str
      The ID of a forecasting model job in the TIM repository.
    configuration : ForecastingRetrainModel
      TIM Engine forecasting retrain configuration.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','production_forecast'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    ForecastingResultsOutputs ->
    id : str | None
      The ID of a forecast job.
    details : Dict | None
      Metadata of the forecasting job.
    logs : list of Dict | None
      Log messages of the forecasting job.
    status : Dict | None
      Final status of the forecasting job.
    table : DataFrame | None
      Table result containing all predicted values.
    production_forecast : DataFrame | None
      Table result containing only the production forecast.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
    production_table : DataFrame | None
      Table result containing the predicted values of a sequence.
    production_accuracies : Dict | None
      Accuracy metrics calculated by TIM on predicted values of a sequence.
    """
    response = self.forecasting.retrain_model(
      parent_job_id=parent_job_id,
      configuration=configuration
      )
    if execute is False: return response
    id = response['id']
    return Tim.execute_forecast_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )

  def forecasting_results_rca(
    self,
    id: str,
    indices_of_model: Optional[List[int]] = None,
    parent_job_id: str = None,
    timestamp: Optional[str] = None,
    radius: Optional[int] = None,
    outputs: Optional[List[ForecastingResultsRCAOptions]] = [
      'id',
      'details',
      'logs',
      'status'
      'results',
      ],
    ) -> ForecastingRCAOutput:
    """ Return the results of a root cause analysis job.
        By default all possible outputs are returned: 
        ['id','details','logs','status','results']

    Parameters
    ----------
    id : str
      The ID of a forecasting root cause analysis job in the TIM repository.
    indices_of_model : list of int
      The model indices from the parent job model.
    parent_job_id : str | None
      The parent forecasting job on which the root cause analysis was performed.
    timestamp : 
      Selected timestamp to retrieve RCA results for; if not provided, the last timestamp of the results table is taken.
    radius : 
      The maximum number of records to return before and after the timestamp.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','results']

    Returns
    -------
    id : str | None
      The ID of the root cause analysis job.
    details : Dict | None
      Metadata of the root cause analysis job.
    logs : list of Dict | None
      Log messages of the root cause analysis job.
    status : Dict | None
      Final status of the root cause analysis job.
    results : DataFrame | None
      Table result containing all root cause analysis values.
    """
    if indices_of_model is None:
      if parent_job_id is None:
        job_details = self.forecasting.job_details(id=id)
        parent_job_id = job_details['parentJob']['id']
      parent_job_details = self.forecasting.job_details(id=parent_job_id)
      model_id = parent_job_details['parentJob'] if parent_job_details['type'] in ['predict','what-if'] else parent_job_id
      results_model = self.forecasting.results_model(model_id)
      indices_of_model = [f['index'] for f in results_model['model']['modelZoo']['models']]
    
    results = []
    for index_of_model in indices_of_model:
      result = self.forecasting.results_rca(
        id=id,
        index_of_model=index_of_model,
        timestamp=timestamp,
        radius=radius
      )
      results.append(RCAResults(indexOfModel=index_of_model,results=result))
    details = self.forecasting.job_details(id) if 'details' in outputs else None
    logs = self.forecasting.job_logs(id) if 'logs' in outputs else None
    status = self.forecasting.status(id) if 'status' in outputs else None
    return ForecastingRCAOutput(
      id=id,
      details=details,
      logs=logs,
      status=status,
      results=results
      )

  def forecasting_root_cause_analysis(
    self,
    parent_job_id: str,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: Optional[List[ForecastingResultsRCAOptions]] = [
      'id',
      'results',
      ],
    indices_of_model: Optional[List[int]] = None,
    timestamp: Optional[str] = None,
    radius: Optional[int] = None,
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    ) -> Union[JobResponse,JobExecuteResponse,ForecastingRCAOutput]:
    """ Register, execute and return the results of a root cause analysis job.
        You can choose to only register the job and return a job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        By default the following outputs are returned: 
        ['id','results']

    Parameters
    ----------
    parent_job_id : str
      The parent forecasting job on which the root cause analysis was performed.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','results'].
    indices_of_model : list of int
      The model indices from the parent job model.
    timestamp : 
      Selected timestamp to retrieve RCA results for; if not provided, the last timestamp of the results table is taken.
    radius : 
      The maximum number of records to return before and after the timestamp.
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    ForecastingRCAOutput ->
    id : str | None
      The ID of the root cause analysis job.
    details : Dict | None
      Metadata of the root cause analysis job.
    logs : list of Dict | None
      Log messages of the root cause analysis job.
    status : Dict | None
      Final status of the root cause analysis job.
    results : DataFrame | None
      Table result containing all root cause analysis values.
    """
    response = self.forecasting.rca(parent_job_id=parent_job_id)
    if execute is False: return response
    id = response['id']
    execute_response = Tim.execute_forecast_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      status_poll=status_poll,
      tries_left=tries_left
      )
    if wait_to_finish is False: return execute_response
    return Tim.forecasting_results_rca(
      self,
      id=id,
      indices_of_model=indices_of_model,
      timestamp=timestamp,
      radius=radius,
      parent_job_id=parent_job_id,
      outputs=outputs
      )

  def forecasting_what_if_analysis(
    self,
    parent_job_id: str,
    configuration: Union[WhatIf,WhatIfPanel],
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[ForecastingResultsOptions] = [
      'id',
      'table'
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300 
    )-> Union[JobResponse,JobExecuteResponse,ForecastingResultsOutputs]:
    """ Register, execute and collect results of a forecasting what-if analysis job.
        The what-if job makes a prediction based on an existing model job in the TIM repository and newly provide data.
        You can choose to only register the job and return a forecasting job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','table']

    Parameters
    ----------
    parent_job_id : str
      The ID of a forecasting job in the TIM repository.
    configuration : Dict
      TIM Engine what-if configuration.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','production_forecast','model','accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    ForecastingResultsOutputs ->
    id : str | None
      The ID of a forecast job.
    details : Dict | None
      Metadata of the forecasting job.
    logs : list of Dict | None
      Log messages of the forecasting job.
    status : Dict | None
      Final status of the forecasting job.
    table : DataFrame | None
      Table result containing all predicted values.
    production_forecast : DataFrame | None
      Table result containing only the production forecast.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
    """
    response = self.forecasting.what_if(
      parent_job_id=parent_job_id,
      configuration=configuration
      )
    if execute is False: return response
    id = response['id']
    return Tim.execute_forecast_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )

  def quick_forecast(
    self,
    dataset: DataFrame,
    job_configuration: ForecastingBuildModel = ForecastingBuildModel(),
    workspace_id: str = None,
    dataset_configuration: UploadDatasetConfiguration = UploadDatasetConfiguration(),
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs = [
        'id',
        'status',
        'table',
    ],
    status_poll: Optional[Callable[[Union[DatasetStatusResponse,StatusResponse]], None]] = None,
    tries_left: int = 300,
    delete_items: bool = False
    ) -> QuickForecast:
    """ Register, execute and collect results of a forecasting build model job from a new dataset.
        The quick forecast offers much flexibility in setting up a forecasting job within TIM and easily clean up afterwards.
        You can choose to only register the job and return a forecasting job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','status','table']

    Parameters
    ----------
    dataset : DataFrame
    job_configuration : ForecastingBuildModel
      TIM Engine model building and forecasting configuration.
    workspace_id : str
      The ID of a workspace in the TIM repository.
    dataset_configuration : UploadDatasetConfiguration
        Metadata of the dataset
        Available keys are: 
        timestampFormat, timestampColumn, decimalSeparator, csvSeparator, timeZone,
        timeZoneName, groupKeys, name, description, samplingPeriod and workspace.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','production_forecast'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.
    delete_items: bool
      Removes all content within TIM after returning the results.
      
    Returns
    -------
    upload_response: Dict | None
    forecasting_response: NamedTuple
      if execute is false:
      JobResponse : Dict | None

      if wait_to_finish is false:
      JobExecuteResponse : Dict | None
      
      else:
      ForecastingResultsOutputs ->
      id : str | None
        The ID of a forecast job.
      details : Dict | None
        Metadata of the forecasting job.
      logs : list of Dict | None
        Log messages of the forecasting job.
      status : Dict | None
        Final status of the forecasting job.
      table : DataFrame | None
        Table result containing all predicted values.
      production_forecast : DataFrame | None
        Table result containing only the production forecast.
      model :  Dict | None
        Contains the model and contextual information about the model.
      accuracies : Dict | None
        Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
      production_table : DataFrame | None
        Table result containing the predicted values of a sequence.
      production_accuracies : Dict | None
        Accuracy metrics calculated by TIM on predicted values of a sequence.
    delete_response: Dict | None
    """
    if delete_items is True and (wait_to_finish is False or execute is False): 
      raise ValueError("'Delete_items' can only be True when both 'wait_to_finish' and 'execute' are True. Change 'wait_to_finish' and 'execute' to True to use the 'delete_items' parameter.")
    configuration = job_configuration.copy()
    try:
        use_case_name = job_configuration['name']
    except:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        use_case_name = f'Quick Forecast - {dt_string}'
        configuration['name'] = use_case_name
    upload_dataset_configuration = dataset_configuration.copy()
    if workspace_id is not None: upload_dataset_configuration['workspace'] = Id(id=workspace_id)
    try: 
        upload_dataset_configuration['name']
    except:
        upload_dataset_configuration['name'] = use_case_name
    upload_dataset = Tim.upload_dataset(
      self,
      dataset = dataset,
      configuration = upload_dataset_configuration,
      wait_to_finish = True,
      status_poll = status_poll,
      tries_left=tries_left
      )
    upload_response = upload_dataset.response
    dataset_id = upload_response['id']
    forecasting_build_model = Tim.forecasting_build_model(
      self,
      configuration = configuration,
      dataset_id = dataset_id,
      execute = execute,
      wait_to_finish = wait_to_finish,
      outputs = outputs,
      status_poll = status_poll,
      tries_left=tries_left
     )
    delete_response = self.datasets.delete_dataset(id=dataset_id) if delete_items else None
    return QuickForecast(
      upload_response = upload_response,
      forecast_response = forecasting_build_model,
      delete_response = delete_response
      )

# -------------------------------- Detection --------------------------------
  def poll_detect_status(
    self,
    id: str,
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    ) -> StatusResponse:
    """Poll for the status and progress of a detection job.

    Parameters
    ----------
    id : str
      The ID of a detection job in the TIM repository.
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the job.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    status : Dict
      Available keys: createdAt (str), status (str), progress (float), memory (int) and CPU (int).
    """
    if tries_left < 1:
      raise ValueError("Timeout error.")
    response = self.detection.status(id)
    if status_poll: status_poll(response)
    if Status(response['status']).value == Status.FAILED.value:
      return response
    if Status(response['status']).value != Status.FINISHED.value and Status(response['status']).value != Status.FINISHED_WITH_WARNING.value:
      sleep(2)
      return Tim.poll_detect_status(self,id, status_poll, tries_left - 1)
    return response

  def detection_job_results(
    self,
    id: str,
    outputs: List[DetectionResultsOptions] = [
      'id',
      'details',
      'logs',
      'status',
      'table',
      'model',
      'accuracies',
      ]
    ) -> DetectionResultsOutputs:
    """Retrieve the results of a detection job. You can choose which outputs you want to return by specifying the outputs.
       By default the following outputs are returned.
       ['id','details','logs','status','table','model','accuracies']

    Parameters
    ----------
    id : str
      The ID of a detection job.
    outputs : array | 
      Possible outputs are ['id','details','logs','status','table'
                            ,'model','accuracies','production_table','production_accuracies']
    Returns
    -------
    id : str | None
      The ID of a detection job for tracing.
    details : Dict | None
      Metadata of the detection job.
    logs : list of Dict | None
      Log messages of the detection job.
    status : Dict | None
      Final status of the detection job.
    table : DataFrame | None
      Table result containing all predicted values.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      The performance metrics of a detection job.
    production_table : DataFrame | None
      Table result of a sequence.
    production_accuracies : Dict | None
      The performance metrics of a sequence.
    """
    details = self.detection.job_details(id) if 'details' in outputs else None
    logs = self.detection.job_logs(id) if 'logs' in outputs else None
    status = self.detection.status(id) if 'status' in outputs else None
    table = self.detection.results_table(id) if 'table' in outputs else None
    if 'model' in outputs:
      model = self.detection.results_model(id) 
      if model == {}:
        job_details = self.detection.job_details(id)
        parent_job_id = job_details['parentJob']['id']
        model = self.detection.results_model(parent_job_id) 
    else:
      model = None
    accuracies = self.detection.results_accuracies(id) if 'accuracies' in outputs else None
    production_table = self.detection.results_production_table(id) if 'production_table' in outputs else None
    production_accuracies = self.detection.results_production_accuracies(id)  if 'production_accuracies'  in outputs else None
    return DetectionResultsOutputs(
      id=id,
      details=details,
      logs=logs,
      status=status,
      table=table,
      model=model,
      accuracies=accuracies,
      production_table=production_table,
      production_accuracies=production_accuracies
    )

  def execute_detection_job(    
    self,
    id: str,
    wait_to_finish: bool = True,
    outputs: List[DetectionResultsOptions] = None,
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    ) -> Union[JobExecuteResponse,DetectionResultsOutputs]:
    """Execute a detection job. You can choose which outputs you want to return by specifying the outputs.
       By default none are returned.

    Parameters
    ----------
    id : str
      The ID of a detection job to execute.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning.
      If set to False, the function will return once the job has started the execution process.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    DetectionResultsOutputs ->
    id : str | None
      The ID of a detection job for tracing.
    details : Dict | None
      Metadata of the detection job.
    logs : list of Dict | None
      Log messages of the detection job.
    status : Dict | None
      Final status of the detection job.
    table : DataFrame | None
      Table result containing all predicted values.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      The performance metrics of a detection job.
    production_table : DataFrame | None
      Table result of a sequence.
    production_accuracies : Dict | None
      The performance metrics of a sequence.
    """
    response = self.detection.execute(id)
    if wait_to_finish is False: 
      return JobExecuteResponse(
        id=id,
        response=response,
        status='Queued'
        )
    status = Tim.poll_detect_status(
      self,
      id=id,
      status_poll=status_poll,
      tries_left=tries_left
      )
    if outputs is None: 
      return JobExecuteResponse(
        id=id,
        response=response,
        status=status
        )
    return Tim.detection_job_results(
      self,
      id=id,
      outputs=outputs
      )

  def detection_build_kpi_model(
    self,
    configuration: DetectionBuildKPIModel,
    dataset_id: str = None,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[DetectionResultsOptions] = [
      'id',
      'logs',
      'status',
      'table',
      'model',
      'accuracies',
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300
    ) -> Union[JobResponse,JobExecuteResponse,DetectionResultsOutputs]:
    """ Register, execute and collect results of a detection build kpi model job.
        The KPI approach detects anomalies within a target variable.
        The build model job makes a new detection model based on a dataset id and configuration.
        You can choose to only register the job and return a detection job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','logs','status','table','model','accuracies']

    Parameters
    ----------
    configuration : DetectionBuildKPIModel
      TIM Engine KPI model building and detection configuration.
    dataset_id : str
      The ID of a dataset in the TIM repository.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','model','accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the detection job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    DetectionResultsOutputs ->
    id : str | None
      The ID of a detection job.
    details : Dict | None
      Metadata of the detection job.
    logs : list of Dict | None
      Log messages of the detection job.
    status : Dict | None
      Final status of the detection job.
    table : DataFrame | None
      Table result containing all predicted values.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      The performance metrics of a detection job.
    """
    try:
      configuration['useCase']['id']
      job_configuration = DetectionBuildKPIModel(**configuration)
    except:
      if dataset_id is None: raise ValueError("'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'")
      dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      create_use_case_configuration = UseCasePost(
        name = f'Quick KPI Detection - {dt_string}',
        dataset = Id(id=dataset_id)
        )
      useCase = self.use_cases.create_use_case(create_use_case_configuration)
      job_configuration = DetectionBuildKPIModel(**configuration,useCase=useCase)
    response = self.detection.build_kpi_model(job_configuration)
    if execute is False: return response
    id = response['id']
    return Tim.execute_detection_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )

  def detection_build_system_model(
    self,
    configuration: DetectionBuildSystemModel,
    dataset_id: str = None,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[DetectionResultsOptions] = [
      'id',
      'logs',
      'status',
      'table',
      'model',
      'accuracies',
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300 
    ) -> Union[JobResponse,JobExecuteResponse,DetectionResultsOutputs]:
    """ Register, execute and collect results of a detection build system model job.
        The system-driven approach doesn't require a target value and detects anomalies in the whole system.
        The build model job makes a new detection model based on a dataset id and configuration.
        You can choose to only register the job and return a detection job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','logs','status','table','model','accuracies']

    Parameters
    ----------
    configuration : DetectionBuildSystemModel
      TIM Engine System driven model building and detection configuration.
    dataset_id : str
      The ID of a dataset in the TIM repository.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table','model','accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the detection job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    DetectionResultsOutputs ->
    id : str | None
      The ID of a detection job.
    details : Dict | None
      Metadata of the detection job.
    logs : list of Dict | None
      Log messages of the detection job.
    status : Dict | None
      Final status of the detection job.
    table : DataFrame | None
      Table result containing all predicted values.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      The performance metrics of a detection job.
    """
    try:
      configuration['useCase']['id']
      job_configuration = DetectionBuildSystemModel(**configuration)
    except:
      if dataset_id is None: raise ValueError("'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'")
      dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      create_use_case_configuration = UseCasePost(
        name = f'Quick System Detection - {dt_string}',
        dataset = Id(id=dataset_id)
        )
      useCase = self.use_cases.create_use_case(create_use_case_configuration)
      job_configuration = DetectionBuildSystemModel(**configuration,useCase=useCase)
    response = self.detection.build_system_model(job_configuration)
    if execute is False: return response
    id = response['id']
    return Tim.execute_detection_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )

  def detection_rebuild_kpi_model(
    self,
    parent_job_id: str,
    configuration: Optional[DetectionRebuildKPIModel] = None,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[DetectionResultsOptions] = [
      'id',
      'logs',
      'status',
      'table',
      'model',
      'accuracies',
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300 
    ) -> Union[JobResponse,JobExecuteResponse,DetectionResultsOutputs]:
    """ Register, execute and collect results of a detection rebuild kpi model job.
        The rebuild updates and extends an existing KPI model in the TIM repository.
        You can choose to only register the job and return a detection job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','logs','status','table','model','accuracies']

    Parameters
    ----------
    parent_job_id : str
      The ID of a detection model job in the TIM repository.
    configuration : DetectionRebuildKPIModel
      TIM Engine KPI model rebuilding and detection configuration.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the detection job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    DetectionResultsOutputs ->
    id : str | None
      The ID of a detection job.
    details : Dict | None
      Metadata of the detection job.
    logs : list of Dict | None
      Log messages of the detection job.
    status : Dict | None
      Final status of the detection job.
    table : DataFrame | None
      Table result containing all predicted values.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      The performance metrics of a detection job.
    production_table : DataFrame | None
      Table result of a sequence.
    production_accuracies : Dict | None
      The performance metrics of a sequence.
    """
    response = self.detection.rebuild_kpi_model(
      parent_job_id=parent_job_id,
      configuration=configuration
      )
    if execute is False: return response
    id = response['id']
    return Tim.execute_detection_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )
  
  def detection_detect(
    self,
    parent_job_id: str,
    configuration: DetectionDetect,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[DetectionResultsOptions] = [
      'id',
      'logs',
      'status',
      'table',
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300 
    )-> Union[JobResponse,JobExecuteResponse,DetectionResultsOutputs]:
    """ Register, execute and collect results of a detection detect job.
        The detect job makes a detection based on an existing model job in the TIM repository.
        You can choose to only register the job and return a detection job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','logs','status','table']

    Parameters
    ----------
    parent_job_id : str
      The ID of a detection model job in the TIM repository.
    configuration : DetectionDetect
      TIM Engine detection configuration.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the detection job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    DetectionResultsOutputs ->
    id : str | None
      The ID of a detection job.
    details : Dict | None
      Metadata of the detection job.
    logs : list of Dict | None
      Log messages of the detection job.
    status : Dict | None
      Final status of the detection job.
    table : DataFrame | None
      Table result containing all predicted values.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      The performance metrics of a detection job.
    production_table : DataFrame | None
      Table result of a sequence.
    production_accuracies : Dict | None
      The performance metrics of a sequence.
    """
    response = self.detection.detect(
      parent_job_id=parent_job_id,
      configuration=configuration
      )
    if execute is False: return response
    id = response['id']
    return Tim.execute_detection_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )

  def detection_results_rca(
    self,
    id: str,
    index_of_model: Optional[int] = None,
    timestamp: Optional[str] = None,
    radius: Optional[int] = None,
    outputs: Optional[List[DetectionResultsRCAOptions]] = [
      'id',
      'details',
      'logs',
      'status',
      'results',
      ]
    ) -> DetectionRCAOutput:
    """ Return the results of a detection root cause analysis job.
        By default all possible outputs are returned: 
        ['id','details','logs','status','results']

    Parameters
    ----------
    id : str
      The ID of a detecion root cause analysis job in the TIM repository.
    index_of_model : int | None
      A model index from the parent job model.
    timestamp : 
      Selected timestamp to retrieve RCA results for; if not provided, the last timestamp of the results table is taken.
    radius : 
      The maximum number of records to return before and after the timestamp.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','results']

    Returns
    -------
    id : str | None
      The ID of the root cause analysis job.
    details : Dict | None
      Metadata of the root cause analysis job.
    logs : list of Dict | None
      Log messages of the root cause analysis job.
    status : Dict | None
      Final status of the root cause analysis job.
    results : DataFrame | None
      Table result containing all root cause analysis values.
    """
    results = self.detection.results_rca(
      id=id,
      index_of_model=index_of_model,
      timestamp=timestamp,
      radius=radius
      )
    details = self.detection.job_details(id) if 'details' in outputs else None
    logs = self.detection.job_logs(id) if 'logs' in outputs else None
    status = self.detection.status(id) if 'status' in outputs else None
    return DetectionRCAOutput(
      id=id,
      details=details,
      logs=logs,
      status=status,
      results=results
      )

  def detection_root_cause_analysis(
    self,
    parent_job_id: str,
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: Optional[List[DetectionResultsRCAOptions]] = [
      'id',
      'results',
      ],
    index_of_model: Optional[int] = None,
    timestamp: Optional[str] = None,
    radius: Optional[int] = None,
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300 
    ) -> Union[JobResponse,JobExecuteResponse,DetectionRCAOutput]:
    """ Register, execute and return the results of a detection root cause analysis job.
        You can choose to only register the job and return a job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        By default the following outputs are returned: 
        ['id','results']

    Parameters
    ----------
    parent_job_id : str
      The parent detection job on which the root cause analysis was performed.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','results'].
    index_of_model : int | None
      A model index from the parent job model.
    timestamp : 
      Selected timestamp to retrieve RCA results for; if not provided, the last timestamp of the results table is taken.
    radius : 
      The maximum number of records to return before and after the timestamp.
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the detection job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    DetectionResultsRCAOptions ->
    id : str | None
      The ID of the root cause analysis job.
    details : Dict | None
      Metadata of the root cause analysis job.
    logs : list of Dict | None
      Log messages of the root cause analysis job.
    status : Dict | None
      Final status of the root cause analysis job.
    results : DataFrame | None
      Table result containing all root cause analysis values.
    """
    response = self.detection.rca(parent_job_id=parent_job_id)
    if execute is False: return response
    id = response['id']
    execute_response = Tim.execute_detection_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      status_poll=status_poll,
      tries_left=tries_left
      )
    if wait_to_finish is False: return execute_response
    return Tim.detection_results_rca(
      self,
      id=id,
      index_of_model=index_of_model,
      timestamp=timestamp,
      radius=radius,
      outputs=outputs
      )

  def detection_what_if_analysis(
    self,
    parent_job_id: str,
    configuration: Union[WhatIf,WhatIfPanel],
    execute: bool = True,
    wait_to_finish: bool = True,
    outputs: List[DetectionResultsOptions] = [
      'id',
      'table'
      ],
    status_poll: Optional[Callable[[StatusResponse], None]] = None,
    tries_left: int = 300 
    )-> Union[JobResponse,JobExecuteResponse,DetectionResultsOutputs]:
    """ Register, execute and collect results of a detection what-if analysis job.
        The what-if job makes a detection based on an existing model job in the TIM repository and newly provide data.
        You can choose to only register the job and return a detection job ID.
        You can also choose to already start the execution of the registered job.
        You can also choose to wait for the job to finish.
        Lastly you can choose which outputs are returned by the function.
        By default the following outputs are returned: 
        ['id','table']

    Parameters
    ----------
    parent_job_id : str
      The ID of a detection job in the TIM repository.
    configuration : Dict
      TIM Engine what-if configuration.
    execute : bool, Optional
      If set to False, the function will return once the job has been registered.
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
      If set to False, the function will return once the job has started the execution process.
    outputs : array, Optional
      Possible outputs are ['id','details','logs','status','table'
                            ,'model','accuracies','production_table','production_accuracies']
    status_poll : Callable, Optional
      A callback function to poll for the status and progress of the detection job execution.
    tries_left: int
      Number of iterations the function will loop to fetch the job status before sending a timeout error.

    Returns
    -------
    if execute is false:
    JobResponse : Dict | None

    if wait_to_finish is false:
    JobExecuteResponse : Dict | None
    
    else:
    DetectionResultsOutputs ->
    id : str | None
      The ID of a detection job.
    details : Dict | None
      Metadata of the detection job.
    logs : list of Dict | None
      Log messages of the detection job.
    status : Dict | None
      Final status of the detection job.
    table : DataFrame | None
      Table result containing all predicted values.
    model :  Dict | None
      Contains the model and contextual information about the model.
    accuracies : Dict | None
      The performance metrics of a detection job.
    production_table : DataFrame | None
      Table result of a sequence.
    production_accuracies : Dict | None
      The performance metrics of a sequence.
    """
    response = self.detection.what_if(
      parent_job_id=parent_job_id,
      configuration=configuration
      )
    if execute is False: return response
    id = response['id']
    return Tim.execute_detection_job(
      self,
      id=id,
      wait_to_finish=wait_to_finish,
      outputs=outputs,
      status_poll=status_poll,
      tries_left=tries_left
      )