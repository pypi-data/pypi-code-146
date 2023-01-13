"""for文などで一定の進捗度に達するたびに特殊な処理を挟むプログラムの補助を行うクラスを纏めたモジュールです。
"""


__all__ = ("NotificationFrequency",)


from typing import Collection, Iterable, Iterator, Tuple, Union

from .cfg import REGEX_NF_VALUE, T


class NotificationFrequency:
    """イテラブルを処理する際、特定の頻度でのみ行いたい処理を行うタイミングを通知するクラスです。

    要素数の分かっているイテラブルやコレクションならばインスタンス生成後、"for_*"系メソッドを使用することでenumerate感覚で使用可能になります。
    "for_collection"はlen(obj)できるイテラブル用。
    "for_iterable"は要素数を把握しているイテラブル用になります。

    Properties:
        length (int): 管理するイテラブルの要素数。

    """

    def __init__(self, nf_value: Union[int, str, "NotificationFrequency"]) -> None:
        """進捗管理インスタンスを生成します。

        整数または整数のみで構成された文字列を与えた場合はその要素数毎にタイミングを通知します。
        整数のみの文字列の末尾に"%"を付けると進捗率がn%進む度にタイミングを通知します。

        Args:
            nf_value (Union[int, str, "NotificationFrequency"]): 処理を挟む頻度。

        Raises:
            ValueError: nf_valueが不正な値の場合に投げられます。
        """
        self.__use_percentage = False
        self.__length = -1
        self.__before = 0
        if isinstance(nf_value, NotificationFrequency):
            nf_value = str(nf_value)
        ng = False
        if type(nf_value) is str:
            find = REGEX_NF_VALUE.search(nf_value)
            if find is not None:
                v, p = find.groups()
                v = int(v)
                if p is not None:
                    if v <= 100:
                        self.__use_percentage = True
                    else:
                        ng = True
                self.__frequency = v
            else:
                ng = True
        elif type(nf_value) is int:
            self.__frequency = nf_value
        else:
            ng = True
        if ng or self.__frequency <= 0:
            msg = f'"{nf_value}"は使用できない値です。'
            raise ValueError(msg)

    def __call__(self, idx: int) -> Tuple[bool, int]:
        return self.check_and_get_percentage(idx)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, NotificationFrequency):
            return str(self) == str(__o)
        return False

    def __str__(self) -> str:
        res = [str(self.__frequency)]
        if self.__use_percentage:
            res.append("%")
        return "".join(res)

    def check_and_get_percentage(self, idx: int) -> Tuple[bool, int]:
        """idx番目の要素が特殊処理を挟むタイミングかを判定し、進捗率と共に返します。

        `nf.check_and_get_percentage(idx)`と`nf(idx)`は等価になります。

        Args:
            idx (int): 現在の進捗。

        Raises:
            AttributeError: 管理するイテラブルの要素数が設定されていない場合に投げられます。

        Returns:
            Tuple[bool, int]: (タイミングか, 進捗率)のタプル。
        """
        if self.length == -1:
            msg = "このインスタンスで進捗管理するイテラブルの要素数を与えてください。"
            raise AttributeError(msg)
        percentage = idx * 100 // self.length
        ok = False
        if percentage == 100:
            self.__before = percentage
            ok = True
        elif self.__use_percentage:
            if percentage - self.__before >= self.__frequency:
                self.__before = percentage
                ok = True
        elif idx - self.__before >= self.__frequency:
            self.__before = idx
            ok = True
        return ok, percentage

    def for_collection(self, it: Collection[T]) -> Iterator[Tuple[bool, int, int, T]]:
        """(タイミングか, インデックス, 進捗率, コレクションの要素)のタプルを順次返すイテレータを生成します。

        インデックスは1からカウントされます。

        Args:
            it (Collection[T]): 進捗管理したいコレクション。

        Yields:
            Iterator[Tuple[bool, int, int, T]]: (タイミングか, インデックス, 進捗率, コレクションの要素)のタプル。
        """
        yield from self.for_iterable(it, len(it))

    def for_iterable(self, it: Iterable[T], length: int) -> Iterator[Tuple[bool, int, int, T]]:
        """(タイミングか, インデックス, 進捗率, コレクションの要素)のタプルを順次返すイテレータを生成します。

        インデックスは1からカウントされます。

        Args:
            it (Iterable[T]): 進捗管理したいイテラブル。
            length (int): イテラブルの要素数。

        Yields:
            Iterator[Tuple[bool, int, int, T]]: (タイミングか, インデックス, 進捗率, コレクションの要素)のタプル。
        """
        nf = NotificationFrequency(self)
        nf.set_length(length)
        for i, v in enumerate(it, 1):
            alert, per = nf(i)
            yield (alert, i, per, v)

    def set_length(self, length: int) -> None:
        """管理するイテラブルの要素数を設定し、進捗を初期化します。

        Args:
            length (int): 要素数。
        """
        self.__length = length
        self.__before = 0

    @property
    def length(self) -> int:
        """管理するイテラブルの要素数。"""
        return self.__length
