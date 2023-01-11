from typing import Dict
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from txp.common.ml.tasks import AssetTask

from txp.ml.common.tasks.slic.encoder import SlicPatchRecognitionEncoder
from txp.ml.common.tasks.policy import Policy
from txp.ml.common.tasks.task import Task
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class SlicPatchRecognitionDecisionTreePolicy(Policy):
    def __init__(self, policy_file: str = None):
        super().__init__(policy_file)
        if self.clf is None:
            self.clf = DecisionTreeClassifier()

    def name(self):
        return self.__class__.name()

    def train(
            self,
            dataset: pd.DataFrame,
            target: str = 'label',
            test_size: float = 0.3,
    ):
        """
        Args:
            dataset: the training dataset MUST have the columns:
                `image`: The features vector of the sample.
                `target`: The label value for the sample (1 or 0)

            target (str): The column name for the targets
            test_size ( float ): The percentage of test data to perform the dataframe split
        """
        x = dataset[['image', 'observation_timestamp']]
        y = dataset[target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=0)
        self.clf = self.clf.fit(x_train["image"].values.tolist(), y_train)
        y_prediction = self.clf.predict(x_test["image"].values.tolist())

        self.accuracy = metrics.accuracy_score(y_test, y_prediction)
        self.set_wrong_predictions(x_test, y_test, y_prediction)
        self.trained = True

    def predict(self, tensor):
        if self.is_trained():
            return self.clf.predict(tensor)
        else:
            return None


class SlicPatchRecognitionTask(Task):
    """General definition for all the task implementations
    that uses the SlicPatch object recognition algorithm.
    """

    def __init__(
            self,
            task_definition=None,
            credentials_str=None,
    ):
        super().__init__(
            self._build_encoder(task_definition),
            self._build_policy(),
            task_definition,
            credentials_str
        )

        if self.task_definition.task_data and credentials_str is not None:
            self.load_from_bucket(self.task_definition.task_data)

            if task_definition.schema_:
                self.encoder.set_schema(task_definition.schema_)

        self.ready = True

        log.info(f"{self.__class__.__name__} instance is ready with file: {self.task_definition.task_data}")

    def _build_encoder(
            self, task_definition: AssetTask
    ) -> SlicPatchRecognitionEncoder:
        """Return a new instance reference to a SlicPatchRecognitionEncoder."""
        return SlicPatchRecognitionEncoder(
            task_definition.parameters['number_of_segments'],
            task_definition.parameters['image_shape'],
            task_definition.parameters['thermal_image_shape'],
            task_definition.parameters['patch_x_y_image'],
            task_definition.parameters['patch_x_y_thermal'],
            task_definition.parameters['pandas_cols'],
            task_definition.schema,
            task_definition.label_def
        )

    def _build_policy(self) -> Policy:
        """Returns the instance reference to the appropriated Policy type."""
        return SlicPatchRecognitionDecisionTreePolicy()

    def predict(self, sampling_window_rows) -> tuple:
        """Returns the prediction results for the given sampling windows
        generated input vectors.

        Args:
            sampling_window_rows: filled Firestore dictionary, this dict
                contains all the rows present in bigquery tables.

        Returns:
            Appropriate enumerated label.
        """
        print(f"{self.__class__.__name__} prediction request.")
        prediction_dataset = self.encoder.transform_input_signals(sampling_window_rows)

        if not prediction_dataset.size:
            return None

        predict_list = list(prediction_dataset.iloc[:, 0])
        return self.task_definition.label_def.int_to_label[
            self.policy.predict(predict_list)[0]
        ]

    def train(self, dataset: pd.DataFrame) -> None:
        self.policy.train(dataset, self.encoder.target)
