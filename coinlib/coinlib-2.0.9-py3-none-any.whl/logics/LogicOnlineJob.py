import pandas as pd

from coinlib.logics import LogicOnlineWorker
from coinlib.logics.LogicBasicWorker import LogicBasicWorker
from coinlib.logics.LogicJob import LogicJob
import simplejson as json

from coinlib.logics.manager.LogicManager import LogicManager


class LogicOnlineJob(LogicJob):
    worker: LogicOnlineWorker
    #, name, group, inputs, df, indicator, worker
    def __init__(self, table, logicComponentInfo, logicElement, inputs, manager: LogicManager, worker: LogicBasicWorker):
        super(LogicOnlineJob, self).__init__(table, logicComponentInfo, logicElement, inputs, manager, worker)
        self.worker = worker
        self.result_col = None

        pass


    def notification(self, text, notificationModule, images=[], parameters={}, auth={}):
        super().notification(text, notificationModule, images=images, parameters=parameters, auth=auth)
        self.worker.runCommand("notification", "notification", {
                "text": text,
                "notification_module": notificationModule,
                "images": images,
                "parameters": parameters,
                "auth": auth
            })
        return True

    def date(self):
        current_date = pd.to_datetime('now').replace(second=0, microsecond=0)
        return current_date

    def time(self):
        current_date = pd.to_datetime('now').replace(second=0, microsecond=0)
        return current_date


    def notificationInteractive(self, callback, text,  buttons, notificationModule, images=[], parameters={}, auth={}):
        super().notificationInteractive(callback, text, buttons, notificationModule, images=images, parameters=parameters, auth=auth)
        self.worker.runCommandWithCallbackAsync("notification", "notificationInteractive", {
                "text": text,
                "notification_module": notificationModule,
                "images": images,
                "buttons": buttons,
                "parameters": parameters,
                "auth": auth
            }, callback)
        return True
