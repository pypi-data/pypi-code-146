# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cellseg_models_pytorch',
 'cellseg_models_pytorch.datamodules',
 'cellseg_models_pytorch.datamodules.tests',
 'cellseg_models_pytorch.datasets',
 'cellseg_models_pytorch.datasets.dataset_writers',
 'cellseg_models_pytorch.datasets.tests',
 'cellseg_models_pytorch.decoders',
 'cellseg_models_pytorch.decoders.long_skips',
 'cellseg_models_pytorch.decoders.long_skips.merging',
 'cellseg_models_pytorch.decoders.tests',
 'cellseg_models_pytorch.inference',
 'cellseg_models_pytorch.inference.tests',
 'cellseg_models_pytorch.losses',
 'cellseg_models_pytorch.losses.criterions',
 'cellseg_models_pytorch.losses.tests',
 'cellseg_models_pytorch.metrics',
 'cellseg_models_pytorch.metrics.tests',
 'cellseg_models_pytorch.models',
 'cellseg_models_pytorch.models.base',
 'cellseg_models_pytorch.models.cellpose',
 'cellseg_models_pytorch.models.hovernet',
 'cellseg_models_pytorch.models.stardist',
 'cellseg_models_pytorch.models.tests',
 'cellseg_models_pytorch.modules',
 'cellseg_models_pytorch.modules.act',
 'cellseg_models_pytorch.modules.conv',
 'cellseg_models_pytorch.modules.norm',
 'cellseg_models_pytorch.modules.self_attention',
 'cellseg_models_pytorch.modules.tests',
 'cellseg_models_pytorch.modules.upsample',
 'cellseg_models_pytorch.optimizers',
 'cellseg_models_pytorch.optimizers.tests',
 'cellseg_models_pytorch.postproc',
 'cellseg_models_pytorch.postproc.functional',
 'cellseg_models_pytorch.postproc.functional.cellpose',
 'cellseg_models_pytorch.postproc.functional.stardist',
 'cellseg_models_pytorch.postproc.tests',
 'cellseg_models_pytorch.training',
 'cellseg_models_pytorch.training.callbacks',
 'cellseg_models_pytorch.training.functional',
 'cellseg_models_pytorch.training.lit',
 'cellseg_models_pytorch.training.tests',
 'cellseg_models_pytorch.transforms',
 'cellseg_models_pytorch.transforms.albu_transforms',
 'cellseg_models_pytorch.transforms.functional',
 'cellseg_models_pytorch.transforms.tests',
 'cellseg_models_pytorch.utils',
 'cellseg_models_pytorch.utils.tests']

package_data = \
{'': ['*'],
 'cellseg_models_pytorch.datasets.tests': ['data/*',
                                           'data/imgs/*',
                                           'data/masks/*'],
 'cellseg_models_pytorch.inference.tests': ['data/*'],
 'cellseg_models_pytorch.training.tests': ['data/*'],
 'cellseg_models_pytorch.utils.tests': ['data/*']}

install_requires = \
['numba>=0.55.2,<0.58.0',
 'numpy>=1.22,<1.24',
 'opencv-python>=4.2.0.32,<5.0.0.0',
 'pathos>=0.2.8,<0.4.0',
 'scikit-image>=0.19,<0.20',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7,<2.0',
 'timm>=0.5.4,<0.7.0',
 'torch>=1.8.1,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

extras_require = \
{'all': ['pytorch-lightning>=1.6.0,<2.0.0',
         'tables>=3.6.0,<4.0.0',
         'albumentations>=1.0.0,<2.0.0',
         'requests>=2.28.0,<3.0.0',
         'geojson>=2.5.0,<3.0.0',
         'torchmetrics>=0.10,<0.12']}

setup_kwargs = {
    'name': 'cellseg-models-pytorch',
    'version': '0.1.20',
    'description': 'Python library for 2D cell/nuclei instance segmentation models written with PyTorch.',
    'long_description': '<div align="center">\n\n![Logo](./images/logo.png)\n\n**Python library for 2D cell/nuclei instance segmentation models written with [PyTorch](https://pytorch.org/).**\n\n[![Generic badge](https://img.shields.io/badge/License-MIT-<COLOR>.svg?style=for-the-badge)](https://github.com/okunator/cellseg_models.pytorch/blob/master/LICENSE)\n[![PyTorch - Version](https://img.shields.io/badge/PYTORCH-1.8.1+-red?style=for-the-badge&logo=pytorch)](https://pytorch.org/)\n[![Python - Version](https://img.shields.io/badge/PYTHON-3.8+-red?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)\n<br>\n[![Github Test](https://img.shields.io/github/actions/workflow/status/okunator/cellseg_models.pytorch/tests.yml?label=Tests&logo=github&&style=for-the-badge)](https://github.com/okunator/cellseg_models.pytorch/actions/workflows/tests.yml)\n[![Pypi](https://img.shields.io/pypi/v/cellseg-models-pytorch?color=blue&logo=pypi&style=for-the-badge)](https://pypi.org/project/cellseg-models-pytorch/)\n[![Codecov](https://img.shields.io/codecov/c/github/okunator/cellseg_models.pytorch?logo=codecov&style=for-the-badge&token=oGSj7FZ1lm)](https://codecov.io/gh/okunator/cellseg_models.pytorch)\n<br>\n[![DOI](https://zenodo.org/badge/450787123.svg)](https://zenodo.org/badge/latestdoi/450787123)\n\n</div>\n\n<div align="center">\n\n</div>\n\n## Introduction\n\n**cellseg-models.pytorch** is a library built upon [PyTorch](https://pytorch.org/) that contains multi-task encoder-decoder architectures along with dedicated post-processing methods for segmenting cell/nuclei instances. As the name might suggest, this library is heavily inspired by [segmentation_models.pytorch](https://github.com/qubvel/segmentation_models.pytorch) library for semantic segmentation.\n\n## Features\n\n- High level API to define cell/nuclei instance segmentation models.\n- 4 cell/nuclei instance segmentation models and more to come.\n- Open source datasets for training and benchmarking.\n- Pre-trained backbones/encoders from the [timm](https://github.com/rwightman/pytorch-image-models) library.\n- All the architectures can be augmented to **panoptic segmentation**.\n- A lot of flexibility to modify the components of the model architectures.\n- Sliding window inference for large images.\n- Multi-GPU inference.\n- Popular training losses and benchmarking metrics.\n- Simple model training with [pytorch-lightning](https://www.pytorchlightning.ai/).\n- Benchmarking utilities both for model latency & segmentation performance.\n- Regularization techniques to tackle batch effects/domain shifts.\n- Ability to add transformers to the decoder layers.\n\n## Installation\n\n**Basic installation**\n\n```shell\npip install cellseg-models-pytorch\n```\n\n**To install extra dependencies (training utilities and datamodules for open-source datasets) use**\n\n```shell\npip install cellseg-models-pytorch[all]\n```\n\n## Models\n\n| Model                      | Paper                                                                          |\n| -------------------------- | ------------------------------------------------------------------------------ |\n| [[1](#Citation)] HoVer-Net | https://www.sciencedirect.com/science/article/pii/S1361841519301045?via%3Dihub |\n| [[2](#Citation)] Cellpose  | https://www.nature.com/articles/s41592-020-01018-x                             |\n| [[3](#Citation)] Omnipose  | https://www.biorxiv.org/content/10.1101/2021.11.03.467199v2                    |\n| [[4](#Citation)] Stardist  | https://arxiv.org/abs/1806.03535                                               |\n\n## Datasets\n\n| Dataset                       | Paper                                                                                            |\n| ----------------------------- | ------------------------------------------------------------------------------------------------ |\n| [[5, 6](#References)] Pannuke | https://arxiv.org/abs/2003.10778 , https://link.springer.com/chapter/10.1007/978-3-030-23937-4_2 |\n| [[7](#References)] Lizard     | http://arxiv.org/abs/2108.11195                                                                  |\n\n## Notebook examples\n\n- [Training Stardist with Pannuke](https://github.com/okunator/cellseg_models.pytorch/blob/main/examples/pannuke_nuclei_segmentation_stardist.ipynb). Train the Stardist model with constant sized Pannuke patches.\n- [Training Cellpose with Lizard](https://github.com/okunator/cellseg_models.pytorch/blob/main/examples/lizard_nuclei_segmentation_cellpose.ipynb). Train the Cellpose model with Lizard dataset that is composed of varying sized images.\n- [Benchmarking Cellpose Trained on Pannuke](https://github.com/okunator/cellseg_models.pytorch/blob/main/examples/pannuke_cellpose_benchmark.ipynb). Benchmark Cellpose trained on Pannuke. Both the model performance and latency.\n\n## Code Examples\n\n**Define Cellpose for cell segmentation.**\n\n```python\nimport cellseg_models_pytorch as csmp\nimport torch\n\nmodel = csmp.models.cellpose_base(type_classes=5)\nx = torch.rand([1, 3, 256, 256])\n\n# NOTE: the outputs still need post-processing.\ny = model(x) # {"cellpose": [1, 2, 256, 256], "type": [1, 5, 256, 256]}\n```\n\n**Define Cellpose for cell and tissue area segmentation (Panoptic segmentation).**\n\n```python\nimport cellseg_models_pytorch as csmp\nimport torch\n\nmodel = csmp.models.cellpose_plus(type_classes=5, sem_classes=3)\nx = torch.rand([1, 3, 256, 256])\n\n# NOTE: the outputs still need post-processing.\ny = model(x) # {"cellpose": [1, 2, 256, 256], "type": [1, 5, 256, 256], "sem": [1, 3, 256, 256]}\n```\n\n**Define panoptic Cellpose model with more flexibility.**\n\n```python\nimport cellseg_models_pytorch as csmp\n\n# the model will include two decoder branches.\ndecoders = ("cellpose", "sem")\n\n# and in total three segmentation heads emerging from the decoders.\nheads = {\n    "cellpose": {"cellpose": 2, "type": 5},\n    "sem": {"sem": 3}\n}\n\nmodel = csmp.CellPoseUnet(\n    decoders=decoders,                   # cellpose and semantic decoders\n    heads=heads,                         # three output heads\n    depth=5,                             # encoder depth\n    out_channels=(256, 128, 64, 32, 16), # num out channels at each decoder stage\n    layer_depths=(4, 4, 4, 4, 4),        # num of conv blocks at each decoder layer\n    style_channels=256,                  # num of style vector channels\n    enc_name="resnet50",                 # timm encoder\n    enc_pretrain=True,                   # imagenet pretrained encoder\n    long_skip="unetpp",                  # unet++ long skips ("unet", "unetpp", "unet3p")\n    merge_policy="sum",                  # concatenate long skips ("cat", "sum")\n    short_skip="residual",               # residual short skips ("basic", "residual", "dense")\n    normalization="bcn",                 # batch-channel-normalization.\n    activation="gelu",                   # gelu activation.\n    convolution="wsconv",                # weight standardized conv.\n    attention="se",                      # squeeze-and-excitation attention.\n    pre_activate=False,                  # normalize and activation after convolution.\n)\n\nx = torch.rand([1, 3, 256, 256])\n\n# NOTE: the outputs still need post-processing.\ny = model(x) # {"cellpose": [1, 2, 256, 256], "type": [1, 5, 256, 256], "sem": [1, 3, 256, 256]}\n```\n\n**Run HoVer-Net inference and post-processing with a sliding window approach.**\n\n```python\nimport cellseg_models_pytorch as csmp\n\n# define the model\nmodel = csmp.models.hovernet_base(type_classes=5)\n\n# define the final activations for each model output\nout_activations = {"hovernet": "tanh", "type": "softmax", "inst": "softmax"}\n\n# define whether to weight down the predictions at the image boundaries\n# typically, models perform the poorest at the image boundaries and with\n# overlapping patches this causes issues which can be overcome by down-\n# weighting the prediction boundaries\nout_boundary_weights = {"hovernet": True, "type": False, "inst": False}\n\n# define the inferer\ninferer = csmp.inference.SlidingWindowInferer(\n    model=model,\n    input_folder="/path/to/images/",\n    checkpoint_path="/path/to/model/weights/",\n    out_activations=out_activations,\n    out_boundary_weights=out_boundary_weights,\n    instance_postproc="hovernet",               # THE POST-PROCESSING METHOD\n    normalization="percentile",                 # same normalization as in training\n    patch_size=(256, 256),\n    stride=128,\n    padding=80,\n    batch_size=8,\n)\n\ninferer.infer()\n\ninferer.out_masks\n# {"image1" :{"inst": [H, W], "type": [H, W]}, ..., "imageN" :{"inst": [H, W], "type": [H, W]}}\n```\n\n## Models API\n\nGenerally, the model building API enables the effortless creation of hard-parameter sharing multi-task encoder-decoder CNN architectures. The general architectural schema is illustrated in the below image.\n\n<br><br>\n![Architecture](./images/architecture_overview.png)\n\n### Class API\n\nThe class API enables the most flexibility in defining different model architectures. It borrows a lot from [segmentation_models.pytorch](https://github.com/qubvel/segmentation_models.pytorch) models API.\n\n**Model classes**:\n\n- `csmp.CellPoseUnet`\n- `csmp.StarDistUnet`\n- `csmp.HoverNet`\n\n**All of the models contain**:\n\n- `model.encoder` - pretrained [timm](https://github.com/rwightman/pytorch-image-models) backbone for feature extraction.\n- `model.{decoder_name}_decoder` - Models can have multiple decoders with unique names.\n- `model.{head_name}_seg_head` - Model decoders can have multiple segmentation heads with unique names.\n- `model.forward(x)` - forward pass.\n- `model.forward_features(x)` - forward pass of the encoder and decoders. Returns enc and dec features\n\n**Defining your own multi-task architecture**\n\nFor example, to define a multi-task architecture that has `resnet50` encoder, four decoders, and 5 output heads with `CellPoseUnet` architectural components, we could do this:\n\n```python\nimport cellseg_models_pytorch as csmp\nimport torch\n\nmodel = csmp.CellPoseUnet(\n    decoders=("cellpose", "dist", "contour", "sem"),\n    heads={\n        "cellpose": {"type": 5, "cellpose": 2},\n        "dist": {"dist": 1},\n        "contour": {"contour": 1},\n        "sem": {"sem": 4}\n    },\n)\n\nx = torch.rand([1, 3, 256, 256])\nmodel(x)\n# {\n#   "cellpose": [1, 2, 256, 256],\n#   "type": [1, 5, 256, 256],\n#   "dist": [1, 1, 256, 256],\n#   "contour": [1, 1, 256, 256],\n#   "sem": [1, 4, 256, 256]\n# }\n```\n\n### Function API\n\nWith the function API, you can build models with low effort by calling the below listed functions. Under the hood, the function API simply calls the above classes with pre-defined decoder and head names. The training and post-processing tools of this library are built around these names, thus, it is recommended to use the function API, although, it is a bit more rigid than the class API. Basically, the function API only lacks the ability to define the output-tasks of the model, but allows for all the rest as the class API.\n\n| Model functions                        | Output names                              | Task                             |\n| -------------------------------------- | ----------------------------------------- | -------------------------------- |\n| `csmp.models.cellpose_base`            | `"type"`, `"cellpose"`,                   | **instance segmentation**        |\n| `csmp.models.cellpose_plus`            | `"type"`, `"cellpose"`, `"sem"`,          | **panoptic segmentation**        |\n| `csmp.models.omnipose_base`            | `"type"`, `"omnipose"`                    | **instance segmentation**        |\n| `csmp.models.omnipose_plus`            | `"type"`, `"omnipose"`, `"sem"`,          | **panoptic segmentation**        |\n| `csmp.models.hovernet_base`            | `"type"`, `"inst"`, `"hovernet"`          | **instance segmentation**        |\n| `csmp.models.hovernet_plus`            | `"type"`, `"inst"`, `"hovernet"`, `"sem"` | **panoptic segmentation**        |\n| `csmp.models.hovernet_small`           | `"type"`,`"hovernet"`                     | **instance segmentation**        |\n| `csmp.models.hovernet_small_plus`      | `"type"`, `"hovernet"`, `"sem"`           | **panoptic segmentation**        |\n| `csmp.models.stardist_base`            | `"stardist"`, `"dist"`                    | **binary instance segmentation** |\n| `csmp.models.stardist_base_multiclass` | `"stardist"`, `"dist"`, `"type"`          | **instance segmentation**        |\n| `csmp.models.stardist_plus`            | `"stardist"`, `"dist"`, `"type"`, `"sem"` | **panoptic segmentation**        |\n\n## References\n\n- [1] S. Graham, Q. D. Vu, S. E. A. Raza, A. Azam, Y-W. Tsang, J. T. Kwak and N. Rajpoot. "HoVer-Net: Simultaneous Segmentation and Classification of Nuclei in Multi-Tissue Histology Images." Medical Image Analysis, Sept. 2019.\n- [2] Stringer, C.; Wang, T.; Michaelos, M. & Pachitariu, M. Cellpose: a generalist algorithm for cellular segmentation Nature Methods, 2021, 18, 100-106\n- [3] Cutler, K. J., Stringer, C., Wiggins, P. A., & Mougous, J. D. (2022). Omnipose: a high-precision morphology-independent solution for bacterial cell segmentation. bioRxiv. doi:10.1101/2021.11.03.467199\n- [4] Uwe Schmidt, Martin Weigert, Coleman Broaddus, & Gene Myers (2018). Cell Detection with Star-Convex Polygons. In Medical Image Computing and Computer Assisted Intervention - MICCAI 2018 - 21st International Conference, Granada, Spain, September 16-20, 2018, Proceedings, Part II (pp. 265–273).\n- [5] Gamper, J., Koohbanani, N., Benet, K., Khuram, A., & Rajpoot, N. (2019) PanNuke: an open pan-cancer histology dataset for nuclei instance segmentation and classification. In European Congress on Digital Pathology (pp. 11-19).\n- [6] Gamper, J., Koohbanani, N., Graham, S., Jahanifar, M., Khurram, S., Azam, A.,Hewitt, K., & Rajpoot, N. (2020). PanNuke Dataset Extension, Insights and Baselines. arXiv preprint arXiv:2003.10778.\n- [7] Graham, S., Jahanifar, M., Azam, A., Nimir, M., Tsang, Y.W., Dodd, K., Hero, E., Sahota, H., Tank, A., Benes, K., & others (2021). Lizard: A Large-Scale Dataset for Colonic Nuclear Instance Segmentation and Classification. In Proceedings of the IEEE/CVF International Conference on Computer Vision (pp. 684-693).\n\n## Citation\n\n```bibtex\n@misc{csmp2022,\n    title={{cellseg_models.pytorch}: Cell/Nuclei Segmentation Models and Benchmark.},\n    author={Oskari Lehtonen},\n    howpublished = {\\url{https://github.com/okunator/cellseg_models.pytorch}},\n    doi = {10.5281/zenodo.7064617}\n    year={2022}\n}\n```\n\n## Licence\n\nThis project is distributed under [MIT License](https://github.com/okunator/cellseg_models.pytorch/blob/main/LICENSE)\n\nThe project contains code from the original cell segmentation and 3rd-party libraries that have permissive licenses:\n\n- [timm](https://github.com/rwightman/pytorch-image-models) (Apache-2)\n- [HoVer-Net](https://github.com/vqdang/hover_net) (MIT)\n- [Cellpose](https://github.com/MouseLand/cellpose) (BSD-3)\n- [Stardist](https://github.com/stardist/stardist) (BSD-3)\n\nIf you find this library useful in your project, it is your responsibility to ensure you comply with the conditions of any dependent licenses. Please create an issue if you think something is missing regarding the licenses.\n',
    'author': 'Okunator',
    'author_email': 'oskari.lehtonen@helsinki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/okunator/cellseg_models.pytorch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
