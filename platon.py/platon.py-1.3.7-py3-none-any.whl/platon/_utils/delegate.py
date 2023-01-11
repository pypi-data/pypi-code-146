from typing import (
    Union,
)

from platon_typing import (
    NodeID,
    HexStr,
)
from platon_typing.evm import (
    Bech32Address,
)
from platon_utils import remove_0x_prefix

from platon.types import (
    InnerFn,
    Von,
    BlockIdentifier,
)
from platon._utils.inner_contract import (
    InnerContract,
    bubble_dict,
)


class _DelegatePart(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000002'

    def delegate(self,
                 node_id: Union[NodeID, HexStr],
                 balance_type: int,
                 amount: Von,
                 ):
        """
        Delegate the amount to the node and get the reward from the node.

        :param balance_type: delegate balance type, including: free balance: 0, restricting: 1, locked balance and restricting: 2
        :param node_id: id of the candidate node to delegate
        :param amount: delegate amount
        """
        kwargs = bubble_dict(dict(locals()), 'balance_type')
        return self.function_processor(InnerFn.delegate_delegate, kwargs)

    def withdrew_delegate(self,
                          node_id: Union[NodeID, HexStr],
                          staking_block_identifier: BlockIdentifier,
                          amount: Von,
                          ):
        """
        Withdrew delegates from sending address,
        and when the remaining delegates amount is less than the minimum threshold, all delegates will be withdrawn.

        :param node_id: id of the node to withdrew delegate
        :param staking_block_identifier: the identifier of the staking block when delegate
        :param amount: withdrew amount
        """
        kwargs = bubble_dict(dict(locals()), 'staking_block_identifier')
        block = self.web3.platon.get_block(staking_block_identifier)
        kwargs['staking_block_identifier'] = block['number']
        return self.function_processor(InnerFn.delegate_withdrewDelegate, kwargs)

    def redeem_delegate(self):
        """
        redeem all unlocked delegates.
        """
        return self.function_processor(InnerFn.delegate_redeemDelegate, locals())

    def get_delegate_list(self, address: Bech32Address):
        """
        Get all delegate information of the address.
        """
        return self.function_processor(InnerFn.delegate_getDelegateList, locals(), is_call=True)

    def get_delegate_info(self,
                          address: Bech32Address,
                          node_id: Union[NodeID, HexStr],
                          staking_block_identifier: BlockIdentifier,
                          ):
        """
        Get delegate information of the address.

        :param address: delegate address
        :param node_id: id of the node that has been delegated
        :param staking_block_identifier: the identifier of the staking block when delegate
        """
        kwargs = bubble_dict(dict(locals()), 'staking_block_identifier')
        block = self.web3.platon.get_block(staking_block_identifier)
        kwargs['staking_block_identifier'] = block['number']
        return self.function_processor(InnerFn.delegate_getDelegateInfo, kwargs, is_call=True)

    def get_delegate_lock_info(self, address: Bech32Address):
        """
        Get locked delegate information of the address.
        """
        return self.function_processor(InnerFn.delegate_getDelegateLockInfo, locals(), is_call=True)


class _DelegateReward(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000006'

    def withdraw_delegate_reward(self):
        """
        withdraw all delegate rewards from sending address
        """
        return self.function_processor(InnerFn.delegate_withdrawDelegateReward, locals())

    def get_delegate_reward(self,
                            address: Bech32Address,
                            node_ids: [HexStr] = None,
                            ):
        """
        Get the delegate reward information of the address, it can be filtered by node id.
        """
        kwargs = dict(locals())
        kwargs['node_ids'] = [bytes.fromhex(remove_0x_prefix(node_id)) for node_id in node_ids]
        return self.function_processor(InnerFn.delegate_getDelegateReward, kwargs, is_call=True)


class Delegate:
    """
    Delegate is a contract structure, not a contract,
    and you can also use contract object by self.delegateBase or self.delegateReward
    """

    def __init__(self, web3: "Web3"):
        self.delegateBase = _DelegatePart(web3)
        self.delegateReward = _DelegateReward(web3)

    def delegate(self,
                 node_id: Union[NodeID, HexStr],
                 balance_type: int,
                 amount: Von,
                 ):
        return self.delegateBase.delegate(node_id, balance_type, amount)

    def withdrew_delegate(self,
                          node_id: Union[NodeID, HexStr],
                          staking_block_identifier: BlockIdentifier,
                          amount: Von,
                          ):
        return self.delegateBase.withdrew_delegate(node_id, staking_block_identifier, amount)

    def redeem_delegate(self):
        return self.delegateBase.redeem_delegate()

    def get_delegate_list(self, address: Bech32Address):
        return self.delegateBase.get_delegate_list(address)

    def get_delegate_info(self,
                          address: Bech32Address,
                          node_id: Union[NodeID, HexStr],
                          staking_block_identifier: BlockIdentifier,
                          ):
        return self.delegateBase.get_delegate_info(address, node_id, staking_block_identifier)

    def get_delegate_lock_info(self, address: Bech32Address):
        return self.delegateBase.get_delegate_lock_info(address)

    def withdraw_delegate_reward(self):
        return self.delegateReward.withdraw_delegate_reward()

    def get_delegate_reward(self,
                            address: Bech32Address,
                            node_ids: [HexStr] = None,
                            ):
        return self.delegateReward.get_delegate_reward(address, node_ids)
