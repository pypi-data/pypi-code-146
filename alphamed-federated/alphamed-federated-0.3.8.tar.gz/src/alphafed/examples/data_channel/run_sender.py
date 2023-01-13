import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)

if True:
    from alphafed import logger
    from alphafed.contractor import TaskMessageContractor
    from alphafed.data_channel import GRPCDataChannel, SharedFileDataChannel
    from alphafed.examples.data_channel import (DEV_TASK_ID, RECEIVER_2_ID,
                                                RECEIVER_4_ID, SENDER_ID)


contractor = TaskMessageContractor(task_id=DEV_TASK_ID)
data_channel = GRPCDataChannel(contractor=contractor)
# The original ports are occupied by alphamed-federated-service
data_channel._ports = [i for i in range(21000, 21010)]

original_msg = 'Hello, 世界！'
data_stream = original_msg.encode('utf-8')
logger.info(f'The original message are: {original_msg} .')

targets = [RECEIVER_2_ID, RECEIVER_4_ID]
for _target in targets:
    data_channel.send_stream(source=SENDER_ID, target=_target, data_stream=data_stream)
logger.info('Sending by GRPC channel complete.')

data_channel = SharedFileDataChannel(contractor=contractor)
accepted = data_channel.send_stream(source=SENDER_ID,
                                    target=targets,
                                    data_stream=data_stream)
if len(accepted) == len(targets):
    logger.info('Sending by shared file channel complete.')
else:
    logger.info('Sending by shared file channel failed.')
    logger.info(f'Accepting list: {accepted} .')
