"""
Developed by Donghua Chen
2023.1.14
"""

import datetime as dt
import pickle

import numpy as np
import cv2
import serial
import serial.tools.list_ports
import threading
import time
import os

class ReThread(threading.Thread):
    def __init__(self,com,TMax=45,TMin=15,baudrate=115200,wait_time=2,save_folder="irt-captured",func_get_matrix=None):
        threading.Thread.__init__(self)
        self.stop_thermal=False           
        self.Tmax = TMax
        self.Tmin = TMin
        self.com=com
        self.baudrate=baudrate
        self.wait_time=wait_time
        self.save_folder=save_folder
        self.func_get_matrix=func_get_matrix

    def run(self):
        self.ser = serial.Serial (self.com)
        self.ser.baudrate = self.baudrate
        self.ser.write(serial.to_bytes([0xA5, 0x25, 0x01, 0xCB]))  # set frequency of module to 4 Hz
        time.sleep(self.wait_time) #wait for data loading
        self.ser.write(serial.to_bytes([0xA5,0x35,0x02,0xDC]))
        try:
            while True:
                if (self.stop_thermal):
                    print ('Thermal camera Stopped!')
                    break
                else:
                    data = self.ser.read(1544)
                    Ta, Tc, temp_array , f = self.getTempArray(data)
                    if f == True:
                        continue
                    ta_img = self.td2Image(temp_array)		
                    # img = cv2.applyColorMap(ta_img, cv2.COLORMAP_JET)
                    img = cv2.applyColorMap(ta_img, cv2.COLORMAP_JET)
                    img = cv2.resize(img, (640,480), interpolation = cv2.INTER_CUBIC)                    
                    img = cv2.flip(img, 1)
                    temp_min=temp_array.min()/100
                    temp_max=temp_array.max()/100
                    if temp_max>self.Tmax:
                        continue                        
                    text1 = 'Min:{:.1f} Max: {:.1f}'.format(temp_min, temp_max)
                    text2 = 'Center {:.1f} TA: {:.1f}'.format(Tc, Ta)
                    blur = cv2.GaussianBlur(img,(5,5),0)
                    median = cv2.medianBlur(blur,5)
                    x_s=int(median.shape[1]*0.15)
                    y_s=int(median.shape[0]*0.8)
                    y_s2=int(median.shape[0]*0.9)
                    cv2.putText(median, text1, (x_s, y_s), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1)
                    cv2.putText(median, text2, (x_s, y_s2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1)
                    cv2.imshow('Thermal Camera', median)  
                    key = cv2.waitKey(1) & 0xFF      # if 's' is pressed - saving of picture                   
                    if key == ord("s"):
                        if self.save_folder!=None:
                            if not os.path.exists(self.save_folder):
                                os.mkdir(self.save_folder)
                        fname = f'{self.save_folder}/irt_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
                        cv2.imwrite(fname, img)
                        print('Saving image ', fname)
                        csv_name = f'{self.save_folder}/irt_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
                        self.save_temp_matrix(data=temp_array,csv_path=csv_name)
                    if self.func_get_matrix!=None:
                        self.func_get_matrix(self.get_matrix(temp_array))
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            self.ser.close()
            cv2.destroyAllWindows()
       
        except KeyboardInterrupt:
            self.ser.write(serial.to_bytes([0xA5,0x35,0x01,0xDB]))
            self.ser.close()
            cv2.destroyAllWindows()
    
    def getTempArray(self, ser_data):
        datum_error=False
        T_a = (int(ser_data[1540]) + int(ser_data[1541])*256)/100 
        T_c = (int(ser_data[1538]) + int(ser_data[1539])*256)/100   
        raw_data = ser_data[4:1540]# getting raw array of pixels temperature
        T_array = np.frombuffer(raw_data, dtype=np.int16)
        if 0<min(T_array)<4500: 
            pass
        else:
            datum_error=True    
        return T_a, T_c, T_array, datum_error

    def save_temp_matrix(self,data,csv_path=None):
        # pickle.dump(data,open("test_data.pickle","wb"))
        list_temp=list(data)
        # create a temperature matrix
        data_temp = []
        for i in range(0, 24):
            ls = []
            for j in range(0, 32):
                p = 32 * i + j
                ls.append(list_temp[p])
            data_temp.append(ls)

        # saving csv file
        print(len(data_temp), len(data_temp[0]))
        if csv_path!=None:
            f_out = open(csv_path, "w", encoding='utf-8')
            for i in range(0, len(data_temp), 1):
                line = []
                for j in range(len(data_temp[0]) - 1, -1, -1):
                    line.append(round(data_temp[i][j] / 100, 2))
                line_str = [str(l) for l in line]
                f_out.write(",".join(line_str) + "\n")
            f_out.close()

    def get_matrix(self,data):
        list_temp = list(data)
        # create a temperature matrix
        data_temp = []
        for i in range(0, 24):
            ls = []
            for j in range(0, 32):
                p = 32 * i + j
                ls.append(list_temp[p])
            data_temp.append(ls)
        data_temp_flip=[]
        for i in range(0, len(data_temp), 1):
            line = []
            for j in range(len(data_temp[0]) - 1, -1, -1):
                line.append(round(data_temp[i][j] / 100, 2))
            data_temp_flip.append(line)
        return data_temp_flip


    def td2Image(self, f):
        norm = np.uint8((f/100 - self.Tmin)*255/(self.Tmax-self.Tmin))
        norm.shape = (24,32)
        return norm
            
    def stopThermal(self,parm):         
        self.stop_thermal=parm #boolean
        print ('shutdown this thread {}'.format(parm))

class IRTCamera:
    '''
    1.
    STM32F407 -- GY-MCU90640 by USART1
    VIN --  VCC(3.3V)
    GND -- GND
    Rx --  RXD
    Tx -- TXD

    2、Upper computer -USART1- STM32F407 --USART2-- GY-MCU-90640
    VIN --  VCC(3.3V)
    GND -- GND
    Rx --  PA3
    Tx -- PA2
    '''
    def __init__(self,com,baudrate=115200,wait_time=2,save_folder=None,
                 TMin=15,TMax=45,running_time=-1,stop_time=2,func_get_matrix=None):
        self.TMax = TMax
        self.TMin = TMin
        self.com = com
        self.baudrate = baudrate
        self.wait_time = wait_time
        self.save_folder = save_folder
        self.running_time=running_time
        self.stop_time=stop_time
        self.func_get_matrix=func_get_matrix

    def run(self):
        testThread = ReThread(com=self.com,wait_time=self.wait_time,save_folder=self.save_folder,
                              TMin=self.TMin,TMax=self.TMax,func_get_matrix=self.func_get_matrix
                              )
        testThread.setDaemon(True)
        testThread.start()
        if self.running_time!=-1:
            time.sleep(self.running_time)
            testThread.stopThermal(True)
        else:
            x=input("running...Press Any Key to quit!")
            exit(0)
        time.sleep(self.stop_time)
        print("Is it alive ? {}".format(testThread.is_alive()))
