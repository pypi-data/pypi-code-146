from dataclasses import dataclass
from typing import Optional


@dataclass
class Morpheme:
    """MeCabの解析結果を要素別に格納するためのdataclassです。

    Variables
    ---------
    token : str
        形態素 （例：'食べ'）

    pos0 : str | None
        語の品詞 (part of speech)
        （例：'動詞'）

    pos1 : str | None
        品詞細分類1
        （例：'代名詞'）

    pos2 : str | None
        品詞細分類2
        （例：'一般'）

    pos3 : str | None
        品詞細分類3
        （例：'場所'）

    conjugation_type : str | None
        活用型
        （例：'下一段-バ行'）

    conjugation : str | None
        活用形
        （例：'未然形-一般'）

    stem_form : str | None
        原形
        （例：'食べる'）

    pronunciation : str | None
        発音
        （例：'タベ'）

    unknown : str | None
        正常に抽出できなかった場合はここに入ります。

    **それぞれの要素に入る値は使用する辞書によって異なります。**
    """
    token: str
    pos0: Optional[str]
    pos1: Optional[str]
    pos2: Optional[str]
    pos3: Optional[str]
    conjugation_type: Optional[str]
    conjugation: Optional[str]
    stem_form: Optional[str]
    pronunciation: Optional[str]
    unknown: Optional[str]
