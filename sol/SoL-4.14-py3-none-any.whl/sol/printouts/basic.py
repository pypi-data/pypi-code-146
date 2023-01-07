# -*- coding: utf-8 -*-
# :Project:   SoL -- Abstract printout class
# :Created:   lun 13 giu 2016 11:21:19 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018, 2020 Lele Gaifax
#

from datetime import datetime
try:
    from importlib.metadata import metadata
except ImportError:
    from importlib_metadata import metadata

from babel.numbers import format_decimal

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    FrameBreak,
    NextPageTemplate,
    Paragraph,
    )

from sqlalchemy.orm.exc import NoResultFound

from ..i18n import translatable_string as _, gettext, translator
from ..models import Tourney
from ..models.errors import OperationAborted

from . import BASE_FONT_NAME, logger, title_style, subtitle_style
from .utils import TotalCountOfPagesCanvas, reduce_fontsize_to_fit_width


class BasicPrintout(object):
    """Abstract base class used to implement the printouts.

    This class implements the logic used by most printouts, producing a PDF document in the
    `output` filename.

    The document has a front page with an header, a body splitted into `columns` frames and
    a footer. Succeding pages do not have the header frame.
    """

    leftMargin = 1*cm
    "The width of the left margin, by default 1cm"

    rightMargin = 1*cm
    "The width of the right margin, by default 1cm"

    topMargin = 1*cm
    "The width of the top margin, by default 1cm"

    bottomMargin = 1*cm
    "The width of the bottom margin, by default 1cm"

    pagesize = A4
    "The page size, by default A4 in portrait orientation"

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        """Extract needed arguments for the constructor from the request.

        :param session: the SQLAlchemy session
        :param request: the Pyramid request instance
        :rtype: a sequence of arguments
        """

        return [request.locale_name]

    def __init__(self, output, locale, columns):
        """Initialize the instance.

        :param output: a filename where the PDF will be written
        :param columns: number of columns
        """

        self.locale = locale
        self.output = output
        self.columns = columns
        self.timestamp = datetime.now()

    @property
    def cache_max_age(self):
        "Compute the cache control max age, in seconds."

        return 0

    def createDocument(self):
        """Create the base Platypus document."""

        doc = self.doc = BaseDocTemplate(
            self.output, pagesize=self.pagesize, showBoundary=1,
            leftMargin=self.leftMargin, rightMargin=self.rightMargin,
            topMargin=self.topMargin, bottomMargin=self.bottomMargin,
            author='SoL %s' % metadata('sol')['Version'],
            creator="https://gitlab.com/metapensiero/SoL",
            subject=self.__class__.__name__,
            title='%s: %s' % (self.getTitle(), self.getSubTitle()))

        title_height = 3.0*cm
        title_width = doc.width
        if self.lit_url is not None:
            title_width -= title_height
        title_frame = Frame(doc.leftMargin, doc.height + doc.bottomMargin - title_height,
                            title_width, title_height)
        self.title_width = title_width

        fp_frames = [title_frame]
        lp_frames = []

        fwidth = doc.width / self.columns
        fheight = doc.height

        bmargin = doc.bottomMargin
        for f in range(self.columns):
            lmargin = doc.leftMargin + f*fwidth
            fp_frames.append(Frame(lmargin, bmargin, fwidth, fheight-title_height))
            lp_frames.append(Frame(lmargin, bmargin, fwidth, fheight))

        templates = [PageTemplate(frames=fp_frames, id="firstPage",
                                  onPage=self.decoratePage),
                     PageTemplate(frames=lp_frames, id="laterPages",
                                  onPage=self.decoratePage)]
        doc.addPageTemplates(templates)

    def getLeftHeader(self):  # pragma: no cover
        "The top left text."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getRightHeader(self):  # pragma: no cover
        "The top right text."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getCenterHeader(self):  # pragma: no cover
        "The top center text."
        # pragma: no cover
        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getTitle(self):  # pragma: no cover
        "The title of the document."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getSubTitle(self):  # pragma: no cover
        "The subtitle of the document."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getLeftFooter(self):
        "The bottom left text, SoL description and version by default."

        return 'SoL %s %s' % (gettext('version'), metadata('sol')['Version'])

    def getRightFooter(self):
        "The bottom right text, current time by default."

        # TRANSLATORS: this is a Python strftime() format, see
        # http://docs.python.org/3/library/time.html#time.strftime
        return self.timestamp.strftime(str(gettext('%m-%d-%Y %I:%M %p')))

    def getCenterFooter(self):
        "The bottom center text, by default the subtitle."

        return self.getSubTitle()

    def decoratePage(self, canvas, doc):
        "Add standard decorations to the current page."

        canvas.saveState()
        canvas.setFont(BASE_FONT_NAME, 6)
        w, h = doc.pagesize
        hh = doc.bottomMargin + doc.height + doc.topMargin/2
        hl = doc.leftMargin
        hc = doc.leftMargin + doc.width/2.0
        hr = doc.leftMargin + doc.width
        canvas.drawString(hl, hh, self.getLeftHeader())
        canvas.drawCentredString(hc, hh, self.getCenterHeader())
        canvas.drawRightString(hr, hh, self.getRightHeader())
        fh = doc.bottomMargin/2
        canvas.drawString(hl, fh, self.getLeftFooter())
        canvas.drawCentredString(hc, fh+doc.bottomMargin/4, self.getCenterFooter())
        canvas.drawRightString(hr, fh, self.getRightFooter())

        if doc.page == 1 and self.lit_url is not None:
            logger.debug('QrCode: %s', self.lit_url)
            qr = QrCodeWidget(self.lit_url)
            bounds = qr.getBounds()
            qrw = bounds[2] - bounds[0]
            qrh = bounds[2] - bounds[1]
            size = 3*cm
            drawing = Drawing(size, size, transform=[size/qrw, 0, 0, size/qrh, 0, 0])
            drawing.add(qr)
            x = w - doc.leftMargin - size
            y = h - doc.topMargin - size
            renderPDF.draw(drawing, canvas, x, y)
            canvas.linkURL(self.lit_url, (x, y, x+size, y+size))
        canvas.restoreState()

    def execute(self, request):
        """Create and build the document.

        :param request: the Pyramid request instance
        """

        self.lit_url = self.getLitURL(request)
        self.createDocument()
        self.doc.build(list(self.getElements()), canvasmaker=TotalCountOfPagesCanvas)

    def getElements(self):  # pragma: no cover
        "Return a list or an iterator of all the elements."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getLitURL(self, request):
        """Compute the Lit URL for this printout, if any.

        :param request: the Pyramid request instance
        """

        return None


class TourneyPrintout(BasicPrintout):
    "Basic tourney printout, to be further specialized."

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        args = super().getArgumentsFromRequest(session, request)
        t = translator(request)

        id = request.matchdict['id']
        if id == 'blank':
            entity = None
        else:
            try:
                idtourney = int(id)
            except ValueError:
                try:
                    entity = session.query(Tourney).filter_by(guid=id).one()
                except NoResultFound:
                    raise OperationAborted(t(_('No tourney with guid $id',
                                               mapping=dict(id=id))))
            else:
                entity = session.query(Tourney).get(idtourney)
                if entity is None:
                    raise OperationAborted(t(_('No tourney with id $id',
                                               mapping=dict(id=str(idtourney)))))

        args.append(entity)
        return args

    def __init__(self, output, locale, tourney, columns):
        super().__init__(output, locale, columns)
        self.tourney = tourney

    @property
    def cache_max_age(self):
        "Cache for one year prized tourneys, no cache otherwise."

        if self.tourney.prized:
            return 60*60*24*365
        else:
            return 0

    def getLitURL(self, request):
        functional_testing = request.registry.settings['desktop.version'] == 'test'
        if not request.host.startswith('localhost') or functional_testing:
            return request.route_url('lit_tourney', guid=self.tourney.guid)

    def getLeftHeader(self):
        "Return championship description."

        return self.tourney.championship.description

    def getRightHeader(self):
        "Return championship's club description, plus the hosting club if any."

        result = self.tourney.championship.club.description
        if self.tourney.hosting_club:
            result += ', ' + gettext('hosted by') + ' ' + self.tourney.hosting_club.description
        return result

    def getCenterHeader(self):
        "Return location and date of the event."

        # TRANSLATORS: this is a Python strftime() format, see
        # http://docs.python.org/3/library/time.html#time.strftime
        dateformat = gettext('%m-%d-%Y')

        if self.tourney.location:
            return gettext('%(location)s, %(date)s') % dict(
                location=self.tourney.location,
                date=self.tourney.date.strftime(dateformat))
        else:
            return self.tourney.date.strftime(dateformat)

    def getTitle(self):
        "Return tourney description."

        return self.tourney.description

    def getElements(self):
        "Yield basic elements for the title frame in the first page."

        title = self.getTitle()
        tstyle, ststyle = reduce_fontsize_to_fit_width(title, self.title_width - 1*cm,
                                                       title_style, subtitle_style)

        yield Paragraph(title, tstyle)
        yield Paragraph(self.getSubTitle(), ststyle)
        yield FrameBreak()
        yield NextPageTemplate('laterPages')

    def format_prize(self, prize):
        if self.tourney.championship.prizes != 'centesimal':
            return format_decimal(prize, '###0', self.locale)
        else:
            return format_decimal(prize, '###0.00', self.locale)
