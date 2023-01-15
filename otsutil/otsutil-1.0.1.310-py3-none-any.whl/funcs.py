"""よく使う関数を纏めたモジュールです。
"""

__all__ = (
    "deduplicate",
    "load_json",
    "read_lines",
    "save_json",
    "setup_path",
    "str_to_path",
    "write_lines",
)


import json

from collections import deque
from pathlib import Path
from typing import Iterable, Iterator, Sequence, overload

from .types import T, pathLike


@overload
def deduplicate(values: deque[T]) -> deque[T]:
    """デックから重複を取り除きます。

    この関数はset(values)で順番を破壊したくない場合などに使用します。

    Args:
        values (deque[T]): 重複を取り除きたいデック。

    Returns:
        deque[T]: 重複を除去したデック。
    """
    ...


@overload
def deduplicate(values: list[T]) -> list[T]:
    """リストから重複を取り除きます。

    この関数はset(values)で順番を破壊したくない場合などに使用します。

    Args:
        values (list[T, ...]): 重複を取り除きたいリスト。

    Returns:
        list[T, ...]: 重複を除去したリスト。
    """
    ...


@overload
def deduplicate(values: tuple[T]) -> tuple[T]:
    """tupleから重複を取り除きます。

    この関数はset(values)で順番を破壊したくない場合などに使用します。

    Args:
        values (tuple[T]): 重複を取り除きたいtuple。

    Returns:
        tuple[T]: 重複を除去したtuple。
    """
    ...


@overload
def deduplicate(values: tuple[T, ...]) -> tuple[T, ...]:
    """タプルから重複を取り除きます。

    この関数はset(values)で順番を破壊したくない場合などに使用します。

    Args:
        values (tuple[T, ...]): 重複を取り除きたいタプル。

    Returns:
        tuple[T, ...]: 重複を除去したタプル。
    """
    ...


def deduplicate(values: Sequence[T]) -> Sequence[T]:
    """シーケンスから重複を取り除きます。

    この関数はset(values)で順番を破壊したくない場合などに使用します。
    また、シーケンスがデック, リスト, タプルのいずれかの場合はシーケンスの型も保持します。
    それ以外の場合はlist[T]になります。

    Args:
        values (Sequence[T]): 重複を取り除きたいシーケンス。

    Returns:
        Sequence[T]: 重複を除去したシーケンス。
    """
    res = sorted(set(values), key=values.index)
    if type(values) is tuple:
        res = tuple(res)
    elif type(values) is deque:
        res = deque(res)
    return res


def load_json(file: pathLike, encoding: str = "utf-8", **kwargs) -> dict | list:
    """json形式のファイルを読み込み、jsonデータを返します。

    キーワード引数にはjson.loadで使用できる引数を与えることができます。

    Args:
        file (Path): json形式のファイル。
        encoding (str, optional): ファイルのエンコード。指定しない場合utf-8で扱います。

    Raises:
        FileNotFoundError: ファイルが存在しないかフォルダの場合に投げられます。

    Returns:
        dict | list: jsonデータ。
    """
    file = str_to_path(file)
    if not file.is_file():
        msg = f"{file}は存在しないかファイルではありません。"
        raise FileNotFoundError(msg)
    with file.open("r", encoding=encoding) as f:
        kwargs["fp"] = f
        return json.load(**kwargs)


def read_lines(file: pathLike, ignore_blank_line: bool = False, encoding: str = "utf-8", **kwargs) -> Iterator[str]:
    """ファイルを読み込み、1行ずつ返すイテレータを生成します。

    行右端の改行を自動で除去します。

    キーワード引数にはopenで使用できる引数を与えることができますが、modeはrで固定されます。

    Args:
        file (pathLike): 読み込むファイル。
        ignore_blank_line (bool, optional): line.strip()したときに空文字になる行を無視します。 Defaults to False.
        encoding (str, optional): 読み込むファイルのエンコード。 Defaults to "utf-8".

    Raises:
        FileNotFoundError: ファイルが存在しないかフォルダの場合に投げられます。

    Yields:
        Iterator[str]: ファイルの各行を返すイテレータ。
    """
    file = str_to_path(file)
    if not file.is_file():
        msg = f"{file}は存在しないかファイルではありません。"
        raise FileNotFoundError(msg)
    kwargs["encoding"] = encoding
    if "file" in kwargs:
        del kwargs["file"]
    kwargs["mode"] = "r"
    with file.open(**kwargs) as f:
        gen = map(lambda x: x.rstrip("\n"), f)
        if ignore_blank_line:
            gen = filter(lambda x: x.strip(), gen)
        for line in gen:
            yield line


def save_json(
    file: pathLike,
    data: dict | list,
    encoding: str = "utf-8",
    ensure_ascii: bool = False,
    indent: int | str | None = 4,
    sort_keys: bool = True,
    **kwargs,
) -> None:
    """指定したファイルにデータをjson形式で書き出します。

    キーワード引数にはjson.dumpで使用できる引数を与えることができます。

    Args:
        file (pathLike): 出力先ファイル。
        data (dict | list): 出力するデータ。
        encoding (str, optional): 出力するファイルのエンコード。 Defaults to "utf-8".
        ensure_ascii (bool, optional): json.dumpsのensure_ascii引数。 Defaults to False.
        indent (int | str | None, optional): json.dumpsのindent引数 Defaults to 4.
        sort_keys (bool, optional): json.dumpsのsort_keys引数 Defaults to True.
    """
    file = setup_path(file)
    with file.open("w", encoding=encoding) as f:
        kwargs["fp"] = f
        kwargs["obj"] = data
        kwargs["ensure_ascii"] = ensure_ascii
        kwargs["indent"] = indent
        kwargs["sort_keys"] = sort_keys
        json.dump(**kwargs)


def setup_path(path: pathLike, is_dir: bool = False) -> Path:
    """親ディレクトリの存在を確認、生成、保証しパスを返します。

    is_dirがTrueの場合にはpathを生成します。

    Args:
        path (Union[str, Path]): 使用したいパス。
        is_dir (bool, optional): パスがディレクトリかどうか。

    Returns:
        Path: 使用可能なパス。
    """
    path = str_to_path(path)
    if is_dir:
        p = path
    else:
        p = path.parent
    if not p.exists():
        p.mkdir(parents=True)
    return path


def str_to_path(path: pathLike) -> Path:
    """文字列をパスに変換します。

    Args:
        path (pathLike): パスにしたい文字列。またはパス。

    Returns:
        Path: パス。
    """
    if isinstance(path, Path):
        return path
    return Path(path)


def write_lines(file: pathLike, lines: Iterable, add_blank_line: bool = False, encoding: str = "utf-8", **kwargs) -> None:
    """ファイルにlinesを1行ずつ書き出します。

    キーワード引数にはPath().openで使用できる引数を与えることができます。

    Args:
        file (pathLike): 出力先ファイル。
        lines (Iterable): 出力する行データ。
        add_blank_line (bool, optional): ファイル末尾が空白行になるようにするか。 Defaults to False.
        encoding (str, optional): 出力するファイルのエンコード。 Defaults to "utf-8".
    """
    file = setup_path(file)
    kwargs["encoding"] = encoding
    kwargs["mode"] = "w"
    if "file" in kwargs:
        del kwargs["file"]
    with file.open(**kwargs) as f:
        last_line = ""
        for i, line in enumerate(map(str, lines)):
            last_line = line
            if i:
                line = f"\n{line}"
            f.write(line)
        if add_blank_line and last_line.strip():
            f.write("\n")
