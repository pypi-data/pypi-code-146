from fpdf import FPDF
from dataclasses import dataclass
from abc import abstractmethod

"""
    NOTE: If you create a class which inherits from PDFBuilder please add corresponding registry at
    txp.common.reports.pdf_builders.__init__.py
"""


@dataclass
class PDFBuilder:
    def __init__(self, tenant_doc, report_id, sections):
        self.tenant_doc = tenant_doc
        self.report_id = report_id
        self.sections = sections

    @abstractmethod
    def build_report_pdf(self) -> FPDF:
        pass
