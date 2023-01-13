from functools import partial
from typing import Callable, Dict, List, Optional, Tuple, Union, cast

import pandas as pd

from .base_generators import NLPEmbeddingGenerator
from .usecases import UseCases
from .utils import is_list_of, logger

try:
    import torch
    from datasets import Dataset
    from transformers import AutoTokenizer  # type: ignore
except ImportError:
    raise ImportError(
        "To enable embedding generation, "
        "the arize module must be installed with the EmbeddingGeneration option: "
        "pip install 'arize[EmbeddingGeneration]'."
    )


class EmbeddingGeneratorForTabularFeatures(NLPEmbeddingGenerator):
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"  use_case={self.use_case},\n"
            f"  model_name={self.model_name},\n"
            f"  tokenizer_max_length={self.tokenizer_max_length},\n"
            f"  tokenizer={self.tokenizer.__class__},\n"
            f"  model={self.model.__class__},\n"
            f"  prompt_fn={self.prompt_fn.__name__},\n"
            f")"
        )

    def __init__(
        self,
        model_name: str = "xlm-roberta-large",
        prompt_fn: Optional[Callable] = None,
        **kwargs,
    ):
        super(EmbeddingGeneratorForTabularFeatures, self).__init__(
            use_case=UseCases.STRUCTURED.TABULAR_FEATURES,
            model_name=model_name,
            **kwargs,
        )
        self.__prompt_fn = prompt_fn

    @property
    def prompt_fn(self) -> Callable:
        if self.__prompt_fn:
            return self.__prompt_fn
        else:
            return self.default_prompt_fn

    @staticmethod
    def default_prompt_fn(row: pd.DataFrame, columns: List[str]) -> str:
        msg = ""
        for col in columns:
            repl_text = col.replace("_", " ")
            value = row[col]
            if isinstance(value, str):
                value = value.strip()
            msg += f"The {repl_text} is {value}. "
        return msg.strip(" ")

    def generate_embeddings(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rename_cols_mapper: Optional[Dict[str, str]] = None,
        return_prompt_col: Optional[bool] = False,
        method: Optional[str] = "cls"
    ) -> Union[pd.Series, Tuple[pd.Series, pd.Series]]:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")
        if not is_list_of(columns, str):
            raise TypeError("columns must be a list of column names (strings)")
        if not all(col in df.columns for col in columns):
            missing_cols = [col for col in columns if col not in df.columns]
            raise ValueError(
                "columns list must only contain columns of the dataframe. "
                f"The following columns are not found {missing_cols}"
            )
        if rename_cols_mapper is not None:
            if not isinstance(rename_cols_mapper, dict):
                raise TypeError(
                    "rename_cols_mapper must be a dictionary mapping column names to new column "
                    "names"
                )
            for k, v in rename_cols_mapper.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    raise ValueError(
                        "rename_cols_mapper dictionary keys and values should be strings"
                    )
            if not all(col in df.columns for col in rename_cols_mapper.keys()):
                missing_cols = [
                    col for col in rename_cols_mapper.keys() if col not in df.columns
                ]
                raise ValueError(
                    "rename_cols_mapper must only contain keys which are columns of the dataframe. "
                    f"The following columns are not found {missing_cols}"
                )

        if rename_cols_mapper is not None:
            new_cols = [
                rename_cols_mapper[col] if col in rename_cols_mapper.keys() else col
                for col in columns
            ]
            prompts = df.rename(columns=rename_cols_mapper).apply(
                lambda row: self.prompt_fn(row, new_cols), axis=1
            )
        else:
            prompts = df.apply(lambda row: self.prompt_fn(row, columns), axis=1)
        prompt_col_name = self.prompt_fn.__name__ + "_text"
        ds = Dataset.from_pandas(pd.DataFrame(prompts, columns=[prompt_col_name]))
        ds.set_transform(partial(self.tokenize, text_col_name=prompt_col_name))
        logger.info("Generating embedding vectors")
        ds = ds.map(
            lambda batch: self.__get_embedding_vector(batch, method),
            batched=True,
            batch_size=self.batch_size,
        )

        if return_prompt_col:
            return cast(pd.DataFrame, ds.to_pandas())["embedding_vector"], cast(
                pd.Series, prompts
            )

        return cast(pd.DataFrame, ds.to_pandas())["embedding_vector"]

    def __get_embedding_vector(
        self,
        batch: Dict[str, torch.Tensor],
        method
    ) -> Dict[str, torch.Tensor]:
        with torch.no_grad():
            outputs = self.model(**batch)
        # (batch_size, seq_length/or/num_tokens, hidden_size)
        if method == "cls":  # Select CLS token vector
            embeddings = outputs.last_hidden_state[:, 0, :]
        elif method == "avg":  # Select avg token vector
            embeddings = torch.mean(outputs.last_hidden_state, 1)
        else:
            raise ValueError(f"Invalid method = {method}")
        return {"embedding_vector": embeddings.cpu().numpy()}
