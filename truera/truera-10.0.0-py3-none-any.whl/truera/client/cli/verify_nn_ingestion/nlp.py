from pathlib import Path
from typing import (
    Callable, Iterable, Mapping, Optional, Sequence, Tuple, Union
)

import numpy as np

from truera.client.cli.verify_nn_ingestion import ArgValidationException
from truera.client.cli.verify_nn_ingestion import ParamValidationContainer
from truera.client.cli.verify_nn_ingestion import VerifyHelper
from truera.client.cli.verify_nn_ingestion import \
    WrapperOutputValidationException
from truera.client.nn import BaselineType
from truera.client.nn import NNBackend as NNB
from truera.client.nn.client_configs import Dimension
from truera.client.nn.client_configs import Layer
from truera.client.nn.client_configs import LayerAnchor
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.wrappers.datasets import convert_to_truera_iterable
from truera.client.nn.wrappers.nlp import Types
from truera.client.nn.wrappers.nlp import Wrappers
from truera.nlp.general.model_runner_proxy.nlp_attributions import \
    NLPAttribution


class NLPVerifyHelper(VerifyHelper):

    def __init__(
        self,
        model_input_type: Optional[str] = None,
        model_output_type: Optional[str] = None,
        attr_config: Optional[NLPAttributionConfiguration] = None,
        model: Optional[NNB.Model] = None,
        split_load_wrapper: Optional[Wrappers.SplitLoadWrapper] = None,
        model_run_wrapper: Optional[Wrappers.ModelRunWrapper] = None,
        model_load_wrapper: Optional[Wrappers.ModelLoadWrapper] = None,
        tokenizer_wrapper: Optional[Wrappers.TokenizerWrapper] = None
    ):
        super().__init__(
            model_input_type=model_input_type,
            model_output_type=model_output_type,
            attr_config=attr_config,
            model=model,
            split_load_wrapper=split_load_wrapper,
            model_run_wrapper=model_run_wrapper,
            model_load_wrapper=model_load_wrapper
        )
        self.add_tokenizer_wrapper(tokenizer_wrapper)

    def add_tokenizer_wrapper(
        self, tokenizer_wrapper: Wrappers.TokenizerWrapper
    ):
        self.tokenizer_wrapper = tokenizer_wrapper

    ### Utility Checks for Data & Batch objects

    def get_cuts_and_expected_shapes(
        self, trubatch: Types.TruBatch, outputbatch: Types.OutputBatch
    ) -> Tuple[Sequence["Cut"], Sequence[Tuple[Tuple, str]]]:
        """ Gets the trulens cuts to check.

        Returns:
            cuts : The list of cuts to check.
            expected_shapes_and_source : A list containing tuples of shapes and a string representing how that shape was gotten.
        """

        from trulens.nn.slices import Cut
        from trulens.nn.slices import InputCut
        from trulens.nn.slices import OutputCut

        attr_config = self.attr_config

        if attr_config.embedding_layer == Layer.INPUT:
            cuts = [InputCut()]
        else:
            cuts = [
                Cut(
                    attr_config.embedding_layer,
                    anchor=str(attr_config.embedding_anchor)
                )
            ]
        expected_shapes_and_source = [
            (
                (
                    len(trubatch.text), self.model_run_wrapper.n_tokens,
                    self.model_run_wrapper.n_embeddings
                ),
                "(`trubatch text batchsize`, `ModelRunWrapper n_tokens`, `ModelRunWrapper n_embeddings`)"
            )
        ]
        if attr_config.output_layer == Layer.OUTPUT:
            cuts.append(OutputCut())
        else:
            cuts.append(
                Cut(
                    attr_config.output_layer,
                    anchor=str(attr_config.output_anchor)
                )
            )
        expected_shapes_and_source.append(
            (outputbatch.probits.shape, "model output")
        )
        if attr_config.attribution_layer is not None:
            cuts.append(
                Cut(
                    attr_config.attribution_layer,
                    anchor=str(attr_config.attribution_anchor)
                )
            )
        # We don't know shape of attribution cut since it can be any intermediate layer
        expected_shapes_and_source.append((None, "attribution cut"))

        return cuts, expected_shapes_and_source

    def verify_trubatch_of_databatch(
        self, databatch: Types.DataBatch, feature_names: Sequence[str]
    ) -> None:
        """
        The NLP Specific validation for verify_trubatch_of_databatch. See the
        VerifyHelper for more details.
        """
        trubatch: Types.TruBatch = self.model_run_wrapper.trubatch_of_databatch(
            databatch, model=self.model, tokenizer=self.tokenizer_wrapper
        )
        batch_size = trubatch.batch_size

        truera_keys = set(["ids", "text", "labels"])
        self.verify_trubatch(
            trubatch=trubatch,
            truera_keys=truera_keys,
        )

        VerifyHelper.verify_shape(
            trubatch.labels, (batch_size,),
            origin="TruBatch.labels",
            shape_desc="(batch,)"
        )

        print("Passed! ModelRunWrapper.trubatch_of_databatch")
        return trubatch

    ### Top-level Checks

    def verify_evaluate_model(
        self, databatch: Types.DataBatch, trubatch: Types.TruBatch
    ) -> Tuple[Types.OutputBatch, Types.InputBatch]:
        """Checks that the ModelRunWrapper evaluate_model method is correctly formed

        Args:
            databatch (DataBatch): Batchable components coming from the SplitLoadWrapper get_ds method.
            trubatch (TruBatch): An object of truera data

        Returns:
            Tuple[Types.OutputBatch, Types.InputBatch]: Returns the output and the input of the model for further verification.

        Raises:
            WrapperOutputValidationException: An exception raised if the method is incorrectly defined.
        """
        assert isinstance(self.model_run_wrapper, Wrappers.ModelRunWrapper)
        textbatch: Types.TextBatch = self.model_run_wrapper.textbatch_of_trubatch(
            trubatch
        )

        # Validate tokenizer
        inputbatch: Types.InputBatch = self.verify_tokenizer(textbatch)
        # TODO (corey): verify inputbatch.args, inputbatch.kwargs shapes

        self.verify_tokenizer_supervised(textbatch)

        if not isinstance(inputbatch.args, list):
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.model_input_args_kwargs first item should return a \"list\". got {str(type(inputbatch.args))}"
            )

        if not isinstance(inputbatch.kwargs, dict):
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.model_input_args_kwargs second item should return a \"dict\". got {str(type(inputbatch.kwargs))}"
            )
        output: Types.OutputBatch = self.model_run_wrapper.evaluate_model(
            self.model, inputbatch
        )
        self.verify_type(
            output,
            Types.OutputBatch,
            origin="Wrappers.ModelRunWrapper.evaluate_model()"
        )

        assert hasattr(
            output, "probits"
        ) and output.probits is not None, "Invalid Types.OutputBatch from ModelRunWrapper.evaluate_model(): Missing probits attribute"

        probits = output.probits

        if not probits.shape[0] == trubatch.batch_size:
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.evaluate_model batch size should match ModelRunWrapper.trubatch_of_databatch[\"ids\"] batch size. Evaluated batch size is {output.probits.shape[0]}, from shape {str(output.probits.shape)}. \"index\" batch size is {trubatch.batch_size}"
            )
        print("Passed! ids check input and output batch sizes match")

        if self.param_validation.seq_2_seq:
            if not probits.shape[1] == self.attr_config.n_time_step_output:
                raise WrapperOutputValidationException(
                    f"The second dimension in ModelRunWrapper.evaluate_model should be the specified n_time_step_output size. The dimension found is {output.probits.shape[1]} in shape {str(output.probits.shape)}. The n_time_step_output specified in the projects is {self.attr_config.n_time_step_output}."
                )
            print("Passed! check output timestep sizes match")
            class_dimension_idx = 2
        else:
            class_dimension_idx = 1

        if not probits.shape[class_dimension_idx
                            ] == self.attr_config.n_output_neurons:
            raise WrapperOutputValidationException(
                f"The dimension index of {class_dimension_idx} in ModelRunWrapper.evaluate_model should be the specified num output neurons from the AttributionConfiguration. The dimension found is {output.probits.shape[class_dimension_idx]} in shape {str(output.probits.shape)}. The num output neurons from the AttributionConfiguration specified in the projects is {self.attr_config.n_output_neurons}."
            )

        if not np.min(probits) >= 0:
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.evaluate_model is expected to return probits between 0 and 1. Found negative values: {np.min(probits)}"
            )
        if not np.max(probits) <= 1:
            raise WrapperOutputValidationException(
                f"ModelRunWrapper.evaluate_model is expected to return probits between 0 and 1. Found values greater than 1: {np.max(probits)}"
            )

        print(
            "Passed! check output num output neurons from the AttributionConfiguration match"
        )
        print(
            "Passed! model_run_wrapper.model_input_args_kwargs and model_run_wrapper.evaluate_model"
        )
        return output, inputbatch

    def verify_wrapper_types(self) -> None:
        """The NLP Specific validation for verify_wrapper_types. See the VerifyHelper for more details.
        """
        super().verify_wrapper_types(
            attr_config_type=NLPAttributionConfiguration,
            model_run_wrapper_type=Wrappers.ModelRunWrapper,
            split_load_wrapper_type=Wrappers.SplitLoadWrapper,
            model_load_wrapper_type=Wrappers.ModelLoadWrapper
        )
        if self.tokenizer_wrapper is not None:
            VerifyHelper.verify_type(
                self.tokenizer_wrapper,
                Wrappers.TokenizerWrapper,
                origin="TokenizerWrapper"
            )

    def verify_attr_config(self):
        """The NLP Specific validation for verify_attr_config. See the VerifyHelper for more details.
        """
        super().verify_attr_config()

        VerifyHelper.verify_type(
            self.attr_config.embedding_layer, (str, Layer),
            origin=f"{self.attr_config_cls_name}.embedding_layer"
        )

        if self.attr_config is not None and hasattr(
            self.attr_config, "embedding_layer"
        ) and self.attr_config.embedding_layer is not None:
            VerifyHelper.verify_type(
                self.attr_config.embedding_layer, (str, Layer),
                origin=f"{self.attr_config_cls_name}.embedding_layer"
            )
            VerifyHelper.verify_type(
                self.attr_config.embedding_anchor,
                (str, LayerAnchor, type(None)),
                origin=f"{self.attr_config_cls_name}.embedding_anchor"
            )
            if not self.attr_config.embedding_anchor in [
                "in", "out", LayerAnchor.IN, LayerAnchor.OUT, None
            ]:
                raise ArgValidationException(
                    "embedding_anchor must be either \"in\" or \"out\". Got %s"
                    % str(self.attr_config.embedding_anchor)
                )
        elif self.attr_config.embedding_anchor is not None:
            print(
                "WARNING: embedding_anchor defined in AttributionConfiguration while embedding_layer is None. embedding_anchor will be ignored."
            )

        if self.attr_config.rebatch_size is not None:
            VerifyHelper.verify_type(
                self.attr_config.rebatch_size,
                int,
                origin="NLPAttributionConfiguration.rebatch_size"
            )
        if self.attr_config.ref_token is not None:
            VerifyHelper.verify_type(
                self.attr_config.ref_token,
                str,
                origin="NLPAttributionConfiguration.ref_token"
            )
        if self.attr_config.resolution is not None:
            VerifyHelper.verify_type(
                self.attr_config.resolution,
                int,
                origin="NLPAttributionConfiguration.resolution"
            )
        print("Passed! attr_config checked.")

    def verify_tokenizer(self, textbatch: Types.TextBatch):
        self.verify_tokenizer_special_tokens()
        self.verify_tokenize_into_tru_words(textbatch)
        self.verify_tokenize_into_tru_tokens(textbatch)
        inputbatch = self.verify_inputbatch_of_textbatch(textbatch)
        print("Passed! TokenizerWrapper checks")
        return inputbatch

    def verify_tokenizer_supervised(self, textbatch: Types.TextBatch):

        test_sentences = [
            "This sentence ends with something that is typically not considered a wordle."
        ]

        tok = self.tokenizer_wrapper.tokenize_into_tru_tokens(
            texts=test_sentences
        )

        input_sentences = test_sentences
        token_ids = tok.token_ids
        sequence_masks = token_ids != self.tokenizer_wrapper.pad_token_id
        spans = tok.spans

        assert self.tokenizer_wrapper.has_tokenspans == (spans is not None)
        if spans is None:
            print(
                "Skipping verify_tokenizer_supervised: tokenize_into_tru_tokens spans are not defined."
            )
            return

        print(
            """
Human-assisted Tokenizer Verification (tm)                        

Each token is shown with "111..." or "000..." indicating its origin in the text.
Ones/zeros indicate the token's sequence_mask. Its string representation and
token id are shown. Zero-length tokens are indicated by '*' or "." for non-zero
attention mask or zero attention mask respectively. If `visible_token` changes a
token name, the original and "visible" are both shown.

====================
"""
        )

        for sentence_index, (input_ids, masks, offsets) in enumerate(
            zip(token_ids, sequence_masks, spans)
        ):
            counting_pad_tokens = None

            for token_index, (input_id, mask, offset) in enumerate(
                zip(input_ids, masks, offsets)
            ):
                if counting_pad_tokens is not None:
                    if input_id == self.tokenizer_wrapper.pad_token_id:
                        counting_pad_tokens += 1
                        if mask != 0:
                            print(
                                "!!!",
                                "warning: attention mask is not 0 for pad token"
                            )
                        continue
                    else:
                        print("   ", input_sentences[sentence_index])
                        print(
                            "...",
                            f"{token_index - counting_pad_tokens:03}-{token_index:03} are pad token(s)"
                        )
                        counting_pad_tokens = None
                else:
                    if input_id == self.tokenizer_wrapper.pad_token_id:
                        if mask != 0:
                            print(
                                "!!!",
                                "warning: attention mask is not 0 for pad token"
                            )
                        counting_pad_tokens = 0
                        continue

                print("   ", input_sentences[sentence_index])
                print(f"{token_index:03}", end=" ")

                token = self.tokenizer_wrapper.token_of_id(input_id)
                token_visible = self.tokenizer_wrapper.visible_token(token)

                # Create the readable token string. If visible_token methods
                # does anything, show the changed value.
                token_str = f'{token}'
                if token != token_visible:
                    token_str += f"->'{token_visible}'"

                begin, end = offset.begin, offset.end

                length = end - begin

                if begin > 0:
                    print(" " * begin, end='')

                if length == 0:
                    if mask:
                        print("*", end='')
                    else:
                        print(".", end='')
                else:
                    if mask:
                        marker = "1"
                    else:
                        marker = "0"

                    print(marker, end='')

                    if length > 2:
                        print(marker * (length - 2), end='')

                    if length > 1:
                        print(marker, end='')

                print(f" {token_str} ({input_id})")

            if counting_pad_tokens is not None:
                print("   ", input_sentences[sentence_index])
                print(
                    "...",
                    f"{token_index - counting_pad_tokens:03}-{token_index:03} are pad token(s)"
                )

        print("====================")

    def verify_tokenizer_special_tokens(self):
        special_tokens = self.tokenizer_wrapper.special_tokens
        vocab = set(self.tokenizer_wrapper.vocab.keys())
        violating_tokens = set()
        for tok in special_tokens:
            if tok not in vocab:
                violating_tokens.add(tok)

        if len(violating_tokens) > 0:
            raise ArgValidationException(
                f"Invalid tokens {list(violating_tokens)} found in TruTokenization.special_tokens missing in Wrappers.TokenizerWrapper vocab."
            )

    def verify_tokenize_into_tru_words(self, textbatch: Types.TextBatch):
        trutok: Types.TruTokenization = self.tokenizer_wrapper.tokenize_into_tru_words(
            textbatch
        )
        self.verify_type(
            trutok,
            Types.TruTokenization,
            origin="Wrappers.TokenizerWrapper.tokenize_into_tru_tokens"
        )

        # Validate no overlapping spans
        for i, spans in enumerate(trutok.spans):
            self.verify_spans(spans, textbatch[i])

    def verify_inputbatch_of_textbatch(
        self, textbatch: Types.TextBatch
    ) -> Types.InputBatch:
        """
        Validate Wrappers.TokenizationWrapper.inputbatch_of_textbatch and
        TruTokenization object

        Args:
            - textbatch (Wrappers.TextBatch): The Wrappers.TextBatch object used to
              generate TruTokenization
        """
        # Verify typing of InputBatch
        inputbatch: Types.InputBatch = self.tokenizer_wrapper.inputbatch_of_textbatch(
            textbatch
        )
        self.verify_inputbatch(inputbatch, dtype=Types.InputBatch)
        return inputbatch

    def verify_spans(self, spans: Iterable[Types.Span], original_str: str):
        """Validate TruTokenization.spans object"""
        prev_end = -1
        str_len = len(original_str)
        for span in spans:
            self.verify_type(span.item, str, origin="Span.item")
            if span.item not in self.tokenizer_wrapper.special_tokens:
                assert span.begin >= prev_end, (
                    f"Invalid Non-special token Spans from TruTokenization: "
                    f"Overlapping spans (.., {prev_end}) ({span.begin}, ...) on token {span.item}"
                )
                prev_end = span.end
        assert prev_end <= str_len, (
            f"Invalid Spans from TruTokenization: "
            f"Span end of {prev_end} exceeds string length of {str_len}"
        )

    def verify_tokenize_into_tru_tokens(self, textbatch: Types.TextBatch):
        """
        Validate Wrappers.TokenizationWrapper.tokenize_into_tru_tokens and
        TruTokenization object

        Args:
            - textbatch (Wrappers.TextBatch): The Wrappers.TextBatch object used to
              generate TruTokenization
        """
        trutok: Types.TruTokenization = self.tokenizer_wrapper.tokenize_into_tru_tokens(
            textbatch
        )

        # Verify Tokenization Output types
        self.verify_type(
            trutok,
            Types.TruTokenization,
            origin="Wrappers.TokenizerWrapper.tokenize_into_tru_tokens"
        )

        self.verify_type(
            trutok.token_ids,
            np.ndarray,
            origin="NLP.TokenizerWrapper.tokenize_into_tru_tokens.token_ids"
        )

        assert self.tokenizer_wrapper.has_tokenspans == (
            trutok.spans is not None
        )
        if trutok.spans is None:
            print(
                "Skipping verify_tokenize_into_tru_tokens span checks: tokenize_into_tru_tokens spans not defined."
            )
        else:
            self.verify_type(
                trutok.spans,
                Iterable,
                origin="NLP.TokenizerWrapper.tokenize_into_tru_tokens.spans"
            )

            # Validate no overlapping spans
            for i, spans in enumerate(trutok.spans):
                self.verify_spans(spans, textbatch[i])

        # Validate token_ids are in vocab range
        vocab = self.tokenizer_wrapper.vocab_inverse
        vocab_tokens = set(vocab.keys())
        token_ids_unique = set(np.unique(trutok.token_ids))

        if len(vocab_tokens | token_ids_unique) != len(vocab_tokens):
            violating_tokens = token_ids_unique - vocab_tokens
            raise ArgValidationException(
                f"Invalid tokens {violating_tokens} found in TruTokenization.token_ids missing in Wrappers.TokenizerWrapper vocab."
            )

    def _get_named_parameters(self) -> ParamValidationContainer:
        """
        Returns an object container that contains many commonly referenced
        parameters.

        Returns:
            - ParamValidationContainer: an object container that contains many
              commonly referenced parameters.
        """
        if not hasattr(
            self, 'model_run_wrapper'
        ) or self.model_run_wrapper is None:
            return None
        return ParamValidationContainer(
            input_seq_dimension=Dimension.POSITION,
            input_data_dimension=Dimension.EMBEDDING,
            config_input_seq_param=self.model_run_wrapper.n_tokens,
            config_input_data_param=self.model_run_wrapper.n_embeddings,
            config_input_seq_param_str="n_tokens",
            config_input_data_param_str="n_embeddings",
            input_dimension_order_str=f"(batch x n_tokens)",
            output_dimension_order_str="(batchsize,)",
            expected_labels_shape=1,
            input_data_key="token_ids",
            seq_2_seq=False
        )

    @staticmethod
    def verify_baseline_attributions_visual(
        *,
        token_ids: np.ndarray,
        baseline_tokens: np.ndarray,
        tokens: Optional[Sequence[Sequence[str]]] = None,
        line_width: int = None
    ):
        print(
            "\nNon-zero attributions check\n\
This is a visual sanity check, only underlined tokens will get non-zero attributions.\
If there are any tokens you do not want to get attribution like PAD, CLS, or SEP\
, please add them to the tokenizer_wrapper.special_tokens with `tokenizer_wrapper.add_special_tokens()`."
        )
        print("====================")
        lines = []
        has_attr_map = np.not_equal(token_ids, baseline_tokens)

        for seq_ids, seq_tokens, seq_has_attr in zip(
            token_ids, tokens, has_attr_map
        ):
            # Gets size of group of matching tokens at tail of seq (e.g. number of PADs)
            end_group_len = len(
                np.split(seq_ids,
                         np.nonzero(np.diff(seq_ids) != 0)[0] + 1)[-1]
            )

            # True if seq_has_attr is all True or all False for last end_group_len tokens
            matching_attr_sign = np.all(
                seq_has_attr[-end_group_len:]
            ) or not np.any(seq_has_attr[-end_group_len:])

            text_batch = []
            underline_batch = []
            for i, (token, token_has_attr) in enumerate(
                zip(seq_tokens, seq_has_attr)
            ):
                token = str(token)
                char = "-" if token_has_attr else " "
                text_batch.append(token)
                underline_batch.append(char * len(token))

                if matching_attr_sign and i >= len(seq_ids) - end_group_len + 2:
                    # Should only print 3 of last token before ellipses
                    end_token = f"...+{end_group_len - 3}*{token}"
                    text_batch.append(end_token)
                    underline_batch.append(char * len(end_token))
                    break
                elif line_width and len(text_batch) > line_width:
                    lines.append(" ".join(text_batch))
                    lines.append(" ".join(underline_batch))
                    text_batch = []
                    underline_batch = []

            if len(text_batch):
                lines.append(" ".join(text_batch))
                lines.append(" ".join(underline_batch))
            lines.append("")
        return "\n".join(lines)

    def verify_baseline(
        self, trubatch: Types.TruBatch, inputbatch: Types.InputBatch
    ) -> None:
        """
            Method for validating baseline construction
        """
        from trulens.nn.models import get_backend
        from trulens.nn.models import get_model_wrapper
        from trulens.nn.slices import Cut
        from trulens.nn.slices import InputCut
        from trulens.utils.typing import ModelInputs

        B = get_backend()
        # Verify with tokenizer
        assert self.attr_config.baseline_type in [e.value for e in BaselineType]
        tl_model = get_model_wrapper(self.model)
        baseline_fn = NLPAttribution._get_baseline_fn(
            model_args=self.attr_config,
            trulens_model=tl_model,
            tokenizer=self.tokenizer_wrapper,
            attribution_cut=Cut(
                self.attr_config.embedding_layer,
                anchor=self.attr_config.embedding_anchor
            ),
            embedding_layer=self.attr_config.embedding_layer,
            input_anchor=self.attr_config.input_anchor,
            return_baseline_tokens=True
        )

        if self.attr_config.attribution_layer is not None:
            attribution_cut = Cut(
                self.attr_config.attribution_layer,
                anchor=self.attr_config.attribution_anchor,
                accessor=None
            )
        elif self.attr_config.embedding_layer == Layer.INPUT:
            attribution_cut = InputCut()
        else:
            attribution_cut = Cut(
                self.attr_config.embedding_layer,
                anchor=self.attr_config.embedding_anchor,
                accessor=None
            )

        model_inputs = ModelInputs(inputbatch.args, inputbatch.kwargs)
        attribution_tensor = tl_model.fprop(
            model_inputs.args,
            model_kwargs=model_inputs.kwargs,
            to_cut=attribution_cut
        )
        baseline, baseline_tokens = baseline_fn(None, model_inputs)
        baseline_tokens = B.as_array(baseline_tokens)

        # Check special tokens are kept in baseline
        special_tokens = set(self.tokenizer_wrapper.special_token_ids)
        unused_special_tokens = list(
            special_tokens - set(np.unique(baseline_tokens))
        )
        if len(unused_special_tokens) > 0:
            tokens_str = ", ".join(
                f"{self.tokenizer_wrapper.token_of_id(t)} ({t})"
                for t in unused_special_tokens
            )
            print(f"WARNING: Special tokens not used: {tokens_str}")

        # Visual baseline check
        tokens = self.tokenizer_wrapper.tokenize_into_tru_tokens(
            texts=trubatch.text
        )
        n_samples = 3
        token_ids = tokens.token_ids[:n_samples]

        token_strs = []
        for record_token_ids in token_ids:
            record_token_strs = []
            for token_id in record_token_ids:
                record_token_strs.append(
                    self.tokenizer_wrapper._vocab_inverse[token_id]
                )
            token_strs.append(record_token_strs)
        print(
            NLPVerifyHelper.verify_baseline_attributions_visual(
                token_ids=tokens.token_ids[:n_samples],
                baseline_tokens=baseline_tokens[:n_samples],
                tokens=token_strs,
                line_width=10
            )
        )
        assert attribution_tensor.shape == baseline.shape, "Embeddings shape does not match baseline shape"
        assert not np.all(
            B.as_array(baseline) == B.as_array(attribution_tensor)
        ), "Embeddings value should not be identical to baseline value"

        # Verify with get_embeddings
        if isinstance(
            self.model_run_wrapper, Wrappers.ModelRunWrapper.WithEmbeddings
        ):
            baseline_fn = NLPAttribution._get_baseline_fn(
                model_args=self.attr_config,
                trulens_model=get_model_wrapper(self.model),
                tokenizer=self.tokenizer_wrapper,
                attribution_cut=Cut(
                    self.attr_config.embedding_layer,
                    anchor=self.attr_config.embedding_anchor
                ),
                model=self.model,
                model_run_wrapper=self.model_run_wrapper
            )
            baseline_dup = baseline_fn(None, model_inputs)
            assert np.allclose(B.as_array(baseline), B.as_array(baseline_dup))
            print("Passed! Baseline consistency check")
        print("Passed! Baseline checks")


class NLPAutowrapVerifyHelper(NLPVerifyHelper):

    def verify_autowrap_ds_from_source(
        self,
        ds_from_source: Callable,
        data_path: Optional[str] = None,
        batch_size: int = 16,
        n_records: int = 16
    ):
        ds = ds_from_source(data_path)
        ds = convert_to_truera_iterable(
            ds, batch_size=batch_size, n_records=n_records
        )
        ds_batch = next(iter(ds))
        return ds_batch

    def verify_autowrap_standardize_databatch(
        self,
        standardize_databatch: Callable,
        databatch: Types.DataBatch,
        expected_batch_size: Optional[int] = None
    ):
        """
        Autowrapper verification for standardize_databatch method return value.
        """
        trubatch = standardize_databatch(databatch)
        self.verify_type(trubatch, Mapping, origin="trubatch")
        assert len(trubatch) == 3
        assert "ids" in trubatch
        assert "text" in trubatch
        assert "labels" in trubatch

        self.verify_type(trubatch['ids'], np.ndarray, origin="trubatch['ids']")
        self.verify_type(
            trubatch['text'], np.ndarray, origin="trubatch['text']"
        )
        self.verify_type(
            trubatch['labels'], np.ndarray, origin="trubatch['labels']"
        )

        if expected_batch_size is not None:
            assert len(trubatch['ids']) == expected_batch_size
            assert len(trubatch['text']) == expected_batch_size
            assert len(trubatch['labels']) == expected_batch_size

        for i, txt in enumerate(trubatch['text']):
            self.verify_type(txt, str, origin=f"trubatch['text'][{i}]")

        print("Passed! databatch_to_truera_batch")
        return trubatch

    def verify_autowrap_get_model(
        self, get_model: Callable, model_path: Optional[str] = None
    ):
        model = get_model(model_path)
        assert callable(model)
        print("Passed! get_model")
        return model

    def verify_autowrap_text_to_inputs(
        self, text_to_inputs: Callable, model: Callable, trubatch: dict
    ):
        """
        Autowrapper verification for text_to_inputs method return value.
        """
        inputbatch = text_to_inputs(trubatch['text'])

        self.verify_type(inputbatch, Mapping, origin="inputbatch")
        assert len(inputbatch) == 2
        assert "args" in inputbatch
        assert "kwargs" in inputbatch

        self.verify_type(
            inputbatch['args'], Iterable, origin="inputbatch['args']"
        )
        self.verify_type(
            inputbatch['kwargs'], Mapping, origin="inputbatch['kwargs']"
        )

        try:
            model(*inputbatch['args'], **inputbatch['kwargs'])
        except Exception as e:
            print(
                f"ERROR: Outputs of text_to_inputs does not pass nicely into model: {e}"
            )
            return
        print("Passed! text_to_inputs")
        return inputbatch

    def verify_autowrap_eval_model(
        self,
        model: Callable,
        eval_model: Callable,
        inputbatch: dict,
        expected_batch_size: Optional[int] = None
    ):
        """
        Autowrapper verification for eval_model method return value.
        """
        assert isinstance(
            eval_model, Callable
        ), f"eval_model needs to be callable, is {type(eval_model)}"

        outputbatch = eval_model(
            model, inputbatch['args'], inputbatch['kwargs']
        )
        self.verify_type(outputbatch, np.ndarray, origin="outputbatch")
        if expected_batch_size is not None:
            assert outputbatch.shape[0] == expected_batch_size
        print("Passed! eval_model")

        return outputbatch

    def verify_autowrap_special_tokens(
        self, unk_token: int, pad_token: int, special_tokens: Sequence
    ):
        """
        Autowrapper verification for UNK, PAD, and special_tokens.
        """
        assert unk_token != pad_token
        self.verify_type(unk_token, int, origin="unk_token")
        self.verify_type(pad_token, int, origin="pad_token")
        self.verify_type(special_tokens, Sequence, origin="special_tokens")
        for i, token in enumerate(special_tokens):
            self.verify_type(token, int, origin=f"speical_tokens[{i}]")
        print("Passed! validated UNK, PAD, and additional special tokens")

    def verify_autowrap_text_to_token_ids(
        self,
        text_to_token_ids: Callable,
        trubatch: dict,
        expected_batch_size: Optional[int] = None,
        n_tokens: Optional[int] = None
    ):
        """
        Autowrapper verification for text_to_token_ids method return value.
        """

        # assert isinstance(trubatch, Types.TruBatch), f"trubatch needs to be a TruBatch but was {type(trubatch)} instead"

        tokenbatch = text_to_token_ids(trubatch['text'])
        self.verify_type(tokenbatch, np.ndarray, origin="tokenbatch")
        if expected_batch_size is not None and n_tokens is not None:
            self.verify_shape(
                tokenbatch, (expected_batch_size, n_tokens),
                origin="tokenbatch",
                shape_desc="(expected_batch_size, n_tokens)"
            )
        print("Passed! text_to_token_ids")
        return tokenbatch

    def verify_autowrap_text_to_spans(
        self,
        text_to_spans: Union[None, Callable],
        trubatch: Mapping,
        expected_batch_size: Optional[int] = None,
        n_tokens: Optional[int] = None,
        special_tokens: Optional[Sequence[int]] = []
    ):
        """
        Autowrapper verification for text_to_spans method return value.
        """
        if text_to_spans is None:
            print("SKIPPING: Got text_to_spans is None.")
            return None

        assert callable(text_to_spans)
        self.verify_type(text_to_spans, Callable, origin="text_to_spans")
        spanss = text_to_spans(trubatch['text'])
        self.verify_type(
            spanss, np.ndarray, origin="text_to_spans(trubatch['text'])"
        )
        assert np.issubdtype(spanss.dtype, np.integer)
        self.verify_shape(
            spanss, (expected_batch_size, n_tokens, 2),
            origin="text_to_spans(trubatch['text']).shape",
            shape_desc="(expected_batch_size, n_tokens, 2)"
        )
        span_begins = spanss[:, :, 0]
        span_ends = spanss[:, :, 1]
        assert np.all(span_begins <= span_ends)
        spans_ascending_check = True
        for record, spans in enumerate(spanss):
            spans_substring_check = False
            span_index = 0
            next_span_index = 1
            while (next_span_index < len(spans)):
                span = spans[span_index]
                next_span = spans[next_span_index]
                if span[0] == span[1]:
                    # Find the starting token with length
                    span_index += 1
                    next_span_index += 1
                elif next_span[0] == next_span[1]:
                    # Find the next token with length
                    next_span_index += 1
                else:
                    spans_substring_check = True
                    if span[1] > next_span[0]:
                        print(
                            f"ERROR: for record index {record} and span with index {span_index}, the span end is greater than the next span start with index {next_span_index}."
                        )
                        spans_ascending_check = False
                    span_index = next_span_index
                    next_span_index = span_index + 1
            if not spans_substring_check:
                print(
                    f"ERROR: for record index {record} no spans with length were found."
                )
            assert spans_substring_check
        assert spans_ascending_check
        print("Passed! text_to_spans")
        return spanss

    def verify_flow(
        self,
        n_tokens: int,
        ds_from_source: Callable,
        get_model: Callable,
        standardize_databatch: Callable,
        unk_token_id: int,
        pad_token_id: int,
        special_tokens: Sequence[int],
        text_to_inputs: Callable,
        text_to_token_ids: Callable,
        eval_model: Optional[Callable] = None,
        text_to_spans: Optional[Callable] = None,
        model_path: Optional[Union[str, Path]] = None,
        data_path: Optional[Union[str, Path]] = None
    ):
        # To test shapes mismatches w/ multiple entries (if applicable)
        batch_size = 2

        # Validate data
        databatch = self.verify_autowrap_ds_from_source(
            ds_from_source, data_path, batch_size=batch_size
        )

        # replace batch_size with actual batch size when dataset size < 2
        batch_size = min(len(databatch), batch_size)

        trubatch = self.verify_autowrap_standardize_databatch(
            standardize_databatch, databatch, expected_batch_size=batch_size
        )

        # Validate tokenizations
        self.verify_autowrap_special_tokens(
            unk_token_id, pad_token_id, special_tokens
        )
        self.verify_autowrap_text_to_spans(
            text_to_spans,
            trubatch,
            expected_batch_size=batch_size,
            n_tokens=n_tokens,
            special_tokens=special_tokens
        )
        self.verify_autowrap_text_to_token_ids(
            text_to_token_ids,
            trubatch,
            expected_batch_size=batch_size,
            n_tokens=n_tokens
        )

        # Validate model running
        model = self.verify_autowrap_get_model(get_model, model_path)
        inputbatch = self.verify_autowrap_text_to_inputs(
            text_to_inputs, model, trubatch
        )
        self.verify_autowrap_eval_model(
            model, eval_model, inputbatch, expected_batch_size=batch_size
        )
        print("Passed! Autowrap verification")
