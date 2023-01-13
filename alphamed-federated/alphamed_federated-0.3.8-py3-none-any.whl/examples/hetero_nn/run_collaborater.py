import argparse
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)

if True:
    from alphafed import logger
    from alphafed.examples.hetero_nn import COLLABORATER_2_ID
    from alphafed.examples.hetero_nn.demos import (SECURE, VANILLA,
                                                   get_collaborator,
                                                   get_task_id)


parser = argparse.ArgumentParser(description='Run aggregator demo.')
parser.add_argument('-m', '--mode',
                    type=str,
                    default=VANILLA,
                    help=f'running mode: {VANILLA}(default) | {SECURE}')
parser.add_argument('-r', '--recover',
                    type=bool,
                    default=False,
                    help='recover mode: true | false')
args = parser.parse_args()


task_id = get_task_id()
collaborator = get_collaborator(mode=args.mode)
logger.debug(f'{type(collaborator)=}')
logger.info(f'run collaborator on task_id = {task_id}')
logger.debug(f'{args.recover=}')
collaborator._run(id=COLLABORATER_2_ID, task_id=task_id, recover=args.recover)
