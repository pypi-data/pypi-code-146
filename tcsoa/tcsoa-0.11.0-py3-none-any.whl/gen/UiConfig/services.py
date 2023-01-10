from tcsoa.gen.UiConfig._2014_11.services import UiConfigService as imp0
from tcsoa.gen.UiConfig._2015_10.services import UiConfigService as imp1
from tcsoa.base import TcService


class UiConfigService(TcService):
    getUIConfigs = imp0.getUIConfigs
    getUIConfigs2 = imp1.getUIConfigs2
    saveUiConfigs = imp0.saveUiConfigs
