import pytest
from pytest_jsonreport.plugin import JSONReport

#import os
#return str(os.getcwd())

class ReportInJSON:
    """
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def json_reporter(self, target_test_path: str, save_jason_file_path: str):
        plugin = JSONReport()
        try:
            pytest.main(['--json-report-file=none', target_test_path], plugins=[plugin])
            plugin.save_report(save_jason_file_path)
            return "JSON Report created successfully"
        except Exception as err:
            return str("JSON Report Error: ", err)