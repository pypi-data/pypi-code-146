from pathlib import Path
from typing import Union

from django.template.loader import render_to_string
from weasyprint import HTML

from w.services.abstract_service import AbstractService
from w.services.technical.filesystem_service import FilesystemService


class PdfService(AbstractService):
    @classmethod
    def _generate(cls, content, filename=None) -> Union[None, bytes]:
        """
        Generate PDF binary data.

        Args:
            content (str|dict): message or template (as dict) :
                    {"template_name": <str>, "context": <dict> }

        Returns:
            bytes: pdf binary data
        """
        if not content:
            raise RuntimeError("Can't generate pdf binary with empty content provided")

        # html content
        if isinstance(content, dict):
            content = render_to_string(**content)
        html = HTML(string=content)
        pdf = html.write_pdf(filename)

        return pdf

    @classmethod
    def generate(cls, content) -> bytes:
        """
        Generate PDF binary data.

        Args:
            content (str|dict): message or template (as dict) :
                    {"template_name": <str>, "context": <dict> }

        Returns:
            bytes: pdf binary data
        """
        return cls._generate(content)

    @classmethod
    def write_file(cls, filename, content) -> None:
        """
        Create a PDF file.

        Args:
            filename (str): output file path
            content (str|dict): message or template (as dict) :
                {"template_name": <str>, "context": <dict> }

        Returns:
            None
        """
        FilesystemService.check_dir_exists(str(Path(filename).parent))
        return cls._generate(content, filename)
