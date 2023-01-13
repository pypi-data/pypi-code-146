import argparse
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)

if True:
    from alphafed import logger
    from alphafed.examples.fed_avg import DATA_OWNER_2_ID
    from alphafed.examples.fed_avg.demos import (DP, FED_IRM, SECURE, SGD,
                                                 VANILLA, get_scheduler,
                                                 get_task_id)

parser = argparse.ArgumentParser(description='Run data owner 2 demo.')
parser.add_argument('-m', '--mode',
                    type=str,
                    default=VANILLA,
                    help=f'running mode: {VANILLA}(default) | {SGD} | {DP} | {SECURE} | {FED_IRM}')
args = parser.parse_args()

task_id = get_task_id()
scheduler = get_scheduler(mode=args.mode)
logger.debug(f'{type(scheduler)=}')
logger.info(f'run data owner 2 in {args.mode} mode: {task_id=}')
scheduler._run(id=DATA_OWNER_2_ID, task_id=task_id)
