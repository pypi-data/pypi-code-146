# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataclass_to_diagram',
 'dataclass_to_diagram.converters',
 'dataclass_to_diagram.dia',
 'dataclass_to_diagram.dia.mermaid_er',
 'dataclass_to_diagram.dia.mermaid_state',
 'dataclass_to_diagram.exporters',
 'dataclass_to_diagram.exporters.c4_to_plantuml',
 'dataclass_to_diagram.exporters.erd_to_dbml',
 'dataclass_to_diagram.exporters.shared',
 'dataclass_to_diagram.exporters.state_to_puml',
 'dataclass_to_diagram.main',
 'dataclass_to_diagram.main.convert',
 'dataclass_to_diagram.main.export',
 'dataclass_to_diagram.models',
 'dataclass_to_diagram.models.c4',
 'dataclass_to_diagram.models.c4.component',
 'dataclass_to_diagram.models.c4.container',
 'dataclass_to_diagram.models.c4.context',
 'dataclass_to_diagram.models.c4.rel',
 'dataclass_to_diagram.models.c4.sprite',
 'dataclass_to_diagram.models.c4.sprite.tupadr3',
 'dataclass_to_diagram.models.c4.tag',
 'dataclass_to_diagram.models.erd',
 'dataclass_to_diagram.models.state_machine',
 'dataclass_to_diagram.shared']

package_data = \
{'': ['*']}

install_requires = \
['httpx', 'requests', 'typer[all]>=0.7.0,<0.8.0', 'typing_extensions']

entry_points = \
{'console_scripts': ['dtd = dataclass_to_diagram.__main__:start']}

setup_kwargs = {
    'name': 'dataclass-to-diagram',
    'version': '0.0.3',
    'description': 'Создание диаграмм из датаклассов python',
    'long_description': '[![PyPI version](https://badge.fury.io/py/dataclass-to-diagram.svg)](https://badge.fury.io/py/dataclass-to-diagram)\n\n# dataclass_to_diagram\n\nСоздание диаграмм из датаклассов python\n\n## Типы диаграмм\n\n### С4\n\nОписание - https://c4model.com/\n\nРеализация на PlantUML - https://github.com/plantuml-stdlib/C4-PlantUML\n\n\n\nСостоит из пакетов:\n\n- main - основной пакет для запуска\n- models - модели на основе dataclass для различных диаграмм\n- exporters - экспорт моделей в текстовый формат\n- converters - конвертирование текстового формата в изображение (svg, png, pdf, ...)\n\n\n\n### exporters\n\n#### dbml\n\nЭкспорт моделей БД (ERD) в формат [dbml](https://www.dbml.org/home/)\n\n\n\n### converters\n\n#### dbml-renderer\n\nКонвертирует файл с разметкой dbml в svg-изображение.\n\nУстановка:\n\n```bash\nnpm install -g @softwaretechnik/dbml-renderer\n```\n\n\n\n\n\n\n\nБиблиотека для генерации диаграмм из текстового описания.\n\nДиаграммы описываются объектами python. Далее геренируются изображения с помощью https://kroki.io.\n\n\n\n\n\n## Как использовать\n\n1. Создать две папки:\n\n   - dia_src - папка с исходным описанием\n   - dia_dist - папка со сгенерированными изображениями\n\n2. В папке dia_src создаются py-файлы. Названия файлов - произвольные. Можно создавать подкаталоги - структура каталогов будет скопирована в целевую папку dia_dist. Примеры создания можно посмотреть в тестовых диаграммах [пакета](https://github.com/Konstantin-Dudersky/konstantin_docs/tree/main/test).\n\n3. В одном файл должна быть только одна диаграмма. Название файла будет названием диаграммы.\n\n4. Для генерации можно создать задачу poetepoet. Прописать в файле pyproject.toml:\n\n   ```toml\n   [tool.poetry.dependencies]\n   konstantin_docs = "*"\n   poethepoet = "*"\n   \n   [tool.poe.tasks]\n   docs = {script = "konstantin_docs.main:generate_images(\'dia_src\', \'dia_dist\')"}\n   ```\n\n5. Запустить командой:\n\n   ```sh\n   poetry run poe docs\n   ```\n\n6. Дополнительно можно создать задачу в vscode. Для этого в файле .vscode/tasks.json:\n\n   ```json\n   {\n     "version": "2.0.0",\n     "tasks": [\n       {\n         "label": "docs",\n         "type": "shell",\n         "command": "poetry run poe docs"\n       }\n     ]\n   }\n   ```\n\n   Запускать командой F1 -> Task: Run task -> docs\n\nERD\n\n```bash\nnpm install -g @softwaretechnik/dbml-renderer\n```\n\n\n\n## Разработка\n\n```bash\npoetry build && poetry publish\n```\n\n\n\n',
    'author': 'konstantin-dudersky',
    'author_email': 'konstantin.dudersky@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Konstantin-Dudersky/dataclass_to_diagram.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
