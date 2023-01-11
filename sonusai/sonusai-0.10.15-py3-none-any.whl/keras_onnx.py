"""sonusai keras_onnx

usage: keras_onnx [-hvr] (-m MODEL) (-w WEIGHTS) [-b BATCH] [-t TSTEPS] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -m MODEL, --model MODEL         Python model file.
    -w WEIGHTS, --weights WEIGHTS   Keras model weights file.
    -b BATCH, --batch BATCH         Batch size.
    -t TSTEPS, --tsteps TSTEPS      Timesteps.
    -o OUTPUT, --output OUTPUT      Output directory.

Convert a trained Keras model to ONNX.

Inputs:
    MODEL       A SonusAI Python model file with build and/or hypermodel functions.
    WEIGHTS     A Keras model weights file (or model file with weights).

Outputs:
    OUTPUT/     A directory containing:
                    <MODEL>.onnx        Model file with batch_size and timesteps equal to provided parameters
                    <MODEL>-b1.onnx     Model file with batch_size=1 and if the timesteps dimension exists it
                                        is set to 1 (useful for real-time inference applications)
                    keras_onnx.log

Results are written into subdirectory <MODEL>-<TIMESTAMP> unless OUTPUT is specified.

"""
from sonusai import logger


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    model_name = args['--model']
    weight_name = args['--weights']
    batch_size = args['--batch']
    timesteps = args['--tsteps']
    output_dir = args['--output']

    from os import makedirs
    from os.path import basename
    from os.path import join
    from os.path import splitext

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.utils import create_ts_name
    from sonusai.utils import keras_onnx

    model_tail = basename(model_name)
    model_root = splitext(model_tail)[0]

    if batch_size is not None:
        batch_size = int(batch_size)

    if timesteps is not None:
        timesteps = int(timesteps)

    if output_dir is None:
        output_dir = create_ts_name(model_root)

    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    create_file_handler(join(output_dir, 'keras_onnx.log'))
    update_console_handler(verbose)
    initial_log_messages('keras_onnx')

    keras_onnx(model_name, weight_name, timesteps, batch_size, output_dir)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
