from typing import (
    Union
)

from platon_typing import (
    NodeID,
    HexStr,
)

from platon._utils.contract_formatter import (
    InnerFn,
)
from platon.types import (
    Version,
    BlockIdentifier,
)
from platon._utils.inner_contract import (
    InnerContract,
)


class Pip(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000005'

    def submit_version_proposal(self,
                                node_id: Union[NodeID, HexStr],
                                pip_number: str,
                                version: Version,
                                voting_rounds: int,
                                ):
        """
        Submit a version proposal to promote version upgrade of the chain.

        :param node_id: the node id of the verifier who submitted the proposal
        :param pip_number: generally, it is the pull request id of github.com/PlatONNetwork/PIPsPIPs project
        :param version: the version you want to upgrade to
        :param voting_rounds: the number of voting consensus rounds, it will be converted to the block number,
            and the voting end block number will be 20 blocks earlier than this
        """
        return self.function_processor(InnerFn.govern_submitVersionProposal, locals())

    def submit_param_proposal(self,
                              node_id: Union[NodeID, HexStr],
                              pip_number: str,
                              module: str,
                              name: str,
                              value: str,
                              ):
        """
        Submit a parameter proposal to change the value of the governable parameter.
        Use 'self.govern_param_list' to get all governable parameters.

        :param node_id: the node id of the verifier who submitted the proposal
        :param pip_number: generally, it is the pull request id of github.com/PlatONNetwork/PIPs project
        :param module: the module to which the parameter belongs
        :param name: parameter name
        :param value: new parameter value
        """
        return self.function_processor(InnerFn.govern_submitParamProposal, locals())

    def submit_text_proposal(self,
                             node_id: Union[NodeID, HexStr],
                             pip_number: str,
                             ):
        """
        Submit a text proposal to collect votes from verifiers.
        This proposal will not have any impact on the chain.

        :param node_id: the node id of the verifier who submitted the proposal
        :param pip_number: generally, it is the pull request id of github.com/PlatONNetwork/PIPs project
        """
        return self.function_processor(InnerFn.govern_submitTextProposal, locals())

    def submit_cancel_proposal(self,
                               node_id: Union[NodeID, HexStr],
                               pip_number: str,
                               voting_rounds: int,
                               proposal_id: Union[bytes, HexStr],
                               ):
        """
        Submit a cancel proposal to cancel another proposal.
        The proposal to be cancelled must be during the voting period, and is not a text proposal or a cancel proposal.

        :param node_id: the node id of the verifier who submitted the proposal
        :param pip_number: generally, it is the pull request id of github.com/PlatONNetwork/PIPs project
        :param voting_rounds: the number of voting consensus rounds, it will be converted to the block number,
            and the voting end block number will be 20 blocks earlier than this
        :param proposal_id: hash id of the proposal to be cancelled
        """
        return self.function_processor(InnerFn.govern_submitCancelProposal, locals())

    def vote(self,
             node_id: Union[NodeID, HexStr],
             proposal_id: Union[bytes, HexStr],
             option: int,
             node_version: Version,
             version_sign: Union[bytes, HexStr],
             ):
        """
        To vote on a proposal, the proposal must be in the voting period.
        When the voting conditions are met, the proposal will be passed and become effective.

        :param node_id: the node id of the verifier who submitted the vote
        :param proposal_id: hash id of the proposal to be voted on
        :param option: voting option, include: Yeas: 1, Nays: 2, Abstentions: 3
        :param node_version: node version, obtained by rpc 'admin_getProgramVersion' interface
        :param version_sign: node version signature, obtained by rpc 'admin_getProgramVersion' interface
        """
        return self.function_processor(InnerFn.govern_vote, locals())

    def declare_version(self,
                        node_id: Union[NodeID, HexStr],
                        node_version: Version,
                        version_sign: Union[bytes, HexStr],
                        ):
        """
        Declare the version of the node to the chain.
        When the node version is the same as the current version of the blockchain,
        the node will be able to participate in the consensus.

        :param node_id: the node id of the candidate who submitted the version declare
        :param node_version: node version, obtained by rpc 'admin_getProgramVersion' interface
        :param version_sign: node version signature, obtained by rpc 'admin_getProgramVersion' interface
        """
        return self.function_processor(InnerFn.govern_declareVersion, locals())

    def get_proposal(self, proposal_id: Union[bytes, HexStr]):
        """
        Get details of the proposal

        :param proposal_id: hash id of the proposal
        """
        return self.function_processor(InnerFn.govern_getProposal, locals(), is_call=True)

    def get_proposal_votes(self,
                           proposal_id: Union[bytes, HexStr],
                           block_identifier: BlockIdentifier = 'latest',
                           ):
        """
        Get the voting information for the proposal based on the block identifier.

        :param proposal_id: hash id of the proposal
        :param block_identifier: block identifier
        """
        kwargs = dict(locals())
        block = self.web3.platon.get_block(block_identifier)
        kwargs['block_identifier'] = block['hash']
        return self.function_processor(InnerFn.govern_getProposalVotes, kwargs, is_call=True)

    def get_proposal_result(self, proposal_id: Union[bytes, HexStr]):
        """
        Get proposal results, you can query only after the proposal is complete.
        use 'self.get_proposal_votes' to get current voting information.

        :param proposal_id: proposal id
        """
        return self.function_processor(InnerFn.govern_getProposalResult, locals(), is_call=True)

    def proposal_list(self):
        """
        Get proposal list for the chain
        """
        return self.function_processor(InnerFn.govern_proposalList, locals(), is_call=True)

    def get_chain_version(self):
        """
        Query the chain effective version of the node
        """
        return self.function_processor(InnerFn.govern_getChainVersion, locals(), is_call=True)

    def get_govern_param(self, module: str, name: str):
        """
        Get the current value of the governable parameter
        Use 'self.govern_param_list' to get all governable parameters.

        :param module: the module to which the parameter belongs
        :param name: parameter name
        """
        return self.function_processor(InnerFn.govern_getGovernParam, locals(), is_call=True)

    def govern_param_list(self, module: str = ''):
        """
        get all governable parameters.

        :param module: optionally, specify a module name
        """
        return self.function_processor(InnerFn.govern_governParamList, locals(), is_call=True)
