# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qutrunk',
 'qutrunk.algorithm',
 'qutrunk.backends',
 'qutrunk.backends.braket',
 'qutrunk.backends.ibm',
 'qutrunk.backends.local',
 'qutrunk.backends.qusaas',
 'qutrunk.backends.qusprout',
 'qutrunk.circuit',
 'qutrunk.circuit.gates',
 'qutrunk.circuit.ops',
 'qutrunk.config',
 'qutrunk.converters',
 'qutrunk.dagcircuit',
 'qutrunk.example',
 'qutrunk.qasm',
 'qutrunk.qasm.node',
 'qutrunk.thrift',
 'qutrunk.thrift.code',
 'qutrunk.thrift.qusprout',
 'qutrunk.thrift.qusproutdata',
 'qutrunk.tools',
 'qutrunk.visualizations']

package_data = \
{'': ['*'],
 'qutrunk.example': ['jupyter/*'],
 'qutrunk.qasm': ['libs/*'],
 'qutrunk.thrift': ['idl/*']}

install_requires = \
['networkx>=2.8,<3.0',
 'numpy>=1.21.6,<2.0.0',
 'ply>=3.11,<4.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.27.1,<3.0.0',
 'retworkx>=0.11.0,<0.12.0',
 'thrift>=0.15.0,<0.16.0']

extras_require = \
{'braket': ['amazon-braket-sdk>=1.32.0,<2.0.0'],
 'parallel': ['mpi4py>=3.1.4,<4.0.0']}

setup_kwargs = {
    'name': 'qutrunk',
    'version': '0.2.0',
    'description': 'qutrunk is an open source library for quantum computing.',
    'long_description': '## QuTrunk\n\n[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://developer.queco.cn/qutrunk_api/)\n[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)\n[![Download Code](https://img.shields.io/badge/download-zip-green.svg)](https://github.com/queco-quantum/qutrunk/archive/refs/heads/main.zip)\n\n\n### **概述**\n---\n* QuTrunk 是启科量子自主研发的一款免费、开源、跨平台的量子计算编程框架，包括量子编程API、量子命令转译、量子计算后端接口等。\n* QuTrunk 使用 Python 作为宿主语言，利用 Python 的语法特性实现针对量子程序的 DSL (领域专用语言)，所有使用 Python 编程的 IDE 均可使用安装。\n* QuTrunk 基于量子逻辑门、量子线路等概念提供量子编程所需各类 API，这些 API 由相应的模块实现。例如 QCircuit 实现量子线路，Qubit 实现量子比特，Qureg 实现量子寄存器，Command 实现每个量子门操作的指令，Backend 实现运行量子线路的后端模块，gate 模块实现各类基础量子门操作。\n* QuTrunk 还可以作为其他上层量子计算应用的基础，例如：量子算法、量子可视化编程、量子机器学习等。\n\nQuTrunk内部模块划分及层次结构如下：  \n\n<div align=center>\n<img src="http://developer.queco.cn/media/images/qutrunkTuPian.original.png"/>\n</div>\n\n\n### **核心模块**\n---\n* cicuit: 量子线路，通过应用各类基础门操作以及算符操作构建量子线路，代表了整个量子算法的实现。\n* qubit: 代表单个量子比特，是量子门和量子算符操作的目标对象。\n* qureg: 用于申请量子计算资源，维护若干个量子比特，用于实现某个具体的量子算法。\n* gate: 量子逻辑门模块，提供各类基础量子门操作，包括:*H*, *X*, *Y*, *Z*，*P*, *R*, *Rx*, *Ry*, *Rz*, *S*, *Sdg*, *T*, *Tdg*, *CNOT*, *Toffoli*, *Swap*等。\n* operator: 量子算符操作，通过若干基础量子门实现某些通用量子操作，比如振幅放大QAA, 量子傅立叶变换QFT等。\n* command: 对量子线路中所有门级操作做参数化处理，对接目标后端模块，用于运行整个量子线路。\n* qasm: 兼容OpenQASM 2.0标准，实现量子线路到OpenQASM指令的序列化和反序列化。\n* qusl: QuTrunk量子汇编标准，实现与qasm类似功能。\n* backend: 量子计算后端模块，用于执行量子线路，支持Python本地后端，qusprout和qusaas两种远程后端以及第三方后端(目前支持IBM和AWS Braket)。\n* qusprout: 对接启科研制的qubox设备，使用经典计算资源并针对量子计算特点做优化，提供高性能量子模拟计算服务。\n* qusaas: 对接启科量子计算云平台，接入多种量子计算资源，包括经典计算资源，离子阱量子计算机（研发中）。\n\n\n### 主要特点\n---\n* 基于量子逻辑门、量子算符和量子线路实现量子程序开发。\n* 提供QuSL量子汇编指令标准，QuSL量子汇编与Python代码完全兼容。\n* 设备独立，同一个量子线路只需替换后端类型即可以在不同的量子后端上运行。\n* 提供多种量子计算体验，本地量子计算提供Python计算后端，远程后端提供OMP多线程、MPI多节点并行、GPU加速等计算模式，同时预留了接口对接启科量子自行研制的离子阱量子计算机。\n* 兼容多种量子汇编指令格式：OpenQASM 2.0标准和QuSL汇编标准。\n* 支持量子可视化编程（需要配合启科量子研发的量子集成开发环境 QuBranch）。\n\n\n### **下载和安装**\n---\n#### **pip安装** \n\nQuTrunk 已发布于 PyPI 官网，可以通过 pip 命令进行安装。\n注意在正式使用 QuTurnk 之前，您需要先安装 Python（版本 3.8+）。\n\n  ```shell\n  pip install qutrunk\n  \n  # AWS Braket后端以可选包的方式提供，需单独安装\n  pip install \'qutrunk[braket]\'\n  ```\n\n验证QuTrunk是否安装成功，打开终端进入python交互模式，执行如下语句：\n\n``` python\nimport qutrunk\nqutrunk.run_check()\n```\n输出结果为："QuTrunk is installed successfully! You can use QuTrunk now."表明QuTrunk安装成功。\n\n\n### **示例代码**\n---\n以下示例展示了利用 QuTrunk 运行 bell-pair 量子算法：\n\n  ```python\n  # import package\n  from qutrunk.circuit import QCircuit\n  from qutrunk.circuit.gates import H, CNOT, Measure, All\n\n  # allocate resource\n  qc = QCircuit()\n  qr = qc.allocate(2) \n\n  # apply quantum gates\n  H * qr[0]   \n  CNOT * (qr[0], qr[1])\n  All(Measure) * qr\n\n  # print circuit\n  qc.print()   \n  # run circuit\n  res = qc.run(shots=1024) \n  # print result\n  print(res.get_counts()) \n  # draw circuit\n  qc.draw()\n  ```\n\n运行结果：\n<div>\n<img src="http://developer.queco.cn/media/images/bell_pairYunXingJieGuo.original.png"/>\n</div>\n\n### **量子可视化编程**  \n---\nQuBranch是由启科量子基于vscode开发的量子编程集成开发环境, QuTrunk与QuBranch相互配合可以实现量子可视化编程,\n具体步骤参见[量子可视化编程](http://developer.queco.cn/learn/doc/detail?id=12&childrenid=14)\n\n### **文档**\n---\n* [QuTrunk 快速上手教程](http://developer.queco.cn/learn/doc/detail?id=12&childrenid=14)\n* [QuTrunk API](http://developer.queco.cn/qutrunk_api/)\n\n\n### **如何参与开发**\n---\n1. 阅读源代码，了解我们当前的开发方向\n2. 找到自己感兴趣的功能或模块\n3. 进行开发，开发完成后自测功能是否正确\n4. Fork代码库，将修复代码提交到fork的代码库\n5. 发起pull request\n6. 更多详情请参见[链接](./CONTRIBUTING.md)\n\n\n### **许可证**\n---\nQuTrunk是自由和开源的，在Apache 2.0许可证版本下发布。\n',
    'author': 'qudoorzh2022',
    'author_email': 'qudoorzh2022@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.qudoor.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
