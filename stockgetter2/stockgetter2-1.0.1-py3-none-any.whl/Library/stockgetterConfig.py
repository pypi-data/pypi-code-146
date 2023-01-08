from Scrapinger.Library.scrapingConfig import scrapingConfig

class stockgetterConfig(scrapingConfig):
    
    """
    stockgetter共通設定クラス(stockgetterConfig)
    """ 
    
    class settingValueStruct(scrapingConfig.settingValueStruct):

        """
        設定値構造体
        """ 

        class MailConfig(scrapingConfig.settingValueStruct.MailConfig):
            
            """
            MailConfig
            """
            
            mail_from = ''
            mail_to = ''
            
            def __init__(self):
                
                """
                コンストラクタ
                """
                
                super().__init__()
                
                self.mail_from = ''
                """ 送信元メールアドレス """
            
                self.mail_to = ''
                """ 送信先メールアドレス """

    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()

        self.stockgetterMailConfig = self.settingValueStruct.MailConfig()
        """ stockgetter Mail Config """

        self.stockgetterMailConfig.mail_from = ''
        """ stockgetter Mail Config - mail_from """

        self.stockgetterMailConfig.mail_to = ''
        """ stockgetter Mail Config - mail_to """
        
        self.processAbortFile = 'stopper.txt'
        """ process abort file """

        self.LimitsScrapingCount = 0
        """ Limits Scraping Count """

        self.jpxUrl = 'https://www.jpx.co.jp'
        """ 日本取引所グループ(JPX)サイトURL """
        
        self.jpxUrlMarkets = 'https://www.jpx.co.jp/markets/statistics-equities/misc/01.html'
        """ 日本取引所グループ(JPX)東証銘柄一覧ページURL """
        
        self.kabuDragonUrl = 'https://www.kabudragon.com/company/s={0}'
        """ 株ドラゴンサイトURL """

        self.downloadFolder = 'CodeList'
        """ 銘柄コードリスト格納ディレクトリ名 """
        
        self.getMstbrandFlg = 0
        """ 銘柄マスタ取得フラグ """

        self.closeFrom = 0
        """ 取引値下限値 """

        self.closeTo = 0
        """ 取引値上限値 """

        self.smaSpanShort = 5
        """ 短期SMA """
        
        self.smaSpanMidium = 25
        """ 中期SMA """
        
        self.smaSpanMidiumLong = 75
        """ 中長期SMA """

        self.emaSpanShort = 12
        """ 短期EMA """
        
        self.emaSpanLong = 26
        """ 長期SMA """
        
        self.macdSig = 9
        """ MACDシグナル """

        self.rsiSpan = 14
        """ RSI """

        self.rsiThresoldUnder = 20
        """ RSI閾値(下方) """

        self.rsiThresoldOver = 80
        """ RSI閾値(上方) """

        self.processAbortFile = 'stopper.txt'
        """ process abort file """

        self.LimitsScrapingCount = 0
        """ Limits Scraping Count """
    
        # 設定ファイル名追加
        self.setConfigFileName('stockgetter2.ini')
        
    def getConfig(self, _scriptFilePath: str, configFileDir: str = ''):
        
        """ 
        設定ファイルを読み込む 
        
        Parameters
        ----------
        _scriptFilePath : str
            スクリプトファイルパス
        configFileDir : str
            設定ファイルの格納場所となるディレクトリ
        """

        # 基底側のiniファイル読込
        super().getConfig(_scriptFilePath, configFileDir)
        
    def setInstanceMemberValues(self):
        
        """ 
        インスタンス変数に読み取った設定値をセットする
        """
        
        # 基底側実行
        super().setInstanceMemberValues()
        
        # 日本取引所グループ(JPX)サイトURL
        self.setConfigValue('jpxUrl',self.config_ini,'SITE','JPX_URL',str)
        
        # 日本取引所グループ(JPX)東証銘柄一覧ページURL
        self.setConfigValue('jpxUrlMarkets',self.config_ini,'SITE','JPX_URL_MARKETS',str)
        
        # 株ドラゴンサイトURL
        self.setConfigValue('kabuDragonUrl',self.config_ini,'SITE','KABU_DRAGON_URL',str)
        
        # 銘柄コードリスト格納ディレクトリ名
        self.setConfigValue('downloadFolder',self.config_ini,'DIR','DL_FOLDER',str)

        # stockgetter MailConfig - mail_from
        self.setConfigValue('stockgetterMailConfig.mail_from',self.config_ini,'MAIL_CONFIG','MAIL_FROM',str)

        # stockgetter MailConfig - mail_to
        self.setConfigValue('stockgetterMailConfig.mail_to',self.config_ini,'MAIL_CONFIG','MAIL_TO',str)

        # stockgetter Limits Scraping Count
        self.setConfigValue('LimitsScrapingCount',self.config_ini,'SITE','LIMITS_SCRAPING_COUNT_ONEDAY',int)

        # process abort file
        self.setConfigValue('processAbortFile',self.config_ini,'ABORT','PROCESS_ABORT_FILE',str)
        
        # mstbrand get flg
        self.setConfigValue('getMstbrandFlg',self.config_ini,'DEFAULT','GET_MSTBRAND_FLG',int)

        # 取引値From～To
        self.setConfigValue('closeFrom',self.config_ini,'TARGET_LIST_FILTER','CLOSE_FROM',int)
        self.setConfigValue('closeTo',self.config_ini,'TARGET_LIST_FILTER','CLOSE_TO',int)

        # SMAパラメーター
        self.setConfigValue('smaSpanShort',self.config_ini,'SMA_SPAN','SMA_SHORT',int)
        self.setConfigValue('smaSpanMidium',self.config_ini,'SMA_SPAN','SMA_MEDIUM',int)
        self.setConfigValue('smaSpanMidiumLong',self.config_ini,'SMA_SPAN','SMA_MEDIUM_LONG',int)
        
        # EMAパラメーター
        self.setConfigValue('emaSpanShort',self.config_ini,'EMA_SPAN','EMA_SHORT',int)
        self.setConfigValue('emaSpanLong',self.config_ini,'EMA_SPAN','EMA_LONG',int)
        self.setConfigValue('macdSig',self.config_ini,'EMA_SPAN','MACD_SIG',int)

        # RSIパラメーター
        self.setConfigValue('rsiSpan',self.config_ini,'RSI_SPAN','RSI',int)
        self.setConfigValue('rsiThresoldUnder',self.config_ini,'RSI_THRESOLD','RSI_THRESOLD_UNDER',int)
        self.setConfigValue('rsiThresoldOver',self.config_ini,'RSI_THRESOLD','RSI_THRESOLD_OVER',int)

        # Limits Scraping Count
        self.setConfigValue('LimitsScrapingCount',self.config_ini,'SITE','LIMITS_SCRAPING_COUNT_ONEDAY',int)

        # process abort file
        self.setConfigValue('processAbortFile',self.config_ini,'ABORT','PROCESS_ABORT_FILE',str)
