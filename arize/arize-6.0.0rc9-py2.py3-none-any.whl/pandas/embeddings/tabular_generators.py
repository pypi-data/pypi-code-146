from functools import partial
from typing import Callable, List, Optional, cast

import pandas as pd

from .base_generators import TabularEmbeddingGenerator
from .usecases import UseCases
from .utils import is_list_of, logger

try:
    import torch
    from datasets import Dataset
except ImportError:
    raise ImportError(
        "To enable embedding generation, "
        "the arize module must be installed with the EmbeddingGeneration option: "
        "pip install 'arize[EmbeddingGeneration]'."
    )


class EmbeddingGeneratorForTabularFeatures(TabularEmbeddingGenerator):
    # def __repr__(self):
    #     uc = self.use_case.split(".")
    #     return (
    #         f"This is EmbeddingGenerator for {uc[0]} {uc[1]} with model = "
    #         f"{self.model_name}, and max_length = {self.max_length}"
    #     )

    def __init__(
        self,
        model_name="xlm-roberta-large",
        prompt_fn=None,
        return_prompt_col: bool = False,
        **kwargs,
    ):
        super(EmbeddingGeneratorForTabularFeatures, self).__init__(model_name, **kwargs)
        self.__use_case = self._parse_use_case(UseCases.NLP.SEQUENCE_CLASSIFICATION)
        self.__prompt_fn = prompt_fn
        self.__return_prompt_col = return_prompt_col

    @property
    def use_case(self) -> str:
        return self.__use_case

    @property
    def prompt_fn(self) -> Callable:
        return self.__prompt_fn if self.__prompt_fn else self.default_prompt_fn

    @property
    def return_prompt_col(self) -> bool:
        return self.__return_prompt_col

    def tokenize(self, batch, text_col):
        return {
            k: v.to(self.device)
            for k, v in self.tokenizer(
                batch[text_col],
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt",
            ).items()
        }

    def generate_embeddings(
        self, df: pd.DataFrame, columns: Optional[List[str]] = None
    ) -> pd.Series:
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

        # if self.return_prompt_col:
        #     res_df = ds.to_pandas()
        #     return res_df["embedding_vector"], res_df[prompt_col]

        return cast(pd.DataFrame, ds.to_pandas())["embedding_vector"]

    def __get_embedding_vector(
        self,
        batch,
    ):
        with torch.no_grad():
            outputs = self.model(**batch)
        # (batch_size, seq_length/or/num_tokens, hidden_size)
        # Select avg token vector
        embeddings = torch.mean(outputs.last_hidden_state, 1)
        return {"embedding_vector": embeddings.cpu().numpy()}
