from enum import Enum
from typing_extensions import TypedDict
from typing import List,Union,Optional,NamedTuple
from pandas import DataFrame

# ------------------------------------ General ------------------------------------

class Id(TypedDict):
  id: str

class SortDirection(Enum):
  CREATED_AT_DESC = '-createdAt'
  CREATED_AT_ASC = '+createdAt'
  UPDATED_AT_DESC = '-updatedAt'
  UPDATED_AT_ASC = '+updatedAt'
  TITLE_DESC = '-title'
  TITLE_ASC = '+title'

class BaseUnit(Enum):
  DAY = 'Day'
  HOUR = 'Hour'
  MINUTE = 'Minute'
  SECOND = 'Second'
  MONTH = 'Month'
  SAMPLE = 'Sample'

class BaseUnitRange(TypedDict):
  baseUnit: BaseUnit
  value: int

class RangeType(Enum):
  FIRST = 'First'
  LAST = 'Last'

class RelativeRange(TypedDict):
  type: RangeType
  baseUnit: BaseUnit
  value: int

Range = TypedDict('Range', {'from': str, 'to': str})

class Status(Enum):
  REGISTERED = 'Registered'
  RUNNING = 'Running'
  FINISHED = 'Finished'
  FINISHED_WITH_WARNING = 'FinishedWithWarning'
  FAILED = 'Failed'
  QUEUED = 'Queued'
# ------------------------------------ Telemetry ------------------------------------

class JobState(Enum):
  EXISTING = 'Existing'
  DELETED = 'Deleted'

class TelemetryCallState(Enum):
  DELETED = 'Deleted'
  REGISTERED = 'Registered'
  RUNNING = 'Running'
  FINISHED = 'Finished'
  FINISHED_WITH_WARNING = 'FinishedWithWarning'
  FAILED = 'Failed'
  QUEUED = 'Queued'

class BlockWithIdStateAndCreatedAt(TypedDict):
  id: str
  state: TelemetryCallState
  createdAt: str

class TelemetryDataset(TypedDict):
  id: str
  version: BlockWithIdStateAndCreatedAt

class TelemetryResponse(TypedDict):
  time: str
  code: int
  APIResponseCode: str

class TelemetryRequest(TypedDict):
  method: str
  target: str
  microservice: str

class DatasetCall(TypedDict):
  id: str
  time: str
  TIMClientOrigin: str
  imageVersion: str
  madeBy: str
  dataset: TelemetryDataset
  response: TelemetryResponse
  request: TelemetryRequest

class TelemetryJob(TypedDict):
  id: str
  parentJob: Id
  state: TelemetryCallState
  createdAt: str

class JobCall(TypedDict):
  id: str
  time: str
  TIMClientOrigin: str
  imageVersion: str
  madeBy: str
  dataset: TelemetryDataset
  response: TelemetryResponse
  request: TelemetryRequest
  job: TelemetryJob
  experiment: Id

# ------------------------------------ Licenses ------------------------------------

class LicensePlan(Enum):
  TRIAL = 'Trial'
  BASIC = 'Basic'
  PROFESSIONAL = 'Professional'
  ENTERPISE = 'Enterprise'
  GENERAL = 'General'
  PARTNER = 'Partner'

class License(TypedDict):
  licenseKey: str
  name: str
  organizationName: str
  expiration: str
  plan: LicensePlan
  storageLimit: float
  datasetRowsLimit: int
  datasetColumnsLimit: int
  additionalLicenseData: TypedDict

class LicenseStorage(TypedDict):
  usedMb: float
  limitMb: float
  hasFreeSpace: bool
  datasetRowsLimit: int
  datasetColumnsLimit: int

# ------------------------------------ User Groups ------------------------------------

class UserGroup(TypedDict,total=False):
  id: str
  name: str
  description: str
  createdAt: str
  createdBy: str
  updatedAt: str
  updatedBy: str

class UserGroupListPayload(TypedDict, total=False):
  offset: int
  limit: int
  sort: SortDirection

class UserGroupUser(TypedDict):
  id: str
  isOwner: bool

class CreateUserGroup(TypedDict):
  name: str
  description: str
  users: List[UserGroupUser]

# ------------------------------------ Authentication ------------------------------------

class Role(Enum):
  ADMINISTRATOR = 'administrator'
  STANDARD = 'standard'

class TokenPayload(TypedDict):
  email: str
  firstName: str
  lastName: str
  userId: str
  licenseKey: str
  role: Role
  loggedInAt: str
  expiresIn: int
  expiresAt: str
  tokenId: str

class LicenseKey(TypedDict):
  licenseKey: str
  
class User(TypedDict):
  id: str
  email: str
  firstName: str
  lastName: str
  license: LicenseKey
  isActive: bool
  isAdmin: bool
  additionalUserData: TypedDict
  personalUserGroup: Id
  lastLogin: str

class AuthResponse(TypedDict):
  token: str
  loggedInAt: str
  expiresIn: int
  tokenPayload: TokenPayload
  license: License
  user: User
  personalUserGroup: UserGroup

# ------------------------------------ Workspaces ------------------------------------

class Workspace(TypedDict):
  id: str
  name: str
  description: str
  userGroup: Id
  isFavorite: bool
  createdAt: str
  createdBy: str
  updatedAt: str
  updatedBy: str

class WorkspaceListPayload(TypedDict, total=False):
  offset: int
  limit: int
  userGroupId: str
  sort: SortDirection

class WorkspacePost(TypedDict):
  name: str
  description: str
  userGroup: Id
  isFavorite: bool

class WorkspacePut(TypedDict):
  name: str
  description: str
  isFavorite: bool

# ------------------------------------ Use Cases ------------------------------------

class UseCase(TypedDict):
  id: str
  name: str
  description: str
  input: str
  output: str
  businessValue: str
  businessObjective: str
  businessKpi: str
  accuracyImpact: int
  workspace: Id
  dataset: Id
  isFavorite: bool
  defaultFExperiment: Id
  defaultADExperiment: Id
  createdAt: str
  createdBy: str
  updatedAt: str
  updatedBy: str

class UseCaseListPayload(TypedDict,total=False):
  offset: int
  limit: int
  userGroupId: str
  workspaceId: str
  datasetId: str
  sort: SortDirection
  isPanelData: bool

class UseCasePost(TypedDict):
  name: str
  description: Optional[str]
  input: Optional[str]
  output: Optional[str]
  businessValue: Optional[str]
  businessObjective: Optional[str]
  businessKpi: Optional[str]
  accuracyImpact: Optional[int]
  workspace: Optional[Id]
  dataset: Optional[Id]
  isFavorite: Optional[bool]

class UseCasePostResponse(TypedDict):
  id: str
  name: str
  description: str
  input: str
  output: str
  businessValue: str
  businessObjective: str
  businessKpi: str
  accuracyImpact: int
  workspace: Id
  dataset: Id
  isFavorite: bool
  createdAt: str
  createdBy: str

class UseCasePut(TypedDict):
  name: str
  description: str
  input: str
  output: str
  businessValue: str
  businessObjective: str
  businessKpi: str
  accuracyImpact: int
  dataset: Id
  isFavorite: bool
  defaultFExperiment: Id
  defaultADExperiment: Id
# # ------------------------------------ Experiments ------------------------------------

class JobType(Enum):
  FORECASTING = 'Forecasting'
  ANOMALYDETECTION = 'AnomalyDetection'

class Experiment(TypedDict):
  id: str
  name: str
  description: str
  useCase: Id
  type: JobType
  createdAt: str
  createdBy: str
  updatedAt: str
  updatedBy: str 

class ExperimentListPayload(TypedDict,total=False):
  offset: int
  limit: int
  workspaceId: str
  useCaseId: str
  datasetId: str
  sort: SortDirection
  type: str

class ExperimentPost(TypedDict):
  name: str
  description: str
  useCase: Id
  type: JobType

class ExperimentPut(TypedDict):
  name: str
  description: str

# # ------------------------------------ Datasets ------------------------------------

class DecimalSeparator(Enum):
  COMMA = ','
  DOT = '.'

class CSVSeparator(Enum):
  SEMICOLON = ';'
  TAB = ' '
  COMMA = ','

class UploadDatasetConfiguration(TypedDict, total=False):
  timestampFormat: str
  timestampColumn: Union[str, int]
  decimalSeparator: DecimalSeparator
  csvSeparator: CSVSeparator
  timeZone:  str
  timeZoneName: str
  groupKeys: List[Union[str, int]]
  name: str
  description: str
  samplingPeriod: BaseUnitRange
  workspace: Id

class DatasetCreated(TypedDict):
  id: str
  version: Id

class UpdateDatasetConfiguration(TypedDict, total=False):
  timestampFormat: str
  timestampColumn: Union[str, int]
  decimalSeparator: DecimalSeparator
  csvSeparator: CSVSeparator

class DatasetVersion(TypedDict):
  version: Id

class DatasetStatusResponse(TypedDict):
  createdAt: str
  status: Status
  progress: int

class DatasetWorkspace(TypedDict):
  id: str
  name: str

class LatestVersion(TypedDict):
  id: str
  status: Status
  numberOfVariables: int
  numberOfObservations: int
  firstTimestamp: str
  lastTimestamp: str

class DatasetDetails(TypedDict):
  id: str
  latestVersion: LatestVersion
  createdAt: str
  createdBy: str
  updatedAt: str
  updatedBy: str
  description: str
  isFavorite: bool
  estimatedSamplingPeriod: str
  groupKeys: List[Union[str, int]]
  timeZoneName: str
  workspace: DatasetWorkspace
  name: str

class Variables(TypedDict):
  name: str
  type: str
  firstTimestamp: str
  lastTimestamp: str
  minimumValue: float
  maximumValue: float
  averageValue: float
  missingObservations: int

class DatasetVersionDetails(TypedDict):
  id: str
  dataset: Id
  estimatedSamplingPeriod: str
  size: int
  numberOfObservations: int
  numberOfVariables: int
  firstTimestamp: str
  lastTimestamp: str
  variables: List[Variables]
  createdAt: str
  status: Status
  groupKeys: List[Union[str, int]]
  timeZoneName: str

class DatasetListPayload(TypedDict, total=False):
  offset: int
  limit: int
  workspaceId: str
  userGroupId: str
  isPanelData: bool
  to: str
  status: Status
  sort: SortDirection

class DatasetVersionListPayload(TypedDict, total=False):
  id: str
  offset: int
  limit: int

class DatasetOrigin(Enum):
  UPLOAD = 'Upload'
  UPDATE = 'Update'

class MessageType(Enum):
  INFO = 'Info'
  WARNING = 'Warning'
  ERROR = 'Error'

class DatasetLog(TypedDict):
  createdAt: str
  origin: DatasetOrigin
  messageType: MessageType
  message: str
  version: Id

class DatasetVersionLog(TypedDict):
  createdAt: str
  origin: DatasetOrigin
  messageType: MessageType
  message: str

class DatasetUpdate(TypedDict):
  name: str
  description: str

class UploadDatasetResponse(NamedTuple):
  response: DatasetVersion
  details: Optional[DatasetDetails]
  logs: List[DatasetLog]
  
class DatasetOutputs(Enum):
  RESPONSE = 'response'
  LOGS = 'logs'
  METADATA = 'metadata'
# ------------------------------------ Forecasting ------------------------------------

class ModelQuality(Enum):
  COMBINED = 'Combined'
  LOW = 'Low'
  MEDIUM = 'Medium'
  HIGH = 'High'
  VERYHIGH = 'VeryHigh'
  ULTRAHIGH = 'UltraHigh'

class Features(Enum):
  EXPONENTIAL_MOVING_AVERAGE = 'ExponentialMovingAverage'
  REST_OF_WEEK = 'RestOfWeek'
  PERIODIC = 'Periodic'
  INTERCEPT = 'Intercept'
  PIECEWISE_LINEAR = 'PiecewiseLinear'
  TIME_OFFSETS = 'TimeOffsets'
  POLYNOMIAL = 'Polynomial'
  IDENTITY = 'Identity'
  SIMPLE_MOVING_AVERAGE = 'SimpleMovingAverage'
  MONTH = 'Month'
  TREND = 'Trend'
  DAY_OF_WEEK = 'DayOfWeek'
  FOURIER = 'Fourier'
  PUBLIC_HOLIDAYS = 'PublicHolidays'
  COS = 'Cos'
  SIN = 'Sin'

class OffsetLimitType(Enum):
  EXPLICIT = 'Explicit'

class OffsetLimit(TypedDict):
  type: OffsetLimitType
  value: int

class PredictionBoundariesType(Enum):
  EXPLICIT = 'Explicit'
  NONE = 'None'

class PredictionBoundaries(TypedDict):
  type: PredictionBoundariesType
  maxValue: float
  minValue: float

class Backtest(Enum):
  ALL = 'All'
  PRODUCTION = 'Production'
  OUT_OF_SAMPLE = 'OutOfSample'

class ImputationType(Enum):
  LINEAR = 'Linear'
  LOCF = 'LOCF'
  NONE = 'None'

class Imputation(TypedDict):
  type: ImputationType
  maxGapLength: int

class Aggregation(Enum):
  MEAN = 'Mean'
  SUM = 'Sum'
  MINIMUM = 'Minumum'
  MAXIMUM = 'Maximum'

class DataUntil(TypedDict):
  column: Union[str, int]
  baseUnit: BaseUnit
  offset: int

class DataAlignement(TypedDict):
  lastTargetTimestamp: str
  dataUntil: List[DataUntil]

class PreprocessorType(Enum):
  CATEGORYFILTER = 'CategoryFilter'

class CategoryFilterSimple(TypedDict):
  column: str
  categories: List[str]

class Preprocessors(TypedDict):
  type: PreprocessorType
  value: Union[CategoryFilterSimple,List[CategoryFilterSimple]]

class ForecastingBuildModelConfiguration(TypedDict):
  predictionTo: BaseUnitRange
  predictionFrom: BaseUnitRange
  modelQuality: ModelQuality
  normalization: bool
  maxModelComplexity: int
  features: List[Features]
  dailyCycle: bool
  allowOffsets: bool
  offsetLimit: OffsetLimit
  memoryLimitCheck: bool
  predictionIntervals: float
  predictionBoundaries: PredictionBoundaries
  rollingWindow: BaseUnitRange
  backtest: Backtest

class ForecastingBuildModelData(TypedDict):
  version: Id
  inSampleRows: Union[RelativeRange, List[Range]]
  outOfSampleRows: Union[RelativeRange, List[Range]]
  imputation: Imputation
  columns: List[Union[str, int]]
  targetColumn: Union[str, int]
  holidayColumn: Union[str, int]
  timeScale: BaseUnitRange
  aggregation: Aggregation  
  alignment: DataAlignement
  preprocessors: List[Preprocessors]

class ForecastingBuildModel(TypedDict):
  name: str
  useCase: Id
  experiment: Id
  configuration: ForecastingBuildModelConfiguration
  data: ForecastingBuildModelData

class RebuildingPolicyType(Enum):
  NEWSITUATIONS = 'NewSituations'
  ALL = 'All'
  OLDERTHAN = 'OlderThan'

class RebuildingPolicy(TypedDict):
  type: RebuildingPolicyType
  time: BaseUnitRange

class ForecastingRebuildModelConfiguration(TypedDict):
  predictionTo: BaseUnitRange
  predictionFrom: BaseUnitRange
  modelQuality: ModelQuality
  normalization: bool
  maxModelComplexity: int
  features: List[Features]
  allowOffsets: bool
  offsetLimit: OffsetLimit
  memoryLimitCheck: bool
  rebuildingPolicy: RebuildingPolicy
  predictionIntervals: float
  predictionBoundaries: PredictionBoundaries
  rollingWindow: BaseUnitRange
  backtest: Backtest

class ForecastingRebuildModelData(TypedDict):
  version: Id
  inSampleRows: Union[RelativeRange, List[Range]]
  outOfSampleRows: Union[RelativeRange, List[Range]]
  imputation: Imputation
  columns: List[Union[str, int]]
  alignment: DataAlignement
  preprocessors: List[Preprocessors]

class ForecastingRebuildModel(TypedDict):
  name: str
  experiment: Id
  configuration: ForecastingRebuildModelConfiguration
  data: ForecastingRebuildModelData

class ForecastingRetrainModelConfiguration(TypedDict):
  predictionTo: BaseUnitRange
  predictionFrom: BaseUnitRange
  normalization: bool
  memoryLimitCheck: bool
  predictionBoundaries: PredictionBoundaries
  rollingWindow: BaseUnitRange
  backtest: Backtest

class ForecastingRetrainModelData(TypedDict):
  version: Id
  inSampleRows: Union[RelativeRange, List[Range]]
  outOfSampleRows: Union[RelativeRange, List[Range]]
  imputation: Imputation
  alignment: DataAlignement
  preprocessors: List[Preprocessors]

class ForecastingRetrainModel(TypedDict):
  name: str
  experiment: Id
  configuration: ForecastingRetrainModelConfiguration
  data: ForecastingRetrainModelData

class ForecastingPredictConfiguration(TypedDict):
  predictionTo: BaseUnitRange
  predictionFrom: BaseUnitRange
  predictionBoundaries: PredictionBoundaries
  rollingWindow: BaseUnitRange

class ForecastingPredictData(TypedDict):
  version: Id
  outOfSampleRows: Union[RelativeRange, List[Range]]
  imputation: Imputation
  alignment: DataAlignement
  preprocessors: List[Preprocessors]

class ForecastingPredict(TypedDict):
  name: str
  experiment: Id
  configuration: ForecastingPredictConfiguration
  data: ForecastingPredictData

class JobResponse(TypedDict):
  id: str
  expectedResultsTableSize: float

class ForecastingJobType(Enum):
  BUILD_MODEL = 'build-model'
  UPLOAD_MODEL = 'upload-model'
  REBUILD_MODEL = 'rebuild-model'
  RETRAIN_MODEL = 'retrain-model'
  PREDICT = 'predict'
  RCA = 'rca'
  WHAT_IF = 'what-if'

class AccuraciesRegression(TypedDict):
  mae: float
  mape: float
  rmse: float

class ConfusionMatrix(TypedDict):
  truePositive: int
  trueNegative: int
  falsePositive: int
  falseNegative: int

class AccuraciesClassification(TypedDict):
  accuracy: float
  AUC: float
  confusionMatrix: ConfusionMatrix

class AccuraciesForecasting(TypedDict):
  name: str
  outOfSample: Union[AccuraciesRegression,AccuraciesClassification]
  inSample: Union[AccuraciesRegression,AccuraciesClassification]

class ErrorMeasures(TypedDict):
  all: AccuraciesForecasting
  bin: List[AccuraciesForecasting]
  samplesAhead: List[AccuraciesForecasting]

class ForecastingJobMetaData(TypedDict):
  registrationBody: Union[ForecastingBuildModel,ForecastingRebuildModel,ForecastingRetrainModel,ForecastingPredict] #Todo add upload,rca,whatif,whatifpanel 
  errorMeasures: ErrorMeasures
  id: str
  name: str
  type: ForecastingJobType
  status: Status
  parentJob: Id
  sequenceId: str
  useCase: Id
  experiment: Id
  dataset: DatasetVersion
  createdAt:str
  executedAt: str
  completedAt: str
  workerVersion: str
  jobLoad: str
  calculationTime: str

class ExecuteResponse(TypedDict):
  message: str
  code: str

class StatusResponse(TypedDict):
  createdAt: str
  status: Status
  progress: float
  memory: int
  CPU: int

class JobExecuteResponse(TypedDict):
  id: str
  response: ExecuteResponse
  status: Union[str,StatusResponse]

class ForecastLogPayload(TypedDict, total=False):
  id: str
  offset: int
  limit: int
  sort: SortDirection

class ForecastTableRequestPayload(TypedDict):
  forecastType: Optional[str]
  modelIndex: Optional[int]

class JobOrigin(Enum):
  REGISTRATION = 'Registration'
  EXECUTION = 'Executed'
  VALIDATION = 'Validation'

class JobLogs(TypedDict):
  createdAt: str
  origin: JobOrigin
  messageType: MessageType
  message: str

class VariableProperties(TypedDict,total=False):
  name: str
  min: float
  max: float
  dataFrom: int
  importance: float
  aggregation: str

class VariableOffsets(TypedDict,total=False):
  name: str
  dataFrom: int
  dataTo: int

class Cases(TypedDict):
  dayTime: str
  variableOffsets: VariableOffsets

class Part(TypedDict):
  type: str
  predictor: str
  offset: int
  value: float
  window: int
  knot: float
  subtype: int
  period: float
  cosOrders: List[float]
  sinOrder: List[float]
  cosβ: List[float]
  sinβ: List[float]
  unit: str
  day: int
  month: int

class Term(TypedDict):
  importance: int
  parts: List[Part]

class ModelZooModel(TypedDict):
  index: int
  terms: List[Term]
  dayTime: str
  variableOffsets: List[VariableOffsets]
  samplesAhead: List[int]
  modelQuality: int
  predictionIntervals: List[int]
  lastTargetTimestamp: str
  RInv: List[float]
  g: List[float]
  mx: List[float]
  cases: List[Cases]

class ModelZoo(TypedDict):
  samplingPeriod: str
  averageTrainingLength: int
  models: List[ModelZooModel]
  difficulty: int
  targetName: str
  holidayName: str
  groupKeys: List[str]
  upperBoundary: int
  lowerBoundary: int
  dailyCycle: bool
  confidenceLevel: int
  variableProperties: List[VariableProperties]
  inSampleRows: List[Range]
  outofSampleRows: List[Range]

class Model(TypedDict):
  modelZoo: ModelZoo

class ForecastModelResult(TypedDict):
  modelVersion: str
  model: Model
  signature: str

class WhatIf(TypedDict):
  column: str
  data: TypedDict

class WhatIfPanel(TypedDict):
  column: str
  groupKeysValues: List[Union[str,int]]
  data: TypedDict

class CopyExperiment(TypedDict):
  experiment: Id

class ProductionAccuraciesForecasting(TypedDict):
  name: str
  production: Union[AccuraciesRegression,AccuraciesClassification]

class ResultsProductionAccuraciesForecasting(TypedDict):
  all: ProductionAccuraciesForecasting
  bin: List[ProductionAccuraciesForecasting]
  samplesAhead: List[ProductionAccuraciesForecasting]

class ModelFromJob(TypedDict):
  job: Id

class ForecastingUploadModel(TypedDict):
  name: str
  useCase: Id
  experiment: Id
  model: Union[ModelFromJob,ForecastModelResult]

class ForecastingResultsOptions(Enum):
  ID = 'id'
  DETAILS = 'details'
  LOGS = 'logs'
  TABLE = 'table'
  STATUS = 'status'
  PRODUCTION_FORECAST = 'production_forecast'
  MODEL = 'model'
  ACCURACIES = 'accuracies'
  PRODUCTION_TABLE = 'production_table'
  PRODUCTION_ACCURACIES = 'production_accuracies'

class ForecastingResultsOutputs(NamedTuple):
  id: Optional[str]
  details: Optional[ForecastingJobMetaData]
  logs: Optional[List[JobLogs]]
  status: Optional[StatusResponse]
  table: Optional[DataFrame]
  production_forecast: Optional[DataFrame]
  model: Optional[ForecastModelResult]
  accuracies: Optional[ErrorMeasures]
  production_table: Optional[DataFrame]
  production_accuracies: Optional[ResultsProductionAccuraciesForecasting]

class RCAResults(TypedDict):
  indexOfModel: int
  results: DataFrame

class ForecastingResultsRCAOptions(Enum):
  ID = 'id'
  DETAILS = 'details'
  LOGS = 'logs'  
  STATUS = 'status'
  RESULTS = 'results'

class ForecastingRCAOutput(NamedTuple):
  id: Optional[str]
  details: Optional[ForecastingJobMetaData]
  logs: Optional[List[JobLogs]]
  status: Optional[StatusResponse]
  results: RCAResults

class QuickForecast(NamedTuple):
  upload_response: Union[DatasetCreated, UploadDatasetResponse]
  forecast_response: Union[JobResponse,JobExecuteResponse,ForecastingResultsOutputs]
  delete_response: ExecuteResponse

# # ------------------------------------ Detection ------------------------------------

class Perspective(Enum):
  RESIDUAL = 'Residual'
  RESIDUAL_CHANGE = 'ResidualChange'
  FLUCTUATION = 'Fluctuation'
  FLUCTUATION_CHANGE = 'FluctuationChange'
  IMBALANCE = 'Imbalance'
  IMBALANCE_CHANGE = 'ImbalanceChange'

class DomainSpecificsKPI(TypedDict):
  perspective: Perspective
  sensitivity: float
  minSensitivity: float
  maxSensitivity: float

class NormalBehaviorModel(TypedDict):
  useNormalBehaviorModel: bool
  normalization: bool
  maxModelComplexity: int
  features: List[Features]
  dailyCycle: bool
  useKPIoffsets: bool
  allowOffsets: bool
  offsetLimit: OffsetLimit

class DetectionIntervalsType(Enum):
  DAY = 'Day'
  HOUR = 'Hour'
  MINUTE = 'Minute'
  SECOND = 'Second'

class DetectionIntervals(TypedDict):
  type: DetectionIntervalsType
  value: str

class AnomalousBehaviorModel(TypedDict):
  maxModelComplexity: int
  detectionIntervals: List[DetectionIntervals]

class UpdateTime(TypedDict):
  type: DetectionIntervalsType
  value: str

class UpdateUntilBaseUnit(Enum):
  DAY = 'Day'
  HOUR = 'Hour'
  SAMPLE = 'Sample'

class UpdateUntil(TypedDict):
  baseUnit: UpdateUntilBaseUnit
  offset: int

class Updates(TypedDict):
  column: Union[str, int]
  updateTime: List[UpdateTime]
  updateUntil: UpdateUntil

class DetectionBuildKPIModelConfiguration(TypedDict):
  domainSpecifics: List[DomainSpecificsKPI]
  normalBehaviorModel: NormalBehaviorModel
  anomalousBehaviorModel: AnomalousBehaviorModel

class DetectionBuildKPIModelData(TypedDict):
  version: Id
  rows: Union[RelativeRange, List[Range]]
  columns: List[Union[str, int]]
  KPIColumn: Union[str, int]
  holidayColumn: Union[str, int]
  labelColumn: Union[str, int]
  imputation: Imputation
  timeScale: BaseUnitRange
  aggregation: Aggregation
  updates: List[Updates]

class DetectionBuildKPIModel(TypedDict):
  name: str
  useCase: Id
  experiment: Id
  configuration: DetectionBuildKPIModelConfiguration
  data: DetectionBuildKPIModelData

class DomainSpecificsSystem(TypedDict):
  sensitivity: float
  minSensitivity: float
  maxSensitivity: float
  anomalyIndicatorWindow: BaseUnitRange

class SystemModelConfiguration(TypedDict):
  numberOfTrees: int
  subSampleSize: int
  maxTreeDepth: int
  extensionLevel: int
  normalization: bool

class DetectionBuildSystemModelConfiguration(TypedDict):
  domainSpecifics: DomainSpecificsSystem
  model: SystemModelConfiguration

class DetectionBuildSystemModelData(TypedDict):
  version: Id
  rows: Union[RelativeRange, List[Range]]
  columns: List[Union[str, int]]
  labelColumn: Union[str, int]
  imputation: Imputation
  timeScale: BaseUnitRange

class DetectionBuildSystemModel(TypedDict):
  name: str
  useCase: Id
  experiment: Id
  configuration: DetectionBuildSystemModelConfiguration
  data: DetectionBuildSystemModelData

class RebuildType(Enum):
  DOMAIN_SPECIFICS = 'DomainSpecifics'
  ANOMALOUS_BEHAVIOR_MODEL = 'AnomalousBehaviorModel'
  ALL = 'All'

class DetectionRebuildKPIModelConfiguration(TypedDict):
  domainSpecifics: List[DomainSpecificsKPI]
  rebuildType: RebuildType

class DetectionRebuildKPIModelData(TypedDict):
  version: Id
  rows: Union[RelativeRange, List[Range]]
  imputation: Imputation

class DetectionRebuildKPIModel(TypedDict):
  name: str
  experiment: Id
  configuration: DetectionRebuildKPIModelConfiguration
  data: DetectionRebuildKPIModelData

class DetectionDetect(TypedDict):
  name: str
  experiment: Id
  data: DetectionRebuildKPIModelData

class DetectionErrorMeasures(TypedDict):
  AUC: float
  confusionMatrix: ConfusionMatrix

class AnomalyDetectionType(Enum):
  BUILD_MODEL = 'build-model'
  UPLOAD_MODEL = 'upload-model'
  REBUILD_MODEL = 'rebuild-model'
  DETECT = 'detect'
  RCA = 'rca'

class Approach(Enum):
  KPI_DRIVEN = 'kpi-driven'
  SYSTEM_DRIVEN = 'system-driven'

class DetectionJobDetails(TypedDict):
  id: str
  name: str
  type: AnomalyDetectionType
  approach : Approach
  status: Status
  parentJob: Id
  sequenceId: str
  useCase: Id
  dataset: DatasetVersion
  createdAt:str
  executedAt: str
  completedAt: str
  experiment: Id
  workerVersion: str
  jobLoad: str
  calculationTime: str
  registrationBody: Union[DetectionBuildKPIModel,DetectionBuildSystemModel,DetectionRebuildKPIModel,DetectionDetect,] #Todo add upload,rca,whatif,whatifpanel 
  errorMeasures: DetectionErrorMeasures

class DetectionPeriods(TypedDict):
  seconds: List[int]
  minutes: List[int]
  hours: List[int]
  DoW: List[int]

class anomalousBehaviorSettings(TypedDict):
  maxModelComplexity: int
  detectionPeriods: DetectionPeriods

class SettingsUpdatesUntil(TypedDict):
  increment: str
  offset: int

class SettingsUpdatesTimes(TypedDict):
  when: DetectionPeriods
  until: SettingsUpdatesUntil

class SettingsUpdates(TypedDict):
  predictorName: str
  update: SettingsUpdatesTimes

class ModelKpiDrivenSettingsData(TypedDict):
  rows: List[Range]
  columns: List[str]
  KPIColumn: str
  holidayColumn: str
  labelColumn: str
  imputation: Imputation
  timeScale: BaseUnitRange
  updates: List[SettingsUpdates]

class ProbabilityDistribution(TypedDict):
  n: int
  d: int
  w: List[float]

class ModelKpiDrivenNormalBehaviorModelModels(TypedDict):
  index: int
  terms: List[Term]
  dayTime: str
  variableOffsets: List[VariableOffsets]

class Submodel(TypedDict):
  perspective: Perspective
  probabilityDistribution: ProbabilityDistribution
  detectedSensitivity: float
  threshold: float
  translation: float
  cut: int

class ModelKpiDrivenSettings(TypedDict):
  data: ModelKpiDrivenSettingsData
  domainSpecifics: List[DomainSpecificsKPI]
  normalBehavior: NormalBehaviorModel
  anomalousBehavior: anomalousBehaviorSettings

class ModelKpiDrivenNormalBehaviorModel(TypedDict):
  samplingPeriod: str
  timeZone: str
  models: List[ModelKpiDrivenNormalBehaviorModelModels]
  VariableProperties: List[VariableProperties]

class ModelKpiDrivenAnomalousBehaviorModel(TypedDict):
  submodels:List[Submodel]

class ModelSystemSettingsData(TypedDict):
  rows: List[Range]
  columns: List[str]
  labelColumn: str
  imputation: Imputation
  timeScale: BaseUnitRange

class ModelSystemSettingsDomainSpecifics(TypedDict):
  sensitivity: float
  anomalyIndicatorWindow: BaseUnitRange

class ModelSystemSettingsModel(TypedDict):
  numberOfTrees: int
  subSampleSize: int
  maxTreeDepth: Union[str,int]
  extensionLevel: Union[str,int]
  normalization: bool

class Hyperplane(TypedDict):
 normal: List[float]
 intercept: List[float]

class InternalNode(TypedDict):
  type: str
  leftNode: TypedDict
  rightNode: TypedDict
  hyperplane: Hyperplane
  numOfRecords: int
  depth: int

class LeafNode(TypedDict):
  type: str
  numOfRecords: int
  depth: int

class rootNode(TypedDict):
  type: str
  leftNode: Union[InternalNode,LeafNode]
  rightNode: Union[InternalNode,LeafNode]
  hyperplane: Hyperplane
  numOfRecords: int
  depth: int

class TreeNodes(TypedDict):
  rootNode: rootNode
  numOfNodes: int

class TreeSettings(TypedDict):
  numOfTrees: int
  subSampleSize: int
  maxTreeDepth: int
  extensionLevel: int

class ModelSystemParametersAnomalyIndicator(TypedDict):
  detectedSensitivity: float
  threshold: float
  translation: float
  windowLength: int

class ModelSystemParametersNormalization(TypedDict):
  variableNames: List[str]
  mu: List[float]
  sigma: List[float]

class ModelSystemSettings(TypedDict):
  data: ModelSystemSettingsData
  domainSpecifics: ModelSystemSettingsDomainSpecifics
  model: ModelSystemSettingsModel

class ModelSystemModel(TypedDict):
  trees: List[TreeNodes]
  settings: TreeSettings

class ModelSystemParameters(TypedDict):
  anomalyIndicator: ModelSystemParametersAnomalyIndicator
  normalization: ModelSystemParametersNormalization
  samplingPeriod: str
  timeZone: str

class ModelKpiDriven(TypedDict):
  settings: ModelKpiDrivenSettings
  normalBehaviorModel: ModelKpiDrivenNormalBehaviorModel
  anomalousBehaviorModel: ModelKpiDrivenAnomalousBehaviorModel

class ModelSystemDriven(TypedDict):
  settings: ModelSystemSettings
  model: ModelSystemModel
  parameters: ModelSystemParameters

class DetectionModelResult(TypedDict):
  modelVersion: str
  approach: str
  model: Union[ModelKpiDriven,ModelSystemDriven]
  signature: str

class DetectionUploadModel(TypedDict):
  name: str
  useCase: Id
  experiment: Id
  model: Union[ModelFromJob,DetectionModelResult]

class DetectionResultsOptions(Enum):
  ID = 'id'
  DETAILS = 'details'
  LOGS = 'logs'
  TABLE = 'table'
  STATUS = 'status'
  MODEL = 'model'
  ACCURACIES = 'accuracies'
  PRODUCTION_TABLE = 'production_table'
  PRODUCTION_ACCURACIES = 'production_accuracies'

class DetectionResultsOutputs(NamedTuple):
  id: Optional[str]
  details: Optional[DetectionJobDetails]
  logs: Optional[List[JobLogs]]
  status: Optional[StatusResponse]
  table: Optional[DataFrame]
  model: Optional[ForecastModelResult]
  accuracies: Optional[ErrorMeasures]
  production_table: Optional[DataFrame]
  production_accuracies: Optional[DetectionErrorMeasures]

class DetectionResultsRCAOptions(Enum):
  ID = 'id'
  DETAILS = 'details'
  LOGS = 'logs'  
  STATUS = 'status'
  RESULTS = 'results'

class DetectionRCAOutput(NamedTuple):
  id: Optional[str]
  details: Optional[DetectionJobDetails]
  logs: Optional[List[JobLogs]]
  status: Optional[StatusResponse]
  results: RCAResults