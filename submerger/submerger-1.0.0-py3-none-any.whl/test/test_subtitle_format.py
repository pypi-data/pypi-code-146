import unittest

from submerger.subtitle_format import SubtitleFormat


TEXT = '''
SOME TEXT  
Якийсь текст 
óõõ
¥ · £ · € · $ · ¢ · ₡ · ₢ · ₣ · ₤ · ₥ · ₦ · ₧ · ₨ · ₩ · ₪ · ₫ · ₭ · ₮ · ₯ · ₹  
ᚠᛇᚻ᛫ᛒᛦᚦ᛫ᚠᚱᚩᚠᚢᚱ᛫ᚠᛁᚱᚪ᛫ᚷᛖᚻᚹᛦᛚᚳᚢᛗ
ඞ
'''


class TestSubtitleFormat(unittest.TestCase):
    def test_text_does_not_change_without_specifying_format(self):
        self.assertEqual(
            SubtitleFormat().format(TEXT),
            TEXT,
        )

    def test_format(self):
        self.assertEqual(
            SubtitleFormat().set_italic().set_position(
                SubtitleFormat.Position.TOP_CENTER).set_color('#333').format(TEXT),
            fr'<font color=#333><i>{{\an8}}{TEXT}</i></font>',
        )
        self.assertEqual(
            SubtitleFormat().set_italic().set_position(
                SubtitleFormat.Position.TOP_RIGHT).set_color('RED').format(TEXT),
            fr'<font color=RED><i>{{\an9}}{TEXT}</i></font>',
        )

    def test_format_idempotence(self):
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.TOP_CENTER).set_color(
                '#696969').set_position(SubtitleFormat.Position.BOTTOM_RIGHT).set_color(
                    '#333').set_italic().set_italic().set_italic().format(TEXT),
            fr'<font color=#333><i>{{\an3}}{TEXT}</i></font>',
        )

    def test_format_position(self):
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.BOTTOM_LEFT).format(TEXT),
            fr'{{\an1}}{TEXT}',
        )
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.BOTTOM_CENTER).format(TEXT),
            fr'{{\an2}}{TEXT}',
        )
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.BOTTOM_RIGHT).format(TEXT),
            fr'{{\an3}}{TEXT}',
        )
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.MIDDLE_LEFT).format(TEXT),
            fr'{{\an4}}{TEXT}',
        )
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.MIDDLE_CENTER).format(TEXT),
            fr'{{\an5}}{TEXT}',
        )
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.MIDDLE_RIGHT).format(TEXT),
            fr'{{\an6}}{TEXT}',
        )
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.TOP_LEFT).format(TEXT),
            fr'{{\an7}}{TEXT}',
        )
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.TOP_CENTER).format(TEXT),
            fr'{{\an8}}{TEXT}',
        )
        self.assertEqual(
            SubtitleFormat().set_position(SubtitleFormat.Position.TOP_RIGHT).format(TEXT),
            fr'{{\an9}}{TEXT}',
        )
