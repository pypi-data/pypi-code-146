# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['langchain',
 'langchain.agents',
 'langchain.agents.conversational',
 'langchain.agents.mrkl',
 'langchain.agents.react',
 'langchain.agents.self_ask_with_search',
 'langchain.callbacks',
 'langchain.chains',
 'langchain.chains.api',
 'langchain.chains.combine_documents',
 'langchain.chains.conversation',
 'langchain.chains.llm_bash',
 'langchain.chains.llm_checker',
 'langchain.chains.llm_math',
 'langchain.chains.natbot',
 'langchain.chains.pal',
 'langchain.chains.qa_with_sources',
 'langchain.chains.question_answering',
 'langchain.chains.sql_database',
 'langchain.chains.summarize',
 'langchain.chains.vector_db_qa',
 'langchain.docstore',
 'langchain.embeddings',
 'langchain.embeddings.hyde',
 'langchain.evaluation',
 'langchain.evaluation.qa',
 'langchain.llms',
 'langchain.prompts',
 'langchain.prompts.example_selector',
 'langchain.utilities',
 'langchain.vectorstores']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6,<7',
 'SQLAlchemy>=1,<2',
 'numpy>=1,<2',
 'pydantic>=1,<2',
 'requests>=2,<3']

extras_require = \
{'all': ['faiss-cpu>=1,<2',
         'wikipedia>=1,<2',
         'elasticsearch>=8,<9',
         'redis>=4,<5',
         'manifest-ml>=0.0.1,<0.0.2',
         'spacy>=3,<4',
         'nltk>=3,<4',
         'transformers>=4,<5',
         'beautifulsoup4>=4,<5',
         'torch>=1,<2',
         'jinja2>=3,<4',
         'pinecone-client>=2,<3',
         'weaviate-client>=3,<4',
         'google-api-python-client==2.70.0',
         'wolframalpha==5.0.0'],
 'all:python_version >= "3.9" and python_version < "4.0"': ['tiktoken>=0,<1'],
 'llms': ['manifest-ml>=0.0.1,<0.0.2', 'transformers>=4,<5', 'torch>=1,<2']}

setup_kwargs = {
    'name': 'langchain',
    'version': '0.0.60',
    'description': 'Building applications with LLMs through composability',
    'long_description': '# 🦜️🔗 LangChain\n\n⚡ Building applications with LLMs through composability ⚡\n\n[![lint](https://github.com/hwchase17/langchain/actions/workflows/lint.yml/badge.svg)](https://github.com/hwchase17/langchain/actions/workflows/lint.yml) [![test](https://github.com/hwchase17/langchain/actions/workflows/test.yml/badge.svg)](https://github.com/hwchase17/langchain/actions/workflows/test.yml) [![linkcheck](https://github.com/hwchase17/langchain/actions/workflows/linkcheck.yml/badge.svg)](https://github.com/hwchase17/langchain/actions/workflows/linkcheck.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/langchainai.svg?style=social&label=Follow%20%40LangChainAI)](https://twitter.com/langchainai) [![](https://dcbadge.vercel.app/api/server/6adMQxSpJS?compact=true&style=flat)](https://discord.gg/6adMQxSpJS)\n\n## Quick Install\n\n`pip install langchain`\n\n## 🤔 What is this?\n\nLarge language models (LLMs) are emerging as a transformative technology, enabling\ndevelopers to build applications that they previously could not.\nBut using these LLMs in isolation is often not enough to\ncreate a truly powerful app - the real power comes when you can combine them with other sources of computation or knowledge.\n\nThis library is aimed at assisting in the development of those types of applications.\n\n## 📖 Documentation\n\nPlease see [here](https://langchain.readthedocs.io/en/latest/?) for full documentation on:\n\n- Getting started (installation, setting up the environment, simple examples)\n- How-To examples (demos, integrations, helper functions)\n- Reference (full API docs)\n  Resources (high-level explanation of core concepts)\n\n## 🚀 What can this help with?\n\nThere are six main areas that LangChain is designed to help with.\nThese are, in increasing order of complexity:\n\n**📃 LLMs and Prompts:**\n\nThis includes prompt management, prompt optimization, generic interface for all LLMs, and common utilities for working with LLMs.\n\n**🔗 Chains:**\n\nChains go beyond just a single LLM call, and are sequences of calls (whether to an LLM or a different utility). LangChain provides a standard interface for chains, lots of integrations with other tools, and end-to-end chains for common applications.\n\n**📚 Data Augmented Generation:**\n\nData Augmented Generation involves specific types of chains that first interact with an external datasource to fetch data to use in the generation step. Examples of this include summarization of long pieces of text and question/answering over specific data sources.\n\n**🤖 Agents:**\n\nAgents involve an LLM making decisions about which Actions to take, taking that Action, seeing an Observation, and repeating that until done. LangChain provides a standard interface for agents, a selection of agents to choose from, and examples of end to end agents.\n\n**🧠 Memory:**\n\nMemory is the concept of persisting state between calls of a chain/agent. LangChain provides a standard interface for memory, a collection of memory implementations, and examples of chains/agents that use memory.\n\n**🧐 Evaluation:**\n\n[BETA] Generative models are notoriously hard to evaluate with traditional metrics. One new way of evaluating them is using language models themselves to do the evaluation. LangChain provides some prompts/chains for assisting in this.\n\nFor more information on these concepts, please see our [full documentation](https://langchain.readthedocs.io/en/latest/?).\n\n## 💁 Contributing\n\nAs an open source project in a rapidly developing field, we are extremely open\nto contributions, whether it be in the form of a new feature, improved infra, or better documentation.\n\nFor detailed information on how to contribute, see [here](CONTRIBUTING.md).\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.github.com/hwchase17/langchain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
