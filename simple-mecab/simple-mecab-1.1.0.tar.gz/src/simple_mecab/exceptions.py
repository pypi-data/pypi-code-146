class InvalidArgumentError(Exception):
    """不正な引数

    このパッケージがサポートしていない引数がMeCabWrapper()のargsに指定された場合に発生します。
    対応しない引数を削除して再度お試しください。
    """
    pass
