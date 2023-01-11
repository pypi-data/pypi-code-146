from abc import ABC, abstractmethod
from dataclasses import dataclass
from txp.common.utils import signals_utils, bigquery_utils
import pandas as pd
from typing import Any, Dict, Union, List
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@dataclass
class EncoderStorage:
    schema: dict
    dataset: any
    target: str


class Encoder(ABC):
    """An encoder is a required piece to create a Task.

    The encoder provides functionality for data transformations:
        a) Database tables dataframe -> Task expected dataframe
        b) Task expected dataframe -> Policy expected in-memory data

    This base Encoder implements transformations for the "a)" step.
    Currently supported:
        - BigQuery Database table to Image Classification dataset:
            self._transform_bq_dataset_to_image_classification()

    The children classes should implement the following contract:
        - self._signal_completed_transform():
            Transforms a SINGLE signal_completed dictionary to the policy understandable data

        - self._transformed_input_to_policy_input():
            Map the inputs array to the compatible grouped data input
                for the policy at runtime (training/prediction)

        - self.build_training_dataset():
            Builds a training dataset for a Task that uses the encoder.
    """

    # TODO: Why is this an attribute of the class definition?
    dataset = None

    def __init__(self, schema):
        self.schema = schema
        self.target = None

    def save(self) -> EncoderStorage:
        return EncoderStorage(self.schema, None, self.target)

    def load(self, encoder_storage: EncoderStorage):
        print("Restoring encoder")
        self.dataset = encoder_storage.dataset
        self.schema = encoder_storage.schema
        self.target = encoder_storage.target

    def set_schema(self, schema):
        self.schema = schema

    def transform_input_signals(self, signals_completed: Dict) -> Any:
        """Transforms the received raw signals into Policy understandable data.

        Note: the signals completed data is based on the Firestore structure for
            the SignalSegregator class.

        Args:
            signals_completed: filled Firestore dictionary, this dict contains all the rows present
                in bigquery tables.
        Returns:
            Any data type compatible with the right policy at runtime.
        """
        transformations = []

        for key_edge_logical_id, value_perceptions in self.schema.items():
            for key_percept, sch_values in value_perceptions.items():
                for table_id in sch_values:
                    if table_id:
                        if (
                            table_id
                            in signals_completed[key_edge_logical_id][key_percept]
                        ):
                            transformations.append(
                                self._signal_completed_transform(
                                    signals_completed,
                                    key_edge_logical_id,
                                    key_percept,
                                    table_id,
                                )
                            )

        # Discard None elements.
        transformations = list(filter(lambda t: t is not None, transformations))

        return self._transformed_input_to_policy_input(transformations)

    ############################################
    # Abstract methods contract
    ############################################
    @abstractmethod
    def _signal_completed_transform(
        self,
        signal_completed: Dict,
        edge_logical_id: str,
        perception: str,
        table_id: str,
    ) -> [Any, None]:
        """Transforms a SINGLE signal_completed dictionary to the policy understandable data.

        Note: the signals completed data is based on the Firestore structure for
            the SignalSegregator class.

        Args:
            signal_completed: filled Firestore dictionary, this dict contains all the rows present
                in bigquery tables.
        Returns:
            Any data type compatible with the right policy at runtime.
            None if some error is catched.
        """
        pass

    @abstractmethod
    def _transformed_input_to_policy_input(self, inputs: List[Any]) -> Any:
        """Map the inputs array to the compatible grouped data input
        for the policy at runtime.

        Args:
            inputs: Array of elements, where each element is an output of self._signal_completed_transform()

        Returns:
            The compatible grouped data input for the policy at runtime
        """
        pass

    @abstractmethod
    def build_training_dataset(self, target, **kwargs) -> Any:
        """Builds a training dataset for a Task that uses the encoder.

        TODO: remove `target` arg. Isn't really necessary.

        Args:
            **kwargs expected by the encoder implementation.

        Returns:
            Returns any Dataset format used in by the Task. For example:
                pandas.DataFrame, HuggingFace datasets.Dataset, etc.

        """
        pass

    ############################################
    # Base transformations
    ############################################

    def _transform_bq_dataset_to_image_classification(
        self, dataframe: pd.DataFrame, perceptions=None
    ) -> pd.DataFrame:
        """This private method provides functionality to children classes to convert
        a Raw Data Dataframe to an Image Classification Dataset.

        Args:
            dataframe: A pandas DataFrame generated with raw data from persistence layer.
            perceptions: The list of Perception Names to be processed from the raw data dataframe.
                Example: ["Image", "ThermalImage"]

        Returns
            A pandas Dataframe for Image Classification Tasks, with columns:
                - image: Contains a PIL Image in memory.
                - observation_timestamp: Contains the observation timestamp for the image.
                - perception_name: Contains the perception_name for the image
                - label: contains the label column value from the database.
        """
        if perceptions is None:
            perceptions = ["Image"]

        # Drop whatever unrecognized perception
        dataframe = dataframe[dataframe.perception_name.isin(perceptions)]

        # Group Images by Signal Timestamp
        images_signals_grouped = dataframe.groupby("signal_timestamp")
        images_df = []

        for signal_timestamp, signal_grp_df in images_signals_grouped:
            all_chunks = signal_grp_df.to_dict("records")
            signal = signals_utils.merge_signal_chunks(all_chunks)

            try:
                image = bigquery_utils.get_image_from_raw_data(
                    signal["data"], lower_quality=False
                )
            # Todo: implement concrete error handling
            except Exception as e:
                logging.warning(f"Unknown error while creating Image in-memory: {e}")
                logging.warning(
                    f"Could not create in-memory image for raw data. Observation Timestamp: "
                    f"{signal.get('observation_timestamp', None)}. "
                    f"Perception: {signal.get('perception_name', None)}"
                )
                continue

            else:
                images_df.append(
                    {
                        "image": image,
                        "observation_timestamp": signal["observation_timestamp"],
                        "perception_name": signal["perception_name"],
                        "label": signal["label"],
                    }
                )

        log.info(
            f"Created Image Classification Dataframe from raw data with {len(images_df)} images"
        )

        df = pd.DataFrame(
            images_df,
            columns=["image", "observation_timestamp", "perception_name", "label"],
        )

        self.dataset = df
        self.target = "label"

        return df
