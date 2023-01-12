from tomwer.core.futureobject import TomwerScanBase
from silx.utils.deprecation import deprecated


@deprecated(replacement="TomwerScanBase", since_version="1.0")
class FutureTomwerScan(TomwerScanBase):
    pass
