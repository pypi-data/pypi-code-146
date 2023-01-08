from dataclasses import dataclass
from typing import List

from onnxruntime import InferenceSession


def replace_stateful_grus(keras_model, onnx_model):
    """Replace stateful GRUs with custom layers."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        from keras.layers import GRU

    stateful_gru_names = []
    for i in range(len(keras_model.layers)):
        layer = keras_model.layers[i]
        if isinstance(layer, GRU):
            if layer.stateful:
                stateful_gru_names.append(layer.name)

    for node_index in range(len(onnx_model.graph.node)):
        node = onnx_model.graph.node[node_index]
        replace = False
        if node.op_type == 'GRU':
            for i in node.input:
                for n in stateful_gru_names:
                    if n in i:
                        replace = True
        if node.name in stateful_gru_names or replace:
            node.op_type = 'SGRU'

    return onnx_model


def add_sonusai_metadata(model,
                         is_flattened: bool = True,
                         has_timestep: bool = True,
                         has_channel: bool = False,
                         is_mutex: bool = True,
                         feature: str = ''):
    """Add SonusAI metadata to ONNX model.
      model           keras model
      is_flattened    model feature data is flattened
      has_timestep    model has timestep dimension
      has_channel     model has channel dimension
      is_mutex        model label output is mutually exclusive
      feature         model feature type
    """
    is_flattened_flag = model.metadata_props.add()
    is_flattened_flag.key = 'is_flattened'
    is_flattened_flag.value = str(is_flattened)

    has_timestep_flag = model.metadata_props.add()
    has_timestep_flag.key = 'has_timestep'
    has_timestep_flag.value = str(has_timestep)

    has_channel_flag = model.metadata_props.add()
    has_channel_flag.key = 'has_channel'
    has_channel_flag.value = str(has_channel)

    is_mutex_flag = model.metadata_props.add()
    is_mutex_flag.key = 'is_mutex'
    is_mutex_flag.value = str(is_mutex)

    feature_flag = model.metadata_props.add()
    feature_flag.key = 'feature'
    feature_flag.value = str(feature)

    return model


@dataclass(frozen=True)
class SonusAIMetaData:
    input_shape: List[int]
    output_shape: List[int]
    flattened: bool
    timestep: bool
    channel: bool
    mutex: bool
    feature: str


def get_sonusai_metadata(model: InferenceSession) -> SonusAIMetaData:
    m = model.get_modelmeta().custom_metadata_map
    return SonusAIMetaData(input_shape=model.get_inputs()[0].shape,
                           output_shape=model.get_outputs()[0].shape,
                           flattened=m['is_flattened'] == 'True',
                           timestep=m['has_timestep'] == 'True',
                           channel=m['has_channel'] == 'True',
                           mutex=m['is_mutex'] == 'True',
                           feature=m['feature'])
