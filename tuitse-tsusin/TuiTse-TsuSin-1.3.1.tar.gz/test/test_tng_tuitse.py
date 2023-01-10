from django.test.testcases import TestCase

from tuitse import kiamtsa
from tuitse.html import tuitse_html


class TuaLiongTuiTse(TestCase):

    def test_tuitse(self):
        tsusin = kiamtsa(self.hanji, self.lomaji)
        tuitse_html(tsusin)

    hanji = (
        '法國人講華語日本人講一支咱臺灣人講臺語，咱遮是臺灣人的優待咱講臺語的今仔日的節目就留寡幫尊顏'
        '佇空中主持你等今仔日欲講的主題是野球啦岸的今仔日欲講的野球的是咧講往擺仔做囡仔時算野球的心適代'
        '往擺仔我咧做囡仔時捌一層咧hông拍野球蠟提準時兩-千空人咧臺灣通講全面倒咧風野球啊半暝仔變時陣的攏咧看王建民'
        '建築彼陣有建議改寫佮三月痟媽祖咧比蠟囡仔規陣的頭仔倒咧學校運動埕拍野球見若講拜六禮拜後攏全人咧神轎的啊人阿叔'
        '有夠攑刀組隊咧比賽幾若間學校攏按呢啦彼陣阮這陣囡仔伴鑼鼓陣拜六禮拜小弟使用sī-la-iah拍球擔上蓋期待拜六禮拜'
        '阮擔欲來拍野球我一家囡仔攏佇運動埕中央彼塊艱苦的草埔遐拍球擔這陣就一寡跑道咧散步的阿伯阿姆來咧齪嘈遐阿伯阿姆'
        '三不五時就來欲共講寡無愛予阮逐个拍球講阮逐家拍球回響著會共𪜶極地上啊今你臭焦欲納稅金閣下草埔遐艱苦著阮囡仔人'
        '大歲叫若的計畫炮台來揣有藍圖攏佇塗跤咧冷矣欲共伊叫著傷仔按呢仔欲教員官實在有影共𪜶按呢共阮官官攏趕袂走啦允人'
        '我透早阮就共三代草木pha著你的尾仔，擋袂牢走去共收遐今我uan-ná被迫叫我卑鄙走來看我一塊囡仔有行捌踏入來為大路頭'
        '佮阮早後逝阮欲來圍牆仔共球拍甲一半故意類的彼相信位仔來話來啊目尾來共阮拖咧走代先受遐毒蛇乖的哪會攏斷無人買搖籃代表'
        '彼逝出一个絕招伊人猶未英台伊就漏水矣草埔遐流水啦一步示愛有影歇毋知綴一个天才也塗堆來流水欲按怎干焦彼箍水流閣較大港'
        '甲一半倚本壘按呢雄雄磅一聲蓋大聲烏白蛇滿四界投手刀仔去予你共看水流予我大港擔彼陣阮拄仔去予逐家看'
    )

    lomaji = (
        'Huat-kok lâng kóng huâ-gí ji̍t-pún-lâng kóng tsi̍t-ki lán tâi-uân-lâng kóng tâi-gí ,'
        ' lán tsia sī tâi-uân-lâng ê iu-thāi lán kóng tâi-gí ê kin-á-ji̍t ê tsiat-bo̍k tō lâu '
        'kuá png tsun gân tī khong-tiong tsú-tshî lí tán kin-á-ji̍t beh kóng ê tsú-tê sī iá-kiû'
        ' lah gān ê kin-á-ji̍t beh kóng ê iá-kiû ê sī leh kóng íng-pái á tsò gín-á-sî sǹg iá-kiû '
        'ê sim-sik tāi íng-pái á guá teh tsò gín-á-sî bat tsi̍t-tsàn teh hông phah iá-kiû la̍h thê '
        'tsún-sî nn̄g-tshing khong lâng-leh tâi-uân thang kóng tsuân-bīn tó-leh hong iá-kiû ah '
        'puànn-mê-á piàn sî-tsūn ê lóng leh khuànn ông-kiàn-bîn kiàn-tio̍k hit-tsūn ū kiàn-gī kái-siá '
        'kah sann-gue̍h siáu má-tsóo teh pí la̍h gín-á kui-tīn ê thâu-á tó-leh ha̍k-hāu ūn-tōng-tiânn '
        'phah iá-kiû kiàn-nā kóng pài-la̍k lé-pài āu lóng tsuân lâng-leh sîn-kiō ê a lâng a-tsik ū-kàu '
        'gia̍h to tsoo-tuī teh pí-sài kuí-nā king ha̍k-hāu lóng án-ne lah hit-tsūn guán tsit-tīn '
        'gín-á-phuānn lô kóo-tīn pài-la̍k lé-pài sió-tī sú-iōng sī-la-iah phah-kiû tann siāng-kài '
        'kî-thāi pài-la̍k lé-pài guán tann beh-lâi phah iá-kiû guá tsi̍t ke gín-á lóng tī ūn-tōng-tiânn '
        'tiong-ng hit tè kan-khóo ê tsháu-poo hia phah-kiû tann tsit-tsūn tō tsi̍t-kuá pháu-tō teh '
        'sàn-pōo ê a-peh a-ḿ lâi-leh tsak-tsō hia a-peh a-ḿ sam-put-gōo-sî tō lâi beh kā kóng-kuá bô-ài'
        ' hōo guán ta̍k-ê phah-kiû kóng guán ta̍k-ke phah-kiû huê-hiáng tio̍h ē kā in ki̍k tē-siōng ah tann'
        ' lí tshàu-ta beh la̍p suè-kim koh hē tsháu-poo hiah kan-khóo tio̍h guán gín-á-lâng tuā hè kiò '
        'ná ê kè-uē phàu-tâi lâi tshuē ū nâ-tôo lóng tī thôo-kha leh líng-ah beh kā-i kiò tio̍h-siong á'
        ' án-ne á beh kàu-uân kuann si̍t-tsāi ū-iánn kā in án-ne kā guán kuann kuann lóng kuánn bē tsáu'
        ' lah ín-lâng guá thàu-tsá guán tō kā sann-tāi tsháu-bo̍k pha tio̍h lí ê bué-á , tòng-bē-tiâu '
        'tsáu-khì kā siu hiah tann guá uan-ná pī-pik kiò guá pi-phí tsáu-lâi khuànn-guá tsi̍t-tè gín-á '
        'ū kiânn bat ta̍h ji̍p-lâi uī tuā-lōo-thâu kah guán tsá āu-tsuā guán beh lâi uî-tshiûnn-á kā kiû'
        ' phah kah tsi̍t-puànn kòo-ì luī ê hit siong-sìn uī-á lâi uē lâi a ba̍k-bué lâi kā gún thua leh '
        'tsáu tāi-sing siū hia to̍k-tsuâ kuai ê ná-ē lóng tn̄g bô-lâng bué iô-nâ tāi-piáu hit tsuā tshut '
        'tsi̍t-ê tsua̍t-tsiau i lâng á-bē ing-tâi i tō lāu-tsuí ah tsháu-poo hia lâu-tsuí lah tsi̍t-pōo '
        'sī-ài ū-iánn hioh m̄-tsai tuè tsi̍t-ê thian-tsâi iā thôo-tui lâi lâu-tsuí beh án-tsuánn kan-na '
        'hit-khoo tsuí-lâu koh-khah tuā-káng kah tsi̍t-puànn uá pún-luí án-ne hiông-hiông pōng tsi̍t-siann '
        'kài tuā-siann oo-pe̍h tsuâ muá-sì-kè tâu-tshiú to-á khì hōo lí kā khuànn tsuí-lâu hōo guá tuā-káng '
        'tann hit-tsūn guán tú-á khì hōo ta̍k-ke khuànn'
    )
