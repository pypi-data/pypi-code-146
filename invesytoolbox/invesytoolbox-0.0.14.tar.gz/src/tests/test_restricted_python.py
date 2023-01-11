# coding=utf-8
"""
run the test from the sr/invesytoolbox directory:
python ../tests/test_text_name.py
"""

import sys
import unittest

sys.path.append(".")

from itb_restricted_python import \
    prettify_html

html_raw = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

html_pretty = """<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The Dormouse's story
   </b>
  </p>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
   </a>
   ,
   <a class="sister" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister" href="http://example.com/tillie" id="link3">
    Tillie
   </a>
   ;
and they lived at the bottom of a well.
  </p>
  <p class="story">
   ...
  </p>
 </body>
</html>"""


class TestRestrictedPython(unittest.TestCase):
    def test_prettify_html(self) -> str:
        html_prettified = prettify_html(html_raw)
        self.assertEqual(
            html_prettified,
            html_pretty
        )


if __name__ == '__main__':
    unittest.main()
