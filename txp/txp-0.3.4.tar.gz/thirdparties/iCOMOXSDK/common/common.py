from sensors import ADXL362
from sensors import ADXL356
from sensors import ADXL356_SMIP
from sensors import BMM150
from sensors import IM69D130
from sensors import ADT7410
from sensors import ADXL1002
#from communications import TCP_connectivity
from common import iCOMOX_list
from common import common_symbols

common_symbols.InitializeConfiguration()    # Read configuration constants from the INI file

app = None
#IPs = TCP_connectivity.GetIpAddresses()
iCOMOXs = iCOMOX_list.sCOMOXs_list()

ADXL362 = ADXL362.class_ADXL362()
ADXL356_SMIP = ADXL356_SMIP.class_ADXL356_SMIP()
ADXL356 = ADXL356.class_ADXL356()
BMM150 = BMM150.class_BMM150(quantile_for_noise_floor_estimator=common_symbols.BMM150_quantile_for_noise_floor_estimator, minimum_SNR_for_speed_detection_dB=common_symbols.BMM150_minimum_SNR_for_speed_detection_dB)
IM69D130 = IM69D130.class_IM69D130()
ADT7410 = ADT7410.class_ADT7410()
ADXL1002 = ADXL1002.class_ADXL1002()
