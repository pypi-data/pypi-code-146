from canner.file import *
from .config import TestConfig


def test_csv_wrapper_utf8_bom():
    expected = ["統一編號", "公司名稱", "負責人", "公司地址", "實收資本額", "公司狀態", "產製日期"]
    with open(TestConfig.SAMPLE_02_UTF8_BOM_CSV, "rb") as f:
        content = f.read()
    csv_wrapper = CsvWrapper(content=content, encoding="utf-8-sig")
    csv = csv_wrapper.to_list()
    assert len(csv) > 0, "Should parse csv correctly"
    assert csv[0] == expected, "first row should be column name"


def test_csv_wrapper_mbcs():
    with open(TestConfig.SAMPLE_01_MBCS_CP950_CSV, "rb") as f:
        content = f.read()
    csv_wrapper = CsvWrapper(content=content, encoding="cp950")
    csv = csv_wrapper.to_pandas()
    assert len(csv) > 0, "Should parse csv correctly"
