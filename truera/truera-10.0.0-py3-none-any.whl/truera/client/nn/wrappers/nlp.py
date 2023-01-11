from __future__ import annotations

from abc import ABC
from abc import abstractmethod
import copy
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Dict, Generic, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union
)

import numpy as np
import numpy.typing as npt

import truera
from truera.client.nn import Batch
from truera.client.nn import NNBackend as NNB
from truera.client.nn import wrappers as base
from truera.client.nn.wrappers import Wrapping
from truera.client.util.func_utils import WrapperMeta


class Types(base.Types):
    Text = str  # raw text inputs, TODO: check for unicode issues

    TokenId = int  # tokens' index into a vocabulary

    Token = str  # canonical representation of a token
    Word = str  # canonical representation of a word
    # Canonical representations may differ than what is in raw text as some
    # inputs get mapped into the same token and sometimes special symbols are
    # added to denote sub-word tokens as being postfixes or not.

    Part = TypeVar("Part", Token, Word)

    TextBatch = Sequence[Text]

    TokenLike = Union[
        Token,
        TokenId]  # tokens are either their readable string or integer index.

    @dataclass
    class Span(Generic[Part]):
        """
        Tokens or words along with indices into the string from which they were
        derived.
        """

        item: Types.Part
        begin: int
        end: int

        @staticmethod
        def of_hugs(
            pair: Tuple[Types.Part, Tuple[int, int]]
        ) -> Types.Span[Types.Part]:
            """
            Convert some structures returned by huggingface parsers/tokenizers into
            a span.
            """
            return Types.Span(item=pair[0], begin=pair[1][0], end=pair[1][1])

    @dataclass
    class StandardBatch(base.Types.StandardBatch):
        """
        Instance data required for Truera NLP product. This standardized data must only come from split.
        """

        # Base has index and labels fields
        text: npt.NDArray[Types.Text] = Batch.field(np.array)  # (batch, )

    @dataclass
    class TruBatch(StandardBatch, base.Types.TruBatch):
        """
        Instance data required for Truera NLP product. For parity with NN generalizability. May get tru elements from data or model.
        """
        ...

    @dataclass
    class TruTokenization(Batch, Generic[Part]):
        # TODO: help(.) is too confusing for this type.
        """
        Outputs of tokenizers used for various aggregation and display purposes.
        Generic in `Part`.
        """

        spans: List[List[Types.Span[Types.Part]]] = Batch.field(
            factory=list, default=None
        )  # None when Part=Token
        token_ids: npt.NDArray[Types.TokenId] = Batch.field(
            factory=np.array, default=None
        )  # None when Part=Word


class Wrappers(base.Wrappers):
    """
    Wrappers for NLP models. In addition to base wrappers, NLP requires a
    tokenizer wrapper. The tokenizer is responsible for final preparation of
    text (string) instaces into the appropriate form accepted by the model.
    Other additions/changes over base wrappers are:

        `ModelLoadWrapper` - `__init__` - each wrapper's initializer must call
          `Wrappers.ModelLoadWrapper`'s initializer specifying `n_tokens` and
          `n_embeddings`, integers indicating the maximum number of tokens the
          model accepts per input instance, and how large is its embedding
          space.

        - `get_tokenizer` - new method loads/retrieves the tokenizer wrapper.
          `ModelRunWrapper` - `trubatch_of_databatch` - process a databatch to
           extract the fields `TruBatch` (see `TruBatch`) requires.

        `SplitLoadWrapper` - no changes from base version `TokenizerWrapper`
          (new wrapper) - `tokenize_into_tru_tokens` - `inputbatch_of_textbatch`
          produces model inputs of the given collection of texts. The method
          `inputbatch_of_databatch` of ModelRunWrapper is implemented for you
          based on this method.

        - (optional) tokenize_into_tru_words - given a collection of texts,
          split them into words along with offsets into the text they come from.
          A default implementation of this method is provided.

        - (optional) visible_token - process string representations of tokens
          into how you'd like them displayed. Default implementation does not do
          any processing.
          
        - (optional) visible_word - process string representations of words into
          how you'd like them displayed. Default implementation does not do any
          processing.
    """

    # Include alias here so help(NLP) mentions it. Types on right refers to
    # `Types` outside of Wrappers defined above.
    Types = Types

    # Can only mix into TokenizerWrapper
    class WithTokenizerWrapperOptional:
        """
        Optional methods to customize some aspects of an NLP analysis. The
        methods defined here come with sensible/noop defaults but can be
        extended in a subclass for alternate behaviour.
        """

        @Wrapping.optional
        def tokenize_into_tru_words(
            self, texts: Iterable[Types.Text]
        ) -> Types.TruTokenization[Types.Word]:
            """
            Split a set of texts, each, into their constituent words. Each
            returned word must come with spanning information into its origin
            string with begining and end indices. Default implementation is a
            whitespace-based splitter using huggingface's
            tokenizers.pre_tokenizers.Whitespace .
            """

            sentences = [
                self._word_splitter.pre_tokenize_str(text) for text in texts  # pylint: disable=E1101
            ]

            return Types.TruTokenization(
                spans=[
                    [Types.Span.of_hugs(p)
                     for p in sentence]
                    for sentence in sentences
                ]
            )

        @Wrapping.optional
        def visible_token(self, token: Types.Token) -> str:
            """
            Render the token for interactive user. By default, no change is made
            from the token's string representation.
            
            Transformers' BertTokenizer has these hashes in some tokens which
            can be removed for visualiztions:
            ```
                if token[:2] == "##":
                    token = token[2:]
                elif token[-2:] == "##":
                    token = token[:-2]
            ```
            """

            return token

        @Wrapping.optional
        def visible_word(self, word: Types.Word) -> str:
            """
            Render the word for interactive user. By default no change is made
            from the word's string representation.
            """
            return word

    # Can only mix into TokenizerWrapper
    class WithTokenizerWrapperUtility:
        """
        Utility methods for helping you with your tokenizer wrapper. These
        cannot be overridden by your wrapper but can be used to simplify
        its construction.
        """

        @Wrapping.utility
        @property
        def model_path(self) -> Path:
            return self._model_path  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def vocab(self) -> Dict[Types.Token, Types.TokenId]:
            return self._vocab  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def vocab_inverse(self) -> Dict[Types.Token, Types.TokenId]:
            return self._vocab_inverse  # pylint: disable=E1101

        @property
        @Wrapping.utility
        def n_tokens(self) -> int:
            """
            Number of tokens a wrapped model expects. This should be
            retrieved from ModelLoadWrapper.
            """
            return self._n_tokens  # pylint: disable=E1101

        @n_tokens.setter
        @Wrapping.utility
        def n_tokens(self, val: int) -> None:
            self._n_tokens = val  # pylint: disable=E1101

        @Wrapping.utility
        def _add_special_token_ids(self, ids: Iterable[Types.TokenId]) -> None:
            self._special_token_ids += ids  # pylint: disable=E1101
            self._special_tokens += [self.token_of_id(id) for id in ids]  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def special_tokens(self) -> List[Types.TokenId]:
            """
            Special tokens are those who do not arise from text itself.
            """
            return self._special_tokens  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def special_token_ids(self):
            """
            Special tokens are those who do not arise from text itself.
            """
            return self._special_token_ids  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def unk_token_id(self) -> Types.TokenId:
            """
            Unknown token. Tokenizers typically return this token in place of
            any token they are not aware of.
            """
            return self._unk_token_id  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def pad_token_id(self) -> Types.TokenId:
            """
            Pad token 'pad' the postfix of a tokenization to make them some
            fixed length.
            """
            return self._pad_token_id  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def unk_token(self) -> Types.Token:
            """
            Unknown token. Tokenizers typically return this token in place of
            any token they are not aware of.
            """
            return self._unk_token  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def pad_token(self) -> Types.Token:
            """
            Pad token 'pad' the postfix of a tokenization to make them some
            fixed length.
            """
            return self._pad_token  # pylint: disable=E1101

        @Wrapping.utility
        def tokens_of_text(self,
                           text: Types.Text) -> List[Types.Span[Types.Token]]:
            """
            Tokenize a single piece of text.
            """
            return self.tokens_of_texts([text])[0]  # pylint: disable=E1101

        @Wrapping.utility
        def words_of_text(self,
                          text: Types.Text) -> List[Types.Span[Types.Word]]:
            """
            Tokenize into words a single piece of text.
            """
            return self.words_of_texts([text])[0]  # pylint: disable=E1101

        @Wrapping.utility
        def ids_of_tokens(
            self, tokens: Iterable[Types.Token]
        ) -> Iterable[Types.TokenId]:
            """
            Given tokens' string representations, produce their ids.
            """
            return [
                self.vocab[token] if token in self.vocab else self.unk_token_id
                for token in tokens
            ]

        @Wrapping.utility
        def id_of_token(self, token: Types.Token) -> Types.TokenId:
            """
            Get the token id of a single token string representation.
            """
            return self.ids_of_tokens([token])[0]

        @Wrapping.utility
        def tokens_of_ids(
            self, ids: Iterable[Types.TokenId]
        ) -> Iterable[Types.Token]:
            """
            Given a sequence of token ids, produce the corresponding sequence of
            tokens as strings.
            """
            return [self.vocab_inverse[token_id] for token_id in ids]

        @Wrapping.utility
        def token_of_id(self, id: Types.TokenId) -> Types.Token:
            """
            Get the string representation of a single token from its id.
            """
            return self.tokens_of_ids([id])[0]

        @Wrapping.utility
        def id_of_tokenlike(self, tokenlike: Types.TokenLike) -> Types.TokenId:
            # TODO: remove from here, move to attribution setup stuff
            """
            TokenLike = Union[Types.Token, Types.TokenId]
            """

            if isinstance(tokenlike, str):
                return self.id_of_token(tokenlike)
            elif isinstance(tokenlike, int):
                return tokenlike
            else:
                raise ValueError(
                    f"Unhandled type ({type(tokenlike)}) of tokenlike {tokenlike}."
                )

    class TokenizerWrapper(
        WithTokenizerWrapperOptional,
        WithTokenizerWrapperUtility,
        metaclass=WrapperMeta
    ):
        """
        Tokenizers split text inputs (sentences, paragraphs, documents, or other
        NLP model inputs) into tokens that can be fed into an NLP model.
        Tokenizer operates on four types of objects. Types.Text strings, integer
        token ids, string tokens and string words. For some models or
        tokenizers, tokens and words are the same.
        """

        @Wrapping.require_init
        def __init__(
            self,
            model_path: Path,
            vocab: Dict[Types.Token, Types.TokenId],
            n_tokens: int,
            unk_token_id: int,
            pad_token_id: int,
            special_tokens: Optional[List[Types.TokenId]] = None,
            *args,
            **kwargs
        ):
            """
            Required args must be provided by sub-class.
            """

            assert unk_token_id is not None, "unknown token not given"
            assert pad_token_id is not None, "pad token not given"

            self._model_path = model_path

            self._vocab: Dict[Types.Token, Types.TokenId] = vocab
            self._vocab_inverse = {i: t for t, i in self._vocab.items()}

            self._special_token_ids: List[Types.TokenId] = []
            self._special_tokens: List[Types.Token] = []

            self._unk_token_id: Types.TokenId = unk_token_id
            self._pad_token_id: Types.TokenId = pad_token_id
            self._unk_token: Types.Token = self._vocab_inverse[unk_token_id]
            self._pad_token: Types.Token = self._vocab_inverse[pad_token_id]

            special_tokens = special_tokens or []
            special_tokens.extend([self.unk_token_id, self.pad_token_id])
            special_tokens = list(set(special_tokens))
            self._add_special_token_ids(special_tokens)

            self._n_tokens: int = n_tokens

            # Whitespace tokenizer for default word splitting.
            # TODO: Replace this with our own greedytokenizer.
            import tokenizers
            self._word_splitter = tokenizers.pre_tokenizers.Whitespace()

        @Wrapping.required
        @abstractmethod
        def inputbatch_of_textbatch(
            self, texts: Types.TextBatch
        ) -> Types.InputBatch:
            """
            Tokenize texts into a form that wrapped model expects.
            """
            ...

        @property
        def has_tokenspans(self):
            return self.tokenize_into_tru_tokens([""]).spans is not None

        @Wrapping.required
        @abstractmethod
        def tokenize_into_tru_tokens(
            self, texts: Types.TextBatch
        ) -> Types.TruTokenization[Types.Token]:
            """
            Tokenize texts and report several fields:
                - token_ids -- the corresponding token_id's
                - (Optional) spans -- the spans which include token names and their begin/end indices
            
            Example for Huggingface's BertTokenizerFast:
            ```
            parts = bert_tokenizer
                .batch_encode_plus(
                    texts,
                    return_offsets_mapping=True, # required for spans
                    return_token_type_ids=False, # don't need these
                )
            input_idss: npt.NDArray[np.int] = parts['input_ids']
            tokenss = [bert_tokenizer.batch_decode(input_ids) for input_ids in input_idss]
            offsetss = parts['offset_mapping']
            
            spanss = [
                [
                    Span(item=t, begin=o[0], end=o[1])
                    for t, o in zip(tokens, offsets)
                ]
                for tokens, offsets in zip(tokenss, offsetss)
            ]
            return Types.TruTokenization(
                spans=spanss,
                token_ids=np.ndarray(input_idss),
            )
            ```
            """
            pass

    class WithModelLoadWrapperUtility:
        """
        Utility methods for model load wrappers. Do not override.
        """

        @Wrapping.utility
        def print_layer_names(self, model: NNB.Model) -> None:
            """
            Print layer names in the given model.
            """

            # TODO: import optional?
            from trulens.nn.models import get_model_wrapper

            wrapper = get_model_wrapper(model)
            wrapper.print_layer_names()

        @Wrapping.utility
        @property
        def n_tokens(self) -> int:
            """
            Number of tokens the model expects.
            """
            return self._n_tokens  # pylint: disable=E1101

    class ModelLoadWrapper(
        base.Wrappers.ModelLoadWrapper, WithModelLoadWrapperUtility
    ):
        """
        Model load wrapper for NLP models.
        """

        @Wrapping.required
        @abstractmethod
        def get_tokenizer(
            self, n_tokens: int = None
        ) -> Wrappers.TokenizerWrapper:
            """
            Return the tokenizer which converts a string into token ids. If the
            tokenizer needs to be loaded from a path, then it will be assumed to
            be available at location indicated by get_code_path.
            
            Args:
            - n_tokens: int - the number of tokens the model expects in its
              input.
            Output
            ----------------
            - A tokenizer wrapper.
            ----------------
            """
            ...

    class WithModelRunWrapperUtility:
        """
        Utility methods for NLP model run wrappers. Do not override.
        """

        @Wrapping.utility
        def inputbatch_of_textbatch(
            self, texts: Types.TextBatch, *, model: NNB.Model,
            tokenizer: Wrappers.TokenizerWrapper
        ) -> Types.InputBatch:
            """
            Create project-specific model inputs to evaluate model on the given
            collection of texts.
            """

            return tokenizer.inputbatch_of_textbatch(texts)

        @Wrapping.utility
        @property
        def n_tokens(self) -> int:
            """
            Number of tokens the model expects.
            """
            return self._n_tokens  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def n_embeddings(self) -> int:
            """
            Number of dimensions in a token's embedding.
            """
            return self._n_embeddings  # pylint: disable=E1101

        @Wrapping.utility
        def textbatch_of_trubatch(
            self, trubatch: Types.TruBatch
        ) -> Types.TextBatch:
            """
            Extract the texts from the given project-agnostic TruBatch. 
            """

            return list(trubatch.text)

        @Wrapping.utility
        def textbatch_of_databatch(
            self, databatch: Types.DataBatch, *, model: NNB.Model,
            tokenizer: Wrappers.TokenizerWrapper
        ) -> Types.TextBatch:
            """
            Extract the texts from the given project-specific Types.DataBatch.
            """

            trubatch = self.trubatch_of_databatch( # pylint: disable=E1101
                databatch, model=model, tokenizer=tokenizer
            )
            return self.textbatch_of_trubatch( # pylint: disable=E1101
                trubatch
            )

        @Wrapping.utility
        def inputbatch_of_databatch(
            self, databatch: Types.DataBatch, *, model: NNB.Model,
            tokenizer: Wrappers.TokenizerWrapper
        ) -> Types.InputBatch:
            """
            Given a project-specific Types.DataBatch, produce the model inputs that
            can be sent to model to evaluate it on the given databatch.
            """

            kw = dict(model=model, tokenizer=tokenizer)
            trubatch = self.trubatch_of_databatch(databatch, **kw)  # pylint: disable=E1101
            textbatch = self.textbatch_of_trubatch(trubatch)
            inputbatch = self.inputbatch_of_textbatch(list(textbatch), **kw)
            return inputbatch

        @Wrapping.utility
        def evaluate_model_from_text(
            self, model: NNB.Model, text: Types.Text,
            tokenizer: Wrappers.TokenizerWrapper
        ) -> Types.OutputBatch:
            """
            Evaluate model on a single piece of text. See `evaluate_model_from_texts`.
            """
            return self.evaluate_model_from_texts(model, [text], tokenizer)

        @Wrapping.utility
        def evaluate_model_from_texts(
            self, model: NNB.Model, texts: Iterable[Types.Text],
            tokenizer: Wrappers.TokenizerWrapper
        ) -> Types.OutputBatch:
            """
            An evaluate model function where the input is in text format. No
            batching is performed here.
            Input
            ----------------
            - model: NNB.Model - The model object
            - texts: Iterable[Types.Text] -- The texts to evaluate.
            - tokenizer: TokenizerWrapper - A tokenizer.
            ----------------
            Output
            ----------------
            - Base.Types.OutputBatch -- arrays of probits and/or logits
            ----------------
            """

            inputs: Types.InputBatch = self.inputbatch_of_textbatch(
                texts=texts, model=model, tokenizer=tokenizer
            )

            return self.evaluate_model(model=model, inputs=inputs)  # pylint: disable=E1101

    class ModelRunWrapper(
        WithModelRunWrapperUtility, base.Wrappers.ModelRunWrapper
    ):
        """
        Model run wrapper for NLP models.
        """

        @Wrapping.require_init_if_extended
        # checks that this method is called if __init__ is overridden by child class
        def __init__(self, n_tokens: int, n_embeddings: int):
            """
            Initalize required parameters of an NLP ModelRunWrapper.
            - n_tokens: int - the number of tokens the model expects in its
              input.
            - n_embeddings: int - the dimensions in token embeddings used in
              this model.
            """
            # Child classes will have to initialize us by giving us these required parameters.
            super().__init__()
            self._n_tokens = n_tokens
            self._n_embeddings = n_embeddings

        @Wrapping.deprecates(
            "ds_elements_to_truera_elements",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        @Wrapping.required
        def trubatch_of_databatch(
            self, databatch: Types.DataBatch, *, model: NNB.Model,
            tokenizer: Wrappers.TokenizerWrapper
        ) -> Types.TruBatch:
            """
            Same as Timeseries version except different fields are required:
            
            - ids = array of size (batch x 1) : <ids to pair with records>
            - labels = array of size (batch x 1) : <label of each record>
            - text = original input texts before any processing
            Input
            ----------------
            - databatch: Types.DataBatch -- the output of a single iteration
              over the SplitLoadWrapper.get_ds object
            - model: NNB.Model -- This may be needed if the model does any
              preprocessing.
            - tokenizer: TokenizerWrapper - tokenizer wrapper in case it is
              needed.
            ----------------
            Output
            ----------------
            - TruBatch: contents of databatch but in tru form.
            ----------------
            """
            # Currently not needing model or tokenizer. Future may change this.
            return Types.TruBatch(**Types.to_map(databatch))

        class WithEmbeddings(ABC):
            # NOTE(piotrm): for the trulens implementation, we need this to
            # define cuts for a distribution of interest.

            @staticmethod
            @abstractmethod
            def get_embeddings(
                model: NNB.Model, word_ids: NNB.Words
            ) -> NNB.Embeddings:
                """
                Produce embeddings for the given words. This intermediate model
                output may be necessary for some explanations when using the
                trulens explanations backend.
                """
                ...

    class SplitLoadWrapper(
        base.Wrappers.SplitLoadWrapper,
        base.Wrappers.SplitLoadWrapper.WithStandardization
    ):
        """
        Split load wrapper for NLP data.
        """

        @Wrapping.required
        @abstractmethod
        def get_ds(self) -> Iterable:
            ...

        class WithSegmentByWord(ABC):
            """Split load wrapper for NLP fairness segments data"""

            @staticmethod
            @abstractmethod
            def get_segment_keywords_map() -> Dict[str, Sequence[str]]:
                """
                [Optional] Only used if split loader is processing text
                inputs for segment metadata
                
                Args:
                    None: 
                Return:
                    segment_keywords_map: [Sequence[str]] a mapping from a
                    segment_name to keywords for text samples that
                    correspond to that segment
                """
                ...


@dataclass
class WrapperCollection(base.WrapperCollection):
    tokenizer_wrapper: Wrappers.TokenizerWrapper = None

    __type_to_field_map = copy.copy(base.WrapperCollection.__type_to_field_map)
    __type_to_field_map[Wrappers.TokenizerWrapper] = "tokenizer_wrapper"
