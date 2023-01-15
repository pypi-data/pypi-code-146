import LibHanger.Library.uwLogger as Logger
from LibHanger.Library.uwGlobals import configer
from LibHanger.Library.uwGlobals import *
from stockgetter2.Library.stockgetterGlobals import *

class stockgetterConfiger(configer):
    
    """
    stockgetter2共通設定クラス
    """
    
    def __init__(self, _tgv:stockgetterGlobal, _file, _configFolderName):
        
        """
        コンストラクタ
        """
        
        # stockgetter2.ini
        da = stockgetterConfig()
        da.getConfig(_file, _configFolderName)

        # gvセット
        _tgv.stockgetterConfig = da
        
        # ロガー設定
        Logger.setting(da)
