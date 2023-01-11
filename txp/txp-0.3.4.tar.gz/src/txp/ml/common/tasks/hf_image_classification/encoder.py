from txp.common.ml.tasks import ClassificationLabelDefinition
from txp.ml.common.tasks.encoder import Encoder
from transformers import AutoFeatureExtractor
from typing import Dict, Any, List
from PIL import Image
import datasets
import pandas as pd
import numpy as np
import io
import json
import logging


class HFImageClassificationEncoder(Encoder):
    """This HuggingFace Encoder for Image Classification is responsible
    for:

        - Using the Feature Extractor to process images into
            data understood by the model.
        - Offer transformations from pandas structured datasets into
            Hugging Face datasets

    Note: The code can be generalized using the AutoFeatureExtractor:
        https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoFeatureExtractor

    """

    def __init__(
        self,
        model_name_or_path: str,
        classification_label: ClassificationLabelDefinition,
        schema: Dict,
    ):
        super(HFImageClassificationEncoder, self).__init__(schema)
        self._classification_def: ClassificationLabelDefinition = classification_label
        self._model_name_or_path = model_name_or_path

        try:
            # Tries to create the feature extractor
            logging.info(
                f"Trying to create Feature Extractor from: {model_name_or_path}"
            )
            print(f"Trying to create Feature Extractor from: {model_name_or_path}")
            self._extractor = AutoFeatureExtractor.from_pretrained(
                self._model_name_or_path
            )
        except Exception as e:
            logging.error(f"Could not instantiate feature extractor: {e}")

    def _transform_samples_batch(self, samples_batch):
        """This is used as the callback passed to Dataset.with_tranform()
        on the encode"""
        model_inputs = self._extractor(
            [x for x in samples_batch["image"]], return_tensors="pt"
        )

        model_inputs["label"] = samples_batch["label"]
        return model_inputs

    def _transform_pandas_to_prepared_ds(
        self, dataframe: pd.DataFrame, split: str = "train[50%:52%]"
    ) -> datasets.DatasetDict:
        """Transforms an Image Classification Vanilla DataFrame into a
        HuggingFace DatasetDict

        Note: Split string reference
             https://huggingface.co/docs/datasets/v1.11.0/splits.html#percent-slicing-and-rounding
        """

        def encode_image_feature(pil_img, feature):
            try:
                return feature.encode_example(pil_img)
            except:
                return None

        # Transforms the PIL Image values to Image Feature from datasets lib
        # https://github.com/huggingface/datasets/issues/4796
        feature = datasets.Image(decode=True)
        dataframe["image"] = dataframe["image"].apply(
            lambda img_pil: encode_image_feature(img_pil, feature)
        )

        # Transforms pandas into Dataset type
        dataframe_filtered = dataframe[dataframe.image.notnull()]
        dataset_vanilla = datasets.Dataset.from_pandas(dataframe_filtered, split=split)
        prepared_ds = dataset_vanilla.with_transform(self._transform_samples_batch)
        prepared_ds.features["image"] = datasets.Image(decode=True, id=None)

        return prepared_ds

    def build_training_dataset(self, target="", **kwargs) -> datasets.DatasetDict:
        """
        Args:
            target: Deprecated arg. TODO: Remove this deprecated arg from the signatures.
            **kwargs:
                - df: The pandas dataframe with raw Tranxpert data.

        Returns:
            datasets.DatasetDict to train.

        """

        def parse_label(label_str: str) -> int:
            labeled_value = json.loads(label_str)["label_value"]
            return self._classification_def.label_to_int[frozenset(labeled_value)]

        images_signals_df = kwargs["df"]
        images_clf_dataset = self._transform_bq_dataset_to_image_classification(
            images_signals_df, ["Image"]
        )
        images_clf_dataset["label"] = images_clf_dataset["label"].map(parse_label)
        hf_ds = self._transform_pandas_to_prepared_ds(images_clf_dataset)
        return hf_ds

    def _signal_completed_transform(
        self,
        signal_completed: Dict,
        edge_logical_id: str,
        perception: str,
        table_id: str
    ) -> [Any, None]:
        try:
            image = [
                int(x)
                for x in signal_completed[edge_logical_id][
                    perception
                ][table_id][0]["data"][0]
            ]
            image = np.frombuffer(bytes(image), dtype=np.uint8)
            image_b = bytes(image)
            image_pil: Image = Image.open(io.BytesIO(image_b))
            return image_pil

        except Exception:
            return None

    def _transformed_input_to_policy_input(self, inputs: List[Any]) -> Any:
        hf_inputs = self._extractor(inputs, return_tensors="pt")
        logging.info(
            f"Inputs transformed by {self.__class__.__name__} encode:"
            f" {len(hf_inputs['pixel_values'])}"
        )

        return hf_inputs
