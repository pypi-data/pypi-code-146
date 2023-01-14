import copy
import subprocess
import time
import json
import os
from enum import Enum
from sharingiscaring.enums import NET
from sharingiscaring.block import ConcordiumBlockInfo
from sharingiscaring.account import AccountBakerPoolStatus, ConcordiumAccountFromClient
from functools import lru_cache
from rich.console import Console
import datetime as dt

console = Console()

CONCORDIUM_CLIENT_PREFIX    = os.environ.get('CONCORDIUM_CLIENT_PREFIX', '')
REQUESTOR_NODES             = os.environ.get('REQUESTOR_NODES', '207.180.201.8,31.20.212.96')
REQUESTOR_NODES             = REQUESTOR_NODES.split(',')
REQUESTOR_NODES_TESTNET             = os.environ.get('REQUESTOR_NODES_TESTNET', '207.180.201.8')
REQUESTOR_NODES_TESTNET             = REQUESTOR_NODES_TESTNET.split(',')

class RequestorType(Enum):
    accountInfo = '{'
    GetAccountList = '['
    consensus = 'E'
    
class Requestor:
    """
    This class is performing the requests to concordium-client.
    """
    total_count = 0
    failing_nodes = {}
    nodes = REQUESTOR_NODES
    nodes_testnet = REQUESTOR_NODES_TESTNET

    console.log (f"{nodes=}")
    failing_nodes = {k:0 for k in nodes}
    
    def request_failed(self, result):
        if result.returncode == 1:
            return True
        else:
            if result.stdout.decode('utf-8') in ['Cannot establish connection to GRPC endpoint.\n', 'gRPC error: not enough bytes\n']:
                return True
            else:
                return False
        # return result.returncode == 1

    def __init__(self, args, check_nodes=False, timeout=5, net=NET.MAINNET):
        Requestor.total_count += 1
        if net == NET.MAINNET:
            self.std_args = [[f"{CONCORDIUM_CLIENT_PREFIX}concordium-client", '--grpc-retry', '3', '--grpc-ip', x] for x in self.nodes] 
        else:
            self.std_args = [[f"{CONCORDIUM_CLIENT_PREFIX}concordium-client", '--grpc-retry', '3', '--grpc-ip', x, '--grpc-port', '10001'] for x in self.nodes_testnet] 
        self.timeout = timeout
        self.args = args
        if not check_nodes:
            self.ask_the_client_with_backup()
        else:
            self.check_nodes_with_heights()

    def check_nodes(self):
        results = {}
        for arg in self.std_args:
            arg.extend(['raw', 'GetBlockInfo'])
            result = subprocess.run(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            results[arg[2]] = not self.request_failed(result)
        self.nodes_ok = results

    def check_nodes_with_heights(self):
        results = {}
        for arg in self.std_args:
            arg.extend(['raw', 'GetBlockInfo'])
            result = subprocess.run(arg, stdout=subprocess.PIPE)
            json_result = json.loads(result.stdout.decode('utf-8'))
            results[arg[2]] = json_result['blockHeight']
        self.nodes_ok = results

    def ask_the_client_with_backup(self):
        result = subprocess.CompletedProcess([], returncode=1)
        node_index = 0
        while self.request_failed(result) :
            if node_index == len(self.nodes):
                node_index = 0
                # time.sleep(0.001)
            self.arguments = copy.deepcopy(self.std_args[node_index])
            self.arguments.extend(self.args)
            assert (len(self.arguments)) == (len(self.std_args[node_index]) + len(self.args))

            try:
                result = subprocess.run(self.arguments, timeout=self.timeout, stdout=subprocess.PIPE)
                if self.request_failed(result):
                    Requestor.failing_nodes[self.nodes[node_index]] += 1    
                    console.log (result, self.failing_nodes, self.arguments)
                    # time.sleep(0.01)
                    node_index += 1

            except:
                Requestor.failing_nodes[self.nodes[node_index]] += 1    
                # console.log ('Timeout', self.failing_nodes, self.arguments)
                # time.sleep(0.01)
                node_index += 1
            
        self.result = result
        if result.stdout.decode('utf-8') == None:
            console.log(self.arguments, result.stdout)

class ConcordiumClient:
    def __init__(self, tooter):
        self.tooter = tooter
        self.get_cns_cache()

    def request_last_block_info_typed(self, net=NET.MAINNET):
        result = Requestor(['raw', 'GetBlockInfo'], net=net).result
        try:
            typed_result = ConcordiumBlockInfo(**json.loads(result.stdout.decode('utf-8')))
            return typed_result
        except:
            return None

    def request_last_block_info_finalized_typed(self, net=NET.MAINNET):
        result = Requestor(['raw', 'GetBlockInfo'], net=net).result
        try:
            typed_result = ConcordiumBlockInfo(**json.loads(result.stdout.decode('utf-8')))
            if typed_result.finalized:
                return typed_result
            else:
                # request the blockLastFinalized block
                typed_result = self.request_block_info_at_typed(typed_result.blockLastFinalized, net=net)
                return typed_result
        except:
            return None

    def request_last_block_info(self, test=False):
        if not test:
            result = Requestor(['raw', 'GetBlockInfo']).result
        else:
            result = Requestor(['raw', 'GetBlockInfo', 'efe7f7367dd59e83ac0b93daa33f713dc8b8245085bf05a15503faecf30e64e6']).result
        try:
            s = json.loads(result.stdout.decode('utf-8'))
            return s, int(s['blockHeight']), s['blockHash'], s['blockParent'] 
        except: 
            return -1, -1, -1

    def request_block_info_at_typed(self, block, net=NET.MAINNET):
        result = Requestor(['raw', 'GetBlockInfo', block], net=net).result

        try:
            typed_result = ConcordiumBlockInfo(**json.loads(result.stdout.decode('utf-8')))
            return typed_result
        except: 
            return None

    def request_blockInfo_at(self, block):
        result = Requestor(['raw', 'GetBlockInfo', block]).result

        try:
            s = json.loads(result.stdout.decode('utf-8'))
            return s, int(s['blockHeight']), s['blockHash'], s['blockParent'] 
        except: 
            return -1, -1, -1

    def request_last_block_info_for_expectation(self):
        result = Requestor(['raw', 'GetBlockInfo']).result
        s = json.loads(result.stdout.decode('utf-8'))
        return s

    def check_node_at(self, ip, port='10000'):
        arg = [f"{CONCORDIUM_CLIENT_PREFIX}concordium-client", '--grpc-retry', '1', 
            '--grpc-ip', ip, '--grpc-port', str(port),
            'raw', 'GetNodeInfo']
        try:
            result = subprocess.run(arg, stdout=subprocess.PIPE, timeout=2)
            return result.stdout.decode('utf-8').split('\n'), None
        except subprocess.TimeoutExpired:
            return -1, 'Timeout Error'

    def request_accountInfo_at(self, block, account):
        result = Requestor(['raw', 'GetAccountInfo', account, block]).result
        return json.loads(result.stdout.decode('utf-8'))

    def request_accountInfo_at_typed(self, block, account):
        result = Requestor(['raw', 'GetAccountInfo', account, block]).result
        try:
            typed_result = ConcordiumAccountFromClient(**json.loads(result.stdout.decode('utf-8')))
            return typed_result
        except:
            return None

    def request_reward_status(self):
        result = Requestor(['raw', 'GetRewardStatus']).result
        return json.loads(result.stdout.decode('utf-8'))

    def request_block_hash_at_height(self, height:int, net=NET.MAINNET, measure=False):
        start = dt.datetime.now()
        result = Requestor(['raw', 'GetBlocksAtHeight', str(height)], net=net).result
        s = json.loads(result.stdout.decode('utf-8'))
        
        measurement = (dt.datetime.now() - start).total_seconds() * 1000 # millisecons

        if not measure:
            return s[0]
        else:
            return s[0], measurement

    def get_last_block_from_node_at(self, ip, port='10000'):
        arg = [f"{CONCORDIUM_CLIENT_PREFIX}concordium-client", '--grpc-retry', '1', 
            '--grpc-ip', ip, '--grpc-port', str(port),
            'raw', 'GetBlockInfo']
        try:
            result = subprocess.run(arg, stdout=subprocess.PIPE, timeout=2)
            s = json.loads(result.stdout.decode('utf-8'))
            return int(s['blockHeight']), None
        except subprocess.TimeoutExpired:
            return -1, 'Timeout Error'
        
        
    def request_blockSummary_at(self, block, net=NET.MAINNET):
        # print (f"request_blockSummary_at {block=}:")
        result = Requestor(['raw', 'GetBlockSummary', block], net=net).result
        return json.loads(result.stdout.decode('utf-8'))

    def request_rewardStatus(self):
        result = Requestor(['raw', 'GetRewardStatus']).result

        try:
            s = json.loads(result.stdout.decode('utf-8'))
            return s['nextPaydayTime']
        except: 
            return -1

    def request_modules(self):
        result = Requestor(['raw', 'GetModuleList']).result
        return json.loads(result.stdout.decode('utf-8'))

    def request_module(self, address):
        result = Requestor(['module', 'inspect', address]).result
        return result.stdout.decode('utf-8')

    def request_contracts(self):
        result = Requestor(['raw', 'GetInstances']).result
        return json.loads(result.stdout.decode('utf-8'))

    def request_contract(self, address):
        index = address['index']
        subindex = address['subindex']
        result = Requestor(['contract', 'show', str(index), '--subindex', str(subindex)]).result
        return result.stdout.decode('utf-8')

    def request_account(self, address):
        result = Requestor(['raw', 'GetAccountInfo', address]).result
        return json.loads(result.stdout.decode('utf-8'))

    def request_identity_providers(self):
        result = Requestor(['raw', 'GetIdentityProviders']).result
        return json.loads(result.stdout.decode('utf-8'))

    def request_pool_status(self, pool_id):
        result = Requestor(['raw', 'GetPoolStatus', '--pool', str(pool_id)]).result
        return json.loads(result.stdout.decode('utf-8'))

    @lru_cache()
    def request_pool_status_at_block_typed(self, pool_id, blockHash:str):
        if pool_id:
            result = Requestor(['raw', 'GetPoolStatus', '--pool', str(pool_id), blockHash]).result
        else:
            result = Requestor(['raw', 'GetPoolStatus', blockHash]).result
        try:
            typed_result = AccountBakerPoolStatus(**json.loads(result.stdout.decode('utf-8')))
            return typed_result
        except Exception as e:
            print (e) 
            return None
        
    ### CNS

    def call_client_with(self, args):
        arguments = [f"{CONCORDIUM_CLIENT_PREFIX}concordium-client", '--grpc-retry', '3', '--grpc-ip', REQUESTOR_NODES[0]]
        arguments.extend(args)
        result = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (_, err) = result.communicate()
        return err.decode()

    # load and save
    def get_cns_cache(self):
        try:
            with open(f'persist/cns_cache_by_name.json', 'r') as f:   
                self.cns_cache_by_name = json.load(f)
                # console.log(f"Read {len(self.cns_cache_by_name.keys()):,.0f} cns domain names from cache.")
        except:
            self.cns_cache_by_name = {}
            console.log("Could not read cns_cache_by_name.json.")

        try:
            with open(f'persist/cns_cache_by_token_id.json', 'r') as f:   
                self.cns_cache_by_token_id = json.load(f)
        except:
            self.cns_cache_by_token_id = {}
        
    def save_cns_cache(self):
        with open(f'persist/cns_cache_by_name.json', 'w') as outfile:
                outfile.write(json.dumps(self.cns_cache_by_name, indent=0))
        
        with open(f'persist/cns_cache_by_token_id.json', 'w') as outfile:
                outfile.write(json.dumps(self.cns_cache_by_token_id, indent=0))
                console.log(f"Wrote {len(self.cns_cache_by_token_id.keys()):,.0f} cns domain names to cache.")
    
    def get_expected_blocks_per_day(self, lp):
        slots_in_day = 14400 * 24
        return slots_in_day * (1.0 - (1-1/40)**(lp))

    def get_bakers_for_day(self, blockHash):
        '''
        This function retrieves the baker state at the specified block. No information is saved to disk.
        '''
        bakers_by_account = {}
        bakers_by_baker_id = {}
        baker_map_lp = {}
        baker_map_bpy = {}
        console.log("Getting bakers for the day...")
        result = Requestor(['consensus', 'show-parameters', '--include-bakers', '--block', blockHash], timeout=3).result
        decoded = result.stdout.decode('utf-8').split('\n')
        bakers_raw = decoded[4:]
        
        for baker_line in bakers_raw:
            if len(baker_line) > 1:
                baker_id = int(baker_line.split(':')[0].split(' ')[-1])
                account = baker_line.split(':')[1].split()[0]
                # if this is a named account...
                if baker_line.split()[-2] == '%':
                    lp = baker_line.split()[-3] if baker_line.split()[-3] != '<0.0001' else 0.0
                else:
                    lp = baker_line.split()[-2] if baker_line.split()[-2] != '<0.0001' else 0.0 
                lp = float(lp) / 100 # to make an actual percentage!
                baker_dict_line = {"baker_id": baker_id, "account": account, "lp": float(lp), "expected_blocks_per_day": self.get_expected_blocks_per_day(lp)  }
                
                bakers_by_baker_id[baker_id] = baker_dict_line
                bakers_by_account[account] = baker_dict_line
                baker_map_lp[account]  = float(lp) / 100
                baker_map_bpy[account] = f"{(8640 * float(lp) / 100 * 365.25):,.2f}"

        bakers_count = len(bakers_by_baker_id.keys())
        return bakers_by_account, bakers_by_baker_id