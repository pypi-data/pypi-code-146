"""基于mongodb的多账户管理"""

import polars as pl
import uuid
from vxquant.model.contants import OrderDirection, OrderOffset, OrderType, OrderStatus
from vxquant.model.exchange import (
    vxAccountInfo,
    vxOrder,
    vxTrade,
    vxCashPosition,
    vxPosition,
)
from vxutils import logger, vxtime


class AccountManager:
    def __init__(self, db, publisher, hqfetcher):
        self._db = db
        self._publisher = publisher
        self._hqfetcher = hqfetcher

    def create_account(
        self,
        account_id=None,
        portfolio_id=None,
        balance=1000000.00,
        channel_name="simtrade",
        on_error="skip",
    ) -> vxAccountInfo:
        account = self._db.accounts.find_one({"account_id": account_id})
        if account and on_error == "skip":
            logger.warning(f"账号: {account_id} 已存在，无需创建。 ")
            return account

        if account:
            logger.warning(f"账号{account_id}已存在，删除原来账号各类信息.")
            self._db.accounts.delete_many({"account_id": account_id})
            self._db.positions.delete_many({"account_id": account_id})
            self._db.orders.delete_many({"account_id": account_id})
            self._db.trades.delete_many({"account_id": account_id})

        account_id = account_id or str(uuid.uuid4())
        portfolio_id = portfolio_id or str(uuid.uuid4())
        account_info = vxAccountInfo(
            account_id=account_id,
            portfolio_id=portfolio_id,
            deposit=balance,
            balance=balance,
            marketvalue=0,
            fund_shares=balance,
            fund_nav_yd=1.0,
            settle_day=vxtime.today("00:00:00") - 60 * 60 * 24,
            channel=channel_name,
        )

        cash_position = vxCashPosition(
            portfolio_id=portfolio_id,
            account_id=account_id,
            volume_today=balance,
        )
        with self._db.start_session() as session:
            self._db.accounts.insert_one(account_info.message, session=session)
            self._db.positions.insert_one(cash_position.message, session=session)
        return account_info

    def get_account(self, account_id):
        item = self._db.accounts.find_one({"account_id": account_id}, {"_id": 0})
        return vxAccountInfo(dict(item))

    def get_orders(self, account_id, order_id=None, unfinished=False, df=False):
        query = {"account_id": account_id}
        if order_id:
            query["order_id"] = order_id

        if unfinished:
            query["status"] = {"$in": ["PendingNew", "New", "PartiallyFilled"]}

        cur = self._db.orders.find(query, {"_id": 0})

        return (
            pl.DataFrame([dict(item) for item in cur])
            if df
            else {item["order_id"]: vxOrder(item) for item in cur}
        )

    def get_execution_reports(self, account_id, order_id=None, df=False):
        query = {"account_id": account_id}
        if order_id:
            query["order_id"] = order_id

        cur = self._db.trades.find(query, {"_id": 0})
        return (
            pl.DataFrame([dict(item) for item in cur])
            if df
            else {item["trade_id"]: vxTrade(item) for item in cur}
        )

    def get_positions(self, account_id, symbol=None, df=False):
        query = {"account_id": account_id}
        if symbol:
            query["symbol"] = symbol

        cur = self._db.positions.find(query, {"_id": 0})
        return (
            pl.DataFrame([dict(item) for item in cur])
            if df
            else {
                item["symbol"]: vxPosition(item)
                if item["symbol"] != "CNY"
                else vxCashPosition(item)
                for item in cur
            }
        )

    def _frozen_position(self, account_id, symbol, volume, session) -> bool:
        """冻结仓位"""

        ret_cur = self._db.positions.update_one(
            {
                "account_id": account_id,
                "symbol": symbol,
                "available": {"$gte": volume},
            },
            {"$inc": {"frozen": volume, "available": -volume}},
            session=session,
        )
        if ret_cur.matched_count == 0:
            raise ValueError(f"账户({account_id}) 冻结{symbol}仓位 :{volume} 失败。")

        if symbol == "CNY":
            self._db.accounts.update_one(
                {
                    "account_id": account_id,
                },
                {"$inc": {"frozen": volume, "available": -volume}},
                session=session,
            )
        return True

    def _release_positon(self, account_id, symbol, volume, session) -> bool:
        ret_cur = self._db.positions.update_one(
            {"account_id": account_id, "symbol": symbol, "frozen": {"$get": volume}},
            {"$inc": {"frozen": -volume, "available": volume}},
            session=session,
        )
        if ret_cur.matched_count == 0:
            raise ValueError(f"账号({account_id}) 解冻{symbol}仓位 {volume} 失败.")
        if symbol == "CNY":
            self._db.accounts.update_one(
                {
                    "account_id": account_id,
                },
                {"$inc": {"frozen": -volume, "available": volume}},
                session=session,
            )
        return True

    def update_account_info(self, account_id):
        self._db.positions

    def order_batch(self, account_id, orders):
        submit_orders = []
        with self._db.start_session() as session:
            for order in orders:
                if not isinstance(order, vxOrder):
                    logger.warning(f"order 类型不正确 : {type(order)}")
                    continue
                order.account_id = account_id
                if order.order_direction == OrderDirection.Buy:
                    frozen_volume = order.volume * order.price * 1.003
                    frozen_symbol = "CNY"
                else:
                    frozen_volume = order.volume
                    frozen_symbol = order.symbol

                try:
                    self._frozen_position(
                        account_id=account_id,
                        symbol=frozen_symbol,
                        volume=frozen_volume,
                        session=session,
                    )
                    self._db.orders.insert_one(order.message)
                    submit_orders.append(order)
                except ValueError as e:
                    logger.error(e)

        item = self._db.accounts.find_one(
            {"account_id": account_id}, {"account_id": 1, "channel": 1}
        )
        channel = item["channel"]
        self._publisher("submit_order_batch", submit_orders, channel=channel)
        return submit_orders

    def order_volume(self, account_id, symbol, volume, price: float = 0.0) -> vxOrder:
        if volume == 0:
            raise ValueError(f"volume 不能为 {volume}")

        if price <= 0.0:
            tick = self._hqfetcher(symbol)[symbol]

        order = vxOrder(
            account_id=account_id,
            symbol=symbol,
            order_direction=OrderDirection.Buy if volume > 0 else OrderDirection.Sell,
            order_offset=OrderOffset.Open if volume > 0 else OrderOffset.Close,
            order_type=OrderType.Limit if price > 0 else OrderType.Market,
            volume=abs(int(volume)),
            price=price or tick.lasttrade,
            status=OrderStatus.PendingNew,
        )
        return self.order_batch(account_id=account_id, orders=[order])


if __name__ == "__main__":
    from vxutils.database.mongodb import vxMongoDB
    from vxquant.mdapi.hq.tdx import TdxAPIPool

    db = vxMongoDB("mongodb://uat:uat@127.0.0.1:27017/uat", "uat")
    manager = AccountManager(db, None, TdxAPIPool())
    # acc = manager.create_account("test", balance=10000000.00, on_error="replace")
    # print(acc)
    print(manager.get_account("test"))
    print(manager.get_positions("test"))
    # order = manager.order_volume("test", "SHSE.600000", 10000, 11.00)
    print(manager.get_orders("test"))
