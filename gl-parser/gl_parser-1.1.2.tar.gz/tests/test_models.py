from gl_parser.models import ParserConfig


class TestPaserConfig:

    def test_defaults(self):
        parser_config = ParserConfig()
        assert parser_config.start_row == 6
        assert parser_config.sheet_name == 'General Ledger'
