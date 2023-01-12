"""agent 基础操作"""

from vxsched import vxengine, vxIntervalTrigger
from vxutils import logger, vxtime
from vxquant.model.exchange import vxTrade
from vxutils import vxWrapper


@vxengine.event_handler("__init__")
def init_remote_event(gmcontext, _) -> None:
    if (not gmcontext.settings.publisher) or (not gmcontext.settings.subscriber):
        logger.info("未开启接送和发送远端消息事件模式...")
        return

    gmcontext.publisher = vxWrapper.init_by_config(gmcontext.settings.publisher)
    logger.info(f"设置publisher: {gmcontext.publisher}")
    gmcontext.subscriber = vxWrapper.init_by_config(gmcontext.settings.subscriber)
    logger.info(f"设置subscriber: {gmcontext.subscriber}")

    vxengine.submit_event(
        "fetch_remote_events",
        trigger=vxIntervalTrigger(1),
    )
    gmcontext.has_remote_event = True
    logger.info("开启接送和发送远端消息事件模式...")


@vxengine.event_handler("__init__")
def init_before_trade(gmcontext, event) -> None:
    if vxtime.today("09:15:00") < vxtime.now() < vxtime.today("15:00:00"):
        vxengine.submit_event("before_trade")
    logger.warning("当前为开盘时间，触发一次before_trade。")
    vxengine.trigger_events()


@vxengine.event_handler("on_broker_order_status")
def system_on_broker_order_status(gmcontext, event) -> None:
    if not gmcontext.has_remote_event:
        return
    broker_order = event.data
    remote_order = gmcontext.remote_orders.get(broker_order.exchange_order_id, None)
    if remote_order is None:
        logger.error(f"收到一个未知委托更新exchange_order_id : {broker_order.exchange_order_id}")
        return

    remote_order.filled_volume = broker_order.filled_volume
    remote_order.filled_amount = broker_order.filled_amount
    remote_order.status = broker_order.status
    remote_order.reject_code = broker_order.reject_code
    remote_order.reject_reason = broker_order.reject_reason

    gmcontext.publisher("on_order_status", remote_order)
    logger.info(f"[远程] 上报委托更新: {remote_order}")


@vxengine.event_handler("on_broker_execution_report")
def system_on_broker_execution_report(gmcontext, event) -> None:
    if not gmcontext.has_remote_event:
        return

    broker_trade = event.data
    remote_order = gmcontext.remote_orders.get(broker_trade.exchange_order_id, None)
    if remote_order is None:
        logger.error(f"收到一个未知委托更新exchange_order_id : {broker_trade.exchange_order_id}")
        return

    remote_trade = vxTrade(broker_trade.message)
    remote_trade.account_id = remote_order.account_id
    remote_trade.order_id = remote_order.order_id

    gmcontext.publisher("on_execution_report", remote_trade)
    logger.info(f"[远程] 上报成交回报: {remote_trade}")


@vxengine.event_handler("fetch_remote_events")
def system_fetch_remote_events(gmcontext, _) -> None:
    if (
        gmcontext.has_remote_event is False
        or gmcontext.last_subscriber_time + 1 > vxtime.now()
    ):
        return

    list(map(vxengine.submit_event, gmcontext.subscriber()))
    gmcontext.last_subscriber_time = vxtime.now()
    vxengine.trigger_events()


@vxengine.event_handler("remote_order_batch")
def system_remote_order_batch(gmcontext, event) -> None:
    remote_orders = event.data
    batch_orders = gmcontext.tdapi.order_batch(*remote_orders)
    for remote_order, batch_order in zip(remote_orders, batch_orders):
        remote_order.exchange_order_id = batch_order.exchange_order_id
        remote_order.status = batch_order.status
        gmcontext.remote_orders[remote_order.exchange_order_id] = remote_order


@vxengine.event_handler("remote_order_cancel")
def system_remote_order_cancel(gmcontext, event) -> None:
    remote_orders = event.data
    gmcontext.tdapi.order_cancel(*remote_orders)


@vxengine.event_handler("remote_sync")
def system_remote_sync(gmcontext, _) -> None:
    if not gmcontext.has_remote_event:
        return

    account = gmcontext.tdapi.get_account()
    orders = gmcontext.tdapi.get_orders()
    trades = gmcontext.tdapi.get_execution_reports()
    gmcontext.publisher(
        "reply_sync", {"account": account, "orders": orders, "trades": trades}
    )
