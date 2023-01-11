from platon_typing import Bech32Address

from platon.types import InnerFn
from platon._utils.inner_contract import (
    InnerContract,
)


class Restricting(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000001'

    def create_restricting(self,
                           release_address: Bech32Address,
                           plans: [dict],
                           ):
        """
        Create a restricting

        :param release_address: released to account
        :param plans: a list of restricting plan, for example:
            [{'Epoch': 2, 'Amount': Web3.toVon(1, 'ether')}, {'Epoch': 8, 'Amount': Web3.toVon(3, 'ether')}]

            restricting plan is defined as follows:
            {
                Epoch: int   # the amount will be released to release address when the epoch ends
                Amount: Von  # restricting amount
            }
        """
        kwargs = dict(locals())     # new dict
        kwargs['plans'] = [list(plan.values()) for plan in plans]
        return self.function_processor(InnerFn.restricting_createRestricting, kwargs)

    def get_restricting_info(self, release_address: Bech32Address):
        """
        Get the restricting information.

        :param release_address: release address for the restricting
        """
        return self.function_processor(InnerFn.restricting_getRestrictingInfo, locals(), is_call=True)
