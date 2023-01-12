class DRIVER:
    FREETDS = 'FreeTDS'
    ODBC_17 = 'ODBC+Driver+17+for+SQL+Server'
    NATIVE_11 = 'SQL+Server+Native+Client+11.0'


class Config:
    def __init__(self, host, user, password, db='univer', driver=DRIVER.FREETDS, *, pool_size=20, max_overflow=0):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.driver = driver
        self.pool_size = pool_size
        self.max_overflow = max_overflow
