from typing import Dict
from txp.common.reports.pdf_builders.pdf_builder import PDFBuilder
from txp.common.reports.pdf_builders.mock_builder import *


BUILDERS_REGISTRY: Dict[str, PDFBuilder] = {
    MockPDFBuilder.__name__: MockPDFBuilder,
}
