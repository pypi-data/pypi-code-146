from typing import List


class ModelKind:
    GENERIC_IC = 'Generic-Classifier'
    GENERIC_OD = 'Generic-Detector'
    VALID_KINDS = [GENERIC_IC, GENERIC_OD]


class ModelProfile:
    LOW_LATENCY = 'lowLatency'
    BALANCED = 'balanced'
    HIGH_ACCURACY = 'highAccuracy'
    VALID_PROFILES = [LOW_LATENCY, BALANCED, HIGH_ACCURACY]


class ModelState:
    QUEUED = 'queued'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    VALID_STATES = [QUEUED, RUNNING, SUCCEEDED, FAILED]


class TrainingParameters:
    def __init__(self, training_dataset_names: List[str], time_budget_in_minutes: int, model_kind: str, model_profile: str = ModelProfile.BALANCED) -> None:
        assert training_dataset_names
        assert time_budget_in_minutes > 0
        assert model_kind in ModelKind.VALID_KINDS
        assert model_profile in ModelProfile.VALID_PROFILES

        self.training_dataset_names = training_dataset_names
        self.time_budget_in_minutes = time_budget_in_minutes
        self.model_kind = model_kind
        self.model_profile = model_profile

        self._params = {
            'TrainingDatasetNames': self.training_dataset_names,
            'TimeBudgetInMinutes': self.time_budget_in_minutes,
            'ModelKind': self.model_kind,
            'ModelProfile': self.model_profile
        }

    @property
    def params(self) -> dict:
        return self._params


class Model:
    def __init__(self, name: str, trainingParams: TrainingParameters) -> None:
        assert name
        self.name = name
        self.training_params = trainingParams

    @property
    def params(self) -> dict:
        return {'TrainingParameters': self.training_params.params}


class ModelResponse(Model):
    def __init__(
            self, name: str, trainingParams: TrainingParameters, training_cost_in_minutes: int, state: str, model_performance: dict, created_date_time: str, last_modified_date_time: str,
            failure_error_code: str, error_message: str) -> None:
        super().__init__(name, trainingParams)
        self.training_cost_in_minutes = training_cost_in_minutes
        self.state = state
        self.model_performance = model_performance
        self.created_date_time = created_date_time
        self.last_modified_date_time = last_modified_date_time
        self.failure_error_code = failure_error_code
        self.error_message = error_message

    @staticmethod
    def from_response(json):
        train_params_dict = json['trainingParameters']
        training_params = TrainingParameters(train_params_dict['trainingDatasetNames'], train_params_dict['timeBudgetInMinutes'], train_params_dict['modelKind'], train_params_dict['modelProfile'])
        return ModelResponse(
            json['name'],
            training_params, json.get('trainingCostInMinutes'),
            json['state'],
            json.get('modelPerformance'),
            json['createdDateTime'],
            json['lastModifiedDateTime'],
            json.get('failureErrorCode'),
            json.get('errorMessage'))
