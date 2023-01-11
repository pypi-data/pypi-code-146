"""AlgoSquare Model API."""
from __future__ import annotations

import io
import json
import pandas as pd
import numpy as np
import time

from typing import Any, Optional, Union

from .api import ApiObject, api_post, api_get, api_delete
from .common import upload_dataframe

def get_deployed():
    """
    Gets all deployed models.
    
    Returns:
        List of Models.
    """
    return [Model.load(x) for x in api_get('api/models/deployments')]

class Model(ApiObject):
    """Base class for all models."""
    def __init__(self, entry):
        if type(self) == Model:
            raise RuntimeError('base class should not be instantiated')
        super().__init__(entry)

    @staticmethod
    def get(model_id: str) -> Model:
        """
        Gets specific model.
        
        Args:
            model_id: string.

        Returns:
            Model.
        """
        return Model.load(api_get(f'api/models/{model_id}'))

    @staticmethod
    def load(entry) -> Union[TabularClassifier, TabularRegressor]:
        base_class = entry['base_class']
        if base_class in ('TabularClassifier', 'TabularClassificationAlgo'):
            return TabularClassifier(entry)
        elif base_class in ('TabularRegressor', 'TabularRegressionAlgo'):
            return TabularRegressor(entry)
        else:
            raise ValueError('unknown base_class')

    def refresh(self) -> None:
        """reloads model."""
        self.update(api_get(f'api/models/{self.model_id}'))

    def tag(self, tag: str) -> None:
        self.update(api_post(f'api/models/{self.model_id}/tag', tag))

    def deploy(self, wait: bool = True) -> None:
        """
        Deploys model.

        Args:
            wait: blocks until model has deployed if true.

        Raises:
            RuntimeError.
        """
        if self.status != 'stopped':
            raise RuntimeError('status must be stopped')

        self.update(api_post(f'api/models/{self.model_id}/deployment'))

        if wait:
            while self.status == 'pending_deployment':
                time.sleep(30)
                self.refresh()

    def discharge(self, wait: bool = False) -> None:
        """
        Discharges model.

        Args:
            wait: blocks until model has discharged if true.

        Raises:
            RuntimeError.
        """
        if self.status != 'running':
            raise RuntimeError('status must be running')

        self.update(api_delete(f'api/models/{self.model_id}/deployment'))

        if wait:
            while self.status == 'pending_discharge':
                time.sleep(30)
                self.refresh()

    def prediction_update(self, prediction_id: str, actual: Union[str, int, float]) -> dict:
        """
        Updating model.
        
        Args:
            prediction_id: output from model.predict.
            actual: observed target.

        Raises:
            RuntimeError.
        """
        if self.status != 'running':
            raise RuntimeError('status must be running')

        return api_put(f'api/models/{self.model_id}/predictions/{prediction_id}', data = json.dumps(actual))

    def derive_task(self, method: str = 'auto', value: Optional[Union[float, int]] = None) -> Task:
        """
        Derive task with subset of features.
        
        Args:
            method: feature selection method - 'auto', 'number', 'proportion' or 'significance'.
            value: in (0, 1) for 'proportion' and 'significance', int otherwise.

        Raises:
            RuntimeError, ValueError.
        """
        if method not in ('auto', 'number', 'proportion', 'significance'):
            raise ValueError('invalid method')

        feature_importance = self.results.get('feature_importance')

        if not feature_importance:
            raise RuntimeError('feature_importance is missing')

        if method != 'auto':
            if value is None:
                raise ValueError('invalid value')

            if method in ('proportion', 'significance'):
                if value <= 0 or value >= 1:
                    raise ValueError('value must be in (0, 1)')

            if method in ('number', 'proportion'):
                if method == 'number':
                    n = int(value)
                else:
                    n = int(len(feature_importance) * value)

                if n <= 0:
                    raise ValueError('no features selected')
                if n >= len(feature_importance):
                    raise ValueError('all features selected')

        payload = dict(method = method)
        if method != 'auto':
            payload['value'] = value

        from .task import Task
        return Task(api_post(f'api/models/{self.model_id}/tasks', json=payload))

    def _predict(self, data, prediction_method):
        if self.status != 'running':
            raise RuntimeError('status must be running')

        if prediction_method not in self.prediction_methods:
            raise NotImplementedError(f'{prediction_method} not implemented in model')

        return api_post(f'api/models/{self.model_id}/predictions', data = json.dumps(dict(data = data, prediction_method = prediction_method)))

    def _predict_batch(self, data, prediction_method, upload_func):
        if self.status != 'running':
            raise RuntimeError('status must be running')

        if prediction_method not in self.prediction_methods:
            raise NotImplementedError(f'{prediction_method} not implemented in model')

        files = upload_func(data)
        payload = dict(prediction_method = prediction_method, files = files)

        return api_post(f'api/models/{self.model_id}/batch', data = json.dumps(payload))


class TabularClassifier(Model):
    """Tabular classifier class."""
    def predict(self, data):
        """
        Using deployed model to make single prediction.
        
        Args:
            data: dict

        Returns:
            dict.

        Raises:
            NotImplementedError, RuntimeError, TypeError.
        """
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')

        return self._predict(data, 'predict')

    def predict_batch(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Using deployed model to make batch prediction.
        
        Args:
            data: DataFrame

        Returns:
            DataFrame.

        Raises:
            NotImplementedError, RuntimeError, TypeError.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError('data must be a dataframe')

        return _batch_to_df(self._predict_batch(data, 'predict', _upload_tabular_inputs))

    def predict_proba(self, data: dict) -> dict:
        """
        Using deployed model to output class probabilities.
        
        Args:
            data: dict

        Returns:
            dict.

        Raises:
            NotImplementedError, RuntimeError, TypeError.
        """
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')

        return self._predict(data, 'predict_proba')

    def predict_proba_batch(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Using deployed model to output class probabilities for batch.
        
        Args:
            data: DataFrame

        Returns:
            DataFrame.

        Raises:
            NotImplementedError, RuntimeError, TypeError.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError('data must be a dataframe')

        return _batch_to_df(self._predict_batch(data, 'predict_proba', _upload_tabular_inputs))

    def decision_function(self, data: dict) -> dict:
        """
        Using deployed model to output decision function.
        
        Args:
            data: dict

        Returns:
            dict.

        Raises:
            NotImplementedError, RuntimeError, TypeError.
        """
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')

        return self._predict(data, 'decision_function')

    def decision_function_batch(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Using deployed model to output decision function for batch.

        Args:
            data: DataFrame

        Returns:
            DataFrame.

        Raises:
            NotImplementedError, RuntimeError, TypeError.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError('data must be a dataframe')

        return _batch_to_df(self._predict_batch(data, 'decision_function', _upload_tabular_inputs))

class TabularRegressor(Model):
    """Tabular regressor class."""
    def predict(self, data: dict) -> dict:
        """
        Using deployed model to make single prediction.
        
        Args:
            data: dict

        Returns:
            dict.

        Raises:
            NotImplementedError, RuntimeError, TypeError.
        """
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')

        return self._predict(data, 'predict')

    def predict_batch(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Using deployed model to make batch prediction.
        
        Args:
            data: DataFrame

        Returns:
            DataFrame.

        Raises:
            NotImplementedError, RuntimeError, TypeError.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError('data must be a dataframe')

        return _batch_to_df(self._predict_batch(data, 'predict', _upload_tabular_inputs))

def _batch_to_df(response):
    with io.StringIO(response['data']) as buffer:
        return pd.read_csv(buffer, index_col = 0)

def _upload_tabular_inputs(data):
    return [dict(namespace = 'inputs', key = upload_dataframe('inputs', data))]
