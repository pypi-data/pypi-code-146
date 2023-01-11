# -*- coding: utf-8 -*-
## $Id: pdf.py 16905 2022-03-25 11:36:28Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""
Reusable components for pdf generation.
"""
import grok
import os
import pytz
from string import Template
from cStringIO import StringIO
from datetime import datetime
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.units import cm, inch, mm
from reportlab.lib.pagesizes import A4, A3, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    SimpleDocTemplate, Spacer, Paragraph, Image, Table)
from zope.formlib.form import setUpEditWidgets
from zope.i18n import translate
from zope.publisher.browser import TestRequest
from zope.component import getUtility, queryUtility
from waeup.kofa.browser.interfaces import IPDFCreator
from waeup.kofa.utils.helpers import now
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _


#: A reportlab paragraph style for 'normal' output.
NORMAL_STYLE = getSampleStyleSheet()['Normal']

#: A reportlab paragraph style for 'normal' output.
HEADING3_STYLE = getSampleStyleSheet()['Heading3']

#: A reportlab paragraph style for headings.
HEADING_STYLE = ParagraphStyle(
    name='Heading3',
    parent=HEADING3_STYLE,
    fontSize=11,
    )

#: A reportlab paragraph style for output of 'code'.
CODE_STYLE = ParagraphStyle(
    name='Code',
    parent=NORMAL_STYLE,
    fontName='Courier',
    fontSize=10,
    leading=10,
    )

#: A reportlab paragraph style for regular form output.
ENTRY1_STYLE = ParagraphStyle(
    name='Entry1',
    parent=NORMAL_STYLE,
    fontSize=11,
    leading=10,
    )

#: A reportlab paragraph style for smaller form output.
SMALL_PARA_STYLE = ParagraphStyle(
    name='Small1',
    parent=NORMAL_STYLE,
    fontSize=8,
    )

#: A reportlab paragraph style for headlines or bold text in form output.
HEADLINE1_STYLE = ParagraphStyle(
    name='Header1',
    parent=NORMAL_STYLE,
    fontName='Helvetica-Bold',
    fontSize=11,
    )

#: A reportlab paragraph style for notes output at end of documents.
NOTE_STYLE = ParagraphStyle(
    name='Note',
    parent=NORMAL_STYLE,
    fontName='Helvetica',
    fontSize=10,
    #leading=9,
    )

#: Base style for signature tables
SIGNATURE_TABLE_STYLE = [
    ('VALIGN',(0,-1),(-1,-1),'TOP'),
    #('FONT', (0,0), (-1,-1), 'Helvetica-BoldOblique', 12),
    ('BOTTOMPADDING', (0,0), (-1,0), 36),
    ('TOPPADDING', (0,-1), (-1,-1), 0),
    ]


def format_html(html):
    """Make HTML code usable for use in reportlab paragraphs.

    Main things fixed here:
    If html code:
    - remove newlines (not visible in HTML but visible in PDF)
    - add <br> tags after <div> (as divs break lines in HTML but not in PDF)
    - replace <li> tags (as lists are not supported by reportlab)

    The link tag must not be used in html coded text. Use a tags instead.

    If not html code:
    - just replace newlines by <br> tags
    """
    if u'₦' in html:
        html = html.replace(u'₦', u'NGN')
    if '</' in html and not '</link' in html:
        html = html.replace('</div>', '</div><br />')
        html = html.replace('<li>', '- ')
        html = html.replace('</li>', '<br />')
        html = html.replace('\n', '')
    else:
        html = html.replace('\n', '<br />')
    return html

def normalize_signature(signature_tuple):
    """Normalize a signature tuple.

    Returns a tuple ``(<PRE-TEXT>, <SIGNATURE>, <POST-TEXT>)`` from
    input tuple. The following rules apply::

      (pre, sig, post)  --> (pre, sig, post)
      (pre, sig)        --> (pre, sig, None)
      (sig)             --> (None, sig, None)

    Also simple strings are accepted as input::

      sig               --> (None, sig, None)

    If input is not a tuple nor a basestring or if the tuple contains
    an invalid number of elements, ``ValueError`` is raised.
    """
    if isinstance(signature_tuple, basestring):
        return (None, signature_tuple, None)
    if not isinstance(signature_tuple, tuple):
        raise ValueError("signature_tuple must be a string or tuple")
    if len(signature_tuple) < 1 or len(signature_tuple) > 3:
        raise ValueError("signature_tuple must have 1, 2, or 3 elements")
    elif len(signature_tuple) == 1:
        signature_tuple = (None, signature_tuple[0], None)
    elif len(signature_tuple) == 2:
        signature_tuple = (signature_tuple[0], signature_tuple[1], None)
    return signature_tuple

def vert_signature_cell(signature, date_field=True, date_text=_('Date:'),
                        start_row=0, start_col=0, underline=True):
    """Generate a table part containing a vertical signature cell.

    Returns the table data as list of lists and an according style.

    `signature`:
       a signature tuple containing (<PRE-TEXT, SIGNATURE-TEXT, POST-TEXT>)

    `date_field`:
       boolean indicating that a 'Date:' text should be rendered into this
       signature cell (or not).

    `date_text`:
       the text to be rendered into the signature field as 'Date:' text.

    `start_row`:
       starting row of the signature cell inside a broader table.

    `start_col`:
       starting column of the signature cell inside a broader table.

    `underline`:
       boolean indicating that the signature cell should provide a line on
       top (`True` by default).

    Vertical signature cells look like this::

      +------------+
      |Pre         |
      +------------+
      |Date:       |
      |            |
      +------------+
      | ---------- |
      | Signature  |
      +------------+
      |Post        |
      +------------+
    """
    # split signature parts, replacing None with empty string
    pre, sig, post = [x or '' for x in signature]
    style = ()
    x, y = start_col, start_row+2
    if underline:
        style += (('LINEABOVE', (x, y), (x, y), 1, colors.black),)
    d_text = date_field and date_text or ''
    data = [[pre], [d_text], [sig], [post]]
    col_widths = [1.0]
    return data, style, col_widths

def horiz_signature_cell(signature, date_field=True, date_text=_('Date'),
                         start_row=0, start_col=0):
    """Generate a table part containing an horizontal signature cell

    Returns the table data as list of lists and an according style.

    `signature`:
       a signature tuple containing (<PRE-TEXT, SIGNATURE-TEXT, POST-TEXT>)

    `date_field`:
       boolean indicating that a 'Date:' text should be rendered into this
       signature cell (or not).

    `date_text`:
       the text to be rendered into the signature field as 'Date:' text.

    `start_row`:
       starting row of the signature cell inside a broader table.

    `start_col`:
       starting column of the signature cell inside a broader table.

    Horizontal signature cells look like this::

      +------------+---+-----------+
      |Pre text possibly filling   |
      |the whole box               |
      +------------+---+-----------+
      |            |   |           |
      |            |   |           |
      +------------+---+-----------+
      | ---------- |   | --------- |
      | Date       |   | Signature |
      +------------+---+-----------+
      |Post                        |
      +------------+---+-----------+

    """
    pre, sig, post = signature
    if not date_field:
        data, style, cols = vert_signature_cell(signature, date_field=False)
        return data, style, cols
    style = (
        # let pre and post text span the whole signature cell
        ('SPAN', (start_col, start_row), (start_col+2, start_row)),
        ('SPAN', (start_col, start_row+3), (start_col+2, start_row+3)),
        )
    # horizontal cells are buildt from vertical ones chained together
    cell1 = vert_signature_cell(  # leftmost date col
        (pre, date_text, post), date_field=False,
        start_row=start_row, start_col=start_col)
    cell2 = vert_signature_cell(  # spacer col (between date and sig)
        ('', '', ''), date_field=False, underline=False,
        start_row=start_row, start_col=start_col+1)
    cell3 = vert_signature_cell(  # rightmost signature column
        ('', sig, ''), date_field=False,
        start_row=start_row, start_col=start_col+2)
    data = map(lambda x, y, z: x+y+z, cell1[0], cell2[0], cell3[0])
    style = style + cell1[1] + cell2[1] + cell3[1]
    col_widths  = [0.3, 0.03, 0.67] # sums up to 1.0
    return data, style, col_widths

def signature_row(signatures, start_row=0, horizontal=None, max_per_row=3):
    data = [[], [], [], []]
    style = ()
    signatures = [normalize_signature(sig) for sig in signatures]
    start_col = 0
    col_widths = []

    if horizontal is None:
        horizontal = len(signatures) == 1
    cell_maker = vert_signature_cell
    if horizontal:
        cell_maker = horiz_signature_cell
    main_cell_height = not horizontal and 36 or 18

    for sig in signatures:
        sig_data, sig_style, sig_cols = cell_maker(
            sig, start_row=start_row, start_col=start_col)
        data = map(lambda x, y: x+y, data, sig_data)
        style += sig_style
        col_widths += sig_cols + [None,]

        start_col += 1
        # add spacer
        spacer, spacer_style, cols = vert_signature_cell(
            ('', '', ''), date_field=False, underline=False,
            start_row=start_row, start_col=start_col)
        data = map(lambda x, y: x+y, data, spacer)
        style += spacer_style
        start_col += 1

    y = start_row
    sig_row = start_row + 2
    style = style + (
        ('TOPPADDING', (0, y+2), (-1, y+2), 0), # signature row
        ('BOTTOMPADDING', (0, y+1), (-1, y+1), main_cell_height),
        ('LEFTPADDING', (0, y), (-1, y), 1), # pre row
        ('LEFTPADDING', (0, y+3), (-1, y+3), 1), # post row
        )

    if len(signatures) == 1:
        # pre and post text should span whole table
        style += (('SPAN', (0, y), (-1, y)),
                  ('SPAN', (0, y+3), (-1, y+3)),
                  )

    if data[0] == [''] * len(data[0]):
        # no pre text: hide pre row by minimizing padding
        style += (('TOPPADDING', (0,y), (-1, y), -6),
                  ('BOTTOMPADDING', (0,y), (-1, y), -6),
                  )
    if data[-1] == [''] * len(data[0]):
        # no post text: hide post row by minimizing padding
        style += (('TOPPADDING', (0,y+3), (-1, y+3), -6),
                  ('BOTTOMPADDING', (0,y+3), (-1, y+3), -6),
                  )

    if len(signatures) > 1:
        data = [x[:-1] for x in data] # strip last spacer
        col_widths = col_widths[:-1]
    return data, style, col_widths

def sig_table(signatures, lang='en', max_per_row=3, horizontal=None,
              single_table=False, start_row=0, landscape=False):
    if landscape:
        space_width = 2.4  # width in cm of space between signatures
        table_width = 24.0 # supposed width of signature table in cms
    else:
        space_width = 0.4  # width in cm of space between signatures
        table_width = 16.0 # supposed width of signature table in cms
    # width of signature cells in cm...
    sig_num = len(signatures)
    sig_col_width = (table_width - ((sig_num - 1) * space_width)) / sig_num
    if sig_num == 1:
        sig_col_width = 0.8 * table_width         # signature cell part
        space_width = table_width - sig_col_width # spacer part on the right

    if sig_num > max_per_row:
        if horizontal is None:
            horizontal = max_per_row == 1
        sigs_by_row = [signatures[x:x+max_per_row] for x in range(
            0, sig_num, max_per_row)]
        result = []
        curr_row = 0
        for num, row_sigs in enumerate(sigs_by_row):
            curr_row = 0
            if single_table:
                curr_row = num * 4
            result.append(
                sig_table(row_sigs, lang=lang, max_per_row=max_per_row,
                          horizontal=horizontal, start_row=curr_row,
                          landscape=landscape)[0],
                          )
        missing_num = len(result[-2][0][0]) - len(result[-1][0][0])
        if missing_num:
            # last row contained less cells, fix it...
            result[-1] = ([x + [''] * missing_num for x in result[-1][0]],
                          result[-1][1], result[-2][2])
        return result

    data, style, cols = signature_row(signatures, horizontal=horizontal,
                                      start_row=start_row)
    style += (('VALIGN', (0,0), (-1,-1), 'TOP'),)

    # compute col widths...
    col_widths = []
    for col in cols:
        if col is not None:
            col = col * sig_col_width * cm
        else:
            col = space_width * cm
        col_widths.append(col)

    # replace strings by paragraphs and translate all contents
    for rnum, row in enumerate(data):
        for cnum, cell in enumerate(row):
            if cell:
                content = translate(cell, lang)
                data[rnum][cnum] = Paragraph(content, NORMAL_STYLE)
    return [(data, style, col_widths),]

def get_sig_tables(signatures, lang='en', max_per_row=3, horizontal=None,
                   single_table=False, landscape=False):
    rows = sig_table(signatures, lang=lang, max_per_row=max_per_row,
                     horizontal=horizontal, single_table=single_table,
                     landscape=landscape)
    if single_table:
        result_data = []
        result_style = ()
        for row in rows:
            data, style, col_widths = row
            result_data += data
            result_style += style
        return [(result_data, result_style, col_widths),]
    return rows

def get_signature_tables(signatures, lang='en', max_per_row=3,
                         horizontal=None, single_table=False,
                         landscape=False):
    """Get a list of reportlab flowables representing signature fields.

    `signatures` is a list of signatures. Each signature can be a
    simple string or a tuple of format::

      (<PRE-TEXT>, <SIGNATURE>, <POST-TEXT>)

    where ``<PRE-TEXT>`` and ``<POST-TEXT>`` are texts that should
    appear on top (PRE) or below (POST) the signature cell. Both
    formats, string and tuple, can be mixed. A single signature would
    be given as ``[('Pre-Text', 'Signature', 'Post-Text'),]`` or
    simply as ``['Signature']`` if not pre or post-text is wanted.

    All texts (pre, sig, post) are rendered as paragraphs, so you can
    pass in also longer texts with basic HTML formatting like ``<b>``,
    ``<i>``, ``<br />``, etc.

    ``lang`` sets the language to use in I18n context. All texts are
    translated to the given language (``en`` by default) if a
    translation is available.

    ``max_per_row`` gives the maximum number of signatures to put into
    a single row. The default is 3. If more signatures are passed in,
    these signatures are put into a new row. So, for example by
    default 8 signatures would be spread over 3 rows.

    ``horizontal`` tells how the single signature cells should be
    rendered: horizontal or vertical. While horizontal cells render
    date and signature fields side by side, in vertical cells date is
    rendered on top of the signature.

    This parameter accepts *three* different values: ``True``,
    ``False``, or ``None``. While with ``True`` each cell is rendered
    in horizontal mode, ``False`` will create only vertical cells.

    The ``None`` value (set by default) is different: if set, the mode
    will be dependent on the number of signatures per row. If a row
    contains exactly one signature (because only one sig was passed
    in, or because ``max_per_row`` was set to ``1``), then this
    signature is rendered in horizontal mode. Otherwise (with more
    than one sig per row) each cell is rendered in vertical mode. This
    pseudo-smart behaviour can be switched off by setting
    ``horizontal`` explicitly to ``True`` or ``False``.

    ``single_table`` is a boolean defaulting to ``False``. By default
    we return the rows of a signature table in several tables, one of
    each row. This makes it easier for reportlab to perform pagebreaks
    in case the page is already full, without wasting space. If the
    parameter is set to ``True``, then always a list with exactly one
    table is returned, which will contain all rows in one table.

    Generally, if a row contains only one signature, only a part of
    the page width is used to render this signature. If two or more
    signatures are passed in, the complete page width will be filled
    and the single signature cells will be shrinked to fit.
    """
    data_list = get_sig_tables(
        signatures, lang=lang, max_per_row=max_per_row,
        horizontal=horizontal, single_table=single_table, landscape=landscape)
    return [Table(row_data, style=row_style, colWidths=row_col_widths,
                  repeatRows=4)
            for row_data, row_style, row_col_widths in data_list]

def format_signatures(signatures, max_per_row=3, lang='en',
                      single_table=False,
                      date_field=True, date_text=_('Date'),
                      base_style=SIGNATURE_TABLE_STYLE):
    result = []
    signature_tuples = [normalize_signature(sig) for sig in signatures]
    for pre, sig, post in signature_tuples:
        row = []
        if pre is not None:
            row.append([
                translate(pre, lang), '', '', ''])
        row.append([
            translate(_('Date'), lang), '',
            translate(sig, lang), ''
            ])
        if post is not None:
            row.append([
                translate(post, lang), '', '', ''])
        result.append((row, base_style))
    return result



class NumberedCanvas(Canvas):
    """A reportlab canvas for numbering pages after all docs are processed.

    Taken from
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """

    def __init__(self, *args, **kw):
        Canvas.__init__(self, *args, **kw)
        self._saved_page_states = []
        return

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        return

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            Canvas.showPage(self)
        Canvas.save(self)
        return

    def draw_page_number(self, page_count):
        """draw string at bottom right with 'page x of y'.

        Location of the string is determined by canvas attributes
        `kofa_footer_x_pos` and `kofa_footer_y_pos` that have to be
        set manually.

        If this canvas also provides an attribute `kofa_footer_text`,
        the contained text is rendered left of the ``page x of y``
        string.
        """
        self.setFont("Helvetica", 9)
        right_footer_text = _(
            '${footer_text} Page ${num1} of ${num2}',
            mapping = {'footer_text': self.kofa_footer_text,
                       'num1':self._pageNumber, 'num2':page_count})
        self.drawRightString(
            self.kofa_footer_x_pos, self.kofa_footer_y_pos,
             translate(right_footer_text))
        return

class PDFCreator(grok.GlobalUtility):
    """A utility to help with generating PDF docs.
    """
    grok.implements(IPDFCreator)

    watermark_path = None
    header_logo_path = None
    header_logo_left_path = None
    watermark_pos = [0, 0]
    logo_pos = [0, 0, 0]
    logo_left_pos = [0, 0, 0]
    pagesize = portrait(A4)

    test_signature_img_path = os.path.join(
        os.path.dirname(__file__), 'static', 'test_signature.png')

    @classmethod
    def _setUpWidgets(cls, form_fields, context):
        """Setup simple display widgets.

        Returns the list of widgets.
        """
        request = TestRequest()
        return setUpEditWidgets(
            form_fields, 'form', context, request, {},
            for_display=True, ignore_request=True
            )

    @classmethod
    def _addCourse(cls, table_data, row_num, course_label, course_link,
                   lang, domain):
        """Add course data to `table_data`.
        """
        if not course_label or not course_link:
            return table_data, row_num
        f_label= translate(
            _(course_label), domain, target_language=lang)
        f_label = Paragraph(f_label, ENTRY1_STYLE)
        f_text = Paragraph(course_link, ENTRY1_STYLE)
        table_data.append([f_label, f_text])
        row_num += 1
        return table_data, row_num

    @classmethod
    def _addDeptAndFaculty(cls, table_data, row_num, dept, faculty,
                           lang, domain):
        """Add `dept` and `faculty` as table rows to `table_data`.

        `dept` and `faculty` are expected to be strings or None. In
        latter case they are not put into the table.
        """
        for label, text in (('Department:', dept), ('Faculty:', faculty)):
            if text is None:
                continue
            label = translate(_(label), domain, target_language=lang)
            table_data.append([
                Paragraph(label, ENTRY1_STYLE),
                Paragraph(text, ENTRY1_STYLE)])
            row_num += 1
        return table_data, row_num

    @classmethod
    def _drawSignatureBoxes(cls, canvas, width, height, signatures=[]):
        """Draw signature boxes into canvas.
        """
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        mystring = "%r" % ([translate(sig) for sig in signatures])
        for num, sig in enumerate(signatures):
            box_width = (width - 4.2*cm) / len(signatures)
            x_box = 2.1*cm + (box_width) * num
            y_box = 0.75*inch
            canvas.rect(x_box+0.1*cm, y_box, box_width-0.2*cm, 0.75*inch)
            canvas.drawString(
                x_box+0.2*cm, 1.35*inch, translate(sig))
        canvas.restoreState()
        return canvas

    @classmethod
    def fromStringList(cls, string_list):
        """Generate a list of reportlab paragraphs out of a list of strings.

        Strings are formatted with :data:`CODE_STYLE` and a spacer is
        appended at end.
        """
        result = []
        for msg in string_list:
            result.append(Paragraph(msg, CODE_STYLE))
        return result

    @classmethod
    def getImage(cls, image_path, orientation='LEFT'):
        """Get an image located at `image_path` as reportlab flowable.
        """
        img = Image(image_path, width=4*cm, height=3*cm, kind='bound')
        img.hAlign=orientation
        return img

    def _getWidgetsTableData(self, widgets, separators, domain,
                             lang, twoDataCols):
        row_num = 0
        table_data = []
        for widget in widgets:
            if separators and separators.get(widget.name):
                f_headline = translate(
                    separators[widget.name], domain, target_language=lang)
                f_headline = Paragraph(f_headline, HEADLINE1_STYLE)
                table_data.append([f_headline])
                row_num += 1
            f_label = translate(widget.label.strip(), domain,
                                target_language=lang)
            colon = ':'
            if f_label[-1:] == '?':
                colon =''
            f_label = Paragraph('%s%s' % (f_label, colon), ENTRY1_STYLE)
            f_text = translate(widget(), domain, target_language=lang)
            f_text = format_html(f_text)
            #if f_text:
            #    hint = ' <font size=9>' + widget.hint + '</font>'
            #    f_text = f_text + hint
            f_text = Paragraph(f_text, ENTRY1_STYLE)
            table_data.append([f_label,f_text])
            row_num += 1
        return table_data, row_num

    def getWidgetsTable(self, form_fields, context, view, lang='en',
                        domain='waeup.kofa', separators=None,
                        course_label=None, course_link=None, dept=None,
                        faculty=None, colWidths=None, twoDataCols=False):
        """Return a reportlab `Table` instance, created from widgets
        determined by `form_fields` and `context`.

        - `form_fields`
           is a list of schema fields as created by grok.AutoFields.
        - `context`
           is some object whose content is rendered here.
        - `view`
           is currently not used but supposed to be a view which is
           actually rendering a PDF document.
        - `lang`
           the portal language. Used for translations of strings.
        - `domain`
           the translation domain used for translations of strings.
        - `separators`
           a list of separators.
        - `course_label` and `course_link`
           if a course should be added to the table, `course_label`
           and `course_link` can be given, both being strings. They
           will be rendered in an extra-row.
        - `dept` and `faculty`
           if these are given, we render extra rows with faculty and
           department.
        - `colWidths`
           defines the the column widths of the data in the right column
           of base data (right to the passport image).
        - `twoDataCols`
           renders data widgets in a parent table with two columns.
        """
        table_style = [('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ]
        widgets = self._setUpWidgets(form_fields, context)

        # Determine table data
        table_data, row_num = self._getWidgetsTableData(
            widgets, separators, domain, lang, twoDataCols)

        # Add course (admitted, etc.) if applicable
        table_data, row_num = self._addCourse(
            table_data, row_num, course_label, course_link, lang, domain,)

        ## Add dept. and faculty if applicable
        table_data, row_num = self._addDeptAndFaculty(
            table_data, row_num, dept, faculty, lang, domain)

        # render two-column table of tables if applicable
        lines = len(table_data)
        middle = lines/2
        if twoDataCols is True and lines > 2:
            table_left = Table(table_data[:middle],
                               style=table_style, colWidths=[3*cm, 6.3*cm])
            table_right = Table(table_data[middle:],
                                style=table_style, colWidths=[3*cm, 6.3*cm])
            table_style.append(('LEFTPADDING', (0,0), (0,-1), 1.2*cm),)
            table = Table([[table_left, table_right],],style=table_style)
            return table

        # render single table
        table = Table(
            table_data,style=table_style, colWidths=colWidths) #, rowHeights=14)
        table.hAlign = 'LEFT'
        return table


    def paint_background(self, canvas, doc):
        """Paint background of a PDF, including watermark, title, etc.

        The `doc` is expected to be some reportlab SimpleDocTemplate
        or similar object.

        Text of headerline is extracted from doc.kofa_headtitle, the
        document title (under the head) from doc.kofa_title.

        This is a callback method that will be called from reportlab
        when creating PDFs with :meth:`create_pdf`.
        """
        canvas.saveState()
        width, height = doc.width, doc.height
        width += doc.leftMargin + doc.rightMargin
        height += doc.topMargin + doc.bottomMargin

        # Watermark
        if self.watermark_path is not None:
            canvas.saveState()
            canvas.drawImage(self.watermark_path,
                self.watermark_pos[0], self.watermark_pos[1])
            canvas.restoreState()

        # Header
        site_config = None
        site = grok.getSite()
        if site is not None:
            site_config = site.get('configuration', None)
        head_title = getattr(
            doc, 'kofa_headtitle', getattr(
                site_config, 'name',
                u'Sample University'))
        canvas.setFont("Helvetica-Bold", 18)
        if self.header_logo_left_path is not None:
            canvas.drawCentredString(width/2.0, height-1.7*cm, head_title)
        else:
            canvas.drawString(1.5*cm, height-1.7*cm, head_title)
        canvas.line(1.5*cm,height-1.9*cm,width-1.5*cm,height-1.9*cm)
        if self.header_logo_path is not None:
            canvas.drawImage(self.header_logo_path,
                self.logo_pos[0], self.logo_pos[1], width=self.logo_pos[2],
                preserveAspectRatio=True, anchor='ne')
        if self.header_logo_left_path is not None:
            canvas.drawImage(self.header_logo_left_path,
                self.logo_left_pos[0], self.logo_left_pos[1],
                width=self.logo_left_pos[2],
                preserveAspectRatio=True, anchor='ne')

        # Title
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 14)
        title = getattr(doc, 'kofa_title', '')
        if '\n' in title:
            title_lines = title.split('\n')
            for num, line in enumerate(title_lines):
                canvas.drawCentredString(
                    width/2.0, height-2.8*cm-(num*0.7*cm), line)
        elif title:
            canvas.drawCentredString(width/2.0, height-2.8*cm, title)
        canvas.restoreState()

        # Footer
        canvas.saveState()
        if getattr(doc, 'sigs_in_footer', False):
            self._drawSignatureBoxes(
                canvas, width, height, doc.sigs_in_footer)
        canvas.line(2.2*cm, 0.62*inch, width-2.2*cm, 0.62*inch)
        canvas.setFont("Helvetica", 9)
        if not getattr(doc, 'kofa_nodate', False):
            tz = getattr(queryUtility(IKofaUtils), 'tzinfo', pytz.utc)
            today = now(tz).strftime('%d/%m/%Y %H:%M:%S %Z')
            canvas.drawString(2.2*cm, 0.5 * inch,
                translate(_(u'Date: ${a}', mapping = {'a': today})))
        # set canves attributes needed to render `page x of y`
        canvas.kofa_footer_x_pos = width-2.2*cm
        canvas.kofa_footer_y_pos = 0.5 * inch
        canvas.kofa_footer_text =  doc.kofa_footer
        canvas.restoreState()

        # Metadata
        canvas.setAuthor(getattr(doc, 'kofa_author', 'Unknown'))
        canvas.setSubject(title)
        canvas.setCreator(u'WAeUP Kofa')
        return

    def _substitute_markers(self, text):
        """If `text` contains some marker, substitute it.

        Markers are standard library string template placeholders. See
        https://docs.python.org/2/library/string.html and
        `string.Template` for details. Roughly, placeholders look like
        ``${some_marker}``.

        Valid markers:
           ``test_signature_img_path`` -- path to signature image stored in
                                     `test_signature_img_path`` attribute.
        """
        text = Template(text)
        PDF_SIGNATURES =  {
            'test_signature_img_path': self.test_signature_img_path,
            }
        return text.safe_substitute(PDF_SIGNATURES)

    def create_pdf(self, data, headerline=None, title=None, author=None,
                   footer='', note=None, sigs_in_footer=[], topMargin=1.5,
                   letterhead_path=None, view=None):
        """Returns a binary data stream which is a PDF document.
        """
        pdf_stream = StringIO()
        bottomMargin = len(sigs_in_footer) and 1.9*inch or 1.2*inch
        if not letterhead_path:
            topMargin += title.count('\n') * 0.2
        doc = SimpleDocTemplate(
            pdf_stream,
            bottomMargin=bottomMargin,
            topMargin=topMargin*inch,
            title=title,
            pagesize=self.pagesize,
            showBoundary=False,
            )
        # Set some attributes that are needed when rendering the background.
        if headerline is not None:
            doc.kofa_headtitle = headerline
        doc.kofa_title = title
        doc.kofa_author = author
        doc.kofa_footer = footer
        doc.sigs_in_footer = sigs_in_footer
        doc.letterhead_path = letterhead_path
        # Forward view in case we need customized watermarks
        self.view = view
        if note is not None:
            # Inject signature images
            note = self._substitute_markers(note)
            # Format html
            html = format_html(note)
            data.append(Paragraph(html, NOTE_STYLE))
        doc.build(data, onFirstPage=self.paint_background,
                  onLaterPages=self.paint_background,
                  canvasmaker=NumberedCanvas
                  )
        result = pdf_stream.getvalue()
        pdf_stream.close()
        return result

class LandscapePDFCreator(PDFCreator):
    """A utility to help with generating PDF docs in
    landscape format.
    """
    grok.name('landscape')
    pagesize = landscape(A4)

class LetterPDFCreator(PDFCreator):
    """A utility to help with generating PDF docs with an original letterhead.
    """
    grok.name('letter')
    letterhead_pos = [0, 0]

    def paint_background(self, canvas, doc):
        """Paint letterhead background of a PDF.

        The `doc` is expected to be some reportlab SimpleDocTemplate
        or similar object.

        This is a callback method that will be called from reportlab
        when creating PDFs with :meth:`create_pdf`.
        """
        canvas.saveState()
        width, height = doc.width, doc.height
        width += doc.leftMargin + doc.rightMargin
        height += doc.topMargin + doc.bottomMargin

        # Letterhead
        if doc.letterhead_path is not None:
            canvas.saveState()
            canvas.drawImage(doc.letterhead_path,
                self.letterhead_pos[0], self.letterhead_pos[1],
                width=width, height=height)
            canvas.restoreState()

        # Footer
        if getattr(doc, 'sigs_in_footer', False):
            self._drawSignatureBoxes(
                canvas, width, height, doc.sigs_in_footer)
        #canvas.line(2.2*cm, 0.62*inch, width-2.2*cm, 0.62*inch)
        canvas.setFont("Helvetica", 9)
        if not getattr(doc, 'kofa_nodate', False):
            tz = getattr(queryUtility(IKofaUtils), 'tzinfo', pytz.utc)
            today = now(tz).strftime('%d/%m/%Y %H:%M:%S %Z')
            #canvas.drawString(2.2*cm, 0.5 * inch,
            #    translate(_(u'Date: ${a}', mapping = {'a': today})))
            canvas.drawString(2.2*cm, 0.3 * inch,
                translate(_(u'Date: ${a}', mapping = {'a': today})))
        # set canves attributes needed to render `page x of y`
        canvas.kofa_footer_x_pos = width-2.2*cm
        #canvas.kofa_footer_y_pos = 0.5 * inch
        canvas.kofa_footer_y_pos = 0.3 * inch
        canvas.kofa_footer_text =  doc.kofa_footer
        canvas.restoreState()

        # Metadata
        title = getattr(doc, 'kofa_title', '')
        canvas.setAuthor(getattr(doc, 'kofa_author', 'Unknown'))
        canvas.setSubject(title)
        canvas.setCreator(u'WAeUP Kofa')
        return


class A3LandscapePDFCreator(LandscapePDFCreator):
    """A utility to help with generating PDF docs in
    A3 landscape format. No watermark is shown.
    """
    grok.name('A3landscape')
    pagesize = landscape(A3)

def get_qrcode(text, width=60.0):
    """Get a QR Code as Reportlab Flowable (actually a `Drawing`).

    `width` gives box width in pixels (I think)
    """
    widget = QrCodeWidget(text)
    bounds = widget.getBounds()
    w_width = bounds[2] - bounds[0]
    w_height = bounds[3] - bounds[1]
    drawing = Drawing(
        width, width,
        transform=[width/w_width, 0, 0, width/w_height, 0, 0])
    drawing.add(widget)
    return drawing
