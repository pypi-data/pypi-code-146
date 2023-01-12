# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_imageutils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'bbcode>=1.1.0,<2.0.0',
 'fonttools>=4.0.0,<5.0.0',
 'httpx>=0.19.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.0.0,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'opencv-python-headless>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-imageutils',
    'version': '0.1.13.5',
    'description': 'Nonebot2 PIL工具插件',
    'long_description': '## nonebot-plugin-imageutils\n\n\n### 功能\n\n- 提供 `BuildImage` 类，方便图片尺寸修改、添加文字等操作\n- 提供 `Text2Image` 类，方便实现文字转图，支持少量 `BBCode` 标签\n- 文字支持多种字体切换，能够支持 `emoji`\n- 添加文字自动调节字体大小\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_imageutils\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_imageutils\n```\n\n\n### 配置字体\n\n本插件选择了一些不同系统上的字体，以支持更多的字符\n\n> 对于 `Ubuntu` 系统，建议安装 `fonts-noto` 软件包 以支持中文字体和 emoji\n>\n> 并将简体中文设置为默认语言：（否则会有部分中文显示为异体（日文）字形，详见 [ArchWiki](https://wiki.archlinux.org/title/Localization_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)/Simplified_Chinese_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E4%BF%AE%E6%AD%A3%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87%E6%98%BE%E7%A4%BA%E4%B8%BA%E5%BC%82%E4%BD%93%EF%BC%88%E6%97%A5%E6%96%87%EF%BC%89%E5%AD%97%E5%BD%A2)）\n> ```bash\n> sudo apt install fonts-noto\n> sudo locale-gen zh_CN zh_CN.UTF-8\n> sudo update-locale LC_ALL=zh_CN.UTF-8 LANG=zh_CN.UTF-8\n> fc-cache -fv\n> ```\n\n默认备选字体列表如下：\n```\n"Arial", "Tahoma", "Helvetica Neue", "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Source Han Sans SC", "Noto Sans SC", "Noto Sans CJK JP", "WenQuanYi Micro Hei", "Apple Color Emoji", "Noto Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"\n```\n\n可在 `.env.*` 文件中添加 `default_fallback_fonts` 变量 来自定义备选字体\n\n字体文件需要在系统目录下，或放置于自定义字体路径中\n\n自定义字体路径默认为机器人运行目录下的 `data/fonts/` 文件夹，\n\n可在 `.env.*` 文件中添加 `custom_font_path` 变量 自定义字体路径\n\n其他插件可以通过 `nonebot_plugin_imageutils/fonts.py` 中的 `add_font` 函数往字体文件夹中添加字体\n\n\n### 使用示例\n\n\n- `BuildImage`\n\n```python\nfrom nonebot_plugin_imageutils import BuildImage\n\n# output: BytesIO\noutput = BuildImage.new((300, 300)).circle().draw_text((30, 30, 270, 270), "测试ymddl😂").save_jpg()\n```\n\n![1.jpg](https://s2.loli.net/2022/05/19/gFdpwWPCzreb2X6.jpg)\n\n\n- `Text2Image`\n\n```python\nfrom nonebot_plugin_imageutils import Text2Image\n\n# img: PIL.Image.Image\nimg = Text2Image.from_text("@mnixry 🤗", 50).to_image()\n\n# 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO\noutput = BytesIO()\nimg.save(output, format="png")\nawait matcher.send(MessageSegment.image(output))\n```\n\n![2.png](https://s2.loli.net/2022/05/19/14EXViZQwcGUW5I.png)\n\n\n- 使用 `BBCode`\n\n```python\nfrom nonebot_plugin_imageutils import text2image\n\n# img: PIL.Image.Image\nimg = text2image("N[size=40][color=red]o[/color][/size]neBo[size=30][color=blue]T[/color][/size]\\n[align=center]太强啦[/align]")\n\n# 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO\noutput = BytesIO()\nimg.save(output, format="png")\nawait matcher.send(MessageSegment.image(output))\n```\n\n![3.png](https://s2.loli.net/2022/05/19/VZAXsKB2x65q7rl.png)\n\n目前支持的 `BBCode` 标签：\n- `[align=left|right|center][/align]`: 文字对齐方式\n- `[color=#66CCFF|red|black][/color]`: 字体颜色\n- `[stroke=#66CCFF|red|black][/stroke]`: 描边颜色\n- `[font=msyh.ttc][/font]`: 文字字体\n- `[size=30][/size]`: 文字大小\n- `[b][/b]`: 文字加粗\n\n\n### 特别感谢\n\n- [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) 基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库，非常可爱的绪山真寻bot\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/noneplugin/nonebot-plugin-imageutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
