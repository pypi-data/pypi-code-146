# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from enum import Enum

__NAMESPACE__ = "http://textgrid.info/namespaces/metadata/script/2010"


class FormOfNotationType(Enum):
    """Set of characters and/or symbols used to express the content of a
    resource.

    Same as: http://rdvocab.info/Elements/formOfNotation.

    Attributes
        ARAB: Arabic
        ARMI: Imperial Aramaic
        ARMN: Armenian
        AVST: Avestan
        BALI: Balinese
        BAMU: Bamum
        BASS: Bassa Vah
        BATK: Batak
        BENG: Bengali
        BLIS: Blissymbols
        BOPO: Bopomofo
        BRAH: Brahmi
        BRAI: Braille
        BUGI: Buginese
        BUHD: Buhid
        CAKM: Chakma
        CANS: Unified Canadian Aboriginal Syllabics
        CARI: Carian
        CHAM: Cham
        CHER: Cherokee
        CIRT: Cirth
        COPT: Coptic
        CPRT: Cypriot
        CYRL: Cyrillic
        CYRS: Cyrillic (Old Church Slavonic variant)
        DEVA: Devanagari (Nagari)
        DSRT: Deseret (Mormon)
        EGYD: Egyptian demotic
        EGYH: Egyptian hieratic
        EGYP: Egyptian hieroglyphs
        ETHI: Ethiopic (Geʻez)
        GEOR: Georgian (Mkhedruli)
        GEOK: Khutsuri (Asomtavruli and Nuskhuri)
        GLAG: Glagolitic
        GOTH: Gothic
        GRAN: Grantha
        GREK: Greek
        GUJR: Gujarati
        GURU: Gurmukhi
        HANG: Hangul (Hangŭl, Hangeul)
        HANI: Han (Hanzi, Kanji, Hanja)
        HANO: Hanunoo (Hanunóo)
        HANS: Han (Simplified variant)
        HANT: Han (Traditional variant)
        HEBR: Hebrew
        HIRA: Hiragana
        HMNG: Pahawh Hmong
        HRKT: (alias for Hiragana + Katakana)
        HUNG: Old Hungarian
        INDS: Indus (Harappan)
        ITAL: Old Italic (Etruscan, Oscan, etc.)
        JAVA: Javanese
        JPAN: Japanese (alias for Han + Hiragana + Katakana)
        KALI: Kayah Li
        KANA: Katakana
        KHAR: Kharoshthi
        KHMR: Khmer
        KNDA: Kannada
        KORE: Korean (alias for Hangul + Han)
        KPEL: Kpelle
        KTHI: Kaithi
        LANA: Tai Tham (Lanna)
        LAOO: Lao
        LATF: Latin (Fraktur variant)
        LATG: Latin (Gaelic variant)
        LATN: Latin
        LEPC: Lepcha (Róng)
        LIMB: Limbu
        LINA: Linear A
        LINB: Linear B
        LISU: Lisu (Fraser)
        LOMA: Loma
        LYCI: Lycian
        LYDI: Lydian
        MAND: Mandaic, Mandaean
        MANI: Manichaean
        MAYA: Mayan hieroglyphs
        MEND: Mende
        MERC: Meroitic Cursive
        MERO: Meroitic Hieroglyphs
        MLYM: Malayalam
        MOON: Moon (Moon code, Moon script, Moon type)
        MONG: Mongolian
        MTEI: Meitei Mayek (Meithei, Meetei)
        MYMR: Myanmar (Burmese)
        NARB: Old North Arabian (Ancient North Arabian)
        NBAT: Nabataean
        NKGB: Nakhi Geba ('Na-'Khi ²Ggŏ-¹baw, Naxi Geba)
        NKOO: N’Ko
        OGAM: Ogham
        OLCK: Ol Chiki (Ol Cemet’, Ol, Santali)
        ORKH: Old Turkic, Orkhon Runic
        ORYA: Oriya
        OSMA: Osmanya
        PALM: Palmyrene
        PERM: Old Permic
        PHAG: Phags-pa
        PHLI: Inscriptional Pahlavi
        PHLP: Psalter Pahlavi
        PHLV: Book Pahlavi
        PHNX: Phoenician
        PLRD: Miao (Pollard)
        PRTI: Inscriptional Parthian
        QAAA: Reserved for private use (start)
        QABX: Reserved for private use (end)
        RJNG: Rejang (Redjang, Kaganga)
        RORO: Rongorongo
        RUNR: Runic
        SAMR: Samaritan
        SARA: Sarati
        SARB: Old South Arabian
        SAUR: Saurashtra
        SGNW: SignWriting
        SHAW: Shavian (Shaw)
        SINH: Sinhala
        SUND: Sundanese
        SYLO: Syloti Nagri
        SYRC: Syriac
        SYRE: Syriac (Estrangelo variant)
        SYRJ: Syriac (Western variant)
        SYRN: Syriac (Eastern variant)
        TAGB: Tagbanwa
        TALE: Tai Le
        TALU: New Tai Lue
        TAML: Tamil
        TAVT: Tai Viet
        TELU: Telugu
        TENG: Tengwar
        TFNG: Tifinagh (Berber)
        TGLG: Tagalog (Baybayin, Alibata)
        THAA: Thaana
        THAI: Thai
        TIBT: Tibetan
        UGAR: Ugaritic
        VAII: Vai
        VISP: Visible Speech
        WARA: Warang Citi (Varang Kshiti)
        XPEO: Old Persian
        XSUX: Cuneiform, Sumero-Akkadian
        YIII: Yi
        ZINH: Code for inherited script
        ZMTH: Mathematical notation
        ZSYM: Symbols
        ZXXX: Code for unwritten documents
        ZYYY: Code for undetermined script
        ZZZZ: Code for uncoded script
    """
    ARAB = "Arab"
    ARMI = "Armi"
    ARMN = "Armn"
    AVST = "Avst"
    BALI = "Bali"
    BAMU = "Bamu"
    BASS = "Bass"
    BATK = "Batk"
    BENG = "Beng"
    BLIS = "Blis"
    BOPO = "Bopo"
    BRAH = "Brah"
    BRAI = "Brai"
    BUGI = "Bugi"
    BUHD = "Buhd"
    CAKM = "Cakm"
    CANS = "Cans"
    CARI = "Cari"
    CHAM = "Cham"
    CHER = "Cher"
    CIRT = "Cirt"
    COPT = "Copt"
    CPRT = "Cprt"
    CYRL = "Cyrl"
    CYRS = "Cyrs"
    DEVA = "Deva"
    DSRT = "Dsrt"
    EGYD = "Egyd"
    EGYH = "Egyh"
    EGYP = "Egyp"
    ETHI = "Ethi"
    GEOR = "Geor"
    GEOK = "Geok"
    GLAG = "Glag"
    GOTH = "Goth"
    GRAN = "Gran"
    GREK = "Grek"
    GUJR = "Gujr"
    GURU = "Guru"
    HANG = "Hang"
    HANI = "Hani"
    HANO = "Hano"
    HANS = "Hans"
    HANT = "Hant"
    HEBR = "Hebr"
    HIRA = "Hira"
    HMNG = "Hmng"
    HRKT = "Hrkt"
    HUNG = "Hung"
    INDS = "Inds"
    ITAL = "Ital"
    JAVA = "Java"
    JPAN = "Jpan"
    KALI = "Kali"
    KANA = "Kana"
    KHAR = "Khar"
    KHMR = "Khmr"
    KNDA = "Knda"
    KORE = "Kore"
    KPEL = "Kpel"
    KTHI = "Kthi"
    LANA = "Lana"
    LAOO = "Laoo"
    LATF = "Latf"
    LATG = "Latg"
    LATN = "Latn"
    LEPC = "Lepc"
    LIMB = "Limb"
    LINA = "Lina"
    LINB = "Linb"
    LISU = "Lisu"
    LOMA = "Loma"
    LYCI = "Lyci"
    LYDI = "Lydi"
    MAND = "Mand"
    MANI = "Mani"
    MAYA = "Maya"
    MEND = "Mend"
    MERC = "Merc"
    MERO = "Mero"
    MLYM = "Mlym"
    MOON = "Moon"
    MONG = "Mong"
    MTEI = "Mtei"
    MYMR = "Mymr"
    NARB = "Narb"
    NBAT = "Nbat"
    NKGB = "Nkgb"
    NKOO = "Nkoo"
    OGAM = "Ogam"
    OLCK = "Olck"
    ORKH = "Orkh"
    ORYA = "Orya"
    OSMA = "Osma"
    PALM = "Palm"
    PERM = "Perm"
    PHAG = "Phag"
    PHLI = "Phli"
    PHLP = "Phlp"
    PHLV = "Phlv"
    PHNX = "Phnx"
    PLRD = "Plrd"
    PRTI = "Prti"
    QAAA = "Qaaa"
    QABX = "Qabx"
    RJNG = "Rjng"
    RORO = "Roro"
    RUNR = "Runr"
    SAMR = "Samr"
    SARA = "Sara"
    SARB = "Sarb"
    SAUR = "Saur"
    SGNW = "Sgnw"
    SHAW = "Shaw"
    SINH = "Sinh"
    SUND = "Sund"
    SYLO = "Sylo"
    SYRC = "Syrc"
    SYRE = "Syre"
    SYRJ = "Syrj"
    SYRN = "Syrn"
    TAGB = "Tagb"
    TALE = "Tale"
    TALU = "Talu"
    TAML = "Taml"
    TAVT = "Tavt"
    TELU = "Telu"
    TENG = "Teng"
    TFNG = "Tfng"
    TGLG = "Tglg"
    THAA = "Thaa"
    THAI = "Thai"
    TIBT = "Tibt"
    UGAR = "Ugar"
    VAII = "Vaii"
    VISP = "Visp"
    WARA = "Wara"
    XPEO = "Xpeo"
    XSUX = "Xsux"
    YIII = "Yiii"
    ZINH = "Zinh"
    ZMTH = "Zmth"
    ZSYM = "Zsym"
    ZXXX = "Zxxx"
    ZYYY = "Zyyy"
    ZZZZ = "Zzzz"
