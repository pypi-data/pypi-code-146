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
            f"  return_prompt_col={self.return_prompt_col},\n"
            f"  prompt_fn={self.prompt_fn.__name__},\n"
            f")"
        )

    def __init__(
        self,
        model_name: str = "xlm-roberta-large",
        prompt_fn: Optional[Callable] = None,
        return_prompt_col: bool = False,
        **kwargs,
    ):
        super(EmbeddingGeneratorForTabularFeatures, self).__init__(
            use_case=UseCases.STRUCTURED.TABULAR_FEATURES,
            model_name=model_name,
            **kwargs,
        )
        self.__return_prompt_col = return_prompt_col
        self.__prompt_fn = prompt_fn

    @property
    def return_prompt_col(self) -> bool:
        return self.__return_prompt_col

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
            msg += f"The {repl_text} is {row[col]}. "
        return msg.strip(" ")

    def generate_embeddings(
        self, df: pd.DataFrame, columns: Optional[List[str]] = None
    ) -> Union[pd.Series, Tuple[pd.Series, pd.Series]]:
        if type(df) != pd.DataFrame:
            raise TypeError("df must be a pandas DataFrame")
        if not columns:
            columns = [col for col in df.columns]
        if not is_list_of(columns, str):
            raise TypeError("columns must be a list of column names (strings)")
        if not all(col in df.columns for col in columns):
            missing_cols = [col for col in columns if col not in df.columns]
            raise ValueError(
                "columns list must only contain columns of the dataframe. "
                f"The following columns are not found {missing_cols}"
            )

        prompts = df.apply(lambda row: self.prompt_fn(row, columns), axis=1)
        prompt_col = self.prompt_fn.__name__ + "_text"
        ds = Dataset.from_pandas(pd.DataFrame(prompts, columns=[prompt_col]))
        ds.set_transform(partial(self.tokenize, text_col=prompt_col))
        logger.info("Generating embedding vectors")
        ds = ds.map(
            lambda batch: self.__get_embedding_vector(batch),
            batched=True,
            batch_size=self.batch_size,
        )

        if self.return_prompt_col:
            return cast(pd.DataFrame, ds.to_pandas())["embedding_vector"], cast(
                pd.Series, prompts
            )

        return cast(pd.DataFrame, ds.to_pandas())["embedding_vector"]

    def __get_embedding_vector(
        self,
        batch: Dict[str, torch.Tensor],
    ) -> Dict[str, torch.Tensor]:
        with torch.no_grad():
            outputs = self.model(**batch)
        # (batch_size, seq_length/or/num_tokens, hidden_size)
        # Select avg token vector
        embeddings = torch.mean(outputs.last_hidden_state, 1)
        return {"embedding_vector": embeddings.cpu().numpy()}
