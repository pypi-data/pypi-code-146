import unittest

from submerger.merge_subtitles import merge_subtitles
from submerger.subtitle_format import SubtitleFormat


class TestSubtitleMerging(unittest.TestCase):
    def test_merge_subtitles(self):
        self.assertEqual(merge_subtitles(
            '''1
00:00:08,833 --> 00:00:14,916
Black holes are considered to be
the hellmouths of the universe.

2
00:00:15,625 --> 00:00:19,083
Those who fall inside disappear.

3
00:00:19,791 --> 00:00:20,625
Forever.

4
00:00:25,000 --> 00:00:26,625
But whereto?

''',
            SubtitleFormat().set_position(SubtitleFormat.Position.BOTTOM_CENTER),
            '''1
00:00:08,833 --> 00:00:14,916
[Wissenschaftler]  Schwarze Löcher gelten
als die Höllenschlunde des Universums.

2
00:00:15,625 --> 00:00:19,708
Wer hineinfällt, verschwindet.

3
00:00:19,791 --> 00:00:21,458
Für immer.

4
00:00:25,000 --> 00:00:26,625
Aber wohin?

''',
            SubtitleFormat().set_position(
                SubtitleFormat.Position.TOP_CENTER).set_color('#333').set_italic(),
        ),
            r'''1
00:00:08,833 --> 00:00:14,916
{\an2}Black holes are considered to be
the hellmouths of the universe.

2
00:00:08,833 --> 00:00:14,916
<font color=#333><i>{\an8}[Wissenschaftler]  Schwarze Löcher gelten
als die Höllenschlunde des Universums.</i></font>

3
00:00:15,625 --> 00:00:19,083
{\an2}Those who fall inside disappear.

4
00:00:15,625 --> 00:00:19,708
<font color=#333><i>{\an8}Wer hineinfällt, verschwindet.</i></font>

5
00:00:19,791 --> 00:00:20,625
{\an2}Forever.

6
00:00:19,791 --> 00:00:21,458
<font color=#333><i>{\an8}Für immer.</i></font>

7
00:00:25,000 --> 00:00:26,625
{\an2}But whereto?

8
00:00:25,000 --> 00:00:26,625
<font color=#333><i>{\an8}Aber wohin?</i></font>

'''
        )
