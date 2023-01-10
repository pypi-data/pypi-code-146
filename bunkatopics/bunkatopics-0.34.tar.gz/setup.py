# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bunkatopics']

package_data = \
{'': ['*']}

install_requires = \
['jupyterlab>=3.5.1,<4.0.0',
 'numpy==1.21.5',
 'pandas==1.4.1',
 'plotly==5.6.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn==1.1.3',
 'sentence-transformers==2.2.0',
 'spacy>=3,<4',
 'textacy==0.12.0',
 'tqdm==4.63.0',
 'umap-learn==0.5.3',
 'xgboost==1.6.2']

setup_kwargs = {
    'name': 'bunkatopics',
    'version': '0.34',
    'description': '',
    'long_description': '# BunkaTopics\n\nBunkaTopics is a Topic Modeling package that leverages Embeddings and focuses on Topic Representation to extract meaningful and interpretable topics from a list of documents.\n\n## Installation\n\nBefore installing bunkatopics, please install the following packages:\n\nLoad the spacy language models\n\n```bash\npython -m spacy download fr_core_news_lg\n```\n\n```bash\npython -m spacy download en_core_web_sm\n```\n\nEventually, install bunkatopic using pip\n\n```bash\npip install bunkatopics\n```\n\n## Quick Start with BunkaTopics\n\n```python\nfrom bunkatopics import BunkaTopics\nimport pandas as pd\n\ndata = pd.read_csv(\'data/imdb.csv\', index_col = [0])\ndata = data.sample(2000, random_state = 42)\n\n# Instantiate the model, extract ther terms and Embed the documents\n\nmodel = BunkaTopics(data, # dataFrame\n                    text_var = \'description\', # Text Columns\n                    index_var = \'imdb\',  # Index Column (Mandatory)\n                    extract_terms=True, # extract Terms ?\n                    terms_embeddings=True, # extract terms Embeddings?\n                    docs_embeddings=True, # extract Docs Embeddings?\n                    embeddings_model="distiluse-base-multilingual-cased-v1", # Chose an embeddings Model\n                    multiprocessing=True, # Multiprocessing of Embeddings\n                    language="en", # Chose between English "en" and French "fr"\n                    sample_size_terms = len(data),\n                    terms_limit=10000, # Top Terms to Output\n                    terms_ents=True, # Extract entities\n                    terms_ngrams=(1, 2), # Chose Ngrams to extract\n                    terms_ncs=True, # Extract Noun Chunks\n                    terms_include_pos=["NOUN", "PROPN", "ADJ"], # Include Part-of-Speech\n                    terms_include_types=["PERSON", "ORG"]) # Include Entity Types\n\n# Extract the topics\n\ntopics = model.get_clusters(topic_number= 15, # Number of Topics\n                    top_terms_included = 1000, # Compute the specific terms from the top n terms\n                    top_terms = 5, # Most specific Terms to describe the topics\n                    term_type = "lemma", # Use "lemma" of "text"\n                    ngrams = [1, 2], # N-grams for Topic Representation\n                    clusterer = \'hdbscan\') # Chose between Kmeans and HDBSCAN\n\n# Visualize the clusters. It is adviced to choose less that 5 terms - top_terms = 5 - to avoid overchanging the Figure\n\nfig = model.visualize_clusters(search = None, \nwidth=1000, \nheight=1000, \nfit_clusters=True,  # Fit Umap to well visually separate clusters\ndensity_plot=False) # Plot a density map to get a territory overview\n\nfig.show()\n\n\ncentroid_documents = model.get_centroid_documents(top_elements=2)\n```\n',
    'author': 'Charles De Dampierre',
    'author_email': 'charles.de-dampierre@hec.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
