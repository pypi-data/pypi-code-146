"""sonusai predict

usage: predict [-hvr] [-i MIXID] (-m MODEL) INPUT

options:
    -h, --help
    -v, --verbose               Be verbose.
    -i MIXID, --mixid MIXID     Mixture ID(s) to generate if input is a mixture database. [default: *].
    -m MODEL, --model MODEL     Trained ONNX model file.
    -r, --reset                 Reset model between each file.

Run prediction on a trained ONNX model using SonusAI genft or WAV data.

Inputs:
    MODEL       A SonusAI trained ONNX model file.
    INPUT       The input data must be one of the following:
                * WAV
                  Using the given model, generate feature data and run prediction. A model file must be
                  provided. The MIXID is ignored.

                * directory
                  Using the given SonusAI mixture database directory, generate feature and truth data if not found.
                  Run prediction. The MIXID is required.

Outputs the following to opredict-<TIMESTAMP> directory:
    <id>.h5
        dataset:    predict
    onnx_predict.log

"""
from sonusai import logger
from sonusai.mixture import Feature
from sonusai.mixture import Predict
from sonusai.utils import SonusAIMetaData


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixids = args['--mixid']
    model_name = args['--model']
    reset = args['--reset']
    input_name = args['INPUT']

    from os import makedirs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    import h5py
    import onnxruntime as rt
    import numpy as np

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import get_feature_from_audio
    from sonusai.mixture import read_audio
    from sonusai.utils import create_ts_name
    from sonusai.utils import get_frames_per_batch
    from sonusai.utils import get_sonusai_metadata

    output_dir = create_ts_name('opredict')
    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    create_file_handler(join(output_dir, 'onnx_predict.log'))
    update_console_handler(verbose)
    initial_log_messages('onnx_predict')

    model = rt.InferenceSession(model_name, providers=['CPUExecutionProvider'])
    model_metadata = get_sonusai_metadata(model)

    batch_size = model_metadata.input_shape[0]
    if model_metadata.timestep:
        timesteps = model_metadata.input_shape[1]
    else:
        timesteps = 0
    num_classes = model_metadata.output_shape[-1]

    frames_per_batch = get_frames_per_batch(batch_size, timesteps)

    logger.info('')
    logger.info(f'feature       {model_metadata.feature}')
    logger.info(f'num_classes   {num_classes}')
    logger.info(f'batch_size    {batch_size}')
    logger.info(f'timesteps     {timesteps}')
    logger.info(f'flatten       {model_metadata.flattened}')
    logger.info(f'add1ch        {model_metadata.channel}')
    logger.info(f'truth_mutex   {model_metadata.mutex}')
    logger.info(f'input_shape   {model_metadata.input_shape}')
    logger.info(f'output_shape  {model_metadata.output_shape}')
    logger.info('')

    if splitext(input_name)[1] == '.wav':
        # Convert WAV to feature data
        logger.info('')
        logger.info(f'Run prediction on {input_name}')
        audio = read_audio(input_name)
        feature = get_feature_from_audio(audio=audio, feature=model_metadata.feature)

        predict = pad_and_predict(feature=feature,
                                  model_name=model_name,
                                  model_metadata=model_metadata,
                                  frames_per_batch=frames_per_batch,
                                  batch_size=batch_size,
                                  timesteps=timesteps,
                                  reset=reset)

        output_name = splitext(input_name)[0] + '.h5'
        with h5py.File(output_name, 'a') as f:
            if 'feature' in f:
                del f['feature']
            f.create_dataset(name='feature', data=feature)

            if 'predict' in f:
                del f['predict']
            f.create_dataset(name='predict', data=predict)

        logger.info(f'Saved results to {output_name}')
        return

    if not isdir(input_name):
        logger.exception(f'Do not know how to process input from {input_name}')
        raise SystemExit(1)

    mixdb = MixtureDatabase(config=input_name, show_progress=True)

    if mixdb.feature != model_metadata.feature:
        logger.exception(f'Feature in mixture database does not match feature in model')
        raise SystemExit(1)

    mixids = mixdb.mixids_to_list(mixids)
    if reset:
        # reset mode cycles through each file one at a time
        for mixid in mixids:
            feature, _ = mixdb.mixture_ft(mixid)

            predict = pad_and_predict(feature=feature,
                                      model_name=model_name,
                                      model_metadata=model_metadata,
                                      frames_per_batch=frames_per_batch,
                                      batch_size=batch_size,
                                      timesteps=timesteps,
                                      reset=reset)

            output_name = join(output_dir, mixdb.mixtures[mixid].name)
            with h5py.File(output_name, 'a') as f:
                if 'predict' in f:
                    del f['predict']
                f.create_dataset(name='predict', data=predict)
    else:
        feature = []
        file_indices = []
        total_frames = 0
        for mixid in mixids:
            current_feature, _ = mixdb.mixture_ft(mixid)
            current_frames = current_feature.shape[0]
            feature.append(current_feature)
            file_indices.append(slice(total_frames, total_frames + current_frames))
            total_frames += current_frames
        feature = np.vstack([feature[i] for i in range(len(feature))])

        predict = pad_and_predict(feature=feature,
                                  model_name=model_name,
                                  model_metadata=model_metadata,
                                  frames_per_batch=frames_per_batch,
                                  batch_size=batch_size,
                                  timesteps=timesteps,
                                  reset=reset)

        # Write data to separate files
        for idx, mixid in enumerate(mixids):
            output_name = join(output_dir, mixdb.mixtures[mixid].name)
            with h5py.File(output_name, 'a') as f:
                if 'predict' in f:
                    del f['predict']
                f.create_dataset('predict', data=predict[file_indices[idx]])

    logger.info(f'Saved results to {output_dir}')


def pad_and_predict(feature: Feature,
                    model_name: str,
                    model_metadata: SonusAIMetaData,
                    frames_per_batch: int,
                    batch_size: int,
                    timesteps: int,
                    reset: bool) -> Predict:
    import onnxruntime as rt
    import numpy as np

    from sonusai.utils import reshape_inputs
    from sonusai.utils import reshape_outputs

    frames = feature.shape[0]
    padding = frames_per_batch - frames % frames_per_batch
    feature = np.pad(array=feature, pad_width=((0, padding), (0, 0), (0, 0)))
    feature, _ = reshape_inputs(feature=feature,
                                batch_size=batch_size,
                                timesteps=timesteps,
                                flatten=model_metadata.flattened,
                                add1ch=model_metadata.channel)
    sequences = feature.shape[0] // model_metadata.input_shape[0]
    feature = np.reshape(feature, [sequences, *model_metadata.input_shape])

    model = rt.InferenceSession(model_name, providers=['CPUExecutionProvider'])
    output_names = [n.name for n in model.get_outputs()]
    input_names = [n.name for n in model.get_inputs()]

    predict = []
    for sequence in range(sequences):
        predict.append(model.run(output_names, {input_names[0]: feature[sequence]}))
        if reset:
            model = rt.InferenceSession(model_name, providers=['CPUExecutionProvider'])

    predict = np.vstack(predict)
    predict, _ = reshape_outputs(predict=predict, timesteps=timesteps)
    predict = predict[:frames, :]

    return predict


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
