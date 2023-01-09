'''方便编写ayaka_doc文档，用于生成文档所需要的特定文字'''
from .fake_cq import fake_cq


def record(name: str, text: str):
    if not fake_cq.config.record:
        return
    text = text.replace("<", "&lt;")
    with open("record.log", "a+", encoding="utf8") as f:
        f.write(f'"{name}" 说：{text}\n')
