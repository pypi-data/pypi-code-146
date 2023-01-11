import abc
from typing import Any, Dict, Optional, Union


class RolloutConfig(abc.ABC):
    def __init__(
        self,
        *,
        project_id: str,
        model_name: Optional[str],
        model_object: Any,
        model_input_sample: Any,
        infer_func_input_format: str,
        infer_func_output_format: str,
        infer_func_input_sample: Any
    ):
        """
        :param project_id: Required. ID of your project. Copy it from cinnaroll web app.
        :param model_name: Optional (can be None). Name of this model version to discern it from other model versions
        in this project.
        :param model_object: Required. Your model's object.
            For Keras models, it has to be a tensorflow.keras.Model or its subclass.
            For PyTorch models, it has to be a subclass of torch.nn.Module.
        :param model_input_sample: Required. Something can pass to your model object's predict function to get
        a prediction.
            For Keras models, it's an argument to model.predict().
            For PyTorch models, it's an argument to myModel() where myModel is an object of your model class.
        :param infer_func_input_format: Required. Input format of your infer() function. One of:
            "json" - JSON-serializable object.
            "file" - arbitrary file that you can open.
        :param infer_func_output_format: Required. Output format of your infer() function. One of:
            "json" - JSON-serializable object.
        :param infer_func_input_sample: Required. Sample that you can pass to your infer function, that is in the format
        of input_format.
        """
        self.project_id = project_id
        self.model_name = model_name
        self.model_object = model_object
        self.model_input_sample = model_input_sample
        self.infer_func_input_format = infer_func_input_format
        self.infer_func_output_format = infer_func_output_format
        self.infer_func_input_sample = infer_func_input_sample
        self.metrics: Optional[Dict[str, Union[float, str]]] = None

    @staticmethod
    @abc.abstractmethod
    def train_eval(model_object: Any) -> Optional[Dict[str, Any]]:
        """
        Paste the code that trains and evaluates your model here, but initialize model object outside this method
        and class. cinnaroll.rollout() will call this function to train and evaluate your model, and save it to disk.
        It is skipped if rollout fails and saved model exists already and is the same as model initialized in code.
        If you're loading a model (for example a pretrained model from disk or web) in your script, you can leave the
        function as is, with just "pass".
        :param model_object: model to be trained.
        :returns dictionary containing metrics in the form of "metric_name": metric_value. You can also include here
        "dataset": "name of dataset" item if you want to indicate that your model was trained on specific dataset or
        version of dataset.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def infer(model_object: Any, input_data: Any) -> Any:
        """
        Function that app cinnaroll builds for you will use to serve inferences. It typically preprocesses input_data,
        feeds it to model_object to get a prediction and formats the prediction into output your app should return.
        Currently, you cannot reference code in local files from this function or code this function depends on, but
        you can reference code from this file, 3rd party libraries, built-in modules and Python lib. Variables that
        this function references must be picklable.
        :param model_object: your model's object.
        :param input_data: data obtained from request to your app, in the format specified by infer_func_input_format.
        :returns data in infer_func_output_format.
        Exceptions raised here will make inference app return the exception's message and error code 500.
        """
        pass
