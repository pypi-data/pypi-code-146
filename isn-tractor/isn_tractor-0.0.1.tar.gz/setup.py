# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isn_tractor']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'scikit-allel>=1.3.5,<2.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.10.0,<2.0.0',
 'torch>=1.13.1,<2.0.0']

setup_kwargs = {
    'name': 'isn-tractor',
    'version': '0.0.1',
    'description': 'Interactome based Individual Specific Networks',
    'long_description': '# ISN-tractor\nInteractome based Individual Specific Networks (Ib-ISN)\n\n## About the project: Interactome Based Individual Specific Networks (Ib-ISN) Computation and its relevance\n\nAn *individual-specific network* in biology is a sort of network that depicts the relationships between the genes, proteins, or other biological molecules of a particular individual. \n\nIt is sometimes referred to as a "personalised network" or "individual network". \n\nThese networks can be computed\xa0using a range of data types, including genetic information, details on protein expression, and other omics data.\n\nOne of the top aims of individual-specific networks is to comprehend **how interactions between different biological molecules affect an individual\'s overall function and behaviour**. For example, an individual-specific network can be used to identify the proteins that are essential for maintaining a certain biological activity or the critical regulatory networks that control a person\'s gene expression. It is also possible to forecast how genetic or environmental changes may affect a person\'s biology by using individual-specific networks. For instance, they can be used to foretell how a specific mutation or environmental exposure may impact the way a certain gene or pathway functions.\n\nThe entire range of interactions between biological macromolecules in a cell, including as those mediated by protein-ligand binding or solely functional connections between proteins, are referred to as the *interactome*. As a result, it offers a summary of the functional activity within a particular cell. Extracellular protein-protein interaction (PPI) networks are particularly significant to illness causation, diagnosis, and treatment due to a number of features. Their functional diversity, chaos, and complexity are a few of these.\n\n[Luck et al.](https://www.nature.com/articles/s41586-020-2188-x) introduced *HuRI*, a human "all-by-all" reference interactome map of human binary protein interactions, which has been demonstrated to have over 53,000 protein-protein interactions. \n\nHuRI, as \n> a systematic proteome-wide reference that connects genetic variation to phenotypic outcomes,\n\nwas the impetus for our decision to create a novel approach for computing interactome-based ISN, starting from SNP data and ending with a gene-based network.\n\n## Getting started\n\n### Installation\n\n```bash\npip install isn-tractor\n```\n\n## Usage\n\n1. Data preprocessing and imputation\n\n```python\nimport pandas as pd\nimport isn_tractor.ibisn as it\n\nsnps = pd.read_csv("snp_dataset.csv")\nsnp_meta = pd.read_csv("snp_metadata.csv")\ninteract = pd.read_csv("interactome_interactions.csv")\ngtf = pd.read_csv("human_genes.csv")\n\n# returns \ngene_info = it.preprocess_gtf(gtf)\n\n# returns \nit.preprocess_snp(snp_meta)\n\n# returns \nsnps = it.impute(snps)\n```\n\n2. Mapping\n\n```python\n# returns \nit.positional_mapping(snp_meta, gene_info, neighborhood=5)\n```\n\n3. Features mapping and interaction\n\n```python\n# returns \n(interact_snp, interact_gene) = it.snp_interaction(interact, gene_info, snp_info)\n```\n\n4. Individual Specific Network (ISN) computation\n\n```python\nisn = it.compute_isn(df, interact_snp, interact_gene, "spearman", "max")\n```\n\nFor more examples, please refer to the _Documentation_.\n\n## Roadmap\n- [ ] Complete the _Usage_ section\n- [ ] Add documentation with examples\n- [ ] Consider a new function for functional mapping\n- [ ] Add:\n    - [ ] Imputation with file saving\n    - [ ] Function ```isn_calculation_per_edge```\n    - [ ] Progressbar\n\n## Contributing\n\nContributions are what make the open source community such a wonderful place to learn, be inspired, and create. \nYour contributions\xa0will be greatly appreciated.\n\nIf you have an idea for how to improve this, please fork the repository and submit a pull request. You can alternatively open a new issue with the tag "improvement". Don\'t forget to :star: the project! Thank you once more!\n\n1. Fork the Project\n2. Create your Feature Branch `(git checkout -b feature/AmazingFeature)`\n3. Commit your Changes `(git commit -m \'Add some AmazingFeature\')`\n4. Push to the Branch `(git push origin feature/AmazingFeature)`\n5. Open a Pull Request\n\n## License\n\n## Contact\nGiada Lalli - giada.lalli@kuleuven.be\n\nZuqi Li - zuqi.li@kuleuven.be\n\nProject Link: \n\n## Acknowledgments\n\n',
    'author': 'Giada Lalli',
    'author_email': 'giada.lalli@kuleuven.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/GiadaLalli/ISN-tractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
