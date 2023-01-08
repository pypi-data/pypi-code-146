from enum import Enum
from uuid import UUID

from serenity_types.refdata.asset import Asset


class TokenAsset(Asset):
    """
    A tokenized asset.
    """

    token_issuance_id: UUID
    """
    A reference to the Exposure UUID for the underlying token issuance. This is to
    allow for the fact that a number of tokens have been issued on more than one
    blockchain, e.g. DAI on Ethereum and Solana in our model would be two different
    assets, tok.dai.ethereum and tok.dai.solana, both pointing to a single DAI
    exposure linked to MakerDAO.
    """

    network_id: UUID
    """
    The blockchain on which this particular asset has been tokenized.
    """


class PegMechanism(Enum):
    """
    The mechanism used to establish and maintain the peg of one asset's price ot another.
    """

    TOKENIZED_CASH = 'TOKENIZED_CASH'
    """
    Pegging to a currency reserve-backed holding, e.g. USDC and BUSD.
    """

    TOKENIZED_ASSET = 'TOKENIZED_ASSET'
    """
    Pegging to an asset reserve-backed holding, e.g. PAXG.
    """

    ALGOSTABLE = 'ALGOSTABLE'
    """
    Pegging via an algorithmic stabilization mechanism, e.g. FRAX.
    """

    COLLATERIZED_DEBT_POSITION = 'COLLATERIZED_DEBT_POSITION'
    """
    A tokenized CDP (Collateralized Debt Position), generally over-collateralized
    with cryptoassets, e.g. DAI.
    """


class PeggedTokenAsset(TokenAsset):
    """
    A token whose price aims to track the price of an Exposure.
    """

    referenced_exposure_id: UUID
    """
    The exposure that is being pegged to, e.g. USD (for USDC) XAU (for PAXG).
    """

    peg_mechanism: PegMechanism
    """
    How the peg is established and maintained, e.g. backed 100% by reserves
    of assets with an identical exposure as referenced_exposure_id, or algorithmically
    stabilized via an arbitrage mechanism, etc..
    """


class WrappedTokenAsset(TokenAsset):
    """
    A token that allows another token Exposure to be represented on a non-native
    network. Typically this is done by locking the asset in a smart contract or
    by a custodian holding the asset in reserve and then issuing a token. At any
    time the holder has a right to redeem the wrapped asset for the underlying
    asset one for one, though there is implicit smart contract / counterparty
    risk involved as this is not guaranteed.
    """

    wrapped_token_issuance_id: UUID
    """
    The token issuance that this asset is wrapping, e.g. BTC for WBTC.
    """

    origin_network_id: UUID
    """
    The original network that the wrapped asset sits on, e.g. bitcoin for WBTC,
    or ethereum or WETH. Note in the case of WETH on Ethereum as an asset, the
    origin_network_id and network_id are the same, because it's just an ERC20
    encapsulation of the native ETH token.
    """
