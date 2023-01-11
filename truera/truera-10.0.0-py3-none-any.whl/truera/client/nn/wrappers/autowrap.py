from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Union

from truera.client.cli.verify_nn_ingestion.nlp import NLPAutowrapVerifyHelper
from truera.client.nn.wrappers import nlp
from truera.client.nn.wrappers.nlp import Types
from truera.client.nn.wrappers.nlp import Wrappers as NLP


class SplitLoadWrapper(NLP.SplitLoadWrapper):
    standardize_databatch_fn = None

    def __init__(
        self, data_path: str, ds_from_source: Callable,
        standardize_databatch: Callable
    ):
        super().__init__(data_path)
        self.ds_from_source = ds_from_source
        self.standardize_databatch_fn = standardize_databatch

    def get_ds(self) -> Iterable:
        return self.ds_from_source(self.get_data_path())

    def standardize_databatch(
        self, ds_batch: Types.DataBatch
    ) -> Types.StandardBatch:
        standard_batch = self.standardize_databatch_fn(ds_batch)
        return Types.StandardBatch(**standard_batch)


class ModelLoadWrapper(NLP.ModelLoadWrapper):

    def __init__(
        self, model_path: str, get_model: Callable, **tokenizer_args: dict
    ):
        super().__init__(model_path=model_path)
        self._get_model = get_model
        self.tokenizer_args = tokenizer_args

    def get_tokenizer(self, n_tokens: int) -> NLP.TokenizerWrapper:
        return TokenizerWrapper(
            model_path=self.model_path,
            n_tokens=n_tokens,
            **self.tokenizer_args
        )

    def get_model(self) -> Callable:
        return self._get_model(self.get_model_path())


class ModelRunWrapper(NLP.ModelRunWrapper):

    def __init__(self, n_tokens, n_embeddings, eval_model: Callable):
        super().__init__(n_tokens=n_tokens, n_embeddings=n_embeddings)
        self.eval_model = eval_model

    def evaluate_model(
        self, model: Callable, inputs: NLP.Types.InputBatch
    ) -> NLP.Types.OutputBatch:
        if self.eval_model:
            out = self.eval_model(model, inputs.args, inputs.kwargs)
        else:
            out = model(*inputs.args, **inputs.kwargs)
        return NLP.Types.OutputBatch(probits=out)


class TokenizerWrapper(NLP.TokenizerWrapper):

    def __init__(
        self,
        model_path: Union[str, Path],
        vocab: Dict[Types.Token, Types.TokenId],
        n_tokens: int,
        unk_token_id: int,
        pad_token_id: int,
        text_to_inputs: Callable,
        text_to_token_ids: Callable,
        text_to_spans: Callable,
        special_tokens: Optional[List[Types.TokenId]] = None,
    ):
        super().__init__(
            model_path=model_path,
            vocab=vocab,
            n_tokens=n_tokens,
            unk_token_id=unk_token_id,
            pad_token_id=pad_token_id,
            special_tokens=special_tokens
        )

        self.text_to_inputs = text_to_inputs
        self.text_to_token_ids = text_to_token_ids
        self.text_to_spans = text_to_spans

    def inputbatch_of_textbatch(
        self, texts: Iterable[str]
    ) -> NLP.Types.InputBatch:
        inputs = self.text_to_inputs(texts)
        return NLP.Types.InputBatch(
            args=inputs['args'], kwargs=inputs['kwargs']
        )

    def tokenize_into_tru_tokens(
        self, texts
    ) -> NLP.Types.TruTokenization[NLP.Types.Token]:
        tokenss = self.text_to_token_ids(texts)
        if not callable(self.text_to_spans):
            spans = None
        else:
            offsetss = self.text_to_spans(texts)
            spans = [
                [
                    NLP.Types.Span(
                        item=self.vocab_inverse[t], begin=o[0], end=o[1]
                    ) for t, o in zip(tokens, offsets)
                ] for tokens, offsets in zip(tokenss, offsetss)
            ]
        return NLP.Types.TruTokenization(token_ids=tokenss, spans=spans)


def autowrap(
    *,
    # general args
    n_tokens: int,
    n_embeddings: int,
    # split load wrapper args
    ds_from_source: Callable,
    standardize_databatch: Callable,
    # load wrapper args
    get_model: Callable,
    # tokenizer args
    vocab: Dict[str, int],
    unk_token_id: int,
    pad_token_id: int,
    special_tokens: List[int],
    text_to_inputs: Callable,
    text_to_token_ids: Callable,
    # Optional args
    eval_model: Optional[Callable] = None,
    text_to_spans: Optional[Callable] = None,
    model_path: Optional[Union[str, Path]] = None,
    data_path: Optional[Union[str, Path]] = None
) -> nlp.WrapperCollection:
    """
    Given a number of parameters, automatically create and 
    return a SplitLoadWrapper, ModelLoadWrapper, ModelRunWrapper,
    and TokenizerWrapper, bundled as a WrapperCollection.

    Args:
        n_tokens (int): The sequence size of the model
        n_embeddings (int): The dimensionality of the model's embeddings
        ds_from_source (Callable): Function that loads a dataset into memory from a path
        standardize_databatch (Callable): Function extracting raw text, labels, and ids from the loaded dataset 
        get_model (Callable): Function that loads model into memory from a path
        vocab (Dict[str, int]): Dictionary mapping tokens to their respective IDs
        unk_token_id (int): The token ID of the UNK token
        pad_token_id (int): The token ID of the PAD token
        special_tokens (List[int]): A list of special tokens (i.e CLS, MASK, SEP, PAD) 
        text_to_inputs (Callable): Function given text and returns args and kwargs to pass to `eval_model`
        text_to_token_ids (Callable): Function tokenizing raw text into token IDs
        eval_model (Callable): Function evaluating the model on args and kwargs from `text_to_inputs`. If None, will use model return value
        text_to_spans (Optional[Callable], optional): Function converting raw text into spans. 
            Spans mark the start and end index of each token in the original text.
            If None, token-level influences are still available, but word-level influences will be disabled. Defaults to None.
        model_path (Optional[Union[str, Path]], optional): Path to your model checkpoint. 
            If None, `get_model` is assumed to return a model in memory. Defaults to None.
        data_path (Optional[Union[str, Path]], optional): Path to your dataset. 
            If None, `ds_from_source` is assumed to return a dataset in memory. Defaults to None.

    Returns:
        nlp.WrapperCollection: A container class containing TruEra wrappers
    """
    verify_helper = NLPAutowrapVerifyHelper()
    verify_helper.verify_flow(
        n_tokens=n_tokens,
        ds_from_source=ds_from_source,
        get_model=get_model,
        standardize_databatch=standardize_databatch,
        unk_token_id=unk_token_id,
        pad_token_id=pad_token_id,
        special_tokens=special_tokens,
        text_to_inputs=text_to_inputs,
        text_to_token_ids=text_to_token_ids,
        eval_model=eval_model,
        text_to_spans=text_to_spans,
        model_path=model_path,
        data_path=data_path
    )

    split_load_wrapper = SplitLoadWrapper(
        data_path=data_path,
        ds_from_source=ds_from_source,
        standardize_databatch=standardize_databatch,
    )

    load_wrapper = ModelLoadWrapper(
        model_path=model_path,
        get_model=get_model,
        vocab=vocab,
        unk_token_id=unk_token_id,
        pad_token_id=pad_token_id,
        text_to_inputs=text_to_inputs,
        text_to_token_ids=text_to_token_ids,
        text_to_spans=text_to_spans,
        special_tokens=special_tokens
    )

    run_wrapper = ModelRunWrapper(
        n_tokens=n_tokens, n_embeddings=n_embeddings, eval_model=eval_model
    )

    tokenizer_wrapper = TokenizerWrapper(
        model_path=model_path,
        vocab=vocab,
        n_tokens=n_tokens,
        unk_token_id=unk_token_id,
        pad_token_id=pad_token_id,
        text_to_inputs=text_to_inputs,
        text_to_token_ids=text_to_token_ids,
        text_to_spans=text_to_spans,
        special_tokens=special_tokens
    )

    return nlp.WrapperCollection(
        split_load_wrapper=split_load_wrapper,
        model_load_wrapper=load_wrapper,
        model_run_wrapper=run_wrapper,
        tokenizer_wrapper=tokenizer_wrapper
    )
