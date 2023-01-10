from requests import post
from .crypted import from_base64
from .kry import start_thread
import re, os


def parivartak(val: str, src: str, to: str, html=False) -> str:
    req = post(
        f"https://lipilekhika.deta.dev",
        json={
            "text": val,
            "from": src,
            "to": to,
            "textType": "html" if html else "plain",
        },
    )
    t = req.text
    req.close()
    return t


def anuvadak(txt: str, src: str, to: str, html=False) -> str:
    API_KEY = os.getenv("AZURE_ANUVADAK_KEY")
    if not API_KEY:
        return "API KEY 'AZURE_ANUVADAK_KEY' not set"

    def trnslt(txt1: str, src1: str, to1: str) -> str:
        rq = post(
            "https://api.cognitive.microsofttranslator.com/translate",
            params={
                "api-version": "3.0",
                "from": src1,
                "to": to1,
                "textType": "html" if html else "plain",
            },
            headers={
                "Ocp-Apim-Subscription-Key": from_base64(API_KEY),
                "Ocp-Apim-Subscription-Region": "centralindia",
            },
            json=[{"text": txt1}],
        )
        v = rq.json()[0]["translations"][0]["text"]
        rq.close()
        return v

    r = []
    last = 0
    thrds = []
    c = 0

    def anu_add(tx: str, x: int):
        def fgh(t: str, i: int):
            r[i] = trnslt(t, src, to)

        r.append("")
        thrds.append(start_thread(lambda: fgh(tx, x)))

    for x in re.finditer("(?<=\{).+?(?=\})", txt):
        anu_add(txt[last : x.start() - 1], c)
        r.append(txt[x.start() - 1 : x.end() + 1])
        last = x.end() + 1
        c += 2
    anu_add(txt[last : len(txt)], c)
    for x in thrds:
        x.join()
    return "".join(r)
