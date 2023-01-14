import pytest
from pathlib import Path
import json
from unittest.mock import Mock
from sharingiscaring.transaction import Transaction
from sharingiscaring.client import ConcordiumClient
from sharingiscaring.tooter import Tooter
from sharingiscaring.cns import CNSActions
from sharingiscaring.user import User, SubscriptionPlans
from sharingiscaring.pool import ConcordiumPool, ConcordiumPoolFromClient
import datetime as dt
from datetime import timezone
# @pytest.fixture
# def tooter():
#     return Tooter('','','','','')


@pytest.fixture
def node():
    return ConcordiumClient(Tooter('','','','',''))

def read_pool_information(pool_id):
    p = Path('tests')
    
    with open(p / 'pools' / f'{pool_id}' / 'GetPoolStatus', 'r') as f:   
            return json.load(f)
    
def test_pool_1(node: ConcordiumClient):
    pool = ConcordiumPoolFromClient(**read_pool_information(72723))
    assert pool.bakerId == 72723
    assert pool.poolInfo.commissionRates.finalizationCommission == 1.0
    assert pool.delegatedCapital == "584273078883"
    assert pool.poolInfo.metadataUrl == "https://concordium-explorer.nl"

# def test_poolstatus_0(node: ConcordiumClient):
#     getPoolStatus = ConcordiumPoolFromClient(**node.request_pool_status('72724'))
#     assert getPoolStatus == None

def test_poolstatus_1(node: ConcordiumClient):
    getPoolStatus = ConcordiumPoolFromClient(**node.request_pool_status('72723'))
    assert getPoolStatus.bakerId == 72723
