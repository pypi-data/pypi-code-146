from pydantic import BaseModel

# do not try to add a link back to the baker/account here
# tried this and it fails (recursion, circular imports, etc).
class ConcordiumNodeFromDashboard(BaseModel):
    nodeName: str
    nodeId: str
    peerType: str
    uptime: int
    client: str
    averagePing: float = None
    peersCount: int
    peersList: list
    bestBlock: str
    bestBlockHeight: int
    bestBlockBakerId: int
    bestArrivedTime: str = None
    blockArrivePeriodEMA: float = None
    blockArrivePeriodEMSD: float = None
    blockArriveLatencyEMA: float
    blockArriveLatencyEMSD: float
    blockReceivePeriodEMA: float = None
    blockReceivePeriodEMSD: float = None
    blockReceiveLatencyEMA: float
    blockReceiveLatencyEMSD: float
    finalizedBlock: str
    finalizedBlockHeight: int
    finalizedTime: str = None
    finalizationPeriodEMA: float = None
    finalizationPeriodEMSD: float = None
    packetsSent: int
    packetsReceived: int
    consensusRunning: bool
    bakingCommitteeMember: str
    consensusBakerId: int = None
    finalizationCommitteeMember: bool
    transactionsPerBlockEMA: float
    transactionsPerBlockEMSD: float
    bestBlockTransactionsSize: int
    bestBlockTotalEncryptedAmount: str = None
    bestBlockTotalAmount: str = None
    bestBlockTransactionCount: int = None
    bestBlockTransactionEnergyCost: int = None
    bestBlockExecutionCost: float = None
    bestBlockCentralBankAmount: str = None
    blocksReceivedCount: int
    blocksVerifiedCount: int
    genesisBlock: str
    finalizationCount: int
    finalizedBlockParent: str
    averageBytesPerSecondIn: int
    averageBytesPerSecondOut: int
  