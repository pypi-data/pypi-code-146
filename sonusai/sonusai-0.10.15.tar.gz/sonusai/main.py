"""sonusai

usage: sonusai [--version] [--help] <command> [<args>...]

The sonusai commands are:
   calc_metric_spenh_targetf    Run speech enhancement and analysis for targetf truth
   evaluate                     Evaluate model performance
   genft                        Generate feature and truth data
   genmix                       Generate mixture and truth data
   genmixdb                     Generate a mixture database
   gentcst                      Generate target configuration from a subdirectory tree
   keras_predict                Run Keras predict on a trained model
   keras_train                  Train a model using Keras
   keras_onnx                   Convert a trained Keras model to ONNX
   lsdb                         List information about a mixture database
   mkwav                        Make WAV files from a mixture database
   onnx_predict                 Run ONNX predict on a trained model
   plot                         Plot mixture data
   post_spenh_targetf           Run post-processing for speech enhancement targetf data
   tplot                        Plot truth data
   vars                         List custom SonusAI variables

Aaware Sound and Voice Machine Learning Framework. See 'sonusai help <command>'
for more information on a specific command.

"""

from sonusai import logger


def main():
    from subprocess import call

    from docopt import docopt

    import sonusai
    from sonusai import SonusAIError
    from sonusai.utils import trim_docstring

    commands = (
        'calc_metric_spenh_targetf',
        'evaluate',
        'genft',
        'genmix',
        'genmixdb',
        'gentcst',
        'keras_predict',
        'keras_train',
        'keras_onnx',
        'lsdb',
        'mkwav',
        'onnx_predict',
        'plot',
        'post_spenh_targetf',
        'tplot',
        'vars',
    )

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    command = args['<command>']
    argv = args['<args>']

    if command == 'help':
        if not argv:
            exit(call(['sonusai', '-h']))
        elif argv[0] in commands:
            exit(call(['python', f'{sonusai.BASEDIR}/{argv[0]}.py', '-h']))
        else:
            raise SonusAIError(f"{argv[0]} is not a SonusAI command. See 'sonusai help'.")
    elif command in commands:
        exit(call(['python', f'{sonusai.BASEDIR}/{command}.py'] + argv))

    raise SonusAIError(f"{command} is not a SonusAI command. See 'sonusai help'.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
