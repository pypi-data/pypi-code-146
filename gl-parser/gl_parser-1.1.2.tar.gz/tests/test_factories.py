from tests.factories import TransactionFactory


def test_create():
    transaction = TransactionFactory.create()
    assert transaction.debit_amount is not None


def test_create_transactions():
    transactions = TransactionFactory.create_transactions(5, 10)
    assert len(transactions) == 50 + 5


def test_create_parsed_accounts():
    transactions = TransactionFactory.create_parsed_accounts(2, 3)
    assert len(transactions.keys()) == 2
