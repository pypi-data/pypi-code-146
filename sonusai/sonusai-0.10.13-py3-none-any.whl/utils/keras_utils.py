from typing import Any

from sonusai import logger


def keras_onnx(model_name: str,
               weight_name: str,
               timesteps: int = None,
               batch_size: int = None,
               output_dir: str = None) -> None:
    from os.path import basename
    from os.path import dirname
    from os.path import join
    from os.path import splitext

    import h5py
    import keras_tuner as kt

    if output_dir is None:
        output_dir = dirname(model_name)

    with h5py.File(weight_name, 'r') as f:
        feature = f.attrs['sonusai_feature']
        num_classes = int(f.attrs['sonusai_num_classes'])

    model = import_keras_model(model_name)
    model_base = basename(model_name)
    model_root = splitext(model_base)[0]
    base_name = join(output_dir, model_root)

    # Build default model to check overrides
    timesteps = check_keras_overrides(model, feature, num_classes, timesteps, batch_size)

    try:
        hypermodel = model.MyHyperModel(feature=feature,
                                        num_classes=num_classes,
                                        timesteps=timesteps,
                                        batch_size=batch_size)
        built_model = hypermodel.build_model(kt.HyperParameters())
    except Exception as e:
        logger.exception(f'Error: build_model() in {model_base} failed: {e}.')
        raise SystemExit(1)

    print('')
    print(f'timesteps               {timesteps}')
    print(f'batch_size              {batch_size}')
    print(f'hypermodel.timesteps    {hypermodel.timesteps}')
    print(f'hypermodel.batch_size   {hypermodel.batch_size}')
    print('')

    # Create and save ONNX model with specified batch and timestep sizes
    onnx_name = base_name + '.onnx'
    try:
        create_onnx_from_keras(keras_model=built_model,
                               is_flattened=hypermodel.flatten,
                               has_timestep=(hypermodel.timesteps > 0),
                               has_channel=hypermodel.add1ch,
                               is_mutex=hypermodel.truth_mutex,
                               feature=feature,
                               filename=onnx_name)
    except Exception as e:
        logger.warning(f'Failed to create ONNX model, no file saved: {e}.')
    logger.info(f'Wrote ONNX model to {onnx_name}')

    # Create and save onnx model with timesteps, batch = 1
    timesteps = hypermodel.timesteps
    if timesteps > 0:
        # only set to 1 if nonzero (exists)
        timesteps = 1
    hypermodel = model.MyHyperModel(feature=feature,
                                    num_classes=num_classes,
                                    timesteps=timesteps,
                                    batch_size=1)
    built_model = hypermodel.build_model(kt.HyperParameters())
    # load weights from previously saved HDF5
    built_model.load_weights(weight_name)
    # save a prediction version of model to base_name-pred-onnx
    onnx_name = base_name + '-b1.onnx'
    create_onnx_from_keras(keras_model=built_model,
                           is_flattened=hypermodel.flatten,
                           has_timestep=(hypermodel.timesteps > 0),
                           has_channel=hypermodel.add1ch,
                           is_mutex=hypermodel.truth_mutex,
                           feature=feature,
                           filename=onnx_name)
    logger.info(f'Wrote inference ONNX model to {onnx_name}')


def check_keras_overrides(model: Any, feature: str, num_classes: int, timesteps: int, batch_size: int) -> int:
    try:
        hypermodel = model.MyHyperModel()
    except Exception as e:
        logger.exception(f'Error: build_model() failed: {e}.')
        raise SystemExit(1)

    if hypermodel.feature != feature:
        logger.warning(f'Overriding feature: default = {hypermodel.feature}; specified = {feature}.')

    if hypermodel.num_classes != num_classes:
        logger.warning(
            f'Overriding num_classes: default = {hypermodel.num_classes}; specified = {num_classes}.')

    if timesteps is not None:
        if hypermodel.timesteps == 0 and timesteps != 0:
            logger.warning(f'Model does not contain timesteps; ignoring override.')
            timesteps = 0

        if hypermodel.timesteps != 0 and timesteps == 0:
            logger.warning(f'Model contains timesteps; ignoring override.')
            timesteps = hypermodel.timesteps

        if hypermodel.timesteps != timesteps:
            logger.info(f'Overriding timesteps: default = {hypermodel.timesteps}; specified = {timesteps}.')

    if batch_size is not None and hypermodel.batch_size != batch_size:
        logger.info(f'Overriding batch_size: default = {hypermodel.batch_size}; specified = {batch_size}.')

    return timesteps


def import_keras_model(name: str) -> Any:
    import os
    import sys
    from importlib import import_module

    from sonusai import SonusAIError

    try:
        path = os.path.dirname(name)
        if len(path) < 1:
            path = './'

        # Add model file location to system path
        sys.path.append(os.path.abspath(path))

        try:
            # expect at least a Keras-tuner build_model(hp) function
            root = os.path.splitext(os.path.basename(name))[0]
            model = import_module(root)
        except Exception as e:
            raise SonusAIError(f'Error: could not import model from {name}: {e}.')
    except Exception as e:
        raise SonusAIError(f'Error: could not find {name}: {e}.')

    return model


def create_onnx_from_keras(keras_model,
                           is_flattened: bool = True,
                           has_timestep: bool = True,
                           has_channel: bool = False,
                           is_mutex: bool = True,
                           feature: str = '',
                           filename: str = ''):
    import tf2onnx
    from keras import backend as kb

    from sonusai.utils import add_sonusai_metadata
    from sonusai.utils import replace_stateful_grus

    kb.clear_session()
    onnx_model, _ = tf2onnx.convert.from_keras(keras_model)
    onnx_model = replace_stateful_grus(keras_model=keras_model, onnx_model=onnx_model)
    onnx_model = add_sonusai_metadata(model=onnx_model,
                                      is_flattened=is_flattened,
                                      has_timestep=has_timestep,
                                      has_channel=has_channel,
                                      is_mutex=is_mutex,
                                      feature=feature)
    if filename:
        import onnx
        onnx.save(onnx_model, filename)
    return onnx_model
