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
    'version': '1.3.0',
    'description': "A script to validate XML files for the game 'The Binding of Isaac: Repentance'",
    'long_description': '# isaac-xml-validator\n\nThis repo contains:\n\n- A [collection of XSD files](https://github.com/wofsauge/isaac-xml-validator/tree/main/xsd) used to validate XML files for mods of the game _[The Binding of Isaac: Repentance](https://store.steampowered.com/app/1426300/The_Binding_of_Isaac_Repentance/)_. (They were generated with the [`online-xml-to-xsd-converter`](https://www.liquid-technologies.com/online-xml-to-xsd-converter) tool.)\n)\n- A [website](https://wofsauge.github.io/isaac-xml-validator/webtool) that allows end-users to copy paste arbitrary XML data to validate it.\n- A [Python script](https://github.com/wofsauge/isaac-xml-validator/blob/main/isaac-xml-validator.py) which allows you to lint all the XML files in the repository for your mod.\n\n## Using the Website\n\nYou can view the website [here](https://wofsauge.github.io/isaac-xml-validator/webtool).\n\n## Usage in VSCode and Other IDEs\n\nMost people create Binding of Isaac mods (and other software) using [VSCode](https://code.visualstudio.com/), which is a very nice text editor / IDE.\n\nIf you make a typo (or some other error) in your XML file, you can get VSCode to automatically show you the error with a little red squiggly line, which is really helpful. This is accomplished by specifying a link to the corresponding schema at the top of the file.\n\nFirst, make sure that you have the [XML extension by Red Hat](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml) installed. Next, add the following to the top of your XML file:\n\n```xml\n<?xml-model href="https://wofsauge.github.io/isaac-xml-validator/xsd/[NAME OF THE FILE].xsd" ?>\n```\n\nFor example, this is how it would look for a "babies.xml" file:\n\n```xml\n<?xml-model href="https://wofsauge.github.io/isaac-xml-validator/xsd/babies.xsd" ?>\n<babies root="gfx/Characters/Player2/">\n  <baby id="0" name="Spider Baby" skin="000_Baby_Spider.png" />\n  <baby id="1" name="Love Baby" skin="001_Baby_Love.pngz" /> <!-- shows an error, because the "skin" attribute doesn\'t contain a .png file, but a .pngz-->\n  <baby id="2" name="Bloat Baby" skin="002_Baby_Bloat.png" />\n</babies>\n```\n\nNote that by default, the XML extension caches the XSD files in the following location:\n\n```text\nC:\\Users\\[username]\\.lemminx\\cache\\https\\wofsauge.github.io\\isaac-xml-validator\n```\n\nYou can remove this directory if you want to purge the cache to download any potentially updated XSD files.\n\n## Using the Python Script\n\nThe tool is published to PyPI, so you can install it via:\n\n```sh\npip install isaac-xml-validator\n```\n\nThen, you can run it via:\n\n```sh\nisaac-xml-validator\n```\n\nBy default, it will recursively scan for all XML files in the current working directory.\n\nYou will likely want to set up your repository so that the script runs in CI (e.g. GitHub Actions).\n\n## Usage in GitHub Actions\n\nFor most users, you will probably want to manually integrate the Python script into your existing lint routine. Alternatively, you can use [a GitHub action](https://github.com/wofsauge/Isaac-xmlvalidator-action) that automatically invokes the script.\n\n## Creating New XSD Files\n\nIf you need to create new XSD files, you can import our common XML schema like this:\n\n```xml\n<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsisaac="https://wofsauge.github.io/isaac-xml-validator">\n  <xs:import schemaLocation="https://wofsauge.github.io/isaac-xml-validator/isaacTypes.xsd" namespace="https://wofsauge.github.io/isaac-xml-validator" />\n  <xs:element name="Test">\n    <xs:complexType>\n      <xs:attribute name="root" type="xsisaac:pngFile" />\n    </xs:complexType>\n  </xs:element>\n</xs:schema>\n```\n',
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
