# HIGH DEBT

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, List, Optional, Type, TypeVar

import numpy as np
from tqdm.auto import tqdm
from trulens.nn.attribution import AttributionMethod
from trulens.nn.attribution import AttributionResult
from trulens.nn.attribution import InternalInfluence
from trulens.nn.backend import get_backend
from trulens.nn.distributions import DoI
from trulens.nn.distributions import LinearDoi
from trulens.nn.models import Backend
from trulens.nn.models import get_model_wrapper
from trulens.nn.models._model_base import ModelWrapper as TrulensModelWrapper
from trulens.nn.slices import Cut
from trulens.nn.slices import InputCut
from trulens.nn.slices import OutputCut
from trulens.utils.typing import ModelInputs
from trulens.utils.typing import numpy_of_nested
from trulens.utils.typing import TensorLike

from truera.client.intelligence.explainer import Explainer
from truera.client.nn import BaselineType
from truera.client.nn import NNBackend as NNB
from truera.client.nn.client_configs import Layer
from truera.client.nn.client_configs import ModelPartition
from truera.client.nn.wrappers.nlp import Types
from truera.client.nn.wrappers.nlp import Wrappers
from truera.client.util.iter_utils import LenIterable
from truera.nlp.general.model_runner_proxy.attribution_utils import \
    combine_tokenized_influence_per_original_word
from truera.nlp.general.model_runner_proxy.mem_utils import load_text_data
from truera.nlp.general.utils.configs import QoIType
from truera.rnn.general.model_runner_proxy.explain_helpers import \
    PostModelFilterProcessor
from truera.rnn.general.model_runner_proxy.general_utils import convert_struct
from truera.rnn.general.model_runner_proxy.mem_utils import load_memmap
from truera.rnn.general.model_runner_proxy.mem_utils import load_pickle
from truera.rnn.general.model_runner_proxy.mem_utils import MemmapStreamer
from truera.rnn.general.model_runner_proxy.mem_utils import save_memmap
from truera.rnn.general.model_runner_proxy.rnn_attributions import \
    RNNAttribution
from truera.rnn.general.model_runner_proxy.rnn_quantities import MultiQoI
from truera.utils.file_utils import as_path

logging.basicConfig()
logger = logging.getLogger(__name__)
log_level = logging.INFO
logger.setLevel(log_level)

# TODO: Use this in ingestion wrappers as well.
DsBatch = TypeVar('DsBatch')

IntegratedGradients = TypeVar(
    'IntegratedGradients', bound=List[InternalInfluence]
)
FilterFunc = Callable[[DsBatch, Wrappers.ModelRunWrapper, Backend], int
                     ]  # might be wrong if this actually needs the base model

DEFAULT_IG_RESOLUTION = 16


class NLPAttribution(RNNAttribution):
    # Choose a percentage of the original batchsize to break on and dispatch for post model filters.
    # Given the filtered sizes will vary from batch to batch, which then join together,
    # The potential sizes of batchs will be [FILTER_BATCH_DISPATCH_BREAK - 2x FILTER_BATCH_DISPATCH_BREAK] (60%-120%)
    FILTER_BATCH_DISPATCH_BREAK = 0.6

    @classmethod
    def count_records(
        cls: Type[NLPAttribution],
        ds: LenIterable[Types.DataBatch],
        model: NNB.Model,
        sample_size: int,
        backend: Backend,
        filter_func: Optional[Callable] = None,
        return_iterations: Optional[bool] = False,
    ) -> int:
        """Get the total records if sample size is greater than the total generator, or filters are applied.

        Args:
            ds (LenIterable[Types.DataBatch]): The generator object
            model (NNB.Model): the model object
            sample_size (int): the intended sample size
            backend (Backend): the trulens model backend
            filter_func (Optional[Callable], optional): An optional filter on the generator. Defaults to None.
            return_iterations (Optional[bool], optional): Wether to return the number of iterations. Defaults to False.

        Returns:
            int: The number of records after a take on sample size.
        """
        # Replicated RNN version here due to some small changes which were
        # getting annoy to handle for both RNN and NLP.

        assert isinstance(ds, LenIterable), "LenIterable expected"

        total_records = 0
        # manually update tqdm since this method is intended to break early.
        tqdm_counter = tqdm(
            ds.enumerate(), desc="counting records", unit=ds.unit()
        )
        for batch_iteration, ds_batch in ds.enumerate():
            assert isinstance(ds_batch, Types.DataBatch), "DataBatch expected"
            tqdm_counter.update(1)
            tqdm_counter.refresh()
            if total_records >= sample_size:
                # This batch is not processed
                batch_iteration - 1
                tqdm_counter.update(tqdm_counter.total - tqdm_counter.n)
                tqdm_counter.refresh()
                break

            if filter_func is not None:
                args, kwargs, _, filtered_indices = filter_func(
                    ds_batch, model, backend
                )
                total_records += len(filtered_indices)
            else:
                total_records += len(ds_batch)

        if return_iterations:
            return total_records, batch_iteration
        return total_records

    @staticmethod
    def _get_infl(
        *,
        model: TrulensModelWrapper,
        attribution_cut: Cut,
        output_cut: Cut,
        doi: DoI,
        model_args: convert_struct,
        with_grads: bool = False
    ) -> List[AttributionMethod]:
        # TODO: R&D work, currently QoI at neuron is hacked to be looking at 5 neurons near to it.
        # Eg: If we have QoI has neuron 300 in internal layer, then our qois is [300,..304], so our analysis
        # will be on class_0. See https://truera.atlassian.net/browse/MLNN-297

        if model_args.partition_at == ModelPartition.INPUT_INTERMEDIATE and model_args.qoi_neuron is not None:
            qois = MultiQoI(
                [
                    cl for cl in
                    range(model_args.qoi_neuron, model_args.qoi_neuron + 5)
                ]
            )
        elif model_args.partition_at == ModelPartition.INPUT_INTERMEDIATE and model_args.qoi_neuron is None:
            raise ValueError(
                "QoI neuron argument must be passed for this configuration"
            )
        else:
            qois = MultiQoI([cl for cl in range(model_args.n_output_neurons)])
        if with_grads:
            extra_args = dict(return_grads=True)
        else:
            extra_args = dict()
        return InternalInfluence(
            model=model,
            cuts=(attribution_cut, output_cut),
            qoi=qois,
            doi=doi,
            rebatch_size=model_args.rebatch_size,
            **extra_args
        )

    @staticmethod
    def _get_attrs(
        *,
        inputbatch: Types.InputBatch,
        model_args: convert_struct,
        infl: List[AttributionMethod],
        mem_streamer: MemmapStreamer,
        mem_streamer_gp: MemmapStreamer = None
    ):
        # TODO: reuse ModelInputs or InputBatch
        model_inputs = ModelInputs(
            args=inputbatch.args, kwargs=inputbatch.kwargs
        )
        B = get_backend()

        # Creates files:
        #  {attr_name} memmap
        #  {attr_name}_grad_path memmap

        attributions = []
        if mem_streamer_gp is None:

            # TODO: this can run out of GPU memory, catch like below
            tensor_result = infl._attributions(model_inputs).attributions

            attributions: np.ndarray = numpy_of_nested(
                backend=B, x=tensor_result
            )
            # first two dims are QoI list, DoI input list.
            attributions = [qoi_attr[0] for qoi_attr in attributions]

        else:
            grad_paths = []
            try:
                # grad_path: resolution x batch_size x num_words x embedding_size
                results: AttributionResult = infl._attributions(model_inputs)
            except RuntimeError as e:
                e = Explainer._check_pytorch_rnn_error(e)
                raise e

            # Class, Batch, Word, Embedding
            input_attrs: np.ndarray = numpy_of_nested(
                backend=B, x=results.attributions
            )[:, 0, ...]
            # Batch, Class, Word, Embedding
            input_attrs = np.swapaxes(input_attrs, 0, 1)
            # Class, Resolution, Batch, Word, Embedding
            grad_paths: np.ndarray = numpy_of_nested(
                backend=B, x=results.gradients
            )[:, 0, ...]
            # batch_size x class x num_words x resolution x embedding_size
            if model_args.partition_at == ModelPartition.INTERMEDIATE_OUTPUT:
                grad_paths = grad_paths.transpose(2, 0, 3, 1)
            else:
                grad_paths = grad_paths.transpose(2, 0, 3, 1, 4)

            # batch_size x num_classes x num_words x resolution
            # TODO: this assumes an aggregation scheme, make a configurable parameter?
            grad_paths = np.abs(grad_paths).sum(axis=-1)

            if not mem_streamer_gp.memmap_is_init():
                mem_streamer_gp.init_memmap_fp(
                    QoIType.CLASS_WISE.get_attr_artifact_save_name() +
                    '_grad_path', list(grad_paths.shape[1:])
                )

            mem_streamer_gp.append(grad_paths)

        if model_args.partition_at == ModelPartition.INTERMEDIATE_OUTPUT:
            if not mem_streamer.memmap_is_init():
                mem_streamer.init_memmap_fp(
                    QoIType.CLASS_WISE.get_attr_artifact_save_name(),
                    list(input_attrs.shape[1:])
                )
            mem_streamer.append(input_attrs)
        else:  # (reducing the token dimension for attributions)
            token_attrs = input_attrs.sum(axis=-1)
            if not mem_streamer.memmap_is_init():
                mem_streamer.init_memmap_fp(
                    QoIType.CLASS_WISE.get_attr_artifact_save_name(),
                    list(token_attrs.shape[1:])
                )
            mem_streamer.append(token_attrs)

    @staticmethod
    def _get_baseline_fn(
        *,
        model_args: convert_struct,
        trulens_model: TrulensModelWrapper,
        tokenizer: Wrappers.TokenizerWrapper,
        attribution_cut: Cut,
        embedding_layer: Optional[str] = None,
        input_anchor: Optional[str] = None,
        model: Optional[NNB.Model] = None,
        model_run_wrapper: Optional[Wrappers.ModelRunWrapper.WithEmbeddings
                                   ] = None,
        return_baseline_tokens: bool = False,
    ) -> Callable[[TensorLike, ModelInputs], TensorLike]:
        """Generate baselines for NLP use cases in a 3 step process:
          1. Get inputs to embedding layer (tokens)
          2. Get baseline token IDs by replacing all tokens with the baseline token
          3. Forward pass the baseline token IDs to the DoI cut

        One of following must be defined:
          1. embedding_layer and input_anchor: Will get embeddings using TruLens forward prop call
          2. model_run_wrapper: Will get embeddings with `model_run_wrapper.get_embeddings()`
        """
        if embedding_layer is not None:
            assert input_anchor
        else:
            # model can be None if model_run_wrapper.get_embeddings() runs
            # without model parameter, so only check model_run_wrapper is provided
            assert model_run_wrapper is not None

        # Output should be differentiable wrt tensor at slice (embedding_layer, embedding_anchor)
        def baseline_embedding_fn(embeddings, model_inputs: ModelInputs):
            B = get_backend()

            # Get token IDs
            # TODO: determine whether rebatching must be done here
            if embedding_layer is not None:
                token_cut = Cut(embedding_layer, input_anchor)
                # TODO: use _fprop
                input_ids = trulens_model.fprop(
                    model_args=model_inputs.args,
                    model_kwargs=model_inputs.kwargs,
                    to_cut=token_cut
                )
            else:
                # If no embedding_layer is defined, input layer is assumed to be embedding layer
                # and model_inputs provided are token IDs
                input_ids = B.as_tensor(
                    B.as_array(model_inputs.args[0], dtype='int')
                )

            device = input_ids.device if hasattr(input_ids, "device") else None

            input_ids_dtype = input_ids.dtype
            input_ids = np.copy(B.as_array(input_ids))
            if not np.issubdtype(input_ids.dtype, np.integer):
                raise RuntimeError(
                    f"Embedding layer inputs were of type {input_ids_dtype} instead of integer token ids. "
                    f"Make sure you set embedding_layer to the very first place in the network that token ids get transformed into embeddings."
                )

            # Replace input_ids with baseline token
            replacement_token = tokenizer.id_of_token(model_args.ref_token)
            keep_tokens = set(tokenizer.special_token_ids)

            if len(set(np.unique(input_ids)) - keep_tokens) == 0:
                logger.warn(
                    f"NLP Baseline: Retaining all {len(keep_tokens)} tokens. No replacement will be performed and baseline will match input text. This may result in influences with magnitude 0."
                )

            idxer = np.isin(input_ids, list(keep_tokens), invert=True)
            input_ids[idxer] = replacement_token
            baseline_input_ids = B.as_tensor(
                input_ids, dtype=input_ids_dtype, device=device
            )

            intervention = baseline_input_ids
            doi_cut = token_cut if embedding_layer is not None else None

            baseline = trulens_model.fprop(
                model_args=model_inputs.args,
                model_kwargs=model_inputs.kwargs,
                doi_cut=doi_cut,
                to_cut=attribution_cut,
                intervention=intervention
            )

            if return_baseline_tokens:
                return baseline, intervention
            else:
                return baseline

        return baseline_embedding_fn

    @staticmethod
    def _get_activations(
        *,
        inputbatch: Types.InputBatch,
        baseline_embedding_fn: Callable,
        tl_model: TrulensModelWrapper,
        embedding_cut: Cut,
        output_cut: Optional[Cut] = None,
        mem_streamer_activation: Optional[MemmapStreamer] = None,
        mem_streamer_baseline_activation: Optional[MemmapStreamer] = None
    ):
        B = get_backend()
        model_inputs = ModelInputs(
            args=inputbatch.args, kwargs=inputbatch.kwargs
        )

        if output_cut is None:
            output_cut = OutputCut()

        # Compute activation
        activations: np.ndarray = numpy_of_nested(
            backend=B,
            x=tl_model.fprop(
                model_args=model_inputs.args,
                model_kwargs=model_inputs.kwargs,
                to_cut=output_cut,
            )
        )

        # Compute baseline activation
        baseline_embeddings: np.ndarray = B.as_array(
            baseline_embedding_fn(None, model_inputs=model_inputs)
        )
        baseline_activations: np.ndarray = numpy_of_nested(
            backend=B,
            x=tl_model.fprop(
                model_args=model_inputs.args,
                intervention=baseline_embeddings,
                model_kwargs=model_inputs.kwargs,
                doi_cut=embedding_cut,
                to_cut=output_cut,
            )
        )

        # Save activation
        if mem_streamer_activation:
            if not mem_streamer_activation.memmap_is_init():
                mem_streamer_activation.init_memmap_fp(
                    'activations', list(activations.shape[1:])
                )
            mem_streamer_activation.append(activations)

        if mem_streamer_baseline_activation:
            # Save baseline activation
            if not mem_streamer_baseline_activation.memmap_is_init():
                mem_streamer_baseline_activation.init_memmap_fp(
                    'baseline_activations',
                    list(baseline_activations.shape[1:])
                )
            mem_streamer_baseline_activation.append(baseline_activations)

        return activations, baseline_activations

    @staticmethod
    def accessor_logits(t):
        # TODO: integrate common accessors into trulens

        if hasattr(t, "logits"):
            return getattr(t, "logits")
        # we are only guessing that model output here is logits
        return t

    @staticmethod
    def calculate_attribution(
        *,
        split_ds: LenIterable[Types.DataBatch],
        batch_size: int,
        model: NNB.Model,
        tokenizer: Wrappers.TokenizerWrapper,
        model_run_wrapper: Wrappers.ModelRunWrapper,
        output_path: Path,
        sample_size: int,
        model_args: convert_struct,
        backend: Backend,
        baseline_type: BaselineType = BaselineType.DYNAMIC,
        baseline: Optional[TensorLike] = None,
        resolution: int = DEFAULT_IG_RESOLUTION,
        gradient_path_sample_size: int = 0,
        filter_func: FilterFunc = None
    ) -> None:
        output_path = as_path(output_path, warn=True)

        if backend == Backend.PYTORCH:
            import torch
            if model_args.use_training_mode:
                logger.warn(
                    "configuration attribute `use_training_mode` is set to `True`. Only use this if you ran into torch errors. Otherwise, torch uses this parameter which can cause inconsistenty on gradients or batch norms."
                )
                model.train()
            else:
                model.eval()
            torch.backends.cudnn.enabled = model_args.use_cuda

        tl_model = get_model_wrapper(
            model, force_eval=not model_args.use_training_mode
        )

        # Renable this to figure out the correct run configuration.
        # tl_model.print_layer_names()

        if model_args.output_layer == Layer.OUTPUT:
            output_cut = OutputCut(accessor=NLPAttribution.accessor_logits)
        else:
            output_cut = Cut(
                model_args.output_layer,
                anchor=model_args.output_anchor or 'out',
                accessor=NLPAttribution.accessor_logits
            )

        if model_args.attribution_layer is not None:
            attribution_cut = Cut(
                model_args.attribution_layer,
                anchor=model_args.attribution_anchor,
                accessor=None
            )
        elif model_args.embedding_layer == Layer.INPUT:
            attribution_cut = InputCut()
        else:
            attribution_cut = Cut(
                model_args.embedding_layer,
                anchor=model_args.embedding_anchor,
                accessor=None
            )

        ## Compute the baseline.
        # TODO: redundancy here compared to NLP.ModelRunWrapper
        if baseline_type == BaselineType.FIXED:
            # TODO: whats the point of the FIXED baseline handling in model.get_baseline?
            assert baseline is not None
            baseline_embedding_fn = baseline
        elif baseline_type == BaselineType.DYNAMIC:
            replacement_token = tokenizer.id_of_token(model_args.ref_token)
            keep_tokens = set(tokenizer.special_token_ids)
            if replacement_token == tokenizer.unk_token_id:
                logger.warn(
                    f"NLP Baseline: The ref_token `{model_args.ref_token}` was not found. Using the unknown token instead."
                )
            if len(keep_tokens) == 0:
                logger.warn(
                    "NLP Baseline: No keep_tokens. All tokens will be replaced"
                )
            baseline_embedding_fn = NLPAttribution._get_baseline_fn(
                model_args=model_args,
                trulens_model=tl_model,
                tokenizer=tokenizer,
                attribution_cut=attribution_cut,
                embedding_layer=model_args.embedding_layer,
                input_anchor=model_args.input_anchor,
                model=model,
                model_run_wrapper=model_run_wrapper
            )
        else:
            raise ValueError(f"unsupported baseline type {baseline_type}")

        if resolution is None:
            resolution = DEFAULT_IG_RESOLUTION

        doi = LinearDoi(
            baseline=baseline_embedding_fn,
            resolution=resolution,
            cut=attribution_cut
        )

        # Set up output writers
        mem_streamer = MemmapStreamer(output_path, sample_size)
        mem_streamer_activation = MemmapStreamer(output_path, sample_size)
        mem_streamer_baseline_activation = MemmapStreamer(
            output_path, sample_size
        )

        mem_streamer_gp = None
        if gradient_path_sample_size > 0:
            mem_streamer_gp = MemmapStreamer(
                output_path, gradient_path_sample_size
            )
        post_model_processor = None
        # Compute the attribution method.
        infl: List[AttributionMethod] = NLPAttribution._get_infl(
            model=tl_model,
            attribution_cut=attribution_cut,
            output_cut=output_cut,
            doi=doi,
            model_args=model_args,
            with_grads=mem_streamer_gp is not None
        )
        # manually track tqdm since loop can break early intentionally (sample size is reached)
        tqdm_counter = tqdm(
            split_ds, desc="computing influence", unit="DataBatch"
        )
        for ds_batch in split_ds:
            ds_batch: Types.DataBatch
            tqdm_counter.update(1)
            tqdm_counter.refresh()
            if mem_streamer.memmap_is_full():
                tqdm_counter.update(tqdm_counter.total - tqdm_counter.n)
                tqdm_counter.refresh()
                break

            if filter_func is not None:
                if post_model_processor is None:
                    post_model_processor = PostModelFilterProcessor(
                        model_run_wrapper, ds_batch, model, batch_size,
                        filter_func, backend
                    )
                post_model_processor.process(ds_batch, model)
                if (
                    mem_streamer.total_records +
                    post_model_processor.get_batch_size() < sample_size and
                    post_model_processor.get_batch_size() <
                    NLPAttribution.FILTER_BATCH_DISPATCH_BREAK * batch_size
                ):
                    continue
                else:
                    big_inputbatch: Types.InputBatch = Types.InputBatch(
                        *post_model_processor.dispatch()
                    )
            else:
                big_inputbatch: Types.InputBatch = model_run_wrapper.inputbatch_of_databatch(
                    ds_batch, model=model, tokenizer=tokenizer
                )
            # rebatching to what the model is expected to handle
            # TODO: figure out if Trulens should do this for us like it does
            # when computing IG.

            # Currently we are looking at activations at final layer for Input_Intermediate configuration
            # (which is same as starting layer for Intermediate_Output configuration).

            big_inputbatch.for_batch(
                func=lambda inputbatch: NLPAttribution._get_attrs(
                    inputbatch=inputbatch,
                    model_args=model_args,
                    infl=infl,
                    mem_streamer=mem_streamer,
                    mem_streamer_gp=mem_streamer_gp,
                ),
                batch_size=model_args.rebatch_size * 2,  # NOTE: heuristic
            )

            big_inputbatch.for_batch(
                func=lambda inputbatch: NLPAttribution._get_activations(
                    inputbatch=inputbatch,
                    baseline_embedding_fn=baseline_embedding_fn,
                    tl_model=tl_model,
                    embedding_cut=attribution_cut,
                    output_cut=output_cut,
                    mem_streamer_activation=mem_streamer_activation,
                    mem_streamer_baseline_activation=
                    mem_streamer_baseline_activation
                ),
                batch_size=model_args.rebatch_size * 2,
            )

            # note that some part of trulens' computation can be done in
            # batches larger than rebatch_size. The other things are rebatched
            # within trulens to rebatch_size separately from the batch_size
            # argument above.

        mem_streamer.close()
        mem_streamer_activation.close()
        mem_streamer_baseline_activation.close()
        if mem_streamer_gp is not None:
            mem_streamer_gp.close()

    @staticmethod
    def calculate_attribution_per_original_word(output_path: Path) -> None:
        """
        combine attribution of tokens into attribution of original words using generated index mappings
        """

        # Uses files:
        #  {output_path}/{attr_name} memmap
        #  {output_path}/{attr_name}_grad_path memmap
        #  {output_path}/sentence_length_tokens memmap
        #  {output_path}/index_mappings pickle
        #  {output_path}/words pickle

        # Creates files:
        #  {output_path}/{attr_name}_original_word memmap
        #  {output_path}/{attr_name}_grad_path_original_word memmap

        output_path = as_path(output_path, warn=True)
        attr_name = QoIType.CLASS_WISE.get_attr_artifact_save_name()

        token_attr = load_memmap(output_path, attr_name)

        token_attr_grad_path = load_memmap(
            output_path, attr_name + '_grad_path'
        )

        index_mappings = load_pickle(output_path, 'index_mappings')
        text_list = load_text_data(output_path, "original_text")
        word_list = load_pickle(output_path, 'words')
        token_list = load_pickle(output_path, 'tokens')

        attr_original_word = combine_tokenized_influence_per_original_word(
            text_list=text_list,
            token_list=token_list,
            word_list=word_list,
            token_attrs=token_attr,
            index_mappings=index_mappings,
        )
        grad_path_original_word = combine_tokenized_influence_per_original_word(
            text_list=text_list,
            token_list=token_list,
            word_list=word_list,
            token_attrs=token_attr_grad_path,
            index_mappings=index_mappings,
        )
        save_memmap(
            output_path,
            attr_name + '_original_word',
            list(attr_original_word),
            dtype='float32'
        )
        save_memmap(
            output_path,
            attr_name + '_grad_path' + '_original_word',
            list(grad_path_original_word),
            dtype='float32'
        )
