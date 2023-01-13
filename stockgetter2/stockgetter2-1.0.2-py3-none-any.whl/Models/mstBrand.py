import LibHanger.Models.modelFields as fld
from sqlalchemy.ext.declarative import declarative_base

# Baseクラス生成
Base = declarative_base()

class mstbrand(Base):

	"""
	mstbrandテーブルクラス
	
	Parameters
    ----------
    Base : 
        Baseクラス
	"""
    
	# テーブル名
	__tablename__ = 'mstbrand'
	
	# スキーマ
	__table_args__ = {'schema': 'stock'}
	
	# 列定義
	brandcd = fld.CharFields(5,primary_key=True,default='')
	brandnm = fld.CharFields(250,default='')
	updymd = fld.CharFields(8,default='')
	marketkbn = fld.CharFields(50,default='')
	indmajorcd = fld.CharFields(5,default='')
	indmajornm = fld.CharFields(30,default='')
	indmiddlecd = fld.CharFields(3,default='')
	indmiddlenm = fld.CharFields(30,default='')
	scalecd = fld.CharFields(3,default='')
	scalenm = fld.CharFields(30,default='')
	updinfo = fld.CharFields(40,default='')

