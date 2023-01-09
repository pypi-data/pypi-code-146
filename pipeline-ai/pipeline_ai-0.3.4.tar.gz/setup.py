# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeline',
 'pipeline.api',
 'pipeline.api.asyncio',
 'pipeline.console',
 'pipeline.docker',
 'pipeline.exceptions',
 'pipeline.objects',
 'pipeline.objects.environment',
 'pipeline.objects.huggingface',
 'pipeline.schemas',
 'pipeline.schemas.redis',
 'pipeline.util',
 'pipeline.util.torch_utils']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.0,<3.0.0',
 'dill>=0.3.6,<0.4.0',
 'httpx>=0.23.1,<0.24.0',
 'packaging>=21.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyhumps>=3.0.2,<4.0.0',
 'setuptools>=65.4.1,<66.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'docker': ['PyYAML>=6.0,<7.0']}

entry_points = \
{'console_scripts': ['pipeline = pipeline.console:_run']}

setup_kwargs = {
    'name': 'pipeline-ai',
    'version': '0.3.4',
    'description': 'Pipelines for machine learning workloads.',
    'long_description': '# [Pipeline](https://pipeline.ai) [![Production workflow](https://github.com/neuro-ai-dev/pipeline/actions/workflows/prod-wf.yml/badge.svg?branch=main)](https://github.com/neuro-ai-dev/pipeline/actions/workflows/prod-wf.yml) [![Version](https://img.shields.io/pypi/v/pipeline-ai)](https://pypi.org/project/pipeline-ai) ![Size](https://img.shields.io/github/repo-size/neuro-ai-dev/pipeline) ![Downloads](https://img.shields.io/pypi/dm/pipeline-ai) [![License](https://img.shields.io/crates/l/ap)](https://www.apache.org/licenses/LICENSE-2.0) [![Discord](https://img.shields.io/badge/discord-join-blue)](https://discord.gg/eJQRkBdEcs)\n\n[_powered by mystic_](https://www.mystic.ai/)\n\n# Table of Contents\n\n- [About](#about)\n- [Version roadmap](#version-roadmap)\n  - [v0.4.0](#v040-jan-2023)\n  - [v0.5.0](#v050-janfeb-2023)\n  - [No current specified version features](#no-current-specified-version-features)\n- [Quickstart](#quickstart)\n  - [Basic maths](#basic-maths)\n  - [Transformers (GPT-Neo 125M)](#transformers-gpt-neo-125m)\n- [Installation instructions](#installation-instructions)\n  - [Linux, Mac (intel)](#linux--mac--intel-)\n  - [Mac (arm/M1)](#mac--arm-m1-)\n- [Development](#development)\n- [License](#license)\n\n# About\n\nPipeline is a python library that provides a simple way to construct computational graphs for AI/ML. The library is suitable for both development and production environments supporting inference and training/finetuning. This library is also a direct interface to [Pipeline.ai](https://pipeline.ai) which provides a compute engine to run pipelines at scale and on enterprise GPUs.\n\nThe syntax used for defining AI/ML pipelines shares some similarities in syntax to sessions in [Tensorflow v1](https://www.tensorflow.org/api_docs/python/tf/compat/v1/InteractiveSession), and Flows found in [Prefect](https://github.com/PrefectHQ/prefect). In future releases we will be moving away from this syntax to a C based graph compiler which interprets python directly (and other languages) allowing users of the API to compose graphs in a more native way to the chosen language.\n# Version roadmap\n\n## v0.4.0 (Jan 2023)\n\n- Custom environments on PipelineCloud (remote compute services)\n- Kwarg inputs to runs\n- Extended IO inputs to `pipeline_function` objects\n\n## v0.5.0 (Jan/Feb 2023)\n\n- Pipeline chaining\n- `if` statements & `while/for` loops\n\n## No current specified version features\n\n- Run log streaming\n- Run progress tracking\n- Resource dedication\n- Pipeline scecific remote load balancer (10% of traffic to one pipeline 80% to another)\n- Usage capping\n- Run result streaming\n- Progromatic autoscaling\n- Alerts\n- Events\n- Different python versions on remote compute services\n# Quickstart\n\n> :warning: **Uploading pipelines to Pipeline Cloud works best in Python 3.9.** We strongly recommend you use Python 3.9 when uploading pipelines because the `pipeline-ai` library is still in beta and is known to cause opaque errors when pipelines are serialised from a non-3.9 environment.\n\n\n## Basic maths\n\n```python\nfrom pipeline import Pipeline, Variable, pipeline_function\n\n\n@pipeline_function\ndef square(a: float) -> float:\n    return a**2\n\n@pipeline_function\ndef multiply(a: float, b: float) -> float:\n    return a * b\n\nwith Pipeline("maths") as pipeline:\n    flt_1 = Variable(type_class=float, is_input=True)\n    flt_2 = Variable(type_class=float, is_input=True)\n    pipeline.add_variables(flt_1, flt_2)\n\n    sq_1 = square(flt_1)\n    res_1 = multiply(flt_2, sq_1)\n    pipeline.output(res_!)\n\noutput_pipeline = Pipeline.get_pipeline("maths")\nprint(output_pipeline.run(5.0, 6.0))\n\n```\n\n## Transformers (GPT-Neo 125M)\n\n_Note: requires `torch` and `transformers` as dependencies._\n```python\nfrom pipeline import Pipeline, Variable\nfrom pipeline.objects.huggingface.TransformersModelForCausalLM import (\n    TransformersModelForCausalLM,\n)\n\nwith Pipeline("HF pipeline") as builder:\n    input_str = Variable(str, is_input=True)\n    model_kwargs = Variable(dict, is_input=True)\n\n    builder.add_variables(input_str, model_kwargs)\n\n    hf_model = TransformersModelForCausalLM(\n        model_path="EleutherAI/gpt-neo-125M",\n        tokenizer_path="EleutherAI/gpt-neo-125M",\n    )\n    hf_model.load()\n    output_str = hf_model.predict(input_str, model_kwargs)\n\n    builder.output(output_str)\n\noutput_pipeline = Pipeline.get_pipeline("HF pipeline")\n\nprint(\n    output_pipeline.run(\n        "Hello my name is", {"min_length": 100, "max_length": 150, "temperature": 0.5}\n    )\n)\n```\n\n# Installation instructions\n\n## Linux, Mac (intel)\n\n```shell\npip install -U pipeline-ai\n```\n\n## Mac (arm/M1)\n\nDue to the ARM architecture of the M1 core it is necessary to take additional steps to install Pipeline, mostly due to the transformers library. We recoomend running inside of a conda environment as shown below.\n\n1. Make sure Rosetta2 is disabled.\n2. From terminal run:\n\n```\nxcode-select --install\n```\n\n3. Install Miniforge, instructions here: [https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge) or follow the below:\n   1. Download the Miniforge install script here: [https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh)\n   2. Make the shell executable and run\n   ```\n   sudo chmod 775 Miniforge3-MacOSX-arm64.sh\n   ./Miniforge3-MacOSX-arm64.sh\n   ```\n4. Create a conda based virtual env and activate:\n\n```\nconda create --name pipeline-env python=3.9\nconda activate pipeline-env\n```\n\n5. Install tensorflow\n\n```\nconda install -c apple tensorflow-deps\npython -m pip install -U pip\npython -m pip install -U tensorflow-macos\npython -m pip install -U tensorflow-metal\n```\n\n6. Install transformers\n\n```\nconda install -c huggingface transformers -y\n```\n\n7. Install pipeline\n\n```\npython -m pip install -U pipeline-ai\n```\n\n\n\n# Development\n\nThis project is made with poetry, [so firstly setup poetry on your machine](https://python-poetry.org/docs/#installation).\n\nOnce that is done, please run\n\n    sh setup.sh\n\nWith this you should be good to go. This sets up dependencies, pre-commit hooks and\npre-push hooks.\n\nYou can manually run pre commit hooks with\n\n    pre-commit run --all-files\n\nTo run tests manually please run\n\n    pytest\n\n# License\n\nPipeline is licensed under [Apache Software License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n',
    'author': 'Paul Hetherington',
    'author_email': 'ph@mystic.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
