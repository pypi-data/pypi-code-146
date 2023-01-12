# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'nonebot_plugin_pixivbot_kook': 'src\\nonebot_plugin_pixivbot_kook',
 'nonebot_plugin_pixivbot_kook.protocol_dep': 'src\\nonebot_plugin_pixivbot_kook/protocol_dep',
 'nonebot_plugin_pixivbot_kook.utils': 'src\\nonebot_plugin_pixivbot_kook/utils',
 'nonebot_plugin_pixivbot_onebot_v11': 'src\\nonebot_plugin_pixivbot_onebot_v11',
 'nonebot_plugin_pixivbot_onebot_v11.handler': 'src\\nonebot_plugin_pixivbot_onebot_v11/handler',
 'nonebot_plugin_pixivbot_onebot_v11.protocol_dep': 'src\\nonebot_plugin_pixivbot_onebot_v11/protocol_dep'}

packages = \
['nonebot_plugin_pixivbot',
 'nonebot_plugin_pixivbot.data',
 'nonebot_plugin_pixivbot.data.local_tag',
 'nonebot_plugin_pixivbot.data.pixiv_binding',
 'nonebot_plugin_pixivbot.data.pixiv_repo',
 'nonebot_plugin_pixivbot.data.pixiv_repo.local_repo',
 'nonebot_plugin_pixivbot.data.source',
 'nonebot_plugin_pixivbot.data.source.mongo',
 'nonebot_plugin_pixivbot.data.source.mongo.migration',
 'nonebot_plugin_pixivbot.data.source.sql',
 'nonebot_plugin_pixivbot.data.source.sql.migration',
 'nonebot_plugin_pixivbot.data.subscription',
 'nonebot_plugin_pixivbot.data.utils',
 'nonebot_plugin_pixivbot.data.utils.sql',
 'nonebot_plugin_pixivbot.data.watch_task',
 'nonebot_plugin_pixivbot.handler',
 'nonebot_plugin_pixivbot.handler.command',
 'nonebot_plugin_pixivbot.handler.common',
 'nonebot_plugin_pixivbot.handler.interceptor',
 'nonebot_plugin_pixivbot.handler.sniffer',
 'nonebot_plugin_pixivbot.handler.watch',
 'nonebot_plugin_pixivbot.model',
 'nonebot_plugin_pixivbot.model.message',
 'nonebot_plugin_pixivbot.model.old',
 'nonebot_plugin_pixivbot.protocol_dep',
 'nonebot_plugin_pixivbot.service',
 'nonebot_plugin_pixivbot.utils',
 'nonebot_plugin_pixivbot_kook',
 'nonebot_plugin_pixivbot_kook.protocol_dep',
 'nonebot_plugin_pixivbot_kook.utils',
 'nonebot_plugin_pixivbot_onebot_v11',
 'nonebot_plugin_pixivbot_onebot_v11.handler',
 'nonebot_plugin_pixivbot_onebot_v11.protocol_dep']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'PixivPy-Async>=1.2.14,<2.0.0',
 'SQLAlchemy[asyncio]>=1.4.17,<=1.4.41',
 'aiohttp-socks>=0.7.1,<0.8.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'asyncache>=0.3.1,<0.4.0',
 'cachetools>=5.2.0,<6.0.0',
 'frozendict>=2.3.4,<3.0.0',
 'lazy>=1.4,<2.0',
 'nonebot-plugin-access-control>=0.2.3,<0.3.0',
 'nonebot2>=2.0.0rc2,<3.0.0',
 'nonebot_plugin_apscheduler>=0.2.0,<0.3.0',
 'numpy>=1.23.1,<2.0.0',
 'shortuuid>=1.0.9,<2.0.0',
 'tzlocal>=4.2,<5.0']

extras_require = \
{'kook': ['nonebot-adapter-kaiheila>=0.1.0,<0.2.0'],
 'mongo': ['motor>=3.0.0,<4.0.0', 'beanie>=1.13.1,<2.0.0'],
 'onebot': ['nonebot-adapter-onebot>=2.1.1,<3.0.0'],
 'postgresql': ['asyncpg>=0.27.0,<0.28.0'],
 'telegram': ['nonebot-adapter-telegram>=0.1.0b3,<0.2.0']}

setup_kwargs = {
    'name': 'nonebot-plugin-pixivbot',
    'version': '1.7.0.post2',
    'description': 'Nonebot Plugin PixivBot',
    'long_description': '<!-- markdownlint-disable MD033 MD036 MD041 -->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\nnonebot_plugin_pixivbot\n=====\n\n_✨ PixivBot ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/ssttkkl/nonebot-plugin-pixivbot/master/LICENSE">\n    <img src="https://img.shields.io/github/license/ssttkkl/nonebot-plugin-pixivbot.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-pixivbot">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-pixivbot.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">\n</p>\n\nNoneBot插件，支持发送随机Pixiv插画、画师更新推送、定时订阅推送……\n\n## 开始使用\n\n适配协议：\n\n- [Onebot V11](https://onebot.adapters.nonebot.dev/)\n- [KOOK / 开黑啦](https://github.com/Tian-que/nonebot-adapter-kaiheila)\n- [Telegram](https://github.com/nonebot/adapter-telegram)\n\n没有找到需要的协议？欢迎适配。[适配指南](https://github.com/ssttkkl/nonebot-plugin-pixivbot/wiki/%E9%80%82%E9%85%8D%E6%8C%87%E5%8D%97)\n\n开箱即用的Docker镜像：[ssttkkl/PixivBot](https://github.com/ssttkkl/PixivBot)\n\n## 触发语句\n\n### 普通语句\n\n所有数字参数均支持中文数字和罗马数字。\n\n- **看看<类型>榜<范围>**：查看pixiv榜单（<类型>可省略，<范围>应为a-b或a）\n  - 示例：看看榜、看看日榜、看看榜1-5、看看月榜一\n- **来<数量>张图**：从推荐插画随机抽选一张插画（<数量>可省略，下同）\n  - 示例：来张图、来五张图\n- **来<数量>张<关键字>图**：搜索关键字，从搜索结果随机抽选一张插画\n  - 示例：来张初音ミク图、来五张初音ミク图\n  - 注：默认开启关键字翻译功能。Bot会在平时的数据爬取时记录各个Tag的中文翻译。在搜索时，若关键字的日文翻译存在，则使用日文翻译代替关键字进行搜索。\n- **来<数量>张<用户>老师的图**：搜索用户，从插画列表中随机抽选一张插画\n  - 示例：来张Rella老师的图、来五张Rella老师的图\n- **看看图<插画ID>**：查看ID对应的插画\n  - 示例：看看图114514\n- **来<数量>张私家车**：从书签中随机抽选一张插画（发送者需绑定Pixiv账号，或者在配置中指定默认Pixiv账号）\n  - 示例：来张私家车、来五张私家车\n- **还要**：重复上一次请求\n- **不够色**：获取上一张插画的相关插画\n\n### 命令语句\n\n- **/pixivbot schedule \\<type\\> \\<schedule\\> [..args]**：为本群（本用户）订阅类型为<type>的定时推送功能，时间满足<schedule>时进行推送\n    - \\<type\\>：可选值有ranking, random_bookmark, random_recommended_illust, random_illust, random_user_illust\n    - \\<schedule\\>：有三种格式，*00:30\\*x*为每隔30分钟进行一次推送，*12:00*为每天12:00进行一次推送，*00:10+00:30\\*x*为从今天00:10开始每隔30分钟进行一次推送（开始时间若是一个过去的时间点，则从下一个开始推送的时间点进行推送）\n    - [..args]：\n      - \\<type\\>为ranking时，接受\\<mode\\> \\<range\\>\n        - 示例：/pixivbot schedle ranking 12:00 day 1-10\n      - \\<type\\>为random_bookmark时，接受\\<pixiv_user_id\\>（可空）\n        - 示例：/pixivbot schedle random_bookmark 01:00*x\n        - 示例：/pixivbot schedle random_bookmark 01:00*x 114514\n      - \\<type\\>为random_illust时，接受\\<word\\>，若需要输入空格请用反斜杠`\\ `\n        - 示例：/pixivbot schedle random_illust 01:00*x\n        - 示例：/pixivbot schedle random_illust 01:00*x ロリ\n        - 示例：/pixivbot schedle random_illust 01:00*x Hatsune\\ Miku\n      - \\<type\\>为random_user_illust时，接受\\<user\\>\n        - 示例：/pixivbot schedle random_user_illust 01:00*x 森倉円\n      - \\<type\\>为random_recommend_illust时，不接受参数\n- **/pixivbot schedule**：查看本群（本用户）的所有定时推送订阅\n- **/pixivbot unschedule \\<id\\>**：取消本群（本用户）的指定的定时推送订阅\n- **/pixivbot watch \\<type\\> [..args]**：为本群（本用户）订阅类型为<type>的更新推送功能\n    - \\<type\\>：可选值有user_illusts, following_illusts\n    - [..args]：\n      - \\<type\\>为user_illusts时，接受\\<user\\>\n        - 示例：/pixivbot watch user_illusts 森倉円\n      - \\<type\\>为following_illusts时，接受\\<pixiv_user_id\\>（可空）\n        - 示例：/pixivbot watch following_illusts\n        - 示例：/pixivbot watch following_illusts 114514\n- **/pixivbot watch**：查看本群（本用户）的所有更新推送订阅\n- **/pixivbot watch fetch \\<id\\>**：【调试用命令】立刻手动触发一次指定的更新推送订阅\n- **/pixivbot unwatch \\<id\\> [..args]**：取消本群（本用户）的指定的更新推送订阅\n- **/pixivbot bind \\<pixiv_user_id\\>**：绑定Pixiv账号（用于随机书签功能）\n- **/pixivbot unbind**：解绑Pixiv账号\n- **/pixivbot invalidate_cache**：清除缓存（只有超级用户能够发送此命令）\n- **/pixivbot**、**/pixivbot help**：查看帮助\n\n\n## 环境配置\n\n事前准备：登录pixiv账号并获取refresh_token。（参考：[@ZipFile Pixiv OAuth Flow](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362)、[eggplants/get-pixivpy-token](https://github.com/eggplants/get-pixivpy-token)）\n\n1. 参考[安装 | NoneBot](https://v2.nonebot.dev/docs/start/installation)安装NoneBot；\n2. 参考[创建项目 | NoneBot](https://v2.nonebot.dev/docs/tutorial/create-project)创建一个NoneBot实例；\n3. 使用`pip install nonebot-plugin-pixivbot[xxx]`安装特定适配器的插件；\n4. 修改pyproject.toml，启用插件（`plugins=[..., "nonebot_plugin_pixivbot"]`）；\n5. 在.env.prod中修改配置（参考下方）；\n\n## 配置外部数据库（可选）\n\nPixivBot需要使用数据库存放订阅以及缓存，默认使用SQLite。\n\n### SQLite\n\n若需要自定义SQLite数据库文件路径，请设置配置项：\n\n- pixiv_sql_conn_url=`sqlite+aiosqlite:///<数据库文件路径>`\n\n### PostgreSQL\n\n若需要使用PostgreSQL，请设置配置项：\n\n- pixiv_sql_conn_url=`postgresql+asyncpg://<用户名>:<密码>@<主机>:<端口>/<数据库名>`\n\n并且安装`nonebot-plugin-pixivbot[postgresql]`\n\n### MongoDB\n\n若需要使用MongoDB，请设置配置项：\n- pixiv_mongo_conn_url=`mongodb://<用户名>:<密码>@<主机>:<端口>/<用户所属的数据库>`\n- pixiv_mongo_database_name=`连接的MongoDB数据库`\n\n并且安装`nonebot-plugin-pixivbot[mongo]`\n\n## 权限控制\n\n插件接入了[nonebot-plugin-access-control](https://github.com/ssttkkl/nonebot-plugin-access-control)实现细粒度的权限控制：\n\n```\nnonebot_plugin_pixivbot\n├── common\n│   ├── illust  （看看图）\n│   ├── ranking  （看看榜）\n│   ├── more  （还要）\n│   ├── random_bookmark  （来张私家车）\n│   ├── random_illust  （来张xx图）\n│   ├── random_recommended_illust  （来张图）\n│   ├── random_related_illust  （不够色）\n│   └── random_user_illust  （来张xx老师的图）\n├── illust_link  （P站链接嗅探）\n├── schedule\n│   ├── receive  （接收定时推送）\n│   └── manage  （管理定时推送）\n├── watch\n│   ├── receive  （接收更新推送）\n│   └── manage  （管理定时推送）\n├── invalidate_cache  （清除缓存）\n├── bind  （绑定P站账号）\n├── help  （帮助文本）\n└── r18  （显示R-18内容）\n    └── g  （显示R-18G内容）\n```\n\n超级用户可以通过发送`/ac subject all deny service nonebot_plugin_pixivbot.r18`全局拦截R-18。\n\n具体可以参考[nonebot-plugin-access-control](https://github.com/ssttkkl/nonebot-plugin-access-control)的文档进行权限控制。\n\n## 配置项一览\n\n最小配置：\n```\npixiv_refresh_token=  # 前面获取的REFRESH_TOKEN\n```\n\n完整配置（除最小配置出现的配置项以外都是可选项，给出的是默认值）（NoneBot配置项这里不列出，参考[配置 | NoneBot](https://v2.nonebot.dev/docs/tutorial/configuration#%E8%AF%A6%E7%BB%86%E9%85%8D%E7%BD%AE%E9%A1%B9)）：\n\n```\nsuperuser=[]  # 能够发送超级命令的用户（JSON数组，格式为["onebot:123456", "kaiheila:1919810"]，下同）\n\npixiv_data_source=  # 使用的数据库类型，可选值：sql，mongo。若未设置，则根据是否设置了pixiv_mongo_conn_url自动判断。\npixiv_sql_conn_url=sqlite+aiosqlite:///pixiv_bot.db  # SQL连接URL，仅支持SQLite与PostgreSQL（通过SQLAlchemy进行连接，必须使用异步的DBAPI）\npixiv_mongo_conn_url=  # MongoDB连接URL，格式：mongodb://<用户名>:<密码>@<主机>:<端口>/<数据库>。\npixiv_mongo_database_name=  # 连接的MongoDB数据库\n\npixiv_refresh_token=  # 前面获取的REFRESH_TOKEN\npixiv_proxy=None  # 代理URL，推荐使用socks5代理\npixiv_query_timeout=60  # 查询超时（单位：秒）\npixiv_loading_prompt_delayed_time=5  # 加载提示消息的延迟时间（“努力加载中”的消息会在请求发出多少秒后发出）（单位：秒）\npixiv_simultaneous_query=8  # 向Pixiv查询的并发数\n\n# 缓存过期时间/删除时间（单位：秒）\npixiv_download_cache_expires_in=604800  # 默认值：7天\npixiv_illust_detail_cache_expires_in=604800\npixiv_user_detail_cache_expires_in=604800\npixiv_illust_ranking_cache_expires_in=21600  # 默认值：6小时\npixiv_search_illust_cache_expires_in=86400  # 默认值：1天\npixiv_search_illust_cache_delete_in=2592000  # 默认值：30天\npixiv_search_user_cache_expires_in=86400\npixiv_search_user_cache_delete_in=2592000\npixiv_user_illusts_cache_expires_in=86400\npixiv_user_illusts_cache_delete_in=2592000\npixiv_user_bookmarks_cache_expires_in=86400\npixiv_user_bookmarks_cache_delete_in=2592000\npixiv_related_illusts_cache_expires_in=86400\npixiv_other_cache_expires_in=21600\n\npixiv_block_tags=[]  # 当插画含有指定tag时会被过滤\npixiv_block_action=no_image  # 过滤时的动作，可选值：no_image(不显示插画，回复插画信息), completely_block(只回复过滤提示), no_reply(无回复)\n\npixiv_download_custom_domain=None  # 使用反向代理下载插画的域名\n\npixiv_compression_enabled=False  # 启用插画压缩\npixiv_compression_max_size=None  # 插画压缩最大尺寸\npixiv_compression_quantity=None  # 插画压缩品质（0到100）\n\npixiv_query_to_me_only=False  # 只响应关于Bot的查询\npixiv_command_to_me_only=False  # 只响应关于Bot的命令\n\npixiv_query_cooldown=0  # 每次查询的冷却时间\npixiv_no_query_cooldown_users=[]  # 在这个列表中的用户不受冷却时间的影响（JSON数组）\npixiv_max_item_per_query=10  # 每个查询最多请求的插画数量\n\npixiv_tag_translation_enabled=True  # 启用搜索关键字翻译功能（平时搜索时记录标签翻译，在查询时判断是否存在对应中日翻译）\n\npixiv_more_enabled=True  # 启用重复上一次请求（还要）功能\npixiv_query_expires_in=10*60  # 上一次请求的过期时间（单位：秒）\n\npixiv_illust_query_enabled=True  # 启用插画查询（看看图）功能\n\npixiv_ranking_query_enabled=True  # 启用榜单查询（看看榜）功能\npixiv_ranking_default_mode=day  # 默认查询的榜单，可选值：day, week, month, day_male, day_female, week_original, week_rookie, day_manga\npixiv_ranking_default_range=[1, 3]  # 默认查询的榜单范围\npixiv_ranking_fetch_item=150  # 每次从服务器获取的榜单项数（查询的榜单范围必须在这个数目内）\npixiv_ranking_max_item_per_query=5  # 每次榜单查询最多能查询多少项\n\npixiv_random_illust_query_enabled=True  # 启用关键字插画随机抽选（来张xx图）功能\npixiv_random_illust_method=bookmark_proportion  # 随机抽选方法，下同，可选值：bookmark_proportion(概率与书签数成正比), view_proportion(概率与阅读量成正比), timedelta_proportion(概率与投稿时间和现在的时间差成正比), uniform(相等概率)\npixiv_random_illust_min_bookmark=0  # 过滤掉书签数小于该值的插画，下同\npixiv_random_illust_min_view=0  # 过滤掉阅读量小于该值的插画，下同\npixiv_random_illust_max_page=20  # 每次从服务器获取的查询结果页数，下同\npixiv_random_illust_max_item=500  # 每次从服务器获取的查询结果项数，下同\n\npixiv_random_recommended_illust_query_enabled=True  # 启用推荐插画随机抽选（来张图）功能\npixiv_random_recommended_illust_method=uniform\npixiv_random_recommended_illust_min_bookmark=0\npixiv_random_recommended_illust_min_view=0\npixiv_random_recommended_illust_max_page=40\npixiv_random_recommended_illust_max_item=1000\n\npixiv_random_related_illust_query_enabled=True  # 启用关联插画随机抽选（不够色）功能\npixiv_random_related_illust_method=bookmark_proportion\npixiv_random_related_illust_min_bookmark=0\npixiv_random_related_illust_min_view=0\npixiv_random_related_illust_max_page=4\npixiv_random_related_illust_max_item=100\n\npixiv_random_user_illust_query_enabled=True  # 启用用户插画随机抽选（来张xx老师的图）功能\npixiv_random_user_illust_method=timedelta_proportion\npixiv_random_user_illust_min_bookmark=0\npixiv_random_user_illust_min_view=0\npixiv_random_user_illust_max_page=2147483647\npixiv_random_user_illust_max_item=2147483647\n\npixiv_random_bookmark_query_enabled=True  # 启用用户书签随机抽选（来张私家车）功能\npixiv_random_bookmark_user_id=0  # 当QQ用户未绑定Pixiv账号时，从该Pixiv账号的书签内抽选\npixiv_random_bookmark_method=uniform\npixiv_random_bookmark_min_bookmark=0\npixiv_random_bookmark_min_view=0\npixiv_random_bookmark_max_page=2147483647\npixiv_random_bookmark_max_item=2147483647\n\npixiv_watch_interval=7200  # 更新推送的查询间隔\n```\n\n## Special Thanks\n\n- [Mikubill/pixivpy-async](https://github.com/Mikubill/pixivpy-async)\n\n- [nonebot/nonebot2](https://github.com/nonebot/nonebot2)\n\n## 在线乞讨\n\n<details><summary>点击请我打两把maimai</summary>\n\n![](https://github.com/ssttkkl/ssttkkl/blob/main/afdian-ssttkkl.jfif)\n\n</details>\n\n\n## LICENSE\n\n```\nMIT License\n\nCopyright (c) 2021 ssttkkl\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n```\n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ssttkkl/nonebot-plugin-pixivbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
