
import numpy as np


def Measure_Offset(BS,channel = 1, gain_IA = 1, acq_duration = 1, Nsample = 8192,coupling = 'DC', Vrange = 10, Voffset = 0):
	sampling_freq = Nsample/acq_duration
	BS.set_STM32_idle()
	if (channel == 1):
		BS.set_recording_channel_1(coupling = coupling, gain = gain_IA)
		BS.interface.in_set_channel(channel=0, Vrange=Vrange, Voffset=Voffset)
	else:
		BS.set_recording_channel_2(coupling = coupling, gain = gain_IA)
		BS.interface.in_set_channel(channel = 1, Vrange=Vrange, Voffset=Voffset)
	BS.set_config()
	BS.interface.set_Auto_chan_trigger(0, timeout=0.1, type="Rising", ref="center")
	t = BS.interface.set_acq(freq=sampling_freq, samples=Nsample)
	dat0, dat1 = BS.interface.acq()
	if(channel == 1):
		offset = np.mean(dat0)
	else :
		offset = np.mean(dat1)
	return(offset)


