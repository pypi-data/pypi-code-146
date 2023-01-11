from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterator, Optional, Type, Union

import numpy as np
import torch.nn
from tqdm import tqdm
from trulens.nn.attribution import InternalInfluence
from trulens.nn.backend import Backend
from trulens.nn.backend import get_backend
from trulens.nn.distributions import PointDoi
from trulens.nn.models._model_base import ModelWrapper as TrulensModelWrapper
from trulens.nn.slices import Cut
from trulens.nn.slices import InputCut
from trulens.nn.slices import OutputCut
from trulens.utils.typing import ModelInputs
from trulens.utils.typing import nested_cast
from trulens.utils.typing import nested_map
from trulens.utils.typing import om_of_many
from trulens.utils.typing import TensorLike

from truera.client.intelligence.explainer import Explainer
from truera.client.nn import NNBackend as NNB
from truera.client.nn.client_configs import Dimension
from truera.client.nn.client_configs import Layer
from truera.client.nn.client_configs import LayerAnchor
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.wrappers.timeseries import Wrappers as Timeseries
from truera.rnn.general.model_runner_proxy.dimension_utils import \
    transpose_to_standard_dimensions
from truera.rnn.general.model_runner_proxy.dimension_utils import \
    TrueraDimension
from truera.rnn.general.model_runner_proxy.explain_helpers import \
    PostModelFilterProcessor
from truera.rnn.general.model_runner_proxy.mem_utils import get_memmap_fp
from truera.rnn.general.model_runner_proxy.rnn_distributions import \
    RNNLinearDoi
from truera.rnn.general.model_runner_proxy.rnn_quantities import \
    InternalAveragePerTimestepQoI
from truera.rnn.general.model_runner_proxy.rnn_quantities import PerTimestepQoI

DATA_CONTAINER_TYPE = (list, tuple)


class RNNAttribution(object):
    # Choose a percentage of the original batchsize to break on and dispatch for post model filters.
    # Given the filtered sizes will vary from batch to batch, which then join together,
    # The potential sizes of batchs will be [FILTER_BATCH_DISPATCH_BREAK - 2x FILTER_BATCH_DISPATCH_BREAK] (60%-120%)
    FILTER_BATCH_DISPATCH_BREAK = 0.6

    @staticmethod
    def get_explainer_model_wrapper(
        model: NNB.Model,
        *,
        n_time_step_input: int,
        n_features_input: int,
        backend: Backend,
        output_layer: Optional[str] = None,
        ingestion_model_wrapper: Optional[Timeseries.ModelRunWrapper] = None,
        force_eval: Optional[bool] = None
    ) -> TrulensModelWrapper:
        """Returns TruLens Model Wrapper from model

        Args:
            model (Model): The model to wrap. Tensorflow, Keras, and PyTorch models are supported
            n_time_step_input (int): Number of time steps in input tensor
            n_features_input (int): Number of features in input tensor
            backend (Backend): TruLens backend representing the model's library
            output_layer (Optional[str], optional): Name of the model output layer. Defaults to None.
            ingestion_model_wrapper (Optional[Timeseries.ModelRunWrapper], optional): Optional 
                ModelRunWrapper used to get computation graph and session from TF1 model. Defaults to None.
            force_eval (Optional[bool], optional): True sets the model in evaluation mode with 
                model.eval() for PyTorch models. Defaults to None.

        Returns:
            TrulensModelWrapper: The TruLens model wraper used to compute influences
        """
        from trulens.nn.models import get_model_wrapper
        if ingestion_model_wrapper and hasattr(
            ingestion_model_wrapper, "tf1_get_graph_and_session"
        ) and callable(ingestion_model_wrapper.tf1_get_graph_and_session):
            import tensorflow as tf

            input_tensors = []
            for attr in dir(model):
                model_obj = getattr(model, attr, None)
                if tf.is_tensor(
                    model_obj
                ) and model_obj.op.type == 'Placeholder':
                    input_tensors.append(model_obj)
            (graph, session
            ) = ingestion_model_wrapper.tf1_get_graph_and_session(model)
            output_tensor = graph.get_tensor_by_name(output_layer)
            nl_model = get_model_wrapper(
                graph,
                input_tensors=input_tensors,
                output_tensors=[output_tensor],
                session=session
            )
        elif backend == Backend.PYTORCH:
            input_shape = (n_time_step_input, n_features_input)
            nl_model = get_model_wrapper(
                model, input_shape=input_shape, force_eval=force_eval
            )
        else:
            nl_model = get_model_wrapper(model)
        return nl_model

    @classmethod
    def count_records(
        cls: Type[RNNAttribution],
        ds: Iterator[Timeseries.Types.DataBatch],
        ingestion_model_wrapper: Optional[Type[Timeseries.ModelRunWrapper]],
        model: NNB.Model,
        sample_size: int,
        backend: Backend,
        filter_func: Optional[Callable] = None,
        return_iterations: Optional[bool] = False
    ):
        total_records = 0
        for batch_iteration, ds_batch in enumerate(
            tqdm(ds, desc="counting records", unit="batch")
        ):
            if (total_records >= sample_size):
                # This batch is not processed
                batch_iteration - 1
                break

            if (filter_func is not None):
                args, kwargs, _, filtered_indices = filter_func(
                    ds_batch, model, backend
                )
                total_records += len(filtered_indices)
            else:
                inputbatch = ingestion_model_wrapper.inputbatch_of_databatch(
                    ds_batch, model
                )
                full_preds = ingestion_model_wrapper.evaluate_model(
                    model, inputbatch
                )
                total_records += len(full_preds)

        if return_iterations:
            return total_records, batch_iteration
        return total_records

    @staticmethod
    def calculate_attribution_per_timestep(
        ds: Iterator[Timeseries.Types.DataBatch],
        ingestion_model_wrapper: Type[Timeseries.ModelRunWrapper],
        model: NNB.Model,
        baseline: TensorLike,
        output_path: Path,
        sample_size: int,
        attr_config: RNNAttributionConfiguration,
        backend: Backend,
        resolution: Optional[int] = 10,
        filter_func: Optional[Callable] = None,
        input_anchor: Optional[Union[str, LayerAnchor]] = "in",
        output_anchor: Optional[Union[str, LayerAnchor]] = "out",
        max_iterations: Optional[int] = None,
        compute_interactions: Optional[bool] = True
    ):
        if isinstance(input_anchor, LayerAnchor):
            input_anchor = input_anchor._to_string()
        if isinstance(output_anchor, LayerAnchor):
            output_anchor = output_anchor._to_string()
        if output_anchor is None:
            output_anchor = "out"
        total_attributions = 0
        batch_size = baseline.shape[0]

        if backend == Backend.PYTORCH:
            if attr_config.use_training_mode:
                model.train()
            else:
                model.eval()
            torch.backends.cudnn.enabled = attr_config.use_cuda

        nl_model = RNNAttribution.get_explainer_model_wrapper(
            model,
            n_time_step_input=attr_config.n_time_step_input,
            n_features_input=attr_config.n_features_input,
            backend=backend,
            output_layer=attr_config.output_layer,
            ingestion_model_wrapper=ingestion_model_wrapper,
            force_eval=not attr_config.use_training_mode
        )
        if (attr_config.input_layer == Layer.INPUT):
            attribution_input_cut = InputCut()
        else:
            attribution_input_cut = Cut(
                attr_config.input_layer, input_anchor, None
            )

        if (attr_config.output_layer == Layer.OUTPUT):
            attribution_output_cut = OutputCut()
        else:
            attribution_output_cut = Cut(
                attr_config.output_layer, output_anchor, None
            )
        doi = RNNLinearDoi(
            backend,
            baseline=baseline,
            cut=attribution_input_cut,
            resolution=resolution
        )
        infl = InternalInfluence(
            nl_model, (attribution_input_cut, attribution_output_cut),
            PerTimestepQoI(attr_config),
            doi,
            return_grads=compute_interactions
        )

        def _process_qoi_outputs(data):

            if isinstance(data, DATA_CONTAINER_TYPE):
                # Multiple QoI will return a DATA_CONTAINER_TYPE, this returns it to a single array
                qoi_stacked = np.stack(data, axis=-1)
            else:
                # The way framework grads/attributions can work is that it strips the DATA_CONTAINER_TYPE if only one QoI is ultimately computed
                # We need to add back that single QoI as a dimension
                qoi_stacked = np.expand_dims(data, -1)
            data_shape_dimensions = None
            if attr_config.input_dimension_order:
                data_shape_dimensions = list(attr_config.input_dimension_order
                                            ).copy()
                data_shape_dimensions.append(TrueraDimension.QOI)

            qoi_stacked = transpose_to_standard_dimensions(
                qoi_stacked, (
                    Dimension.BATCH, Dimension.TIMESTEP, Dimension.FEATURE,
                    TrueraDimension.QOI
                ),
                data_dimension_order=data_shape_dimensions
            )

            attr_shape = list(qoi_stacked.shape)[:-1]
            attr_shape.extend(
                [attr_config.n_time_step_output, attr_config.n_output_neurons]
            )

            data = np.reshape(qoi_stacked, tuple(attr_shape))

            return data

        def _save_batched_memmap(
            data, memmap_fp: np.memmap, memmap_name: str, sample_size: int,
            total_attributions: int
        ):
            num_records = len(data)
            if (memmap_fp is None):
                memmap_fp = get_memmap_fp(
                    output_path, memmap_name,
                    [sample_size] + list(data[0].shape)
                )
            if (num_records > 0):
                memmap_fp[total_attributions:total_attributions +
                          num_records] = data
                total_attributions += num_records
            return total_attributions, memmap_fp

        def get_attrs(
            args, kwargs, memmap_fp, grad_path_memmap_fp, total_attributions
        ):
            all_grads = None
            B = get_backend()
            try:
                if compute_interactions:
                    model_inputs = ModelInputs(args=args, kwargs=kwargs)
                    return_type = type(model_inputs.first_batchable(B))
                    pieces = infl._attributions(model_inputs)
                    input_attrs = nested_cast(
                        backend=B, astype=return_type, args=pieces.attributions
                    )
                    input_attrs = [om_of_many(attr) for attr in input_attrs]
                    input_attrs = om_of_many(input_attrs)
                    all_grads = pieces.gradients
                else:
                    input_attrs = infl.attributions(*args, **kwargs)

            except RuntimeError as e:
                e = Explainer._check_pytorch_rnn_error(e)
                raise e

            if B.backend == Backend.PYTORCH:
                map_to_cpu = lambda x: x.cpu() if B.is_tensor(x) else x
                input_attrs = nested_map(input_attrs, map_to_cpu)
                if all_grads:
                    all_grads = nested_map(all_grads, map_to_cpu)

            # Shapes up to this point:
            # input_attrs: Outputs[Inputs[DataLike[feature x timsteps]]] (batch dimension order is the Input list length)
            # all_grads: Outputs[Inputs[DataLike[resolution x batch x feature x timsteps]]]

            input_attrs = _process_qoi_outputs(input_attrs)
            total_attributions_new, memmap_fp = _save_batched_memmap(
                input_attrs, memmap_fp, 'input_attrs_per_timestep', sample_size,
                total_attributions
            )
            if all_grads:
                # All grads is a list of list of data, but the second list is one value as the doi*batch dimension is in the DataLike tensor
                # resolution x batch x in timesteps, features, out timesteps, classes
                all_grads = _process_qoi_outputs(
                    [container[0] for container in all_grads]
                )
                # get the last qoi
                # resolution x batch x in timesteps, features, classes
                grad_paths = all_grads[:, :, :, :, -1, :]
                # reset batch to first dimension
                grad_paths = np.swapaxes(grad_paths, 0, 1)
                _, grad_paths_memmap_fp = _save_batched_memmap(
                    grad_paths, grad_path_memmap_fp, 'grad_paths_last',
                    sample_size, total_attributions
                )
                return total_attributions_new, memmap_fp, grad_paths_memmap_fp

            return total_attributions_new, memmap_fp, None

        memmap_fp = None
        grad_path_memmap_fp = None
        post_model_processor = None
        for batch, ds_batch in enumerate(
            tqdm(
                ds,
                total=max_iterations,
                desc="computing attributions",
                unit="batch"
            )
        ):
            if (total_attributions >= sample_size):
                break
            if (filter_func is not None):
                if post_model_processor is None:
                    post_model_processor = PostModelFilterProcessor(
                        ingestion_model_wrapper, ds_batch, model, batch_size,
                        filter_func, backend
                    )
                post_model_processor.process(ds_batch, model)
                if (
                    total_attributions + post_model_processor.get_batch_size() <
                    sample_size and post_model_processor.get_batch_size() <
                    RNNAttribution.FILTER_BATCH_DISPATCH_BREAK * batch_size
                ):
                    continue
                else:
                    args, kwargs = post_model_processor.dispatch()
            else:
                inputbatch = ingestion_model_wrapper.inputbatch_of_databatch(
                    ds_batch, model
                )
                args, kwargs = inputbatch.args, inputbatch.kwargs

            total_attributions, memmap_fp, grad_path_memmap_fp = get_attrs(
                args, kwargs, memmap_fp, grad_path_memmap_fp, total_attributions
            )
        if post_model_processor is not None and total_attributions < sample_size:
            args, kwargs = post_model_processor.dispatch()
            # last batch process
            if args is not None:
                total_attributions, memmap_fp, grad_path_memmap_fp = get_attrs(
                    args, kwargs, memmap_fp, grad_path_memmap_fp,
                    total_attributions
                )
        del memmap_fp, grad_path_memmap_fp

    @staticmethod
    def calculate_internal_attribution_per_timestep(
        ds: Iterator[Timeseries.Types.DataBatch],
        ingestion_model_wrapper: Type[Timeseries.ModelRunWrapper],
        model: NNB.Model,
        batch_size: int,
        output_path: Path,
        sample_size: int,
        attr_config: RNNAttributionConfiguration,
        backend: Backend,
        filter_func: Optional[Callable] = None,
        input_anchor: Optional[Union[str, LayerAnchor]] = "in",
        output_anchor: Optional[Union[str, LayerAnchor]] = "out",
        internal_anchor: Optional[Union[str, LayerAnchor]] = "out"
    ):

        if isinstance(input_anchor, LayerAnchor):
            input_anchor = input_anchor._to_string()
        if isinstance(output_anchor, LayerAnchor):
            output_anchor = output_anchor._to_string()
        if output_anchor is None:
            output_anchor = "out"
        if isinstance(internal_anchor, LayerAnchor):
            internal_anchor = internal_anchor._to_string()

        nl_model = RNNAttribution.get_explainer_model_wrapper(
            model,
            n_time_step_input=attr_config.n_time_step_input,
            n_features_input=attr_config.n_features_input,
            backend=backend,
            output_layer=attr_config.output_layer,
            ingestion_model_wrapper=ingestion_model_wrapper
        )

        if (attr_config.input_layer == Layer.INPUT):
            attribution_input_cut = InputCut()
        else:
            attribution_input_cut = Cut(
                attr_config.input_layer, input_anchor, None
            )

        if (attr_config.output_layer == Layer.OUTPUT):
            attribution_output_cut = OutputCut()
        else:
            attribution_output_cut = Cut(
                attr_config.output_layer, output_anchor, None
            )
        doi_cut = attribution_input_cut
        doi = RNNLinearDoi(backend, cut=doi_cut)
        point_doi = PointDoi(cut=doi_cut)

        def get_internal_attrs(
            args, kwargs, inner_memmap_fp, outer_memmap_fp, total_attributions
        ):
            infl = InternalInfluence(
                nl_model, (
                    Cut(attr_config.internal_layer, internal_anchor,
                        None), attribution_output_cut
                ), PerTimestepQoI(attr_config), doi
            )

            outer_attrs = infl.attributions(*args, **kwargs)

            # start with (timestep_out*classes) x batch x timestep (in) x Nfeatures
            # convert to batch x timestep (in) x Nfeatures x timestep (out) x classes

            if isinstance(outer_attrs, DATA_CONTAINER_TYPE):
                # Multiple QoI will return a DATA_CONTAINER_TYPE, this returns it to a single array
                qoi_stacked = np.stack(outer_attrs, axis=-1)
            else:
                # The way framework grads/attributions can work is that it strips the DATA_CONTAINER_TYPE if only one QoI is ultimately computed
                # We need to add back that single QoI as a dimension
                qoi_stacked = np.expand_dims(outer_attrs, -1)
            attr_shape = list(qoi_stacked.shape)[:-1]
            attr_shape.extend(
                [attr_config.n_time_step_output, attr_config.n_output_neurons]
            )

            outer_attrs = np.reshape(qoi_stacked, tuple(attr_shape))

            num_records = len(outer_attrs)
            num_neurons = attr_config.n_internal_neurons

            for j in tqdm(
                range(attr_config.n_internal_neurons),
                desc="computing internal attribution",
                unit="neuron"
            ):
                cq = InternalAveragePerTimestepQoI(j)
                infl_j = InternalInfluence(
                    nl_model, (
                        Cut(attr_config.input_layer, input_anchor, None),
                        Cut(attr_config.internal_layer, internal_anchor, None)
                    ),
                    cq,
                    point_doi,
                    multiply_activation=False
                )
                attrs_j = np.stack(
                    infl_j.attributions(*args, **kwargs), axis=-1
                )

                # Instantiate memmaps
                if (outer_memmap_fp is None):
                    outer_memmap_fp = get_memmap_fp(
                        output_path, 'outer_attrs_per_timestep',
                        [sample_size] + list(outer_attrs[0].shape)
                    )
                    # batch x timestep x Nfeatures x timestep (out) x neurons
                    inner_memmap_fp = get_memmap_fp(
                        output_path, 'inner_attrs_per_timestep',
                        [sample_size] + list(attrs_j[0].shape) + [num_neurons]
                    )

                # Write straight to memmap
                for record in range(num_records):
                    inner_memmap_fp[total_attributions + record, :, :, :,
                                    j] = attrs_j[record]

            if (num_records > 0):
                outer_memmap_fp[total_attributions:total_attributions +
                                num_records] = outer_attrs
                total_attributions += num_records

            return total_attributions, inner_memmap_fp, outer_memmap_fp

        # Evaluate loop
        total_attributions = 0
        inner_memmap_fp = None
        outer_memmap_fp = None
        post_model_processor = None

        for batch, ds_batch in enumerate(
            tqdm(ds, desc="computing per-timestep attributions", unit="batch")
        ):
            if (total_attributions >= sample_size):
                break
            if (filter_func is not None):
                if post_model_processor is None:
                    post_model_processor = PostModelFilterProcessor(
                        ingestion_model_wrapper, ds_batch, model, batch_size,
                        filter_func, backend
                    )
                post_model_processor.process(ds_batch, model)
                if (
                    total_attributions + post_model_processor.get_batch_size() <
                    sample_size and post_model_processor.get_batch_size() <
                    RNNAttribution.FILTER_BATCH_DISPATCH_BREAK * batch_size
                ):
                    continue
                else:
                    args, kwargs = post_model_processor.dispatch()
            else:
                inputbatch = ingestion_model_wrapper.inputbatch_of_databatch(
                    ds_batch, model
                )
                args, kwargs = inputbatch.args, inputbatch.kwargs
            total_attributions, inner_memmap_fp, outer_memmap_fp = get_internal_attrs(
                args, kwargs, inner_memmap_fp, outer_memmap_fp,
                total_attributions
            )

        if post_model_processor is not None and total_attributions < sample_size:
            args, kwargs = post_model_processor.dispatch()
            # last batch process
            if args is not None:
                total_attributions, inner_memmap_fp, outer_memmap_fp = get_internal_attrs(
                    args, kwargs, inner_memmap_fp, outer_memmap_fp,
                    total_attributions
                )

        del inner_memmap_fp
        del outer_memmap_fp
