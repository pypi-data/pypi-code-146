from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from looqbox.global_calling import GlobalCalling
from looqbox.utils.utils import random_hash
from typing import Union, Literal, List
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path
from fpdf import FPDF
import numpy as np
import sys
import os
import re


def set_font_path():
    return os.path.join(os.path.dirname(__file__), "fonts/Inter/static")


class PDFBuilder(FPDF):

    def __init__(self, user_name, user_id, logo_path, question_link):
        super().__init__(orientation='P', unit='mm', format="A4")
        user_id = str(user_id) if user_id else ""
        self.user_name = user_name + " " + user_id
        self.logo_path = logo_path
        self.question_link = question_link
        self.footer_text = f"Pergunta feita por: {self.user_name}\nEm: {datetime.today().strftime('%d/%m/%y às %H:%M:%S')}"
        self.name = GlobalCalling.looq.temp_file("result_pdf.pdf")
        self.set_margins(0, 0)

        self.font = "Inter"

        self.add_font("Inter", style="", fname=os.path.join(set_font_path(), "Inter-Regular.ttf"), uni=True)
        self.add_font("Inter", style="B", fname=os.path.join(set_font_path(), "Inter-Bold.ttf"), uni=True)

        self.set_font(self.font, '', 12)

    def header(self):
        self.image(self.logo_path, x=165, y=5, w=33)
        self.set_font(self.font, '', 12)
        self.set_text_color(37, 33, 59)
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.set_margins(5, 0)
        self.set_font(self.font, '', 8)

        self.set_text_color(135, 135, 135)

        separated_text = self.footer_text.split('\n')
        for i, text in enumerate(separated_text):
            self.cell(0, i*10, text, 0, 0, 'R')

        self.set_margins(0, 0)

    def create_watermark(self, filename, user_name):
        """
        Create a watermark for a PDF file.

        @param filename: The PDF file to add the watermark to.
        @param user_name: The watermark text.

        @return: The PDF file with the watermark.
        """
        c = canvas.Canvas(filename)
        c.translate(14.40, 14.85)
        c.rotate(30)
        c.setFillColorRGB(0.85, 0.85, 0.85)
        c.setFillAlpha(0.2)

        x_space = np.log(len(user_name)) * 50
        y_space = x_space/2
        iter_range = int(1000/y_space)

        for i in range(0, iter_range):
            for j in range(0, iter_range):
                c.drawString(i * x_space, j * y_space, user_name)
                c.drawString(i * x_space, j * -y_space, user_name)

        c.save()

    def add_image(self, image_path: str, x: int, y: int, w: int, h: int):
        """
        Add an image to the PDF document
        """
        self.add_page()
        self.ln()
        self.image(image_path, x, y, w)

    # function to add watermark to an existing PDF
    def watermark(
            self,
            content_pdf: Path,
            stamp_pdf: Path,
            pdf_result: Path,
            page_indices: Union[Literal["ALL"], List[int]] = "ALL",
    ):
        """
        Add a watermark to a PDF file.

        @param content_pdf: The PDF file to add the watermark to.
        @param stamp_pdf: The PDF file with only the watermark.
        @param pdf_result: the output PDF file with the watermark.
        @param page_indices: The page indices to add the watermark to.

        @return: The PDF file with the watermark.
        """
        reader = PdfReader(content_pdf)
        if page_indices == "ALL":
            page_indices = list(range(0, len(reader.pages)))

        writer = PdfWriter()
        for index in page_indices:
            content_page = reader.pages[index]
            mediabox = content_page.mediabox

            reader_stamp = PdfReader(stamp_pdf)
            image_page = reader_stamp.pages[0]

            content_page.merge_page(image_page)
            content_page.mediabox = mediabox
            writer.add_page(content_page)

        with open(pdf_result, "wb") as fp:
            writer.write(fp)

    def merge_pdf(self, pdfs_to_merge):
        merger = PdfMerger()
        for pdf in pdfs_to_merge:
            merger.append(pdf)
        merger.write(self.name)
        merger.close()

    def merge_page_before(self, pdf_to_merge):
        self.merge_pdf([pdf_to_merge, self.name])

    def merge_page_after(self, pdf_to_merge):
        self.merge_pdf([self.name, pdf_to_merge])

    def add_watermark(self):
        self.create_watermark("watermark.pdf", self.user_name)
        self.watermark(
            Path(self.name),
            Path("watermark.pdf"),
            Path(self.name),
            page_indices="ALL"
        )
        os.remove("watermark.pdf")
