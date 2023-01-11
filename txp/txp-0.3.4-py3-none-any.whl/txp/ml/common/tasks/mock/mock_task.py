from typing import Dict, Any, List

from txp.ml.common.tasks.policy import Policy
from txp.ml.common.tasks.task import Task
from txp.ml.common.tasks.encoder import Encoder
import pandas as pd


class MockTask(Task):

    def __init__(self, task_definition=None, credentials_str=None):

        schema = None
        if task_definition is not None:
            schema = task_definition.schema_

        policy = MockPolicy()
        super().__init__(MockEncoder(schema), policy, task_definition, credentials_str)
        self.ready = True
        print("MockTask is ready.")

    def predict(self, sampling_window_rows) -> tuple:
        print(f"MockTask prediction request.")
        return self.task_definition.label_def.int_to_label[0]

    def train(self, dataset):
        self.policy.train(dataset, self.encoder.target)


class MockEncoder(Encoder):

    def _transformed_input_to_policy_input(self, inputs: List[Any]) -> Any:
        pass

    def _signal_completed_transform(self, signal_completed: Dict, edge_logical_id: str, perception: str,
                                    table_id: str) -> [Any, None]:
        pass

    def __init__(self, schema):
        super().__init__(schema)

    def transform_input_signals(self, signals_completed) -> pd.DataFrame:
        """
            At this moment we don't need to make predictions for Mock driver
        """
        return pd.DataFrame()

    def build_training_dataset(self, tables, target):
        """
            At this moment we don't need to make predictions for Mock driver
        """
        return pd.DataFrame()


class MockPolicy(Policy):

    def __init__(self, policy_file: str = None):
        super().__init__(policy_file)
        self.clf = None

    def name(self):
        return "MockPolicy"

    def train(self, dataset, target, test_size=0.3):
        """
            At this moment we don't need to make actual predictions
        """
        self.accuracy = 1
        self.trained = True

    def predict(self, tensor):
        """
           At this moment we don't need to make actual predictions
        """
        return None
