from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import xgboost as xgb
from txp.ml.common.tasks.policy import Policy
from txp.ml.common.tasks.task import Task
from txp.ml.common.tasks.vibration_baseline.encoder import VibrationEncoder


class VibrationBasicTask(Task):

    def __init__(self, task_definition=None, credentials_str=None, decision_tree_policy=False):

        schema = None
        task_file = None
        if task_definition is not None:
            schema = task_definition.schema_
            task_file = task_definition.task_data

        policy = VibrationDecisionTreePolicy()
        if not decision_tree_policy:
            parameters = None
            if task_definition is not None:
                parameters = task_definition.parameters
            policy = VibrationGradientBoostPolicy(parameters)

        super().__init__(VibrationEncoder(schema), policy, task_definition, credentials_str)

        if task_file is not None and credentials_str is not None:
            self.load_from_bucket(task_file)

            if schema is not None:
                self.encoder.set_schema(schema)

        self.ready = True
        print("VibrationBasicTask is ready.")

    def predict(self, sampling_window_rows) -> tuple:
        """
            Args:
                sampling_window_rows: filled firestore dictionary, this dict contains all the rows present
                                   in bigquery tables.
            Returns:
                Predicted VibrationBasicEvent.
        """
        print(f"VibrationBasicTask prediction request.")
        prediction_dataset = self.encoder.transform_input_signals(sampling_window_rows)
        return self.task_definition.label_def.int_to_label[int(self.policy.predict(prediction_dataset)[0])]

    def train(self, dataset):
        self.policy.train(dataset, self.encoder.target)


class VibrationDecisionTreePolicy(Policy):

    def __init__(self, policy_file: str = None):
        super().__init__(policy_file)
        if self.clf is None:
            self.clf = DecisionTreeClassifier()

    def name(self):
        return "VibrationDecisionTreePolicy"

    def train(self, dataset, target, test_size=0.3):
        features_col = list(dataset.columns)
        features_col.remove(target)
        x = dataset[features_col]
        y = dataset[target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=0)

        self.clf = self.clf.fit(x_train, y_train)
        y_prediction = self.clf.predict(x_test)

        self.accuracy = metrics.accuracy_score(y_test, y_prediction)
        self.set_wrong_predictions(x_test, y_test, y_prediction)
        self.trained = True

    def predict(self, tensor):
        if self.is_trained():
            return self.clf.predict(tensor)
        else:
            return None


class VibrationGradientBoostPolicy(Policy):

    def __init__(self, parameters=None):
        if parameters is None:
            self.param = {
                'max_depth': 1000,
                'eta': 1,
                'objective': 'multi:softmax',
                'num_class': 4,
                'num_round': 10
            }
        else:
            self.param = parameters
        super().__init__()

    def name(self):
        return "VibrationGradientBoostPolicy"

    def train(self, dataset, target, test_size=0.3):
        features_col = list(dataset.columns)
        features_col.remove(target)
        x = dataset[features_col]
        y = dataset[target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=0)

        train_matrix = xgb.DMatrix(x_train.values, y_train.values)
        test_matrix = xgb.DMatrix(x_test.values)

        params = self.param.copy()
        params.pop("num_round", None)

        self.clf = xgb.train(params, train_matrix, self.param["num_round"])
        y_prediction = self.clf.predict(test_matrix)

        self.accuracy = metrics.accuracy_score(y_test, y_prediction)
        self.set_wrong_predictions(x_test, y_test, y_prediction)
        self.trained = True

    def predict(self, tensor):
        if self.is_trained():
            matrix_to_predict = xgb.DMatrix(tensor.values)
            return self.clf.predict(matrix_to_predict)
        else:
            return None
