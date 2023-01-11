from txp.common.reports.pdf_builders.pdf_builder import PDFBuilder
from fpdf import FPDF


class MockPDFBuilder(PDFBuilder):

    def build_report_pdf(self) -> FPDF:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(40, 10, f"this is a report for {self.tenant_doc['tenant_id']}, report: {self.report_id}")
        return pdf
