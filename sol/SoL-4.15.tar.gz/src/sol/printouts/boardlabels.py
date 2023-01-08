# -*- coding: utf-8 -*-
# :Project:   SoL -- Board labels printout
# :Created:   lun 27 apr 2020, 16:49:51
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2020 Lele Gaifax
#

try:
    from importlib.metadata import metadata
except ImportError:
    from importlib_metadata import metadata

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    )

from ..i18n import translatable_string as gettext

from . import boardnumber_style, subtitle_style
from .basic import TourneyPrintout


class BoardLabelsPrintout(TourneyPrintout):
    "Board labels."

    def __init__(self, output, locale, tourney):
        super().__init__(output, locale, tourney, 3)

    def execute(self, request):
        """Create and build the document.

        :param request: the Pyramid request instance
        """

        self.request = request
        self.createDocument()
        self.doc.build(list(self.getElements()))

    def createDocument(self):
        doc = self.doc = BaseDocTemplate(
            self.output, pagesize=A4, showBoundary=0,
            leftMargin=0.5*cm, rightMargin=0.5*cm,
            topMargin=0.5*cm, bottomMargin=0.5*cm,
            author='SoL %s' % metadata('sol')['Version'],
            creator="https://gitlab.com/metapensiero/SoL",
            subject=self.__class__.__name__,
            title=gettext('Board labels'))

        lp_frames = []

        fwidth = doc.width / self.columns
        fheight = doc.height

        bmargin = doc.bottomMargin
        for f in range(self.columns):
            lmargin = doc.leftMargin + f*fwidth
            lp_frames.append(Frame(lmargin, bmargin, fwidth, fheight))

        templates = [PageTemplate(frames=lp_frames, onPage=self.decoratePage)]
        doc.addPageTemplates(templates)

    def decoratePage(self, canvas, doc):
        "Add crop-marks to the page."

        line = canvas.line
        for iy in range(0, 5):
            y = doc.bottomMargin + iy * (doc.height/4)
            for ix in range(0, 4):
                x = doc.leftMargin + ix * (doc.width/3)
                line(x-5, y, x+5, y)
                line(x, y-5, x, y+5)

    def getElements(self):
        ncomp = len(self.tourney.competitors)
        if not ncomp:  # pragma: no cover
            return

        if ncomp % 2:  # pragma: no cover
            ncomp -= 1

        qrcode_width = 3*cm

        for boardno in range(1, ncomp // 2 + 1):
            url = self.tourney.getEditBoardURL(self.request, boardno)
            drawing = Drawing(qrcode_width, qrcode_width)
            drawing.hAlign = 'CENTER'
            drawing.add(QrCodeWidget(value=url, barWidth=qrcode_width, barHeight=qrcode_width))
            yield Paragraph(gettext('Board'), subtitle_style)
            yield Paragraph(str(boardno), boardnumber_style)
            yield drawing
            if boardno % 4 == 0:
                yield FrameBreak()
            else:
                yield Spacer(0, 0.8*cm)
