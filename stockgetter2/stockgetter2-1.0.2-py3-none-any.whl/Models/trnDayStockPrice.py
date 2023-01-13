import LibHanger.Models.modelFields as fld
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import Null

# Baseクラス生成
Base = declarative_base()

class trnDayStockPrice(Base):

    """ 
    trndaystockpriceテーブルクラス 

    Parameters
    ----------
    Base : 
        Baseクラス
    """
    
    # テーブル名
    __tablename__ = 'trndaystockprice'

    # スキーマ
    __table_args__ = {'schema': 'stock'}

    # 列定義
    brandcd = fld.CharFields(5,primary_key=True,default='')
    stockymd = fld.DateTimeFields(primary_key=True,default=Null)
    open = fld.IntFields(default=0)
    high = fld.IntFields(default=0)
    low	= fld.IntFields(default=0)
    close = fld.IntFields(default=0)
    volume= fld.IntFields(default=0)
    smashort= fld.IntFields(default=0)
    smamidium= fld.IntFields(default=0)
    smamidiumlong= fld.IntFields(default=0)
    smalong	= fld.IntFields(default=0)
    emashort = fld.FloatFields(default=0)
    emalong = fld.FloatFields(default=0)
    macd = fld.FloatFields(default=0)
    macdsig = fld.FloatFields(default=0)
    rsi	= fld.NumericFields(5,2,default=0)
    macdsign = fld.CharFields(2,default='')
    rsisign = fld.CharFields(2,default='')
    updinfo	= fld.CharFields(40,default='')
