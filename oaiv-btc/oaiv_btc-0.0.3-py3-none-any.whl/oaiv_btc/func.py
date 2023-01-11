
import math
import random
import datetime

import numpy
import numpy as np

from bitcoinlib.wallets import WalletError, WalletKey, Address
from bitcoinlib.transactions import Output, TransactionError, get_unlocking_script_type, Input
from bitcoinlib.values import Value, value_to_satoshi
from bitcoinlib.config.config import DEFAULT_NETWORK, SIGHASH_ALL, SIGHASH_ANYONECANPAY, SIGHASH_SINGLE, SIGHASH_NONE, SEQUENCE_LOCKTIME_DISABLE_FLAG, MAX_TRANSACTIONS, SEQUENCE_LOCKTIME_TYPE_FLAG, SEQUENCE_REPLACE_BY_FEE
from bitcoinlib.networks import Network
from bitcoinlib.encoding import int_to_varbyteint, varstr, double_sha256, to_bytes
from bitcoinlib.services.services import Service
from bitcoinlib.keys import HDKey, Key, sign


class Transactor:
    # def __init__(self, witness_type, address, compressed, hdkey):
    def __init__(self, address, hdkey):
        # self.witness_type = witness_type
        self.address = address
        self.db_cache_uri = None
        self.providers = None
        self.multisig_n_required = 1
        self.sort_keys = False
        # self.compressed = compressed
        self.hdkey = hdkey
        self.network = Network(DEFAULT_NETWORK)
        self.compressed = hdkey.compressed
    def addresslist(self):
        return [self.address]
    @property
    def encoding(self):
        return self.hdkey.encoding
    @property
    def witness_type(self):
        return self.hdkey.witness_type
    def send_to(self, to_address, amount, input_key_id=None, account_id=None, network=None, fee=None, min_confirms=1,
                priv_keys=None, locktime=0, offline=True, number_of_change_outputs=1):
        """
        Create transaction and send it with default Service objects :func:`services.sendrawtransaction` method.

        Wrapper for wallet :func:`send` method.

        >>> w = Wallet('bitcoinlib_legacy_wallet_test')
        >>> t = w.send_to('1J9GDZMKEr3ZTj8q6pwtMy4Arvt92FDBTb', 200000, offline=True)
        >>> t
        <WalletTransaction(input_count=1, output_count=2, status=new, network=bitcoin)>
        >>> t.outputs # doctest:+ELLIPSIS
        [<Output(value=..., address=..., type=p2pkh)>, <Output(value=..., address=..., type=p2pkh)>]

        :param to_address: Single output address as string Address object, HDKey object or WalletKey object
        :type to_address: str, Address, HDKey, WalletKey
        :param amount: Output is the smallest denominator for this network (ie: Satoshi's for Bitcoin), as Value object or value string as accepted by Value class
        :type amount: int, str, Value
        :param input_key_id: Limit UTXO's search for inputs to this key ID or list of key IDs. Only valid if no input array is specified
        :type input_key_id: int, list
        :param account_id: Account ID, default is last used
        :type account_id: int
        :param network: Network name. Leave empty for default network
        :type network: str
        :param fee: Set fee manually, leave empty to calculate fees automatically. Set fees in the smallest currency  denominator, for example satoshi's if you are using bitcoins. You can also supply a string: 'low', 'normal' or 'high' to determine fees automatically.
        :type fee: int, str
        :param min_confirms: Minimal confirmation needed for an UTXO before it will be included in inputs. Default is 1. Option is ignored if input_arr is provided.
        :type min_confirms: int
        :param priv_keys: Specify extra private key if not available in this wallet
        :type priv_keys: HDKey, list
        :param locktime: Transaction level locktime. Locks the transaction until a specified block (value from 1 to 5 million) or until a certain time (Timestamp in seconds after 1-jan-1970). Default value is 0 for transactions without locktime
        :type locktime: int
        :param offline: Just return the transaction object and do not send it when offline = True. Default is True
        :type offline: bool
        :param number_of_change_outputs: Number of change outputs to create when there is a change value. Default is 1. Use 0 for random number of outputs: between 1 and 5 depending on send and change amount
        :type number_of_change_outputs: int

        :return WalletTransaction:
        """

        outputs = [(to_address, amount)]
        return self.send(outputs, input_key_id=input_key_id, account_id=account_id, network=network, fee=fee,
                         min_confirms=min_confirms, priv_keys=priv_keys, locktime=locktime, offline=offline,
                         number_of_change_outputs=number_of_change_outputs)

    def send(self, output_arr, input_arr=None, input_key_id=None, account_id=None, network=None, fee=None,
             min_confirms=1, priv_keys=None, max_utxos=MAX_TRANSACTIONS, locktime=0, offline=True, number_of_change_outputs=1):
        """
        Create a new transaction with specified outputs and push it to the network.
        Inputs can be specified but if not provided they will be selected from wallets utxo's
        Output array is a list of 1 or more addresses and amounts.

        Uses the :func:`transaction_create` method to create a new transaction, and uses a random service client to send the transaction.

        >>> w = Wallet('bitcoinlib_legacy_wallet_test')
        >>> t = w.send([('1J9GDZMKEr3ZTj8q6pwtMy4Arvt92FDBTb', 200000)], offline=True)
        >>> t
        <WalletTransaction(input_count=1, output_count=2, status=new, network=bitcoin)>
        >>> t.outputs # doctest:+ELLIPSIS
        [<Output(value=..., address=..., type=p2pkh)>, <Output(value=..., address=..., type=p2pkh)>]

        :param output_arr: List of output tuples with address and amount. Must contain at least one item. Example: [('mxdLD8SAGS9fe2EeCXALDHcdTTbppMHp8N', 5000000)]. Address can be an address string, Address object, HDKey object or WalletKey object
        :type output_arr: list
        :param input_arr: List of inputs tuples with reference to a UTXO, a wallet key and value. The format is [(txid, output_n, key_id, value)]
        :type input_arr: list
        :param input_key_id: Limit UTXO's search for inputs to this key ID or list of key IDs. Only valid if no input array is specified
        :type input_key_id: int, list
        :param account_id: Account ID
        :type account_id: int
        :param network: Network name. Leave empty for default network
        :type network: str
        :param fee: Set fee manually, leave empty to calculate fees automatically. Set fees in the smallest currency  denominator, for example satoshi's if you are using bitcoins. You can also supply a string: 'low', 'normal' or 'high' to determine fees automatically.
        :type fee: int, str
        :param min_confirms: Minimal confirmation needed for an UTXO before it will be included in inputs. Default is 1. Option is ignored if input_arr is provided.
        :type min_confirms: int
        :param priv_keys: Specify extra private key if not available in this wallet
        :type priv_keys: HDKey, list
        :param max_utxos: Maximum number of UTXO's to use. Set to 1 for optimal privacy. Default is None: No maximum
        :type max_utxos: int
        :param locktime: Transaction level locktime. Locks the transaction until a specified block (value from 1 to 5 million) or until a certain time (Timestamp in seconds after 1-jan-1970). Default value is 0 for transactions without locktime
        :type locktime: int
        :param offline: Just return the transaction object and do not send it when offline = True. Default is True
        :type offline: bool
        :param number_of_change_outputs: Number of change outputs to create when there is a change value. Default is 1. Use 0 for random number of outputs: between 1 and 5 depending on send and change amount
        :type number_of_change_outputs: int

        :return WalletTransaction:
        """

        if input_arr and max_utxos and len(input_arr) > max_utxos:
            raise WalletError("Input array contains %d UTXO's but max_utxos=%d parameter specified" %
                              (len(input_arr), max_utxos))

        transaction = self.transaction_create(output_arr, input_arr, input_key_id, account_id, network, fee,
                                              min_confirms, max_utxos, locktime, number_of_change_outputs)

        if transaction.fee < 500:
            transaction.fee_per_kb = transaction.fee_per_kb * 2
            transaction.fee = transaction.fee * 2
            if self.address in [x.address for x in transaction.outputs]:
                ix = [x.address for x in transaction.outputs].index(self.address)
                if transaction.outputs[ix].value > transaction.fee:
                    transaction.outputs[ix].value = transaction.outputs[ix].value - (transaction.fee // 2)
                else:
                    print("Fee might be extremely low")
                    transaction.fee_per_kb = int(transaction.fee_per_kb / 2)
                    transaction.fee = int(transaction.fee / 2)
            else:
                print("Fee might be extremely low")
                transaction.fee_per_kb = int(transaction.fee_per_kb / 2)
                transaction.fee = int(transaction.fee / 2)

        transaction.sign(priv_keys)
        # Calculate exact fees and update change output if necessary
        if fee is None and transaction.fee_per_kb and transaction.change:
            fee_exact = transaction.calculate_fee()
            # Recreate transaction if fee estimation more than 10% off
            if fee_exact != self.network.fee_min and fee_exact != self.network.fee_max and \
                    fee_exact and abs((float(transaction.fee) - float(fee_exact)) / float(fee_exact)) > 0.10:
                print("Transaction fee not correctly estimated (est.: %d, real: %d). "
                      "Recreate transaction with correct fee" % (transaction.fee, fee_exact))
                transaction = self.transaction_create(output_arr, input_arr, input_key_id, account_id, network,
                                                      fee_exact, min_confirms, max_utxos, locktime,
                                                      number_of_change_outputs)
                transaction.sign(priv_keys)

        transaction.rawtx = transaction.raw()
        transaction.size = len(transaction.rawtx)
        transaction.calc_weight_units()
        transaction.fee_per_kb = int(float(transaction.fee) / float(transaction.vsize) * 1000)
        transaction.txid = transaction.signature_hash()[::-1].hex()
        transaction.send(offline)
        return transaction
    def transaction_create(self, output_arr, input_arr=None, input_key_id=None, account_id=None, network=None, fee=None,
                           min_confirms=1, max_utxos=MAX_TRANSACTIONS, locktime=0, number_of_change_outputs=1,
                           random_output_order=True):
        """
        Create new transaction with specified outputs.

        Inputs can be specified but if not provided they will be selected from wallets utxo's with :func:`select_inputs` method.

        Output array is a list of 1 or more addresses and amounts.

        >>> w = Wallet('bitcoinlib_legacy_wallet_test')
        >>> t = w.transaction_create([('1J9GDZMKEr3ZTj8q6pwtMy4Arvt92FDBTb', 200000)])
        >>> t
        <WalletTransaction(input_count=1, output_count=2, status=new, network=bitcoin)>
        >>> t.outputs # doctest:+ELLIPSIS
        [<Output(value=..., address=..., type=p2pkh)>, <Output(value=..., address=..., type=p2pkh)>]

        :param output_arr: List of output as Output objects or tuples with address and amount. Must contain at least one item. Example: [('mxdLD8SAGS9fe2EeCXALDHcdTTbppMHp8N', 5000000)]
        :type output_arr: list of Output, tuple
        :param input_arr: List of inputs as Input objects or tuples with reference to a UTXO, a wallet key and value. The format is [(txid, output_n, key_ids, value, signatures, unlocking_script, address)]
        :type input_arr: list of Input, tuple
        :param input_key_id: Limit UTXO's search for inputs to this key_id. Only valid if no input array is specified
        :type input_key_id: int
        :param account_id: Account ID
        :type account_id: int
        :param network: Network name. Leave empty for default network
        :type network: str
        :param fee: Set fee manually, leave empty to calculate fees automatically. Set fees in the smallest currency  denominator, for example satoshi's if you are using bitcoins. You can also supply a string: 'low', 'normal' or 'high' to determine fees automatically.
        :type fee: int, str
        :param min_confirms: Minimal confirmation needed for an UTXO before it will be included in inputs. Default is 1 confirmation. Option is ignored if input_arr is provided.
        :type min_confirms: int
        :param max_utxos: Maximum number of UTXO's to use. Set to 1 for optimal privacy. Default is None: No maximum
        :type max_utxos: int
        :param locktime: Transaction level locktime. Locks the transaction until a specified block (value from 1 to 5 million) or until a certain time (Timestamp in seconds after 1-jan-1970). Default value is 0 for transactions without locktime
        :type locktime: int
        :param number_of_change_outputs: Number of change outputs to create when there is a change value. Default is 1. Use 0 for random number of outputs: between 1 and 5 depending on send and change amount        :type number_of_change_outputs: int
        :type number_of_change_outputs: int
        :param random_output_order: Shuffle order of transaction outputs to increase privacy. Default is True
        :type random_output_order: bool

        :return WalletTransaction: object
        """

        if not isinstance(output_arr, list):
            raise WalletError("Output array must be a list of tuples with address and amount. "
                              "Use 'send_to' method to send to one address")
        if not network and output_arr:
            if isinstance(output_arr[0], Output):
                network = output_arr[0].network.name
            elif isinstance(output_arr[0][1], str):
                network = Value(output_arr[0][1]).network.name
        ## network, account_id, acckey = self._get_account_defaults(network, account_id)    ## to REMOVE
        ## network = None

        if input_arr and max_utxos and len(input_arr) > max_utxos:
            raise WalletError("Input array contains %d UTXO's but max_utxos=%d parameter specified" %
                              (len(input_arr), max_utxos))

        # Create transaction and add outputs
        amount_total_output = 0
        transaction = WalletTransaction(hdwallet=self, account_id=account_id, network=network, locktime=locktime)
        transaction.outgoing_tx = True
        for o in output_arr:
            if isinstance(o, Output):
                transaction.outputs.append(o)
                amount_total_output += o.value
            else:
                value = value_to_satoshi(o[1], network=transaction.network)
                amount_total_output += value
                addr = o[0]
                if isinstance(addr, WalletKey):
                    addr = addr.key()
                transaction.add_output(value, addr)
                pass

        srv = Service(network=network, providers=self.providers, cache_uri=self.db_cache_uri)
        transaction.fee_per_kb = None
        if isinstance(fee, int):
            fee_estimate = fee
        else:
            n_blocks = 3
            priority = ''
            if isinstance(fee, str):
                priority = fee
            transaction.fee_per_kb = srv.estimatefee(blocks=n_blocks, priority=priority)
            if not input_arr:
                fee_estimate = int(transaction.estimate_size(number_of_change_outputs=number_of_change_outputs) /
                                   1000.0 * transaction.fee_per_kb)
            else:
                fee_estimate = 0
            if isinstance(fee, str):
                fee = fee_estimate

        # Add inputs
        sequence = 0xffffffff
        if 0 < transaction.locktime < 0xffffffff:
            sequence = 0xfffffffe
        amount_total_input = 0
        if input_arr is None:
            selected_utxos = self.select_inputs(amount_total_output + fee_estimate, transaction.network.dust_amount,
                                                input_key_id, account_id, network, min_confirms, max_utxos, False)
            if not selected_utxos:
                raise WalletError("Not enough unspent transaction outputs found")
            for utxo in selected_utxos:
                amount_total_input += utxo['value']
                # inp_keys, key = self._objects_by_key_id(utxo.key_id)
                ## I THINK HERE WE HAVE LIST UTXO TRANSFORMED INTO INPUT TYPE WHICH MIGHT HAVE ALL NEEDED ATTRIBUTES
                ## PLEASE CHECK IF IT IS CORRECT!
                inp_keys = [self.hdkey]
                address = Address.parse(address=utxo['address'])
                multisig = False if isinstance(inp_keys, list) and len(inp_keys) < 2 else True
                key_path = ''
                unlock_script_type = get_unlocking_script_type(address.script_type, self.witness_type, multisig=multisig)
                # transaction.add_input(utxo.transaction.txid, utxo.output_n, keys=inp_keys,
                #                       script_type=unlock_script_type, sigs_required=self.multisig_n_required,
                #                       sort=self.sort_keys, compressed=key.compressed, value=utxo.value,
                #                       address=utxo.key.address, sequence=sequence,
                #                       key_path=utxo.key.path, witness_type=self.witness_type)
                transaction.add_input(utxo['txid'], utxo['output_n'], keys=inp_keys,
                                      script_type=unlock_script_type, sigs_required=self.multisig_n_required,
                                      sort=self.sort_keys, compressed=self.compressed, value=utxo['value'],
                                      address=utxo['address'], sequence=sequence,
                                      key_path=key_path, witness_type=self.witness_type)
                # FIXME: Missing locktime_cltv=locktime_cltv, locktime_csv=locktime_csv (?)
                pass
                # REFER TO THIS
                '''
                inp_keys = [self.hdkey]
                multisig = False if len(inp_keys) < 2 else True
                address = Address.parse(address=utxo['address'])
                script_type = get_unlocking_script_type(address.script_type, multisig=multisig)
                compressed = None
                network_name = network.name
                # inputs.append(Input(utxo.transaction.txid, utxo.output_n, keys=inp_keys, script_type=script_type,
                #               sigs_required=self.multisig_n_required, sort=self.sort_keys, address=key.address,
                #               compressed=key.compressed, value=utxo.value, network=key.network_name))
                inputs.append(Input(utxo['txid'], utxo['output_n'], keys=inp_keys, script_type=script_type,
                              sigs_required=self.multisig_n_required, sort=self.sort_keys, address=utxo['address'],
                              compressed=compressed, value=utxo['value'], network=network_name))
                '''
        # TEMPORARY BANNED
        else:
            raise Exception("ELSE ALERT!")
        '''
        else:
            for inp in input_arr:
                locktime_cltv = None
                locktime_csv = None
                unlocking_script_unsigned = None
                unlocking_script_type = ''
                if isinstance(inp, Input):
                    prev_txid = inp.prev_txid
                    output_n = inp.output_n
                    key_id = None
                    value = inp.value
                    signatures = inp.signatures
                    unlocking_script = inp.unlocking_script
                    unlocking_script_unsigned = inp.unlocking_script_unsigned
                    unlocking_script_type = inp.script_type
                    address = inp.address
                    sequence = inp.sequence
                    locktime_cltv = inp.locktime_cltv
                    locktime_csv = inp.locktime_csv
                # elif isinstance(inp, DbTransactionOutput):
                #     prev_txid = inp.transaction.txid
                #     output_n = inp.output_n
                #     key_id = inp.key_id
                #     value = inp.value
                #     signatures = None
                #     # FIXME: This is probably not an unlocking_script
                #     unlocking_script = inp.script
                #     unlocking_script_type = get_unlocking_script_type(inp.script_type)
                #     address = inp.key.address
                else:
                    prev_txid = inp[0]
                    output_n = inp[1]
                    key_id = None if len(inp) <= 2 else inp[2]
                    value = 0 if len(inp) <= 3 else inp[3]
                    signatures = None if len(inp) <= 4 else inp[4]
                    unlocking_script = b'' if len(inp) <= 5 else inp[5]
                    address = '' if len(inp) <= 6 else inp[6]
                # Get key_ids, value from Db if not specified
                if not (key_id and value and unlocking_script_type):
                    if not isinstance(output_n, TYPE_INT):
                        output_n = int.from_bytes(output_n, 'big')
                    inp_utxo = self._session.query(DbTransactionOutput).join(DbTransaction). \
                        filter(DbTransaction.wallet_id == self.wallet_id,
                               DbTransaction.txid == to_bytes(prev_txid),
                               DbTransactionOutput.output_n == output_n).first()
                    if inp_utxo:
                        key_id = inp_utxo.key_id
                        value = inp_utxo.value
                        address = inp_utxo.key.address
                        unlocking_script_type = get_unlocking_script_type(inp_utxo.script_type, multisig=self.multisig)
                        # witness_type = inp_utxo.witness_type
                    else:
                        _logger.info("UTXO %s not found in this wallet. Please update UTXO's if this is not an "
                                     "offline wallet" % to_hexstring(prev_txid))
                        key_id = self._session.query(DbKey.id).\
                            filter(DbKey.wallet_id == self.wallet_id, DbKey.address == address).scalar()
                        if not key_id:
                            raise WalletError("UTXO %s and key with address %s not found in this wallet" % (
                                to_hexstring(prev_txid), address))
                        if not value:
                            raise WalletError("Input value is zero for address %s. Import or update UTXO's first "
                                              "or import transaction as dictionary" % address)

                amount_total_input += value
                inp_keys, key = self._objects_by_key_id(key_id)
                transaction.add_input(prev_txid, output_n, keys=inp_keys, script_type=unlocking_script_type,
                                      sigs_required=self.multisig_n_required, sort=self.sort_keys,
                                      compressed=key.compressed, value=value, signatures=signatures,
                                      unlocking_script=unlocking_script, address=address,
                                      unlocking_script_unsigned=unlocking_script_unsigned,
                                      sequence=sequence, locktime_cltv=locktime_cltv, locktime_csv=locktime_csv,
                                      witness_type=self.witness_type, key_path=key.path)
        '''
        # Calculate fees
        transaction.fee = fee
        fee_per_output = None
        transaction.size = transaction.estimate_size(number_of_change_outputs=number_of_change_outputs)
        if fee is None:
            if not input_arr:
                if not transaction.fee_per_kb:
                    transaction.fee_per_kb = srv.estimatefee()
                if transaction.fee_per_kb < transaction.network.fee_min:
                    transaction.fee_per_kb = transaction.network.fee_min
                transaction.fee = int((transaction.size / 1000.0) * transaction.fee_per_kb)
                fee_per_output = int((50 / 1000.0) * transaction.fee_per_kb)
            else:
                if amount_total_output and amount_total_input:
                    fee = False
                else:
                    transaction.fee = 0

        if fee is False:
            transaction.change = 0
            transaction.fee = int(amount_total_input - amount_total_output)
        else:
            transaction.change = int(amount_total_input - (amount_total_output + transaction.fee))

        # Skip change if amount is smaller than the dust limit or estimated fee
        if (fee_per_output and transaction.change < fee_per_output) or transaction.change <= transaction.network.dust_amount:
            transaction.fee += transaction.change
            transaction.change = 0
        if transaction.change < 0:
            raise WalletError("Total amount of outputs is greater then total amount of inputs")
        if transaction.change:
            min_output_value = transaction.network.dust_amount * 2 + transaction.network.fee_min * 4
            if transaction.fee and transaction.size:
                if not transaction.fee_per_kb:
                    transaction.fee_per_kb = int((transaction.fee * 1000.0) / transaction.vsize)
                min_output_value = transaction.fee_per_kb + transaction.network.fee_min * 4 + \
                                   transaction.network.dust_amount

            if number_of_change_outputs == 0:
                if transaction.change < amount_total_output / 10 or transaction.change < min_output_value * 8:
                    number_of_change_outputs = 1
                elif transaction.change / 10 > amount_total_output:
                    number_of_change_outputs = random.randint(2, 5)
                else:
                    number_of_change_outputs = random.randint(1, 3)
                    # Prefer 1 and 2 as number of change outputs
                    if number_of_change_outputs == 3:
                        number_of_change_outputs = random.randint(3, 4)
                transaction.size = transaction.estimate_size(number_of_change_outputs=number_of_change_outputs)

            average_change = transaction.change // number_of_change_outputs
            if number_of_change_outputs > 1 and average_change < min_output_value:
                raise WalletError("Not enough funds to create multiple change outputs. Try less change outputs "
                                  "or lower fees")

            # if self.scheme == 'single':
            #     change_keys = [self.get_key(account_id=account_id, network=network, change=1)]
            # else:
            #     change_keys = self.get_keys(account_id=account_id, network=network, change=1,
            #                                 number_of_keys=number_of_change_outputs)
            change_keys = [self.hdkey]

            if number_of_change_outputs > 1:
                rand_prop = transaction.change - number_of_change_outputs * min_output_value
                change_amounts = list(((np.random.dirichlet(np.ones(number_of_change_outputs), size=1)[0] *
                                        rand_prop) + min_output_value).astype(int))
                # Fix rounding problems / small amount differences
                diffs = transaction.change - sum(change_amounts)
                for idx, co in enumerate(change_amounts):
                    if co - diffs > min_output_value:
                        change_amounts[idx] += change_amounts.index(co) + diffs
                        break
            else:
                change_amounts = [transaction.change]

            for idx, ck in enumerate(change_keys):
                on = transaction.add_output(change_amounts[idx], ck.address(), encoding=self.encoding)
                # transaction.outputs[on].key_id = ck.key_id

        # Shuffle output order to increase privacy
        if random_output_order:
            transaction.shuffle()

        # Check tx values
        transaction.input_total = sum([i.value for i in transaction.inputs])
        transaction.output_total = sum([o.value for o in transaction.outputs])
        if transaction.input_total != transaction.fee + transaction.output_total:
            raise WalletError("Sum of inputs values is not equal to sum of outputs values plus fees")

        transaction.txid = transaction.signature_hash()[::-1].hex()
        if not transaction.fee_per_kb:
            transaction.fee_per_kb = int((transaction.fee * 1000.0) / transaction.vsize)
        if transaction.fee_per_kb < transaction.network.fee_min:
            raise WalletError("Fee per kB of %d is lower then minimal network fee of %d" %
                              (transaction.fee_per_kb, transaction.network.fee_min))
        elif transaction.fee_per_kb > transaction.network.fee_max:
            raise WalletError("Fee per kB of %d is higher then maximum network fee of %d" %
                              (transaction.fee_per_kb, transaction.network.fee_max))

        return transaction
    def select_inputs(self, amount, variance=None, input_key_id=None, account_id=None, network=None, min_confirms=1,
                      max_utxos=MAX_TRANSACTIONS, return_input_obj=True, skip_dust_amounts=True):
        """
        Select available unspent transaction outputs (UTXO's) which can be used as inputs for a transaction for
        the specified amount.

        >>> w = Wallet('bitcoinlib_legacy_wallet_test')
        >>> w.select_inputs(50000000)
        [<Input(prev_txid='748799c9047321cb27a6320a827f1f69d767fe889c14bf11f27549638d566fe4', output_n=0, address='16QaHuFkfuebXGcYHmehRXBBX7RG9NbtLg', index_n=0, type='sig_pubkey')>]

        :param amount: Total value of inputs in the smallest denominator (sathosi) to select
        :type amount: int
        :param variance: Allowed difference in total input value. Default is dust amount of selected network. Difference will be added to transaction fee.
        :type variance: int
        :param input_key_id: Limit UTXO's search for inputs to this key ID or list of key IDs. Only valid if no input array is specified
        :type input_key_id: int, list
        :param account_id: Account ID
        :type account_id: int
        :param network: Network name. Leave empty for default network
        :type network: str
        :param min_confirms: Minimal confirmation needed for an UTXO before it will be included in inputs. Default is 1 confirmation. Option is ignored if input_arr is provided.
        :type min_confirms: int
        :param max_utxos: Maximum number of UTXO's to use. Set to 1 for optimal privacy. Default is None: No maximum
        :type max_utxos: int
        :param return_input_obj: Return inputs as Input class object. Default is True
        :type return_input_obj: bool
        :param skip_dust_amounts: Do not include small amount to avoid dust inputs
        :type skip_dust_amounts: bool

        :return: List of previous outputs
        :rtype: list of DbTransactionOutput, list of Input
        """

        # network, account_id, _ = self._get_account_defaults(network, account_id)
        network = DEFAULT_NETWORK
        dust_amount = Network(network).dust_amount
        if variance is None:
            variance = dust_amount

        # utxo_query = self._session.query(DbTransactionOutput).join(DbTransaction).join(DbKey). \
        #     filter(DbTransaction.wallet_id == self.wallet_id, DbTransaction.account_id == account_id,
        #            DbTransaction.network_name == network, DbKey.public != b'',
        #            DbTransactionOutput.spent.is_(False), DbTransaction.confirmations >= min_confirms)
        # if input_key_id:
        #     if isinstance(input_key_id, int):
        #         utxo_query = utxo_query.filter(DbKey.id == input_key_id)
        #     else:
        #         utxo_query = utxo_query.filter(DbKey.id.in_(input_key_id))

        srv = Service(network=network, providers=self.providers, cache_uri=self.db_cache_uri)
        last_txid = ''

        utxos = [x for x in srv.getutxos(self.address, after_txid=last_txid, limit=max_utxos) if
                 x['confirmations'] >= min_confirms]

        utxos_vmask = numpy.argsort([x['value'] for x in utxos])
        utxos = [utxos[j] for j in utxos_vmask]
        utxos.reverse()

        if skip_dust_amounts:
            # utxo_query = utxo_query.filter(DbTransactionOutput.value > dust_amount)
            utxos = [x for x in utxos if x['value'] > dust_amount]

        # utxos = utxo_query.order_by(DbTransaction.confirmations.desc()).all()

        if not utxos:
            raise WalletError("Create transaction: No unspent transaction outputs found or no key available for UTXO's")

        # TODO: Find 1 or 2 UTXO's with exact amount +/- self.network.dust_amount

        # Try to find one utxo with exact amount
        # one_utxo = utxo_query.filter(DbTransactionOutput.spent.is_(False),
        #                              DbTransactionOutput.value >= amount,
        #                              DbTransactionOutput.value <= amount + variance).first()

        one_utxo = [u for u in utxos if (u['value'] >= amount) and (u['value'] <= amount + variance)]

        selected_utxos = []
        if one_utxo:
            # selected_utxos = [one_utxo]

            selected_utxos = [one_utxo[0]]

        else:
            # Try to find one utxo with higher amount
            # one_utxo = utxo_query. \
            #     filter(DbTransactionOutput.spent.is_(False), DbTransactionOutput.value >= amount).\
            #     order_by(DbTransactionOutput.value).first()

            one_utxo = [u for u in utxos if (u['value'] >= amount)]

            if one_utxo:
                # selected_utxos = [one_utxo]
                selected_utxos = [one_utxo[0]]

            elif max_utxos and max_utxos <= 1:
                print("No single UTXO found with requested amount, use higher 'max_utxo' setting to use "
                      "multiple UTXO's")
                return []

        # Otherwise compose of 2 or more lesser outputs
        if not selected_utxos:
            # lessers = utxo_query. \
            #     filter(DbTransactionOutput.spent.is_(False), DbTransactionOutput.value < amount).\
            #     order_by(DbTransactionOutput.value.desc()).all()
            lessers = [u for u in utxos if (u['value'] < amount)]

            total_amount = 0
            selected_utxos = []
            for utxo in lessers[:max_utxos]:
                if total_amount < amount:
                    selected_utxos.append(utxo)
                    # total_amount += utxo.value
                    total_amount += utxo['value']
            if total_amount < amount:
                return []
        if not return_input_obj:
            return selected_utxos
        else:
            inputs = []
            for utxo in selected_utxos:
                # amount_total_input += utxo.value
                # inp_keys, key = self._objects_by_key_id(utxo.key_id)
                inp_keys = [self.hdkey]
                multisig = False if len(inp_keys) < 2 else True
                address = Address.parse(address=utxo['address'])
                script_type = get_unlocking_script_type(address.script_type, multisig=multisig)
                compressed = None
                network_name = network.name
                # inputs.append(Input(utxo.transaction.txid, utxo.output_n, keys=inp_keys, script_type=script_type,
                #               sigs_required=self.multisig_n_required, sort=self.sort_keys, address=key.address,
                #               compressed=key.compressed, value=utxo.value, network=key.network_name))
                inputs.append(Input(utxo['txid'], utxo['output_n'], keys=inp_keys, script_type=script_type,
                              sigs_required=self.multisig_n_required, sort=self.sort_keys, address=utxo['address'],
                              compressed=compressed, value=utxo['value'], network=network_name))
            return inputs


class Transaction(object):
    """
    Transaction Class

    Contains 1 or more Input class object with UTXO's to spent and 1 or more Output class objects with destinations.
    Besides the transaction class contains a locktime and version.

    Inputs and outputs can be included when creating the transaction, or can be added later with add_input and
    add_output respectively.

    A verify method is available to check if the transaction Inputs have valid unlocking scripts.

    Each input in the transaction can be signed with the sign method provided a valid private key.
    """

    def __init__(self, inputs=None, outputs=None, locktime=0, version=None,
                 network=DEFAULT_NETWORK, fee=None, fee_per_kb=None, size=None, txid='', txhash='', date=None,
                 confirmations=None, block_height=None, block_hash=None, input_total=0, output_total=0, rawtx=b'',
                 status='new', coinbase=False, verified=False, witness_type='legacy', flag=None):
        """
        Create a new transaction class with provided inputs and outputs.

        You can also create an empty transaction and add input and outputs later.

        To verify and sign transactions all inputs and outputs need to be included in transaction. Any modification
        after signing makes the transaction invalid.

        :param inputs: Array of Input objects. Leave empty to add later
        :type inputs: list (Input)
        :param outputs: Array of Output object. Leave empty to add later
        :type outputs: list (Output)
        :param locktime: Transaction level locktime. Locks the transaction until a specified block (value from 1 to 5 million) or until a certain time (Timestamp in seconds after 1-jan-1970). Default value is 0 for transactions without locktime
        :type locktime: int
        :param version: Version rules. Defaults to 1 in bytes
        :type version: bytes, int
        :param network: Network, leave empty for default network
        :type network: str, Network
        :param fee: Fee in smallest denominator (ie Satoshi) for complete transaction
        :type fee: int
        :param fee_per_kb: Fee in smallest denominator per kilobyte. Specify when exact transaction size is not known.
        :type fee_per_kb: int
        :param size: Transaction size in bytes
        :type size: int
        :param txid: The transaction id (same for legacy/segwit) based on [nVersion][txins][txouts][nLockTime as hexadecimal string
        :type txid: str
        :param txhash: The transaction hash (differs from txid for witness transactions), based on [nVersion][marker][flag][txins][txouts][witness][nLockTime] in Segwit (as hexadecimal string). Unused at the moment
        :type txhash: str
        :param date: Confirmation date of transaction
        :type date: datetime
        :param confirmations: Number of confirmations
        :type confirmations: int
        :param block_height: Block number which includes transaction
        :type block_height: int
        :param block_hash: Hash of block for this transaction
        :type block_hash: str
        :param input_total: Total value of inputs
        :type input_total: int
        :param output_total: Total value of outputs
        :type output_total: int
        :param rawtx: Bytes representation of complete transaction
        :type rawtx: bytes
        :param status: Transaction status, for example: 'new', 'unconfirmed', 'confirmed'
        :type status: str
        :param coinbase: Coinbase transaction or not?
        :type coinbase: bool
        :param verified: Is transaction successfully verified? Updated when verified() method is called
        :type verified: bool
        :param witness_type: Specify witness/signature position: 'segwit' or 'legacy'. Determine from script, address or encoding if not specified.
        :type witness_type: str
        :param flag: Transaction flag to indicate version, for example for SegWit
        :type flag: bytes, str

        """

        self.coinbase = coinbase
        self.inputs = []
        if inputs is not None:
            for inp in inputs:
                self.inputs.append(inp)
            if not input_total:
                input_total = sum([i.value for i in inputs])
        id_list = [i.index_n for i in self.inputs]
        if list(dict.fromkeys(id_list)) != id_list:
            print("Identical transaction indexes (tid) found in inputs, please specify unique index. "
                  "Indexes will be automatically recreated")
            index_n = 0
            for inp in self.inputs:
                inp.index_n = index_n
                index_n += 1
        if outputs is None:
            self.outputs = []
        else:
            self.outputs = outputs
            if not output_total:
                output_total = sum([o.value for o in outputs])
        if fee is None and output_total and input_total:
            fee = input_total - output_total
            if fee < 0 or fee == 0 and not self.coinbase:
                raise TransactionError("Transaction inputs total value must be greater then total value of "
                                       "transaction outputs")
        if not version:
            version = b'\x00\x00\x00\x01'
        if isinstance(version, int):
            self.version = version.to_bytes(4, 'big')
            self.version_int = version
        else:
            self.version = version
            self.version_int = int.from_bytes(version, 'big')
        self.locktime = locktime
        self.network = network
        if not isinstance(network, Network):
            self.network = Network(network)
        self.flag = flag
        self.fee = fee
        self.fee_per_kb = fee_per_kb
        self.size = size
        self.vsize = size
        self.txid = txid
        self.txhash = txhash
        self.date = date
        self.confirmations = confirmations
        self.block_height = block_height
        self.block_hash = block_hash
        self.input_total = input_total
        self.output_total = output_total
        self.rawtx = rawtx
        self.status = status
        self.verified = verified
        self.witness_type = witness_type
        self.change = 0
        self.calc_weight_units()
        # if self.witness_type not in ['legacy', 'segwit']:
        if self.witness_type not in ['legacy', 'segwit', 'taproot']:
            raise TransactionError("Please specify a valid witness type: legacy or segwit")
        if not self.txid:
            self.txid = self.signature_hash()[::-1].hex()
    def calc_weight_units(self):
        """
        Calculate weight units and vsize for this Transaction. Weight units are used to determine fee.

        :return int:
        """
        if not self.size:
            return None
        witness_data_size = len(self.witness_data())
        wu = self.size * 4
        if self.witness_type == 'segwit' and witness_data_size > 1:
            wu = wu - 6  # for segwit marker and flag
            wu = wu - witness_data_size * 3
        self.vsize = math.ceil(wu / 4)
        return wu
    def witness_data(self):
        """
        Get witness data for all inputs of this transaction

        :return bytes:
        """
        witness_data = b''
        for i in self.inputs:
            witness_data += int_to_varbyteint(len(i.witnesses)) + b''.join([bytes(varstr(w)) for w in i.witnesses])
        return witness_data
    def signature_hash(self, sign_id=None, hash_type=SIGHASH_ALL, witness_type=None, as_hex=False):
        """
        Double SHA256 Hash of Transaction signature

        :param sign_id: Index of input to sign
        :type sign_id: int
        :param hash_type: Specific hash type, default is SIGHASH_ALL
        :type hash_type: int
        :param witness_type: Legacy or Segwit witness type? Leave empty to use Transaction witness type
        :type witness_type: str
        :param as_hex: Return value as hexadecimal string. Default is False
        :type as_hex: bool

        :return bytes: Transaction signature hash
        """
        return double_sha256(self.signature(sign_id, hash_type, witness_type), as_hex=as_hex)
    def signature(self, sign_id=None, hash_type=SIGHASH_ALL, witness_type=None):
        """
        Serializes transaction and calculates signature for Legacy or Segwit transactions

        :param sign_id: Index of input to sign
        :type sign_id: int
        :param hash_type: Specific hash type, default is SIGHASH_ALL
        :type hash_type: int
        :param witness_type: Legacy or Segwit witness type? Leave empty to use Transaction witness type
        :type witness_type: str

        :return bytes: Transaction signature
        """

        if witness_type is None:
            witness_type = self.witness_type
        if witness_type == 'legacy' or sign_id is None:
            return self.raw(sign_id, hash_type, 'legacy')
        elif witness_type in ['segwit', 'p2sh-segwit']:
            return self.signature_segwit(sign_id, hash_type)
        else:
            raise TransactionError("Witness_type %s not supported" % self.witness_type)
    def raw(self, sign_id=None, hash_type=SIGHASH_ALL, witness_type=None):
        """
        Serialize raw transaction

        Return transaction with signed inputs if signatures are available

        :param sign_id: Create raw transaction which can be signed by transaction with this input ID
        :type sign_id: int, None
        :param hash_type: Specific hash type, default is SIGHASH_ALL
        :type hash_type: int
        :param witness_type: Serialize transaction with other witness type then default. Use to create legacy raw transaction for segwit transaction to create transaction signature ID's
        :type witness_type: str

        :return bytes:
        """

        if witness_type is None:
            witness_type = self.witness_type

        r = self.version[::-1]
        if sign_id is None and witness_type == 'segwit':
            r += b'\x00'  # marker (BIP 141)
            r += b'\x01'  # flag (BIP 141)

        r += int_to_varbyteint(len(self.inputs))
        r_witness = b''
        for i in self.inputs:
            r += i.prev_txid[::-1] + i.output_n[::-1]
            if i.witnesses and i.witness_type != 'legacy':
                r_witness += int_to_varbyteint(len(i.witnesses)) + b''.join([bytes(varstr(w)) for w in i.witnesses])
            else:
                r_witness += b'\0'
            if sign_id is None:
                r += varstr(i.unlocking_script)
            elif sign_id == i.index_n:
                r += varstr(i.unlocking_script_unsigned)
            else:
                r += b'\0'
            r += i.sequence.to_bytes(4, 'little')

        r += int_to_varbyteint(len(self.outputs))
        for o in self.outputs:
            if o.value < 0:
                raise TransactionError("Output value < 0 not allowed")
            r += int(o.value).to_bytes(8, 'little')
            r += varstr(o.lock_script)

        if sign_id is None and witness_type == 'segwit':
            r += r_witness

        r += self.locktime.to_bytes(4, 'little')
        if sign_id is not None:
            r += hash_type.to_bytes(4, 'little')
        else:
            if not self.size and b'' not in [i.unlocking_script for i in self.inputs]:
                self.size = len(r)
                self.calc_weight_units()
        return r
    def signature_segwit(self, sign_id, hash_type=SIGHASH_ALL):
        """
        Serialize transaction signature for segregated witness transaction

        :param sign_id: Index of input to sign
        :type sign_id: int
        :param hash_type: Specific hash type, default is SIGHASH_ALL
        :type hash_type: int

        :return bytes: Segwit transaction signature
        """
        assert (self.witness_type == 'segwit')
        prevouts_serialized = b''
        sequence_serialized = b''
        outputs_serialized = b''
        hash_prevouts = b'\0' * 32
        hash_sequence = b'\0' * 32
        hash_outputs = b'\0' * 32

        for i in self.inputs:
            prevouts_serialized += i.prev_txid[::-1] + i.output_n[::-1]
            sequence_serialized += i.sequence.to_bytes(4, 'little')
        if not hash_type & SIGHASH_ANYONECANPAY:
            hash_prevouts = double_sha256(prevouts_serialized)
            if (hash_type & 0x1f) != SIGHASH_SINGLE and (hash_type & 0x1f) != SIGHASH_NONE:
                hash_sequence = double_sha256(sequence_serialized)
        if (hash_type & 0x1f) != SIGHASH_SINGLE and (hash_type & 0x1f) != SIGHASH_NONE:
            for o in self.outputs:
                outputs_serialized += int(o.value).to_bytes(8, 'little')
                outputs_serialized += varstr(o.lock_script)
            hash_outputs = double_sha256(outputs_serialized)
        elif (hash_type & 0x1f) != SIGHASH_SINGLE and sign_id < len(self.outputs):
            outputs_serialized += int(self.outputs[sign_id].value).to_bytes(8, 'little')
            outputs_serialized += varstr(self.outputs[sign_id].lock_script)
            hash_outputs = double_sha256(outputs_serialized)

        is_coinbase = self.inputs[sign_id].script_type == 'coinbase'
        if not self.inputs[sign_id].value and not is_coinbase:
            raise TransactionError("Need value of input %d to create transaction signature, value can not be 0" %
                                   sign_id)

        if not self.inputs[sign_id].redeemscript:
            self.inputs[sign_id].redeemscript = self.inputs[sign_id].script_code

        if (not self.inputs[sign_id].redeemscript or self.inputs[sign_id].redeemscript == b'\0') and \
                self.inputs[sign_id].redeemscript != 'unknown' and not is_coinbase:
            raise TransactionError("Redeem script missing")

        ser_tx = \
            self.version[::-1] + hash_prevouts + hash_sequence + self.inputs[sign_id].prev_txid[::-1] + \
            self.inputs[sign_id].output_n[::-1] + \
            varstr(self.inputs[sign_id].redeemscript) + int(self.inputs[sign_id].value).to_bytes(8, 'little') + \
            self.inputs[sign_id].sequence.to_bytes(4, 'little') + \
            hash_outputs + self.locktime.to_bytes(4, 'little') + hash_type.to_bytes(4, 'little')
        return ser_tx
    def add_output(self, value, address='', public_hash=b'', public_key=b'', lock_script=b'', spent=False,
                   output_n=None, encoding=None, spending_txid=None, spending_index_n=None, strict=True):
        """
        Add an output to this transaction

        Wrapper for the append method of the Output class.

        :param value: Value of output in the smallest denominator of currency, for example satoshi's for bitcoins
        :type value: int
        :param address: Destination address of output. Leave empty to derive from other attributes you provide.
        :type address: str, Address
        :param public_hash: Hash of public key or script
        :type public_hash: bytes, str
        :param public_key: Destination public key
        :type public_key: bytes, str
        :param lock_script: Locking script of output. If not provided a default unlocking script will be provided with a public key hash.
        :type lock_script: bytes, str
        :param spent: Has output been spent in new transaction?
        :type spent: bool, None
        :param output_n: Index number of output in transaction
        :type output_n: int
        :param encoding: Address encoding used. For example bech32/base32 or base58. Leave empty for to derive from script or script type
        :type encoding: str
        :param spending_txid: Transaction hash of input spending this transaction output
        :type spending_txid: str
        :param spending_index_n: Index number of input spending this transaction output
        :type spending_index_n: int
        :param strict: Raise exception when output is malformed or incomplete
        :type strict: bool

        :return int: Transaction output number (output_n)
        """

        lock_script = to_bytes(lock_script)
        if output_n is None:
            output_n = len(self.outputs)
        if not float(value).is_integer():
            raise TransactionError("Output must be of type integer and contain no decimals")
        if lock_script.startswith(b'\x6a'):
            if value != 0:
                raise TransactionError("Output value for OP_RETURN script must be 0")
        self.outputs.append(Output(value=int(value), address=address, public_hash=public_hash,
                                   public_key=public_key, lock_script=lock_script, spent=spent, output_n=output_n,
                                   encoding=encoding, spending_txid=spending_txid, spending_index_n=spending_index_n,
                                   strict=strict, network=self.network.name))
        return output_n
    def estimate_size(self, number_of_change_outputs=0):
        """
        Get estimated vsize in for current transaction based on transaction type and number of inputs and outputs.

        For old-style legacy transaction the vsize is the length of the transaction. In segwit transaction the
        witness data has less weight. The formula used is: math.ceil(((est_size-witness_size) * 3 + est_size) / 4)

        :param number_of_change_outputs: Number of change outputs, default is 0
        :type number_of_change_outputs: int

        :return int: Estimated transaction size
        """

        # if self.input_total and self.output_total + self.fee == self.input_total:
        #     add_change_output = False
        est_size = 10
        witness_size = 2
        if self.witness_type != 'legacy':
            est_size += 2
        # TODO: if no inputs assume 1 input
        if not self.inputs:
            est_size += 125
            witness_size += 72
        for inp in self.inputs:
            est_size += 40
            scr_size = 0
            if inp.witness_type != 'legacy':
                est_size += 1
            if inp.unlocking_script and len(inp.signatures) >= inp.sigs_required:
                scr_size += len(varstr(inp.unlocking_script))
                if inp.witness_type == 'p2sh-segwit':
                    scr_size += sum([1 + len(w) for w in inp.witnesses])
            else:
                if inp.script_type == 'sig_pubkey':
                    scr_size += 107
                    if not inp.compressed:
                        scr_size += 33
                    if inp.witness_type == 'p2sh-segwit':
                        scr_size += 24
                # elif inp.script_type in ['p2sh_multisig', 'p2sh_p2wpkh', 'p2sh_p2wsh']:
                elif inp.script_type == 'p2sh_multisig':
                    scr_size += 9 + (len(inp.keys) * 34) + (inp.sigs_required * 72)
                    if inp.witness_type == 'p2sh-segwit':
                        scr_size += 17 * inp.sigs_required
                elif inp.script_type == 'signature':
                    scr_size += 9 + 72
                else:
                    raise TransactionError("Unknown input script type %s cannot estimate transaction size" %
                                           inp.script_type)
            est_size += scr_size
            witness_size += scr_size
        for outp in self.outputs:
            est_size += 8
            if outp.lock_script:
                est_size += len(varstr(outp.lock_script))
            else:
                raise TransactionError("Need locking script for output %d to estimate size" % outp.output_n)
        if number_of_change_outputs:
            is_multisig = True if self.inputs and self.inputs[0].script_type == 'p2sh_multisig' else False
            co_size = 8
            if not self.inputs or self.inputs[0].witness_type == 'legacy':
                co_size += 24 if is_multisig else 26
            elif self.inputs[0].witness_type == 'p2sh-segwit':
                co_size += 24
            else:
                co_size += 33 if is_multisig else 23
            est_size += (number_of_change_outputs * co_size)
        self.size = est_size
        self.vsize = est_size
        if self.witness_type == 'legacy':
            return est_size
        else:
            self.vsize = math.ceil((((est_size - witness_size) * 3 + est_size) / 4) - 1.5)
            return self.vsize
    def add_input(self, prev_txid, output_n, keys=None, signatures=None, public_hash=b'', unlocking_script=b'',
                  unlocking_script_unsigned=None, script_type=None, address='',
                  sequence=0xffffffff, compressed=True, sigs_required=None, sort=False, index_n=None,
                  value=None, double_spend=False, locktime_cltv=None, locktime_csv=None,
                  key_path='', witness_type=None, witnesses=None, encoding=None, strict=True):
        """
        Add input to this transaction

        Wrapper for append method of Input class.

        :param prev_txid: Transaction hash of the UTXO (previous output) which will be spent.
        :type prev_txid: bytes, hexstring
        :param output_n: Output number in previous transaction.
        :type output_n: bytes, int
        :param keys: Public keys can be provided to construct an Unlocking script. Optional
        :type keys: bytes, str
        :param signatures: Add signatures to input if already known
        :type signatures: bytes, str
        :param public_hash: Specify public hash from key or redeemscript if key is not available
        :type public_hash: bytes
        :param unlocking_script: Unlocking script (scriptSig) to prove ownership. Optional
        :type unlocking_script: bytes, hexstring
        :param unlocking_script_unsigned: TODO: find better name...
        :type unlocking_script_unsigned: bytes, str
        :param script_type: Type of unlocking script used, i.e. p2pkh or p2sh_multisig. Default is p2pkh
        :type script_type: str
        :param address: Specify address of input if known, default is to derive from key or scripts
        :type address: str, Address
        :param sequence: Sequence part of input, used for timelocked transactions
        :type sequence: int, bytes
        :param compressed: Use compressed or uncompressed public keys. Default is compressed
        :type compressed: bool
        :param sigs_required: Number of signatures required for a p2sh_multisig unlocking script
        :param sigs_required: int
        :param sort: Sort public keys according to BIP0045 standard. Default is False to avoid unexpected change of key order.
        :type sort: boolean
        :param index_n: Index number of position in transaction, leave empty to add input to end of inputs list
        :type index_n: int
        :param value: Value of input
        :type value: int
        :param double_spend: True if double spend is detected, depends on which service provider is selected
        :type double_spend: bool
        :param locktime_cltv: Check Lock Time Verify value. Script level absolute time lock for this input
        :type locktime_cltv: int
        :param locktime_csv: Check Sequency Verify value.
        :type locktime_csv: int
        :param key_path: Key path of input key as BIP32 string or list
        :type key_path: str, list
        :param witness_type: Specify witness/signature position: 'segwit' or 'legacy'. Determine from script, address or encoding if not specified.
        :type witness_type: str
        :param witnesses: List of witnesses for inputs, used for segwit transactions for instance.
        :type witnesses: list of bytes, list of str
        :param encoding: Address encoding used. For example bech32/base32 or base58. Leave empty to derive from script or script type
        :type encoding: str
        :param strict: Raise exception when input is malformed or incomplete
        :type strict: bool

        :return int: Transaction index number (index_n)
        """

        if index_n is None:
            index_n = len(self.inputs)
        sequence_int = sequence
        if isinstance(sequence, bytes):
            sequence_int = int.from_bytes(sequence, 'little')
        if self.version == b'\x00\x00\x00\x01' and 0 < sequence_int < SEQUENCE_LOCKTIME_DISABLE_FLAG:
            self.version = b'\x00\x00\x00\x02'
            self.version_int = 2
        if witness_type is None:
            witness_type = self.witness_type
        self.inputs.append(
            Input(prev_txid=prev_txid, output_n=output_n, keys=keys, signatures=signatures, public_hash=public_hash,
                  unlocking_script=unlocking_script, unlocking_script_unsigned=unlocking_script_unsigned,
                  script_type=script_type, address=address, sequence=sequence, compressed=compressed,
                  sigs_required=sigs_required, sort=sort, index_n=index_n, value=value, double_spend=double_spend,
                  locktime_cltv=locktime_cltv, locktime_csv=locktime_csv, key_path=key_path, witness_type=witness_type,
                  witnesses=witnesses, encoding=encoding, strict=strict, network=self.network.name))
        return index_n
    def shuffle(self):
        """
        Shuffle transaction inputs and outputs in random order.

        :return:
        """
        self.shuffle_inputs()
        self.shuffle_outputs()
    def shuffle_inputs(self):
        """
        Shuffle transaction inputs in random order.

        :return:
        """
        random.shuffle(self.inputs)
        for idx, o in enumerate(self.inputs):
            o.index_n = idx
    def shuffle_outputs(self):
        """
        Shuffle transaction outputs in random order.

        :return:
        """
        random.shuffle(self.outputs)
        for idx, o in enumerate(self.outputs):
            o.output_n = idx
    def sign(self, keys=None, index_n=None, multisig_key_n=None, hash_type=SIGHASH_ALL, fail_on_unknown_key=True,
             replace_signatures=False):
        """
        Sign the transaction input with provided private key

        :param keys: A private key or list of private keys
        :type keys: HDKey, Key, bytes, list
        :param index_n: Index of transaction input. Leave empty to sign all inputs
        :type index_n: int
        :param multisig_key_n: Index number of key for multisig input for segwit transactions. Leave empty if not known. If not specified all possibilities will be checked
        :type multisig_key_n: int
        :param hash_type: Specific hash type, default is SIGHASH_ALL
        :type hash_type: int
        :param fail_on_unknown_key: Method fails if public key from signature is not found in public key list
        :type fail_on_unknown_key: bool
        :param replace_signatures: Replace signature with new one if already signed.
        :type replace_signatures: bool

        :return None:
        """

        if index_n is None:
            tids = range(len(self.inputs))
        else:
            tids = [index_n]

        if keys is None:
            keys = []
        elif not isinstance(keys, list):
            keys = [keys]

        for tid in tids:
            n_signs = 0
            tid_keys = [k if isinstance(k, (HDKey, Key)) else Key(k, compressed=self.inputs[tid].compressed)
                        for k in keys]
            for k in self.inputs[tid].keys:
                if k.is_private and k not in tid_keys:
                    tid_keys.append(k)
            # If input does not contain any keys, try using provided keys
            if not self.inputs[tid].keys:
                self.inputs[tid].keys = tid_keys
                self.inputs[tid].update_scripts(hash_type=hash_type)
            if self.inputs[tid].script_type == 'coinbase':
                raise TransactionError("Can not sign coinbase transactions")
            pub_key_list = [k.public_byte for k in self.inputs[tid].keys]
            n_total_sigs = len(self.inputs[tid].keys)
            sig_domain = [''] * n_total_sigs

            txid = self.signature_hash(tid, witness_type=self.inputs[tid].witness_type)
            for key in tid_keys:
                # Check if signature signs known key and is not already in list
                if key.public_byte not in pub_key_list:
                    if fail_on_unknown_key:
                        raise TransactionError("This key does not sign any known key: %s" % key.public_hex)
                    else:
                        print("This key does not sign any known key: %s" % key.public_hex)
                        continue
                if not replace_signatures and key in [x.public_key for x in self.inputs[tid].signatures]:
                    print("Key %s already signed" % key.public_hex)
                    break

                if not key.private_byte:
                    raise TransactionError("Please provide a valid private key to sign the transaction")
                sig = sign(txid, key)
                newsig_pos = pub_key_list.index(key.public_byte)
                sig_domain[newsig_pos] = sig
                n_signs += 1

            if not n_signs:
                break

            # Add already known signatures on correct position
            n_sigs_to_insert = len(self.inputs[tid].signatures)
            for sig in self.inputs[tid].signatures:
                if not sig.public_key:
                    break
                newsig_pos = pub_key_list.index(sig.public_key.public_byte)
                if sig_domain[newsig_pos] == '':
                    sig_domain[newsig_pos] = sig
                    n_sigs_to_insert -= 1
            if n_sigs_to_insert:
                for sig in self.inputs[tid].signatures:
                    free_positions = [i for i, s in enumerate(sig_domain) if s == '']
                    for pos in free_positions:
                        sig_domain[pos] = sig
                        n_sigs_to_insert -= 1
                        break
            if n_sigs_to_insert:
                print("Some signatures are replaced with the signatures of the provided keys")
            self.inputs[tid].signatures = [s for s in sig_domain if s != '']
            self.inputs[tid].update_scripts(hash_type)
    def calculate_fee(self):
        """
        Get fee for this transaction in the smallest denominator (i.e. Satoshi) based on its size and the
        transaction.fee_per_kb value

        :return int: Estimated transaction fee
        """

        if not self.fee_per_kb:
            raise TransactionError("Cannot calculate transaction fees: transaction.fee_per_kb is not set")
        if self.fee_per_kb < self.network.fee_min:
            self.fee_per_kb = self.network.fee_min
        elif self.fee_per_kb > self.network.fee_max:
            self.fee_per_kb = self.network.fee_max
        if not self.vsize:
            self.estimate_size()
        fee = int(self.vsize / 1000.0 * self.fee_per_kb)
        return fee
    def raw_hex(self, sign_id=None, hash_type=SIGHASH_ALL, witness_type=None):
        """
        Wrapper for raw() method. Return current raw transaction hex

        :param sign_id: Create raw transaction which can be signed by transaction with this input ID
        :type sign_id: int
        :param hash_type: Specific hash type, default is SIGHASH_ALL
        :type hash_type: int
        :param witness_type: Serialize transaction with other witness type then default. Use to create legacy raw transaction for segwit transaction to create transaction signature ID's
        :type witness_type: str

        :return hexstring:
        """

        return self.raw(sign_id, hash_type=hash_type, witness_type=witness_type).hex()
    def verify(self):
        """
        Verify all inputs of a transaction, check if signatures match public key.

        Does not check if UTXO is valid or has already been spent

        :return bool: True if enough signatures provided and if all signatures are valid
        """

        self.verified = False
        for inp in self.inputs:
            try:
                transaction_hash = self.signature_hash(inp.index_n, inp.hash_type, inp.witness_type)
            except TransactionError as e:
                print("Could not create transaction hash. Error: %s" % e)
                return False
            if not transaction_hash:
                print("Need at least 1 key to create segwit transaction signature")
                return False
            self.verified = inp.verify(transaction_hash)
            if not self.verified:
                return False

        self.verified = True
        return True
    def info(self):
        """
        Prints transaction information to standard output
        """

        print("Transaction %s" % self.txid)
        print("Date: %s" % self.date)
        print("Network: %s" % self.network.name)
        if self.locktime and self.locktime != 0xffffffff:
            if self.locktime < 500000000:
                print("Locktime: Until block %d" % self.locktime)
            else:
                print("Locktime: Until %s UTC" % datetime.utcfromtimestamp(self.locktime))
        print("Version: %d" % self.version_int)
        print("Witness type: %s" % self.witness_type)
        print("Status: %s" % self.status)
        print("Verified: %s" % self.verified)
        print("Inputs")
        replace_by_fee = False
        for ti in self.inputs:
            print("-", ti.address, Value.from_satoshi(ti.value, network=self.network).str(1), ti.prev_txid.hex(),
                  ti.output_n_int)
            validstr = "not validated"
            if ti.valid:
                validstr = "valid"
            elif ti.valid is False:
                validstr = "invalid"
            print("  %s %s; sigs: %d (%d-of-%d) %s" %
                  (ti.witness_type, ti.script_type, len(ti.signatures), ti.sigs_required or 0, len(ti.keys), validstr))
            if ti.sequence <= SEQUENCE_REPLACE_BY_FEE:
                replace_by_fee = True
            if ti.sequence <= SEQUENCE_LOCKTIME_DISABLE_FLAG:
                if ti.sequence & SEQUENCE_LOCKTIME_TYPE_FLAG:
                    print("  Relative timelock for %d seconds" % (512 * (ti.sequence - SEQUENCE_LOCKTIME_TYPE_FLAG)))
                else:
                    print("  Relative timelock for %d blocks" % ti.sequence)
            if ti.locktime_cltv:
                if ti.locktime_cltv & SEQUENCE_LOCKTIME_TYPE_FLAG:
                    print("  Check Locktime Verify (CLTV) for %d seconds" %
                          (512 * (ti.locktime_cltv - SEQUENCE_LOCKTIME_TYPE_FLAG)))
                else:
                    print("  Check Locktime Verify (CLTV) for %d blocks" % ti.locktime_cltv)
            if ti.locktime_csv:
                if ti.locktime_csv & SEQUENCE_LOCKTIME_TYPE_FLAG:
                    print("  Check Sequence Verify Timelock (CSV) for %d seconds" %
                          (512 * (ti.locktime_csv - SEQUENCE_LOCKTIME_TYPE_FLAG)))
                else:
                    print("  Check Sequence Verify Timelock (CSV) for %d blocks" % ti.locktime_csv)

        print("Outputs")
        for to in self.outputs:
            if to.script_type == 'nulldata':
                print("- NULLDATA ", to.lock_script[2:])
            else:
                spent_str = ''
                if to.spent:
                    spent_str = 'S'
                elif to.spent is False:
                    spent_str = 'U'
                print("-", to.address, Value.from_satoshi(to.value, network=self.network).str(1), to.script_type,
                      spent_str)
        if replace_by_fee:
            print("Replace by fee: Enabled")
        print("Size: %s" % self.size)
        print("Vsize: %s" % self.vsize)
        print("Fee: %s" % self.fee)
        print("Confirmations: %s" % self.confirmations)
        print("Block: %s" % self.block_height)


class WalletTransaction(Transaction):
    """
    Used as attribute of Wallet class. Child of Transaction object with extra reference to
    wallet and database object.

    All WalletTransaction items are stored in a database
    """

    def __init__(self, hdwallet, account_id=None, *args, **kwargs):
        """
        Initialize WalletTransaction object with reference to a Wallet object

        :param hdwallet: Wallet object, wallet name or ID
        :type hdWallet: HDwallet, str, int
        :param account_id: Account ID
        :type account_id: int
        :param args: Arguments for HDWallet parent class
        :type args: args
        :param kwargs: Keyword arguments for Wallet parent class
        :type kwargs: kwargs
        """

        # assert isinstance(hdwallet, Wallet)
        # self.hdwallet = hdwallet
        self.pushed = False
        self.error = None
        self.response_dict = None
        self.account_id = account_id
        # if not account_id:
        #     self.account_id = self.hdwallet.default_account_id
        self.account_id = None
        witness_type = 'legacy'
        if hdwallet.witness_type in ['segwit', 'p2sh-segwit']:
            witness_type = 'segwit'
        if hdwallet.witness_type in ['taproot']:
            witness_type = 'taproot'
        Transaction.__init__(self, witness_type=witness_type, *args, **kwargs)
        addresslist = hdwallet.addresslist()
        self.outgoing_tx = bool([i.address for i in self.inputs if i.address in addresslist])
        self.incoming_tx = bool([o.address for o in self.outputs if o.address in addresslist])
    def sign(self, keys=None, index_n=0, multisig_key_n=None, hash_type=SIGHASH_ALL, fail_on_unknown_key=False,
             replace_signatures=False):
        """
        Sign this transaction. Use existing keys from wallet or use keys argument for extra keys.

        :param keys: Extra private keys to sign the transaction
        :type keys: HDKey, str
        :param index_n: Transaction index_n to sign
        :type index_n: int
        :param multisig_key_n: Index number of key for multisig input for segwit transactions. Leave empty if not known. If not specified all possibilities will be checked
        :type multisig_key_n: int
        :param hash_type: Hashtype to use, default is SIGHASH_ALL
        :type hash_type: int
        :param fail_on_unknown_key: Method fails if public key from signature is not found in public key list
        :type fail_on_unknown_key: bool
        :param replace_signatures: Replace signature with new one if already signed.
        :type replace_signatures: bool

        :return None:
        """
        priv_key_list_arg = []
        if keys:
            key_paths = list(dict.fromkeys([ti.key_path for ti in self.inputs if ti.key_path[0] == 'm']))
            if not isinstance(keys, list):
                keys = [keys]
            for priv_key in keys:
                if not isinstance(priv_key, HDKey):
                    if isinstance(priv_key, str) and len(str(priv_key).split(' ')) > 4:
                        priv_key = HDKey.from_passphrase(priv_key, network=self.network)
                    else:
                        priv_key = HDKey(priv_key, network=self.network.name)
                priv_key_list_arg.append((None, priv_key))
                if key_paths and priv_key.depth == 0 and priv_key.key_type != "single":
                    for key_path in key_paths:
                        priv_key_list_arg.append((key_path, priv_key.subkey_for_path(key_path)))
        for ti in self.inputs:
            priv_key_list = []
            for (key_path, priv_key) in priv_key_list_arg:
                if (not key_path or key_path == ti.key_path) and priv_key not in priv_key_list:
                    priv_key_list.append(priv_key)
            priv_key_list += [k for k in ti.keys if k.is_private]
            Transaction.sign(self, priv_key_list, ti.index_n, multisig_key_n, hash_type, fail_on_unknown_key,
                             replace_signatures)
        self.verify()
        self.error = ""
    def send(self, offline=False):
        """
        Verify and push transaction to network. Update UTXO's in database after successful send

        :param offline: Just return the transaction object and do not send it when offline = True. Default is False
        :type offline: bool

        :return None:

        """

        self.error = None
        if not self.verified and not self.verify():
            self.error = "Cannot verify transaction"
            return None

        if offline:
            return None

        # srv = Service(network=self.network.name, providers=self.hdwallet.providers,
        #               cache_uri=self.hdwallet.db_cache_uri)
        srv = Service(network=self.network.name, providers=None,
                      cache_uri=None)
        res = srv.sendrawtransaction(self.raw_hex())
        if not res:
            self.error = "Cannot send transaction. %s" % srv.errors
            return None
        if 'txid' in res:
            print("Successfully pushed transaction, result: %s" % res)
            self.txid = res['txid']
            self.status = 'unconfirmed'
            self.confirmations = 0
            self.pushed = True
            self.response_dict = srv.results
            # self.store()

            '''
            # Update db: Update spent UTXO's, add transaction to database
            for inp in self.inputs:
                txid = inp.prev_txid
                utxos = self.hdwallet._session.query(DbTransactionOutput).join(DbTransaction).\
                    filter(DbTransaction.txid == txid,
                           DbTransactionOutput.output_n == inp.output_n_int,
                           DbTransactionOutput.spent.is_(False)).all()
                for u in utxos:
                    u.spent = True
            self.hdwallet._commit()
            self.hdwallet._balance_update(network=self.network.name)
            '''
            return None
        self.error = "Transaction not send, unknown response from service providers"
    def info(self):
        """
        Print Wallet transaction information to standard output. Include send information.
        """

        Transaction.info(self)
        print("Pushed to network: %s" % self.pushed)
        # print("Wallet: %s" % self.hdwallet.name)
        if self.error:
            print("Errors: %s" % self.error)
        print("\n")
