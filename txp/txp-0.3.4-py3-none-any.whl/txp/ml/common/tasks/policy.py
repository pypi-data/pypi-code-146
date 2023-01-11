from abc import ABC, abstractmethod
from joblib import dump, load
from dataclasses import dataclass


@dataclass
class PolicyStorage:
    handler: any
    trained: bool
    accuracy: float


class Policy(ABC):

    def __init__(self, policy_file=None):

        if policy_file is not None:
            print(f"Restoring policy from {policy_file}")
            self.clf = load(policy_file)
            self.trained = True
        else:
            self.trained = False
            self.clf = None
        self.accuracy = -1
        self.failed_predictions = []

    @abstractmethod
    def train(self, dataset, target, test_size=0.3):
        pass

    @abstractmethod
    def predict(self, tensor):
        pass

    @abstractmethod
    def name(self):
        pass

    def save(self) -> PolicyStorage:
        return PolicyStorage(self.clf, self.trained, self.accuracy)

    def load(self, policy_storage: PolicyStorage):
        print("Restoring policy")
        self.clf = policy_storage.handler
        self.trained = policy_storage.trained
        self.accuracy = policy_storage.accuracy

    def is_trained(self):
        return self.trained

    def set_wrong_predictions(self, x_test, y_test, y_predicted):
        self.failed_predictions = []
        for i in range(len(y_test)):
            if y_predicted[i] != y_test.iloc[i]:
                self.failed_predictions.append({
                    "observation_timestamp": str(x_test.iloc[i]["observation_timestamp"]),
                    "predicted_label": y_predicted[i],
                    "real_label": y_test.iloc[i]
                })
