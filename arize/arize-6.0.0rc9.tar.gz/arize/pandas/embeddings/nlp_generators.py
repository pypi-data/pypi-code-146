from functools import partial
from typing import cast

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
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"  use_case={self.use_case},\n"
            f"  model_name={self.model_name},\n"
            f"  max_length={self.tokenizer_max_length},\n"
            f"  tokenizer={self.tokenizer.__class__},\n"
            f"  model={self.model.__class__},\n"
            f")"
        )

    def __init__(self, model_name="xlm-roberta-large", **kwargs):
        super(EmbeddingGeneratorForNLPSequenceClassification, self).__init__(
            model_name, **kwargs
        )
        self.__use_case = self._parse_use_case(UseCases.NLP.SEQUENCE_CLASSIFICATION)

    @property
    def use_case(self) -> str:
        return self.__use_case

    def tokenize(self, batch, text_col):
        return self.tokenizer(
            batch[text_col],
            padding=True,
            truncation=True,
            max_length=self.tokenizer_max_length,
            return_tensors="pt"
        ).to(self.device)

    def tokenize2(self, batch, text_col):
        return {
            k: v.to(self.device)
            for k, v in self.tokenizer(
                batch[text_col],
                padding=True,
                truncation=True,
                max_length=self.tokenizer_max_length,
                return_tensors="pt",
            ).items()
        }

    def generate_embeddings(self, df, text_col: str = "") -> pd.Series:
        if type(df) != pd.DataFrame:
            raise TypeError("df must be a pandas DataFrame")
        if type(text_col) != str:
            raise TypeError("text_col must be a string")
        if not text_col or text_col not in df.columns:
            raise ValueError("text_col must be a column of the dataframe")

        ds = Dataset.from_pandas(df[[text_col]])
        ds.set_transform(partial(self.tokenize, text_col=text_col))
        logger.info("Generating embedding vectors")
        ds = ds.map(
            lambda batch: self.__get_embedding_vector(batch),
            batched=True,
            batch_size=self.batch_size,
            num_proc=4
        )
        return cast(pd.DataFrame, ds.to_pandas())["embedding_vector"]

    def generate_embeddings2(self, df, text_col: str = "") -> pd.Series:
        if type(df) != pd.DataFrame:
            raise TypeError("df must be a pandas DataFrame")
        if type(text_col) != str:
            raise TypeError("text_col must be a string")
        if not text_col or text_col not in df.columns:
            raise ValueError("text_col must be a column of the dataframe")

        ds = Dataset.from_pandas(df[[text_col]])
        ds.set_transform(partial(self.tokenize2, text_col=text_col))
        logger.info("Generating embedding vectors")
        ds = ds.map(
            lambda batch: self.__get_embedding_vector(batch),
            batched=True,
            batch_size=self.batch_size,
            num_proc=4
        )
        return cast(pd.DataFrame, ds.to_pandas())["embedding_vector"]

    def __get_embedding_vector(self, batch):
        with torch.no_grad():
            outputs = self.model(**batch)
        # (batch_size, seq_length/or/num_tokens, hidden_size)
        # Select CLS token vector
        embeddings = outputs.last_hidden_state[:, 0, :]
        return {"embedding_vector": embeddings.cpu().numpy()}
