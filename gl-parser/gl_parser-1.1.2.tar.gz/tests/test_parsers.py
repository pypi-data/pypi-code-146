import pytest

from gl_parser.exceptions import GLParserException
from gl_parser.parsers import parse_general_ledger


def test_parse_general_ledger(fixtures_folder, default_parser_config):
    excel_file = fixtures_folder / 'general_ledger_small.xlsx'
    parsed_results = parse_general_ledger(excel_file, default_parser_config)
    assert len(parsed_results['headers']) == 4
    assert len(parsed_results['accounts'].keys()) == 2
    for account_id, transactions in parsed_results['accounts'].items():
        for i, transaction in enumerate(transactions, 1):
            max_len = len(transactions)
            if i < max_len:
                assert transaction.account_id == account_id
            else:
                assert transaction.account_id is None


def test_parse_general_ledger_no_sheet(fixtures_folder, default_parser_config):
    excel_file = fixtures_folder / 'general_ledger_no_sheet.xlsx'
    with pytest.raises(GLParserException) as e:
        parse_general_ledger(excel_file, default_parser_config)
    assert str(e.value) == 'Sheet General Ledger not found in general_ledger_no_sheet.xlsx'


def test_parse_general_ledger_missing_columnt(fixtures_folder, default_parser_config):
    excel_file = fixtures_folder / 'general_ledger_missing_col.xlsx'
    with pytest.raises(GLParserException) as e:
        parse_general_ledger(excel_file, default_parser_config)
    error_lines = str(e.value).split('\n')
    assert len(error_lines) == 3
    assert error_lines[1] == 'description'


@pytest.mark.integration
def test_parse_general_ledger_integration(output_folder, default_parser_config):
    excel_file = output_folder / 'integration_data' / 'ITA General Ledger I.xlsx'
    parsed_results = parse_general_ledger(excel_file, default_parser_config)
    assert len(parsed_results['headers']) == 4
    assert len(parsed_results['accounts'].keys()) == 114

