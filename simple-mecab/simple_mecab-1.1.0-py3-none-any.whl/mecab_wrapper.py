import re
from typing import List, Literal

import MeCab

from simple_mecab.exceptions import InvalidArgumentError
from simple_mecab.morpheme import Morpheme


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

    - 同ライブラリの中の Morpheme dataclass を使用して結果を格納します。
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
        InvalidArgumentError
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
            raise InvalidArgumentError(
                "対応しない引数がargsに指定されました。\n"
                "MeCabWrapperのargsでは以下に示す引数を使用することはできません。\n"
                f"{banned_args}\n"
                "[ヒント] もし分かち書きをしたいのであれば、wakati_gaki関数を使用することができます。")

    def parse(self, sentence: str) -> List[Morpheme]:
        """日本語の文字列をMeCabで解析します。

        Parameters
        ----------
        sentence : str
            MeCabで解析したい1行の文章

        Returns
        -------
        list[Morpheme]
            形態素ごとにそれぞれ Morpheme クラスに情報が格納されています。
            （アクセス例：`mecab_agent.parse()[0].token`）
            詳細は Morpheme クラスの DocString を参照してください。
        """
        result: List[Morpheme] = []
        if sentence is not None:
            self.latest_input = sentence
        parsed_string = self.tagger.parse(self.latest_input)
        words: List[str] = parsed_string.split('\n')
        words.remove('EOS')
        words.remove('')
        for w in words:
            result.append(self._extract(w))
        return result

    def _extract(self, parsed_word: str) -> Morpheme:
        if self.parse_type == 'ipadic':
            surface, others = parsed_word.split('\t')
            info = others.split(',')
            ret = Morpheme(surface,
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
                "mecab-ipadic-NEologd辞書のパーサーは未実装です。")
        elif self.parse_type == 'unidic':
            raise NotImplementedError("UniDic辞書のパーサーは未実装です。")
        else:
            surface, feature = parsed_word.split()
            ret = Morpheme(surface, None, None, None, None,
                           None, None, None, None, feature)
            return ret

    def wakati_gaki(self, sentence: str) -> str:
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
        wakati_list: List[str] = []
        for e in self.parse(sentence):
            wakati_list.append(e.token)
        return ' '.join(wakati_list)
