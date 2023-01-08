import os
import re
import pandas as pd
import requests
import xlrd
import urllib.request
import urllib.parse
import LibHanger.Library.uwLogger as Logger
from bs4 import BeautifulSoup
from LibHanger.Models.recset import recset
from stockgetter2.Getter.Base.baseGetter import baseGetter
from stockgetter2.Models.mstBrand import mstbrand
from stockgetter2.Library.stockgetterException import getterError
from stockgetter2.Library.stockgetterGlobals import *

class getter_mstbrand(baseGetter):
    
    """
    東証銘柄一覧リスト取得クラス
    (mstbrand)
    """
    
    def __init__(self) -> None:
        
        """
        コンストラクタ
        """
        
        super().__init__()

        # レコードセット初期化
        self.init_recset()

    def init_recset(self):
        
        """
        レコードセット初期化
        """
        
        # レコードセット初期化
        self.rsMstBrand = recset[mstbrand](mstbrand)
        
    def getData(self, *args, **kwargs):
        
        """
        レース結果取得
        
        Parameters
        ----------
        None
        """
        
        # レース結果をDataFrameで取得
        try:
            kwargs['getter'] = self
            result = self.getMstBrandToDataFrame(**kwargs)
        except:
            raise getterError
        return result
    
    @Logger.loggerDecorator("getMstBrandToDataFrame")
    def getMstBrandToDataFrame(self, *args, **kwargs):

        """
        レース結果取得
        
        Parameters
        ----------
        None
        """
        
        # pandasデータを返却する
        return self.downloadBrandCodeList()

    def downloadBrandCodeList(self):

        """
        Parameters
        ----------
        None
        """
        
        # ログ出力
        Logger.logging.info('>> Get BrandList Start')

        # 東証銘柄一覧Excelファイルのhrefをスクレイピングで特定
        response = requests.get(gv.stockgetterConfig.jpxUrlMarkets)
        bs = BeautifulSoup(response.content, 'lxml')
        href = bs.select_one("a[href*='xls']").get('href')

        # 東証銘柄一覧Excelファイルダウンロード
        csv_url = urllib.parse.urljoin(gv.stockgetterConfig.jpxUrl, href)
        fname = href.split('/')[-1]
        xls_path = os.path.join(gv.stockgetterConfig.downloadFolder, fname)
        if (not os.path.exists(xls_path)):
            os.mkdir(xls_path)
        urllib.request.urlretrieve(csv_url, xls_path)

        # ダウンロードしたExcelファイル取得
        wb = xlrd.open_workbook(xls_path)
        # 先頭シート取得
        sh = wb.sheet_by_index(0)

        # 株価の小数点以下表記を除去
        cr = re.compile(r'\.0$')
        codeListData = [
            [cr.sub('',str(v)) if isinstance(v, float) else str(v) for v in sh.row_values(r)]
            for r in range(sh.nrows)
        ]

        # 銘柄一覧リスト取得
        dfBrandCodeList = pd.DataFrame(codeListData[1:sh.nrows], columns = codeListData[0])

        # model用意
        rsMstBrand = recset[mstbrand](mstbrand)
        for index, item in dfBrandCodeList.iterrows():
            rsMstBrand.newRow()
            rsMstBrand.fields(mstbrand.brandcd.key).value = item['コード']
            rsMstBrand.fields(mstbrand.brandnm.key).value = item['銘柄名']
            rsMstBrand.fields(mstbrand.updymd.key).value = item['日付']
            rsMstBrand.fields(mstbrand.marketkbn.key).value = item['市場・商品区分']
            rsMstBrand.fields(mstbrand.indmajorcd.key).value = item['33業種コード']
            rsMstBrand.fields(mstbrand.indmajornm.key).value = item['33業種区分']
            rsMstBrand.fields(mstbrand.indmiddlecd.key).value = item['17業種コード']
            rsMstBrand.fields(mstbrand.indmiddlenm.key).value = item['17業種区分']
            rsMstBrand.fields(mstbrand.scalecd.key).value = item['規模コード']
            rsMstBrand.fields(mstbrand.scalenm.key).value = item['規模区分']
            rsMstBrand.fields(mstbrand.updinfo.key).value = self.getUpdInfo()
            
        # ログ出力
        Logger.logging.info('<< Get BrandList End')

        # レコードセットマージ
        self.rsMstBrand.merge(rsMstBrand)
        
        # 戻り値を返す
        return dfBrandCodeList
