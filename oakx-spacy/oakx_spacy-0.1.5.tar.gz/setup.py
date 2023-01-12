# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oakx_spacy']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'importlib>=1.0.4,<2.0.0',
 'oaklib>=0.1,<0.2',
 'scispacy>=0.5.1,<0.6.0',
 'setuptools>=65.0.1,<66.0.0',
 'spacy>=3.4.4,<4.0.0',
 'tox>=3.25.1,<4.0.0']

extras_require = \
{':extra == "docs"': ['sphinx[docs]>=5.3.0,<6.0.0',
                      'sphinx-rtd-theme[docs]>=1.0.0,<2.0.0',
                      'sphinx-autodoc-typehints[docs]>=1.19.4,<2.0.0',
                      'sphinx-click[docs]>=4.3.0,<5.0.0',
                      'myst-parser[docs]>=0.18.1,<0.19.0']}

entry_points = \
{'console_scripts': ['oxpacy = oakx_spacy.cli:main'],
 'oaklib.plugins': ['spacy = '
                    'oakx_spacy.spacy_implementation:SpacyImplementation']}

setup_kwargs = {
    'name': 'oakx-spacy',
    'version': '0.1.5',
    'description': 'oakx-spacy',
    'long_description': '# oakx-spacy\n\n[Spacy](https://spacy.io) + [SciSpacy](https://scispacy.apps.allenai.org) plugin for OAK.\n\n**ALPHA**\n\n## Usage\n\n### Non-developers:\nCreate a preferred virtual environment (`conda`, `poetry`, `venv` etc.). Install `oakx-spacy` using `pip install`.\n```\npip install oakx-spacy\n```\n\nNext, desired models (Spacy and/or SciSpacy) need to be downloaded/installed. Following is the list of models available.\n\n#### Spacy models\nEnglish pipelines optimized for CPU.\nIn order to install any of the below run `python -m spacy download en_core_web_xxx`\n\n1. `en_core_web_sm`: Components: tok2vec, tagger, parser, senter, ner, attribute_ruler, lemmatizer.\n2. `en_core_web_md`: Components: tok2vec, tagger, parser, senter, ner, attribute_ruler, lemmatizer.\n3. `en_core_web_lg`: Components: tok2vec, tagger, parser, senter, ner, attribute_ruler, lemmatizer.\n4. `en_core_web_trf`: Components: transformer, tagger, parser, ner, attribute_ruler, lemmatizer.\n\n#### SciSpacy models\nIn order to install any of the below use the corresponding line in [`pyproject.toml`](https://github.com/hrshdhgd/oakx-spacy/blob/main/pyproject.toml#L35-L65)\n\nFor example, if [CRAFT corpus](https://github.com/UCDenver-ccp/CRAFT) trained model is desired, do the following:\n```\npip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_craft_md-0.5.1.tar.gz\n```\nAvailable models:\n\n1. `en_ner_craft_md`: A spaCy NER model trained on the CRAFT corpus.\n2. `en_ner_jnlpba_md`: A spaCy NER model trained on the JNLPBA corpus.\n3. `en_ner_bc5cdr_md`: A spaCy NER model trained on the BC5CDR corpus.\n4. `en_ner_bionlp13cg_md`: A spaCy NER model trained on the BIONLP13CG corpus.\n5. `en_core_sci_scibert`: A full spaCy pipeline for biomedical data with a ~785k vocabulary and allenai/scibert-base as the transformer model.\n6. `en_core_sci_sm`: A full spaCy pipeline for biomedical data.\n7. `en_core_sci_md`: A full spaCy pipeline for biomedical data with a larger vocabulary and 50k word vectors.\n8. `en_core_sci_lg`: A full spaCy pipeline for biomedical data with a larger vocabulary and 600k word vectors.\n\n#### SciSpacy linkers\nThese come preinstalled with `scispacy` package itself. Available linkers are:\n1. `umls`: Links to the Unified Medical Language System, levels 0,1,2 and 9. This has ~3M concepts.\n2. `mesh`: Links to the Medical Subject Headings. This contains a smaller set of higher quality entities, which are used for indexing in Pubmed. MeSH contains ~30k entities. NOTE: The MeSH KB is derived directly from MeSH itself, and as such uses different unique identifiers than the other KBs.\n3. `rxnorm`: Links to the RxNorm ontology. RxNorm contains ~100k concepts focused on normalized names for clinical drugs. It is comprised of several other drug vocabularies commonly used in pharmacy management and drug interaction, including First Databank, Micromedex, and the Gold Standard Drug Database.\n4. `go`: Links to the Gene Ontology. The Gene Ontology contains ~67k concepts focused on the functions of genes.\n5. `hpo`: Links to the Human Phenotype Ontology. The Human Phenotype Ontology contains 16k concepts focused on phenotypic abnormalities encountered in human disease.\n\n### Developers:\n\n#### Clone the repository\n```\ngit clone https://github.com/hrshdhgd/oakx-spacy.git\n```\n\n#### Install `poetry`\n```\npip install poetry\n```\n\n#### SciSpacy models\nIn [`pyproject.toml`](https://github.com/hrshdhgd/oakx-spacy/blob/main/pyproject.toml#L35-L65), uncomment the 2 lines corresponding to the models desired. For example, if the desired model is the CRAFT corpus, uncomment the following:\n\n```\n[tool.poetry.dependencies.en_ner_craft_md]\nurl = "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_craft_md-0.5.1.tar.gz"\n```\n\n#### Install dependencies\n```\npoetry install\n```\n\n#### Spacy models\nInstructions similar to non-developers. Just make sure to prepend the command by `poetry run`\n\nThe default model is set to `en_ner_craft_md` and default linker to `umls`.\n\n## How it works\n\n### Using an ontology\nThe input argument can be expressed as `spacy:sqlite:obo:name-of-ontology` e.g. `spacy:sqlite:obo:bero`.\n1. A `.txt` file [`runoak -i spacy:sqlite:obo:bero annotate --text-file tests/input/text.txt`]\n2. Words that need to be annotated.[`runoak -i spacy:sqlite:obo:bero annotate Myeloid derived suppressor cells \\(MDSC\\) are immature myeloid cells with immunosuppressive activity.`] should yield:\n```\ninfo: \'JsonObj(alias_map=JsonObj(**{\'\'rdfs:label\'\': [\'\'Myeloid-Derived Suppressor\n  Cell\'\']}))\'\nsubject_end: 30\nsubject_label: Myeloid-Derived Suppressor Cell\nsubject_source: myeloid derive suppressor cell ( mdsc ) be immature myeloid cell with\n  immunosuppressive activity .\nsubject_start: 0\nsubject_text_id: NCIT:C129908\n\n---\ninfo: \'JsonObj(alias_map=JsonObj(**{\'\'rdfs:label\'\': [\'\'Immature Myeloid Cell\'\']}))\'\nsubject_end: 64\nsubject_label: Immature Myeloid Cell\nsubject_source: myeloid derive suppressor cell ( mdsc ) be immature myeloid cell with\n  immunosuppressive activity .\nsubject_start: 43\nsubject_text_id: NCIT:C113503\n```\n\n### Using SciSpacy.\nThe input argument can be expressed as `spacy:linker-name` e.g. `spacy:mesh`.\nThere are two possible inputs to this plugin:\n1. A `.txt` file [`runoak -i spacy: annotate --text-file text.txt`]\n2. Words that need to be annotated.[`runoak -i spacy: annotate Myeloid derived suppressor cells \\(MDSC\\) are immature myeloid cells with immunosuppressive activity.`] should yield (shortened):\n```\nconfidence: 0.9999999403953552\ninfo: JsonObj(aliases=[\'t cell suppressor\', \'suppressor cell\', \'T suppressor cell\',\n  \'suppressor cells\', \'Suppressor cell\', \'suppressor T lymphocyte\', \'cells suppressor\n  t\', \'Suppressor cells\', \'Suppressor cell (cell)\'], canonical_name=\'Suppressor T\n  Lymphocyte\', concept_id=\'C0038856\', definition=\'subpopulation of CD8+ T-lymphocytes\n  which suppress antibody production or inhibit cellular immune responses.\', types=[\'T025\'])\nsubject_end: 30\nsubject_label: suppressor cell\nsubject_source: myeloid derive suppressor cell ( mdsc ) be immature myeloid cell with\n  immunosuppressive activity .\nsubject_start: 15\nsubject_text_id: C0038856\n\n---\n\n...\n\n---\nconfidence: 0.8391554355621338\ninfo: JsonObj(aliases=[\'Myeloid Cell Leukemia Sequence 1\', \'Myeloid Cell Leukemia\n  Sequence 1 Protein\', \'Induced Myeloid Leukemia Cell Differentiation Protein Mcl-1\',\n  \'Myeloid Cell Factor-1\', \'Myeloid Cell Factor 1\', \'Induced Myeloid Leukemia Cell\n  Differentiation Protein Mcl 1\', \'Factor-1, Myeloid Cell\', \'Cell Factor-1, Myeloid\'],\n  canonical_name=\'Myeloid Cell Leukemia Sequence 1 Protein\', concept_id=\'C1510444\',\n  definition=\'A member of the myeloid leukemia factor (MLF) protein family with multiple\n  alternatively spliced transcript variants encoding different protein isoforms. In\n  hematopoietic cells, it is located mainly in the nucleus, and in non-hematopoietic\n  cells, primarily in the cytoplasm with a punctate nuclear localization. MLF1 plays\n  a role in cell cycle differentiation.\', types=[\'T116\', \'T123\'])\nsubject_end: 64\nsubject_label: myeloid cell\nsubject_source: myeloid derive suppressor cell ( mdsc ) be immature myeloid cell with\n  immunosuppressive activity .\nsubject_start: 52\nsubject_text_id: C1510444\n```\n\n# Acknowledgements\n\nThis [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) project was developed from the [oakx-plugin-cookiecutter](https://github.com/INCATools/oakx-plugin-cookiecutter) template and will be kept up-to-date using [cruft](https://cruft.github.io/cruft/).',
    'author': 'Harshad Hegde',
    'author_email': 'hhegde@lbl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
