import io
from typing import Tuple, List, Dict, Any
import PIL
import numpy as np
import pandas as pd
from PIL import Image
import json
import logging

from txp.common.ml.tasks import ClassificationLabelDefinition
from txp.ml.common.tasks.encoder import Encoder
from txp.ml.common.tasks.slic.slic_patch_image_helpers import SlicPatchImageProcessor
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class SlicPatchRecognitionEncoder(Encoder):
    """Encoder definition for all the task implementations
    that uses the SlicPatch object recognition algorithm.
    """

    def __init__(
            self,
            number_of_segments: int,
            image_shape: Tuple,
            thermal_image_shape: Tuple,
            patch_x_y_image: Tuple,
            patch_x_y_thermal: Tuple,
            pandas_cols: List[str],
            schema: Dict,
            classification_label: ClassificationLabelDefinition,
    ):
        super(SlicPatchRecognitionEncoder, self).__init__(schema)
        self._number_of_segments: int = number_of_segments
        self._image_shape: Tuple = image_shape
        self._thermal_image_shape: Tuple = thermal_image_shape
        self._patch_x_y_image: Tuple = patch_x_y_image
        self._patch_x_y_thermal: Tuple = patch_x_y_thermal
        self._slic_processor: SlicPatchImageProcessor = SlicPatchImageProcessor(
            self._number_of_segments
        )
        self._pandas_cols: List[str] = pandas_cols
        self._classification_def: ClassificationLabelDefinition = classification_label

    def parse_label(self, label_str: str) -> int:
        labeled_value = json.loads(label_str)["label_value"]
        return self._classification_def.label_to_int[frozenset(labeled_value)]

    def transform_image_to_vector(self, image) -> List:
        try:
            return self._slic_processor.process_image_patches(
                np.array(image),
                self._patch_x_y_image[0],
                self._patch_x_y_image[1],
            )
        except Exception:
            logging.warning(f"There was a problem processing a PIL IMAGE. Vector could not be generated.")
            return []

    def build_training_dataset(self, target, **kwargs) -> pd.DataFrame:
        """Builds the training dataset for the task.
        Args
          **kwargs:
            'df' (pandas df): pre processed signals df, after downloading time df, label values are applied
                              and at the end this is de dataframe that we get.

        Returns:
            pandas.DataFrame used to train the Task that uses this encoder.
        """
        images_signals_df = kwargs["df"]
        images_clf_dataset = self._transform_bq_dataset_to_image_classification(
            images_signals_df, ["Image"]
        )

        images_clf_dataset = images_clf_dataset.dropna()
        print(images_clf_dataset)
        images_clf_dataset["label"] = images_clf_dataset["label"].map(self.parse_label)
        # Transforms images to numeric data
        images_clf_dataset["image"] = images_clf_dataset["image"].map(self.transform_image_to_vector)
        images_clf_dataset = images_clf_dataset[images_clf_dataset["image"].map(lambda v: len(v) > 0)]

        return images_clf_dataset

    def _get_slic_vector(self, img_array: np.ndarray, key_percept: str, carry_array: List) -> List[float]:
        """
            TODO: Why are we using `extend` ? Ask.
        """
        if key_percept == "Image":
            if len(carry_array) > 0:
                carry_array.extend(self._slic_processor.process_image_patches(
                    img_array,
                    self._patch_x_y_image[0],
                    self._patch_x_y_image[1]
                ))
            else:
                carry_array = self._slic_processor.process_image_patches(
                    img_array,
                    self._patch_x_y_image[0],
                    self._patch_x_y_image[1]
                )
        elif key_percept == "ThermalImage":
            if len(carry_array) > 0:
                carry_array.extend(
                    self._slic_processor.process_image_patches(
                        img_array,
                        self._patch_x_y_image[0],
                        self._patch_x_y_image[1]
                    )
                )
            else:
                carry_array = self._slic_processor.process_image_patches(
                    img_array,
                    self._patch_x_y_image[0],
                    self._patch_x_y_image[1]
                )

        return carry_array

    @staticmethod
    def _get_image_array(image_data: List) -> np.ndarray:
        image = np.frombuffer(bytes(image_data), dtype=np.uint8)
        image_b = bytes(image)
        try:
            image_pil = Image.open(io.BytesIO(image_b))
            img_np_array = np.array(image_pil)
            return img_np_array
        except PIL.UnidentifiedImageError as e:
            log.error(f"Could not open image: {e}")
            return None

    def _signal_completed_transform(self, signal_completed: Dict, edge_logical_id: str, perception: str,
                                    table_id: str) -> [Any, None]:
        image = [
            int(x) for x in
            signal_completed[edge_logical_id][perception][table_id][0]["data"][0]
        ]
        img_np_array = self._get_image_array(image)
        try:
            if img_np_array is not None and img_np_array.shape != ():
                log.info(f"{self.__class__.__name__} Prediction "
                         f"with image shape: {img_np_array.shape}")
                print(f"{self.__class__.__name__} Prediction "
                      f"with image shape: {img_np_array.shape}")
                vector = self._get_slic_vector(img_np_array, perception, [])
                return vector
            else:
                return None
        except Exception:
            return None

    def _transformed_input_to_policy_input(self, inputs: List[Any]) -> Any:
        dataset = pd.DataFrame()
        dataset = dataset.append([inputs], ignore_index=True)
        return dataset

