from abc import ABC, abstractmethod
import requests
from investaholic_common.classes.proposal import Proposal
from investaholic_common.errors.errors import AssociationError
from investaholic_common.representation.proposal_representation import ProposalRepresentation
from investaholic_common.representation.user_representation import UserRepresentation
from investaholic_common.classes.user import User
from tabulate import tabulate


class Advisor(ABC):
    def __init__(self):
        self._customer: User = None
        self._url = 'http://127.0.0.1:5000'

    @property
    def proposals(self):
        return self._get_user_proposals()

    def _get_user_proposals(self):
        response = requests.get(f'{self._url}/proposals/users/{self.customer.id}')

        if response.status_code != 200:
            raise ConnectionError(f'Proposals retrieval [GET] returned {response.status_code}:{response.json()["message"]}')

        if not isinstance(response.json(), list):
            return ProposalRepresentation.as_object(response.json())

        return [ProposalRepresentation.as_object(x) for x in response.json()]

    def get_last_proposal(self):
        proposals = self.proposals

        if isinstance(proposals, list):
            return list(sorted(proposals, key=lambda x: x.code, reverse=True))[0]

        return proposals

    def associate_new_customer(self, customer: User):
        if self.customer is not None:
            raise AssociationError(f'Advisor already associated to customer {self.customer.id}')

        self._add_customer(customer)
        self._customer = customer

    def associate_existing_customer(self, customer_id: str):
        if self.customer is not None:
            raise AssociationError(f'Advisor already associated to customer {self.customer.id}')

        self._customer = self._get_customer(customer_id)

    def _get_customer(self, customer_id: str) -> User:
        response = requests.get(f'{self._url}/users/{customer_id}')

        if response.status_code != 200:
            raise ConnectionError(f'Customer retrieval returned {response.status_code}:{response.json()["message"]}')

        return UserRepresentation.as_object(response.json())

    @property
    def customer(self):
        return self._customer

    @abstractmethod
    def advise(self):
        pass

    def _add_customer(self, customer: User):
        response = requests.get(f'{self._url}/users/{customer.id}')

        if response.status_code != 404:
            raise ValueError('Customer ID already present in the database')

        body = {
            'id': customer.id,
            'name': customer.name,
            'surname': customer.surname,
            'risk': customer.risk.value,
            'capital': customer.capital
        }
        requests.post(f'{self._url}/users',
                      json=body)
        
    def delete_proposal(self, n_proposal: int):
        if self.customer is None:
            raise AssociationError('Advisor has no customer associated.')

        if not self._validate_n_proposal(n_proposal):
            raise ValueError(f'{n_proposal} does not belong to user {self._customer.id}')
        response = requests.delete(f'{self._url}/proposals/{n_proposal}')

        if response.status_code != 200:
            raise ConnectionError(f'Proposal deletion [DELETE] returned {response.status_code}:{response.json()["message"]}')

    def _validate_n_proposal(self, n_proposal: int):
        request = requests.get(f'{self._url}/proposals/{n_proposal}')
        if request.status_code == 404:
            raise ValueError(f'{n_proposal} is not a valid proposal code')

        return self._customer.id in request.json()['user_id']

    def display_proposals(self) -> str:
        # start data, code, user_id, position
        if not isinstance(self.proposals, list):
            return self._tabulate_proposal(self.proposals)

        fmt = ''
        for proposal in self.proposals:
            fmt += f"{self._tabulate_proposal(proposal)}" \
                   f"\n\n{'-' * 100}\n\n"
        return fmt

    @classmethod
    def _tabulate_proposal(cls, proposal: Proposal):
        table = []
        headers = ['Start date', 'Proposal code', 'User ID', 'Ticker', 'Quantity', 'Closing date', 'Total capital']

        for i, position in enumerate(proposal.positions):
            start_date = proposal.date.strftime('%d/%m/%Y') if i == 0 else '-'
            code = proposal.code if i == 0 else '-'
            user_id = proposal.user_id if i == 0 else '-'
            closing_date = position.closing_date.strftime('%d/%m/%Y') if position.closing_date is not None else '-'
            table.append([start_date, code, user_id, position.ticker.symbol, position.quantity, closing_date,
                          f'{position.total_price():.2f} $'])
        table.append(['Total'] + (['-'] * (len(headers) - 2)) + [f'{proposal.total_price():.2f} $'])
        return tabulate(table, headers=headers)
