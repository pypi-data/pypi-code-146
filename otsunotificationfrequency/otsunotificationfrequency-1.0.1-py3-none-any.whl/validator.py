"""NotificationFrequency用のバリデータとコンバータが定義されたモジュールです。

`otsuvalidator`ライブラリをインストールしている人向けのモジュールです。
インストールされていない場合にはImportErrorが発生します。
"""

__all__ = (
    "CNotificationFrequency",
    "VNotificationFrequency",
)


try:
    from typing import Any

    from otsuvalidator.bases import Converter, Validator

    from .classes import NotificationFrequency

except ImportError:
    msg = 'このモジュールは"otsuvalidator"をインストールしている場合のみ使用できます。'
    raise ImportError(msg)


class VNotificationFrequency(Validator):
    """オブジェクトがNotificationFrequencyか確認するバリデータです。"""

    def __get__(self, instance, otype) -> NotificationFrequency:
        return super().__get__(instance, otype)

    def validate(self, value: Any) -> NotificationFrequency:
        if type(value) is not NotificationFrequency:
            msg = self.ERRMSG("NotificationFrequency型である必要があります", value)
            raise TypeError(msg)
        return value


class CNotificationFrequency(VNotificationFrequency, Converter):
    """VNotificationFrequencyの拡張バリデータです。

    NotificationFrequency型に変換可能なオブジェクトは例外を投げずに変換を試みます。
    """

    def validate(self, value: Any) -> NotificationFrequency:
        if type(value) is not NotificationFrequency:
            try:
                value = NotificationFrequency(value)
            except:
                msg = self.ERRMSG("NotificationFrequency型として扱える必要があります", value)
                raise TypeError(msg)
        return super().validate(value)

    def super_validate(self, value: Any) -> NotificationFrequency:
        return super().validate(value)
