import gl_parser.writers
from tests.factories import TransactionFactory


def test_write_fake_gl_file(page_headers, output_folder, default_parser_config):
    general_ledger_file = output_folder / 'general_ledger.xlsx'
    general_ledger_file.unlink(missing_ok=True)

    accounts_dict = TransactionFactory.create_parsed_accounts(5, 10)
    parsed_data = {'headers': page_headers, 'accounts': accounts_dict}

    account_count, transaction_count = gl_parser.writers.write_fake_gl_file(general_ledger_file, parsed_data,
                                                                            default_parser_config)
    assert general_ledger_file.exists()
    assert account_count == 5
    assert transaction_count == 55
