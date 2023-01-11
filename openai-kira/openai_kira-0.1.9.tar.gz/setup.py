# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['openai_kira',
 'openai_kira.Chat',
 'openai_kira.Chat.module',
 'openai_kira.Chat.module.plugin',
 'openai_kira.Chat.text_analysis_tools',
 'openai_kira.Chat.text_analysis_tools.api.keyphrase',
 'openai_kira.Chat.text_analysis_tools.api.keywords',
 'openai_kira.Chat.text_analysis_tools.api.sentiment',
 'openai_kira.Chat.text_analysis_tools.api.summarization',
 'openai_kira.Chat.text_analysis_tools.api.text_similarity',
 'openai_kira.api',
 'openai_kira.resouce',
 'openai_kira.utils']

package_data = \
{'': ['*'],
 'openai_kira.Chat.text_analysis_tools': ['api/data/*'],
 'openai_kira.Chat.text_analysis_tools.api.sentiment': ['data/*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'elara>=0.5.4,<0.6.0',
 'httpx>=0.23.1,<0.24.0',
 'jieba>=0.42.1,<0.43.0',
 'loguru>=0.6.0,<0.7.0',
 'nltk>=3.8,<4.0',
 'numpy>=1.24.1,<2.0.0',
 'openai-async>=0.0.2,<0.0.3',
 'pillow>=9.3.0,<10.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'redis>=4.4.0,<5.0.0',
 'transformers>=4.25.1,<5.0.0']

setup_kwargs = {
    'name': 'openai-kira',
    'version': '0.1.9',
    'description': 'A chat client',
    'long_description': '# openai-kira\n\nOpenai GPT3 ChatBot 框架包，在未公开前快速实现类 ChatGPT接入（公开后就接入chatGPT），打包成依赖的玩具。提供 redis 和 文件数据库\n两个选择。\n\n## Use\n\n`pip install -U openai-kira`\n\n**init**\n\n```python\nimport openai_kira\n\n# \nopenai_kira.setting.redisSetting = openai_kira.setting.RedisConfig()\nopenai_kira.setting.dbFile = "openai_msg.db"\nopenai_kira.setting.openaiApiKey = ["key", "key2"]\nopenai_kira.setting.proxyUrl = None  # "127.0.0.1"\n# 插件的设置\nopenai_kira.setting.webServerUrlFilter = False\nopenai_kira.setting.webServerStopSentence = ["广告", "营销号"]\n```\n\n## Exp\n\nSEE `./test` for More Exp!\n\n```python\nimport asyncio\n\nimport openai_kira\nfrom openai_kira import Chat\n\nprint(openai_kira.RedisConfig())\nopenai_kira.setting.openaiApiKey = ["key"]\n\nreceiver = Chat.Chatbot(\n    conversation_id=10086,\n    call_func=None,  # Api_keys.pop_api_key,\n    start_sequ="Ai:",\n    restart_sequ="Human:",\n)\n\n\nasync def main():\n    response = await receiver.get_chat_response(model="text-davinci-003",\n                                                prompt="你好",\n                                                max_tokens=500,\n                                                role="你扮演...",\n                                                web_enhance_server={"time": ""}\n                                                )\n    print(response)\n\n\nasyncio.run(main())\n```\n\n```python\nimport asyncio\nimport openai_kira\n\nprint(openai_kira.RedisConfig())\nopenai_kira.setting.openaiApiKey = ["key"]\nprint(openai_kira.setting.openaiApiKey)\n\n\nasync def main():\n    try:\n        response = await openai_kira.Completion().create(model="text-davinci-003",\n                                                         prompt="Say this is a test",\n                                                         temperature=0,\n                                                         max_tokens=20)\n        # TEST\n        print(response)\n        print(type(response))\n    except Exception as e:\n        print(e)\n        if "Incorrect API key provided" in e:\n            print("OK")\n        else:\n            print("NO")\n\n\nasyncio.run(main())\n```\n\n## Plugin\n\n**Table**\n\n| plugins   | desc              | value/server                                          | use                                   |\n|-----------|-------------------|-------------------------------------------------------|---------------------------------------|\n| `time`    | now time          | `""`,no need                                          | `明昨今天`....                            |\n| `week`    | week time         | `""`,no need                                          | `周几` .....                            |\n| `search`  | Web Search        | `["some.com?searchword={}"]`,must need                | `查询` `你知道` len<80 / end with`?`len<15 |\n| `duckgo`  | Web Search        | `""`,no need,but need `pip install duckduckgo_search` | `查询` `你知道` len<80 / end with`?`len<15 |\n| `details` | answer with steps | `""`,no need                                          | Ask for help `how to`                 |\n\n## Plugin dev\n\nThere is a middleware between the memory pool and the analytics that provides some networked retrieval support and\noperational support. It can be spiked with services that interface to other Api\'s.\n\n**Prompt Injection**\n\nUse `""` `[]` to emphasise content.\n\n### Exp\n\nFirst create a file in `openai_kira/Chat/module/plugin` without underscores (`_`) in the file name.\n\n**Template**\n\n```python\nfrom ..platform import ChatPlugin, PluginConfig\nfrom ._plugin_tool import PromptTool\nimport os\nfrom loguru import logger\n\nmodulename = os.path.basename(__file__).strip(".py")\n\n\n@ChatPlugin.plugin_register(modulename)\nclass Week(object):\n    def __init__(self):\n        self._server = None\n        self._text = None\n        self._time = ["time", "多少天", "几天", "时间", "几点", "今天", "昨天", "明天", "几月", "几月", "几号",\n                      "几个月",\n                      "天前"]\n\n    def requirements(self):\n        return []\n\n    async def check(self, params: PluginConfig) -> bool:\n        if PromptTool.isStrIn(prompt=params.text, keywords=self._time):\n            return True\n        return False\n\n    async def process(self, params: PluginConfig) -> list:\n        _return = []\n        self._text = params.text\n        # 校验\n        if not all([self._text]):\n            return []\n        # GET\n        from datetime import datetime, timedelta, timezone\n        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)\n        bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))\n        now = bj_dt.strftime("%Y-%m-%d %H:%M")\n        _return.append(f"Current Time UTC8 {now}")\n        # LOGGER\n        logger.trace(_return)\n        return _return\n```\n\n`openai_kira/Chat/module/plugin/_plugin_tool.py` provides some tool classes, PR is welcome\n\n**Testing**\n\nYou cannot test directly from within the module package, please run the `openai_kira/Chat/test_module.py` file to test\nthe module, with the prompt matching check.\n\nAlternatively, you can safely use `from loguru import logger` + `logger.trace(_return)` in the module to debug the\nmodule variables and the trace level logs will not be output by the production environment.\n\n## 结构\n\n```markdown\n.\n└── openai_kira\n├── api\n│ ├── api_url.json\n│ ├── api_utils.py\n│ ├── network.py\n├── Chat\n│ ├── __init__.py\n│ ├── module\n│ ├── Summer.py\n│ ├── test_module.py\n│ ├── text_analysis_tools\n│ └── vocab.json\n├── __init__.py\n├── requirements.txt\n├── resouce\n│ ├── completion.py\n│ ├── __init__.py\n└── utils\n├── data.py\n├── Network.py\n└── Talk.py\n```\n\n## EULA(end-user-license-agreement)\n\n**cn**\n\n1. 自行因为不当操作导致的损失。\n2. 本项目并非官方项目。\n3. 因为安全事故导致的损失我不负责。\n4. 拒绝未经授权的专利/软著相关用途。\n\n**en**\n\n1. the damage caused by improper operation on its own.\n2. This is not an official project.\n3. I am not responsible for any damage caused by safety incidents.\n',
    'author': 'sudoskys',
    'author_email': 'coldlando@hotmail.com',
    'maintainer': 'sudoskys',
    'maintainer_email': 'coldlando@hotmail.com',
    'url': 'https://github.com/sudoskys/openai-kira',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
