from typing import Dict
import warnings

from ... import Model, ModelServer
from ...utils import failed_response_with_break, success_response


try:
    from jpmml_evaluator import make_evaluator
    from jpmml_evaluator.py4j import launch_gateway, Py4JBackend
except ImportError as ipt_e:
    warnings.warn(
        "import jpmml_evaluator were error, please install this pkg manually or use command: "
        "pip install 'python-metaai[pmml]'"
    )
    raise ipt_e


MODEL_EXTENSIONS = ".pmml"


class PmmlModel(Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False
        self.evaluator = None
        self.input_fields = []
        self._gateway = None
        self._backend = None

    def load(self) -> bool:

        self._gateway = launch_gateway()
        self._backend = Py4JBackend(self._gateway)
        self.evaluator = make_evaluator(self._backend, self.model_path).verify()
        self.input_fields = [
            inputField.getName() for inputField in self.evaluator.getInputFields()
        ]
        self.ready = True
        return self.ready

    def predict(self, request: Dict) -> Dict:
        instances = request["instances"]
        try:
            result = [
                self.evaluator.evaluate(dict(zip(self.input_fields, instance)))
                for instance in instances
            ]
            return success_response({"predictions": result})
        except Exception as e:
            failed_response_with_break(message="Failed to predict %s" % e)


if __name__ == "__main__":

    model = PmmlModel(name="custom")

    ModelServer.start(model)
