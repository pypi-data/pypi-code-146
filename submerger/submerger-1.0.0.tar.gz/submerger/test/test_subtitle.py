import datetime
import unittest

from submerger.subtitle import Subtitle


class TestSubtitleParsing(unittest.TestCase):
    def test_from_srt(self):
        expected = []
        expected.append(Subtitle(datetime.timedelta(
            seconds=1), datetime.timedelta(seconds=3),
            '''some
text
here
for
testing'''))

        actual = Subtitle.from_srt(f'1\n{str(expected[0])}')

        self.assertEqual(str(actual[0]), str(expected[0]))

    def test_to_srt(self):
        expected = '''1
00:01:00,000 --> 00:02:00,000
111

2
00:02:01,000 --> 00:03:00,000
222

3
00:03:00,000 --> 00:04:00,000
333

4
00:04:00,000 --> 00:05:00,000
444

5
00:05:00,000 --> 00:06:00,000
555

6
00:06:00,000 --> 00:07:00,000
666

7
00:07:00,000 --> 00:08:00,000
777

8
00:08:00,000 --> 00:09:00,000
888

9
01:00:00,000 --> 01:01:00,000
999

'''
        subtitle_list = []
        subtitle_list.extend(Subtitle.from_srt(expected))

        actual = Subtitle.to_srt(subtitle_list)

        self.assertEqual(actual, expected)
        self.assertListEqual(Subtitle.from_srt(actual),
                             Subtitle.from_srt(expected))

    def test___str__(self):
        actual1 = Subtitle(datetime.timedelta(
            seconds=123, milliseconds=456), datetime.timedelta(seconds=321, milliseconds=54),
            'some text')

        self.assertEqual(
            str(actual1), '00:02:03,456 --> 00:05:21,054\nsome text\n\n')

        actual2 = Subtitle(datetime.timedelta(
            seconds=1234, milliseconds=2), datetime.timedelta(seconds=4321),
            'some text')

        self.assertEqual(
            str(actual2), '00:20:34,002 --> 01:12:01,000\nsome text\n\n')
