"""形態素解析ライブラリMeCabを簡単に使えるようにするモジュールです。

Requirements
------------
- Python 3.6 以上で動作します。
- コンピュータに MeCab がインストールされている必要があります。
- mecab ライブラリが必要です。
"""
import re
from dataclasses import dataclass
from typing import List, Literal, Optional

import MeCab


@dataclass
class Morph:
    """MeCabの解析結果を要素別に格納するためのdataclassです。

    Variables
    ---------
    word : str
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
    word: str
    pos0: Optional[str]
    pos1: Optional[str]
    pos2: Optional[str]
    pos3: Optional[str]
    conjugation_type: Optional[str]
    conjugation: Optional[str]
    stem_form: Optional[str]
    pronunciation: Optional[str]
    unknown: Optional[str]


class InvalidArgumentsError(Exception):
    pass


class MeCabWrapper:
    """MeCabをより簡単に使えるようにするラッパークラスです。

    Features
    --------
    - MeCabの処理結果をdataclassに格納し、アクセスしやすくしています。

    - EOSや空文字('')の除去を行っています。


    Attributes
    ----------
    multiple_instance : bool
        `True` に設定すると、通常通りインスタンスを複数作成できます。

        `False` に設定すると、何度インスタンス生成を行っても同じインスタンスを使用します。

        デフォルトは `False` です。


    Dependencies
    ------------
    - コンピュータにMeCabがインストールされ、プログラムからアクセス可能である必要があります。

    - `mecab-python3` ライブラリがインストールされている必要があります。

    - 同ライブラリの中の Morph dataclass を使用して結果を格納します。
    """

    _none_pattern: List[str] = ['', ' ', '*']  # 該当なしのパターン

    def __init__(self, args: str = '',
                 dict_type: Literal['ipadic', 'neologd', 'unidic'] = 'ipadic') -> None:
        """
        Parameters
        ----------
        args : str, optional
            MeCabの実行時引数を入力してください。
            ただし以下の引数は入力しないでください。

            `-Owakati`, 出力フォーマットを指定するオプション

            デフォルトは引数なしです。

        dict_type : Literal['ipadic, 'neologd', 'unidic'], optional
            MeCabで使用する辞書の表示タイプを選択してください。
            - `'ipadic'` : IPA辞書のデフォルト表示タイプ
            - `'neologd'` : mecab-ipadic-NEologdのデフォルト表示タイプ
            - `'unidic'` : UniDicのデフォルト表示タイプ

            辞書の出力と表示タイプが一致していない場合、正しく結果を抽出できません。
            デフォルトは `'ipadic'` です。

        Raises
        ------
        NotSupportedError
            argsに禁止されている引数が存在する場合に発生します。
        """
        banned_args = (r'-Owakati',
                       r'-F', r'--node-format',
                       r'-U', r'--unk-format',
                       r'-B', r'--bos-format',
                       r'-E', r'--eos-format',
                       r'-S', r'--eon-format',
                       r'-x', r'--unk-feature')
        banned_pattern = '|'.join(banned_args)
        if not re.findall(banned_pattern, args):
            self.tagger = MeCab.Tagger(args)
            self.parse_type = dict_type
        else:
            raise InvalidArgumentsError(
                "対応しない引数がargsに指定されました。\n"
                "MeCabWrapperのargsでは以下に示す引数を使用することはできません。\n"
                f"{banned_args}\n"
                "[ヒント] もし分かち書きをしたいのであれば、wakati_gaki関数を使用することができます。")

    def parse(self, sentence: str) -> List[Morph]:
        """日本語の文字列をMeCabで解析します。

        Parameters
        ----------
        sentence : str
            MeCabで解析したい1行の文章

        Returns
        -------
        list[Morph]
            形態素ごとにそれぞれ Morph クラスに情報が格納されています。
            （アクセス例：`mecab_agent.parse()[0].word`）
            詳細は Morph クラスの DocString を参照してください。
        """
        result: list[Morph] = []
        if sentence is not None:
            self.latest_input = sentence
        parsed_string = self.tagger.parse(self.latest_input)
        words: list[str] = parsed_string.split('\n')
        words.remove('EOS')
        words.remove('')
        for w in words:
            result.append(self._extract(w))
        return result

    def _extract(self, parsed_word: str) -> Morph:
        if self.parse_type == 'ipadic':
            surface, others = parsed_word.split('\t')
            info = others.split(',')
            ret = Morph(surface,
                        info[0] if len(
                            info) > 0 and info[0] not in self._none_pattern else None,
                        info[1] if len(
                            info) > 1 and info[1] not in self._none_pattern else None,
                        info[2] if len(
                            info) > 2 and info[2] not in self._none_pattern else None,
                        info[3] if len(
                            info) > 3 and info[3] not in self._none_pattern else None,
                        info[4] if len(
                            info) > 4 and info[4] not in self._none_pattern else None,
                        info[5] if len(
                            info) > 5 and info[5] not in self._none_pattern else None,
                        info[6] if len(
                            info) > 6 and info[6] not in self._none_pattern else None,
                        info[7] if len(
                            info) > 7 and info[7] not in self._none_pattern else None,
                        None)
            return ret
        elif self.parse_type == 'neologd':
            raise NotImplementedError(
                "NEologd dictionary is not supported now. Please wait for version 2.0.0.")
        elif self.parse_type == 'unidic':
            raise NotImplementedError(
                "UniDic dictionary is not supported now. Please wait for version 2.0.0.")
        else:
            word, other = parsed_word.split()
            ret = Morph(word, None, None, None, None,
                        None, None, None, None, other)
            return ret

    def wakati_gaki(self, sentence: str):
        """文を分かち書きして、リストに格納します。

        Parameters
        ----------
        sentence : str
            分かち書きしたい文（一文）

        Returns
        -------
        list[str]
            分かち書きされた形態素のリスト
        """
        wakati_list = []
        for e in self.parse(sentence):
            wakati_list.append(e.word)
        return wakati_list
