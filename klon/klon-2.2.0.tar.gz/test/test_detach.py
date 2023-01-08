#!/usr/bin/env python3

# standards
import re

# klon
from klon import detach, parse_html_etree, tostring


def _dedent(text):
    """ Remove text indentation. Unlike `textwrap.dedent`, preserve empty lines """
    text = text.lstrip('\n').rstrip()
    indent = re.search(r'^ +', text)[0]
    return re.sub(fr'^{indent}', '', text, flags=re.M)


def test_detach():
    doc = parse_html_etree(
        _dedent('''
          <html>
            <body>
              First:
              <p>This is the <b>first </b>paragraph.</p>
              Second:
              <p><em>This</em> is the <i>second </i>paragraph</p>
            </body>
          </html>
        ''')
    )

    # Here the detached node's `tail` is reattached to the paren't text
    detach(doc.xpath('//p/b')[0])
    assert tostring(doc) == _dedent('''
        <html>
          <body>
            First:
            <p>This is the paragraph.</p>
            Second:
            <p><em>This</em> is the <i>second </i>paragraph</p>
          </body>
        </html>
    ''')

    # Whitespace around the detached node is preserved
    detach(doc.xpath('//p')[0])
    assert tostring(doc) == _dedent('''
        <html>
          <body>
            First:
            
            Second:
            <p><em>This</em> is the <i>second </i>paragraph</p>
          </body>
        </html>
    ''')

    # The previous sibling's `tail` gets concatenated with the detached node's `tail`
    detach(doc.xpath('//p/i')[0])
    assert tostring(doc) == _dedent('''
        <html>
          <body>
            First:
            
            Second:
            <p><em>This</em> is the paragraph</p>
          </body>
        </html>
    ''')
