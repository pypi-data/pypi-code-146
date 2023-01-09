# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jquantsapi']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.6,<2.0',
 'pandas>=1.3.5,<2.0',
 'requests>=2.23.0,<3.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'types-python-dateutil>=2.8.19,<3.0.0',
 'types-requests>=2.28.5,<3.0.0',
 'urllib3>=1.24.3,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'jquants-api-client',
    'version': '0.2.2',
    'description': 'J-Quants API Client Library',
    'long_description': '# jquants-api-client\n\n[![PyPI version](https://badge.fury.io/py/jquants-api-client.svg)](https://badge.fury.io/py/jquants-api-client)\n\n個人投資家向けデータAPI配信サービス「 [J-Quants API](https://jpx-jquants.com/#jquants-api) 」のPythonクライアントライブラリです。\nJ-QuantsやAPI仕様についての詳細を知りたい方は [公式ウェブサイト](https://jpx-jquants.com/) をご参照ください。\n現在、J-Quants APIはベータ版サービスとして提供されています。\n\n## 使用方法\n\npip経由でインストールします。\n\n```shell\npip install jquants-api-client\n```\n\n### J-Quants API の利用\n\nTo use J-Quants API, you need to "Applications for J-Quants API" from [J-Quants API Web site](https://jpx-jquants.com/?lang=en#jquants-api).\n\nJ-Quants APIを利用するためには[J-Quants API の Web サイト](https://jpx-jquants.com/#jquants-api) から「J-Quants API申し込み」が必要になります。\n\njquants-api-client-python を使用するためには「J-Quants API ログインページで使用するメールアドレスおよびパスワード」または「J-Quants API メニューページから取得したリフレッシュトークン」が必要になります。必要に応じて下記のWebサイトより取得してください。\n\n[J-Quants API ログインページ](https://application.jpx-jquants.com/)\n\n### サンプルコード\n\n```python\nfrom datetime import datetime\nfrom dateutil import tz\nimport jquantsapi\n\nmy_mail_address:str = "*****"\nmy_password: str = "*****"\ncli = jquantsapi.Client(mail_address=my_mail_address, password=my_password)\ndf = cli.get_price_range(\n    start_dt=datetime(2022, 7, 25, tzinfo=tz.gettz("Asia/Tokyo")),\n    end_dt=datetime(2022, 7, 26, tzinfo=tz.gettz("Asia/Tokyo")),\n)\nprint(df)\n```\n\nAPIレスポンスがDataframeの形式で取得できます。\n\n```shell\n       Code       Date  ...  AdjustmentClose  AdjustmentVolume\n0     13010 2022-07-25  ...           3630.0            8100.0\n1     13050 2022-07-25  ...           2023.0           54410.0\n2     13060 2022-07-25  ...           2001.0          943830.0\n3     13080 2022-07-25  ...           1977.5          121300.0\n4     13090 2022-07-25  ...          43300.0             391.0\n...     ...        ...  ...              ...               ...\n4189  99930 2022-07-26  ...           1426.0            5600.0\n4190  99940 2022-07-26  ...           2605.0            7300.0\n4191  99950 2022-07-26  ...            404.0           13000.0\n4192  99960 2022-07-26  ...           1255.0            4000.0\n4193  99970 2022-07-26  ...            825.0          133600.0\n\n[8388 rows x 14 columns]\n```\n\nより具体的な使用例は [サンプルノートブック(/examples)](examples) をご参照ください。\n\n## 対応API\n\n### ラッパー群\u3000 \n\nJ-Quants API の各APIエンドポイントに対応しています。\n\n  - get_refresh_token\n  - get_id_token\n  - get_listed_info\n  - get_listed_sections\n  - get_prices_daily_quotes\n  - get_indices_topix\n  - get_markets_trades_spec\n  - get_fins_statements\n  - get_fins_announcement\n\n### ユーティリティ群\n\n業種や市場区分一覧などを返します。\n  - get_market_segments\n  - get_17_sectors\n  - get_33_sectors\n\n日付範囲を指定して一括でデータ取得して、取得したデータを結合して返すようなユーティリティが用意されています。\n\n  - get_list\n  - get_price_range\n  - get_statements_range\n\n## 設定\n\n認証用のメールアドレス/パスワードおよびリフレッシュトークンは設定ファイルおよび環境変数を使用して指定することも可能です。\n設定は下記の順に読み込まれ、設定項目が重複している場合は後に読み込まれた値で上書きされます。\n\n1. `/content/drive/MyDrive/drive_ws/secret/jquants-api.toml` (Google Colabのみ)\n2. `${HOME}/.jquants-api/jquants-api.toml`\n3. `jquants-api.toml`\n4. `os.environ["JQUANTS_API_CLIENT_CONFIG_FILE"]`\n5. `${JQUANTS_API_MAIL_ADDRESS}`, `${JQUANTS_API_PASSWORD}`, `${JQUANTS_API_REFRESH_TOKEN}`\n\n### 設定ファイル例\n\n`jquants-api.toml` は下記のように設定します。\n\n```toml\n[jquants-api-client]\nmail_address = "*****"\npassword = "*****"\nrefresh_token = "*****"\n```\n\n## 動作確認\n\nGoogle Colab および Python 3.10 で動作確認を行っています。\nJ-Quants APIは現在β版のため、本ライブラリも今後仕様が変更となる可能性があります。\nPython 3.7 サポートは廃止予定です。将来のバージョンではサポート対象外となります。\nPlease note Python 3.7 support is deprecated.\n\n## 開発\n\nJ-Quants API Clientの開発に是非ご協力ください。\nGithub上でIssueやPull Requestをお待ちしております。\n',
    'author': 'J-Quants Project Contributors',
    'author_email': 'j-quants@jpx.co.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/J-Quants/jquants-api-client-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
