"""よく使うクラスを纏めたモジュールです。
"""

__all__ = (
    "ObjectSaver",
    "OtsuNone",
    "Timer",
)


import base64
import pickle
import time

from datetime import datetime, timedelta
from typing import Any, Iterator

from .funcs import setup_path
from .types import hmsValue, pathLike


class ObjectSaver:
    """オブジェクトを保存するファイルを扱うクラスです。

    Properties:
        obj (Any): ファイルに保存されているオブジェクト。
    """

    def __init__(self, file: pathLike) -> None:
        self.__file = setup_path(file)
        if self.__file.exists():
            obj = self.load_file()
        else:
            obj = None
        self.__obj = obj

    @staticmethod
    def dumps(obj: Any) -> str:
        """オブジェクトのpickle文字列を返します。

        Args:
            obj (Any): pickle文字列を取得したいオブジェクト。

        Returns:
            str: pickle文字列。
        """
        otb = pickle.dumps(obj, protocol=4)
        return base64.b64encode(otb).decode("utf-8")

    @staticmethod
    def loads(pickle_str: str) -> Any:
        """pickle文字列をオブジェクト化します。

        Args:
            pickle_str (str): pickle文字列。

        Returns:
            Any: 復元されたオブジェクト。
        """
        stb = base64.b64decode(pickle_str.encode())
        return pickle.loads(stb)

    def load_file(self) -> Any:
        """ファイルに保存されているデータを読み込み、取得します。

        ファイルが存在しなかった場合にはNoneを保存したファイルを生成し、Noneを返します。

        Returns:
            Any: ファイルに保存されていたオブジェクト。
        """
        file = self.__file
        if file.exists():
            with file.open("r", encoding="utf-8") as f:
                return self.loads(f.read())
        else:
            self.save_file(None)
        return None

    def save_file(self, obj: Any) -> bool:
        """ファイルにobjを保存し、成否を返します。

        また、obj属性を更新します。

        Args:
            obj (Any): 保存したいオブジェクト。

        Returns:
            bool: 保存の成否。
        """
        try:
            bts = self.dumps(obj)
            with self.__file.open("w", encoding="utf-8") as f:
                f.write(bts)
            self.__obj = obj
            return True
        except:
            return False

    @property
    def obj(self) -> Any:
        """ファイルに保存されているオブジェクト。

        新規ファイルでインスタンス生成した場合の初期値はNoneになります。
        """
        return self.__obj


class __OtsuNoneType:
    """Noneが返るのが正常な場合など、異常なNoneを表す場合に使用するクラスです。"""

    __instance = None

    def __new__(cls) -> "__OtsuNoneType":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __repr__(self) -> str:
        return "OtsuNone"

    def __bool__(self) -> bool:
        return False


class Timer:
    """指定時間が経過したかを判定したり指定時間秒処理を停止させるタイマーのクラスです。

    Properties:
        delta (timedelta): インスタンスの基準待機時間です。
        start_time (datetime): タイマーを開始した時刻です。
        target_time (datetime): タイマーを終了する時刻です。
    """

    def __init__(self, hours: int = 0, minutes: int = 0, seconds: float = 0) -> None:
        """h時間m分s秒を測るタイマーインスタンスを生成します。

        Args:
            hours (int, optional): h時間 Defaults to 0.
            minutes (int, optional): m分。 Defaults to 0.
            seconds (float, optional): s秒。 Defaults to 0.

        Raises:
            ValueError: マイナス秒になるような時間が指定されている場合に投げられます。
        """
        delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        if delta < timedelta(seconds=0):
            msg = f"0秒未満のTimerインスタンスを生成することはできません。 ({delta.total_seconds():0.2f}秒)"
            raise ValueError(msg)
        self.__delta = delta
        self.reset()

    def __bool__(self) -> bool:
        return self.target_time > datetime.now()

    def __str__(self) -> str:
        hms = self.calc_hms(self.delta.total_seconds())
        res = []
        for i, s in zip(hms, ("時間", "分", "秒")):
            if i > 0:
                res.append(f"{i}{s}")
        return "".join(res) + "のタイマーです。"

    @staticmethod
    def calc_hms(seconds: float) -> hmsValue:
        """秒数から時分秒のタプルを返します。

        Args:
            seconds (float): 秒数。

        Returns:
            hmsValue: 時分秒のタプル。
        """
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h, m = map(int, (h, m))
        return (h, m, s)

    def begin(self, span_seconds: float = 0) -> None:
        """現在から指定時間秒待機します。

        Args:
            span_seconds (float, optional): 待機終了を確認する頻度秒。 Defaults to 0.
        """
        self.reset()
        self.join(span_seconds)

    def join(self, span_seconds: float = 0) -> None:
        """開始時刻から指定時間秒経過するまで待機します。

        Timer.beginと違い、インスタンス生成やTimer.resetからの経過時間に応じて待機時間が減少します。

        Args:
            span_seconds (float, optional): 待機終了を確認する頻度秒。 Defaults to 0.
        """
        span = min(0, span_seconds)
        while self:
            time.sleep(span)

    def reset(self) -> None:
        """タイマーの開始時刻をリセットし、終了時刻を更新します。"""
        self.__start_time = datetime.now()
        self.__target_time = self.start_time + self.delta

    def wiggle_begin(self) -> Iterator[hmsValue]:
        """待機時間を確認後に処理を挟むことのできるTimer.beginです。

        for文などと合わせて使うことができます。

        Yields:
            Iterator[hmsValue]: 指定時刻までの残り時分秒のタプル。
        """
        self.reset()
        yield from self.wiggle_join()

    def wiggle_join(self) -> Iterator[hmsValue]:
        """待機時間を確認後に処理を挟むことのできるTimer.joinです。

        for文などと合わせて使うことができます。

        Yields:
            Iterator[hmsValue]: 指定時刻までの残り時分秒のタプル。
        """
        while self:
            delta = self.target_time - datetime.now()
            yield self.calc_hms(delta.total_seconds())

    @property
    def delta(self) -> timedelta:
        """インスタンスの基準待機時間です。"""
        return self.__delta

    @property
    def start_time(self) -> datetime:
        """タイマーを開始した時刻です。

        この時刻を基準にdelta秒経過したかを判定します。
        インスタンス生成時、またはTimer.begin, Timer.resetメソッドを呼び出した場合にこの属性が更新されます。
        """
        return self.__start_time

    @property
    def target_time(self) -> datetime:
        """タイマーを終了する時刻です。

        インスタンス生成時、またはTimer.begin, Timer.resetメソッドを呼び出した場合にこの属性が更新されます。
        """
        return self.__target_time


OtsuNone = __OtsuNoneType()
