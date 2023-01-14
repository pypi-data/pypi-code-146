# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['isaac_xml_validator']
install_requires = \
['lxml>=4.9.2,<5.0.0']

entry_points = \
{'console_scripts': ['isaac-xml-validator = isaac_xml_validator:main']}

setup_kwargs = {
    'name': 'isaac-xml-validator',
    'version': '1.1.1',
    'description': "A script to validate XML files for the game 'The Binding of Isaac: Rebirth'",
    'long_description': '# isaac-xml-validator\n\nThis repo contains:\n\n- A [collection of XSD files](https://github.com/wofsauge/isaac-xml-validator/tree/main/xsd) used to validate XML files for mods of the game _[The Binding of Isaac: Repentance](https://store.steampowered.com/app/1426300/The_Binding_of_Isaac_Repentance/)_. (They were generated with the [`online-xml-to-xsd-converter`](https://www.liquid-technologies.com/online-xml-to-xsd-converter) tool.)\n)\n- A [website](https://wofsauge.github.io/isaac-xml-validator/webtool) that allows end-users to copy paste arbitrary XML data to validate it.\n- A [Python script](https://github.com/wofsauge/isaac-xml-validator/blob/main/isaac-xml-validator.py) which allows you to lint all the XML files in the repository for your mod.\n\n## Using the Website\n\nYou can view the website [here](https://wofsauge.github.io/isaac-xml-validator/webtool).\n\n## Using the Python Script\n\nThe tool is published to PyPI, so you can install it via:\n\n```sh\npip install isaac-xml-validator\n```\n\nThen, you can run it via:\n\n```sh\nisaac-xml-validator\n```\n\nBy default, it will recursively scan for all XML files in the current working directory.\n\n## Usage in GitHub Actions\n\nFor most users, you will probably want to manually integrate the Python script into your existing lint routine. Alternatively, you can use [a GitHub action](https://github.com/wofsauge/Isaac-xmlvalidator-action) that automatically invokes the script.\n\n## Add XSD as a validation Header\n\nIf you want to use the XSD files for external validation tools, for example as a live evaluation in VS Code with the ["XML" extension by Red Hat](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml), you can add the following line of code at the top of your .xml file:\n\n```xml\n<?xml-model href="https://wofsauge.github.io/isaac-xml-validator/xsd/[NAME OF THE FILE].xsd" ?>\n```\n**Example for the "babies.xml" file:**\n\n```xml\n<?xml-model href="https://wofsauge.github.io/isaac-xml-validator/xsd/babies.xsd" ?>\n<babies root="gfx/Characters/Player2/">\n\t<baby id="0" name="Spider Baby" skin="000_Baby_Spider.png" />\n\t<baby id="1" name="Love Baby" skin="001_Baby_Love.pngz" />\t<!-- evaluates as an error, because the "skin" attribute doesn\'t contain a .png file, but a .pngz-->\n\t<baby id="2" name="Bloat Baby" skin="002_Baby_Bloat.png" />\n</babies>\n```\n\n\n## Creating New XSD Files\n\nIf you need to create new XSD files, you can import our common XML schema like this:\n\n```xml\n<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsisaac="https://wofsauge.github.io/isaac-xml-validator">\n  <xs:import schemaLocation="https://wofsauge.github.io/isaac-xml-validator/isaacTypes.xsd" namespace="https://wofsauge.github.io/isaac-xml-validator" />\n  <xs:element name="Test">\n    <xs:complexType>\n      <xs:attribute name="root" type="xsisaac:pngFile" />\n    </xs:complexType>\n  </xs:element>\n</xs:schema>\n```\n',
    'author': 'Wofsauge',
    'author_email': 'jan-.-@t-online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
