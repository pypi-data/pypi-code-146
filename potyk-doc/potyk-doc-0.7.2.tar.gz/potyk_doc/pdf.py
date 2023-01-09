import dataclasses
import io
from pathlib import Path
from typing import Dict, Union

import PyPDF2
import pdfkit

from potyk_doc.models import HTMLStr, FileData


@dataclasses.dataclass()
class WkhtmltopdfOptions:
    """
    >>> WkhtmltopdfOptions().page_width('209.804').page_height("296.926").options
    {'--page-width': '209.804', '--page-height': '296.926'}
    """
    options: Dict[str, str] = dataclasses.field(default_factory=dict)

    def add_option(self, option_name, option_val):
        return dataclasses.replace(self, options={**self.options, option_name: option_val})

    def page_width(self, page_width_mm: str):
        return self.add_option('--page-width', page_width_mm)

    def page_height(self, page_height_mm: str):
        return self.add_option('--page-height', page_height_mm)

    def footer_html(self, footer_html_path: str):
        return self.add_option("--footer-html", footer_html_path)

    def header_html(self, header_html_path: str):
        return self.add_option("--header-html", header_html_path)

    def margin_bottom(self, margin_mm: str):
        margin_mm = margin_mm if margin_mm.endswith('mm') else f'{margin_mm}mm'
        return self.add_option("margin-bottom", margin_mm)


def render_pdf_from_html(
    pdf_html: HTMLStr,
    css_path: Union[str, Path, None] = None,
    options: Union[dict, WkhtmltopdfOptions, None] = None,
) -> FileData:
    """
    Рендерит pdf из html {pdf_html}.
    Рендер происходит с помощью либы pdfkit,
    которая в свою очередь использует `wkhtmltopdf <https://wkhtmltopdf.org/>`_ (=> она должна быть установлена)

    :param pdf_html: HTML-строка
    :param css_path: (опционально) путь к css-файлу, в котором будут стили, применяемые к html перед рендерингом
    :param options: (опционально) Словарь опций wkhtmltopdf, напр. {"--page-width": "209.804"}
    :return: pdf-байты
    """
    options = options.options if isinstance(options, WkhtmltopdfOptions) else options
    pdf_data = pdfkit.from_string(pdf_html, False, css=css_path, options=options)
    return pdf_data


def pdfs_are_equal(pdf_1: bytes, pdf_2: bytes) -> bool:
    pdf_1_data = PyPDF2.PdfReader(io.BytesIO(pdf_1))
    pdf_2_data = PyPDF2.PdfReader(io.BytesIO(pdf_2))
    return (
        len(pdf_1_data.pages) == len(pdf_2_data.pages) and
        all(
            pdf_1_page.extract_text() == pdf_2_page.extract_text()
            for pdf_1_page, pdf_2_page in zip(pdf_1_data.pages, pdf_2_data.pages)
        )
    )
