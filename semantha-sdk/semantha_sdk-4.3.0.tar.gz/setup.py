# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semantha_sdk',
 'semantha_sdk.api',
 'semantha_sdk.model',
 'semantha_sdk.request',
 'semantha_sdk.response',
 'semantha_sdk.rest']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.28.1']

setup_kwargs = {
    'name': 'semantha-sdk',
    'version': '4.3.0',
    'description': 'This is a python client sdk for accessing semantha (the semantic platform)',
    'long_description': '![](https://www.semantha.de/wp-content/uploads/semantha-inverted.svg)\n\n# semantha® SDK\n\nThe semantha SDK is a high-level REST client to access the [semantha](http://semantha.ai) API.\nThe SDK is still under development.\nAn overview of the current progress (i.e. implemented and tested resources and endpoints) may be found at the end of\nthis document (State of Development).\nThe semantha SDK is compatible with python >= 3.8.\n\n### Disclaimer\n\n**IMPORTANT:** The SDK is under development and interfaces may change at any time without notice.\nUse with caution and on own risk.\n\n### Access\n\nTo access semantha\'s API you will need an API and a server url.\nBoth can be requested via [this contact form](https://www.semantha.de/request/).\n\n### Basic Usage\n\n#### Import\n\n```\nimport semantha_sdk\n```\n\n#### Authentication\n\n```\nsemantha = semantha_sdk.login(url="<semantha platform server URL>", key="<your key>")\n# or\nsemantha = semantha_sdk.login(url="<semantha platform server URL>", key_file="<path to your key file (json format)>")\n```\n\n#### End-point Access\n\n```\n# end-points (resp. resources) can be used like objects\ncurrent_user = semantha.current_user\nmy_domain = semantha.domains.get_one("my_domain")\n\n# they may have sub-resources, which can be retrieved as objects as well\nreference_documents = my_domains.reference_documents\n```\n\n#### CRUD on End-points\n\n```\n# CRUD operations are functions\ndomain_settings = my_domain.get_settings()\nmy_domain.reference_documents.delete_all()\n```\n\n#### Function Return Types & semantha Data Model\n\n```\n# some functions only return None, e.g.\nmy_domain.reference_documents.delete_all() # returns NoneType\n\n# others return built in types, e.g\nroles_list = current_user.get_user_roles() # returns list[str]\n\n# but most return objects of the semantha Data Model\n# (all returned objects are instances of frozen dataclasses)\nsettings = my_domain.get_settings() # returns instance of DomainSettings\n# attributes can be accessed as properties, e.g.\nsettings.enable_tagging # returns true or false\n# Data Model objects may be complex\ndocument = my_domain.references.post(file=a, reference_document=b) # returns instance of Document\n# the following returns the similarity value of the first references of the first sentence of the\n# the first paragraph on the first page of the document (if a reference was found for this sentence)\nsimilarity = pages[0].contents[0].paragraphs[0].references[0].similarity # returns float\n```\n\n### State of Development\n\nThe following resources and end-points are fully functional and (partially) tested:\n\nCurrentUser\n\n* get_user_data\n* get_user_roles\n\nDiff\n\n* post\n\nDomains\n\n* get_all\n* get_one --> returns sub-resource Domain\n    * get_configuration\n    * get_settings\n    * get_tags\n    * get_stopwords\n    * References\n        * post\n    * ReferenceDocuments\n        * get_all\n        * get_one\n        * delete_all\n        * delete_one\n        * post\n        * patch_document_information\n        * get_paragraph\n        * patch_paragraph\n        * delete_paragraph\n        * get_sentence\n        * get_clusters_of_documents\n        * get_named_entities\n        * get_statistic\n    * Documents\n        * post_document_model\n\nModel/Domains\n\n* get_one --> returns sub-resource DomainModel\n    * Boostwords\n        * get_all\n        * get_one\n        * delete_all\n        * delete_one\n        * post_word\n        * post_regex\n        * put_word\n        * put_regex\n    * Synonyms\n        * get_all\n        * get_one\n        * delete_all\n        * delete_one\n        * post_word\n        * post_regex\n        * put_word\n        * put_regex',
    'author': 'Tom Kaminski',
    'author_email': 'tom.kaminski@semantha.de',
    'maintainer': 'semantha support',
    'maintainer_email': 'support@semantha.de',
    'url': 'https://semantha.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
