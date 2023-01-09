from typing import Dict
import warnings

try:
    import joblib
except ImportError as ipt_e:
    warnings.warn(
        "import joblib were error, "
        "please install this pkg manually or use command: pip install 'python-metaai[sklearn]'"
    )
    raise ipt_e


from ... import Model
from ...utils import success_response, failed_response_with_break


MODEL_EXTENSIONS = (".joblib", ".pkl", ".pickle")
ENV_PREDICT_PROBA = "PREDICT_PROBA"


class SKLearnModel(Model):  # pylint:disable=c-extension-no-member
    def __init__(self, name: str):
        super().__init__(name)
        self._model = None

    def load(self) -> bool:
        self._model = joblib.load(self.model_path)
        self.ready = True
        return self.ready

    def predict(self, request: Dict) -> Dict:
        instances = request["instances"]
        try:
            result = self._model.predict(instances).tolist()
            return success_response({"predictions": result})
        except Exception as e:
            failed_response_with_break(message=str(e))
