from functools import partial
from typing import Dict, cast

import numpy as np
import pandas as pd

from .base_generators import CVEmbeddingGenerator
from .usecases import UseCases
from .utils import logger

try:
    import torch
    from datasets import Dataset
except ImportError:
    raise ImportError(
        "To enable embedding generation, "
        "the arize module must be installed with the EmbeddingGeneration option: "
        "pip install 'arize[EmbeddingGeneration]'."
    )


class EmbeddingGeneratorForCVImageClassification(CVEmbeddingGenerator):
    def __init__(self, model_name: str = "google/vit-base-patch32-224-in21k", **kwargs):
        super(EmbeddingGeneratorForCVImageClassification, self).__init__(
            use_case=UseCases.CV.IMAGE_CLASSIFICATION, model_name=model_name, **kwargs
        )

    def generate_embeddings(self, df: pd.DataFrame, image_path_col: str) -> pd.Series:
        if type(df) != pd.DataFrame:
            raise TypeError("df must be a pandas DataFrame")
        if type(image_path_col) != str:
            raise TypeError("image_path_col must be a string")
        if not image_path_col or image_path_col not in df.columns:
            raise ValueError("image_path_col must be a column of the dataframe")

        # Validate that there are no null image paths
        if df[image_path_col].isnull().any():
            raise ValueError(
                f"There can't be any null values in the column: df[{image_path_col}]"
            )

        ds = Dataset.from_pandas(df[[image_path_col]])
        ds.set_transform(
            partial(self.extract_image_features, image_path_col=image_path_col)
        )
        logger.info("Generating embedding vectors")
        ds = ds.map(
            lambda batch: self.__get_embedding_vector(batch),
            batched=True,
            batch_size=self.batch_size,
        )
        return cast(pd.DataFrame, ds.to_pandas())["embedding_vector"]

    def __get_embedding_vector(
        self, batch: Dict[str, torch.Tensor]
    ) -> Dict[str, np.ndarray]:
        with torch.no_grad():
            outputs = self.model(**batch)
        # (batch_size, seq_length/or/num_tokens, hidden_size)
        # Select avg image vector
        embeddings = torch.mean(outputs.last_hidden_state, 1)
        return {"embedding_vector": embeddings.cpu().numpy()}
