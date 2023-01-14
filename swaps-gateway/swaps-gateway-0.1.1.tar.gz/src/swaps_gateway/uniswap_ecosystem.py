from decimal import Decimal
import json
from web3 import Web3
from uniswap import Uniswap
from time import time

class GeneralSwapV2:
    provider_url: str
    router_address: str
    _tokens_list: dict
    max_swap_gas: int
    max_approve_gas: int

    def __init__(self, privkey, base_token_symbol="ETH") -> None:
        self.base_token_symbol = base_token_symbol
        self.base_token_address = "0x0000000000000000000000000000000000000000"
        self.web3 = Web3(Web3.HTTPProvider(self.provider_url))
        self.owner_address = self.web3.eth.account.from_key(privkey).address
        self.private_key = privkey
        router_abi = json.load(open("./src/swaps_gateway/router_abi.txt", "r"))
        self.router_contract = self.web3.eth.contract(address=self.router_address, abi=router_abi)
        self.weth = self.router_contract.functions.WETH().call()
        self._tokens_list = {
            base_token_symbol: {
                "address": self.base_token_address,
                "decimals": 18
            }
        }
    
    def add_token(self, symbol:str, address:str, decimals: int):
        self._tokens_list[symbol] = {"address": address, "decimals": decimals}
    
    def remove_token(self, symbol:str):
        if symbol in self._tokens_list:
            del self._tokens_list[symbol]

    def get_tokens_list(self):
        return self._tokens_list

    def to_unit(self, value, token_symbol):
        return int(value * 10 ** self._tokens_list[token_symbol]["decimals"])
    
    def from_unit(self, value, token_symbol):
        return Decimal(value) / Decimal(10 ** self._tokens_list[token_symbol]["decimals"])
    
    def estimate_spending_amount(self, amount_token2, token1=None, token2=None, tokens_list=None):
        swap_symbols = tokens_list if tokens_list else [token1, token2]
        swap_path = [self._tokens_list[item]["address"] for item in swap_symbols]
        token1_symbol = swap_symbols[0]
        token2_symbol = swap_symbols[-1]
        receive_amount_units = self.to_unit(amount_token2, token2_symbol)
        swap_eth = self.base_token_address in swap_path
        if swap_eth:
            swap_path[swap_path.index(self.base_token_address)] = self.weth
        
        result = self.router_contract.functions.getAmountsIn(
            receive_amount_units, 
            swap_path
            ).call()

        return self.from_unit(result[0], token1_symbol)
    
    def estimate_receiving_amount(self, amount_token1, token1=None, token2=None, tokens_list=None):
        swap_symbols = tokens_list if tokens_list else [token1, token2]
        swap_path = [self._tokens_list[item]["address"] for item in swap_symbols]
        token1_symbol = swap_symbols[0]
        token2_symbol = swap_symbols[-1]
        spend_amount_units = self.to_unit(amount_token1, token1_symbol)
        swap_eth = self.base_token_address in swap_path
        if swap_eth:
            swap_path[swap_path.index(self.base_token_address)] = self.weth
        
        result = self.router_contract.functions.getAmountsOut(
            spend_amount_units, 
            swap_path
            ).call()
        return self.from_unit(result[-1], token2_symbol)
    
    def _execute_swap(self, fixed_receive, receive_amount, spend_amount, token1=None, token2=None, tokens_list=None, deadline=None):
        swap_symbols = tokens_list if tokens_list else [token1, token2]
        token1_symbol = swap_symbols[0]
        token2_symbol = swap_symbols[-1]
        swap_path = [self._tokens_list[item]["address"] for item in swap_symbols]
        nonce = self.web3.eth.getTransactionCount(self.owner_address)
        gas = self.max_swap_gas
        deadline = deadline if deadline else int(int(round(time())) + 10 * 60)
        swap_eth = self.base_token_address in swap_path
        sell_eth = swap_eth and self.base_token_address == swap_path[0]

        receive_amount_units = self.to_unit(receive_amount, token2_symbol)
        spend_amount_units = self.to_unit(spend_amount, token1_symbol)

        if swap_eth:
            swap_path[swap_path.index(self.base_token_address)] = self.weth
            if sell_eth:
                if fixed_receive:
                    tx_body = self.router_contract.functions.swapETHForExactTokens(
                        receive_amount_units,
                        swap_path,
                        self.owner_address,
                        deadline
                    )
                else:
                    tx_body = self.router_contract.functions.swapExactETHForTokens(
                        spend_amount_units,
                        swap_path,
                        self.owner_address,
                        deadline
                    )
            else:
                if fixed_receive:
                    tx_body = self.router_contract.functions.swapTokensForExactETH(
                        receive_amount_units,
                        spend_amount_units,
                        swap_path,
                        self.owner_address,
                        deadline
                    )
                else:
                    tx_body = self.router_contract.functions.swapExactTokensForETH(
                        spend_amount_units,
                        receive_amount_units,
                        swap_path,
                        self.owner_address,
                        deadline
                    )
        else:
            if fixed_receive:
                tx_body = self.router_contract.functions.swapTokensForExactTokens(
                    receive_amount_units,
                    spend_amount_units,
                    swap_path,
                    self.owner_address,
                    deadline
                )
            else:
                tx_body = self.router_contract.functions.swapExactTokensForTokens(
                    spend_amount_units,
                    receive_amount_units,
                    swap_path,
                    self.owner_address,
                    deadline
                )       
        raw_tx = tx_body.buildTransaction(
            {
                'nonce': nonce,
                'gas': gas,
                'gasPrice': self.web3.eth.gas_price,
                'from': self.owner_address,
                'value': spend_amount_units if sell_eth else 0,
                'chainId': self.chain_id
            }
        )
        signed_tx = self.web3.eth.account.sign_transaction(raw_tx, self.private_key)
        result = self.web3.eth.send_raw_transaction(transaction=signed_tx.rawTransaction)
        return result.hex()

    def execute_swap_fixed_input(self, spend_amount, token1=None, token2=None, tokens_list=None, deadline=None):
        receive_amount = self.estimate_spending_amount(spend_amount, token1, token2)
        return self._execute_swap(False, receive_amount, spend_amount, token1, token2, tokens_list, deadline)

    def execute_swap_fixed_output(self, receive_amount, token1=None, token2=None, tokens_list=None, deadline=None):
        spend_amount = self.estimate_spending_amount(receive_amount, token1, token2)
        return self._execute_swap(True, receive_amount, spend_amount, token1, token2, tokens_list, deadline)
    
    def get_allowance_list(self):
        result = {}
        erc20_abi = json.load(open("./src/swaps_gateway/erc20_abi.txt", "r"))
        for item in self._tokens_list:
            if item == self.base_token_symbol:
                continue
            contract = self.web3.eth.contract(address=self._tokens_list[item]["address"], abi=erc20_abi)
            result[item] = self.from_unit(contract.functions.allowance(
                    self.owner_address,
                    self.router_address
                ).call(), item)
        return result
    
    def approve_swap_contract(self, token, amount):
        erc20_abi = json.load(open("./src/swaps_gateway/erc20_abi.txt", "r"))
        amount_units = self.to_unit(amount, token)
        contract = self.web3.eth.contract(address=self._tokens_list[token]["address"], abi=erc20_abi)
        nonce = self.web3.eth.getTransactionCount(self.owner_address)
        raw_tx = contract.functions.approve(self.router_address, amount_units).build_transaction(
            {
                'nonce': nonce,
                'gas': self.max_approve_gas,
                'gasPrice': self.web3.eth.gas_price,
                'from': self.owner_address,
                'value': 0,
                'chainId': self.chain_id
            }
        )
        signed_tx = self.web3.eth.account.sign_transaction(raw_tx, self.private_key)
        result = self.web3.eth.send_raw_transaction(transaction=signed_tx.rawTransaction)
        return result.hex()    

class BinanceSmartChainSwap(GeneralSwapV2):
    provider_url = 'https://bscrpc.com'
    router_address = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
    max_swap_gas = 200_000
    max_approve_gas = 40_000
    chain_id = 56


class BinanceSmartChainTestnetSwap(GeneralSwapV2):
    provider_url = 'https://bsc-testnet.public.blastapi.io'
    router_address = '0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3'
    max_swap_gas = 200_000
    max_approve_gas = 40_000
    chain_id = 97


class GeneralSwapV3:
    provider_url: str
    uniswap: Uniswap
    _tokens_list: dict

    def __init__(self, privkey, base_token_symbol="ETH") -> None:
        self.base_token_symbol = base_token_symbol
        self.base_token_address = "0x0000000000000000000000000000000000000000"
        self.web3 = Web3(Web3.HTTPProvider(self.provider_url))
        self.owner_address = self.web3.eth.account.from_key(privkey).address
        self.private_key = privkey
        self.uniswap = Uniswap(address=self.owner_address, private_key=self.private_key, version=3, provider=self.provider_url)
        self._tokens_list = {
            base_token_symbol: {
                "address": self.base_token_address,
                "decimals": 18
            }
        }
    
    def add_token(self, symbol:str, address:str, decimals: int):
        self._tokens_list[symbol] = {"address": address, "decimals": decimals}
    
    def remove_token(self, symbol:str):
        if symbol in self._tokens_list:
            del self._tokens_list[symbol]

    def get_tokens_list(self):
        return self._tokens_list

    def to_unit(self, value, token_symbol):
        return int(value * 10 ** self._tokens_list[token_symbol]["decimals"])
    
    def from_unit(self, value, token_symbol):
        return Decimal(value) / Decimal(10 ** self._tokens_list[token_symbol]["decimals"])

    def estimate_receiving_amount(self, amount_token1, token1=None, token2=None, tokens_list=None):
        token1 = token1 if token1 else tokens_list[0]
        token2 = token2 if token2 else tokens_list[1]
        token1_address = self._tokens_list[token1]["address"]
        token2_address = self._tokens_list[token2]["address"]
        qty_units = self.to_unit(amount_token1, token1)
        result = self.uniswap.get_price_input(token1_address, token2_address, qty_units, fee=3000)
        return result

    def estimate_spending_amount(self, amount_token2, token1=None, token2=None, tokens_list=None):
        token1 = token1 if token1 else tokens_list[0]
        token2 = token2 if token2 else tokens_list[1]
        token1_address = self._tokens_list[token1]["address"]
        token2_address = self._tokens_list[token2]["address"]
        qty_units = self.to_unit(amount_token2, token2)
        result = self.uniswap.get_price_output(token1_address, token2_address, qty_units, fee=3000)
        return result

    def _execute_swap(self, fixed_receive, receive_amount, spend_amount, token1=None, token2=None, tokens_list=None, deadline=None, fee=3000):
        token1 = token1 if token1 else tokens_list[0]
        token2 = token2 if token2 else tokens_list[1]
        token1_address = self._tokens_list[token1]["address"]
        token2_address = self._tokens_list[token2]["address"]
        spend_amount_units = self.to_unit(spend_amount, token1)
        receive_amount_units = self.to_unit(receive_amount, token2)
        res = self.uniswap.make_trade_output(
            token1_address,
            token2_address,
            receive_amount_units,
            self.owner_address,
            fee
        ) if fixed_receive else \
            self.uniswap.make_trade(
            token1_address,
            token2_address,
            spend_amount_units,
            self.owner_address,
            fee
        )
        return res.hex()

    def execute_swap_fixed_input(self, spend_amount, token1=None, token2=None, tokens_list=None, deadline=None):
        receive_amount = self.estimate_spending_amount(spend_amount, token1, token2)
        return self._execute_swap(False, receive_amount, spend_amount, token1, token2, tokens_list, deadline)

    def execute_swap_fixed_output(self, receive_amount, token1=None, token2=None, tokens_list=None, deadline=None):
        spend_amount = self.estimate_spending_amount(receive_amount, token1, token2)
        return self._execute_swap(True, receive_amount, spend_amount, token1, token2, tokens_list, deadline)


class EthGoerliTestnetSwap(GeneralSwapV3):
    provider_url = 'https://eth-goerli.public.blastapi.io'
    router_address = '0xE592427A0AEce92De3Edee1F18E0157C05861564'
    max_swap_gas = 200_000
    max_approve_gas = 40_000
    chain_id = 5

class PolygonSwap(GeneralSwapV2):
    provider_url = 'https://polygon.llamarpc.com'
    router_address = '0xE592427A0AEce92De3Edee1F18E0157C05861564'
    max_swap_gas = 200_000
    max_approve_gas = 40_000
    chain_id = 137

