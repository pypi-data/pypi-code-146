"""
    Python library to use BIMMS measurement setup
    Authors: Florian Kolbl / Louis Regnacq
    (c) ETIS - University Cergy-Pontoise
        IMS - University of Bordeaux
        CNRS

    Requires:
        Python 3.6 or higher
        Analysis_Instrument - class handling Analog Discovery 2 (Digilent)

    Dev notes:
        - LR: in BIMMS_constants, IO15 change with IO7 because hardware issue.  
        - LR: TIA relay modified too

"""
import sys
import os
import andi as ai
import faulthandler
import numpy as np
import os 
import json
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter,butter, lfilter, freqz
from   time         import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import constants as cst


### for debug
faulthandler.enable()
### verbosity of the verbosity
verbose = True

#############################
## miscalleneous functions ##
#############################
def convert(int32_val):
    bin = np.binary_repr(int32_val, width = 32)
    #int8_arr = [int(bin[24:32],2), int(bin[16:24],2), int(bin[8:16],2), int(bin[0:8],2)] 	# LSBs First
    int8_arr = [int(bin[0:8],2),int(bin[8:16],2),int(bin[16:24],2),int(bin[24:32],2)]		# MSBs First
    return int8_arr

def ComputeSplitFit(coef_list,freq_lim,freq):
    Nsplit = len(freq_lim)
    data_arr = []
    data = []
    freq_list_array = []
    if (Nsplit == 1):
        data_poly = np.poly1d(coef_list[0])
        data = data_poly(freq)
    else:
        for idx in range (Nsplit):
            if (idx==0):
                x = np.where(freq<=freq_lim[idx])
            else:
                x = np.where((freq<=freq_lim[idx]) & (freq>freq_lim[idx-1]))
            if (x):
                freq_split = freq[x]
                data_poly = np.poly1d(coef_list[idx])
                data = np.concatenate((data,data_poly(freq_split)),axis =0)
                freq_list_array = np.concatenate((freq_list_array,freq_split),axis =0)
        data = np.interp(freq, freq_list_array, data)
    return(data)

def unwrap_phase(phase):
    for x in range (len(phase)):
        if phase[x]>180:
            phase[x] = 360-phase[x]
            #print(open_cal_phase[x])
        if phase[x]<0:
            phase[x] = -(phase[x])
    return(-phase)

##############################
## CLASS FOR BIMMS HANDLING ##
##############################
class BIMMS(object):
    def __init__(self):
        super(BIMMS, self).__init__()
        self.interface = ai.Andi()
        if verbose:
            print('device opened')
        self.SPI_init()
        self.ID = self.get_board_ID()
        if (self.ID == 0 or self.ID > 255):
            self.close()
            if verbose:
                raise ValueError('Failed to communicate with STM32 MCU. Make sure that BIMMS is powered (try to reconnect USB).')
            quit()
        if verbose:
            print('You are connected to BIMMS '+str(self.ID))

        # default values for gains of all channels
        self.CalFile = ''
        self.Gain_TIA = 100
        self.Gain_Voltage_SE = 1.1
        self.Gain_Voltage_DIFF = 2.2
        self.Gain_High_current = 1/5000
        self.Gain_Low_current = 1/50000


        # Relay states
        self.Ch1Coupling = 0 
        self.Chan1Scope1 = 0
        self.Ch2Coupling = 0
        self.Chan2Scope2 = 0
        self.DCFeedback = 0
        self.InternalAWG = 0
        self.TIANegIn1 = 0
        self.TIANegIn2 = 0
        self.TIA2Chan2 = 0
        self.TIACoupling = 0
        self.EnPotentiostat = 0
        self.EnCurrentSource = 0
        self.GainCurrentSource = 0
        self.Potentiostat2StimPos = 0
        self.Ipos2StimPos = 0
        self.VoutPos2StimPos = 0
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 0
        self.StimCoupling = 0
        self.StimNeg2VNeg = 0
        self.StimPos2VPos = 0

        #IA gain IO
        self.CH1_A0_0 = 0
        self.CH1_A1_0 = 0
        self.CH1_A0_1 = 0
        self.CH1_A1_1 = 0
        self.CH2_A0_0 = 0
        self.CH2_A1_0 = 0
        self.CH2_A0_1 = 0
        self.CH2_A1_1 = 0

        #LEDs 
        self.LED_status = 0
        self.LED_err = 0

        #Free AD2 DIO (O is input, 1 is ouput)
        self.IO6_IO = 0
        self.IO7_IO = 0
        self.IO6_value = 0
        self.IO7_value = 0

        self.OSLCalibration = False 
        self.cal_folder = './CalibrationData/'
        self.OSL_cal_data = 0

        self.DIO_init()


        #Try to load DC calibration file 
        if (self.Load_DCCal()):
            self.DCCalibration = True 
            if verbose:
                print("DC Calibration data successfully loaded.")
        else :
            self.DCCalibration = False 
            if verbose:
                print("WARNING: DC Calibration does not exist.")
                print("Estimated current, voltage and impedance will be innacurate.")
                print("Consider running DC calibration script.")

        
        if (self.Load_OSLCal()==12):
            self.OSH_all_cal = 1
            if verbose:
                print("All Open-Short-Load calibration data loaded.")
            self.OSLCalibration = True 
        elif(self.Load_OSLCal()>0):
            self.OSLCalibration = True 
            if verbose:
                print("WARNING: Some Open-Short-Load Calibration data are missing.")
        else:
            if verbose:
                print("WARNING: Open-Short-Load Calibration does not exist.")
                print("Estimated impedance will be innacurate.")
                print("Consider running Open-Short-Load calibration script.")
            self.OSLCalibration = False 

    def __del__(self):
        self.close()

    def close(self):
        self.set_state(cst.STM32_stopped)
        self.interface.close()
        if verbose:
            print('device closed')

    def Load_DCCal(self):
        if not os.path.exists(self.cal_folder):
            if verbose:
                return(0)
        else:
            file_name = self.cal_folder + 'DCCal_BIMMS_' + str(self.ID) + '.json'
            try:
                json_file = open(file_name) 
                self.DCCalFile = json.load(json_file)
                json_file.close()
                if (self.DCCalFile['BIMMS_SERIAL'] != self.ID):
                    return(0)
            except:
                return(0)
        if (self.DCCalFile):

            if 'gain_TIA' in self.DCCalFile:
                self.Gain_TIA = self.DCCalFile['gain_TIA']
            if 'gain_voltage_SE' in self.DCCalFile:
                self.Gain_Voltage_SE = self.DCCalFile['gain_voltage_SE']
            if 'gain_voltage_DIFF' in self.DCCalFile:
                self.Gain_Voltage_DIFF = self.DCCalFile['gain_voltage_DIFF']
            if 'low_gain_current' in self.DCCalFile:
                self.Gain_Low_current = self.DCCalFile['low_gain_current']
            if 'high_gain_current' in self.DCCalFile:
                self.Gain_High_current = self.DCCalFile['high_gain_current']
        return(1)


    def Load_OSLCal(self):
        if not os.path.exists(self.cal_folder):
            return(0)
        else:
            file_name = './' + self.cal_folder + '/OSLCal_BIMMS_' + str(self.ID) + '.json'
            try:
                json_file = open(file_name) 
                self.OSLCalFile = json.load(json_file)
                if (self.OSLCalFile['BIMMS_SERIAL'] != self.ID):
                    return(0)
            except:
                return(0)

        n_cal_data = 0
        if(self.OSLCalFile["potentiostat"]["SE"]["DC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["potentiostat"]["SE"]["AC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["potentiostat"]["differential"]["DC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["potentiostat"]["differential"]["AC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["galvanostat"]["SE"]['High_gain']["DC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["galvanostat"]["SE"]['High_gain']["AC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["galvanostat"]["SE"]['Low_gain']["DC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["galvanostat"]["SE"]['Low_gain']["AC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["galvanostat"]["differential"]['High_gain']["DC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["galvanostat"]["differential"]['High_gain']["AC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["galvanostat"]["differential"]['Low_gain']["DC"]!={}):
            n_cal_data = n_cal_data + 1 
        if(self.OSLCalFile["galvanostat"]["differential"]['Low_gain']["AC"]!={}):
            n_cal_data = n_cal_data + 1 
        return(n_cal_data)


    def Update_DCCal(self,measured_gain,value):
        if (self.DCCalibration == 0):			#Create Cal file if does not exist
            if verbose:
                print('Creating new DC Calibration file for BIMMS '+str(self.ID) + '.')
            if not os.path.exists(self.cal_folder):
                os.makedirs(self.cal_folder)
            self.DCCalFile = {}
            self.DCCalFile['BIMMS_SERIAL'] = self.ID 

        self.DCCalFile[measured_gain] = value

        outfile_name = './' + self.cal_folder + '/DCCal_BIMMS_' + str(self.ID) + '.json'
        outfile = open(outfile_name,'w')
        json.dump(self.DCCalFile,outfile)
        outfile.close()
        self.DCCalibration = True 
        self.Load_DCCal()


    def Create_OSLCal(self):
        if not os.path.exists(self.cal_folder):
            os.makedirs(self.cal_folder)
        self.OSLCalFile = {}
        self.OSLCalFile['BIMMS_SERIAL'] = self.ID
        self.OSLCalFile['potentiostat'] = {}
        self.OSLCalFile['potentiostat']['SE'] = {}
        self.OSLCalFile['potentiostat']['differential'] = {}
        self.OSLCalFile['potentiostat']['SE']['AC'] = {} 
        self.OSLCalFile['potentiostat']['SE']['DC'] = {} 
        self.OSLCalFile['potentiostat']['differential']['AC'] = {} 
        self.OSLCalFile['potentiostat']['differential']['DC'] = {}

        self.OSLCalFile['galvanostat'] = {}
        self.OSLCalFile['galvanostat']['SE'] = {}
        self.OSLCalFile['galvanostat']['differential'] = {}
        self.OSLCalFile['galvanostat']['SE']["Low_gain"] = {}
        self.OSLCalFile['galvanostat']['SE']["High_gain"] = {}

        self.OSLCalFile['galvanostat']['differential']["Low_gain"] = {}
        self.OSLCalFile['galvanostat']['differential']["High_gain"] = {}

        self.OSLCalFile['galvanostat']['differential']["High_gain"]["DC"] = {}
        self.OSLCalFile['galvanostat']['differential']["High_gain"]["AC"] = {}
        self.OSLCalFile['galvanostat']['differential']["Low_gain"]["DC"] = {}
        self.OSLCalFile['galvanostat']['differential']["Low_gain"]["AC"] = {}

        self.OSLCalFile['galvanostat']['SE']["High_gain"]["DC"] = {}
        self.OSLCalFile['galvanostat']['SE']["High_gain"]["AC"] = {}
        self.OSLCalFile['galvanostat']['SE']["Low_gain"]["DC"] = {}
        self.OSLCalFile['galvanostat']['SE']["Low_gain"]["AC"] = {}

        outfile_name = './' + self.cal_folder + '/OSLCal_BIMMS_' + str(self.ID) + '.json'
        outfile = open(outfile_name,'w')
        json.dump(self.OSLCalFile,outfile)
        outfile.close()
        self.OSLCalibration = True
        self.Load_OSLCal()




    def Update_OSLCal(self,Z_load,data_open,data_short,data_load,excitation_mode = 'potentiostat',differential = True, high_current_gain = True,coupling = 'DC'):
        if (self.OSLCalibration == False):			#Create Cal file if does not exist
            if verbose:
                print('Creating new OSL Calibration file for BIMMS '+str(self.ID) + '.')
            self.Create_OSLCal()

        data = {}
        data['load'] = data_load.toJson()
        data['open'] = data_open.toJson()
        data['short'] = data_short.toJson()
        data['resistor'] = Z_load

        if(differential):
            connection_mode = 'differential'
        else :
            connection_mode = 'SE'
        if(high_current_gain):
            current_gain = 'High_gain'
        else :
            current_gain = 'Low_gain'

        if (excitation_mode == 'potentiostat'):
            self.OSLCalFile[excitation_mode][connection_mode][coupling] = {}
            self.OSLCalFile[excitation_mode][connection_mode][coupling] = data
        else :
            self.OSLCalFile[excitation_mode][connection_mode][current_gain][coupling] = {}
            self.OSLCalFile[excitation_mode][connection_mode][current_gain][coupling] = data

        outfile_name = './' + self.cal_folder + '/OSLCal_BIMMS_' + str(self.ID) + '.json'
        outfile = open(outfile_name,'w')
        json.dump(self.OSLCalFile,outfile)
        outfile.close()
        self.OSLCalibration = True
        self.Load_OSLCal()



    ##############################################
    ## AD2 Digital IO methods for gains control ##
    ##############################################
    def DIO_init(self):
        self.interface.configure_digitalIO()
        self.set_DIO_mode()

    def set_DIO_mode(self):
        IO_vector = 0
        IO_vector += self.IO6_IO * cst.IO6
        

        #IO_vector += self.IO7_IO * cst.IO7
        #LEDs and IA gain IOs are always set as outputs
        IO_vector += cst.LED_status
        IO_vector += cst.LED_err
        IO_vector += cst.CH1_A0_0
        IO_vector += cst.CH1_A1_0
        IO_vector += cst.CH1_A0_1
        IO_vector += cst.CH1_A1_1
        IO_vector += cst.CH2_A0_0
        IO_vector += cst.CH2_A1_0
        IO_vector += cst.CH2_A0_1
        IO_vector += cst.CH2_A1_1
        self.interface.digitalIO_set_as_output(IO_vector) 

    def set_DIO_output(self):
        OUTPUT_vector = 0
        OUTPUT_vector += self.IO6_value * cst.IO6
        OUTPUT_vector += self.IO7_value * cst.IO7
        #LEDs and IA gain IOs are always set as outputs
        OUTPUT_vector += self.LED_status * cst.LED_status
        OUTPUT_vector += self.LED_err * cst.LED_err
        OUTPUT_vector += self.CH1_A0_0 * cst.CH1_A0_0
        OUTPUT_vector += self.CH1_A1_0 * cst.CH1_A1_0
        OUTPUT_vector += self.CH1_A0_1 * cst.CH1_A0_1
        OUTPUT_vector += self.CH1_A1_1 * cst.CH1_A1_1
        OUTPUT_vector += self.CH2_A0_0 * cst.CH2_A0_0
        OUTPUT_vector += self.CH2_A1_0 * cst.CH2_A1_0
        OUTPUT_vector += self.CH2_A0_1 * cst.CH2_A0_1
        OUTPUT_vector += self.CH2_A1_1 * cst.CH2_A1_1

        self.interface.digitalIO_output(OUTPUT_vector)

    def set_LED_status (self, value = True):
        if (value):
            self.LED_status = 1
        else :
            self.LED_status = 0
        self.set_DIO_output()

    def set_LED_error (self, value = True):
        if (value):
            self.LED_err = 1
        else :
            self.LED_err = 0
        self.set_DIO_output()

    def set_gain_ch1_1(self,value):
        if (value != 1) and (value != 2) and (value != 5) and (value != 10): #Invalid gain value
            self.CH1_A0_0 = 0												 #Gain is one
            self.CH1_A1_0 = 0		
        if value == 1: 
            self.CH1_A0_0 = 0
            self.CH1_A1_0 = 0	
        if value == 2:
            self.CH1_A0_0 = 1
            self.CH1_A1_0 = 0	
        if value == 5: 
            self.CH1_A0_0 = 0
            self.CH1_A1_0 = 1	
        if value == 10: 
            self.CH1_A0_0 = 1
            self.CH1_A1_0 = 1	
        self.set_DIO_output()

    def set_gain_ch1_2(self,value):
        if (value != 1) and (value != 2) and (value != 5) and (value != 10): #Invalid gain value
            self.CH1_A0_1 = 0
            self.CH1_A1_1 = 0										     #Gain is one
        if value == 1: 
            self.CH1_A0_1 = 0
            self.CH1_A1_1 = 0
        if value == 2:
            self.CH1_A0_1 = 1
            self.CH1_A1_1 = 0
        if value == 5: 
            self.CH1_A0_1 = 0
            self.CH1_A1_1 = 1
        if value == 10: 
            self.CH1_A0_1 = 1
            self.CH1_A1_1 = 1
        self.set_DIO_output()

    def set_gain_ch2_1(self,value):
        if (value != 1) and (value != 2) and (value != 5) and (value != 10): #Invalid gain value
            self.CH2_A0_0 = 0
            self.CH2_A1_0 = 0											     #Gain is one
        if value == 1: 
            self.CH2_A0_0 = 0
            self.CH2_A1_0 = 0
        if value == 2:
            self.CH2_A0_0 = 1
            self.CH2_A1_0 = 0
        if value == 5: 
            self.CH2_A0_0 = 0
            self.CH2_A1_0 = 1
        if value == 10: 
            self.CH2_A0_0 = 1
            self.CH2_A1_0 = 1
        self.set_DIO_output()

    def set_gain_ch2_2(self,value):
        if (value != 1) and (value != 2) and (value != 5) and (value != 10): #Invalid gain value
            self.CH2_A0_1 = 0
            self.CH2_A1_1 = 0										     #Gain is one
        if value == 1: 
            self.CH2_A0_1 = 0
            self.CH2_A1_1 = 0	
        if value == 2:
            self.CH2_A0_1 = 1
            self.CH2_A1_1 = 0	
        if value == 5: 
            self.CH2_A0_1 = 0
            self.CH2_A1_1 = 1	
        if value == 10: 
            self.CH2_A0_1 = 1
            self.CH2_A1_1 = 1	
        self.set_DIO_output()

    def set_gain_IA(self,channel = 1, gain = 1):
        gain_array = np.array([1,2,4,5,10,20,25,50,100])
        gain_IA1 = np.array([1,2,2,5,5,10,5,10,10])
        gain_IA2 = np.array([1,1,2,1,2,2,5,5,10])
        idx_gain = np.where(gain_array==gain)
        idx_gain=idx_gain[0]
        if  idx_gain!= None:
            if (channel == 1):
                self.set_gain_ch1_1(gain_IA1[idx_gain])
                self.set_gain_ch1_2(gain_IA2[idx_gain])
            if (channel == 2):
                self.set_gain_ch2_1(gain_IA1[idx_gain])
                self.set_gain_ch2_2(gain_IA2[idx_gain])
        else:
            if verbose:
                print('WARNING: Wrong IA gain value. IA gain set to 1.')
            if (channel == 1):
                self.set_gain_ch1_1(gain_IA1[0])
                self.set_gain_ch1_2(gain_IA2[0])
            if (channel == 2):
                self.set_gain_ch2_1(gain_IA1[0])
                self.set_gain_ch2_2(gain_IA2[0])


    #################################
    ## STM32 communitation methods ##
    #################################
    def SPI_init(self):
        self.interface.SPI_reset()
        self.interface.set_SPI_frequency(1e6)
        self.interface.set_SPI_Clock_channel(1)
        self.interface.set_SPI_Data_channel(ai.SPIDataIdx['DQ0_MOSI_SISO'],2)
        self.interface.set_SPI_Data_channel(ai.SPIDataIdx['DQ1_MISO'],3)
        self.interface.set_SPI_mode(ai.SPIMode['CPOL_1_CPA_1'])
        self.interface.set_SPI_MSB_first()
        self.interface.set_SPI_CS(0,ai.LogicLevel['H'])

    def tx_2_STM32(self,value):
        tx_8bvalues = convert(value)
        self.interface.set_SPI_CS(0,ai.LogicLevel['L'])		
        for k in tx_8bvalues:
            self.interface.SPI_write_one(ai.SPI_cDQ['MOSI/MISO'],8,k)
        self.interface.set_SPI_CS(0,ai.LogicLevel['H'])

    def rx_from_STM32(self):
        offsets = [2**24, 2**16, 2**8, 2**0]
        value = 0
        self.interface.set_SPI_CS(0,ai.LogicLevel['L'])
        for k in offsets:
            rx = self.interface.SPI_read_one(ai.SPI_cDQ['MOSI/MISO'],8)
            value += rx*k
        self.interface.set_SPI_CS(0,ai.LogicLevel['H'])
        return value

    def read_STM32_register(self, address):
        value = cst.cmd_shift * cst.read_register + address
        #print(bin(2**32))
        #print(bin(value))
        self.tx_2_STM32(value)
        register_value = self.rx_from_STM32()
        return register_value

    def set_state(self,state):
        '''
            Set the state of STM32

            Parameters
            ----------
            state : int
                either STM32_stopped, STM32_idle, STM32_locked, STM32_error = 0x03
                defined in BIMMS_constants
        '''
        value = cst.cmd_shift * cst.set_STM32_state + state
        self.tx_2_STM32(value)

    def set_STM32_stopped(self):
        self.set_state(cst.STM32_stopped)

    def set_STM32_idle(self):
        self.set_state(cst.STM32_idle)

    def set_STM32_locked(self):
        self.set_state(cst.STM32_locked)

    def set_STM32_error(self):
        self.set_state(cst.STM32_error)

    def get_state(self):
        '''
            Get the state of the STM32

            Returns
            -------
            state	: int
                0: STM32_stopped
                1: STM32_idle
                2: STM32_locked
                3: STM32_error
        '''
        state = self.read_STM32_register(cst.state_add)
        return state

    def get_STM32_error(self):
        error = self.read_STM32_register(cst.error_add)
        return error

    #######################
    ## low level methods ##
    #######################
    def get_board_ID(self):
        ID = self.read_STM32_register(cst.ID_add)
        return ID

    def get_config_vector(self):
        vector = 0
        vector += self.Ch1Coupling * cst.Ch1Coupling_rly
        vector += self.Chan1Scope1 * cst.Chan1Scope1_rly
        vector += self.Ch2Coupling * cst.Ch2Coupling_rly
        vector += self.Chan2Scope2 * cst.Chan2Scope2_rly
        vector += self.DCFeedback * cst.DCFeedback_rly
        vector += self.InternalAWG * cst.InternalAWG_rly
        vector += self.TIANegIn1 * cst.TIANegIn1_rly
        vector += self.TIANegIn2 * cst.TIANegIn2_rly
        vector += self.TIA2Chan2 * cst.TIA2Chan2_rly
        vector += self.TIACoupling * cst.TIACoupling_rly
        vector += self.EnPotentiostat * cst.EnPotentiostat_rly 
        vector += self.EnCurrentSource * cst.EnCurrentSource_rly 
        vector += self.GainCurrentSource * cst.GainCurrentSource_rly 
        vector += self.Potentiostat2StimPos * cst.Potentiostat2StimPos_rly 
        vector += self.Ipos2StimPos * cst.Ipos2StimPos_rly 
        vector += self.VoutPos2StimPos * cst.VoutPos2StimPos_rly 
        vector += self.Ineg2StimNeg * cst.Ineg2StimNeg_rly 
        vector += self.VoutNeg2StimNeg * cst.VoutNeg2StimNeg_rly 
        vector += self.TIA2StimNeg * cst.TIA2StimNeg_rly 
        vector += self.GND2StimNeg * cst.GND2StimNeg_rly 
        vector += self.StimCoupling * cst.StimCoupling_rly 
        vector += self.StimNeg2VNeg * cst.StimNeg2VNeg_ryl 
        vector += self.StimPos2VPos * cst.StimPos2VPos_rly
        return vector 

    def set_relays(self, rvector):
        '''
            Set all the relays values at once

            Parameters
            ----------
            rvector : int
                see BIMMS_constant for relays mapping
        '''
        value = cst.cmd_shift * cst.set_relay + rvector
        self.tx_2_STM32(value)

    def get_relays(self):
        '''
            Get the values of all relays

            Returns
            -------
            values : int
                see BIMMS_constant for relays mapping
        '''
        relays_map = self.read_STM32_register(cst.relays_map_add)
        return relays_map

    def set_config(self):
        '''
            Set the relay config to the one stored in the current object
        '''
        rvector = self.get_config_vector()
        self.set_relays(rvector)
        # error handling to be written here

    #################################
    ## BIMMS configuration methods ##
    #################################

    def connect_CH1_to_scope_1 (self):
        self.Chan1Scope1 = 1

    def disconnect_CH1_from_scope_1 (self):
        self.Chan1Scope1 = 0

    def connect_CH2_to_scope_2 (self):
        self.Chan2Scope2 = 1

    def disconnect_CH2_from_scope_2 (self):
        self.Chan2Scope2 = 0

    def set_CH1_AC_coupling (self):
        self.Ch1Coupling = 1
    
    def set_CH1_DC_coupling (self):
        self.Ch1Coupling = 0

    def set_CH2_AC_coupling (self):
        self.Ch2Coupling = 1
    
    def set_CH2_DC_coupling (self):
        self.Ch2Coupling = 0

    def connect_Vpos_to_StimPos(self):
        self.VoutPos2StimPos = 1
        self.Ipos2StimPos = 0
        self.Potentiostat2StimPos=0

    def connect_Ipos_to_StimPos(self):
        self.VoutPos2StimPos = 0
        self.Ipos2StimPos = 1
        self.Potentiostat2StimPos=0

    def connect_Potentiostat_to_StimPos(self):
        self.VoutPos2StimPos = 0
        self.Ipos2StimPos = 0
        self.Potentiostat2StimPos=1		
                                
    def disconnect_StimPos(self):
        self.VoutPos2StimPos = 0
        self.Ipos2StimPos = 0
        self.Potentiostat2StimPos = 0

    def connect_Ineg_to_StimNeg(self):
        self.Ineg2StimNeg = 1
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 0

    def connect_Vneg_to_StimNeg(self):
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 1
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 0

    def connect_TIA_to_StimNeg(self):
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 1
        self.GND2StimNeg = 0

    def connect_GND_to_StimNeg(self):
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 1

    def disconnect_StimNeg(self):
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 0

    def enable_DC_feedback(self):
        self.DCFeedback=1

    def disable_DC_feedback(self):
        self.DCFeedback=0

    def connect_external_AWG(self):
        self.InternalAWG=1

    def connect_internal_AWG(self):
        self.InternalAWG=0

    def connect_TIA_to_CH2(self):				# BUG !! Normalement = 0 pour disconnect mais 1 ici pour réparer bug Hardware
        self.TIA2Chan2=0

    def disconnect_TIA_from_CH2(self):			#Ne marche pas car bug Hardware
        self.TIA2Chan2=1

    def connect_TIA_Neg_to_ground(self):
        self.TIANegIn1=0
        self.TIANegIn2=0

    def connect_TIA_Neg_to_Vneg(self):
        self.TIANegIn1=1
        self.TIANegIn2=0

    def connect_TIA_Neg_to_Ineg(self):
        self.TIANegIn1=1
        self.TIANegIn2=1

    def set_TIA_AC_coupling(self):
        self.TIACoupling=1

    def set_TIA_DC_coupling(self):
        self.TIACoupling=0
    
    def enable_potentiostat(self):
        self.EnPotentiostat=1

    def disable_potentiostat(self):
        self.EnPotentiostat=0

    def enable_current_source(self):
        self.EnCurrentSource=0

    def disable_current_source(self):		#Might not be usefull / bad for AD830
        self.EnCurrentSource=1

    def set_high_gain_current_source(self):
        self.GainCurrentSource=0
    
    def set_low_gain_current_source(self):
        self.GainCurrentSource=1

    def set_Stim_DC_coupling(self):
        self.StimCoupling=1
    
    def set_Stim_AC_coupling(self):
        self.StimCoupling=0

    ################################
    ## BIMMS measurements methods ##
    ################################

    def set_2_points_config(self):
        self.StimNeg2VNeg = 1
        self.StimPos2VPos = 1

    def set_3_points_config(self):
        pass

    def set_4_points_config(self):
        self.StimNeg2VNeg = 0
        self.StimPos2VPos = 0

    def set_current_excitation(self, coupling = 'DC', differential_stim = True, DC_feedback = False, Internal_AWG = True, High_gain = False):
        if coupling == 'DC':
            self.set_Stim_DC_coupling()
            self.disable_DC_feedback()
        else:
            self.set_Stim_AC_coupling()
        if DC_feedback:
            self.enable_DC_feedback()
        else:
            self.disable_DC_feedback()
        self.connect_Ipos_to_StimPos()
        if differential_stim:
            self.connect_Ineg_to_StimNeg()
        else:
            self.connect_GND_to_StimNeg()

        if High_gain:
            self.set_high_gain_current_source()
        else:
            self.set_low_gain_current_source()

        if Internal_AWG:
            self.connect_internal_AWG()
        else: 
            self.connect_external_AWG()
        self.disable_potentiostat()

    def set_voltage_excitation(self, coupling = 'DC', differential_stim = True, Internal_AWG = True):
        self.disable_DC_feedback()
        if coupling == 'DC':
            self.set_Stim_DC_coupling()
        else:
            self.set_Stim_AC_coupling()
        self.connect_Vpos_to_StimPos()
        
        if differential_stim:
            self.connect_Vneg_to_StimNeg()
        else:
            self.connect_GND_to_StimNeg()

        if Internal_AWG:
            self.connect_internal_AWG()
        else: 
            self.connect_external_AWG()
        #self.disable_current_source()			#need to be tested, bug with AD830?
        self.disable_potentiostat()
        

    def set_recording_channel_1(self, coupling = 'DC', gain = 1.0):
        self.connect_CH1_to_scope_1()
        if coupling == 'DC':
            self.set_CH1_DC_coupling()
        else:
            self.set_CH1_AC_coupling()

        self.set_gain_IA(channel = 1, gain = gain)

    def set_recording_channel_2(self, coupling = 'DC', gain = 1.0):
        self.connect_CH2_to_scope_2()
        if coupling == 'DC':
            self.set_CH2_DC_coupling()
        else:
            self.set_CH2_AC_coupling()

        self.set_gain_IA(channel = 2, gain = gain)

    def set_recording_voltage(self, coupling = 'DC', gain = 1.0):
        self.set_recording_channel_1(coupling = coupling, gain = gain)

    def set_recording_current(self, differential = True, coupling = 'DC', gain = 1.0):
        self.set_recording_channel_2(coupling = coupling, gain = gain)
        self.connect_TIA_to_CH2()
        self.connect_TIA_to_StimNeg()
        #self.connect_TIA_Neg_to_ground()
        
        if differential:
            if self.VoutPos2StimPos:  #Voltage excitation
                self.connect_TIA_Neg_to_Vneg()
            else:
                if self.connect_Ipos_to_StimPos(): #Current excitation
                    self.connect_TIA_Neg_to_Ineg()
                else:
                    self.connect_TIA_Neg_to_ground()
        else:
            self.connect_TIA_Neg_to_ground()
        if coupling == 'DC':
            self.set_TIA_DC_coupling()
        else: 
            self.set_TIA_DC_coupling()

    def set_potentiostat_EIS_config(self,differential = True, two_wires = True, coupling = 'DC',voltage_gain=1,current_gain = 1):
        self.set_STM32_idle()
        if (differential):
            if (coupling == 'DC'):
                self.set_voltage_excitation(coupling = 'DC', differential_stim = True)
                self.set_recording_current(differential = True, coupling = 'DC', gain = current_gain)		
                self.set_recording_voltage(coupling = 'DC', gain = voltage_gain)							
            else :
                self.set_voltage_excitation(coupling = 'AC', differential_stim = True)		
                self.set_recording_current(differential = True, coupling = 'DC', gain = current_gain)		
                self.set_recording_voltage(coupling = 'AC', gain = voltage_gain)							
        else :
            if (coupling == 'DC'):
                self.set_voltage_excitation(coupling = 'DC', differential_stim = False)
                self.set_recording_current(differential = False, coupling = 'DC', gain = current_gain)		
                self.set_recording_voltage(coupling = 'DC', gain = voltage_gain)							
            else :
                self.set_voltage_excitation(coupling = 'AC', differential_stim = False)
                self.set_recording_current(differential = False, coupling = 'DC', gain = current_gain)		
                self.set_recording_voltage(coupling = 'AC', gain = voltage_gain)							
        if (two_wires):
            self.set_2_points_config()
        else :
            self.set_4_points_config()
        self.set_config()


    def set_galvanostat_EIS_config(self,differential = True, two_wires = True,High_gain = True, coupling = 'DC', DC_feedback = False,voltage_gain=1,current_gain = 1):
        self.set_STM32_idle()
        if (differential):
            if (coupling == 'DC'):
                self.set_current_excitation(coupling = 'DC', differential_stim = True, DC_feedback = DC_feedback, Internal_AWG = True, High_gain = High_gain)
                self.set_recording_current(differential = True, coupling = 'DC', gain = current_gain)		
                self.set_recording_voltage(coupling = 'DC', gain = voltage_gain)							
            else :
                self.set_current_excitation(coupling = 'AC', differential_stim = True, DC_feedback = DC_feedback, Internal_AWG = True, High_gain = High_gain)	
                self.set_recording_current(differential = True, coupling = 'DC', gain = current_gain)		
                self.set_recording_voltage(coupling = 'DC', gain = voltage_gain)							
        else :
            if (coupling == 'DC'):
                self.set_current_excitation(coupling = 'DC', differential_stim = False, DC_feedback = DC_feedback, Internal_AWG = True, High_gain = High_gain)
                self.set_recording_current(differential = False, coupling = 'DC', gain = current_gain)		
                self.set_recording_voltage(coupling = 'DC', gain = voltage_gain)							
            else :
                self.set_current_excitation(coupling = 'AC', differential_stim = False, DC_feedback = DC_feedback, Internal_AWG = True, High_gain = High_gain)
                self.set_recording_current(differential = False, coupling = 'DC', gain = current_gain)		
                self.set_recording_voltage(coupling = 'DC', gain = voltage_gain)							
        if (two_wires):
            self.set_2_points_config()
        else :
            self.set_4_points_config()

        self.set_config()

    def set_cyclic_voltametry_config(self, mode = 'two_points', coupling = 'DC', differential = True):
        self.set_STM32_idle()
        if (mode == 'two_points'):
            if (coupling == 'DC'):
                self.set_voltage_excitation(coupling = 'DC', differential_stim = differential)
                self.set_recording_current(differential = differential, coupling = 'DC', gain = 1)		
                self.set_recording_voltage(coupling = 'DC', gain = 1)									
            else :
                self.set_voltage_excitation(coupling = 'AC', differential_stim = differential)		
                self.set_recording_current(differential = differential, coupling = 'DC', gain = 1)		
                self.set_recording_voltage(coupling = 'AC', gain = 1)									
            self.set_2_points_config()

        self.set_config()


    def set_cyclic_amperometry_config(self, mode = 'two_points', coupling = 'DC', differential = True,High_gain = True, DC_feedback = False):
        self.set_STM32_idle()
        if (mode == 'two_points'):
            if (coupling == 'DC'):
                self.set_current_excitation(coupling = 'DC', differential_stim = True, DC_feedback = DC_feedback, Internal_AWG = True, High_gain = High_gain)
                self.set_recording_current(differential = differential, coupling = 'DC', gain = 1)		
                self.set_recording_voltage(coupling = 'DC', gain = 1)									
            else :
                self.set_current_excitation(coupling = 'DC', differential_stim = True, DC_feedback = DC_feedback, Internal_AWG = True, High_gain = High_gain)
                self.set_recording_current(differential = differential, coupling = 'DC', gain = 1)		
                self.set_recording_voltage(coupling = 'AC', gain = 1)									
            self.set_2_points_config()
        self.set_config()




    #########################
    ## Calibration methods ##
    #########################

    def apply_OSLCal(self,freq,mag,phase,excitation_mode = 'potentiostat',differential = True, high_current_gain = True,coupling = 'DC'):
        if self.OSLCalibration:
            if(differential):
                connection_mode = 'differential'
            else :
                connection_mode = 'SE'
            if(high_current_gain):
                current_gain = 'High_gain'
            else :
                current_gain = 'Low_gain'
            if (excitation_mode == 'potentiostat'):
                cal_data = self.OSLCalFile[excitation_mode][connection_mode][coupling]

            else :
                cal_data = self.OSLCalFile[excitation_mode][connection_mode][current_gain][coupling]
                
            if(cal_data == {}):
                if (excitation_mode == 'potentiostat'):
                    if verbose:
                        print("WARNING: Potentiostat EIS calibration data not found.")
                else:
                    if verbose:
                        print("WARNING: Galvanostat EIS calibration data not found.")
                return(freq,mag,phase)

            cal_load = cal_data['load']
            cal_open = cal_data['open']
            cal_short = cal_data['short']
            Z_load = cal_data['resistor'] 
            load_coef_mag = np.array(cal_load['mag_coeff'])
            load_freq_mag = np.array(cal_load['mag_freq_range'])
            load_coef_phase = np.array(cal_load['phase_coeff'])
            load_freq_phase = np.array(cal_load['phase_freq_range'])

            short_coef_mag = np.array(cal_short['mag_coeff'])
            short_freq_mag = np.array(cal_short['mag_freq_range'])
            
            short_coef_phase = np.array(cal_short['phase_coeff'])
            short_freq_phase = np.array(cal_short['phase_freq_range'])

            open_coef_mag = np.array(cal_open['mag_coeff'])
            open_freq_mag = np.array(cal_open['mag_freq_range'])

            open_coef_phase = np.array(cal_open['phase_coeff'])
            open_freq_phase = np.array(cal_open['phase_freq_range'])

            #Compute Calibration Poly for freq_meas range
            load_mag_data = ComputeSplitFit(load_coef_mag,load_freq_mag,freq)		
            load_phase_data = ComputeSplitFit(load_coef_phase,load_freq_phase,freq) 
            short_mag_data = ComputeSplitFit(short_coef_mag,short_freq_mag,freq)
            short_phase_data = ComputeSplitFit(short_coef_phase,short_freq_phase,freq) 
            open_mag_data = ComputeSplitFit(open_coef_mag,open_freq_mag,freq)		
            open_phase_data = ComputeSplitFit(open_coef_phase,open_freq_phase,freq)	

            
            Z_cal_load = load_mag_data * np.exp(1j*load_phase_data*np.pi/180)
            Z_cal_short = short_mag_data * np.exp(1j*short_phase_data*np.pi/180)
            Z_cal_open = open_mag_data * np.exp(1j*open_phase_data*np.pi/180)
            Z_measured = mag * np.exp(1j*phase*np.pi/180)

            num = Z_load*(Z_measured-Z_cal_short)*(Z_cal_open-Z_cal_load)
            denom = (Z_cal_open-Z_measured)*(Z_cal_load-Z_cal_short) 
            Z_cal = (num/denom)

            mag_calibrated = np.abs(Z_cal)
            phase_calibrated = np.angle(Z_cal)*180/np.pi

        else :
            if verbose:
                print("WARNING: Calibration file not found. Please consider calibrating the board.")
            return(freq,mag,phase)
        
        return(freq,mag_calibrated,phase_calibrated)


    


    #########################
    ## Measurement Methods ##
    #########################

    def impedance_spectroscopy(self, fmin = 1e2, fmax = 1e7, n_pts = 501, amp = 1, offset = 0, settling_time = 0.1, NPeriods = 32, 
                                Vrange_CH1 = 1.0,Vrange_CH2 = 1.0,offset_CH1 = 0.0,offset_CH2 = 0.0):
        '''
            docstring for the impedance spectrocopy
        '''
        # perform bode measurement
        if (2*Vrange_CH1>5.0):
            Vrange_CH1 = 50.0
        else:
            Vrange_CH1 = 5.0

        if (2*Vrange_CH2>5.0):
            Vrange_CH2 = 50.0
        else:
            Vrange_CH2 = 5.0

        freq, gain_mes, phase_mes, gain_ch1 = self.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods , 
                                                Vrange_CH1 = Vrange_CH1, Vrange_CH2 = Vrange_CH2, offset_CH1 = offset_CH1, offset_CH2 = offset_CH2, verbose = verbose)
        return freq, gain_mes, phase_mes


    def galvanostat_EIS(self,fmin = 1e2, fmax = 1e7, n_pts = 501, I_amp = 1, I_offset = 0, settling_time = 0.1, NPeriods = 32,voltage_gain=1,current_gain = 1,
                                V_range = 1.0, V_offset = 0.0, differential = True,High_gain = True, two_wires = True, coupling = 'DC', DC_feedback = False, apply_cal = True):
        
        self.set_galvanostat_EIS_config(differential=differential, two_wires = two_wires,High_gain = High_gain, coupling = coupling,DC_feedback = DC_feedback,
                                        voltage_gain=voltage_gain,current_gain=current_gain)

        if (High_gain):
            amp = I_amp/self.Gain_High_current
            offset = I_offset/self.Gain_High_current
        else :
            amp = I_amp/self.Gain_Low_current
            offset = I_offset/self.Gain_Low_current

        self.interface.configure_network_analyser()
        Vrange_CH1 = V_range*1.5
        offset_CH1 = V_offset*1.5
        Vrange_CH2 = 1.0
        offset_CH2 = I_offset * 1.5

        freq, gain_mes, phase_mes = self.impedance_spectroscopy(fmin = fmin, fmax = fmax, n_pts = n_pts, amp = amp, offset = offset, settling_time = settling_time, NPeriods = NPeriods, 
                                Vrange_CH1 = Vrange_CH1,Vrange_CH2 = 1.0,offset_CH1 = offset_CH1,offset_CH2 = 0.0)

        mag = gain_mes*self.Gain_TIA
        phase = phase_mes -180

        if (apply_cal):
            freq,mag,phase = self.apply_OSLCal(freq,mag,phase,excitation_mode = 'galvanostat',differential = differential,coupling = coupling,high_current_gain = High_gain)

        return freq, mag, phase



    def potentiostat_EIS(self, fmin = 1e2, fmax = 1e7, n_pts = 501, V_amp = 1, V_offset = 0, settling_time = 0.1, NPeriods = 32,voltage_gain=1,current_gain = 1,
                        differential = True, two_wires = True, coupling = 'DC', apply_cal = True):

        self.set_potentiostat_EIS_config(differential=differential, two_wires = two_wires, coupling = coupling,voltage_gain=voltage_gain,current_gain=current_gain)
            
        if (differential):
            amp = V_amp/self.Gain_Voltage_DIFF
            offset = V_offset/self.Gain_Voltage_DIFF
        else :
            amp = V_amp/self.Gain_Voltage_SE
            offset = V_offset/self.Gain_Voltage_SE

        self.interface.configure_network_analyser()
        Vrange_CH1 = V_amp * 1.5
        offset_CH1 = V_offset * 1.5

        freq, gain_mes, phase_mes = self.impedance_spectroscopy(fmin = fmin, fmax = fmax, n_pts = n_pts, amp = amp, offset = offset, settling_time = settling_time, NPeriods = NPeriods, 
                                Vrange_CH1 = Vrange_CH1,Vrange_CH2 = 1.0,offset_CH1 = offset_CH1,offset_CH2 = 0.0)

        mag = gain_mes*self.Gain_TIA
        phase = phase_mes -180

        if (apply_cal):
            freq,mag,phase = self.apply_OSLCal(freq,mag,phase,excitation_mode = 'potentiostat',differential = differential,coupling = coupling)


        return freq, mag, phase


    def cyclic_voltametry(self,period,V_amp,n_delay,n_avg,filter=True, mode = 'two_points', coupling = 'DC', differential = True):

        N_pts = int(8192)
        fs = (1/(period+0.12*period))*N_pts
        self.set_cyclic_voltametry_config(mode = mode, coupling = coupling, differential = differential)
        if (2*V_amp>=5.0):
            vrange1 = 50.0
        else:
            vrange1 = 5.0
        vrange2 = 1

        if (differential):
            V_awg =V_amp/self.Gain_Voltage_DIFF
        else:
            V_awg =V_amp/self.Gain_Voltage_SE 

        trig_th = 0 
        self.interface.in_set_channel(channel=0, Vrange = vrange1, Voffset=0.0)
        self.interface.in_set_channel(channel=1, Vrange = vrange2, Voffset=0.0)
        self.interface.set_Chan_trigger(0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left") #Improvement: use internal trigger instead
        self.interface.triangle(channel=0, freq=1/period, amp=V_awg, offset=0.0)
        if (n_delay):
            print("Wait for settling...")
            sleep(n_delay*period)
        print("Measuring...")
        t = self.interface.set_acq(freq=fs, samples=N_pts)
        voltage, current = self.interface.acq()
        if n_avg > 0:
            current_array = []
            voltage_array = []
            for i in range (n_avg):
                print ("Average: " + str(i+1))
                self.interface.set_Chan_trigger(0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left") #Improvement: use internal trigger instead
                t = self.interface.set_acq(freq=fs, samples=N_pts)
                voltage, current = self.interface.acq()
                voltage_array.append(voltage)
                current_array.append(current)
            voltage_array = np.array(voltage_array)
            current_array = np.array(current_array)
            voltage = np.mean(voltage_array,axis = 0)
            current = np.mean(current_array,axis = 0)
        else : 
            self.interface.set_Chan_trigger(0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left") #Improvement: use internal trigger instead
            t = self.interface.set_acq(freq=fs, samples=N_pts)
            voltage, current = self.interface.acq()
        if (filter):
            cutoff = 10*(1/period)
            order = 2
            nyq = 0.5 * fs
            normal_cutoff = cutoff / nyq
            b, a = butter(order, normal_cutoff, btype='low', analog=False)
            current = lfilter(b, a, current)
            voltage = lfilter(b, a, voltage)
        t = t-0.05*period
        idx = np.where(t <= 0)
        t = np.delete(t,idx)
        voltage = np.delete(voltage,idx)
        current = np.delete(current,idx)
        print("Done!")

        return(t,voltage,-current/self.Gain_TIA)

    def cyclic_amperometry(self,period,I_amp,V_range,n_delay,n_avg,filter=True, mode = 'two_points', coupling = 'DC', differential = True,High_gain = True, DC_feedback = False):

        N_pts = int(8192)
        fs = (1/(period+0.12*period))*N_pts
        self.set_cyclic_amperometry_config(mode = mode, coupling = coupling, differential = differential,High_gain = High_gain, DC_feedback = DC_feedback)

        if (2*V_range>=5.0):
            vrange1 = 50.0
        else:
            vrange1 = 5.0
        vrange2 = 1

        if (High_gain):
            amp = I_amp/self.Gain_High_current
        else :
            amp = I_amp/self.Gain_Low_current

        trig_th = 0

        self.interface.in_set_channel(channel=0, Vrange = vrange1, Voffset=0)
        self.interface.in_set_channel(channel=1, Vrange = vrange2, Voffset=0)
        self.interface.triangle(channel=0, freq=1/period, amp=amp, offset=0)
        if (n_delay):
            print("Wait for settling...")
            sleep(n_delay*period)
        print("Measuring...")
        t = self.interface.set_acq(freq=fs, samples=N_pts)
        voltage, current = self.interface.acq()
        if n_avg > 0:
            current_array = []
            voltage_array = []
            for i in range (n_avg):
                print ("Average: " + str(i+1))
                self.interface.set_Chan_trigger(0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left") #Improvement: use internal trigger instead
                t = self.interface.set_acq(freq=fs, samples=N_pts)
                voltage, current = self.interface.acq()
                voltage_array.append(voltage)
                current_array.append(current)
            voltage_array = np.array(voltage_array)
            current_array = np.array(current_array)
            voltage = np.mean(voltage_array,axis = 0)
            current = np.mean(current_array,axis = 0)
        else : 
            self.interface.set_Chan_trigger(0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left") #Improvement: use internal trigger instead
            t = self.interface.set_acq(freq=fs, samples=N_pts)
            voltage, current = self.interface.acq()
        if (filter):
            cutoff = 10*(1/period)
            order = 2
            nyq = 0.5 * fs
            normal_cutoff = cutoff / nyq
            b, a = butter(order, normal_cutoff, btype='low', analog=False)
            current = lfilter(b, a, current)
            voltage = lfilter(b, a, voltage)
        t = t-0.05*period
        idx = np.where(t <= 0)
        t = np.delete(t,idx)
        voltage = np.delete(voltage,idx)
        current = np.delete(current,idx)
        print("Done!")

        return(t,voltage,-current/self.Gain_TIA)


    def AW_Potentiostat(self,something):
        pass

    def AW_Galvanostat(self,something):
        pass
