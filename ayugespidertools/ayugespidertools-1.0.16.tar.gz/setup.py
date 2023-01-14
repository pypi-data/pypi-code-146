# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayugespidertools',
 'ayugespidertools.commands',
 'ayugespidertools.common',
 'ayugespidertools.templates.project.module',
 'ayugespidertools.templates.project.module.common',
 'ayugespidertools.templates.project.module.spiders',
 'ayugespidertools.utils']

package_data = \
{'': ['*'],
 'ayugespidertools': ['VIT/*',
                      'docs/*',
                      'docs/images/*',
                      'templates/project/*',
                      'templates/spiders/*'],
 'ayugespidertools.templates.project.module': ['VIT/*']}

install_requires = \
['DBUtils>=3.0.2,<4.0.0',
 'Pillow>=9.2.0,<10.0.0',
 'PyExecJS>=1.5.1,<2.0.0',
 'PyMySQL>=1.0.2,<2.0.0',
 'SQLAlchemy>=1.4.41,<2.0.0',
 'Scrapy>=2.6.3,<3.0.0',
 'WorkWeixinRobot>=1.0.1,<2.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'environs>=9.5.0,<10.0.0',
 'html2text>=2020.1.16,<2021.0.0',
 'itemadapter>=0.7.0,<0.8.0',
 'loguru>=0.6.0,<0.7.0',
 'mmh3>=3.0.0,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'opencv-python>=4.6.0.66,<5.0.0.0',
 'oss2>=2.16.0,<3.0.0',
 'pandas>=1.5.0,<2.0.0',
 'pycryptodome>=3.15.0,<4.0.0',
 'pymongo>=3.12.3,<4.0.0',
 'requests>=2.28.1,<3.0.0',
 'retrying>=1.3.3,<2.0.0']

entry_points = \
{'console_scripts': ['ayugespidertools = '
                     'ayugespidertools.utils.cmdline:execute']}

setup_kwargs = {
    'name': 'ayugespidertools',
    'version': '1.0.16',
    'description': 'scarpy 扩展库：在爬虫和其它开发中遇到的一些工具库集合',
    'long_description': '![image-20221213151510988](https://raw.githubusercontent.com/shengchenyang/AyugeSpiderTools/main/ayugespidertools/docs/images/ayugespidertools_logo.png)\n\n\n# AyugeSpiderTools 工具说明\n\n> 本文章用于说明在爬虫开发中遇到的各种通用方法，还有 `scrapy` 扩展库开发，将其打包成 `Pypi` 包以方便安装和使用，此工具会长久维护。\n\n## 前言\n在使用 `Python` `Scrapy` 库开发爬虫时，免不了会重复的修改和编写 `settings.py`，`middlewares.py`，`pipelines.py`，`item.py` 和一些通用方法或脚本，但其实各个项目中的这些文件内容大致相同，那为何不把他们统一整理在一起呢。虽说可以使用 `scrapy` 的模板功能，但是还是无法适配所有的开发场景，它只适用于锦上添花。\n\n刚开始我也只是想把它用来适配 `Mysql` 存储的场景，可以自动创建相关数据库，数据表，字段注释，自动添加新添加的字段，和自动修复常见（字段编码，`Data too long`，存储字段不存在等等）的存储问题。后来不断优化和添加各种场景，使得爬虫开发几乎只用在意 `spider` 脚本的解析规则和 `VIT` 下的 `.conf` 配置即可，脱离无意义的重复操作。\n\n至于此库做了哪些功能，只要你熟悉 `python` 语法和 `scrapy` 库，再结合 [DemoSpider](https://github.com/shengchenyang/DemoSpider) 的应用示例，你可以很快上手。\n\n**在使用过程中若遇到各种问题，或有任何优化建议欢迎提 Issues**\n\n## 项目状态\n\n> 目前项目正处于**积极开发和维护**中\n\n项目目前暂定主要包含**两大部分**：\n\n- 开发场景中的工具库\n  - 比如 `MongoDB`，`Mysql sql` 语句的生成，图像处理，数据处理相关 ... ...\n- `Scrapy` 扩展功能（主推功能）\n  - 使爬虫开发无须在意数据库和数据表结构，不用去管常规 `item, pipelines` 和 `middlewares` 的文件的编写\n\n注：具体内容请查看本文中的 [TodoList](# TodoList) 内容\n\n## 1. 前提条件\n\n> `python 3.8+` 可以直接输入以下命令：\n\n```shell\npip install ayugespidertools -i https://pypi.org/simple\n```\n\n注：本库依赖中的 `pymongo` 版本要在 `3.12.3` 及以下是因为我的 `mongoDB` 的版本为 `3.4`，`pymogo` 官方从 `3.12.3` 以后的版本开始不再支持 `3.6` 版本以下的 `MongoDB` 数据库了，望周知！\n\n### 1.1. 使用方法\n\n#### 1.1.1. Scrapy 扩展库场景\n\n> 此扩展使 `Scrapy` 爬虫开发不用考虑其 `item` 编写，内置通用的 `middlewares` 中间件方法（随机请求头，动态/独享代理等），和常用的 `pipelines` 方法（`Mysql`，`MongoDB` 存储，`Kafka`，`RabbitMQ` 推送队列等）。\n>\n> 开发人员只需根据命令生成示例模板，再配置并激活相关设置即可，可以专注于爬虫 `spider` 的开发。\n\n使用方法示例 `GIF` 如下： \n\n![ayugespidertools.gif](https://raw.githubusercontent.com/shengchenyang/AyugeSpiderTools/main/ayugespidertools/docs/images/ayugespidertools.gif)\n\n对以上 `GIF` 中的步骤进行解释：\n\n```shell\n查看库版本\nayugespidertools version\n\n创建项目\nayugespidertools startproject <project_name>\n\n进入项目根目录\ncd <project_name>\n\n生成爬虫脚本\nayugespidertools genspider <spider_name> <example.com>\n\n替换(覆盖)为真实的配置 .conf 文件；这里是为了演示方便，正常情况是直接在 VIT 路径下的 .conf 配置文件填上相关配置即可\ncp /root/mytemp/.conf DemoSpider/VIT/.conf\n\n运行脚本\nscrapy crawl <spider_name>\n```\n\n具体使用方法请在 [DemoSpider 之 AyugeSpiderTools 工具应用示例](https://github.com/shengchenyang/DemoSpider) 项目中查看，目前已适配以下场景：\n\n```diff\n# 采集数据存入 `Mysql` 的场景：\n- 1).demo_one: 配置根据本地 `settings` 的 `LOCAL_MYSQL_CONFIG` 中取值\n+ 3).demo_three: 配置根据 `consul` 的应用管理中心中取值\n+ 5).demo_five: 异步存入 `Mysql` 的场景\n\n# 采集数据存入 `MongoDB` 的场景：\n- 2).demo_two: 采集数据存入 `MongoDB` 的场景（配置根据本地 `settings` 的 `LOCAL_MONGODB_CONFIG` 中取值）\n+ 4).demo_four: 采集数据存入 `MongoDB` 的场景（配置根据 `consul` 的应用管理中心中取值）\n+ 6).demo_six: 异步存入 `MongoDB` 的场景\n\n# 将 `Scrapy` 的 `Request`，`FormRequest` 替换为其它工具实现的场景\n- 以上为使用 scrapy Request 的场景\n+ 7).demo_seven: scrapy Request 替换为 requests 请求的场景(一般情况下不推荐使用，同步库会拖慢 scrapy 速度，可用于测试场景)\n\n+ 8).demo_eight: 同时存入 Mysql 和 MongoDB 的场景\n\n- 9).demo_aiohttp_example: scrapy Request 替换为 aiohttp 请求的场景，提供了各种请求场景示例（GET,POST）\n+ 10).demo_aiohttp_test: scrapy aiohttp 在具体项目中的使用方法示例\n\n+ 11).demo_proxy_one: 快代理动态隧道代理示例\n+ 12).demo_proxy_two: 测试快代理独享代理\n```\n\n注：具体内容及时效性请以 [DemoSpider](https://github.com/shengchenyang/DemoSpider) 项目中描述为准。\n\n#### 1.1.2. 开发场景\n\n其开发场景下的功能，请在本文 [2. 功能介绍](# 2. 功能介绍) 部分中查看。\n\n## 2. 功能介绍\n\n### 2.1. 数据格式化\n\n> 目前此场景下的功能较少，后面会慢慢丰富其功能\n\n#### 2.1.1. get_full_url\n\n根据域名 `domain_name` 拼接 `deal_url` 来获得完整链接，示例如下：\n\n```python\nfull_url = FormatData.get_full_url(\n    domain_name="https://static.geetest.com",\n    deal_url="/captcha_v3/batch/v3/2021-04-27T15/word/4406ba6e71cd478aa31e0dca37601cd4.jpg")\nprint(full_url)\n```\n\n输出为：\n\n```\nhttps://static.geetest.com/captcha_v3/batch/v3/2021-04-27T15/word/4406ba6e71cd478aa31e0dca37601cd4.jpg\n```\n\n#### 2.1.2. click_point_deal\n\n将小数 `decimal` 保留小数点后 `decimal_places` 位，结果四舍五入，示例如下：\n\n```\nres = FormatData.click_point_deal(13.32596516, 3)\n```\n\n输出为：\n\n```\n13.326\n```\n\n#### 2.1.3. normal_to_stamp\n\n将网页中显示的正常时间转为时间戳\n\n```python\nnormal_stamp = FormatData.normal_to_stamp("Fri, 22 Jul 2022 01:43:06 +0800")\nprint("normal_stamp1:", normal_stamp)\n\nnormal_stamp = FormatData.normal_to_stamp("Thu Jul 22 17:59:44 2022")\nprint("normal_stamp2:", normal_stamp)\n\nnormal_stamp = FormatData.normal_to_stamp("2022-06-21 16:40:00")\n\nnormal_stamp = FormatData.normal_to_stamp("2022/06/21 16:40:00")\nprint("normal_stamp4:", normal_stamp)\n\nnormal_stamp = FormatData.normal_to_stamp("2022/06/21", date_is_full=False)\nprint("normal_stamp4_2:", normal_stamp)\n\n# 当是英文的其他格式，或者混合格式时，需要自己自定时间格式化符\nnormal_stamp = FormatData.normal_to_stamp(\n    normal_time="2022/Dec/21 16:40:00",\n    _format_t="%Y/%b/%d %H:%M:%S")\nprint("normal_stamp5:", normal_stamp)\n```\n\n输出为：\n\n```\nnormal_stamp1: 1658425386\nnormal_stamp2: 1658483984\nnormal_stamp3: 1655800800\nnormal_stamp4: 1655800800\nnormal_stamp4_2: 1655740800\nnormal_stamp5: 1671612000\n```\n\n### 2.2. 图片相关操作\n\n#### 2.2.1. 滑块验证码缺口距离识别\n\n通过背景图片和缺口图片识别出滑块距离，示例如下：\n\n```python\n# 参数为图片全路径的情况\ngap_distance = Picture.identify_gap("doc/image/2.jpg", "doc/image/1.png")\nprint("滑块验证码的缺口距离1为：", gap_distance)\nassert gap_distance in list(range(205, 218))\n\n# 参数为图片 bytes 的情况\nwith open("doc/image/1.png", "rb") as f:\n    target_bytes = f.read()\nwith open("doc/image/2.jpg", "rb") as f:\n    template_bytes = f.read()\ngap_distance = Picture.identify_gap(template_bytes, target_bytes, "doc/image/33.png")\nprint("滑块验证码的缺口距离2为：", gap_distance)\n```\n\n结果为：\n\n| 识别结果展示                                                 | 备注                                                   |\n| :----------------------------------------------------------- | ------------------------------------------------------ |\n| <img src="ayugespidertools/docs/images/image-20220802110652131.png" alt="image-20221208100846241" style="zoom: 25%;" /> | 无                                                     |\n| <img src="ayugespidertools/docs/images/image-20220802110842737.png" alt="image-20221208100846241" style="zoom: 25%;" /> | 可以展示只识别滑块小方块的结果，得到更精准的坐标数据。 |\n\n#### 2.2.2. 滑块验证轨迹生成\n\n根据滑块缺口的距离生成轨迹数组，目前也不是通用版。\n\n```python\ntracks = VerificationCode.get_normal_track(space=120)\n```\n\n结果为：\n\n```\n生成的轨迹为： [[2, 2, 401], [4, 4, 501], [8, 6, 603], [13, 7, 701], [19, 7, 801], [25, 7, 901], [32, 10, 1001], [40, 12, 1101], [48, 14, 1201], [56, 15, 1301], [65, 18, 1401], [74, 19, 1501], [82, 21, 1601], [90, 21, 1701], [98, 22, 1801], [105, 23, 1901], [111, 25, 2001], [117, 26, 2101], [122, 28, 2201], [126, 30, 2301], [128, 27, 2401], [130, 27, 2502], [131, 30, 2601], [131, 28, 2701], [120, 30, 2802]]\n```\n\n### 2.3. Mysql 相关\n\n`sql` 语句简单场景生成，目前是残废版，只适用于简单场景。\n\n更多复杂的场景请查看 [directsql](https://pypi.org/project/directsql/#history), [python-sql](https://pypi.org/project/python-sql/#history),  [pypika](https://pypi.org/project/PyPika/#description) 或 [pymilk](https://pypi.org/project/pymilk/) 的第三方库实现，以后会升级本库的方法。\n\n```python\n# mysql 连接\nfrom ayugespidertools import MysqlClient\nfrom ayugespidertools.common.SqlFormat import AboutSql\n\n\nmysql_client = MysqlClient.MysqlOrm(NormalConfig.PYMYSQL_CONFIG)\n\n# test_select_data\nselect_sql, select_value = AboutSql.select_generate(\n    db_table="zhihu_answer_info",\n    key=["id", "q_title"],\n    rule={"q_id|=": "34987206"},\n    limit=1)\nprint(f"select_sql: {select_sql}, select_value: {select_value}")\nmysql_client.search_data(select_sql, select_value, type="one")\n\n# test_insert_data\ninsert_sql, insert_value = AboutSql.insert_generate(\n    db_table="user",\n    data={"name": "zhangsan", "age": 18})\nprint(f"insert_sql: {insert_sql}, insert_value: {insert_value}")\nmysql_client.insert_data(insert_sql, insert_value)\n\n# test_update_data\nupdate_sql, update_value = AboutSql.update_generate(\n    db_table="user",\n    data={"score": 4},\n    rule={"name": "zhangsan"})\nprint(f"update_sql: {update_sql}, update_value: {update_value}")\nmysql_client.update_data(update_sql, update_value)\n```\n\n结果为：\n```\nselect_sql: select `id`, `q_title` from `zhihu_answer_info` where `q_id`=%s limit 1, select_value: (\'34987206\',)\ninsert_sql: insert into `user` (`name`, `age`) values (%s, %s), insert_value: (\'zhangsan\', 18)\nupdate_sql: update `user` set `score`=%s where `name`=%s, update_value: (4, \'zhangsan\')\n```\n\n### 2.4. 自动化相关\n\n目前是残废阶段，以后放上一些自动化相关操作\n\n### 2.5. 执行 js 相关\n\n鸡肋封装，以后会优化和添加多个常用功能。**推荐  [`PyMiniRacer`](https://github.com/sqreen/PyMiniRacer) 或 `D8` 运行 `js`，会少很多坑！**\n\n```python\n# 测试运行 js 文件中的方法\njs_res = RunJs.exec_js("doc/js/add.js", "add", 1, 2)\nprint("test_exec_js:", js_res)\nassert js_res\n\n# 测试运行 ctx 句柄中的方法\nwith open(\'doc/js/add.js\', \'r\', encoding=\'utf-8\') as f:\n    js_content = f.read()\nctx = execjs.compile(js_content)\n\njs_res = RunJs.exec_js(ctx, "add", 1, 2)\nprint("test_exec_js_by_file:", js_res)\nassert js_res\n```\n\n## 3. 总结\n\n项目目前是疯狂开发阶段，会慢慢丰富 `python` 开发中的遇到的通用方法。\n\n## TodoList\n\n- [x] `scrapy` 的扩展功能场景\n  - [ ] `scrapy` 结合 `crawlab` 的日志统计功能\n  - [x] `scrapy` 脚本运行信息统计和项目依赖表采集量统计，可用于日志记录和预警\n  - [x] 自定义模板，在 `ayugespidertools startproject <projname>` 和 `ayugespidertools genspider <spidername>` 时生成适合本库的模板文件\n  - [x] ~~增加根据 `nacos` 来获取配置的功能~~ -> 改为增加根据 `consul` 来获取配置的功能\n  - [x] 代理中间件（独享代理、动态隧道代理）\n  - [x] 随机请求头 `UA` 中间件，根据 `fake_useragent` 中的权重来随机\n  - [x] 使用以下工具来替换 `scrapy` 的 `Request` 来发送请求\n    - [ ] `selenum`: 性能没有 `pyppeteer` 强\n    - [x] `pyppeteer`: `Gerapy-pyppeteer` 库已经实现此功能\n    - [x] `requests`: 这个不推荐使用，`requests` 同步库会降低 `scrapy` 运行效率\n    - [ ] `splash`: 继承 `splash` 渲染 `js` 的功能\n    - [x] `aiohttp`: 集成将 `scrapy Request` 替换为 `aiohttp` 的协程方式\n  - [x] `Mysql` 存储的场景下适配\n    - [x] 自动创建 `Mysql` 用户场景下需要的数据库和数据表及字段格式，还有字段注释\n  - [x] `MongoDB` 存储的场景下适配，编写风格与 `Mysql` 存储等场景下一致\n  - [ ] 集成 `Kafka`，`RabbitMQ` 等数据推送功能\n  - [ ] ... ...\n- [x] 常用开发场景\n  - [x] `sql` 语句拼接，只是简单场景，后续优化。已给出优化方向，参考库等信息。\n  - [x] `mongoDB` 语句拼接\n  - [x] 数据格式化处理，比如：去除网页标签，去除无效空格等\n  - [ ] 字体反爬还原方法\n  - [x] `html` 格式转 `markdown` 格式\n  - [x] `html` 数据处理，去除标签，不可见字符，特殊字符改成正常显示等等等\n  - [x] 添加常用的图片验证码中的处理方法\n    - [x] 滑块缺口距离的识别方法（多种实现方式）\n    - [x] 根据滑块距离生成轨迹数组的方法\n    - [x] 识别点选验证码位置及点击顺序，识别结果不太好，待优化\n    - [ ] 图片乱序混淆的还原方法\n  - [ ] ... ...\n',
    'author': 'ayuge',
    'author_email': 'ayuge.s@qq.com',
    'maintainer': 'ayuge',
    'maintainer_email': 'ayuge.s@qq.com',
    'url': 'http://175.178.210.193:8090/mkdocs-material/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
