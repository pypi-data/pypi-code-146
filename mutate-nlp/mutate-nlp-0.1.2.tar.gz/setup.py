# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mutate', 'mutate.parsers', 'mutate.pipelines', 'mutate.prompt_datasets']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3',
 'datasets>=1.6.2',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'torch>=1.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers>=4.5.1']

setup_kwargs = {
    'name': 'mutate-nlp',
    'version': '0.1.2',
    'description': 'Text data synthesize and pseudo labelling using LLMs',
    'long_description': '# 🦠 Mutate   <br>\n\nA library to synthesize text datasets using Large Language Models (LLM). Mutate reads through the examples in the dataset and\ngenerates similar examples using auto generated few shot prompts.\n\n## 1. Installation\n\n```\npip install mutate-nlp\n```\n\nor\n\n```\npip install git+https://github.com/infinitylogesh/mutate\n```\n\n\n## 2. Usage\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dPDVl3EvmsnJc7lxWYdAnTtlJgJjR2O2?usp=sharing)\n\n\n### 2.1 Synthesize text data from local csv files\n\n```python\nfrom mutate import pipeline\n\npipe = pipeline("text-classification-synthesis",\n                model="EleutherAI/gpt-neo-125M",\n                device=1)\n\ntask_desc = "Each item in the following contains movie reviews and corresponding sentiments. Possible sentimets are neg and pos"\n\n\n# returns a python generator\ntext_synth_gen = pipe("csv",\n                    data_files=["local/path/sentiment_classfication.csv"],\n                    task_desc=task_desc,\n                    text_column="text",\n                    label_column="label",\n                    text_column_alias="Comment",\n                    label_column_alias="sentiment",\n                    shot_count=5,\n                    class_names=["pos","neg"])\n\n#Loop through the generator to synthesize examples by class\nfor synthesized_examples  in text_synth_gen:\n    print(synthesized_examples)\n```\n\n<details>\n<summary>Show Output</summary>\n\n```python\n{\n    "text": ["The story was very dull and was a waste of my time. This was not a film I would ever watch. The acting was bad. I was bored. There were no surprises. They showed one dinosaur,",\n    "I did not like this film. It was a slow and boring film, it didn\'t seem to have any plot, there was nothing to it. The only good part was the ending, I just felt that the film should have ended more abruptly."]\n    "label":["neg","neg"]\n}\n\n{\n    "text":["The Bell witch is one of the most interesting, yet disturbing films of recent years. It’s an odd and unique look at a very real, but very dark issue. With its mixture of horror, fantasy and fantasy adventure, this film is as much a horror film as a fantasy film. And it‘s worth your time. While the movie has its flaws, it is worth watching and if you are a fan of a good fantasy or horror story, you will not be disappointed."],\n    "label":["pos"]\n}\n\n# and so on .....\n\n```\n</details>\n\n\n### 2.2 Synthesize text data from 🤗 datasets\n\nUnder the hood Mutate uses the wonderful 🤗 datasets library for dataset processing, So it supports 🤗 datasets out of the box.\n\n```python\n\nfrom mutate import pipeline\n\npipe = pipeline("text-classification-synthesis",\n                model="EleutherAI/gpt-neo-2.7B",\n                device=1)\n\ntask_desc = "Each item in the following contains customer service queries expressing the mentioned intent"\n\nsynthesizerGen = pipe("banking77",\n                    task_desc=task_desc,\n                    text_column="text",\n                    label_column="label",\n                    # if the `text_column` doesn\'t have a meaningful value\n                    text_column_alias="Queries",\n                    label_column_alias="Intent", # if the `label_column` doesn\'t have a meaningful value\n                    shot_count=5,\n                    dataset_args=["en"])\n\n\nfor exp in synthesizerGen:\n    print(exp)\n\n```\n\n<details>\n<summary>Show Output</summary>\n\n```python\n{"text":["How can i know if my account has been activated? (This is the one that I am confused about)",\n         "Thanks! My card activated"],\n"label":["activate_my_card",\n         "activate_my_card"]\n}\n\n{\n"text": ["How do i activate this new one? Is it possible?",\n         "what is the activation process for this card?"],\n"label":["activate_my_card",\n         "activate_my_card"]\n}\n\n# and so on .....\n\n```\n</details>\n\n\n### 2.3 I am feeling lucky : Infinetly loop through the dataset to generate examples indefinetly\n\n**Caution**: Infinetly looping through the dataset has a higher chance of duplicate examples to be generated.\n\n```python\n\nfrom mutate import pipeline\n\npipe = pipeline("text-classification-synthesis",\n                model="EleutherAI/gpt-neo-2.7B",\n                device=1)\n\ntask_desc = "Each item in the following contains movie reviews and corresponding sentiments. Possible sentimets are neg and pos"\n\n\n# returns a python generator\ntext_synth_gen = pipe("csv",\n                    data_files=["local/path/sentiment_classfication.csv"],\n                    task_desc=task_desc,\n                    text_column="text",\n                    label_column="label",\n                    text_column_alias="Comment",\n                    label_column_alias="sentiment",\n                    class_names=["pos","neg"],\n                    # Flag to generate indefinite examples\n                    infinite_loop=True)\n\n#Infinite loop\nfor exp in synthesizerGen:\n    print(exp)\n```\n\n\n## 3. Support\n### 3.1 Currently supports\n-  **Text classification dataset synthesis** : Few Shot text data synsthesize for text classification datasets using Causal LLMs ( GPT like )\n\n### 3.2 Roadmap:\n- **Other types of text Dataset synthesis** - NER , sentence pairs etc\n- Finetuning support for better quality generation\n- Pseudo labelling\n\n\n## 4. Credit\n- [EleutherAI](https://eluether.ai) for democratizing Large LMs.\n- This library uses 🤗 [Datasets](https://huggingface.co/docs/datasets) and 🤗 [Transformers](https://huggingface.co/docs/transformers) for processing datasets and models.\n\n\n## 5. References\n\nThe Idea of generating examples from Large Language Model is inspired by the works below,\n- [A Few More Examples May Be Worth Billions of Parameters](https://arxiv.org/abs/2110.04374) by Yuval Kirstain, Patrick Lewis, Sebastian Riedel, Omer Levy\n- [GPT3Mix: Leveraging Large-scale Language Models for Text Augmentation](https://arxiv.org/abs/2104.08826) by Kang Min Yoo, Dongju Park, Jaewook Kang, Sang-Woo Lee, Woomyeong Park\n- [Data Augmentation using Pre-trained Transformer Models](https://arxiv.org/abs/2003.02245) by Varun Kumar, Ashutosh Choudhary, Eunah Cho\n\n',
    'author': 'Logesh Kumar Umapathi',
    'author_email': 'logeshkumaru@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
