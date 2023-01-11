import datetime
import queue
import time

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import inspect

from coinlib.broker.Broker import BrokerContractType, BrokerAssetType
from coinlib.broker.BrokerDTO import CoinlibBrokerAccount, CoinlibBrokerLoginParams, BrokerEvent, OrderUpdateInformation
from coinlib.brokerWorker.BrokerSession import BrokerSession, BrokerSessionListener
from coinlib.brokerWorker.TestProtocolResult import TestProtocolResult
from coinlib.data.DataTable import DataTable
import pandas as pd
import asyncio
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from coinlib.logics.broker.LogicBrokerInterface import LogicBrokerInterface
from coinlib.logics.manager.LogicManager import LogicManager
from coinlib.logics.onlineManager.LogicOnlineJobBroker import LogicOnlineJobBroker
from coinlib.statistics.StatisticMethodJob import StatisticMethodJob


class LogicTestBrokerWorker(WorkerJobProcess, BrokerSessionListener):
    portfolio: statsModel.BrokerPortfolio

    def __init__(self, workerJob, factory):
        self.appWorkerConfig = None
        self.waitingQueue = None
        self.brokerWorkerProcessInfo = None
        self.canceled = False
        self.command_running = False
        self.brokerWorkerRegistrationInfo = None
        super(LogicTestBrokerWorker, self).__init__(workerJob, factory)

    def initialize(self):
        self.registrar = Registrar()
        self.appWorkerInterface = stats.AppWorkerStub(self.getChannel())
        if self.appWorkerConfig is None:
            appWorkerConfigGlobal = self.appWorkerInterface.GetConfig(self.workerJob, metadata=self.registrar.getAuthMetadata())
            if appWorkerConfigGlobal.HasField("testConfig"):
                self.appWorkerConfig = appWorkerConfigGlobal.testConfig
            self.portfolio = self.appWorkerConfig.portfolio
            self.sessionId = self.appWorkerConfig.sessionId
            self.brokerAccount = self.appWorkerConfig.brokerAccount

        pass

    def onErrorHappened(self, message):

        indicatorError = statsModel.BrokerError()
        indicatorError.error.message = str(message)
        indicatorError.worker.CopyFrom(self.workerJob)

        self.appWorkerInterface.OnBrokerErrorOccured(indicatorError, metadata=self.registrar.getAuthMetadata())

    def setConfig(self, configuration):
        self.appWorkerConfig = configuration
        pass

    def onBrokerErrorHappenedInCommunication(self, error):
        pass

    def onBrokerCommandReceived(self, command):
        pass

    def testLogicBroker(self):

        print("BANAN")

        testprotocol = statsModel.BrokerTestProtocolData()
        testprotocol.worker.CopyFrom(self.workerJob)

        data = TestProtocolResult()

        logicConfig = statsModel.LogicRunnerLogic()


        try:
            manager = LogicManager("Test", logicConfig,  self.brokerAccount, self.portfolio)
            self.brokerInterface = LogicBrokerInterface(self.workerJob, self.sessionId, self.appWorkerInterface, self)
            logicBroker = LogicOnlineJobBroker(manager, self.brokerInterface)

            

            symbols = logicBroker.symbols()
            data.fetch_symbols = True

            data.appendLog("Fetched " + str(len(symbols)) + " Symbols from Broker")

            base = symbols[0]["base"]
            quote = symbols[0]["quote"]
            price = logicBroker.price(base, quote)
            data.appendLog("Fetched Price for: " + str(base) + "/" + quote + ": " + str(price) + quote)
            data.fetch_price_for_symbol = True

            data.no_trade_open = logicBroker.imIn() is False
            if data.no_trade_open == False:
                raise Exception("There is no open position currently - or should not be")

            data.appendLog("Fine you are currently not in")

            canLeverage = False
            if logicBroker.canLeverage():
                data.appendLog("Yes we can leverage")
                canLeverage = True
            else:
                data.appendLog("We can not test leverage")

            lastOrders = logicBroker.lastOrders(symbols[0]["symbol"])
            data.fetch_last_orders = True
            data.appendLog("Fetched last orders - found: "+str(len(lastOrders))+" Orders")

            ## lets search for USDT / USD or BUSD to anounce a good buy

            balance = manager.getAssets()
            usdt = manager.getAsset("USDT")
            usdt_money = manager.getMoney("USDT")

            trading_money = usdt_money
            if trading_money > 50:
                trading_money = 50

            data.appendLog("Found "+str(usdt_money)+" USDT in your account")
            data.money_available = True

            for s in symbols:
                if s["quote"] == "USDT":
                    selected_symboL = s
                    break

            symbol_price = logicBroker.price(selected_symboL["base"], selected_symboL["quote"])
            trading_money_quote = logicBroker.calculate_amount(trading_money, selected_symboL)

            data.appendLog("Selecting the Symbol: "+s["base"]+"/"+s["quote"])

            ## test making some orders

            ##########################################
            #####
            #####        Testing FUTURE Trading
            #####
            ##########################################

            if manager.isFuture():

                leverage=1
                if canLeverage:
                    leverage = 3

                # First Try: Buy with limit and test cancel

                try:

                    ## we buy a asset with a price which is very unrealistic to be sure
                    ## that it wont "fill" the order
                    order = logicBroker.long(s, trading_money_quote*2, leverage=3, price=symbol_price*0.5)
                    data.create_limit_order = True
                    data.appendLog("Buying Long worked with order id: "+str(order["clientOrderId"]))

                    # we check all open orders
                    openOrders = logicBroker.openOrders()
                    data.order_found_in_open_orders = False
                    for o in openOrders:
                        if o["clientOrderId"] == order["clientOrderId"]:
                            data.order_found_in_open_orders = True
                    data.appendLog("Found the order in the list of open orders")

                    ## we wait until the order is done - but it wont - thats why timeout happens
                    ## then we cancel the order directly
                    cancel_data = logicBroker.cancelOrder(order["clientOrderId"])
                    data.cancel_order = True


                    # we check all open orders
                    openOrders = logicBroker.openOrders()
                    data.order_after_cancel_removed = True
                    for o in openOrders:
                        if o["clientOrderId"] == order["clientOrderId"]:
                            data.order_after_cancel_removed = False
                            data.appendLog("The open orders does not refresh correctly")

                    data.appendLog("Canceling Order works fine!")

                    ## we check all closed orders

                except Exception as e:
                    data.appendLog("Long Buy does not work: "+str(e))
                    self.logger().error(e)

                ## Second Try: Buy with a market price

                try:

                    ## buy a logn with leverage

                    ## we buy a asset with a price which is very unrealistic to be sure
                    ## that it wont "fill" the order
                    order = logicBroker.long(s, trading_money_quote, leverage=2, group="basic")
                    data.create_order = True
                    data.appendLog("Buying Long worked with order id: "+str(order["clientOrderId"]))

                    ## wait: now the order should be filled within seconds

                    if logicBroker.imIn():
                        # should be true
                        data.im_in_check_works = True
                    else:
                        data.im_in_check_works = False

                    time_in = logicBroker.time_in()
                    if time_in is not None:
                        seconds_in = time_in["secondsIn"]
                        data.check_time_in = True
                        data.appendLog("No we are in since "+str(seconds_in)+" Seconds")
                    else:
                        data.check_time_in = False

                    pnl = logicBroker.profitFuture()
                    if pnl is not None:
                        profit = pnl["profitInPercentage"]
                        data.profit_future_works = True
                        data.appendLog("No we have a future profit of: "+str(profit)+" % because we started with entryPrice: "+str(pnl["priceIn"]))
                    else:
                        data.profit_future_works = False

                    pnl = logicBroker.profitSession()
                    if pnl is not None:
                        profit = pnl["profitInPercentage"]
                        data.profit_works = True
                        data.appendLog("No we have a session profit of: "+str(profit)+" % started session with: "+str(pnl["startMoney"]))
                    else:
                        data.profit_works = False

                    pnl = logicBroker.profitGroup("basic")
                    if pnl is not None:
                        profit = pnl["profitInPercentage"]
                        data.profit_group_works = True
                        data.appendLog("No we have a position profit of: "+str(profit)+" %")
                    else:
                        data.profit_group_works = False

                    ## check all open positions
                    data.position_in_position_list = False
                    positions = logicBroker.positions()
                    for o in positions:
                        if o["entryClientOrderId"] == order["clientOrderId"]:
                            data.position_in_position_list = True
                            data.appendLog("We found the list in open orders")

                    ## from here we check if we have the correct assets filled

                    ## close Position
                    logicBroker.closePosition(order["clientOrderId"], group="basic")
                    data.appendLog("Close the curernt position worked")

                    if logicBroker.imOut():
                        # should be true
                        data.im_out_check_works_after_out = True
                    else:
                        data.im_out_check_works_after_out = False


                except Exception as e:
                    data.appendLog("Long Buy does not work: "+str(e))
                    self.logger().error(e)


            ##########################################
            #####
            #####        Testing SPOT Trading
            #####
            ##########################################

            elif manager.isSpot():

                leverage = 1
                if canLeverage:
                    leverage = 3

                # First Try: Buy with limit and test cancel

                try:

                    ## we buy a asset with a price which is very unrealistic to be sure
                    ## that it wont "fill" the order
                    order = logicBroker.buy(s, trading_money_quote * 2, price=symbol_price * 0.5)
                    data.create_limit_order = True
                    data.appendLog("Buying worked with order id: " + str(order["clientOrderId"]))

                    # we check all open orders
                    openOrders = logicBroker.openOrders()
                    data.order_found_in_open_orders = False
                    for o in openOrders:
                        if o["clientOrderId"] == order["clientOrderId"]:
                            data.order_found_in_open_orders = True
                    data.appendLog("Found the order in the list of open orders")

                    ## we wait until the order is done - but it wont - thats why timeout happens
                    ## then we cancel the order directly
                    cancel_data = logicBroker.cancelOrder(order["clientOrderId"])
                    data.cancel_order = True

                    # we check all open orders
                    openOrders = logicBroker.openOrders()
                    data.order_after_cancel_removed = True
                    for o in openOrders:
                        if o["clientOrderId"] == order["clientOrderId"]:
                            data.order_after_cancel_removed = False
                            data.appendLog("The open orders does not refresh correctly")

                    data.appendLog("Canceling Order works fine!")

                    ## we check all closed orders

                except Exception as e:
                    data.appendLog("Buy does not work: " + str(e))
                    self.logger().error(e)

                ## Second Try: Buy with a market price

                try:

                    ## buy a logn with leverage
                    ## we buy a asset with a price which is very unrealistic to be sure
                    ## that it wont "fill" the order
                    order = logicBroker.buy(s, trading_money_quote, group="basic")
                    data.create_order = True
                    data.appendLog("Buying worked with order id: " + str(order["clientOrderId"]))

                    ## wait: now the order should be filled within seconds

                    time.sleep(10)

                    if logicBroker.imIn():
                        # should be true
                        data.im_in_check_works = True
                    else:
                        data.im_in_check_works = False

                    time_in = logicBroker.time_in()
                    if time_in is not None:
                        seconds_in = time_in["secondsIn"]
                        data.check_time_in = True
                        data.appendLog("No we are in since " + str(seconds_in) + " Seconds")
                    else:
                        data.check_time_in = False

                    pnl = logicBroker.profitSession()
                    if pnl is not None:
                        profit = pnl["profitInPercentage"]
                        data.profit_works = True
                        data.appendLog(
                            "No we have a session profit of: " + str(profit) + " % started session with: " + str(
                                pnl["startMoney"]))
                    else:
                        data.profit_works = False

                    pnl = logicBroker.profitGroup("basic")
                    if pnl is not None:
                        profit = pnl["profitInPercentage"]
                        data.profit_group_works = True
                        data.appendLog("No we have a position profit of: " + str(profit) + " %")
                    else:
                        data.profit_group_works = False

                    ## close Position
                    logicBroker.sell(s, trading_money_quote*0.98, group="basic")
                    data.appendLog("Sell the asset again")

                    if logicBroker.imOut():
                        # should be true
                        data.im_out_check_works_after_out = True
                    else:
                        data.im_out_check_works_after_out = False


                except Exception as e:
                    data.appendLog("Sell or Buy does not work: " + str(e))
                    self.logger().error(e)


            elif manager.isOption():
                pass





        except Exception as e:
            data.appendLog("ERROR: "+str(e))
            pass



        testprotocol.data = json.dumps(data, default=BrokerSession.serialize)

        self.appWorkerInterface.OnBrokerTestResult(testprotocol, metadata=self.registrar.getAuthMetadata())

        self.shutdown()

        return True

    def shutdown(self):
        self.canceled = True
        super().stop()
        super().closeChannel()

    def runProcess(self):
        try:
            self.run()

        except Exception as e:
            self.logger().error(e)
            self.onErrorProcess(e)
            return

        self.factory.onWorkerJobProcessFinished(self)
        self.logger().info("Finished")
        return True

    def run(self):

        self.testLogicBroker()



        return True
