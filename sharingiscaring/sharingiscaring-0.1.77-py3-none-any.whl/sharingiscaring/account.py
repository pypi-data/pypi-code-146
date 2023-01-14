from pydantic import BaseModel, Extra
from sharingiscaring.pool import PoolInfo, APY, CommissionRates
from sharingiscaring.node import ConcordiumNodeFromDashboard
from sharingiscaring.credential import Identity

microCCD = int

class AccountBakerPool(BaseModel):
    delegatorCount: int
    delegatedStake: int
    totalStake: int
    apy_30: APY
    apy_7: APY

class AccountBakerState(BaseModel):
    pool: AccountBakerPool = None

class AccountBakerFromCCDScan(BaseModel):
    state: AccountBakerState
    
class AccountBaker(BaseModel):
    bakerAggregationVerifyKey: str
    bakerElectionVerifyKey: str
    bakerId: int
    bakerPoolInfo: PoolInfo
    bakerSignatureVerifyKey: str
    restakeEarnings: bool
    stakedAmount: microCCD
    
class AccountReleaseScheduleNodes(BaseModel):
    nodes: list

class AccountReleaseScheduleFromCCDScan(BaseModel):
    schedule: AccountReleaseScheduleNodes
    totalAmount: int
class AccountReleaseSchedule(BaseModel):
    schedule: list
    total: str
    
    
class DelegationTarget(BaseModel, extra=Extra.ignore):
    bakerId: int = None
    delegateType: str = None
    
class AccountDelegation(BaseModel):
    delegationTarget: DelegationTarget
    delegatorId: int = None
    restakeEarnings: bool
    stakedAmount: int

class BakerStakePendingChange(BaseModel):
    bakerEquityCapital: int = None
    effectiveTime: str = None
    pendingChangeType: str

class CurrentPaydayStatus(BaseModel):
    bakerEquityCapital: int
    blocksBaked: int
    delegatedCapital: int
    effectiveStake: int
    finalizationLive: bool
    lotteryPower: float
    transactionFeesEarned: int
    
class AccountBakerPoolStatus(BaseModel):
    allPoolTotalCapital: int
    bakerAddress: str = None
    bakerEquityCapital: int = None
    bakerId: int = None
    bakerStakePendingChange: BakerStakePendingChange = None
    currentPaydayDelegatedCapital: int = None
    currentPaydayTransactionFeesEarned: int = None
    currentPaydayStatus: CurrentPaydayStatus = None
    delegatedCapital: int
    delegatedCapitalCap: int = None
    poolInfo: PoolInfo = None
    commissionRates: CommissionRates = None
    poolType: str

class ConcordiumAccountFromClient(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = Extra.ignore

    accountAddress: str
    accountAmount: int
    accountBaker: AccountBaker = None
    accountBakerPoolStatus: AccountBakerPoolStatus = None
    accountBakerPaydayExpectation: float = None
    accountDelegation: AccountDelegation = None
    accountEncryptionKey: str
    accountIndex: int
    accountNonce: int
    accountReleaseSchedule: AccountReleaseSchedule
    accountThreshold: int
    accountNode: ConcordiumNodeFromDashboard = None
    accountIdentity: Identity = None

# class ConcordiumBakerFromClient(ConcordiumAccountFromClient, extra=Extra.ignore):
#     accountBaker: AccountBaker

class Address(BaseModel):
    asString: str
class ConcordiumAccountFromCCDScan(BaseModel):
    createdAt: str
    id: str
    transactionCount: int
    amount: int
    address: Address
    delegation: AccountDelegation = None
    baker: AccountBakerFromCCDScan = None
    releaseSchedule: AccountReleaseScheduleFromCCDScan

class RewardAmount(BaseModel):
    sumRewardAmount: int

class ConcordiumAccountRewards(BaseModel):
    LAST24_HOURS: RewardAmount
    LAST7_DAYS: RewardAmount
    LAST30_DAYS: RewardAmount

class ConcordiumAccount(BaseModel):
    via_client:     ConcordiumAccountFromClient    = None
    via_ccdscan:    ConcordiumAccountFromCCDScan   = None
    rewards:        ConcordiumAccountRewards       = None
# TODO: config extra ignore