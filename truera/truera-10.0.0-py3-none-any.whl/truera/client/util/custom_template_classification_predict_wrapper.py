from typing import Dict, Union

import numpy
import pandas


class PredictProbaWrapper(object):

    def __init__(self, model):
        self.model = model

    def predict(
        self, model_input: Union[pandas.DataFrame, Dict[str, numpy.ndarray],
                                 numpy.ndarray]
    ) -> Union[numpy.ndarray, pandas.Series, pandas.DataFrame]:
        """
            This function is a wrapper around your model's predict_proba method.  
            Using the model artifacts that you have loaded, implement this predict function.

        Args:
            model_input (Union[
                pandas.DataFrame, 
                Dict[str, numpy.ndarray (ndim=1)], 
                numpy.ndarray (ndim=2)]): 
                Data that can be given directly to the model.
            
        Returns:
            Union[numpy.ndarray, pandas.Series, pandas.DataFrame]: Model output
        """
        pass

    def get_model(self):
        """
            **Optional**
            Only implement if you are using a model that is supported by truera-tree influence compuations.

        Returns:
            Model Object: Provides an api to access the underlying model structure
        """
        return self.model


def _load_pyfunc(path: str):
    """
        The purpose of this function is to load any serialized components of a given model and return a model wrapper that implements a predict method.
        This function is provided with the path to the model data file/directory that was specified during packaging.
        This function should return an instance of a class implementing a predict method with the signature shown above.  
        
    Args:
        path (str): Contains the path to the serialized model that was provided during packaging.  
            This is specified by the "data" field in the MLmodel file at the root of the packaged model

    Returns:
        PredictWrapper: Instance of the class defined above with an implemented predict method
    """

    loaded_model = "Loaded and Deserialized Model"
    return PredictProbaWrapper(loaded_model)
