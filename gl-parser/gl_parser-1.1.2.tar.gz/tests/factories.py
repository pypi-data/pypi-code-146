from decimal import Decimal
from typing import List, Any, Dict

from factory import Factory
from factory import LazyAttribute, Iterator
from factory import lazy_attribute
from faker import Factory as FakerFactory

from gl_parser.models import Transaction

faker = FakerFactory.create()
accounts = [
    'Abono y Dpositos x Identificar',
    'Account Description',
    'Adelanto de Salarios',
    'Ajustes a Periodos Anteriores',
    'Alquiler Oficina',
    'Amorti.Gastos Pagados por Adel',
    'Anulacion y Devolución Ventas,',
    'Banco General,Cuenta Corriente',
    'Bonificaciones Especiales',
    'Bonificaciones XIII Mes',
    'Caja',
    'Cargos y Gastos No Deducibles',
    'Comisiones Bancarias por TDC',
]


class TransactionFactory(Factory):
    class Meta:
        model = Transaction

    account_description = Iterator(accounts)
    date = LazyAttribute(lambda x: faker.date_between(start_date="-1y",  # type: ignore
                                                      end_date="now"))
    # date = datetime.date(2022, 1, 2)
    reference = LazyAttribute(lambda x: faker.random_int(min=1000, max=8000))
    journal = Iterator([None, 'CDJ', 'GENJ', 'Jrnl'])
    debit_amount = LazyAttribute(lambda x: faker.pydecimal(left_digits=5, right_digits=2))  # type: ignore
    credit_amount = LazyAttribute(lambda x: faker.pydecimal(left_digits=5, right_digits=2))  # type: ignore
    balance = LazyAttribute(lambda x: faker.pydecimal(left_digits=5, right_digits=2))  # type: ignore

    @lazy_attribute
    def description(self):
        name = faker.name()
        return f'Reembolso {name}'

    @lazy_attribute
    def account_id(self):
        first = faker.random_int(min=100, max=900)
        second = faker.random_int(min=0, max=99)
        third = faker.random_int(min=0, max=999)
        return f'{first}-{second}-{third}'

    @classmethod
    def create_transactions(cls, account_count: int,
                            transactions_per_account: int = 5) -> List[Transaction]:
        transactions = list()
        for _ in range(account_count):
            trx = cls.create()
            transactions.append(trx)
            trx_dup = cls.create_batch(transactions_per_account - 1, account_id=trx.account_id,
                                       account_description=trx.account_description)
            transactions.extend(trx_dup)
            balance_transaction = Transaction(date=trx.date, description='Ending balance',
                                              balance=Decimal('152.25'))
            transactions.append(balance_transaction)
        return transactions

    @classmethod
    def create_parsed_accounts(cls, account_count: int,
                               transactions_per_account: int = 5) -> Dict[str, List[Transaction]]:
        transactions = cls.create_transactions(account_count, transactions_per_account)
        parsed_accounts: Dict[str, List[Any]] = dict()
        transaction: Transaction
        previous_account_id = None
        for transaction in transactions:
            current_account_id = transaction.account_id
            if parsed_accounts.get(current_account_id) is None:  # type: ignore
                if current_account_id is not None:
                    parsed_accounts[current_account_id] = list()  # type: ignore
            if current_account_id is None:
                parsed_accounts[previous_account_id].append(transaction)  # type: ignore
            else:
                previous_account_id = current_account_id
                parsed_accounts[current_account_id].append(transaction)  # type: ignore

        return parsed_accounts
