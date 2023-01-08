import re
import LibHanger.Library.uwGetter as CmnGetter
from LibHanger.Models.fields import *
from Scrapinger.Library.browserContainer import browserContainer
from Scrapinger.Library.webDriverController import webDriverController
from stockgetter2.Library.stockgetterGlobals import *

class stockgetterBrowserController(browserContainer):
    
    """
    stockgetterブラウザコントローラー
    """
    
    def __init__(self) -> None:
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()
        
        # WebDriverController
        self.wdc = webDriverController(gv.stockgetterConfig, self)
    
    def quitWebDriver(self):
        
        """
        webdriver破棄
        """
        
        # quit
        self.wdc.browserCtl.wDriver.quit()
        
        # print
        print('quit webdriver.')
    
    def getData(self, *args, **kwargs):
        
        """
        データ取得
        """
        
        pass
    
    def getUpdInfo(self):

        """
        更新情報取得
        """

        return CmnGetter.getNow().strftime('%Y/%m/%d %H:%M:%S')
    
    def isdigitEx(self, targetString:str) -> bool:
        
        """
        数値判定
        """
        
        return re.compile("^\d+\.?\d*\Z").match(targetString)
    