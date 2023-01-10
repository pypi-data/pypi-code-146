import datetime as dt
import numpy as np
import pandas as pd
from etherscan import Etherscan

class EtherCrammer:
    def __init__(self, api_key: str, address: str = None, contract: str = None) -> None:
        self._api = Etherscan(api_key)
        self._address = None
        self._contract = None
        self.set_address_and_contract(address, contract)

    def _test_has_results(self, method, endblock, startblock, page):
        """A quick search with only one result to check transaction counts"""
        try:
            method(address=self._address, endblock=endblock, startblock=startblock, sort='desc', offset=1, page=page)
            return True
        except AssertionError as e:
            if str(e) == '[] -- No transactions found':
                return False
            raise e

    def _get_current_block(self):
        timestamp = dt.datetime.now().timestamp()
        block = self._api.get_block_number_by_timestamp(round(timestamp), closest='before')
        return int(block)

    def _recursive_transaction_download(self, endblock, increment, search='eth'):
        def _recursion(endblock, increment):
            if search == 'eth':
                method = self._api.get_normal_txs_by_address
                method_paginated = self._api.get_normal_txs_by_address_paginated
            elif search == 'erc20':
                method = self._api.get_erc20_token_transfer_events_by_address
                method_paginated = self._api.get_erc20_token_transfer_events_by_address_paginated
            else:
                raise ValueError('Choose between "eth" or "erc20" for "search"')
            # The startblock can never be less than 0.
            increment = increment if endblock > increment else endblock
            startblock = endblock - increment
            # If there are no results, nothing is added.
            if not self._test_has_results(method_paginated, endblock, startblock, 1):
                return
            # Etherscan has a maximum amount of results it will return. If the max is hit, it will try again after cutting the period in half.
            if self._test_has_results(method_paginated, endblock, startblock, 10000):
                increment = increment//2
                _recursion(endblock, increment)
                endblock = endblock - increment
                increment = endblock - startblock
                _recursion(endblock, increment)
                return
            transactions = method(address=self._address, startblock=startblock, endblock=endblock, sort='desc')
            all_transactions.extend(transactions)

        all_transactions = []
        _recursion(endblock, increment)
        return all_transactions

    def _simplify_erc20_value(self, df):
        """ERC20 Token amounts are expressed using two columns. This function
        consolidates them to their numerical values"""
        decimal_column = 'tokenDecimal'
        value_column = 'value'
        df[decimal_column] = df[decimal_column].replace('', np.nan)
        df[decimal_column] = 10 ** df[decimal_column].astype(float)
        df[value_column] = df[value_column].astype(float) / df[decimal_column]
        return df.drop(columns=[decimal_column])

    def _convert_wei_to_eth(self, df):
        """All results from API are expressed in wei. Converts to human
        readable eth units."""
        value_column = 'value'
        df[value_column] = df[value_column].astype(float) / 1000000000000000000
        return df

    def _add_direction_column(self, df):
        if not self._address:
            return df
        direction_column = 'direction'
        direction_values = ['SELF', 'IN', 'OUT']
        incoming = df['to'] == self._address
        outgoing = df['from'] == self._address
        conditions = pd.concat([incoming & outgoing, incoming & ~outgoing, ~incoming & outgoing], axis=1)
        conditions.columns = direction_values
        df[direction_column] = conditions.idxmax(axis=1)
        return df

    def _results_to_dataframe(self, transactions, search='eth'):
        timestamp_column = 'timeStamp'
        time_column = 'time'
        df = pd.DataFrame(transactions)
        df[timestamp_column] = pd.to_datetime(df[timestamp_column].astype(int), unit='s')
        if search == 'eth':
            df = self._convert_wei_to_eth(df)
        elif search == 'erc20':
            df = self._simplify_erc20_value(df)
        df = self._add_direction_column(df)
        return df.rename(columns={timestamp_column: time_column})

    def set_address_and_contract(self, address: str = None, contract: str = None):
        """Sets the instance variables for address and contract for ethereum
        searches.

        Args:
            address (str, optional): An ethereum address hash. Defaults to None.
            contract (str, optional): An ethereum contract hash. Defaults to
                None.

        Raises:
            ValueError: If anything other than address is used.
        """
        if contract or not address:
            raise ValueError('Only address supported at this time. Must choose an address without specifying contract')
        self._address = address

    def download_eth_history(self, search='eth'):
        endblock = self._get_current_block()
        transactions = self._recursive_transaction_download(endblock, increment=endblock, search=search)
        if len(transactions) == 0:
            print('No results found')
            return
        return self._results_to_dataframe(transactions, search)

    
def main():
    api_key = '9NJTVVUW7TDEM2TMZJ3I5SYA37QM7GADE1'
    address = '0x0f4ee9631f4be0a63756515141281a3e2b293bbe'
    eth = EtherCrammer(api_key, address)
    hist = eth.download_eth_history(search='erc20')
    print(hist)


if __name__ == '__main__':
    main()
