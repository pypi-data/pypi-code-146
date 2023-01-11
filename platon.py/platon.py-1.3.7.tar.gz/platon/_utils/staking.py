from typing import (
    Union,
)

from platon_typing import (
    NodeID,
    URI,
    BLSPubkey,
    BLSSignature,
    HexStr,
    Decodable,
)
from platon_typing.evm import (
    Bech32Address,
)
from platon.types import (
    InnerFn,
)
from platon.types import (
    Von,
    Version,
)
from platon._utils.inner_contract import (
    InnerContract,
    bubble_dict,
)


class Staking(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000002'

    def create_staking(self,
                       balance_type: int,
                       benefit_address: Bech32Address,
                       node_id: Union[NodeID, HexStr],
                       external_id: str,
                       node_name: str,
                       website: URI,
                       details: str,
                       amount: Von,
                       reward_per: int,
                       node_version: Version,
                       version_sign: Union[Decodable, HexStr],
                       bls_pubkey: Union[BLSPubkey, HexStr],
                       bls_proof: Union[BLSSignature, HexStr],
                       ):
        """
        Staking a node to be candidate.

        :param balance_type: staking balance type, including: 0: free balance, 1: restricting, 2: all and restricting first
        :param benefit_address: the address that accepts the staking reward
        :param node_id: id of the node to staking
        :param external_id: custom external id, will be attached to the staking information
        :param node_name: custom node name, will be attached to the staking information
        :param website: custom node website, will be attached to the staking information
        :param details: custom node detail, will be attached to the staking information
        :param amount: staking amount
        :param reward_per: the proportion of the staking reward allocated to the delegate, 1 BasePoint = 0.01%
        :param node_version: node version, obtained by rpc 'admin_getProgramVersion' interface
        :param version_sign: node version signature, obtained by rpc 'admin_getProgramVersion' interface
        :param bls_pubkey: node bls public key, obtained by rpc 'admin_nodeInfo' interface
        :param bls_proof: node bls Proof, obtained by rpc 'admin_getSchnorrNIZKProve' interface
        """
        return self.function_processor(InnerFn.staking_createStaking, locals())

    def edit_staking(self,
                     node_id: Union[NodeID, HexStr],
                     benefit_address: Bech32Address = None,
                     reward_per: int = None,
                     external_id: str = None,
                     node_name: str = None,
                     website: str = None,
                     details: str = None,
                     ):
        """
        edit staking information.

        :param node_id: id of node that has been staking
        :param benefit_address: the address that accepts the staking reward
        :param external_id: custom external id, will be attached to the staking information
        :param node_name: custom node name, will be attached to the staking information
        :param website: custom node website, will be attached to the staking information
        :param details: custom node detail, will be attached to the staking information
        :param reward_per: the proportion of the staking reward allocated to the delegate, 1 BasePoint = 0.01%
        """
        kwargs = bubble_dict(dict(locals()), 'benefit_address')
        return self.function_processor(InnerFn.staking_editStaking, kwargs)

    def increase_staking(self,
                         node_id: Union[NodeID, HexStr],
                         balance_type: int,
                         amount: Von,
                         ):
        """
        Increase the amount of staking.

        :param balance_type: balance type of increase staking, including: 0: free balance, 1: restricting
        :param node_id: id of node that has been staking
        :param amount: increase staking amount
        """
        return self.function_processor(InnerFn.staking_increaseStaking, locals())

    def withdrew_staking(self, node_id: Union[NodeID, HexStr]):
        """
        Revoke the staking of the node and withdraw the staking amount.

        :param node_id: id of the node to be withdrew staking
        """
        return self.function_processor(InnerFn.staking_withdrewStaking, locals())

    def get_candidate_list(self):
        """
        Gets all staking node information.
        """
        return self.function_processor(InnerFn.staking_getCandidateList, locals(), is_call=True)

    def get_verifier_list(self):
        """
        Get all verifier node information.
        """
        return self.function_processor(InnerFn.staking_getVerifierList, locals(), is_call=True)

    def get_validator_list(self):
        """
        get information about the current consensus verifier node.
        """
        return self.function_processor(InnerFn.staking_getValidatorList, locals(), is_call=True)

    def get_candidate_info(self, node_id: Union[NodeID, HexStr]):
        """
        Get staking node information.

        :param node_id: staking node id
        """
        return self.function_processor(InnerFn.staking_getCandidateInfo, locals(), is_call=True)

    def get_block_reward(self):
        """
        get the current block reward, which is updated every epoch.
        """
        return self.function_processor(InnerFn.staking_getBlockReward, locals(), is_call=True)

    def get_staking_reward(self):
        """
        get the current staking reward, which is updated every epoch.
        """
        return self.function_processor(InnerFn.staking_getStakingReward, locals(), is_call=True)

    def get_avg_block_time(self):
        """
        Get the average block time over history.
        """
        return self.function_processor(InnerFn.staking_getAvgBlockTime, locals(), is_call=True)
