"""
There are actually three really good libraries which implements these tests:

| library     | category     | algorithm                                     | short | import script                                      | url |
|-------------|--------------|-----------------------------------------------|-------|----------------------------------------------------|-----|
| pmdarima    | Stationarity | Augmented Dickey-Fuller                       | ADF   | `from pmdarima.arima import ADFTest`               | https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.ADFTest.html#pmdarima.arima.ADFTest
|             | Stationarity | Kwiatkowski-Phillips-Schmidt-Shin             | KPSS  | `from pmdarima.arima import KPSSTest`              | https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.KPSSTest.html
|             | Stationarity | Phillips-Peron                                | PP    | `from pmdarima.arima import PPTest`                | https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.PPTest.html
|             | Seasonality  | Osborn-Chui-Smith-Birchenhall                 | OCSB  | `from pmdarima.arima import OCSBTest`              | https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.OCSBTest.html
|             | Seasonality  | Canova-Hansen                                 | CH    | `from pmdarima.arima import CHTest`                | https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.CHTest.html
|             | Correlation  | Auto-Correlation                              | ACF   | `from pmdarima.utils import ACFTest`               | https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.utils.acf.html#pmdarima.utils.acf
|             | Correlation  | Partial Auto-Ccorrelation                     | PACF  | `from pmdarima.utils import PACFTest`              | https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.utils.pacf.html
| statsmodels | Stationarity | Augmented Dickey-Fuller                       | ADF   | `from statsmodels.api import adfuller`             | https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html
|             | Stationarity | Kwiatkowski-Phillips-Schmidt-Shin             | KPSS  | `from statsmodels.api import kpss`                 | https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.kpss.html
|             | Unit-Root    | Zivot-Andrews structural-break unit-root test | KPSS  | `from statsmodels.api import zivot_andrews`        | https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.zivot_andrews.html
|             | Stationarity | Range unit-root test for stationarity         | RUR   | `from statsmodels.api import range_unit_root_test` | https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.range_unit_root_test.html
|             | White-Noise  | Ljung-Box Q Statistic                         | LB    | `from statsmodels.api import q_stat`               | https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.q_stat.html
|             | Correlation  | Auto-Correlation                              | ACF   | `from statsmodels.api import acf`                  | https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.acf.html
|             | Correlation  | Partial Auto-Ccorrelation                     | PACF  | `from statsmodels.api import pacf`                 | https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html
| arch        |

"""
# from pmdarima.arima.stationarity import PPTest, ADFTest, KPSSTest
# from statsmodels.tsa.api import adfuller, kpss
# """
# For a really good article on ADF & KPSS tests, check: [When A Time Series Only Quacks Like A Duck: Testing for Stationarity Before Running Forecast Models. With Python. And A Duckling Picture.](https://towardsdatascience.com/when-a-time-series-only-quacks-like-a-duck-10de9e165e)
# """
