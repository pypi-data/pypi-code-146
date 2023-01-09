"""
Building a sequential MultiLayerPerceptron from a given config file
"""

# Imports
from typing import List
import yaml
# noinspection PyPackageRequirements
from keras import Sequential
# noinspection PyPackageRequirements
from keras.layers import Dense, Dropout, Normalization
# noinspection PyPackageRequirements
from keras.optimizers import Adam, Adadelta, Adamax, Adagrad, Nadam, RMSprop, SGD, Ftrl

import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter('%(log_color)s[%(levelname).1s %(log_color)s%(asctime)s] - %(log_color)s%(name)s - '
                             '%(message)s')
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)

"""
Author: vickyparmar
File: build_sequential_mlp.py
Created on: 06-10-2022, Thu, 11:38:34

Last modified by: vickyparmar
Last modified on: 13-10-2022, Thu, 17:00:21
"""


# [ ] ToDo: Documentation


# Class SequentialMLP
class SequentialMLP:
    """
        Initializing a class instance.

        Parameters
        ----------
        config_path: str
            Path to a yaml file containing the config.

        Methods
        -------
        method1(param='abcd')
            Description of method 1.
        method2(param=xyz)
            Description of method 2.

        Raises
        ------
        type of Exception raised
            Description of raised exception.

        See Also
        --------
        othermodule : Other module to see.

        Notes
        -----
        In Progress

        Examples
        --------
        >>> builder = SequentialMLP('config_file.yaml')
        >>> mlp = builder.get_mlp()
        >>> mlp.summary()
        """

    def __init__(self, config_path: str):
        self.config = yaml.safe_load(open(config_path, 'rb'))
        self.model_name = 'MLP'
        if 'model_name' in self.config.keys():
            self.model_name = self.config['model_name']

    # Building Layers
    def build_layers(self) -> List:
        """
        Building layers according to the config file.
        Returns
        -------
        layers: List
            A list of keras layers with a specified config.
        """
        layer_config = self.config['layers']
        final_layers = []
        for k, v in layer_config.items():
            if 'input' in k:
                if 'input_shape' not in v.keys():
                    logger.warning("Input shape not found in the config file. Model will not be build."
                                   "To Build the model please run `model.build(input_shape)`.")
                if v['name'] == 'Normalization':
                    final_layers.append(Normalization(**v))
                elif v['name'] == 'Dense':
                    final_layers.append(Dense(**v))
                else:
                    logger.error('', exc_info=True)
                    raise ValueError(
                        f"First layer can be either Normalization or Dense."
                    )

            elif "output" in k:
                if v['name'] == 'Dense':
                    final_layers.append(Dense(**v))
                else:
                    logger.error('', exc_info=True)
                    raise ValueError(
                        f"Only Dense output supported for the time being."
                    )

            else:
                if 'dense' in k:
                    final_layers.append(Dense(**v))
                elif "dropout" in k:
                    final_layers.append(Dropout(**v))
                else:
                    logger.error('', exc_info=True)
                    raise ValueError(
                        f"Only Dense and Dropout layers supported for now."
                    )
        return final_layers

    # Compiling the model
    def compile_mlp(self) -> Sequential:
        """
        Calls the build_mlp method and compiles the model based on the config file.
        Returns
        -------
        compiled_model: Sequential
            A compiled model with the configuration from the config file.
        """
        optim = self.config["optimizer"]
        compile_params = self.config["compile_params"]
        if optim['name'].lower() == 'adam':
            opt = Adam(**optim)
        elif optim['name'].lower() == 'sgd':
            opt = SGD(**optim)
        elif optim['name'].lower() == 'rmsprop':
            opt = RMSprop(**optim)
        elif optim['name'].lower() == 'adadelta':
            opt = Adadelta(**optim)
        elif optim['name'].lower() == 'adamax':
            opt = Adamax(**optim)
        elif optim['name'].lower() == 'adagrad':
            opt = Adagrad(**optim)
        elif optim['name'].lower() == 'nadam':
            opt = Nadam(**optim)
        elif optim['name'].lower() == 'ftrl':
            opt = Ftrl(**optim)
        else:
            logger.error("Please specify a valid optimizer")
            raise ValueError(
                f"Please provide a valid optimizer. Choices: [`adam`, `sgd`, `rmsprop`, "
                f"`adadelta`, `adamax`, `adagrad`, `nadam`, `ftrl`]"
            )

        mlp = self.build_mlp()
        mlp.compile(optimizer=opt, **compile_params)
        return mlp

    # Building MLP
    def build_mlp(self) -> Sequential:
        """
        Calls the build_layers method and builds a Sequential model
        Returns
        -------
        mlp_model: Sequential
            A non-compiled Sequential model built with the layers from the config.
        """
        layers = self.build_layers()
        mlp = Sequential(layers=layers, name=self.model_name)
        return mlp

    # Build and return the model
    def get_mlp(self) -> Sequential:
        if self.config['compile']:
            return self.compile_mlp()
        logger.warning("Returning a non-compiled, non-built model. The input_shape parameter in the input layer is "
                       "missing. Either modify the config file, or perform `model.build(input_shape)` before compiling"
                       "the model.")
        return self.build_mlp()
