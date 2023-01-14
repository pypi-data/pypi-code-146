import pytest
from pathlib import Path
import json
from unittest.mock import Mock
from sharingiscaring.transaction import Transaction
from sharingiscaring.client import ConcordiumClient
from sharingiscaring.tooter import Tooter
from sharingiscaring.cns import CNSActions
from sharingiscaring.user import User, SubscriptionPlans
import datetime as dt
from datetime import timezone
# @pytest.fixture
# def tooter():
#     return Tooter('','','','','')


@pytest.fixture
def node():
    return ConcordiumClient(Tooter('','','','',''))

def read_block_information(blockHeight):
    p = Path('tests')
    
    with open(p / 'blocks' / f'{blockHeight}' / 'blockInfo', 'r') as f:   
            blockInfo = json.load(f)
    with open(p / 'blocks' / f'{blockHeight}' / 'blockSummary', 'r') as f:    
            blockSummary = json.load(f)
    
    block = {'blockInfo': blockInfo, 'blockSummary': blockSummary}
    return block

def get_tx_at_index(node, blockHeight, index):
    block = read_block_information (blockHeight)
    if 'transactionSummaries' in block['blockSummary']:
        tx_by_index = {x['index']: x for x in  block['blockSummary']['transactionSummaries']}
        tx_at_index = tx_by_index[index]
        tx_at_index.update({'blockInfo': block['blockInfo']})
        return Transaction(node).init_from_node(tx_at_index)
    else:
        return None

def test_user_1(node: ConcordiumClient):
    user = User()
    user.perform_subscription_logic(node)
    
    assert user.subscription.site_active == False
    assert user.subscription.bot_active == False

def test_user_1(node: ConcordiumClient):
    user = User()
    user.explorer_ccd_transactions  = []
    user.explorer_ccd_delegators    = []
    user.perform_subscription_logic()
    user.subscription.count_messages = 0
    
    user.determine_bot_status()
    # user.set_count_messages = 100
    # user.perform_subscription_logic(node)
    
    assert user.subscription.site_active == False
    assert user.subscription.bot_active == False

def test_user_unlimited_1_tx(node: ConcordiumClient):
    user = User()
    user.token = '90dd67'
    tx = Transaction(node)
    tx.memo = '90dd67'
    tx.sender = 'bla'
    tx.amount = 5_000_000_000
    tx.block['blockSlotTime'] = dt.datetime(2022,12,2,0,0,0).astimezone(timezone.utc)
    user.explorer_ccd_transactions  = [tx]
    user.explorer_ccd_delegators    = {}
    user.perform_subscription_logic()
    user.subscription.count_messages = 0
    user.determine_bot_status()
    
    assert user.subscription.site_active == True
    assert user.subscription.bot_active == True
    assert user.subscription.plan == SubscriptionPlans.UNLIMITED
    assert user.subscription.start_date == tx.block['blockSlotTime']

def test_user_plus_1_tx(node: ConcordiumClient):
    user = User()
    user.token = '90dd67'
    tx = Transaction(node)
    tx.memo = '90dd67'
    tx.sender = 'bla'
    tx.amount = 1_000_000_000
    tx.block['blockSlotTime'] = dt.datetime(2022,12,2,0,0,0).astimezone(timezone.utc)
    user.explorer_ccd_transactions  = [tx]
    user.explorer_ccd_delegators    = {}
    user.perform_subscription_logic()
    user.subscription.count_messages = 0
    user.determine_bot_status()
    
    assert user.subscription.site_active == True
    assert user.subscription.bot_active == True
    assert user.subscription.plan == SubscriptionPlans.PLUS
    assert user.subscription.remaining_message_credits == 50
    assert user.subscription.start_date == tx.block['blockSlotTime']


def test_user_delegation(node: ConcordiumClient):
    user = User()
    user.token = '90dd67'
    tx = Transaction(node)
    tx.memo = '90dd67'
    tx.sender = '4sRifhDV6yCQmzze4oAUJRJEs9X98scxdhtCwJjtSFp5hiQwVu'
    tx.amount = 1_000_000
    tx.block['blockSlotTime'] = dt.datetime(2022,12,2,0,0,0).astimezone(timezone.utc)
    user.explorer_ccd_transactions  = [tx]
    delegator = {
        'stakedAmount': 123_456_789_098,

    }
    user.explorer_ccd_delegators    = {'4sRifhDV6yCQmzze4oAUJRJEs9X98scxdhtCwJjtSFp5hiQwVu': delegator}
    user.perform_subscription_logic()
    user.subscription.count_messages = 0
    user.determine_bot_status()
    
    assert user.subscription.site_active == True
    assert user.subscription.bot_active == True
    assert user.subscription.remaining_message_credits == 50
    assert user.subscription.plan == SubscriptionPlans.DELEGATION
    assert user.subscription.start_date == tx.block['blockSlotTime']