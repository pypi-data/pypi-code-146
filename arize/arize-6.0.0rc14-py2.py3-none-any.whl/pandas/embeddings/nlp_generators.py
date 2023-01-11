from functools import partial
from typing import Dict, Optional, cast

import numpy as np
import pandas as pd

from .base_generators import NLPEmbeddingGenerator
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


class EmbeddingGeneratorForNLPSequenceClassification(NLPEmbeddingGenerator):
    def __init__(self, model_name: str = "distilbert-base-uncased", **kwargs):
        super(EmbeddingGeneratorForNLPSequenceClassification, self).__init__(
            use_case=UseCases.NLP.SEQUENCE_CLASSIFICATION,
            model_name=model_name,
            **kwargs,
        )

    def generate_embeddings(
        self, df: pd.DataFrame, text_col: str, class_label_col: Optional[str] = None
    ) -> pd.Series:
        if type(df) != pd.DataFrame:
            raise TypeError("df must be a pandas DataFrame")
        if type(text_col) != str:
            raise TypeError("text_col must be a string")
        if not text_col or text_col not in df.columns:
            raise ValueError("text_col must be a column of the dataframe")
        if class_label_col and class_label_col not in df.columns:
            raise ValueError(
                "class_label_col must be a column of the dataframe containing "
                "classification labels"
            )

        if class_label_col:
            prepared_text_series = df[[text_col, class_label_col]].apply(
                lambda row: row[text_col] + f" The "
                f"classification label is {row[class_label_col]}.",
                axis=1,
            )
            ds = Dataset.from_pandas(
                pd.DataFrame(prepared_text_series, columns=[text_col]),
                preserve_index=False,
            )
        else:
            ds = Dataset.from_pandas(df[[text_col]], preserve_index=False)
        ds.set_transform(partial(self.tokenize, text_col=text_col))
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
        # Select CLS token vector
        embeddings = outputs.last_hidden_state[:, 0, :]
        return {"embedding_vector": embeddings.cpu().numpy()}
