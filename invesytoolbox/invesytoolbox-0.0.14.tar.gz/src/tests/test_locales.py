# coding=utf-8
"""
run the test from the sr/invesytoolbox directory:
python ../tests/test_country_language.py
"""

import sys
import unittest
import datetime
import DateTime

sys.path.append(".")

from itb_locales import \
    fetch_all_countries, \
    fetch_holidays, \
    format_price, \
    get_country, \
    get_language_name, \
    get_locale, \
    is_holiday

test_locale = ('de_AT', 'UTF-8')
locale_dict = {
    'locale': ('de_AT', 'UTF-8'),
    'locale_str': 'de_AT',
    'language': 'de',
    'country': 'AT',
    'currency': 'EUR'
}

check_all_countries = [
    ('AF', 'Afghanistan', 'Afghanistan'),
    ('EG', 'Ägypten', 'Agypten'),
    ('AL', 'Albanien', 'Albanien'),
    ('DZ', 'Algerien', 'Algerien'),
    ('AS', 'Amerikanisch-Samoa', 'Amerikanisch-Samoa'),
    ('VI', 'Amerikanische Jungferninseln', 'Amerikanische Jungferninseln'),
    ('AD', 'Andorra', 'Andorra'),
    ('AO', 'Angola', 'Angola'),
    ('AI', 'Anguilla', 'Anguilla'),
    ('AQ', 'Antarktis', 'Antarktis'),
    ('AG', 'Antigua und Barbuda', 'Antigua und Barbuda'),
    ('GQ', 'Äquatorialguinea', 'Aquatorialguinea'),
    ('AR', 'Argentinien', 'Argentinien'),
    ('AM', 'Armenien', 'Armenien'),
    ('AW', 'Aruba', 'Aruba'),
    ('AZ', 'Aserbaidschan', 'Aserbaidschan'),
    ('ET', 'Äthiopien', 'Athiopien'),
    ('AU', 'Australien', 'Australien'),
    ('BS', 'Bahamas', 'Bahamas'),
    ('BH', 'Bahrain', 'Bahrain'),
    ('BD', 'Bangladesch', 'Bangladesch'),
    ('BB', 'Barbados', 'Barbados'),
    ('BE', 'Belgien', 'Belgien'),
    ('BZ', 'Belize', 'Belize'),
    ('BJ', 'Benin', 'Benin'),
    ('BM', 'Bermuda', 'Bermuda'),
    ('BT', 'Bhutan', 'Bhutan'),
    ('BO', 'Bolivien, Plurinationaler Staat', 'Bolivien, Plurinationaler Staat'),
    ('BQ', 'Bonaire, Sint Eustatius und Saba', 'Bonaire, Sint Eustatius und Saba'),
    ('BA', 'Bosnien und Herzegowina', 'Bosnien und Herzegowina'),
    ('BW', 'Botsuana', 'Botsuana'),
    ('BV', 'Bouvet-Insel', 'Bouvet-Insel'),
    ('BR', 'Brasilien', 'Brasilien'),
    ('VG', 'Britische Jungferninseln', 'Britische Jungferninseln'),
    ('IO', 'Britisches Territorium im Indischen Ozean', 'Britisches Territorium im Indischen Ozean'),
    ('BN', 'Brunei Darussalam', 'Brunei Darussalam'),
    ('BG', 'Bulgarien', 'Bulgarien'),
    ('BF', 'Burkina Faso', 'Burkina Faso'),
    ('BI', 'Burundi', 'Burundi'),
    ('CV', 'Cabo Verde', 'Cabo Verde'),
    ('KY', 'Cayman-Inseln', 'Cayman-Inseln'),
    ('CL', 'Chile', 'Chile'),
    ('CN', 'China', 'China'),
    ('CK', 'Cookinseln', 'Cookinseln'),
    ('CR', 'Costa Rica', 'Costa Rica'),
    ('CI', "Côte d'Ivoire", "Cote d'Ivoire"),
    ('CW', 'Curaçao', 'Curacao'),
    ('CZ', 'Czechia', 'Czechia'),
    ('DK', 'Dänemark', 'Danemark'),
    ('CD', 'Demokratische Republik Kongo', 'Demokratische Republik Kongo'),
    ('DE', 'Deutschland', 'Deutschland'),
    ('DM', 'Dominica', 'Dominica'),
    ('DO', 'Dominikanische Republik', 'Dominikanische Republik'),
    ('DJ', 'Dschibuti', 'Dschibuti'),
    ('EC', 'Ecuador', 'Ecuador'),
    ('SV', 'El Salvador', 'El Salvador'),
    ('ER', 'Eritrea', 'Eritrea'),
    ('EE', 'Estland', 'Estland'),
    ('SZ', 'Eswatini', 'Eswatini'),
    ('FK', 'Falklandinseln (Malwinen)', 'Falklandinseln (Malwinen)'),
    ('FO', 'Färöer-Inseln', 'Faroer-Inseln'),
    ('FJ', 'Fidschi', 'Fidschi'),
    ('FI', 'Finnland', 'Finnland'),
    ('FR', 'Frankreich', 'Frankreich'),
    ('GF', 'Französisch-Guyana', 'Franzosisch-Guyana'),
    ('PF', 'Französisch-Polynesien', 'Franzosisch-Polynesien'),
    ('TF', 'Französische Süd- und Antarktisgebiete', 'Franzosische Sud- und Antarktisgebiete'),
    ('GA', 'Gabun', 'Gabun'),
    ('GM', 'Gambia', 'Gambia'),
    ('GE', 'Georgien', 'Georgien'),
    ('GH', 'Ghana', 'Ghana'),
    ('GI', 'Gibraltar', 'Gibraltar'),
    ('GD', 'Grenada', 'Grenada'),
    ('GR', 'Griechenland', 'Griechenland'),
    ('GL', 'Grönland', 'Gronland'),
    ('GP', 'Guadeloupe', 'Guadeloupe'),
    ('GU', 'Guam', 'Guam'),
    ('GT', 'Guatemala', 'Guatemala'),
    ('GG', 'Guernsey', 'Guernsey'),
    ('GN', 'Guinea', 'Guinea'),
    ('GW', 'Guinea-Bissau', 'Guinea-Bissau'),
    ('GY', 'Guyana', 'Guyana'),
    ('HT', 'Haiti', 'Haiti'),
    ('HM', 'Heard und McDonaldinseln', 'Heard und McDonaldinseln'),
    ('VA', 'Heiliger Stuhl (Staat Vatikanstadt)', 'Heiliger Stuhl (Staat Vatikanstadt)'),
    ('HN', 'Honduras', 'Honduras'),
    ('HK', 'Hongkong', 'Hongkong'),
    ('IN', 'Indien', 'Indien'),
    ('ID', 'Indonesien', 'Indonesien'),
    ('IM', 'Insel Man', 'Insel Man'),
    ('IQ', 'Irak', 'Irak'),
    ('IR', 'Iran, Islamische Republik', 'Iran, Islamische Republik'),
    ('IE', 'Irland', 'Irland'),
    ('IS', 'Island', 'Island'),
    ('IL', 'Israel', 'Israel'),
    ('IT', 'Italien', 'Italien'),
    ('JM', 'Jamaika', 'Jamaika'),
    ('JP', 'Japan', 'Japan'),
    ('YE', 'Jemen', 'Jemen'),
    ('JE', 'Jersey', 'Jersey'),
    ('JO', 'Jordanien', 'Jordanien'),
    ('KH', 'Kambodscha', 'Kambodscha'),
    ('CM', 'Kamerun', 'Kamerun'),
    ('CA', 'Kanada', 'Kanada'),
    ('KZ', 'Kasachstan', 'Kasachstan'),
    ('QA', 'Katar', 'Katar'),
    ('KE', 'Kenia', 'Kenia'),
    ('KG', 'Kirgisistan', 'Kirgisistan'),
    ('KI', 'Kiribati', 'Kiribati'),
    ('CC', 'Kokos-(Keeling-)Inseln', 'Kokos-(Keeling-)Inseln'),
    ('CO', 'Kolumbien', 'Kolumbien'),
    ('KM', 'Komoren', 'Komoren'),
    ('CG', 'Kongo', 'Kongo'),
    ('KP', 'Korea, Demokratische Volksrepublik', 'Korea, Demokratische Volksrepublik'),
    ('KR', 'Korea, Republik', 'Korea, Republik'),
    ('HR', 'Kroatien', 'Kroatien'),
    ('CU', 'Kuba', 'Kuba'),
    ('KW', 'Kuwait', 'Kuwait'),
    ('LA', 'Laos, Demokratische Volksrepublik', 'Laos, Demokratische Volksrepublik'),
    ('LS', 'Lesotho', 'Lesotho'),
    ('LV', 'Lettland', 'Lettland'),
    ('LB', 'Libanon', 'Libanon'),
    ('LR', 'Liberia', 'Liberia'),
    ('LY', 'Libyen', 'Libyen'),
    ('LI', 'Liechtenstein', 'Liechtenstein'),
    ('LT', 'Litauen', 'Litauen'),
    ('LU', 'Luxemburg', 'Luxemburg'),
    ('MO', 'Macao', 'Macao'),
    ('MG', 'Madagaskar', 'Madagaskar'),
    ('MW', 'Malawi', 'Malawi'),
    ('MY', 'Malaysia', 'Malaysia'),
    ('MV', 'Malediven', 'Malediven'),
    ('ML', 'Mali', 'Mali'),
    ('MT', 'Malta', 'Malta'),
    ('MA', 'Marokko', 'Marokko'),
    ('MH', 'Marshallinseln', 'Marshallinseln'),
    ('MQ', 'Martinique', 'Martinique'),
    ('MR', 'Mauretanien', 'Mauretanien'),
    ('MU', 'Mauritius', 'Mauritius'),
    ('YT', 'Mayotte', 'Mayotte'),
    ('MX', 'Mexiko', 'Mexiko'),
    ('FM', 'Mikronesien, Föderierte Staaten von', 'Mikronesien, Foderierte Staaten von'),
    ('MD', 'Moldau, Republik', 'Moldau, Republik'),
    ('MC', 'Monaco', 'Monaco'),
    ('MN', 'Mongolei', 'Mongolei'),
    ('ME', 'Montenegro', 'Montenegro'),
    ('MS', 'Montserrat', 'Montserrat'),
    ('MZ', 'Mosambik', 'Mosambik'),
    ('MM', 'Myanmar', 'Myanmar'),
    ('NA', 'Namibia', 'Namibia'),
    ('NR', 'Nauru', 'Nauru'),
    ('NP', 'Nepal', 'Nepal'),
    ('NC', 'Neukaledonien', 'Neukaledonien'),
    ('NZ', 'Neuseeland', 'Neuseeland'),
    ('NI', 'Nicaragua', 'Nicaragua'),
    ('NL', 'Niederlande', 'Niederlande'),
    ('NE', 'Niger', 'Niger'),
    ('NG', 'Nigeria', 'Nigeria'),
    ('NU', 'Niue', 'Niue'),
    ('MP', 'Nördliche Mariana-Inseln', 'Nordliche Mariana-Inseln'),
    ('NF', 'Norfolkinsel', 'Norfolkinsel'),
    ('MK', 'North Macedonia', 'North Macedonia'),
    ('NO', 'Norwegen', 'Norwegen'),
    ('OM', 'Oman', 'Oman'),
    ('AT', 'Österreich', 'Osterreich'),
    ('PK', 'Pakistan', 'Pakistan'),
    ('PS', 'Palästina, Staat', 'Palastina, Staat'),
    ('PW', 'Palau', 'Palau'),
    ('PA', 'Panama', 'Panama'),
    ('PG', 'Papua-Neuguinea', 'Papua-Neuguinea'),
    ('PY', 'Paraguay', 'Paraguay'),
    ('PE', 'Peru', 'Peru'),
    ('PH', 'Philippinen', 'Philippinen'),
    ('PN', 'Pitcairn', 'Pitcairn'),
    ('PL', 'Polen', 'Polen'),
    ('PT', 'Portugal', 'Portugal'),
    ('PR', 'Puerto Rico', 'Puerto Rico'),
    ('RE', 'Réunion', 'Reunion'),
    ('RW', 'Ruanda', 'Ruanda'),
    ('RO', 'Rumänien', 'Rumanien'),
    ('RU', 'Russische Föderation', 'Russische Foderation'),
    ('MF', 'Saint Martin (Französischer Teil)', 'Saint Martin (Franzosischer Teil)'),
    ('BL', 'Saint-Barthélemy', 'Saint-Barthelemy'),
    ('SX', 'Saint-Martin (Niederländischer Teil)', 'Saint-Martin (Niederlandischer Teil)'),
    ('SB', 'Salomoninseln', 'Salomoninseln'),
    ('ZM', 'Sambia', 'Sambia'),
    ('WS', 'Samoa', 'Samoa'),
    ('SM', 'San Marino', 'San Marino'),
    ('ST', 'São Tomé und Príncipe', 'Sao Tome und Principe'),
    ('SA', 'Saudi-Arabien', 'Saudi-Arabien'),
    ('SE', 'Schweden', 'Schweden'),
    ('CH', 'Schweiz', 'Schweiz'),
    ('SN', 'Senegal', 'Senegal'),
    ('RS', 'Serbien', 'Serbien'),
    ('SC', 'Seychellen', 'Seychellen'),
    ('SL', 'Sierra Leone', 'Sierra Leone'),
    ('ZW', 'Simbabwe', 'Simbabwe'),
    ('SG', 'Singapur', 'Singapur'),
    ('SK', 'Slowakei', 'Slowakei'),
    ('SI', 'Slowenien', 'Slowenien'),
    ('SO', 'Somalia', 'Somalia'),
    ('GS', 'South Georgia und die Südlichen Sandwichinseln', 'South Georgia und die Sudlichen Sandwichinseln'),
    ('ES', 'Spanien', 'Spanien'),
    ('LK', 'Sri Lanka', 'Sri Lanka'),
    ('SH', 'St. Helena, Ascension und Tristan da Cunha', 'St. Helena, Ascension und Tristan da Cunha'),
    ('KN', 'St. Kitts und Nevis', 'St. Kitts und Nevis'),
    ('LC', 'St. Lucia', 'St. Lucia'),
    ('PM', 'St. Pierre und Miquelon', 'St. Pierre und Miquelon'),
    ('VC', 'St. Vincent und die Grenadinen', 'St. Vincent und die Grenadinen'),
    ('ZA', 'Südafrika', 'Sudafrika'),
    ('SD', 'Sudan', 'Sudan'),
    ('SS', 'Südsudan', 'Sudsudan'),
    ('SR', 'Suriname', 'Suriname'),
    ('SJ', 'Svalbard und Jan Mayen', 'Svalbard und Jan Mayen'),
    ('SY', 'Syrien, Arabische Republik', 'Syrien, Arabische Republik'),
    ('TJ', 'Tadschikistan', 'Tadschikistan'),
    ('TW', 'Taiwan, Chinesische Provinz', 'Taiwan, Chinesische Provinz'),
    ('TZ', 'Tansania, Vereinigte Republik', 'Tansania, Vereinigte Republik'),
    ('TH', 'Thailand', 'Thailand'),
    ('TL', 'Timor-Leste', 'Timor-Leste'),
    ('TG', 'Togo', 'Togo'),
    ('TK', 'Tokelau', 'Tokelau'),
    ('TO', 'Tonga', 'Tonga'),
    ('TT', 'Trinidad und Tobago', 'Trinidad und Tobago'),
    ('TD', 'Tschad', 'Tschad'),
    ('TN', 'Tunesien', 'Tunesien'),
    ('TR', 'Türkei', 'Turkei'),
    ('TM', 'Turkmenistan', 'Turkmenistan'),
    ('TC', 'Turks- und Caicosinseln', 'Turks- und Caicosinseln'),
    ('TV', 'Tuvalu', 'Tuvalu'),
    ('UG', 'Uganda', 'Uganda'),
    ('UA', 'Ukraine', 'Ukraine'),
    ('HU', 'Ungarn', 'Ungarn'),
    ('UM', 'United States Minor Outlying Islands', 'United States Minor Outlying Islands'),
    ('UY', 'Uruguay', 'Uruguay'),
    ('UZ', 'Usbekistan', 'Usbekistan'),
    ('VU', 'Vanuatu', 'Vanuatu'),
    ('VE', 'Venezuela, Bolivarische Republik', 'Venezuela, Bolivarische Republik'),
    ('AE', 'Vereinigte Arabische Emirate', 'Vereinigte Arabische Emirate'),
    ('US', 'Vereinigte Staaten', 'Vereinigte Staaten'),
    ('GB', 'Vereinigtes Königreich', 'Vereinigtes Konigreich'),
    ('VN', 'Vietnam', 'Vietnam'),
    ('WF', 'Wallis und Futuna', 'Wallis und Futuna'),
    ('CX', 'Weihnachtsinseln', 'Weihnachtsinseln'),
    ('BY', 'Weißrussland', 'Weisrussland'),
    ('EH', 'Westsahara', 'Westsahara'),
    ('CF', 'Zentralafrikanische Republik', 'Zentralafrikanische Republik'),
    ('CY', 'Zypern', 'Zypern'),
    ('AX', 'Åland-Inseln', 'Åland-Inseln')
]

check_country = {
    'name': 'Österreich',
    'alpha_2': 'AT',
    'alpha_3': 'AUT',
    'numeric': '040',
    'official_name': 'Republic of Austria'
}

language_names = {
    'de': {
        'de': 'Deutsch',
        'fr': 'allemand',
        'en': 'German',
        'it': 'tedesco'
    },
    'fr': {
        'de': 'Französisch',
        'fr': 'français',
        'en': 'French',
        'it': 'francese'
    }
}

days_and_holidays = {
    '1.4.2020': False,
    '2022-05-01': True,
    '6.1.2023': True,
    '2023/6/1': False,
    '01/06/2023': True,
    '1/6/2023': True,
    '13.8.2022': False,
    datetime.date(2022, 5, 1): True,
    datetime.date(2022, 12, 11): False,
    datetime.datetime(2023, 1, 6): True,
    datetime.datetime(2023, 1, 11): False,
    DateTime.DateTime(2023, 1, 6): True,
    DateTime.DateTime(2023, 1, 11): False,
}

feiertage_2022_2023 = {
    datetime.date(2022, 1, 1): 'Neujahr',
    datetime.date(2022, 1, 6): 'Heilige Drei Könige',
    datetime.date(2022, 4, 18): 'Ostermontag',
    datetime.date(2022, 5, 1): 'Staatsfeiertag',
    datetime.date(2022, 5, 26): 'Christi Himmelfahrt',
    datetime.date(2022, 6, 6): 'Pfingstmontag',
    datetime.date(2022, 6, 16): 'Fronleichnam',
    datetime.date(2022, 8, 15): 'Mariä Himmelfahrt',
    datetime.date(2022, 10, 26): 'Nationalfeiertag',
    datetime.date(2022, 11, 1): 'Allerheiligen',
    datetime.date(2022, 12, 8): 'Mariä Empfängnis',
    datetime.date(2022, 12, 25): 'Christtag',
    datetime.date(2022, 12, 26): 'Stefanitag',
    datetime.date(2023, 1, 1): 'Neujahr',
    datetime.date(2023, 1, 6): 'Heilige Drei Könige',
    datetime.date(2023, 4, 10): 'Ostermontag',
    datetime.date(2023, 5, 1): 'Staatsfeiertag',
    datetime.date(2023, 5, 18): 'Christi Himmelfahrt',
    datetime.date(2023, 5, 29): 'Pfingstmontag',
    datetime.date(2023, 6, 8): 'Fronleichnam',
    datetime.date(2023, 8, 15): 'Mariä Himmelfahrt',
    datetime.date(2023, 10, 26): 'Nationalfeiertag',
    datetime.date(2023, 11, 1): 'Allerheiligen',
    datetime.date(2023, 12, 8): 'Mariä Empfängnis',
    datetime.date(2023, 12, 25): 'Christtag',
    datetime.date(2023, 12, 26): 'Stefanitag',
    datetime.date(2024, 1, 1): 'Neujahr',
    datetime.date(2024, 1, 6): 'Heilige Drei Könige',
    datetime.date(2024, 4, 1): 'Ostermontag',
    datetime.date(2024, 5, 1): 'Staatsfeiertag',
    datetime.date(2024, 5, 9): 'Christi Himmelfahrt',
    datetime.date(2024, 5, 20): 'Pfingstmontag',
    datetime.date(2024, 5, 30): 'Fronleichnam',
    datetime.date(2024, 8, 15): 'Mariä Himmelfahrt',
    datetime.date(2024, 10, 26): 'Nationalfeiertag',
    datetime.date(2024, 11, 1): 'Allerheiligen',
    datetime.date(2024, 12, 8): 'Mariä Empfängnis',
    datetime.date(2024, 12, 25): 'Christtag',
    datetime.date(2024, 12, 26): 'Stefanitag'
}


class TestLocales(unittest.TestCase):
    def test_get_locale(self):
        loc = get_locale(test_locale)
        if 'locale' not in loc:
            loc['locale'] = test_locale
        self.assertEqual(
            locale_dict,
            loc
        )

    def test_fetch_all_countries(self):
        all_countries = fetch_all_countries(
            language='de'
        )
        self.assertEqual(
            check_all_countries,
            all_countries
        )

    def test_get_country(self):
        country_info = get_country(
            country='at',
            language='de'
        )
        self.assertEqual(
            check_country,
            country_info
        )

    def test_get_language_name(self):
        for lang_code, names in language_names.items():
            for code, name in names.items():
                lang_name = get_language_name(
                    code=lang_code,
                    language=code
                )
                self.assertEqual(
                    name,
                    lang_name
                )

    def test_fetch_holidays(self):
        holidays = fetch_holidays(
            country='AT',
            state=9,
            years=[2022, 2023, 2024]
        )
        self.assertEqual(holidays, feiertage_2022_2023)

        holidays = fetch_holidays(
            country='AT',
            state=9,
            daterange=['1.1.2022', '31.12.2024']
        )
        self.assertEqual(holidays, feiertage_2022_2023)

    def test_is_holiday(self):
        for date, check in days_and_holidays.items():
            checked = is_holiday(
                datum=date,
                country='AT',
                state=9)

            self.assertEqual(
                checked,
                check
            )

    def test_format_price(self):
        for price in (
            123,
            2,
            234234,
            234100
        ):
            print(format_price(price))


if __name__ == '__main__':
    unittest.main()

    # print('finished country & language tests.')
