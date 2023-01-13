from Scrapinger.Library.scrapingerGlobals import scrapingerGlobal
from stockgetter2.Library.stockgetterConfig import stockgetterConfig

class stockgetterGlobal(scrapingerGlobal):
    
    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ呼び出し
        super().__init__()

        self.stockgetterConfig:stockgetterConfig = None
        """ stockgetter共通設定 """

# インスタンス生成(import時に実行される)
gv = stockgetterGlobal()
