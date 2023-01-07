# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtcli', 'mtcli.pa']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'metatrader5>=5.0.43,<6.0.0',
 'numpy>=1.24,<2.0',
 'python-dotenv>=0.19,<0.20']

entry_points = \
{'console_scripts': ['mt = mtcli.mt:mt']}

setup_kwargs = {
    'name': 'mtcli',
    'version': '0.23.0',
    'description': 'Converte gráfico do MetaTrader 5 para texto',
    'long_description': '# mtcli  \n  \nFerramenta de linha de comando para usuários cegos do MetaTrader 5.\n  \n[PyPI](https://pypi.python.org/pypi/mtcli)  \n[Documentação](https://vfranca.github.io/mtcli)  \n  \n------------\n\n## Pré-requisitos  \n\n* [MetaTrader 5](https://www.metatrader5.com/pt) - Plataforma de trading.  \n* [Indicador mtcli](https://drive.google.com/open?id=1yKYI873r_liiexugqisgc-OeVc_5IlGH&authuser=vfranca3%40gmail.com&usp=drive_fs) -programa MQL5 executado no MetaTrader 5.  \n* [Python](https://www.python.org/downloads/windows) - Interpretador de comandos.  \n\n\n## Instalação  \n\n1. Instalar o MetaTrader 5.  \n2. Executar o indicador mtcli.ex5 e anexar a um gráfico.  \n3. Instalar o Python:\n\n```cmd\nwinget install python\n```\n\n4. Instalar o mtcli:\n\n```cmd\npip install mtcli\n```\n\n\n\nOpcionalmente baixe a pasta mtcli e descompacte os arquivos.\nhttps://drive.google.com/file/d/1olFEKJnnunBI1SDoW7QoMT9p6_yRQyhp/view?usp=sharing  \n\n\n## Comandos  \n  \n```cmd\nmt bars <ticker_de_ativo> \n```\nExibe as barras do gráfico do ticker de ativo.\n\n```cmd\nmt mm <ticker_de_ativo>\n```\nExibe a média móvel simples dos últimos 20 períodos do ticker de ativo.\n\n```cmd\nmt rm <ticker_de_ativo>\n```\nExibe o range médio dos últimos 14 períodos do ticker_de_ativo.\n\n------------\n \n  ## Agradecimentos  \n  \nAo @MaiconBaggio desenvolvedor do PyMQL5 que faz uma comunicação com o MetaTrader5 e fornecedor do primeiro EA exportador das cotações.  \nAo Claudio Garini que transferiu a geração das cotações para um indicador.  \n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vfranca/mtcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
