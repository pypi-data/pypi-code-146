import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)


if True:
    from alphafed import logger
    from alphafed.examples.hetero_nn import COLLABORATER_2_ID, HOST_ID
    # from alphafed.examples.hetero_nn import (COLLABORATER_3_ID,
    #                                          COLLABORATER_4_ID,
    #                                          COLLABORATER_5_ID, HOST_ID)
    from alphafed.examples.hetero_nn.psi.demos import get_ids, get_task_id
    from alphafed.hetero_nn.psi import RSAPSIInitiatorScheduler


ids = get_ids()
logger.info(f'local ids: {ids}')
initiator_scheduler = RSAPSIInitiatorScheduler(
    task_id=get_task_id(),
    initiator_id=HOST_ID,
    ids=ids,
    collaborator_ids=[COLLABORATER_2_ID]
    # collaborator_ids=[COLLABORATER_3_ID, COLLABORATER_4_ID, COLLABORATER_5_ID]
)
intersection = initiator_scheduler.make_intersection()
logger.info(f'intersection ids: {intersection}')
