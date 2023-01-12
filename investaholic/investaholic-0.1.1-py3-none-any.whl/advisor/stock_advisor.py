from typing import Optional, List
from datetime import datetime as dt
from .advisor import Advisor
from investaholic_common.classes.position import Position
from investaholic_common.classes.proposal import Proposal
from investaholic_common.representation.position_representation import PositionRepresentation
from investaholic_common.representation.proposal_representation import ProposalRepresentation
import requests


class StockAdvisor(Advisor):
    def __init__(self):
        Advisor.__init__(self)

    def advise(self) -> Proposal:
        response = requests.post(f'{self._url}/proposals/users/{self.customer.id}')
        if response.status_code != 200:
            raise ConnectionError(f'Proposal creation [POST] return {response.status_code}:{response.text}')

        return ProposalRepresentation.as_object(response.json())

    def modify_position_quantity(self, ticker: str, n_proposal: int, quantity: float) -> Optional[Position]:
        return self._modify_position(ticker=ticker, n_proposal=n_proposal, quantity=quantity)

    def close_position_scheduled(self, ticker: str, n_proposal: int, closing_date: dt):
        return self._modify_position(ticker=ticker, n_proposal=n_proposal, closing_date=closing_date)

    def close_position_now(self, ticker: str, n_proposal: int):
        return self._modify_position(ticker=ticker, n_proposal=n_proposal)

    def _modify_position(self, ticker: str, n_proposal: int, quantity=None, closing_date=None):
        self._validate_position(ticker=ticker, n_proposal=n_proposal)

        # Assign the body to link to the request
        if quantity is not None and closing_date is None:
            body = {'quantity': quantity}
        elif closing_date is not None and quantity is None:
            body = {'closing_date': closing_date.strftime("%d-%m-%Y")}
        elif quantity is None and closing_date is None:
            body = {'closing_date': dt.now().strftime("%d-%m-%Y")}
        else:
            raise ValueError('Cannot specify both the quantity and the closing date')

        response = requests.put(f'{self._url}/positions/proposals/{n_proposal}'
                                f'/tickers/{ticker}', json=body)

        if response.status_code != 200:
            raise ConnectionError(f'Position modification [PUT] returned {response.status_code}:{response.json()["message"]}')

        return PositionRepresentation.as_object(response.json())

    def remove_position(self, ticker: str, n_proposal: int):
        self._validate_position(n_proposal=n_proposal, ticker=ticker)

        response = requests.delete(f'{self._url}/positions/proposals/{n_proposal}/'
                                   f'tickers/{ticker}')

        if response.status_code != 200:
            raise ConnectionError(f'User deletion [DELETE] returned {response.status_code}:{response.json()["message"]}')

        return PositionRepresentation.as_object(response.json())

    def __str__(self) -> str:
        return f'Stock advisor of {self.customer.name} {self.customer.surname} (ID: {self.customer.id})'

    def _validate_ticker(self, ticker: str):
        response = requests.get(f'{self._url}/tickers/{ticker}')
        if response.status_code != 200:
            raise ConnectionError(f'{response.json()["message"]}')

    def _validate_position(self, ticker: str, n_proposal: int):
        """
        Check whether the given position exists and belongs to the associated
        customer
        """

        self._validate_n_proposal(n_proposal=n_proposal)
        self._validate_ticker(ticker=ticker)
        response = requests.get(f'{self._url}/proposals/users/{self.customer.id}')

        # Response checks
        if response.status_code == 404:
            raise ValueError(f'Customer {self.customer.id} has no proposals yet.')
        if response.status_code != 200:
            raise ConnectionError(f'Position retrival [GET] returned {response.status_code}:{response.json()["message"]}')

        # Belonging validation

        # If single proposal
        if not isinstance(response.json(), list):
            user_proposals: Proposal = [ProposalRepresentation.as_object(response.json())]

        # If multiple
        else:
            user_proposals: List[Proposal] = [ProposalRepresentation.as_object(x) for x in response.json() if
                                           x['code'] == n_proposal]

        if not len(user_proposals) == 1 or not (
                ticker in [position.ticker.symbol for position in user_proposals[0].positions]):
            raise ValueError('Position not belonging to user')