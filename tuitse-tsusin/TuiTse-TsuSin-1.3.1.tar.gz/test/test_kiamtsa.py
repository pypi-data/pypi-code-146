from django.test.testcases import TestCase
from tuitse import THAU_JI, LIAN_JI, KHIN_SIANN_JI
from tuitse import kiamtsa


class MockTshigiam(TestCase):

    def test_u_tsitji(self):
        hanji = '「'
        lomaji = 'ˮ'

        def hamsik_tsitji_ubo(x):
            return True
        kiatko = kiamtsa(hanji, lomaji, hamsik_tsitji_ubo)
        self.assertTrue(kiatko[0][3])


class KangJiSooTshiGiam(TestCase):
    def tearDown(self):
        kiat_ko = kiamtsa(self.hanji, self.lomaji)
        self.assertEqual(kiat_ko, self.bang)

    def test_ok_我(self):
        self.hanji = '我'
        self.lomaji = 'guá'
        self.bang = [
            ('我', 'guá', THAU_JI, True),
        ]

    def test_bo_tuitang_好_bái(self):
        self.hanji = '好'
        self.lomaji = 'bái'
        self.bang = [
            ('好', 'bái', THAU_JI, False),
        ]

    def test_hanlo_芳kongkong(self):
        self.hanji = '芳kòng-kòng'
        self.lomaji = 'phang-kòng-kòng'
        self.bang = [
            ('芳', 'phang', THAU_JI, True),
            ('kòng', 'kòng', LIAN_JI, True),
            ('kòng', 'kòng', LIAN_JI, True),
        ]

    def test_hanlo_kinnkinn叫_羅馬字有漢字代表是華文(self):
        self.hanji = 'kinn-kinn叫'
        self.lomaji = 'kinn-kinn叫'
        self.bang = [
            ('kinn', 'kinn', THAU_JI, True),
            ('kinn', 'kinn', LIAN_JI, True),
            ('叫', '叫', THAU_JI, True),
        ]

    def test_tiongng_bo_tuitang_行轉去(self):
        self.hanji = '行轉去'
        self.lomaji = 'kiânn--ng-i'
        self.bang = [
            ('行', 'kiânn', THAU_JI, True),
            ('轉', 'ng', KHIN_SIANN_JI, False),
            ('去', 'i', LIAN_JI, False),
        ]

    def test_nng_su(self):
        self.hanji = '真好'
        self.lomaji = 'tsin hó'
        self.bang = [
            ('真', 'tsin', THAU_JI, True),
            ('好', 'hó', THAU_JI, True),
        ]

    def test_huagi_su_帥哥(self):
        self.hanji = '帥哥'
        self.lomaji = '帥哥'
        self.bang = [
            ('帥', '帥', THAU_JI, True),
            ('哥', '哥', LIAN_JI, True),
        ]

    def test_inggi_su_Pig(self):
        self.hanji = 'Pig'
        self.lomaji = 'Pig'
        self.bang = [
            ('Pig', 'Pig', THAU_JI, True),
        ]

    def test_sooji_33(self):
        self.hanji = '33'
        self.lomaji = '33'
        self.bang = [
            ('33', '33', THAU_JI, False),
        ]

    def test_phiautiam(self):
        self.hanji = '「'
        self.lomaji = ','
        self.bang = [
            ('「', ',', THAU_JI, False),
        ]

    def test_han_ma_khinsiann(self):
        self.hanji = '予--in'
        self.lomaji = 'hōo--in'
        self.bang = [
            ('予', 'hōo', THAU_JI, True),
            ('in', 'in', KHIN_SIANN_JI, True),
        ]

    def test_han_bo_khinsiann(self):
        self.hanji = '予in'
        self.lomaji = 'hōo--in'
        self.bang = [
            ('予', 'hōo', THAU_JI, True),
            ('in', 'in', KHIN_SIANN_JI, True),
        ]


class BoKangJiSooTshiGiam(TestCase):
    def tearDown(self):
        kiat_ko = kiamtsa(self.hanji, self.lomaji)
        self.assertEqual(kiat_ko, self.bang)

    def test_khiam_hanji_姑_kooniû(self):
        self.hanji = '姑'
        self.lomaji = 'koo-niû'
        self.bang = [
            ('姑', 'koo', THAU_JI, True),
            ('', 'niû', LIAN_JI, False),
        ]

    def test_khiam_hanji_姑_suí_koo(self):
        self.hanji = '姑'
        self.lomaji = 'suí koo'
        self.bang = [
            ('', 'suí', THAU_JI, False),
            ('姑', 'koo', THAU_JI, True),
        ]

    def test_khiam_lomaji_姑娘_niû(self):
        self.hanji = '姑娘'
        self.lomaji = 'niû'
        self.bang = [
            ('姑', '', THAU_JI, False),
            ('娘', 'niû', THAU_JI, True),
        ]

    def test_khiam_lomaji_媠姑娘_suí_niû(self):
        self.hanji = '媠姑娘'
        self.lomaji = 'suí niû'
        self.bang = [
            ('媠', 'suí', THAU_JI, True),
            ('姑', '', THAU_JI, False),
            ('娘', 'niû', THAU_JI, True),
        ]

    def test_bo_tuitang_媠姑娘_suíniû(self):
        self.hanji = '媠姑娘'
        self.lomaji = 'suí-niû'
        self.bang = [
            ('媠', 'suí', THAU_JI, True),
            ('姑', '', LIAN_JI, False),
            ('娘', 'niû', LIAN_JI, True),
        ]

    def test_khiam_hanji_tiongng_媠娘_suíkooniû(self):
        self.hanji = '媠娘'
        self.lomaji = 'suí-koo-niû'
        self.bang = [
            ('媠', 'suí', THAU_JI, True),
            ('', 'koo', LIAN_JI, False),
            ('娘', 'niû', LIAN_JI, True),
        ]

    def test_bo_tuitang_歡歡喜喜(self):
        self.hanji = '歡歡喜喜'
        self.lomaji = 'huann-hí'
        self.bang = [
            ('歡', 'huann', THAU_JI, True),
            ('歡', '', LIAN_JI, False),
            ('喜', 'hí', LIAN_JI, True),
            ('喜', '', THAU_JI, False),
        ]

    def test_nng_su_真好(self):
        self.hanji = '真好'
        self.lomaji = 'hó'
        self.bang = [
            ('真', '', THAU_JI, False),
            ('好', 'hó', THAU_JI, True),
        ]

    def test_huagi_su_帥哥(self):
        self.hanji = '帥哥'
        self.lomaji = '帥'
        self.bang = [
            ('帥', '帥', THAU_JI, True),
            ('哥', '', THAU_JI, False),
        ]

    def test_long_tui_bo_梳妝打扮(self):
        self.hanji = '梳妝打扮'
        self.lomaji = 'se-tsan'
        self.bang = [
            ('梳', 'se', THAU_JI, True),
            ('妝', 'tsan', LIAN_JI, False),
            ('打', '', THAU_JI, False),
            ('扮', '', THAU_JI, False),
        ]

    def test_tianto_豬仔(self):
        # 筆記：這个試驗是欲保證選著siōng ē hô--ê
        #
        # 豬仔
        #   á-ti  => 1 ok, 0 fake_couple, 2 orphan
        #
        # 豬仔
        # á-ti  => 0 ok, 2 fake_couple, 0 orphan
        #
        self.hanji = '豬仔'
        self.lomaji = 'á-ti'
        self.bang = [
            ('豬', '', THAU_JI, False),
            ('仔', 'á', THAU_JI, True),
            ('', 'ti', LIAN_JI, False),
        ]

    def test_bunpehim_个的(self):
        # 筆記：這个試驗是欲保證選著siōng ē hô--ê
        # 个 的
        # ti̍k ê  => 1 ok, 1 fake_couple
        #
        # 个的
        #   ti̍k ê  => 1 ok, 0 fake_couple, 2 orphan
        #
        self.hanji = '个的'
        self.lomaji = 'ti̍k ê'
        self.bang = [
            ('个', 'ti̍k', THAU_JI, False),
            ('的', 'ê', THAU_JI, True),
        ]

    def test_sooji_tui_lomaji_33_sanntsapsann(self):
        self.hanji = '33'
        self.lomaji = 'sann-tsa̍p-sann'
        self.bang = [
            ('33', 'sann', THAU_JI, False),
            ('', 'tsa̍p', LIAN_JI, False),
            ('', 'sann', LIAN_JI, False),
        ]

    def test_hanji_tui_sooji_33(self):
        self.hanji = '三十三'
        self.lomaji = '33'
        self.bang = [
            ('三', '33', THAU_JI, False),
            ('十', '', THAU_JI, False),
            ('三', '', THAU_JI, False),
        ]

    def test_phiautiam(self):
        self.hanji = '「九月'
        self.lomaji = 'káu-gue̍h'
        self.bang = [
            ('「', '', THAU_JI, False),
            ('九', 'káu', THAU_JI, True),
            ('月', 'gue̍h', LIAN_JI, True),
        ]
