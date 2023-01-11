# SMALL DEBT

import functools

import numpy as np
from trulens.nn.backend import Backend

from truera.client.nn import NNBackend as NNB
from truera.client.nn.wrappers.timeseries import Wrappers as Timeseries


# TODO this is a placeholder that only works on one customer model, use modelwrapper.convert_model_eval_to_binary_classifier if we decide to use this more broadly
def baseline_minimizer(x):
    '''
    Define a metric on the model output that will be minimized if model output baseline is used
    '''
    return (1 - x[..., 0:1]).sum(axis=1).squeeze()


def _accuracy_labeler(preds, labels, threshold=0.5):
    '''
    Using model predictions and labels, create segment labels ['TP','FP','TN','FN']
    '''
    accuracy_labels = []
    pred_class = preds > threshold
    for i in range(len(preds)):
        if (pred_class[i] and labels[i]):
            accuracy_labels.append("TP")
        elif (pred_class[i] and not labels[i]):
            accuracy_labels.append("FP")
        elif (not pred_class[i] and labels[i]):
            accuracy_labels.append("FN")
        else:
            accuracy_labels.append("TN")
    return accuracy_labels


def evaluate_model_helper(
    model_wrapper: Timeseries.ModelRunWrapper,
    ds_batch: Timeseries.Types.DataBatch, model: NNB.Model
):
    inputbatch = model_wrapper.inputbatch_of_databatch(ds_batch, model)
    return model_wrapper.evaluate_model(model, inputbatch)


def accuracy_filter_func(config_args, model_wrapper):
    return functools.partial(
        PostModelFilterProcessor.filter_by_accuracy_labels, config_args,
        model_wrapper
    )


class PostModelFilterProcessor(object):
    '''
    Class that helps filter dataset batches given confusion matrix designations, and rebatches for optimal GPU usage. 
    '''

    def __init__(
        self, model_wrapper, ds_batch, model, batch_size, filter_func, backend
    ):
        self.filter_func = filter_func
        self.backend = backend
        self.clear()
        self.batched_indicator, self.tensor_indicator = PostModelFilterProcessor._get_input_metadata(
            model_wrapper, ds_batch, model, batch_size, self.backend
        )

    @staticmethod
    def _get_input_metadata(
        model_wrapper, ds_batch, model, batch_size, backend
    ):
        '''
        keep track of which args/kwargs are batched inputs or tensor inputs.
        batched inputs will be filtered. tensor inputs need to be temporarily converted to nparray.
        '''
        args, kwargs = model_wrapper.model_input_args_kwargs(ds_batch, model)
        batched_indicator = {}
        tensor_indicator = {}
        batched_indicator['args'] = [
            len(arg) == batch_size if hasattr(arg, '__len__') else False
            for arg in args
        ]
        batched_indicator['kwargs'] = {
            k: len(v) == batch_size if hasattr(v, '__len__') else False
            for k, v in kwargs.items()
        }

        if backend == Backend.PYTORCH:
            import torch
            tensor_indicator['args'] = [torch.is_tensor(arg) for arg in args]
            tensor_indicator['args_device'] = [
                'cpu' if not is_tensor else arg.device
                for is_tensor, arg in zip(tensor_indicator['args'], args)
            ]
            tensor_indicator['kwargs'] = {}
            tensor_indicator['kwargs_device'] = {}
            for k, v in kwargs.items():
                tensor_indicator['kwargs'][k] = torch.is_tensor(v)
                if not torch.is_tensor(v):
                    tensor_indicator['kwargs_device'][k] = 'cpu'
                else:
                    tensor_indicator['kwargs_device'][k] = v.device
        elif backend == Backend.TENSORFLOW or backend == Backend.TF_KERAS:
            import tensorflow as tf
            tensor_indicator['args'] = [tf.is_tensor(arg) for arg in args]

            tensor_indicator['kwargs'] = {
                k: tf.is_tensor(v) for k, v in kwargs.items()
            }

            if 'feed_dict' in kwargs:
                batched_indicator['feed_dict'] = {
                    k: len(v) == batch_size if hasattr(v, '__len__') else False
                    for k, v in kwargs['feed_dict'].items()
                }
                tensor_indicator['feed_dict'] = {
                    k: tf.is_tensor(v) for k, v in kwargs['feed_dict'].items()
                }
        else:
            raise Exception(
                'Post model filters for this backend are not yet supported'
            )

        return batched_indicator, tensor_indicator

    @staticmethod
    def _join_args_kwargs(args1, args2, kwargs1, kwargs2, batched_indicator):
        '''
        Concatenate filtered results together. only join batched structures in args/kwargs/feed_dict
        '''
        for i in range(len(args1)):
            if batched_indicator['args'][i]:
                args1[i] = np.concatenate((args1[i], args2[i]))

        for k in kwargs1:
            if batched_indicator['kwargs'][k]:
                kwargs1[k] = np.concatenate((kwargs1[k], kwargs2[k]))

        if 'feed_dict' in kwargs1:
            for k in kwargs1['feed_dict']:
                if batched_indicator['feed_dict'][k]:
                    kwargs1['feed_dict'][k] = np.concatenate(
                        (kwargs1['feed_dict'][k], kwargs2['feed_dict'][k])
                    )
        return args1, kwargs1

    @staticmethod
    def _convert_args_kwargs_to_tensor(args, kwargs, tensor_indicator, backend):
        '''
        Filtering will have operated on non tensors. Convert back to tensor if the arg/kwargs/feed_dict structures were originally tensors.
        '''
        if backend == Backend.PYTORCH:
            import torch
        elif backend == Backend.TENSORFLOW or backend == Backend.TF_KERAS:
            import tensorflow as tf
        else:
            raise Exception(
                'Post model filters for this backend are not yet supported'
            )
        for i in range(len(args)):
            if tensor_indicator['args'][i]:
                if backend == Backend.PYTORCH:
                    args[i] = torch.from_numpy(args[i]).to(
                        tensor_indicator['args_device'][i]
                    )
                elif backend == Backend.TENSORFLOW or backend == Backend.TF_KERAS:
                    args[i] = tf.convert_to_tensor(args[i])

        for k in kwargs:
            if tensor_indicator['kwargs'][k]:
                if backend == Backend.PYTORCH:
                    kwargs[k] = torch.from_numpy(kwargs[k]).to(
                        tensor_indicator['kwargs_device'][k]
                    )
                elif backend == Backend.TENSORFLOW or backend == Backend.TF_KERAS:
                    kwargs[k] = tf.convert_to_tensor(kwargs[k])

        if 'feed_dict' in kwargs:
            for k in kwargs['feed_dict']:
                if tensor_indicator['feed_dict'][k]:
                    kwargs['feed_dict'][k] = tf.convert_to_tensor(
                        kwargs['feed_dict'][k]
                    )

        return args, kwargs

    @staticmethod
    def filter_batched_data(x, batch_size, filtered_indices, backend):
        '''
        Apply filtered indices to x, if x is a batched tensor or numpy array.
        Filtered outputs of this will be numpy arrays to allow subsequent methods to operate 
        '''
        # check x is tensor and size is batch_size.
        # this is because x can be given any arg from args or kwargs, and we use this naive check to make sure it is
        # a batched input rather than some other supplementary data.
        # In that case, return the arg/kwarg unfiltered.
        if isinstance(x, np.ndarray) and len(x) == batch_size:
            return np.take(x, filtered_indices, axis=0)
        elif isinstance(x, list) and len(x) == batch_size:
            if isinstance(x[0], str):  ## text data used in nlp
                return [x[fi] for fi in filtered_indices]
        elif backend == Backend.PYTORCH:
            import torch
            if torch.is_tensor(x) and len(x) == batch_size:
                return np.take(
                    x.detach().cpu().numpy(), filtered_indices, axis=0
                )
        elif backend == Backend.TENSORFLOW or backend == Backend.TF_KERAS:
            import tensorflow as tf
            if tf.is_tensor(x) and len(x) == batch_size:
                return tf.convert_to_tensor(
                    np.take(x.numpy(), filtered_indices, axis=0)
                )
        return x

    def clear(self):
        '''
        clears the current args/kwargs to None.
        '''
        self.curr_filtered_batch_size = 0
        self.curr_args = None
        self.curr_kwargs = None

    def process(self, ds_batch, model):
        '''
        Takes an unfiltered ds_batch, filter it, then join with a previous filtered batch.
        '''
        args, kwargs, _, filtered_indices = self.filter_func(
            ds_batch, model, self.backend
        )
        assert args is not None
        assert kwargs is not None
        self.curr_filtered_batch_size += len(filtered_indices)
        if self.curr_args is not None:
            self._join_args_kwargs(
                self.curr_args, args, self.curr_kwargs, kwargs,
                self.batched_indicator
            )
        else:
            self.curr_args = args
            self.curr_kwargs = kwargs

    def dispatch(self):
        '''
        Dispatch the aggregated filtered batches to be sent into model inputs.
        Convert args/kwargs to tensor if needed. 
        '''
        if self.curr_args is None:
            return None, None
        return_args, return_kwargs = self._convert_args_kwargs_to_tensor(
            self.curr_args, self.curr_kwargs, self.tensor_indicator,
            self.backend
        )
        self.clear()
        return return_args, return_kwargs

    def get_batch_size(self):
        '''
        return the current aggregated batch size to inform when to dispatch.
        '''
        return self.curr_filtered_batch_size

    @classmethod
    def filter_by_accuracy_labels(
        cls, config_args, model_wrapper, ds_batch, model, backend
    ):
        '''
        Filter args/kwargs by confusion matrix designations in config_args.post_model_filter_labels
        '''
        args, kwargs = model_wrapper.model_input_args_kwargs(ds_batch, model)
        full_preds = evaluate_model_helper(model_wrapper, ds_batch, model)

        preds = model_wrapper.convert_model_eval_to_binary_classifier(
            ds_batch, full_preds, labels=False
        )
        labels = model_wrapper.convert_model_eval_to_binary_classifier(
            ds_batch,
            model_wrapper.ds_elements_to_truera_elements(ds_batch,
                                                         model)['labels'],
            labels=True
        )

        accuracy_labels = _accuracy_labeler(
            preds, labels, config_args.post_model_filter_thresh
        )
        filtered_indices = []
        for i in range(len(accuracy_labels)):
            if (accuracy_labels[i] in config_args.post_model_filter_labels):
                filtered_indices.append(i)

        batch_size = len(preds)
        args = [
            cls.filter_batched_data(arg, batch_size, filtered_indices, backend)
            for arg in args
        ]
        kwargs = {
            k: cls.filter_batched_data(
                kwargs[k], batch_size, filtered_indices, backend
            ) for k in kwargs
        }

        if 'feed_dict' in kwargs:
            kwargs['feed_dict'] = {
                k: cls.filter_batched_data(
                    kwargs['feed_dict'][k], batch_size, filtered_indices,
                    backend
                ) for k in kwargs['feed_dict']
            }

        return args, kwargs, cls.filter_batched_data(
            full_preds, batch_size, filtered_indices, backend
        ), filtered_indices
