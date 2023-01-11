# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kakao_json', 'kakao_json.components']

package_data = \
{'': ['*']}

install_requires = \
['msgspec>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'kakao-json',
    'version': '1.0.1',
    'description': '카카오챗봇 JSON helper',
    'long_description': '<div align="center">\n<p>\n    <img width="680" src="https://raw.githubusercontent.com/Alfex4936/kakaoChatbot-Ajou/main/imgs/chatbot.png">\n</p>\n\n<h2>카카오톡 챗봇 빌더 도우미</h2>\n<h3>Python언어 전용</h3>\n</div>\n\n# 소개\n\nPython 언어로 카카오 챗봇 서버를 만들 때 좀 더 쉽게 JSON 메시지 응답을 만들 수 있게 도와줍니다.\n\nSimpleText, SimpleImage, ListCard, Carousel, BasicCard, CommerceCard, ItemCard 등의\n\n챗봇 JSON 데이터를 쉽게 만들 수 있도록 도와줍니다.\n\n# 설치\n```bash\npip install pykakao\n```\n\n\n# 사용법\n\n## ListCard 예제\n\n```python\nfrom pykakao import Button, Kakao, ListItem\n\n\nk = Kakao()\n\n    k.add_qr("오늘", "카톡 발화문1")\n    k.add_qr("어제")  # label becomes also messageText\n\n    list_card = k.init_list_card().set_header("리스트 카드 제목")\n    list_card.add_button(Button("그냥 텍스트 버튼", "message"))\n    list_card.add_button(k.init_button("link label").set_link("https://google.com"))\n    list_card.add_button(\n        k.init_button("share label").set_action_share().set_msg("카톡에 보이는 메시지")\n    )\n    list_card.add_button(k.init_button("call label").set_number("010-1234-5678"))\n\n    list_card.add_item(\n        ListItem("title").set_desc("description").set_link("https://naver.com")\n    )\n\n    k.add_output(list_card)\n\n    print(k.to_json())\n\n```\n\n```json\n/*\nResult:\n{\n  "template": {\n    "outputs": [\n      {\n        "listCard": {\n          "buttons": [\n            {\n              "label": "그냥 텍스트 버튼",\n              "action": "message"\n            },\n            {\n              "label": "link label",\n              "action": "webLink",\n              "webLinkUrl": "https://google.com"\n            },\n            {\n              "label": "share label",\n              "action": "share",\n              "messageText": "카톡에 보이는 메시지"\n            },\n            {\n              "label": "call label",\n              "action": "phone",\n              "phoneNumber": "010-1234-5678"\n            }\n          ],\n          "header": {\n            "title": "리스트 카드 제목!"\n          },\n          "items": [\n            {\n              "title": "title",\n              "description": "description",\n              "link": {\n                "web": "https://naver.com"\n              }\n            }\n          ]\n        }\n      }\n    ],\n    "quickReplies": [\n      {\n        "action": "message",\n        "label": "오늘",\n        "messageText": "오늘 공지 보여줘"\n      },\n      {\n        "action": "message",\n        "label": "어제",\n        "messageText": "어제 공지 보여줘"\n      }\n    ]\n  },\n  "version": "2.0"\n}\n*/\n```\n',
    'author': 'Seok Won',
    'author_email': 'ikr@kakao.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
