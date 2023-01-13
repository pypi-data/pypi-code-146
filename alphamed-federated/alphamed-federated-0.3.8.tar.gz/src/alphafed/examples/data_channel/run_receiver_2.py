import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)

if True:
    from alphafed import logger
    from alphafed.contractor import (ApplyGRPCSendingDataEvent,
                                     ApplySharedFileSendingDataEvent,
                                     TaskMessageContractor)
    from alphafed.data_channel import GRPCDataChannel, SharedFileDataChannel
    from alphafed.examples.data_channel import DEV_TASK_ID, RECEIVER_2_ID


contractor = TaskMessageContractor(task_id=DEV_TASK_ID)
data_channel = GRPCDataChannel(contractor=contractor)
# The original ports are occupied by alphamed-federated-service
data_channel._ports = [i for i in range(21000, 21010)]
for _event in contractor.contract_events():
    if isinstance(_event, ApplyGRPCSendingDataEvent):
        data_stream = data_channel.receive_stream(apply_event=_event)
        original_msg = data_stream.decode('utf-8')
        logger.info(f'Received a message: {original_msg} .')
        break

data_channel = SharedFileDataChannel(contractor=contractor)
for _event in contractor.contract_events():
    if isinstance(_event, ApplySharedFileSendingDataEvent):
        data_stream = data_channel.receive_stream(apply_event=_event, receiver=RECEIVER_2_ID)
        original_msg = data_stream.decode('utf-8')
        logger.info(f'Received a message: {original_msg} .')
        break
