from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import numpy as np
import numpy.typing as npt

from truera.client.nn import Batch
from truera.client.nn import NNBackend as NNB
from truera.client.nn import wrappers as base
from truera.client.nn.wrappers import Wrapping


class Types(base.Types):
    # Timeseries keys:
    #    - ids = array of size (batch x 1) : <ids to pair with records>
    #    - features = array of size (batch x features) : <feature values to which
    #      attributions explain>
    #    - lengths = array of size (batch x 1) : <number of timesteps associated
    #      with each record>
    #    - labels = array of size (batch x 1) : <label of each record>
    @dataclass
    class TruBatch(base.Types.TruBatch):
        ids: npt.NDArray[np.long] = Batch.field(np.array)
        features: npt.NDArray[np.number] = Batch.field(np.array)
        lengths: npt.NDArray[np.long] = Batch.field(np.array)
        preprocessed_features: Optional[npt.NDArray[np.number]] = None

    # TODO: not currently used


class Wrappers(base.Wrappers):

    # Aliased here so help(Timeseries) mentions it.
    Types = Types

    class ModelLoadWrapper(base.Wrappers.ModelLoadWrapper):
        """A model load wrapper used for time series."""

    class SplitLoadWrapper(base.Wrappers.SplitLoadWrapper):
        """A split load wrapper used for time series."""

        @Wrapping.required
        @abstractmethod
        def get_feature_names(self) -> List[str]:
            """
          This gets a list of feature names in the same index as the model
          inputs.

          Output
          ----------------
          - a list of feature names
          ----------------
          """
            ...

        @Wrapping.required
        @abstractmethod
        def get_short_feature_descriptions(self) -> Dict[str, str]:
            """
          This gets a dictionary of feature names to short feature
          descriptions

          Output
          ----------------
          - dictionary of feature names to short feature descriptions
          ----------------
          """
            ...

        @Wrapping.required
        @abstractmethod
        def get_missing_values(self) -> Union[Dict[str, List[Any]], List[str]]:
            """
          This returns either a dictionary of feature names to their
          respective missing feature vals, or it can return a list of features
          that have missing values. In this case, the explanations will
          naively assume the mode value is the missing value.
          
          Output
          ----------------
          - Mapping of features to missing values or list of features with
            missing values.
          ----------------
          """
            ...

    class ModelRunWrapper(base.Wrappers.ModelRunWrapper):
        """
      A model run wrapper used for time series. Static methods only.

      - evaluate_model output shape should be (# in batch, # output timesteps,
        # classes).
      """

        @Wrapping.deprecates(
            "ds_elements_to_truera_elements",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        @Wrapping.required
        @staticmethod
        @abstractmethod
        def trubatch_of_databatch(
            ds_batch: Types.DataBatch, *, model: NNB.Model
        ) -> Types.TruBatch:  # TODO: use hinted type
            """
          This transforms the dataset items into a form that the truera tool
          will use. The form should be a TruBatch of `ids`, `features`,
          `lengths`, `labels` to the batched values. Optional keys are
          `preprocessed_features`. If this is used, the wrapper method
          get_one_hot_sizes must be implemented.

          Example: - trubatch = TruBatch - trubatch.ids = array of
          size (batch x 1) : <index ids to pair with
            records>
          - trubatch.features = array of size (batch x features) :
            <feature values to which attributions explain>
          - trubatch.lengths = array of size (batch x 1) : <number
            of timesteps associated with each record>
          - trubatch.labels = array of size (batch x 1) : <label of
            each record>

          - trubatch.preprocessed_features: Non mandatory. 
          Use this if preprocessing occurs like one hot
          encodings. If using this, trubatch.features feature
          lengths should match the one hot encoding layer size
          trubatch.preprocessed_features = array of size (batch x
          features) : <feature values of preprocessed features before
          encodings>
          
          Input
          ----------------
          - ds_batch: the output of a single iteration over the
            DataWrapper.get_ds object
          - model: the model object. This may be needed if the model does any
            preprocessing.
          ----------------
          Output
          ----------------
          - ds_batch transformed to be used by the Truera Platform. Features,
            lengths, and labels should by numpy ndarrays.
          ----------------
          """
            ...

        class WithOneHot(ABC):
            """
          Run wrapper requirements for models with one hot encodings.
          """

            @staticmethod
            @abstractmethod
            def get_one_hot_sizes() -> Dict[str, int]:
                """
              [Special Use Case, Optional] Only used if one hot encoding takes
              place within the model. The input layer should specify the layer
              containing the one hot encoded tensors. This method should then
              return a mapping of input feature to encoding size. This method
              assumes that the features layer is a single concatenated list of
              all encodings in order of the feature_names.
              """
                ...


@dataclass
class WrapperCollection(base.WrapperCollection):
    pass
    # split_load_wrapper: Wrappers.SplitLoadWrapper
    # model_load_wrapper: Wrappers.ModelLoadWrapper
    # model_run_wrapper: Wrappers.ModelRunWrapper
