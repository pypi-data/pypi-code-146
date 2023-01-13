import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)


if True:
    from alphafed import logger
    from alphafed.examples.hetero_nn import COLLABORATER_4_ID
    from alphafed.examples.hetero_nn.psi.demos import get_ids, get_task_id
    from alphafed.hetero_nn.psi import RSAPSICollaboratorScheduler


ids = get_ids()
logger.info(f'local ids: {ids}')
initiator_scheduler = RSAPSICollaboratorScheduler(task_id=get_task_id(),
                                                  collaborator_id=COLLABORATER_4_ID,
                                                  ids=ids)
intersection = initiator_scheduler.collaborate_intersection()
logger.info(f'intersection ids: {intersection}')
