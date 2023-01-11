# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dputils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'docx2txt>=0.8,<0.9',
 'fpdf2>=2.5.4,<3.0.0',
 'pdfminer.six>=20220524,<20220525',
 'python-docx>=0.8.11,<0.9.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'dputils',
    'version': '0.2.0',
    'description': 'This library is utility library from digipodium',
    'long_description': 'A python library which can be used to extraxct data from files, pdfs, doc(x) files, as well as save data into these files. This library can be used to scrape and extract webpage data from websites as well.\n\n### Installation Requirements and Instructions\n\nPython versions 3.8 or above should be installed. After that open your terminal:\nFor windows users:\n```shell\npip install dputils\n```\nFor Mac/Linux users:\n```shell\npip3 install dputils\n```\n\n### Files Modules\n\nFunctions from dputils.files:\n1. get_data: \n    - To import, use statement: \n        ```python3\n        from dputils.files import get_data\n        ``` \n    - Obtains data from files of any extension given as args(supports text files, binary files, pdf, doc for now, more coming!)\n    - sample call:\n        ```python3\n        content = get_data(r"sample.docx")\n        print(content)\n        ```\n    - Returns a string or binary data depending on the output arg\n    - images will not be extracted\n\n2. save_data:\n    - To import, use statement:\n         ```python3\n        from dputils.files import save_data\n        ```\n    - save_data can be used to write and save data into a file of valid   extension.\n    - sample call: \n         ```python3\n        pdfContent = save_data("sample.pdf", "Sample text to insert")\n        print(pdfContent)\n        ```\n    - Returns True if file is successfully accessed and modified. Otherwise False.\n\n### Scrape Modules\nFunctions from dputils.scrape:\n1. get_webpage_data:\n    - To import, use statement: \n         ```python3\n        from dputils.scrape import get_webpage_data\n        ```\n    - get_webpage_data can be used to obtain data from any website in the   form of BeautifulSoup object\n    - sample call: \n        ```python3\n        soup = get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)")\n        print(type(soup))\n        ```\n    - Returns data as a BeautifulSoup object\n\n2. extract_one:\n    - extract_one can be used to extract a data item as a dict from data in a given BeautifulSoup object\n    - To import, use statement: \n        ```python3\n        from dputils.scrape import extract_one\n        ```\n    - usage: \n        ```python3\n        soup = get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)")\n\n        dataDict = extract_one(soup, title = {\'tag\' : \'h1\', \'attrs\' : {\'id\' : \'firstHeading\'}, \'output\' : \'text\'})\n        print(dataDict)\n        ```\n    - Output will be of type dict\n\n    ```python3\n    example here\n    ```\n3. extract_many:\n\n    import the functions\n    ```python3\n    from dputils.scrape import extract_many, get_webpage_data\n    ```\n    grap your soup\n    ```python3\n    url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"\n    soup = get_webpage_data(url)\n    ```\n    Provide all the parameters in the dict as shown in the example below.\n    ```python3\n    target = {\n    \'tag\': \'div\',\n    \'attrs\':{\'class\':\'_1YokD2 _3Mn1Gg\'}\n    }\n    items = {\n        \'tag\': \'div\',\n        \'attrs\':{\'class\':\'_1AtVbE col-12-12\'}\n    }\n    title = {\n        \'tag\': \'div\',\n        \'attrs\':{\'class\':\'_4rR01T\'}\n    }\n    price = {\n        \'tag\': \'div\',\n        \'attrs\':{\'class\':\'_30jeq3 _1_WHN1\'}\n    }\n    rating = {\n        \'tag\': \'div\',\n        \'attrs\':{\'class\':\'_3LWZlK\'}\n    }\n    link = {\n        \'tag\': \'a\',\n        \'attrs\':{\'class\':\'_1fQZEK\'},\n        \'output\':\'href\'\n    }\n    ```\n    call the functions with correct names\n    - **soup** : from get_webpage_data() function\n    - **target**: the subsection where the contents are present (optional)\n    - **items** : the repeating HTML code the contains the items (required)\n    - others will be the names and dicts of items to be extracted just link in extract one\n    ```python3\n    out= extract_many_1(soup, target=target, items=items, title=title, price=price, rating=rating, link=link)\n    ```\n    - Output will be a list of dicts\n    ```python3\n    print(out)\n    ```\n    (optional) Convert the data into pandas dataframe\n    ```python3\n    import pandas as pd\n    df = pd.DataFrame(out)\n    print(df)\n    ```\n    <img src = "https://digipodium.github.io/dputils/imgs/outputdf.png">\n\n4. extract_urls\n    - extract_urls can be used to extract all urls as a list from data in a given BeautifulSoup object\n    - To import, use statement: \n        ```python3\n        from dputils.scrape import extract_urls\n        ```\n    - usage: \n        ```python3\n        soup = get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)")\n\n        urlList = extract_urls(soup, target = {\'tag\' : \'div\', \'attrs\' : {\'class\':\'s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16\'}})\n        print(urlList)\n        ```\n    - Output will be list of urls\n\nThese functions can used on python versions 3.8 or greater.\n\nReferences for more help: https://github.com/digipodium/dputils\n\nThank you for using dputils!',
    'author': 'AkulS1008',
    'author_email': 'akulsingh0708@gmail.com',
    'maintainer': 'Zaid Kamil',
    'maintainer_email': 'xaidmetamorphos@gmail.com',
    'url': 'https://digipodium.github.io/dputils/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
