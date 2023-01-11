import os
import tempfile
import unittest
from reportlab.lib import colors
from reportlab.platypus.flowables import PageBreak
from waeup.kofa.browser.pdf import (
    format_html, normalize_signature, format_signatures,
    vert_signature_cell, horiz_signature_cell, signature_row, get_sig_tables,
    PDFCreator, Paragraph, Table, NORMAL_STYLE, sig_table,
    get_signature_tables)

DRAW_SAMPLE_GRID = True

class HelperTest(unittest.TestCase):

    def test_format_html(self):
        # test format_html()
        intext = 'Two\nLines'
        self.assertEqual(format_html(intext), 'Two<br />Lines')
        intext = '<div>Two</div>\nLines'
        self.assertEqual(format_html(intext), '<div>Two</div><br />Lines')
        intext = '<div>Two</div>Lines'
        self.assertEqual(format_html(intext), '<div>Two</div><br />Lines')
        return

class SignatureNormalizerTests(unittest.TestCase):
    # Tests for normalize_signature()

    def test_invalid_input_type(self):
        # we accept only strings and tuples
        self.assertRaises(
            # we don't accept number, for instance
            ValueError, normalize_signature, 12)
        return

    def test_invalid_number_of_items(self):
        # a signature tuple must contain 1, 2, or 3 elements
        self.assertRaises(
            # empty tuple
            ValueError, normalize_signature, ())
        self.assertRaises(
            # overcrowded tuple
            ValueError, normalize_signature, ('a', 'b', 'c', 'd'))
        return

    def test_simple_string(self):
        # we accept a simple string
        self.assertEqual(
            normalize_signature('sig1'),
            ((None, 'sig1', None)))
        # also unicode is allowed
        self.assertEqual(
            normalize_signature(u'sig1'),
            ((None, u'sig1', None)))

    def test_one_item_tuple(self):
        # we accept a tuple with a single signature string
        self.assertEqual(
            normalize_signature(('sig1',)),
            ((None, 'sig1', None)))
        return

    def test_two_items_tuple(self):
        # we accept a tuple with two items
        self.assertEqual(
            normalize_signature(('pre-text', 'sig1')),
            (('pre-text', 'sig1', None)))
        return

    def test_three_items_tuple(self):
        # we accept a tuple with three items, of course
        self.assertEqual(
            normalize_signature(('pre-text', 'sig1', 'post-text')),
            (('pre-text', 'sig1', 'post-text')))
        return

class SignaturesFormatterTests(unittest.TestCase):

    def test_single_signature(self):
        # we can format a single signature (w/o pre or post blocks)
        data, style = format_signatures(['My Signature'])[0]
        self.assertEqual(
            data, [['Date', '', 'My Signature', '']])
        #self.assertEqual(style, )
        return

    def test_single_sig_with_pre_text(self):
        # we can format a single signature (with pre-text)
        data, style = format_signatures([('Pre-Text', 'My Sig', None)])[0]
        self.assertEqual(
            data,
            [['Pre-Text', '', '', ''],
             ['Date', '', 'My Sig', '']])
        return

    def test_single_sig_with_post_text(self):
        # we can format a single signature (with post-text)
        data, style = format_signatures([(None, 'My Sig', 'Post-Text')])[0]
        self.assertEqual(
            data,
            [['Date', '', 'My Sig', ''],
             ['Post-Text', '', '', '']])
        return

    def test_single_sig_with_pre_and_post_text(self):
        # we can format a single signature (with pre- and post-text)
        data, style = format_signatures([('Pre', 'My Sig', 'Post')])[0]
        self.assertEqual(
            data,
            [['Pre', '', '', ''],
             ['Date', '', 'My Sig', ''],
             ['Post', '', '', '']])
        return

class SignatureCellFormatterTests(unittest.TestCase):

    def test_vert_signature(self):
        # we can create vertical signatures
        data, style, cols = vert_signature_cell(
            ('Pre', 'Sig', 'Post'))
        self.assertEqual(
            data,
            [['Pre'], ['Date:'], ['Sig'], ['Post']])
        self.assertEqual(
            style,
            (('LINEABOVE', (0, 2), (0, 2), 1, colors.black),)
            )
        return

    def test_vert_signature_custom_row_and_col(self):
        # custom row and col nums are respected
        data, style, cols = vert_signature_cell(
            ('Pre', 'Sig', 'Post'), start_row=5, start_col=3)
        self.assertEqual(
            style,
            (('LINEABOVE', (3, 7), (3, 7), 1, colors.black),)
            )
        return

    def test_vert_signature_no_underline(self):
        # we can suppress the underlining of signature cell
        data, style, cols = vert_signature_cell(
            ('Pre', 'Sig', 'Post'), underline=False)
        self.assertEqual(
            style, ())
        return

    def test_vert_signature_custom_date(self):
        # we can create vertical signatures with customized date text
        data, style, cols = vert_signature_cell(
            ('Pre', 'Sig', 'Post'), date_text='My Date')
        self.assertEqual(
            data,
            [['Pre'], ['My Date'], ['Sig'], ['Post']])
        return

    def test_vert_signature_no_date(self):
        # we can create vertical signatures without date
        data, style, cols = vert_signature_cell(
            ('Pre', 'Sig', 'Post'), date_field=False)
        self.assertEqual(
            data,
            [['Pre'], [''], ['Sig'], ['Post']])
        return

    def test_vert_signature_no_pre(self):
        # we can create vertical signatures w/o pre-text
        data, style, cols = vert_signature_cell(
            (None, 'Sig', 'Post'))
        self.assertEqual(
            data,
            [[''], ['Date:'], ['Sig'], ['Post']])
        return

    def test_vert_signature_no_post(self):
        # we can create vertical signatures w/o post-text
        data, style, cols = vert_signature_cell(
            ('Pre', 'Sig', None))
        self.assertEqual(
            data,
            [['Pre'], ['Date:'], ['Sig'], ['']])
        return

    def test_horiz_signature_cell(self):
        # we can create horizontal signatures
        data, style, cols = horiz_signature_cell(
            ('Pre', 'Sig', 'Post'))
        self.assertEqual(
            data, [['Pre', '', ''],
                   ['', '', ''],
                   ['Date', '', 'Sig'],
                   ['Post', '', '']])
        self.assertEqual(
            style,
            (
                ('SPAN', (0, 0), (2, 0)),
                ('SPAN', (0, 3), (2, 3)),
                ('LINEABOVE', (0, 2), (0, 2), 1, colors.black),
                ('LINEABOVE', (2, 2), (2, 2), 1, colors.black),
             ))
        return

    def test_horiz_signature_cell_no_date(self):
        # we can create horizontal signatures without date
        data, style, cols = horiz_signature_cell(
            ('Pre', 'Sig', 'Post'), date_field=False)
        self.assertEqual(
            data, [['Pre'], [''], ['Sig'], ['Post']])
        self.assertEqual(
            style, (('LINEABOVE', (0, 2), (0, 2), 1, colors.black),))
        return

    def test_horiz_signature_cell_custom_date(self):
        # we can create horizontal signatures with custom date text
        data, style, cols = horiz_signature_cell(
            ('Pre', 'Sig', 'Post'), date_text='My Date')
        self.assertEqual(
            data, [['Pre', '', ''],
                   ['', '', ''],
                   ['My Date', '', 'Sig'],
                   ['Post', '', '']])
        self.assertEqual(
            style,
            (
                ('SPAN', (0, 0), (2, 0)),
                ('SPAN', (0, 3), (2, 3)),
                ('LINEABOVE', (0, 2), (0, 2), 1, colors.black),
                ('LINEABOVE', (2, 2), (2, 2), 1, colors.black),
                ))
        return

    def test_horiz_signature_cell_no_pre(self):
        # we can create horizontal signatures without pre-text
        data, style, cols = horiz_signature_cell(
            (None, 'Sig', 'Post'))
        self.assertEqual(
            data, [['', '', ''],
                   ['', '', ''],
                   ['Date', '', 'Sig'],
                   ['Post', '', '']])
        self.assertEqual(
            style,
            (
                ('SPAN', (0, 0), (2, 0)),
                ('SPAN', (0, 3), (2, 3)),
                ('LINEABOVE', (0, 2), (0, 2), 1, colors.black),
                ('LINEABOVE', (2, 2), (2, 2), 1, colors.black),
                ))
        return

    def test_horiz_signature_cell_no_post(self):
        # we can create horizontal signatures without post-text
        data, style, cols = horiz_signature_cell(
            ('Pre', 'Sig', None))
        self.assertEqual(
            data, [['Pre', '', ''],
                   ['', '', ''],
                   ['Date', '', 'Sig'],
                   ['', '', '']])
        self.assertEqual(
            style,
            (
                ('SPAN', (0, 0), (2, 0)),
                ('SPAN', (0, 3), (2, 3)),
                ('LINEABOVE', (0, 2), (0, 2), 1, colors.black),
                ('LINEABOVE', (2, 2), (2, 2), 1, colors.black),
                ))
        return

    def test_horiz_signature_cell_custom_row_and_col(self):
        # custom col and row numbers are respected in styles
        data, style, cols = horiz_signature_cell(
            ('Pre', 'Sig', 'Post'), start_row=3, start_col=5)
        self.assertEqual(
            style,
            (
                ('SPAN', (5, 3), (7, 3)),
                ('SPAN', (5, 6), (7, 6)),
                ('LINEABOVE', (5, 5), (5, 5), 1, colors.black),
                ('LINEABOVE', (7, 5), (7, 5), 1, colors.black),
                ))
        return

class SignatureRowFormatterTests(unittest.TestCase):

    def test_vertical_row(self):
        data, style, cols = signature_row(
            ['Sig 1', 'Sig 2',])
        self.assertEqual(
            data, [['', '', ''], ['Date:', '', 'Date:'],
                   ['Sig 1', '', 'Sig 2'], ['', '', '']]
            )
        self.assertEqual(
            style, (
                ('LINEABOVE', (0, 2), (0, 2), 1, colors.black),
                ('LINEABOVE', (2, 2), (2, 2), 1, colors.black),
                ('TOPPADDING', (0, 2), (-1, 2), 0),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 36),
                ('LEFTPADDING', (0, 0), (-1, 0), 1),
                ('LEFTPADDING', (0, 3), (-1, 3), 1),
                ('TOPPADDING', (0, 0), (-1, 0), -6),
                ('BOTTOMPADDING', (0, 0), (-1, 0), -6),
                ('TOPPADDING', (0, 3), (-1, 3), -6),
                ('BOTTOMPADDING', (0, 3), (-1, 3), -6)
                )
            )
        return

def samples_dir():
    # create a directory for sample sheets, if it doesn't exist,
    # and return its path.
    tmp_dir = os.path.join(
        tempfile.gettempdir(), 'waeup.kofa.pdf-samples')
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    return tmp_dir

def draw_sample_pdf(data, name='signatures.pdf',
                    title='Sample Title', author='Test Author'):
    # create a pdf document with data as content
    #data = [Paragraph('<b>Sample</b>', NORMAL_STYLE)]
    creator = PDFCreator()
    pdf = creator.create_pdf(
        data, title=title, author=author)
    path = os.path.join(samples_dir(), name)
    open(path, 'wb').write(pdf)
    return path


class SampleSheet(unittest.TestCase):

    def add_tables(self, data, title, tables, grid=DRAW_SAMPLE_GRID):
        # add tables to `data`
        mod_tables = []
        data += [Paragraph(title, NORMAL_STYLE),]
        for table in tables:
            if grid:
                table.setStyle((
                    ('INNERGRID',(0,0),(-1,-1), 0.25, colors.blue),
                    ('BOX', (0,0), (-1, -1), 0.25, colors.blue)),)
            data += [table,]
        return data


    def test_draw_sample(self):
        # create a sample sheet as PDF
        # single signature
        data = [
            Paragraph('Signature Samples in here are created by '
                      'calling the '
                      '<font face="Times">get_signature_tables()</font> '
                      'function.<br />'
                      'Grids are drawn for better visibility of '
                      'internal table structure only. You can set '
                      'DRAW_SAMPLE_GRID value in browser/tests/test_pdf.py.'
                      '<br /><br />',
                      NORMAL_STYLE),
            ]

        tables = get_signature_tables(['Signature 1'])
        data = self.add_tables(
            data, '<b>Single Signature:</b> '
            '<font face="Times">get_signature_tables(["Signature 1"])</font>',
            tables)

        # two signatures in a row
        tables = get_signature_tables(['Signature 1', 'Signature 2'])
        data = self.add_tables(
            data, '<br /><b>Two Signatures:</b> '
            '<font face="Times">get_signature_tables(["Signature 1",'
            ' "Signature 2"])</font></b>',
            tables)

        # single signature with pre/post text
        tables = get_signature_tables(
            [('Pre-Text', 'Signature 1', 'Post-Text')])
        data = self.add_tables(
            data,
            '<br /><b>Single Signature with Pre- and Post Text:</b> '
            '<font face="Times">get_signature_tables('
            '[("Pre-Text", "Signature 1", "Post-Text")])</font>',
            tables)

        # three signatures
        tables = get_signature_tables(['Sig 1', 'Sig 2', 'Sig 3'])
        data = self.add_tables(
            data,
            '<br /><b>Three Signatures:</b> '
            '<font face="Times">get_signature_tables('
            '["Sig 1", "Sig 2", "Sig 3"])</font>',
            tables)

        # four signatures
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2', 'Sig 3', 'Sig 4'])
        data = self.add_tables(
            data,
            '<br /><b>Sample: Four Signatures (each row a table)</b>',
            tables)

        # four sigs in one table
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2', 'Sig 3', 'Sig 4'], single_table=True)
        data = self.add_tables(
            data,
            '<br /><b>Sample: Four Signatures (as one table)</b>',
            tables)


        data += [PageBreak(), Paragraph(
            '<br /><br /><font size="14"><font face="Times">horizontal</font>'
            ' Parameter (with one sig): </b><br />',
            NORMAL_STYLE)]

        # one signature (default behaviour)
        tables = get_signature_tables(
            ['Sig 1'], horizontal=None)
        data = self.add_tables(
            data, '<br /><b>One Signature (default, horizontal=None):</b> '
            '<font face="Times">get_signature_tables(["Signature 1"], '
            'horizontal=None)</font></b>',
            tables)

        # one signature (horizontal)
        tables = get_signature_tables(
            ['Sig 1'], horizontal=True)
        data = self.add_tables(
            data, '<br /><b>One Signature (horizontal=True):</b> '
            '<font face="Times">get_signature_tables(["Signature 1"], '
            'horizontal=True)</font></b>',
            tables)

        # one signature (vertical)
        tables = get_signature_tables(
            ['Sig 1'], horizontal=False)
        data = self.add_tables(
            data, '<br /><b>One Signature (horizontal=False):</b> '
            '<font face="Times">get_signature_tables(["Signature 1"], '
            'horizontal=False)</font></b>',
            tables)

        data += [Paragraph(
            '<br /><br /><font size="14"><font face="Times">horizontal</font>'
            ' Parameter (with two sigs): </b><br />',
            NORMAL_STYLE)]

        # two signatures (default behaviour)
        tables = get_signature_tables(
            ['Signature 1', 'Signature 2'], horizontal=None)
        data = self.add_tables(
            data, '<br /><b>Two Signatures (default, horizontal=None):</b> '
            '<font face="Times">get_signature_tables(["Signature 1",'
            ' "Signature 2"])</font></b>',
            tables)

        # two sigs, both horizontal
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2'], horizontal=True)
        data = self.add_tables(
            data,
            '<br /><b>Two Signatures (horizontal=True):</b> '
            '<font face="Times">get_signature_tables('
            '["Sig 1", "Sig 2"], horizontal=True)</font>',
            tables)

        # two sigs, both vertical
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2'], horizontal=False)
        data = self.add_tables(
            data,
            '<br /><b>Two Signatures (vertical, horizontal=False):</b> '
            '<font face="Times">get_signature_tables('
            '["Sig 1", "Sig 2"], horizontal=False)</font>',
            tables)


        data += [PageBreak(), Paragraph(
            '<br /><br /><font size="14"><font face="Times">max_per_row</font>'
            ' Parameter: </b><br />',
            NORMAL_STYLE)]

        # four signature (default)
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2', 'Sig 3', 'Sig 4'])
        data = self.add_tables(
            data,
            '<br /><b>Four Sigs (default, max_per_row=3):</b> '
            '<font face="Times">get_signature_tables('
            '["Sig 1", "Sig 2", "Sig 3", "Sig 4"])</font>',
            tables)

        # four signature (max_per_row=1)
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2', 'Sig 3', 'Sig 4'], max_per_row=1)

        data = self.add_tables(
            data,
            '<br /><b>Four Sigs (max_per_row=1):</b> '
            '<font face="Times">get_signature_tables('
            '["Sig 1", "Sig 2", "Sig 3", "Sig 4"], max_per_row=1)</font>'
            '<br /><i>Please note: mode switches from vertical to '
            'horizontal automatically</i>',
            tables)

        # four signature (max_per_row=2)
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2', 'Sig 3', 'Sig 4'], max_per_row=2)
        data = self.add_tables(
            data,
            '<br /><b>Four Sigs (max_per_row=2):</b> '
            '<font face="Times">get_signature_tables('
            '["Sig 1", "Sig 2", "Sig 3", "Sig 4"], max_per_row=2)</font>',
            tables)

        data += [PageBreak()]

        # four signature (max_per_row=4)
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2', 'Sig 3', 'Sig 4'], max_per_row=4)
        data = self.add_tables(
            data,
            '<b>Four Sigs (max_per_row=4):</b> '
            '<font face="Times">get_signature_tables('
            '["Sig 1", "Sig 2", "Sig 3", "Sig 4"], max_per_row=4)</font>',
            tables)

        # four signature (max_per_row=5)
        tables = get_signature_tables(
            ['Sig 1', 'Sig 2', 'Sig 3', 'Sig 4'], max_per_row=5)
        data = self.add_tables(
            data,
            '<br /><b>Four Sigs (max_per_row=5):</b> '
            '<font face="Times">get_signature_tables('
            '["Sig 1", "Sig 2", "Sig 3", "Sig 4"], max_per_row=5)</font>',
            tables)


        # create PDF from data
        path = draw_sample_pdf(data, title=u"Signatures Sample Sheet")
        print "Sample PDF written to %s" % path
        return
