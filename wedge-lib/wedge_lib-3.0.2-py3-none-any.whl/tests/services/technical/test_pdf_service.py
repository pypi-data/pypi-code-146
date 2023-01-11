import pytest
from django.template import TemplateDoesNotExist

from w.services.technical.pdf_service import PdfService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestPdfService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.filename = "test_pdf_service.pdf"

    """
    generate
    """

    def test_generate_with_empty_content_raise_exception(self):
        """
        Ensure pdf service raises RuntimeError exception if no content is provided
        """
        params = {
            "content": {},
        }
        match = "Can't generate pdf binary with empty content provided"
        with pytest.raises(RuntimeError, match=match):
            PdfService.generate(**params)

    def test_generate_with_unknown_template_raise_exception(self):
        """
        Ensure pdf service raises TemplateDoesNotExist exception if provided template
        is unknown
        """
        params = {
            "content": {"template_name": "unknown_template.html", "context": ""},
        }
        match = "unknown_template.html"
        with pytest.raises(TemplateDoesNotExist, match=match):
            PdfService.generate(**params)

    def test_generate_with_html_template_return_bytes(self):
        """
        Ensure pdf service returns PDF binary data built from provided html template
        """
        pdf_context = {"name": "test_name"}
        params = {
            "content": {
                "template_name": "pdf/test_pdf_service.html",
                "context": pdf_context,
            },
        }
        pdf = PdfService.generate(**params)
        assert pdf is not None and isinstance(pdf, bytes)

    def test_generate_with_html_string_return_bytes(self):
        """
        Ensure pdf service returns PDF binary data built from provided html string
        """
        params = {
            "content": "<h1>test</h1>",
        }
        pdf = PdfService.generate(**params)
        assert pdf is not None and isinstance(pdf, bytes)

    """
    write_file
    """

    def test_create_with_nonexistent_output_directory_raise_exception(self):
        """
        Ensure pdf service raises RuntimeError exception if provided output directory
        does not exist
        """
        params = {
            "filename": "/inexistent_directory/output_file.pdf",
            "content": "<h1>test</h1>",
        }
        match = "/inexistent_directory does not exist"
        with pytest.raises(RuntimeError, match=match):
            PdfService.write_file(**params)

    def test_create_with_html_string_create_file_and_return_bytes(self):
        """
        Ensure pdf service creates PDF file from provided html string and returns PDF
        binary data
        """
        self.clean_sandbox()
        params = {
            "filename": self.get_sandbox_dir(filename=self.filename),
            "content": "<h1>test</h1>",
        }
        assert PdfService.write_file(**params) is None
        self.assert_file_exists(params["filename"])
