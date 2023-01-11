from typing import (
    Union,
)

from platon_typing import (
    NodeID,
    HexStr,
)

from platon.types import (
    InnerFn, BlockIdentifier,
)
from platon._utils.inner_contract import (
    InnerContract,
)


class Slashing(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000004'

    def report_duplicate_sign(self, report_type: int, data: str):
        """
        Report a node signs the illegal consensus message after it signs the correct consensus message.

        :param report_type: duplicate sign type, prepareBlock: 1, prepareVote: 2, viewChange: 3
        :param data: a JSON string of evidence, format reference RPC platon_Evidences
        """
        return self.function_processor(InnerFn.slashing_reportDuplicateSign, locals())

    def check_duplicate_sign(self,
                             report_type: int,
                             node_id: Union[NodeID, HexStr],
                             block_identifier: BlockIdentifier,
                             ):
        """
        get whether the node has been reported for duplicate-signed from someone

        :param report_type: duplicate sign type, prepareBlock: 1, prepareVote: 2, viewChange: 3
        :param node_id: node id to report
        :param block_identifier: duplicate-signed block identifier
        """
        kwargs = dict(locals())
        block = self.web3.platon.get_block(block_identifier)
        kwargs['block_identifier'] = block['number']
        return self.function_processor(InnerFn.slashing_checkDuplicateSign, kwargs, is_call=True)
