from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable, List, Sequence, Tuple, Type, Union
import unicodedata

import numpy as np
import numpy.typing as npt
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers import BertTokenizerFast
from transformers import PreTrainedModel
from transformers import PreTrainedTokenizerFast
from transformers import RobertaTokenizerFast

from truera.client.nn import BaselineType
from truera.client.nn import Batch
from truera.client.nn import wrappers as base
from truera.client.nn.wrappers import Wrapping
from truera.client.nn.wrappers.nlp import Types
from truera.client.nn.wrappers.nlp import Wrappers
from truera.client.nn.wrappers.torch import Backend
from truera.client.nn.wrappers.torch import Torch
from truera.client.util.func_utils import compose
from truera.client.util.iter_utils import iter_csv
from truera.client.util.iter_utils import LenIterable

PathOrName = Union[Path, str]


def path_and_name(path_or_name: PathOrName) -> Tuple[Path, str]:
    if isinstance(path_or_name, Path):
        path = path_or_name
        name = str(path_or_name)
    else:
        path = Path.cwd()
        name = path_or_name

    return path, name


class Process:
    """
    Data processing utilities that are common to huggingface models. Some things
    might be more general and could be moved out of here in the future.
    """

    class Unicode:
        """
        Unicode-related preprocessing.
        """

        @staticmethod
        def to_ascii(s: str) -> str:
            """Replace unicode characters with their ascii approximations."""

            return unicodedata.normalize('NFKD',
                                         s).encode('ascii',
                                                   'ignore').decode('ascii')

    class Strip:
        """
        Utilities for stripping strings of certain elements.
        """

        r_html_tag = re.compile(
            r'[<＜][^>＞]*[>＞]'
        )  # some unicode greater/less than signs included

        @staticmethod
        def html(s: str) -> str:
            """
            Strip away html tags but not text between them.
            """
            return Process.Strip.r_html_tag.sub('', s)

        @staticmethod
        def unicode(s: str) -> str:
            """
            Strip away unicode characters.
            """
            return s.encode('ascii', 'ignore')


class TruHugsTokenizer(Wrappers.TokenizerWrapper):
    """
    Implements TokenizerWrapper requirements that are common for all hugging
    face tokenizers.
    """

    @Wrapping.require_init
    def __init__(
        self,
        model_path: PathOrName,
        hugs_class: Type[PreTrainedTokenizerFast],
        n_tokens: int = None,
        *args,
        **kwargs
    ):
        """Wrap the given huggingface fast tokenizer."""

        path, name = path_and_name(model_path)

        hugs = hugs_class.from_pretrained(name)
        if n_tokens is None:
            n_tokens = hugs.model_max_len  # this might be a bit too much for default?

        self.__hugs: PreTrainedTokenizerFast = hugs

        # for us
        self._sep_token_id = hugs.sep_token_id
        self._cls_token_id = hugs.cls_token_id
        self._mask_token_id = hugs.mask_token_id

        # Get vocab and added vocab from hugging face tokenizer:
        vocab = {k: v for k, v in self.__hugs.get_vocab().items()}
        vocab2 = self.__hugs.get_added_vocab()
        vocab.update(vocab2)

        super().__init__(
            model_path=path,
            vocab=vocab,
            unk_token_id=hugs.unk_token_id,
            pad_token_id=hugs.pad_token_id,
            n_tokens=n_tokens,
            *args,
            **kwargs
        )

        # TODO: still cannot enforce that the parent init happens before methods that require it like this one below:
        self._add_special_token_ids(
            [self._sep_token_id, self._cls_token_id, self._mask_token_id]
        )

    # For our baselines.
    @Wrapping.utility
    @property
    def cls_token_id(self) -> Types.TokenId:
        return self._cls_token_id

    # For our baselines.
    @Wrapping.utility
    @property
    def sep_token_id(self) -> Types.TokenId:
        return self._sep_token_id

    # NLP.TokenizerWrapper requirement
    @Wrapping.protected
    def inputbatch_of_textbatch(
        self, texts: Types.TextBatch
    ) -> Types.InputBatch:
        if isinstance(texts, np.ndarray):
            texts = list(texts)
        assert isinstance(texts, List) and len(texts) > 0 and isinstance(
            texts[0], str
        ), f"unexpected input type {type(texts)}, wanted List[str]"

        inputs = self.__hugs.__call__(
            texts,
            padding="max_length",
            max_length=self.n_tokens,
            truncation=True,
            return_tensors="pt"
        )

        device = Torch.get_device()
        input_ids: Backend.Words = Backend.Words(inputs.input_ids.to(device))
        attention_mask: Backend.Batchable = Backend.Batchable(
            inputs.attention_mask.to(device)
        )

        return Types.InputBatch(
            args=[input_ids], kwargs=dict(attention_mask=attention_mask)
        )

    # NLP.TokenizerWrapper requirement
    @Wrapping.protected
    def tokenize_into_tru_tokens(
        self, texts: Types.TextBatch
    ) -> Types.TruTokenization[Types.Token]:

        parts = self.__hugs.batch_encode_plus(
            list(texts),
            padding="max_length",
            max_length=self.n_tokens,
            truncation=True,
            return_tensors='np',  # numpy
            return_offsets_mapping=True,  # required for spans
            return_token_type_ids=False,  # don't need these
            return_attention_mask=True  # require for TruTokenization
        )

        input_idss: npt.NDArray[np.int] = parts['input_ids']

        tokenss = [
            self.__hugs.batch_decode(input_ids) for input_ids in input_idss
        ]
        offsetss = parts['offset_mapping']

        spanss = [
            [
                Types.Span(item=t, begin=o[0], end=o[1])
                for t, o in zip(tokens, offsets)
            ]
            for tokens, offsets in zip(tokenss, offsetss)
        ]

        return Types.TruTokenization(
            spans=spanss,
            token_ids=input_idss,
        )


class TruHugsLoadWrapper(Wrappers.ModelLoadWrapper):
    """
    Model load wrapper for loading huggingface models. User needs to provide the
    model class and tokenizer class.
    
        - _get_model_class - the actual transformers model from their repo like
          RobertaForSequenceClassification
        - _get_tokenizer_class - the tokenizer used for the model, e.g.
          BertTokenizerWrapper
    """

    # our requirement
    @Wrapping.required
    @abstractmethod
    def _get_model_class(self) -> Type[PreTrainedModel]:
        pass

    # our requirement
    @Wrapping.required
    @abstractmethod
    def _get_tokenizer_class(self) -> Type[TruHugsTokenizer]:
        pass

    # NLP.ModelLoadWrapper requirement
    @Wrapping.protected
    def get_tokenizer(self, n_tokens: int = None) -> TruHugsTokenizer:
        tokenizer_class: Type[TruHugsTokenizer] = self._get_tokenizer_class()

        tokenizer = tokenizer_class(
            model_path=self.model_path, n_tokens=n_tokens
        )

        return tokenizer

    # NLP.ModelLoadWrapper requirement
    @Wrapping.protected
    def get_model(self) -> Backend.Model:
        model_class: Type[PreTrainedModel] = self._get_model_class()

        model = model_class.from_pretrained(str(self.model_path))
        model = model.to(Torch.get_device())

        return model


class TruHugsRunWrapper(
    base.Wrappers.ModelRunWrapper.WithBinaryClassifier,
    Wrappers.ModelRunWrapper.WithEmbeddings, Wrappers.ModelRunWrapper
):
    """
    Model run wrappers for huggingface models. 
    """

    # Base.ModelRunWrapper requirement
    # args and kwargs intentionally not allowed to expand over lists, dicts:
    # Ignored in the trulens version as we use get_model_wrapper there.
    # TODO: merge with the above so it can be used in trulens
    @classmethod
    def evaluate_model(
        cls, model: Backend.Model, inputs: Types.InputBatch
    ) -> Types.OutputBatch:
        # TODO: is no_grad useful here?

        with torch.no_grad():
            model_out = model(*inputs.args, **inputs.kwargs)

            logits = model_out.logits if hasattr(
                model_out, "logits"
            ) else model_out

            if hasattr(model_out, "probits"):
                probits = model_out.probits
            else:
                probits = torch.nn.functional.softmax(logits, dim=-1)

            return Types.OutputBatch(probits=probits.cpu().detach().numpy())

    # TODO: Can this be deprecated? Baselines are for influences, which should use customer model.
    # TODO: should be a requirement but not yet noted that way
    # TODO: finish type hint.
    # NLP.ModelRunWrapper requirement
    @classmethod
    def get_baseline(
        cls,
        model: PreTrainedModel,
        tokenizer: TruHugsTokenizer,
        ref_token: Types.TokenLike,
        baseline_type: BaselineType = BaselineType.FIXED,
        attention_mask=None
    ):
        """ref_token: str or float or int, if str or int, represents baseline
        embedding value; if str, represent baseline token
        """

        # lots of torch-specific stuff
        ref_token_id = torch.LongTensor([tokenizer.id_of_tokenlike(ref_token)])

        if ref_token_id == tokenizer.unk_token_id:
            raise ValueError(
                f"Reference token {ref_token} decodes to the same id as the unknown token ({ref_token_id}). "
                f"It is likely that reference token does not exist in the vocabulary."
            )

        if baseline_type == BaselineType.FIXED:
            baseline_input_ids = torch.unsqueeze(
                ref_token_id.repeat(tokenizer.n_tokens), 0
            )
            ### all ref_token_id
        else:
            pad_token_id = torch.LongTensor([tokenizer.pad_token_id])
            # A token used for generating token reference
            cls_token_id = torch.LongTensor([tokenizer.cls_token_id])
            if baseline_type == BaselineType.CLS_PAD:
                baseline_input_ids = torch.unsqueeze(
                    torch.cat(
                        (
                            cls_token_id,
                            pad_token_id.repeat(tokenizer.n_tokens - 1)
                        )
                    ), 0
                )

            elif baseline_type == BaselineType.DYNAMIC:
                assert attention_mask is not None

                input_length = attention_mask.shape[1]
                sep_token_id = torch.LongTensor(
                    [tokenizer.sep_token_id]
                )  # A token used as a separator between question and text and it is also added to the end of the text.

                lengths = attention_mask.detach().cpu().sum(-1).numpy(
                )  # sentence length extracted from attention_mask

                baseline_input_ids = cls._construct_input_baseline(
                    lengths,
                    input_length=input_length,
                    ref_token_id=ref_token_id,
                    sep_token_id=sep_token_id,
                    cls_token_id=cls_token_id,
                    pad_token_id=pad_token_id
                )

        word_ids = Backend.Words(baseline_input_ids.to(Torch.get_device()))
        baseline_embeddings = Backend.Embeddings(
            cls._get_embedder(model)(word_ids)
        )

        if isinstance(ref_token, float) or isinstance(ref_token, int):
            if baseline_type == BaselineType.FIXED:
                baseline_embeddings = torch.ones_like(
                    baseline_embeddings
                ) * ref_token
            elif baseline_type == BaselineType.DYNAMIC:
                for li, length in enumerate(lengths):
                    baseline_embeddings[li, 1:length - 1, :] = ref_token

        return baseline_embeddings

    # Base.ModelRunWrapper.WithBinaryClassifier requirement
    @staticmethod
    def convert_model_eval_to_binary_classifier(
        ds_batch: Types.DataBatch,
        model_eval_output_or_labels: Types.OutputBatch,
        labels: bool = False
    ) -> Backend.Outputs:
        # DOGFOOD: fix and update docs or make out of scope
        """
        [Optional] Only used if post_model_filter_splits is used. See README on
        run_configuration.yml This method returns batched binary evaluations to
        help determine model performance. The value should be between 0 and 1,
        with 1 indicating a "truth" value. This method is used to create
        post_model_filters This method already contains the
        model_eval_output_or_labels to save compute time

        If labels=True, the explainer will send the labels from
        trubatch_of_databatch["labels"] into model_eval_output_or_labels.
        
        Input
        ----------------
        - ds_batch: contains a batch of data from the dataset. This is an
          iteration of SplitLoadWrapper.get_ds .
        - model: the model object. This is the output of ModelWrapper.get_model
        - model_eval_output: the output of ModelWrapper.evaluate_model. this is
          precomputed to save time.
        ----------------
        Output
        ----------------
        - predictions - batched binary predictions
        - labels - batched binary labels
        ----------------
        """

        # TODO: temporarily binarizes into class 0 vs rest.

        if labels:
            return model_eval_output_or_labels != 0
        else:
            return np.argmax(model_eval_output_or_labels.probits, -1) != 0

    # NLP.ModelRunWrapper.WithEmbedding requirement:
    @classmethod
    def get_embeddings(
        cls, model: PreTrainedModel, word_ids: Backend.Words
    ) -> Backend.Embeddings:
        return Backend.Embeddings(cls._get_embedder(model)(word_ids))

    # Our requirements:
    @staticmethod
    def _get_embedder(model: PreTrainedModel) -> torch.nn.Module:
        raise NotImplementedError(
            "Abstract method was called. You might need to change your staticmethods into classmethods."
        )

    # Our implementations:
    @staticmethod
    def _construct_input_baseline(
        lengths, input_length, ref_token_id, sep_token_id, cls_token_id,
        pad_token_id
    ):

        # repeat that works correctly if size is non-positive
        safe_repeat = lambda tensor, size: tensor.repeat(
            size
        ) if size > 0 else torch.LongTensor()
        ##baseline -> [CLS] + [ref_token_id] * length + [SEP] + [PAD] * (input_length(128) - length)

        ref_input_ids = torch.cat(
            [
                torch.unsqueeze(
                    torch.cat(
                        (
                            cls_token_id, safe_repeat(ref_token_id,
                                                      length - 2), sep_token_id,
                            safe_repeat(pad_token_id, input_length - length)
                        ), 0
                    ), 0
                ) for length in lengths
            ], 0
        )

        return ref_input_ids


@dataclass
class TruHugsDataBatch(Types.DataBatch):
    text: np.ndarray = Batch.field(factory=np.array)
    label: np.ndarray = Batch.field(factory=np.array)
    ids: np.ndarray = Batch.field(factory=np.array)


class TruNLPSplitLoadWrapper(Wrappers.SplitLoadWrapper):

    @Wrapping.utility
    def remove_urls(self, series: pd.Series) -> pd.Series:
        """
        Remove http/https indicated urls from the Series of strings.
        """
        return series.str.replace(r"https?:\/\/\S+", "",
                                  regex=True).str.split().str.join(" ")

    @Wrapping.required
    @abstractmethod
    def _process_dataframe(self, df: pd.DataFrame) -> TruHugsDataBatch:
        """
        A Truera specific and custom helper function that runs any preprocessing
        on the dataframe. Usually column renames. Returns the modified df as
        well as the text for storage.

        Args:
            df (pd.DataFrame): A custom dataframe loaded from truera sources
        Returns:
            TruHugsDataBatch -- contents of the dataframe in dataclass
        """
        ...

    def get_ds(self,
               batch_size: int = 1024,
               num_records: int = sys.maxsize) -> LenIterable[Types.DataBatch]:
        """
        Load a split in a lazy manner producing batches of size `batch_size`.       
        """

        # Doing the tokenization later as there are two different endpoints
        # (model vs. truera) that have slightly different tokenization
        # parameters.

        return iter_csv(
            path=self.data_path / "dataset.csv",
            chunksize=batch_size,
            index_col=0,
            nrows=num_records,
            encoding="L1"
        ).map(self._process_dataframe)

    def standardize_databatch(
        self, ds_batch: Types.DataBatch
    ) -> Types.StandardBatch:
        assert isinstance(
            ds_batch, Types.DataBatch
        ), f"data batch was a {type(ds_batch)} instead of DataBatch subclass"
        # expected fields:
        #  - text
        #  - label
        #  - ids

        return Types.StandardBatch(
            ids=ds_batch.ids,
            labels=ds_batch.label,
            text=ds_batch.text,
        )


class TruNLPCounterfactualSplitLoadWrapper(TruNLPSplitLoadWrapper):
    """
    A SplitLoadWrapper that produces TextBatch from get_ds (instead of
    NLP.Types.DataBatch).
    """

    def _process_labels(self, labels: pd.Series) -> Sequence[int]:
        raise NotImplementedError()

    def _process_dataframe(self, df: pd.DataFrame) -> Types.TextBatch:
        df['index'] = df.index.astype(int)

        labels: np.ndarray = np.zeros_like(df.index)

        # cannot return a full TruBatch without all the required fields
        return TruHugsDataBatch(
            ids=df['index'].to_numpy(),
            label=labels,
            text=df['Text'].to_numpy(),
        )


class TruHugsRobertaTokenizerWrapper(TruHugsTokenizer):

    def __init__(self, *args, **kwargs):
        # Should only be called by ModelLoadWrapper which provides n_tokens.
        TruHugsTokenizer.__init__(
            self, hugs_class=RobertaTokenizerFast, *args, **kwargs
        )


class TruHugsBertTokenizerWrapper(TruHugsTokenizer):

    def __init__(self, *args, **kwargs):
        # Should only be called by ModelLoadWrapper which provides n_tokens.
        TruHugsTokenizer.__init__(
            self, hugs_class=BertTokenizerFast, *args, **kwargs
        )


class NLP:

    class SplitLoadWrapper:

        class Sequences(Wrappers.SplitLoadWrapper):
            """
            Creates a SplitLoadWrapper from a sequence of strings and labels.
            Has capability to `shuffle` as well as its `seed`, and text
            processing via a sequence of callables `process`.
            """

            def __init__(
                self,
                texts: Sequence[Types.Text],
                labels: Sequence[int],
                shuffle: bool = False,
                seed: int = 0xdeadbeef,
                process: list = lambda t: t
            ):
                super().__init__(Path.cwd())

                if isinstance(process, Iterable):
                    process = compose(process)

                texts = np.array(texts)
                texts_processed = np.array([process(t) for t in texts])
                labels = np.array(labels)

                if shuffle:
                    np.random.seed(seed)

                    indices = np.random.permutation(len(texts))
                    texts = texts[indices]
                    texts_processed = texts_processed[indices]
                    labels = labels[indices]

                self.__texts = texts
                self.__texts_processed = texts_processed
                self.__labels = labels

            def get_ds(self, batch_size: int = 1024):

                everything = TruHugsDataBatch(
                    ids=np.arange(len(self.__texts)),
                    text=self.__texts_processed,
                    label=self.__labels
                )

                return everything.batch(batch_size=batch_size)

    class TokenizerWrapper:

        class Pretrained(TruHugsTokenizer):

            def __init__(
                self,
                model_path: PathOrName,
                n_tokens: int = None,
                *args,
                **kwargs
            ):
                # Should only be called by ModelLoadWrapper which provides n_tokens.
                TruHugsTokenizer.__init__(
                    self,
                    hugs_class=AutoTokenizer,
                    n_tokens=n_tokens,
                    model_path=model_path,
                    *args,
                    **kwargs
                )

        class Preloaded(TruHugsTokenizer):

            def __init__(
                self,
                tokenizer: AutoTokenizer,
                n_tokens: int = None,
                *args,
                **kwargs
            ):
                # Should only be called by ModelLoadWrapper which provides n_tokens.
                TruHugsTokenizer.__init__(
                    self,
                    hugs_class=AutoTokenizer,
                    n_tokens=n_tokens,
                    model_path=None,
                    *args,
                    **kwargs
                )

    class ModelLoadWrapper:

        class Pretrained(Wrappers.ModelLoadWrapper):
            # nlp.Wrappers.ModelLoadWrapper requirement
            def get_tokenizer(self, n_tokens: int = None):
                tokenizer = NLP.TokenizerWrapper.Pretrained(
                    model_path=self.model_path, n_tokens=n_tokens
                )

                return tokenizer

            # nlp.Wrappers.ModelLoadWrapper requirement
            def get_model(self):
                model = AutoModelForSequenceClassification.from_pretrained(
                    self.model_path
                )
                model = model.to(Torch.get_device())

                return model

        class Preloaded(Wrappers.ModelLoadWrapper):

            def __init__(
                self, model: PreTrainedModel, tokenizer: PreTrainedTokenizerFast
            ):
                super().__init__(model_path=None)

                self._model = model
                self._tokenizer = tokenizer

            # nlp.Wrappers.ModelLoadWrapper requirement
            def get_tokenizer(self, n_tokens: int = None):

                tokenizer_wrapper = NLP.TokenizerWrapper.Preloaded(
                    n_tokens=n_tokens, tokenizer=self._tokenizer
                )

                return tokenizer_wrapper

            # nlp.Wrappers.ModelLoadWrapper requirement
            def get_model(self):
                model = self._model.to(Torch.get_device())

                return model

    class ModelRunWrapper:

        @staticmethod
        def AutoWrapper(n_tokens: int,
                        n_embeddings: int) -> Type[Wrappers.ModelRunWrapper]:

            class AutoWrapped(TruHugsRunWrapper):

                def __init__(self):
                    super().__init__(
                        n_tokens=n_tokens, n_embeddings=n_embeddings
                    )

                # TruHugsRunWrapper requirement
                @staticmethod
                def _get_embedder(
                    model: AutoModelForSequenceClassification
                ) -> torch.nn.Module:
                    # TODO: generalize
                    return model.bert.embeddings.word_embeddings

            return AutoWrapped
