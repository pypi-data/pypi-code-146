import enum


class MethodName(str, enum.Enum):
    AUTHENTICATE = "public/auth"
    ADD_ORDER = "private/create-order"
    CANCEL_ORDER = "private/cancel-order-list"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    GET_OPEN_ORDERS = "private/get-open-orders"
    USER_BALANCE = "private/user-balance"


__all__ = [
    "MethodName",
]
