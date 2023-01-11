# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bolivia_cc']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bolivia_cc = bolivia_cc.cli:main']}

setup_kwargs = {
    'name': 'bolivia-cc',
    'version': '0.1.3a0',
    'description': 'El código de control es un dato alfanumérico generado por un sistema de facturación y sirve para determinar la validez o no de una factura en Bolivia.',
    'long_description': '# Bolivia Codigo de Control\n\nEl Código de control Es un dato alfanumérico generado e impreso por un sistema de facturación computarizado SFV al momento de emitir una factura y sirve sirve para determinar la validez o no de una factura.\n\nEjemplo: CB-5E-CF-8B-05\n\nEstá constituido por pares de datos alfanuméricos separados por guiones (-) y expresados en formato hexadecimal (A, B, C, D, E y F), no contene la letra “O” solamente el número cero (0). Se genera en base a información de dosificación de la transacción comercial y la llave asignada a la dosificación utilizando los algoritmos Alleged RC4, Verhoeff y Base 64 como se explica en la [Especificación Técnica para la generación del Código de Control](https://www.impuestos.gob.bo/ckeditor/plugins/imageuploader/uploads/356aea02e.pdf).\n\nEste es una implementacion completa del generador y validacion del Código de Control\n\n## Uso\n\n``` terminal\n$ pip install bolivia-cc\n$ bolivia_cc --generar \\\n    --autorizacion=7000000006000 \\\n    --factura=560001 \\\n    --nit=3200000 \\\n    --fecha=2023-01-01 \\\n    --total=10000 \\\n    --llave=SECRET \\\n7B-F3-48-A8\n```\n\n``` python\nimport bolivia_cc\n\ncodigo_control = bolivia_cc.generate_control_code(\n    autorizacion="20040010113",\n    factura="665",\n    nitci="1004141023",\n    fecha="20070108",\n    monto="905.23",\n    llave="442F3w5AggG7644D737asd4BH5677sasdL4%44643(3C3674F4",\n)\n\nassert codigo_control == "771-D5-61-C8"\n```\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tugerente-com/bolivia-cc',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
