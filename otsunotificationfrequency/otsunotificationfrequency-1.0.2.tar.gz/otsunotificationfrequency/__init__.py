"""for文などで一定の進捗度に達するたびに特殊な処理を挟むプログラムの補助を行うライブラリです。

`otsuvalidator`ライブラリを別途インストールしている場合に使えるvalidatorモジュールもあります。
使用したい場合にはotsunotificationfrequency.validatorをインポートしてください。
"""

__all__ = (
    "REGEX_NF_VALUE",
    "NotificationFrequency",
    "T",
)

from .cfg import REGEX_NF_VALUE, T
from .classes import NotificationFrequency
