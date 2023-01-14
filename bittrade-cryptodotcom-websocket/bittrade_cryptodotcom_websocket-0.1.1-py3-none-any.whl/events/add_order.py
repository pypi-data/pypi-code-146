import dataclasses
from decimal import Decimal
import functools
from logging import getLogger
from typing import Optional, Literal, Tuple

from reactivex import Observable, operators, throw
from reactivex.abc import ObserverBase, SchedulerBase
from reactivex.subject import BehaviorSubject
from reactivex.disposable import CompositeDisposable

from expression import curry_flip

from .methods import MethodName
from ..models import (
    EnhancedWebsocket,
    Order,
    OrderType,
    OrderSide,
    OrderStatus,
    CryptodotcomRequestMessage,
    CryptodotcomResponseMessage,
    # is_final_state,
)
from .ids import id_iterator
from ..connection.request_response import (
    wait_for_response,
    response_ok,
)

from ccxt import cryptocom, Exchange

logger = getLogger(__name__)


def exchange_to_order(
    x: CryptodotcomResponseMessage,
) -> RequiresContext[Exchange, ExchangeDependency]:
    return RequiresContext(lambda deps: deps.exchange.parse_orders(x.result["data"]))


def map_response_to_order():
    return operators.map(exchange_to_order)


@curry_flip(1)
def order_related_messages_only(
    source: Observable[dict | list], order_id: str
) -> Observable[dict[str, str]]:
    def subscribe(observer: ObserverBase, scheduler: Optional[SchedulerBase] = None):
        def on_next(message):
            try:
                is_valid = message[1] == "openOrders" and order_id in message[0][0]
            except:
                pass
            else:
                if is_valid:
                    observer.on_next(message[0][0][order_id])

        return source.subscribe(
            on_next=on_next,
            on_error=observer.on_error,
            on_completed=observer.on_completed,
            scheduler=scheduler,
        )

    return Observable(subscribe)


def update_order(existing: Order, message: dict) -> Order:
    updates = {
        "status": OrderStatus(message["status"]),
        "reference": message["userref"],
    }
    if "vol" in message:
        updates["volume"] = message["vol"]
    if "vol_exec" in message:
        updates["volume_executed"] = message["vol_exec"]
    if "open_tm" in message:
        updates["open_time"] = message["open_tm"]
    details = message.get("descr")
    if details and type(details) == dict:
        updates["price"] = message["descr"]["price"]
        updates["price2"] = message["descr"]["price2"]
    # Immutable version
    return dataclasses.replace(existing, **updates)


def create_order_lifecycle(x, messages) -> Observable[Order]:
    request, connection = x

    def subscribe(observer: ObserverBase, scheduler: Optional[SchedulerBase] = None):
        # To be on the safe side, we start recording messages at this stage; note that there is currently no sign of the websocket sending messages in the wrong order though
        recorded_messages = messages.pipe(operators.replay())

        def initial_order_received(order: Order):
            order_id = order.order_id
            observer.on_next(order)
            return recorded_messages.pipe(
                order_related_messages_only(order_id),
                operators.scan(update_order, order),
                operators.take_while(
                    lambda o: not is_final_state(o.status), inclusive=True
                ),
            )

        obs = messages.pipe(
            wait_for_response(request.reqid, 5.0),
            response_ok(),
            map_response_to_order(request),
            operators.flat_map(initial_order_received),
        )
        connection.send_json(dataclasses.asdict(request))  # type: ignore
        return CompositeDisposable(
            obs.subscribe(observer, scheduler=scheduler), recorded_messages.connect()
        )

    return Observable(subscribe)


def add_order_factory(
    exchange: Exchange,
    socket: BehaviorSubject[EnhancedWebsocket],
    messages: Observable[CryptodotcomResponseMessage],
):
    def add_order(
        symbol: str,
        type: Literal["limit", "market", "stop_loss", "stop_limit"],
        side: Literal["buy", "sell"],
        amount: Decimal,
        price=None,
        params=None,
    ) -> Observable[Order]:

        connection = socket.value
        uppercaseType = type.upper()
        instrument = exchange.market(symbol)
        request = {
            "instrument_name": instrument,
            "side": side.upper(),
            "type": uppercaseType,
            "quantity": exchange.amount_to_precision(symbol, amount),
        }
        if (uppercaseType == "LIMIT") or (uppercaseType == "STOP_LIMIT"):
            request["price"] = exchange.price_to_precision(symbol, price)
        postOnly = exchange.safe_value(params, "postOnly", False)
        if postOnly:
            request["exec_inst"] = "POST_ONLY"
            params = self.omit(params, ["postOnly"])
        request = CryptodotcomRequestMessage(method=MethodName.ADD_ORDER, params={})
        if not request.event:
            request.event = MethodName.ADD_ORDER
        if not request.reqid:
            request.reqid = next(id_iterator)

        return create_order_lifecycle((request, current_connection), messages)

    return add_order


__all__ = ["add_order_factory"]
