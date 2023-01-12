# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basedosdados',
 'basedosdados.cli',
 'basedosdados.download',
 'basedosdados.upload']

package_data = \
{'': ['*'],
 'basedosdados': ['configs/*',
                  'configs/templates/dataset/*',
                  'configs/templates/table/*']}

install_requires = \
['Jinja2==3.0.3',
 'ckanapi==4.6',
 'click==8.0.3',
 'google-cloud-bigquery-storage==1.1.0',
 'google-cloud-bigquery==2.30.1',
 'google-cloud-storage==1.42.3',
 'importlib-metadata>=4.11.3,<5.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pandas-gbq>=0.17.4,<0.18.0',
 'pandas>=1.3.5,<2.0.0',
 'pandavro>=1.6.0,<2.0.0',
 'pyaml==20.4.0',
 'pyarrow==6.0.0',
 'ruamel.yaml==0.17.10',
 'shapely>=1.6.0,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'tomlkit==0.7.0',
 'tqdm==4.50.2']

entry_points = \
{'console_scripts': ['basedosdados = basedosdados.cli.cli:cli']}

setup_kwargs = {
    'name': 'basedosdados',
    'version': '1.6.10',
    'description': 'Organizar e facilitar o acesso a dados brasileiros através de tabelas públicas no BigQuery.',
    'long_description': '# Python Package\n\n## Desenvolvimento Linux e Mac: \n\nClone o repositório principal:\n\n```sh\ngit clone https://github.com/basedosdados/mais.git\n```\nEntre na pasta local do repositório usando `cd mais/` e suba o ambiente localmente:\n\n```sh\nmake create-env\n. .mais/bin/activate\ncd python-package/\npython setup.py develop\n```\n\n### Desenvolva uma nova feature\n\n1. Abra uma branch com o nome issue-<X>\n2. Faça as modificações necessárias\n3. Suba o Pull Request apontando para a branch `python-next-minor` ou `python-next-patch`. \n    Sendo, minor e patch referentes ao bump da versão: v1.5.7 --> v\\<major>.\\<minor>.\\<patch>.\n4. O nome do PR deve seguir o padrão\n    `[infra] <titulo explicativo>`\n\n\n### O que uma modificação precisa ter\n\n  \n- Resolver o problema\n- Lista de modificações efetuadas\n    1. Mudei a função X para fazer Y\n    2. Troquei o nome da variavel Z\n- Referência aos issues atendidos\n- Documentação e Docstrings\n- Testes\n  \n\n## Versionamento\n\n**Para publicar uma nova versão do pacote é preciso seguir os seguintes passos:**\n\n1. Fazer o pull da branch:\n\n    ```bash\n    git pull origin [python-version]\n    ```\n  \n    Onde `[python-version]` é a branch da nova versão do pacote.\n\n2. Se necessario adicionar novas dependências:\n    ```bash\n      poetry add <package-name>\n    ```\n\n3. Gerar novo `requirements-dev.txt` \n\n    ```bash\n    poetry export -f requirements.txt --output requirements-dev.txt --without-hashes\n    ```\n\n4. Editar `pyproject.toml`:\n\n    O arquivo `pyproject.toml` contém, entre outras informações, a versão do pacote em python da **BD**. Segue excerto do arquivo:\n\n    ```toml\n    description = "Organizar e facilitar o acesso a dados brasileiros através de tabelas públicas no BigQuery."\n    homepage = "https://github.com/base-dos-dados/bases"\n    license = "MIT"\n    name = "basedosdados"\n    packages = [\n      {include = "basedosdados"},\n    ]\n    readme = "README.md"\n    repository = "https://github.com/base-dos-dados/bases"\n    version = "1.6.1-beta.2"\n    ```\n    \n    O campo `version` deve ser alterado para o número da versão sendo lançada.\n\n5. Push para branch:\n\n    ```bash\n    git push origin [python-version]\n    ```\n\n6. Publicação do pacote no PyPI (exige usuário e senha):\n\n    Para publicar o pacote no PyPI, use:\n    \n    ```bash\n    poetry version [python-version]\n    poetry publish --build\n    ```\n\n7. Faz merge da branch para a master\n8. Faz release usando a UI do GitHub\n9. Atualizar versão do pacote usada internamente\n',
    'author': 'Joao Carabetta',
    'author_email': 'joao.carabetta@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/base-dos-dados/bases',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
