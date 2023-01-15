from LibHanger.Library.DataAccess.uwPostgres import uwPostgreSQL
from stockgetter2.Register.Base.baseRegister import baseRegister

class register_StockData(baseRegister):
    
    """
    データ一括登録クラス
    """
    
    def __init__(self, __psgr:uwPostgreSQL):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__(__psgr)
    