import matplotlib
import numpy as np
import adi
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QStackedLayout, QMessageBox, QGridLayout, QHBoxLayout
import pyqtgraph as pg
import threading

from PyModulace import Ui_ModulaceWindow
import TxRxModul

matplotlib.use('QT5Agg')

width = 0
height = 0

class MyThread(threading.Thread): # Třída pro threading
    def __init__(self, demodulace, rx_samples, nDemodulace=0):
        super(MyThread, self).__init__()
        self.dSamples = None
        self.text = None
        self.demodulace = demodulace
        self.kolik = None
        self.rx_samples = rx_samples
        self.nDemodulace = nDemodulace

    def run(self): # Rozhoduje jaký podprogram má pustit na demodulaci
        if self.demodulace == "AM": 
            self.dSamples = TxRxModul.dAM(self.rx_samples)
        if self.demodulace == "FM": 
            self.dSamples = TxRxModul.dFM(self.rx_samples,100e3)
        if self.demodulace == "ASK":
            self.text, self.kolik = TxRxModul.dASK(self.rx_samples,self.nDemodulace)
        if self.demodulace == "FSK":
            self.text, self.kolik = TxRxModul.dFSK(self.rx_samples,self.nDemodulace)
        if self.demodulace == "PSK":
            self.text, self.kolik = TxRxModul.dPSK(self.rx_samples,self.nDemodulace)
        if self.demodulace == "QAM":
            self.text, self.kolik = TxRxModul.dQAM(self.rx_samples,self.nDemodulace)

    

class Ui_MainWindow(object):
    '''
    Proměnné
    '''
    # Rádio
    num_samps = 15000
    center_freq = 70e6
    sample_rate = 600e3
    samples = []
    rx_samples = []
    tx_samples = []
    # Stav
    provoz = False
    tx = False
    demod = False
    # Vysílání a příjem
    modulace = ''
    demodulace = ''
    nModulace = 2
    nDemodulace = 2
    zprava = ''
    mSamples = [] # Pro AM nebo FM - modulace
    dSamples = [] # Pro dAM nebo dFM - demodulace
    vyhodnoceni = []
    frekvenceMin = 100


    def cJakFunguje(self): # Otevře PyModulace
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ModulaceWindow()
        self.ui.setupUi(self.window, width, height)
        self.window.show()

    def VypocetFFT(self, Signal, N) -> float: # Vypočítá FFT magnitudu a vrátí k tomu i osu frekvence
        Fs = self.sample_rate
        FFT = np.abs(np.fft.fftshift(np.fft.fft(Signal)))
        # FFT_Mag = 10*np.log10(np.abs(FFT))
        FFT_Mag = 10*np.log10(np.abs((FFT)**2)) -140 # 140 podle kalibrace
        f = np.arange(Fs / -2, Fs / 2, Fs / N) + self.center_freq
        return FFT_Mag, f

    def VyhodnoceniZpravy(self, zprava, kolik): # Počítá kolikrát jaká zpráva bylo přijata
        if len(self.vyhodnoceni) == 0 and zprava != "": # Dokud nezachytí zprávu, tak napočítá prázdné zprávy
            # Inicializace
            self.vyhodnoceni.append(zprava) # Zpráva
            self.vyhodnoceni.append(float(kolik)) # Kolikkrát byla zachycena
        else: # Už byla někdy zachycená zpráva
            for i in np.arange(int(len(self.vyhodnoceni)/2),dtype=int):
                if self.vyhodnoceni[2*i] == zprava: # Zpráva už byla někdy zaznamenána
                    if zprava == "":
                        self.vyhodnoceni[2*i+1] += 0.25 # Prázdný text má nižší váhu
                    else:
                        self.vyhodnoceni[2*i+1] += float(kolik)
                    self.ZobrazeniZpravy()
                    break # Neprovede se if pod
                if i == len(self.vyhodnoceni)/2 - 1: # Úplně nová zpráva
                    self.vyhodnoceni.append(zprava)
                    self.vyhodnoceni.append(int(1))
        
    
    def ZobrazeniZpravy(self): # Zobrazí zprávu, která byla nejvíce rozpoznána demodulací
        pocet = np.zeros(int(len(self.vyhodnoceni)/2)) # Počet koliktrá byla každá zpráva zachycená
        for i in np.arange(0,len(self.vyhodnoceni),2): # Nahrání hodnot
            pocet[int(i/2)] = self.vyhodnoceni[i+1]
        index = np.argmax(pocet) # Nalezení nejčastější zprávy
        self.lEzachycenaSekv.setText(str(self.vyhodnoceni[int(2*index)])) # Zobrazení nejčastější zprávy

    def Prevod(self): # Převede hodnoty SpinBoxů na číslo pro center_freq                       
        """
        Převod do proměnné
        """
        setValue = []
        setValue.append(self.sBGHz.value())
        setValue.append(self.sBMHz3.value())
        setValue.append(self.sBMHz2.value())
        setValue.append(self.sBMHz1.value())
        setValue.append(self.sBkHz3.value())
        setValue.append(self.sBkHz2.value())
        setValue.append(self.sBkHz1.value())

        """
        Cyklení
        """ 
        setValueHelper = []
        setValueHelper.append(self.sBGHz.value())
        setValueHelper.append(self.sBMHz3.value())
        setValueHelper.append(self.sBMHz2.value())
        setValueHelper.append(self.sBMHz1.value())
        setValueHelper.append(self.sBkHz3.value())
        setValueHelper.append(self.sBkHz2.value())
        setValueHelper.append(self.sBkHz1.value())
        
        rozsah = np.arange(len(setValue)-1,0, -1)
        
        """
        Změna řádu
        """
        for i in rozsah:
            """
            Zvýšení řádu
            """
            if setValue[i] == 10:
                setValue[i] = 0
                setValue[i-1] += 1
                if i == 1:
                    self.sBMHz3.setValue(0)
                    self.sBGHz.setValue(setValue[i-1])
                elif i == 2:
                    self.sBMHz2.setValue(0)
                    self.sBMHz3.setValue(setValue[i-1])
                elif i == 3:
                    self.sBMHz1.setValue(0)
                    self.sBMHz2.setValue(setValue[i-1])
                elif i == 4:
                    self.sBkHz3.setValue(0)
                    self.sBMHz1.setValue(setValue[i-1])
                elif i == 5:
                    self.sBkHz2.setValue(0)
                    self.sBkHz3.setValue(setValue[i-1])
                elif i == 6:
                    self.sBkHz1.setValue(0)
                    self.sBkHz2.setValue(setValue[i-1])

            """
            Snížení řádu
            """
            if setValue[i] == -1:
                setValue[i] = 9
                setValue[i-1] -= 1
                if i == 1:
                    self.sBMHz3.setValue(9)
                    self.sBGHz.setValue(setValue[i-1])
                elif i == 2:
                    self.sBMHz2.setValue(9)
                    self.sBMHz3.setValue(setValue[i-1])
                elif i == 3:
                    self.sBMHz1.setValue(9)
                    self.sBMHz2.setValue(setValue[i-1])
                elif i == 4:
                    self.sBkHz3.setValue(9)
                    self.sBMHz1.setValue(setValue[i-1])
                elif i == 5:
                    self.sBkHz2.setValue(9)
                    self.sBkHz3.setValue(setValue[i-1])
                elif i == 6:
                    self.sBkHz1.setValue(9)
                    self.sBkHz2.setValue(setValue[i-1])

        for i in np.arange(7):
            if setValue[i] != setValueHelper[i]:
                if i == 1:
                    self.sBMHz3.setValue(setValue[i])
                elif i == 2:
                    self.sBMHz2.setValue(setValue[i])
                elif i == 3:
                    self.sBMHz1.setValue(setValue[i])
                elif i == 4:
                    self.sBkHz3.setValue(setValue[i])
                elif i == 5:
                    self.sBkHz2.setValue(setValue[i])
                elif i == 6:
                    self.sBkHz1.setValue(setValue[i])

        out = 0
        for i in range(0,7): # Z hodnot ze SpinBoxů se vytvoří číslo
            out = 10*out+setValue[i]
        out *= 1000 # Z kHz se udělá Hz 

        """
        Kontrola frekvence
        """
        if out <= 6e9 and out >= 70e6:
            center_freq = out
        elif out > 6e9: # Překročení maxima
            center_freq = 6e9
            self.sBGHz.setValue(6)
            self.sBMHz3.setValue(0)
            self.sBMHz2.setValue(0)
            self.sBMHz1.setValue(0)
            self.sBkHz3.setValue(0)
            self.sBkHz2.setValue(0)
            self.sBkHz1.setValue(0)
        elif out < 70e6: # Překročení minima
            center_freq = 70e6
            self.sBGHz.setValue(0)
            self.sBMHz3.setValue(0)
            self.sBMHz2.setValue(7)
            self.sBMHz1.setValue(0)
            self.sBkHz3.setValue(0)
            self.sBkHz2.setValue(0)
            self.sBkHz1.setValue(0)

        self.ZmenaFrekvence(center_freq)  

    # def ZmenaVzorkovani(self, sample_rate):
    #     self.sample_rate = sample_rate
    #     self.sdr.sample_rate = int(self.sample_rate)
    #     self.sdr.rx_rf_bandwidth = int(self.sample_rate)  


    #     freq = np.arange(self.sample_rate / -2, self.sample_rate / 2, self.sample_rate / self.num_samps) + self.center_freq
    #     image_height = abs(0-20)
    #     image_width = abs(freq[0]-freq[-1])  # if x and y-scales are the same
    #     # pixel_size = image_height/(freq.size-1)
    #     self.img.setRect(QtCore.QRectF(freq[0], 0., image_width, image_height))

    def ZmenaFrekvence(self, center_freq): # Uloží nosnou frekvenci do veřejné proměnné a nastaví ji do SDR
        self.center_freq = center_freq
        try:
            self.sdr.rx_lo = int(self.center_freq)
        except:
            pass  

    def ZmenaZesileniPrijem(self): # Upravý nastavení zesílení SDR
        if self.provoz: # Lze pouze, když se přijímá
            if self.cBmzesileniPrijem.currentText() == "Manual":
                try:
                    self.sdr.gain_control_mode_chan0 = 'manual'
                except:
                    self.dlg = QMessageBox(self.centralwidget)
                    self.dlg.setIcon(QMessageBox.Critical)
                    self.dlg.setWindowTitle("Problém")
                    # self.dlg.setInformativeText('More information')
                    self.dlg.setText("SDR není připojeno nebo se nelze připojit.")
                    self.dlg.exec()
                else:
                    self.ZmenaZesileniPrijem_manual()
            elif self.cBmzesileniPrijem.currentText() == "Slow attack":
                try:
                    self.sdr.gain_control_mode_chan0 = 'slow_attack'
                except:
                    self.dlg = QMessageBox(self.centralwidget)
                    self.dlg.setIcon(QMessageBox.Critical)
                    self.dlg.setWindowTitle("Problém")
                    # self.dlg.setInformativeText('More information')
                    self.dlg.setText("SDR není připojeno nebo se nelze připojit.")
                    self.dlg.exec()
            elif self.cBmzesileniPrijem.currentText() == "Fast attack":
                try:
                    self.sdr.gain_control_mode_chan0 = 'fast_attack'
                except:
                    self.dlg = QMessageBox(self.centralwidget)
                    self.dlg.setIcon(QMessageBox.Critical)
                    self.dlg.setWindowTitle("Problém")
                    # self.dlg.setInformativeText('More information')
                    self.dlg.setText("SDR není připojeno nebo se nelze připojit.")
                    self.dlg.exec()
    
    def ZmenaZesileniPrijem_manual(self): # Nastavení zesílení příjmu je manuální a nastavuje hodnotu
        try:
            self.sdr.rx_hardwaregain_chan0 = float(self.sBzesileniManualPrijem.value())
        except:
            self.dlg = QMessageBox(self.centralwidget)
            self.dlg.setIcon(QMessageBox.Critical)
            self.dlg.setWindowTitle("Problém")
            # self.dlg.setInformativeText('More information')
            self.dlg.setText("SDR není připojeno nebo se nelze připojit.")
            self.dlg.exec()

    def ZmenaZesileniVysilani(self): # Nastaví atenuátor SDR
        if self.tx:
            try:
                self.sdr.tx_hardwaregain_chan0 = float(self.sBzesileniManualVysilani.value()) # -90 do 0 dB
            except:
                self.dlg = QMessageBox(self.centralwidget)
                self.dlg.setIcon(QMessageBox.Critical)
                self.dlg.setWindowTitle("Problém")
                # self.dlg.setInformativeText('More information')
                self.dlg.setText("SDR není připojeno, nelze se připojit nebo špatně nastavené tesílení.")
                self.dlg.exec()

    def ZmenaVlastniSignal(self): # Převede tabulku na vlastní signál
        # if self.rBzobrazeni2.isChecked():
        frekvence = []
        for i in np.arange(15):
            """
            Zpracování sloupce frekvence
            """
            if self.tWvlastniSignal.item(i,0) != None and self.tWvlastniSignal.item(i,1) != None and self.tWvlastniSignal.item(i,2) != None: # Pokud je prvek v řádku None nejde se dál
                if self.tWvlastniSignal.item(i,0).text() != '' and self.tWvlastniSignal.item(i,1).text() != '' and self.tWvlastniSignal.item(i,2).text() != '': # Řádek musí být vyplněný, aby se počítal
                    frekvence.append(float(self.tWvlastniSignal.item(i,0).text())) # Převedení frekvence v tabulce do listu frekvencí
                    if np.max(frekvence) > 25000: # Omezení pro max frekvenci ve vlastním signálu
                        self.dlg = QMessageBox(self.centralwidget)
                        self.dlg.setIcon(QMessageBox.Critical)
                        self.dlg.setWindowTitle("Problém")
                        self.dlg.setText("Maximální frekvence je 25 kHz!")
                        self.dlg.exec()
                        return # Ukončí se funkce

        self.frekvenceMin = np.min(frekvence) # Nalezení min frekvence pro správné nastavení zobrazení
        t = np.arange(0,2/self.frekvenceMin,1/self.sample_rate)
        vlastniSignal = np.zeros(len(t))
        
        """
        Zpracování zbylých sloupců
        """
        for i in np.arange(15):
            # Podmínky jsou stejné jako výše
            if self.tWvlastniSignal.item(i,0) != None and self.tWvlastniSignal.item(i,1) != None and self.tWvlastniSignal.item(i,2) != None:
                if self.tWvlastniSignal.item(i,0).text() != '' and self.tWvlastniSignal.item(i,1).text() != '' and self.tWvlastniSignal.item(i,2).text() != '':
                    vlastniSignal += float(self.tWvlastniSignal.item(i,1).text()) * np.sin(2*np.pi * frekvence[i] * t + np.deg2rad(float(self.tWvlastniSignal.item(i,2).text()))) # Výsledný vlastní signál
        
        self.data_line2.setData(t, vlastniSignal) # Zobrazení 
        pen = pg.mkPen(color=(255, 0, 0))  
        self.data_line3.setData(t, vlastniSignal, pen=pen) # Zobrazení   
        self.mSamples = vlastniSignal # Pro modulaci
    
    def ZmenaModulaceVysilani(self): # Do proměnné zapíše jaká se používá modulace
        if self.cBmodulaceVysilani.currentText() == "AM": self.modulace = "AM" 
        if self.cBmodulaceVysilani.currentText() == "FM": self.modulace = "FM"
        if self.cBmodulaceVysilani.currentText() == "ASK": self.modulace = "ASK"
        if self.cBmodulaceVysilani.currentText() == "FSK": self.modulace = "FSK"
        if self.cBmodulaceVysilani.currentText() == "PSK": self.modulace = "PSK"
        if self.cBmodulaceVysilani.currentText() == "QAM": self.modulace = "QAM"

    def ZmenaDemodulacePrijem(self): # Do proměnné zapíše jaká se používá demodulace
        if self.cBmodulacePrijem.currentText() == "AM": self.demodulace = "AM" 
        if self.cBmodulacePrijem.currentText() == "FM": self.demodulace = "FM"
        if self.cBmodulacePrijem.currentText() == "ASK": self.demodulace = "ASK"
        if self.cBmodulacePrijem.currentText() == "FSK": self.demodulace = "FSK"
        if self.cBmodulacePrijem.currentText() == "PSK": self.demodulace = "PSK"
        if self.cBmodulacePrijem.currentText() == "QAM": self.demodulace = "QAM"

    def ZmenaRaduModulace(self): # Zapíše do proměnné řád modulace
        self.nModulace = int(self.cBnbitmodulaceVysilani.currentText())

    def ZmenaRaduDemodulace(self): # Zapíše do proměnné řád demodulace
        self.nDemodulace = int(self.cBnbitmodulacePrijem.currentText())

    def AktivaveZobrazeni1(self): # Změní index stacked layoutu na zobrazení 1
        self.layoutStacked.setCurrentIndex(0) # Změna indexu změní zobrazovaný graf waterfall
        
    def AktivaveZobrazeni2(self): # Změní index stacked layoutu na zobrazení 2
        self.layoutStacked.setCurrentIndex(1) # Změna indexu změní zobrazovaný graf Vlastní signál
        self.ZmenaVlastniSignal() # Zobrazí se signál

    def ZobrazeniDemodulace(self): # Zobrazí výsledky demodulace
        if self.demod:
            if self.demodulace == "AM": 
                # self.dSamples = TxRxModul.dAM(self.rx_samples)
                t = np.arange(0,2/self.frekvenceMin,1/self.sample_rate)
                # Nejdříve se zobrazuje a až poté se počítá, takže musí proběhnout aspoň jeden cyklus, aby bylo, co zobrazit
                try:
                    # Zobrazení
                    self.data_line2.setData(t, self.dSamples[0:len(t)])
                    pen = pg.mkPen(color=(255, 0, 0))
                    self.data_line3.setData(t, self.dSamples[0:len(t)],pen=pen)  
                except:
                    pass
                self.t2 = MyThread(self.demodulace, self.rx_samples)
                self.t2.run()
                # t = np.arange(0,2/self.frekvenceMin,1/self.sample_rate)
                self.dSamples = self.t2.dSamples
                # self.data_line2.setData(t, self.dSamples[0:len(t)])
                # pen = pg.mkPen(color=(255, 0, 0))
                # self.data_line3.setData(t, self.dSamples[0:len(t)],pen=pen)  
            if self.demodulace == "FM": 
                # self.dSamples = TxRxModul.dFM(self.rx_samples,100e3)
                t = np.arange(0,2/self.frekvenceMin,1/self.sample_rate)
                # Nejdříve se zobrazuje a až poté se počítá, takže musí proběhnout aspoň jeden cyklus, aby bylo, co zobrazit
                try:
                    # Zobrazení
                    self.data_line2.setData(t, self.dSamples[0:len(t)])
                    pen = pg.mkPen(color=(255, 0, 0))
                    self.data_line3.setData(t, self.dSamples[0:len(t)],pen=pen)  
                except:
                    pass
                self.t3 = MyThread(self.demodulace, self.rx_samples)
                self.t3.run()
                self.dSamples = self.t3.dSamples
                # self.data_line2.setData(t, self.dSamples[0:len(t)])
                # pen = pg.mkPen(color=(255, 0, 0))
                # self.data_line3.setData(t, self.dSamples[0:len(t)],pen=pen)
            if self.demodulace == "ASK":
                # text, kolik = TxRxModul.dASK(self.rx_samples,self.nDemodulace)
                # Nejdříve se zobrazuje a až poté se počítá, takže musí proběhnout aspoň jeden cyklus, aby bylo, co zobrazit
                try:
                    # Zobrazení
                    self.VyhodnoceniZpravy(self.text, self.kolik)
                except:
                    pass
                self.t4 = MyThread(self.demodulace, self.rx_samples, nDemodulace=self.nDemodulace)
                self.t4.run()
                self.text = self.t4.text
                self.kolik = self.t4.kolik
                # self.VyhodnoceniZpravy(text, kolik)
            if self.demodulace == "FSK":
                # text, kolik = TxRxModul.dFSK(self.rx_samples,self.nDemodulace)
                # Nejdříve se zobrazuje a až poté se počítá, takže musí proběhnout aspoň jeden cyklus, aby bylo, co zobrazit
                try:
                    # Zobrazení
                    self.VyhodnoceniZpravy(self.text, self.kolik)
                except:
                    pass
                self.t5 = MyThread(self.demodulace, self.rx_samples, nDemodulace=self.nDemodulace)
                self.t5.run()
                self.text = self.t5.text
                self.kolik = self.t5.kolik
                # self.VyhodnoceniZpravy(text, kolik)
            if self.demodulace == "PSK":
                # text, kolik = TxRxModul.dPSK(self.rx_samples,self.nDemodulace)
                # Nejdříve se zobrazuje a až poté se počítá, takže musí proběhnout aspoň jeden cyklus, aby bylo, co zobrazit
                try:
                    # Zobrazení
                    self.VyhodnoceniZpravy(self.text, self.kolik)
                except:
                    pass
                self.t6 = MyThread(self.demodulace, self.rx_samples, nDemodulace=self.nDemodulace)
                self.t6.run()
                self.text = self.t6.text
                self.kolik = self.t6.kolik
                # self.VyhodnoceniZpravy(text, kolik)
            if self.demodulace == "QAM":
                # text, kolik = TxRxModul.dQAM(self.rx_samples,self.nDemodulace)
                # Nejdříve se zobrazuje a až poté se počítá, takže musí proběhnout aspoň jeden cyklus, aby bylo, co zobrazit
                try:
                    # Zobrazení
                    self.VyhodnoceniZpravy(self.text, self.kolik)
                except:
                    pass
                self.t7 = MyThread(self.demodulace, self.rx_samples, nDemodulace=self.nDemodulace)
                self.t7.run()
                self.text = self.t7.text
                self.kolik = self.t7.kolik
                # self.VyhodnoceniZpravy(text, kolik)
            
            """
            Zobrazení IQ složky
            """
            if self.demodulace != "AM" and self.demodulace != "FM" or not self.demod and self.rBzobrazeni2.isChecked():
                self.data_line2.setData(np.real(self.rx_samples[0:3000]))
                pen = pg.mkPen(color=(0, 255, 0))
                self.data_line3.setData(np.imag(self.rx_samples[0:3000]), pen=pen)

    def RostouciSekvence(self): # Vygeneruje rostoucí sekvenci
        self.lEvlastniSekvence.setText(str(np.arange(0, int(self.cBnbitmodulaceVysilani.currentText()))))

    def NahodnaSekvence(self): # Vygeneruje náhodnou sekvenci
        self.lEvlastniSekvence.setText(str(np.random.randint(0, int(self.cBnbitmodulaceVysilani.currentText()), 2*int(self.cBnbitmodulaceVysilani.currentText()))))

    def cStartVysilani(self): # Spustí vysílání
        if self.provoz: # Musí se přijímat
            if self.modulace == "ASK" or self.modulace == "PSK" or self.modulace == "FSK" or self.modulace == "QAM":
                # Výběr typu tvorby sekvence
                if self.rBvlSekv.isChecked(): zprava = self.lEvlastniSekvence.text()
                if self.rBrostSekv.isChecked(): zprava = self.lEvlastniSekvence.text()
                if self.rBgenSekv.isChecked(): zprava = self.lEvlastniSekvence.text()

                """
                Kontrola textu, který se má vysílat
                """
                if self.nModulace == 2: maxDelka = 61
                if self.nModulace > 2 : maxDelka = 125

                if len(zprava) > maxDelka:
                    self.zprava = ""
                    self.dlg = QMessageBox(self.centralwidget)
                    self.dlg.setIcon(QMessageBox.Critical)
                    self.dlg.setWindowTitle("Problém")
                    # self.dlg.setInformativeText('More information')
                    self.dlg.setText("Zpráva je moc dlouhá. Maxumum znaků je " + maxDelka)
                    self.dlg.exec()  

                if self.zprava == "" and self.modulace != "AM" and self.modulace != "FM": # Nevysílá se prázná zpráva
                    return

                allowed_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','(',')','$','%','_','/','[',']',' ',',','.']
                if any(x not in allowed_characters for x in zprava):
                    self.zprava = ""
                    self.dlg = QMessageBox(self.centralwidget)
                    self.dlg.setIcon(QMessageBox.Critical)
                    self.dlg.setWindowTitle("Problém")
                    # self.dlg.setInformativeText('More information')
                    self.dlg.setText("Nepovolený symbol! Diakritika a některé symboly jsou zakázané.")
                    self.dlg.exec()
                else:
                    self.zprava = ""
                    for i in zprava:
                        if i != '[' and i != ']':
                            self.zprava += i
                self.lEvlastniSekvence.setText(self.zprava)

                if self.zprava == "" and self.modulace != "AM" and self.modulace != "FM": # Nevysílá se prázná zpráva
                    return

            if self.modulace == "QAM" and self.nModulace == 2: # QAM n=2 není definováno
                self.dlg = QMessageBox(self.centralwidget)
                self.dlg.setIcon(QMessageBox.Critical)
                self.dlg.setWindowTitle("Problém")
                # self.dlg.setInformativeText('More information')
                self.dlg.setText("QAM je pouze definovaná pro 4 nebo 8 stavů!")
                self.dlg.exec()
                return

            #Výběr modulace
            if self.modulace == "AM": self.tx_samples = TxRxModul.AM(100e3,self.frekvenceMin,0.5,self.mSamples)
            if self.modulace == "FM": self.tx_samples = TxRxModul.FM(100e3,self.frekvenceMin,2,self.mSamples)
            if self.modulace == "ASK": self.tx_samples = TxRxModul.ASK(self.nModulace,self.zprava)
            if self.modulace == "FSK": self.tx_samples = TxRxModul.FSK(self.nModulace,self.zprava)
            if self.modulace == "PSK": self.tx_samples = TxRxModul.PSK(self.nModulace,self.zprava)
            if self.modulace == "QAM": self.tx_samples = TxRxModul.QAM(self.nModulace,self.zprava)

            try:
                self.sdr.tx_destroy_buffer()
                self.sdr.rx_destroy_buffer()
                self.sdr.tx_rf_bandwidth = int(self.sample_rate)
                self.sdr.tx_lo = int(self.center_freq)

                # Vysílání
                self.sdr.tx_cyclic_buffer = True # Povolení cyklického vysílání
                self.sdr.tx(self.tx_samples) # start vysílání
            except:
                self.dlg = QMessageBox(self.centralwidget)
                self.dlg.setIcon(QMessageBox.Critical)
                self.dlg.setWindowTitle("Problém")
                # self.dlg.setInformativeText('More information')
                self.dlg.setText("SDR není připojeno nebo se nelze připojit.")
                self.dlg.exec()
            else:
                self.tx = True
                self.pBstartVysilani.setStyleSheet("background-color: green") # Nastavení barvy tlačítka pro indikaci

    def cStopVysilani(self): # Zastaví vysílání
        try:
            # Vyprázdnění bufferů
            self.sdr.tx_destroy_buffer()
            self.sdr.rx_destroy_buffer()
        except:
            self.dlg = QMessageBox(self.centralwidget)
            self.dlg.setIcon(QMessageBox.Critical)
            self.dlg.setWindowTitle("Problém")
            # self.dlg.setInformativeText('More information')
            self.dlg.setText("SDR není připojeno nebo se nelze připojit.")
            self.dlg.exec()
        finally:
            self.tx = False
            self.pBstartVysilani.setStyleSheet("background-color: red") # Nastavení barvy tlačítka pro indikaci

    def cStartDemodulace(self): # Start demodulace
        if self.provoz: # Je možné demodulovat jen, když se přijímá
            # Inicializace
            self.demod = True
            self.pBstartPrijem.setStyleSheet("background-color: green") # Nastavení barvy tlačítka pro indikaci
            self.vyhodnoceni = []
            self.lEzachycenaSekv.setText("")
            self.text = ""
            self.kolik = 0
        else:
            self.dlg = QMessageBox(self.centralwidget)
            self.dlg.setIcon(QMessageBox.Critical)
            self.dlg.setWindowTitle("Problém")
            # self.dlg.setInformativeText('More information')
            self.dlg.setText("Příjem musí být zapnutý.")
            self.dlg.exec()

        if self.nDemodulace == 2 and self.demodulace == "QAM": # QAM není def pro n=2
            self.demod = False
            self.pBstartPrijem.setStyleSheet("background-color: red") # Nastavení barvy tlačítka pro indikaci
        
            self.dlg = QMessageBox(self.centralwidget)
            self.dlg.setIcon(QMessageBox.Critical)
            self.dlg.setWindowTitle("Problém")
            # self.dlg.setInformativeText('More information')
            self.dlg.setText("QAM je pouze definovaná pro 4 nebo 8 stavů!")
            self.dlg.exec()
    
    def cStopDemodulace(self): # Zastaví demodulaci
        self.demod = False
        self.pBstartPrijem.setStyleSheet("background-color: red") # Nastavení barvy tlačítka pro indikaci

    def cStop(self): # Zastaví příjem
        self.timer.stop() 
        self.provoz = False
        self.tx = False
        self.demod = False
        self.pBstartVysilani.setStyleSheet("background-color: red") # Nastavení barvy tlačítka pro indikaci
        self.pBstartPrijem.setStyleSheet("background-color: red") # Nastavení barvy tlačítka pro indikaci
        self.pBstart.setStyleSheet("background-color: red") # Nastavení barvy tlačítka pro indikaci
        # Zastavení vysílání
        try:
             # Vyprázdnění bufferů
            self.sdr.tx_destroy_buffer()
            self.sdr.rx_destroy_buffer()
        except:
            pass

    def cStart(self): # Start příjmu
        try:
            self.sdr = adi.Pluto("ip:192.168.2.1") # Vytvoří objekt SDR, ktelrý je přímo spojený s reálným SDR            
        except:
            self.dlg = QMessageBox(self.centralwidget)
            self.dlg.setIcon(QMessageBox.Critical)
            self.dlg.setWindowTitle("Problém")
            # self.dlg.setInformativeText('More information')
            self.dlg.setText("SDR není připojeno nebo se nelze připojit.")
            self.dlg.exec()
        else:
            """
            Inicializace a nastavení SDR
            """
            self.provoz = True
            self.sdr.sample_rate = int(self.sample_rate)
            self.sdr.rx_lo = int(self.center_freq)
            self.sdr.rx_rf_bandwidth = int(self.sample_rate)
            self.sdr.rx_buffer_size = self.num_samps
            self.sdr.gain_control_mode_chan0 = "slow_attack"
            self.sdr.rx_destroy_buffer() # Pro bezpečnost, pokud by tam něco bylo

            self.ZmenaZesileniPrijem()  
            self.timer.start()  
            self.pBstart.setStyleSheet("background-color: green") # Nastavení barvy tlačítka pro indikaci            
        
        # creating thread
        # self.t1 = threading.Thread(target=Vlakno)

    def Vlakno(self): # Pro výpočet FFT a waterfallu
        mag_samples, f1 = self.VypocetFFT(self.rx_samples, self.num_samps)
        
        # Předání proměnných do třídy
        self.x = f1
        self.y = mag_samples

        self.img_array = np.roll(self.img_array, 1, 0) # Posunutí o jedno
        self.img_array[-1:] = self.y # Odebrání jedné řady dat a nahrání nové řady

        # Nastavení widgetu waterfallu
        freq = np.arange(self.sample_rate / -2, self.sample_rate / 2, self.sample_rate / self.num_samps) + self.center_freq
        image_height = abs(0-20)
        image_width = abs(freq[0]-freq[-1])
        self.img.setRect(QtCore.QRectF(freq[0], 0., image_width, image_height))

    def ZobrazeniFFT(self): # Zobrazí FFT a waterfall     
        try:
            self.rx_samples = self.sdr.rx() # Vzorky v buffru
        except:
            self.dlg = QMessageBox(self.centralwidget)
            self.dlg.setIcon(QMessageBox.Critical)
            self.dlg.setWindowTitle("Problém")
            # self.dlg.setInformativeText('More information')
            self.dlg.setText("SDR není připojeno nebo se nelze připojit.")
            self.dlg.exec()
        else:
            if self.rBzobrazeni1.isChecked(): self.img.setImage(np.transpose(self.img_array), autoLevels=False)
            self.data_line.setData(self.x, self.y)  # Update zobrazení FFT
            
            # Vytvoření vlákna
            self.t1 = threading.Thread(target=self.Vlakno) # Vytvoření vlákna
            self.t1.start() # Odstartování vlákna pro výpočet a zobrazení výsledku

    def Zamek(self):
        """
        Co bude vidět na základě Vysílám? nebo Přijímám?
        """
        if self.cBprijem.isChecked():
            self.lEzachycenaSekv.setVisible(True)
            self.label2.setVisible(True)
            self.cBmodulaceVysilani.setVisible(False)
            self.pBjakModulace1.setVisible(True)
            self.cBmodulacePrijem.setVisible(True)
            self.cBnbitmodulacePrijem.setVisible(True)
            self.pBstartPrijem.setVisible(True)
            self.pBstopPrijem.setVisible(True)
        if self.cBvysilani.isChecked():
            self.lEvlastniSekvence.setVisible(True)
            self.label1.setVisible(True)
            self.rBgenSekv.setVisible(True)
            self.rBvlSekv.setVisible(True)
            self.rBrostSekv.setVisible(True)
            self.cBmodulaceVysilani.setVisible(True)
            self.pBjakModulace.setVisible(True)
            self.cBnbitmodulaceVysilani.setVisible(True)
            self.pBstartVysilani.setVisible(True)
            self.pBstopVysilani.setVisible(True)
            self.sBzesileniManualVysilani.setVisible(True)
            self.lVysilaniManual.setVisible(True)
            self.tWvlastniSignal.setVisible(True)    
        if not self.cBprijem.isChecked():
            self.lEzachycenaSekv.setVisible(False)
            self.label2.setVisible(False)
            self.cBmodulacePrijem.setVisible(False)
            self.pBjakModulace1.setVisible(False)
            self.cBnbitmodulacePrijem.setVisible(False)
            self.pBstartPrijem.setVisible(False)
            self.pBstopPrijem.setVisible(False)
        if not self.cBvysilani.isChecked():
            self.lEvlastniSekvence.setVisible(False)
            self.label1.setVisible(False)
            self.rBgenSekv.setVisible(False)
            self.rBvlSekv.setVisible(False)
            self.rBrostSekv.setVisible(False)
            self.cBmodulaceVysilani.setVisible(False)
            self.pBjakModulace.setVisible(False)
            self.cBnbitmodulaceVysilani.setVisible(False)
            self.pBstartVysilani.setVisible(False)
            self.pBstopVysilani.setVisible(False)
            self.sBzesileniManualVysilani.setVisible(False)
            self.lVysilaniManual.setVisible(False)
            self.tWvlastniSignal.setVisible(False)

        """
        Co budu vysílat?
        """
        if self.rBgenSekv.isChecked():
            self.lEvlastniSekvence.setEnabled(False)
        if self.rBvlSekv.isChecked():
            self.lEvlastniSekvence.setEnabled(True)
        if self.rBrostSekv.isChecked():
            self.lEvlastniSekvence.setEnabled(False)

        """
        Jaká modulace?
        """
        if self.cBmodulaceVysilani.currentText() == "AM":
            self.rBgenSekv.setEnabled(False)
            self.rBvlSekv.setEnabled(False)
            self.rBrostSekv.setEnabled(False)
            self.cBnbitmodulaceVysilani.setEnabled(False)
            self.lEvlastniSekvence.setEnabled(False)
            self.label1.setEnabled(False)
            self.tWvlastniSignal.setEnabled(True)
        if self.cBmodulaceVysilani.currentText() == "FM":
            self.rBgenSekv.setEnabled(False)
            self.rBvlSekv.setEnabled(False)
            self.rBrostSekv.setEnabled(False)
            self.cBnbitmodulaceVysilani.setEnabled(False)
            self.lEvlastniSekvence.setEnabled(False)
            self.label1.setEnabled(False)
            self.tWvlastniSignal.setEnabled(True)
        if self.cBmodulaceVysilani.currentText() == "ASK":
            self.rBgenSekv.setEnabled(True)
            self.rBvlSekv.setEnabled(True)
            self.rBrostSekv.setEnabled(True)
            self.cBnbitmodulaceVysilani.setEnabled(True)
            self.label1.setEnabled(True)
            self.tWvlastniSignal.setEnabled(False)
        if self.cBmodulaceVysilani.currentText() == "FSK":
            self.rBgenSekv.setEnabled(True)
            self.rBvlSekv.setEnabled(True)
            self.rBrostSekv.setEnabled(True)
            self.cBnbitmodulaceVysilani.setEnabled(True)
            self.label1.setEnabled(True)
            self.tWvlastniSignal.setEnabled(False)
        if self.cBmodulaceVysilani.currentText() == "PSK":
            self.rBgenSekv.setEnabled(True)
            self.rBvlSekv.setEnabled(True)
            self.rBrostSekv.setEnabled(True)
            self.cBnbitmodulaceVysilani.setEnabled(True)
            self.label1.setEnabled(True)
            self.tWvlastniSignal.setEnabled(False)
        if self.cBmodulaceVysilani.currentText() == "QAM":
            self.rBgenSekv.setEnabled(True)
            self.rBvlSekv.setEnabled(True)
            self.rBrostSekv.setEnabled(True)
            self.cBnbitmodulaceVysilani.setEnabled(True)
            self.label1.setEnabled(True)
            self.tWvlastniSignal.setEnabled(False)

        """
        Jaká demodulace?
        """
        if self.cBmodulacePrijem.currentText() == "AM": self.cBnbitmodulacePrijem.setEnabled(False)
        if self.cBmodulacePrijem.currentText() == "FM": self.cBnbitmodulacePrijem.setEnabled(False)
        if self.cBmodulacePrijem.currentText() == "ASK": self.cBnbitmodulacePrijem.setEnabled(True)
        if self.cBmodulacePrijem.currentText() == "FSK": self.cBnbitmodulacePrijem.setEnabled(True)
        if self.cBmodulacePrijem.currentText() == "PSK": self.cBnbitmodulacePrijem.setEnabled(True)
        if self.cBmodulacePrijem.currentText() == "QAM": self.cBnbitmodulacePrijem.setEnabled(True)

        """
        Zesileni prijem
        """
        if self.cBmzesileniPrijem.currentText() == "Manual":
            self.sBzesileniManualPrijem.setEnabled(True)
            self.lPrijemManual.setEnabled(True)
        else:
            self.sBzesileniManualPrijem.setEnabled(False)
            self.lPrijemManual.setEnabled(False)

   
    def setupUi(self, MainWindow):
        """Nastavení hlavního okna"""
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setMinimumSize(1600, 960)
        # MainWindow.setMaximumSize(QtCore.QSize(10000, 10000))
        MainWindow.showMaximized() # Okno mám maxilmální velikost (obrazovky)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        """Nastavení tl. Start"""
        self.pBstart = QtWidgets.QPushButton(self.centralwidget)
        self.pBstart.setGeometry(10, 100, 93, 28)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBstart.setFont(font)
        self.pBstart.setObjectName("pBstart")
        self.pBstart.setStyleSheet("background-color: red") # Nastavení barvy tlačítka pro indikaci
        self.pBstart.clicked.connect(self.cStart)
        """Vodorovné rozložení"""
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(10, 10, 521, 80)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        """Spin box v layout, 1 GHz"""
        self.sBGHz = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.sBGHz.setObjectName("sBGHz")
        self.sBGHz.setMaximum(6)
        self.sBGHz.valueChanged.connect(self.Prevod)
        self.horizontalLayout.addWidget(self.sBGHz)
        """Label GHz"""
        self.label_GHz = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_GHz.setFont(font)
        self.label_GHz.setObjectName("label_GHz")
        self.horizontalLayout.addWidget(self.label_GHz)
        """Spin box v layout, 100 MHz"""
        self.sBMHz3 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.sBMHz3.setObjectName("sBMHz3")
        self.sBMHz3.setMaximum(10)
        self.sBMHz3.setMinimum(-1)
        self.sBMHz3.valueChanged.connect(self.Prevod)
        self.horizontalLayout.addWidget(self.sBMHz3)
        """Spin box v layout, 10 MHz"""
        self.sBMHz2 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.sBMHz2.setObjectName("sBMHz2")
        self.sBMHz2.setMaximum(10)
        self.sBMHz2.setMinimum(-1)
        self.sBMHz2.setValue(7)
        self.sBMHz2.valueChanged.connect(self.Prevod)
        self.horizontalLayout.addWidget(self.sBMHz2)
        """Spin box v layout, 1 MHz"""
        self.sBMHz1 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.sBMHz1.setObjectName("sBMHz1")
        self.sBMHz1.setMaximum(10)
        self.sBMHz1.setMinimum(-1)
        self.sBMHz1.valueChanged.connect(self.Prevod)
        self.horizontalLayout.addWidget(self.sBMHz1)
        """Label MHz"""
        self.label_MHz = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_MHz.setFont(font)
        self.label_MHz.setObjectName("label_MHz")
        self.horizontalLayout.addWidget(self.label_MHz)
        """Spin box v layout, 100 kHz"""
        self.sBkHz3 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.sBkHz3.setObjectName("sBkHz3")
        self.sBkHz3.setMaximum(10)
        self.sBkHz3.setMinimum(-1)
        self.sBkHz3.valueChanged.connect(self.Prevod)
        self.horizontalLayout.addWidget(self.sBkHz3)
        """Spin box v layout, 10 kHz"""
        self.sBkHz2 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.sBkHz2.setObjectName("sBkHz2")
        self.sBkHz2.setMaximum(10)
        self.sBkHz2.setMinimum(-1)
        self.sBkHz2.valueChanged.connect(self.Prevod)
        self.horizontalLayout.addWidget(self.sBkHz2)
        """Spin box v layout, 1 kHz"""
        self.sBkHz1 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.sBkHz1.setObjectName("sBkHz1")
        self.sBkHz1.setMaximum(10)
        self.sBkHz1.setMinimum(-1)
        self.sBkHz1.valueChanged.connect(self.Prevod)
        self.horizontalLayout.addWidget(self.sBkHz1)
        """Label kHz"""
        self.label_kHz = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_kHz.setFont(font)
        self.label_kHz.setObjectName("label_kHz")
        self.horizontalLayout.addWidget(self.label_kHz)
        """tl Stop"""
        self.pBstop = QtWidgets.QPushButton(self.centralwidget)
        self.pBstop.setGeometry(110, 100, 93, 28)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBstop.setFont(font)
        self.pBstop.setObjectName("pBstop")
        # self.pBstop.clicked.connect(plot_widget)
        self.pBstop.clicked.connect(self.cStop)
        """ComboBox na výběr zesílení"""
        self.cBmzesileniPrijem = QtWidgets.QComboBox(self.centralwidget)
        self.cBmzesileniPrijem.setGeometry(245, 97, 150, 30)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cBmzesileniPrijem.setFont(font)
        self.cBmzesileniPrijem.setObjectName("cBmzesileniPrijem")
        self.cBmzesileniPrijem.addItems(["Slow attack", "Fast attack", "Manual"])
        self.cBmzesileniPrijem.currentIndexChanged.connect(self.Zamek)
        self.cBmzesileniPrijem.currentIndexChanged.connect(self.ZmenaZesileniPrijem)
        """Manuální zesílení"""
        self.sBzesileniManualPrijem = QtWidgets.QSpinBox(self.centralwidget)
        self.sBzesileniManualPrijem.setGeometry(400, 97, 50, 30)
        self.sBzesileniManualPrijem.setFont(font)
        self.sBzesileniManualPrijem.setObjectName("sBzesileniManualPrijem")
        self.sBzesileniManualPrijem.setMaximum(73)
        self.sBzesileniManualPrijem.setMinimum(0)
        self.sBzesileniManualPrijem.setValue(10)
        self.sBzesileniManualPrijem.valueChanged.connect(self.ZmenaZesileniPrijem_manual)
        """Manuální zesílení - label"""
        self.lPrijemManual = QtWidgets.QLabel(self.centralwidget)
        self.lPrijemManual.setGeometry(458, 101, 181, 21)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lPrijemManual.setFont(font)
        self.lPrijemManual.setObjectName("lPrijemManual")
        """ComboBox na výběr modulace při vysílání"""
        self.cBmodulaceVysilani = QtWidgets.QComboBox(self.centralwidget)
        self.cBmodulaceVysilani.setGeometry(10, 170, 80, 31)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cBmodulaceVysilani.setFont(font)
        self.cBmodulaceVysilani.setObjectName("cBmodulaceVysilani")
        self.cBmodulaceVysilani.addItems(["AM","FM","ASK","PSK","FSK","QAM"])
        self.cBmodulaceVysilani.currentIndexChanged.connect(self.Zamek)
        self.cBmodulaceVysilani.currentIndexChanged.connect(self.ZmenaModulaceVysilani)
        """Kolika úrovňová demodulace to je"""
        self.cBnbitmodulaceVysilani = QtWidgets.QComboBox(self.centralwidget)
        self.cBnbitmodulaceVysilani.setGeometry(QtCore.QRect(110, 170, 80, 31))
        self.cBnbitmodulaceVysilani.setFont(font)
        self.cBnbitmodulaceVysilani.setObjectName("cBnbitmodulaceVysilani")
        self.cBnbitmodulaceVysilani.addItems(["2","4","8"])
        self.cBnbitmodulaceVysilani.currentIndexChanged.connect(self.ZmenaRaduModulace)
        # self.cBnbitmodulace.currentIndexChanged.connect(Modulace)
        """tl jak funguji modulace"""
        self.pBjakModulace = QtWidgets.QPushButton(self.centralwidget)
        self.pBjakModulace.setGeometry(210, 170, 221, 31)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBjakModulace.setFont(font)
        self.pBjakModulace.setObjectName("pBjakModulace")
        self.pBjakModulace.clicked.connect(self.cJakFunguje)
        """FFT"""
        styles = {'color':'r', 'font-size':'20px'}

        self.graphWidget = pg.PlotWidget(self.centralwidget)
        self.graphWidget.setLabel('left', 'Výkon', units='dBmW', **styles)
        self.graphWidget.setGeometry(QtCore.QRect(525, 0, width-525, int(height/2)-50))
        self.graphWidget.setBackground('w')
        self.graphWidget.plotItem.setMouseEnabled(y=False) # Zakáže zoom
        self.graphWidget.plotItem.setMouseEnabled(x=False)
        self.graphWidget.setYRange(0, -120)
        self.graphWidget.setLabel('bottom', 'Frekvence', units='Hz')
        self.graphWidget.plotItem.setDownsampling(True)
        self.graphWidget.plotItem.showGrid(True,True)
        
        # Pro inicializaci
        self.x = list(range(int(69700e3),int(70300e3)))
        self.y = np.zeros(int(np.abs(69700e3-70300e3)))

        # Vytvoření data linku
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        """Timer 1"""
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.ZobrazeniFFT)
        self.timer.timeout.connect(self.ZobrazeniDemodulace)
        """Waterfall"""
        self.graphWidget2 = pg.PlotWidget(self.centralwidget)
        # self.graphWidget2.setAntialiasing(False)
        self.graphWidget2.setBackground('w')
        self.graphWidget2.setGeometry(QtCore.QRect(525, int(height/2)-50, width-525, int(height/2)-50))
        # self.data_line2 = self.graphWidget2.plot(self.x, self.y, pen=pen)

        self.img = pg.ImageItem()
        self.img.setAutoDownsample(True)
        self.graphWidget2.addItem(self.img)

        self.img_array = np.zeros((200, self.num_samps)) # Vytvoření matice, která se používá pro zobrazení

        # bipolar colormap
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        # Nastavení colormap
        self.img.setLookupTable(lut)
        self.img.setLevels([-120,-30])

        # správný scaling
        # self.img.setImage(np.transpose(self.img_array), autoLevels=False)
        self.img.setImage(np.transpose(self.img_array), autoLevels=False)
        freq = np.arange(self.sample_rate / -2, self.sample_rate / 2, self.sample_rate / self.num_samps) + self.center_freq
        image_height = abs(0-20)
        image_width = abs(freq[0]-freq[-1])
        self.img.setRect(QtCore.QRectF(freq[0], 0., image_width, image_height))

        self.graphWidget2.setLabel('bottom', 'Frekvence', units='Hz')
        self.graphWidget2.setLabel('left', 'Čas', units='s', **styles)
        # self.setLabel('left', 'Time', units='s')
        self.graphWidget2.invertY(True)
        """Vlastni modulační signál AM a FM"""
        self.graphWidget3 = pg.PlotWidget(self.centralwidget)
        self.graphWidget3.setLabel('left', 'A', **styles)
        self.graphWidget3.setGeometry(QtCore.QRect(525, int(height/2)-50, width-525, int(height/2)-50))
        self.graphWidget3.setBackground('w')
        self.graphWidget3.plotItem.setMouseEnabled(y=True) # Umožní zoom v ose
        self.graphWidget3.plotItem.setMouseEnabled(x=True)
        self.graphWidget3.setLabel('bottom', 'Time', units='s')

        # Vytvoření data linku
        self.data_line2 = self.graphWidget3.plot(self.x, self.y, pen=pen)
        pen = pg.mkPen(color=(0, 255, 0))
        self.data_line3 = self.graphWidget3.plot(self.x, self.y, pen=pen)
        """Vytvoření 2 vrstev"""
        self.layoutStacked = QStackedLayout()
        self.layoutStacked.addWidget(self.graphWidget2)
        self.layoutStacked.addWidget(self.graphWidget3)
        """Přijímám?"""
        self.cBprijem = QtWidgets.QCheckBox(self.centralwidget)
        self.cBprijem.setGeometry(10, 140, 81, 20)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cBprijem.setFont(font)
        self.cBprijem.setObjectName("cBprijem")
        self.cBprijem.clicked.connect(self.Zamek)
        """Vysílám?"""
        self.cBvysilani = QtWidgets.QCheckBox(self.centralwidget)
        self.cBvysilani.setGeometry(90, 140, 81, 20)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cBvysilani.setFont(font)
        self.cBvysilani.setObjectName("cBvysilani")
        self.cBvysilani.clicked.connect(self.Zamek)
        """Zadaní vlastní sekvence"""
        self.lEvlastniSekvence = QtWidgets.QLineEdit(self.centralwidget)
        self.lEvlastniSekvence.setGeometry(10, 350, 211, 22)
        self.lEvlastniSekvence.setFont(font)
        self.lEvlastniSekvence.setObjectName("lEvlastniSekvence")
        """Label: Zadej vysílanou sekvenci:"""
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(10, 320, 220, 21)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label1.setFont(font)
        self.label1.setMouseTracking(False)
        self.label1.setObjectName("label1")
        """Vygeneruj sekvenci"""
        self.rBgenSekv = QtWidgets.QRadioButton(self.centralwidget)
        self.rBgenSekv.setGeometry(10, 220, 220, 20)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBgenSekv.setFont(font)
        self.rBgenSekv.setObjectName("rBgenSekv")
        self.rBgenSekv.setChecked(True)
        self.rBgenSekv.clicked.connect(self.Zamek)
        self.rBgenSekv.clicked.connect(self.NahodnaSekvence)
        """Vlastní sekvence"""
        self.rBvlSekv = QtWidgets.QRadioButton(self.centralwidget)
        self.rBvlSekv.setGeometry(10, 250, 200, 20)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBvlSekv.setFont(font)
        self.rBvlSekv.setObjectName("rBvlSekv")
        self.rBvlSekv.clicked.connect(self.Zamek)
        """Rostoucí sekvence"""
        self.rBrostSekv = QtWidgets.QRadioButton(self.centralwidget)
        self.rBrostSekv.setGeometry(QtCore.QRect(10, 280, 240, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBrostSekv.setFont(font)
        self.rBrostSekv.setObjectName("rBrostSekv")
        self.rBrostSekv.setChecked(True)
        # self.sekvence_Group.addButton(self.rBrostSekv)
        # self.rBrostSekv.clicked.connect(Modulace)
        self.rBrostSekv.clicked.connect(self.Zamek)
        self.rBrostSekv.clicked.connect(self.RostouciSekvence)
        """tl. Start vysílání"""
        self.pBstartVysilani = QtWidgets.QPushButton(self.centralwidget)
        self.pBstartVysilani.setGeometry(10, 655, 93, 28)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBstartVysilani.setFont(font)
        self.pBstartVysilani.setObjectName("pBstartVysilani")
        self.pBstartVysilani.setStyleSheet("background-color: red")
        self.pBstartVysilani.clicked.connect(self.cStartVysilani)
        """tl Stop vysílání"""
        self.pBstopVysilani = QtWidgets.QPushButton(self.centralwidget)
        self.pBstopVysilani.setGeometry(110, 655, 93, 28)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBstopVysilani.setFont(font)
        self.pBstopVysilani.setObjectName("pBstopVysilani")
        self.pBstopVysilani.clicked.connect(self.cStopVysilani)
        """Manuální zesílení vysílání"""
        self.sBzesileniManualVysilani = QtWidgets.QSpinBox(self.centralwidget)
        self.sBzesileniManualVysilani.setGeometry(10, 390, 50, 25)
        self.sBzesileniManualVysilani.setFont(font)
        self.sBzesileniManualVysilani.setObjectName("sBzesileniManualVysilani")
        self.sBzesileniManualVysilani.setMaximum(0)
        self.sBzesileniManualVysilani.setMinimum(-60)
        self.sBzesileniManualVysilani.setValue(-30)
        self.sBzesileniManualVysilani.valueChanged.connect(self.ZmenaZesileniVysilani)
        """Manuální zesílení vysílání - label"""
        self.lVysilaniManual = QtWidgets.QLabel(self.centralwidget)
        self.lVysilaniManual.setGeometry(68, 392, 181, 21)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lVysilaniManual.setFont(font)
        self.lVysilaniManual.setObjectName("lVysilaniManual")
        """Tabulka na konfiguraci signálu pro AM a FM"""
        self.tWvlastniSignal = QTableWidget(self.centralwidget)
        self.tWvlastniSignal.setGeometry(10, 435, 400, 200)
        self.tWvlastniSignal.setObjectName("tWvlastniSignal")
        self.tWvlastniSignal.setRowCount(15)
        self.tWvlastniSignal.setColumnCount(3)
        self.tWvlastniSignal.setHorizontalHeaderLabels(["Frekvence [Hz]", "Amplituda", "Fáze [°]"])
        self.tWvlastniSignal.setItem(0,0, QTableWidgetItem(str(self.frekvenceMin)))
        self.tWvlastniSignal.setItem(0,1, QTableWidgetItem("1"))
        self.tWvlastniSignal.setItem(0,2, QTableWidgetItem("0"))
        self.tWvlastniSignal.currentCellChanged.connect(self.ZmenaVlastniSignal)
        """Vyber zobrazení 1"""
        self.rBzobrazeni1 = QtWidgets.QRadioButton(self.centralwidget)
        self.rBzobrazeni1.setGeometry(500, 530, 220, 20)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBzobrazeni1.setFont(font)
        self.rBzobrazeni1.setObjectName("rBzobrazeni1")
        self.rBzobrazeni1.setChecked(True)
        self.rBzobrazeni1.clicked.connect(self.AktivaveZobrazeni1)
        """Vyber zobrazení 2"""
        self.rBzobrazeni2 = QtWidgets.QRadioButton(self.centralwidget)
        self.rBzobrazeni2.setGeometry(500, 550, 220, 20)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBzobrazeni2.setFont(font)
        self.rBzobrazeni2.setObjectName("rBzobrazeni1")
        self.rBzobrazeni2.clicked.connect(self.AktivaveZobrazeni2)
        """ComboBox na výběr modulace při přijímání"""
        self.cBmodulacePrijem = QtWidgets.QComboBox(self.centralwidget)
        self.cBmodulacePrijem.setGeometry(10, 780, 80, 31)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cBmodulacePrijem.setFont(font)
        self.cBmodulacePrijem.setObjectName("cBmodulacePrijem")
        self.cBmodulacePrijem.addItems(["AM","FM","ASK","PSK","FSK","QAM"])
        self.cBmodulacePrijem.currentIndexChanged.connect(self.Zamek)
        self.cBmodulacePrijem.currentIndexChanged.connect(self.ZmenaDemodulacePrijem)
        """tl jak funguji modulace"""
        self.pBjakModulace1 = QtWidgets.QPushButton(self.centralwidget)
        self.pBjakModulace1.setGeometry(210, 780, 221, 31)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBjakModulace1.setFont(font)
        self.pBjakModulace1.setObjectName("pBjakModulace1")
        self.pBjakModulace1.clicked.connect(self.cJakFunguje)
        """Label: Příjatá sekvence:"""
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(10, 830, 181, 21)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label2.setFont(font)
        self.label2.setMouseTracking(False)
        self.label2.setObjectName("label2")
        """Pro zobrazení zachycené sekvence"""
        self.lEzachycenaSekv = QtWidgets.QLineEdit(self.centralwidget)
        self.lEzachycenaSekv.setGeometry(10, 860, 300, 22)
        self.lEzachycenaSekv.setFont(font)
        self.lEzachycenaSekv.setObjectName("lEzachycenaSekv")
        self.lEzachycenaSekv.setEnabled(False)
        """Kolika úrovňová demodulace to je"""
        self.cBnbitmodulacePrijem = QtWidgets.QComboBox(self.centralwidget)
        self.cBnbitmodulacePrijem.setGeometry(QtCore.QRect(110, 780, 80, 31))
        self.cBnbitmodulacePrijem.setFont(font)
        self.cBnbitmodulacePrijem.setObjectName("cBnbitmodulacePrijem")
        self.cBnbitmodulacePrijem.addItems(["2","4","8"])
        self.cBnbitmodulacePrijem.currentIndexChanged.connect(self.ZmenaRaduDemodulace)
        # self.cBnbitmodulace.currentIndexChanged.connect(Modulace)
        """tl. Start příjem"""
        self.pBstartPrijem = QtWidgets.QPushButton(self.centralwidget)
        self.pBstartPrijem.setGeometry(10, 900, 93, 28)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBstartPrijem.setFont(font)
        self.pBstartPrijem.setObjectName("pBstartPrijem")
        self.pBstartPrijem.setStyleSheet("background-color: red")
        self.pBstartPrijem.clicked.connect(self.cStartDemodulace)
        # self.pBstartVysilani.clicked.connect(cStart)
        """tl Stop příjem"""
        self.pBstopPrijem = QtWidgets.QPushButton(self.centralwidget)
        self.pBstopPrijem.setGeometry(110, 900, 93, 28)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBstopPrijem.setFont(font)
        self.pBstopPrijem.setObjectName("pBstopPrijem")
        self.pBstopPrijem.clicked.connect(self.cStopDemodulace)
        """Rozdělení RadioButton do skupin"""
        self.sekvence_layout = QButtonGroup()
        self.formatVysilani_layout = QButtonGroup()
        self.formatPrijimani_layout = QButtonGroup()
        self.sekvence_layout.addButton(self.rBvlSekv)
        self.sekvence_layout.addButton(self.rBgenSekv)
        self.sekvence_layout.addButton(self.rBrostSekv)
        """"""
        MainWindow.setCentralWidget(self.centralwidget)

        """
        Layout
        """
        outerLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        leftLayout_0 = QGridLayout()
        leftLayout_0.addWidget(self.sBGHz,0,0,1,1)
        leftLayout_0.addWidget(self.label_GHz,0,1,1,1)
        leftLayout_0.addWidget(self.sBMHz3,0,2,1,1)
        leftLayout_0.addWidget(self.sBMHz2,0,3,1,1)
        leftLayout_0.addWidget(self.sBMHz1,0,4,1,1)
        leftLayout_0.addWidget(self.label_MHz,0,5,1,1)
        leftLayout_0.addWidget(self.sBkHz3,0,6,1,1)
        leftLayout_0.addWidget(self.sBkHz2,0,7,1,1)
        leftLayout_0.addWidget(self.sBkHz1,0,8,1,1)
        leftLayout_0.addWidget(self.label_kHz,0,9,1,1)
        leftLayout.addLayout(leftLayout_0)
        leftLayout.addSpacing(20)
        leftLayout_11 = QGridLayout()
        leftLayout_11.addWidget(self.cBmzesileniPrijem,0,0,1,1)
        leftLayout_11.addWidget(self.sBzesileniManualPrijem,0,1,1,1)
        leftLayout_11.addWidget(self.lPrijemManual,0,2,1,1)
        leftLayout_11.setColumnStretch(3,1)
        leftLayout.addLayout(leftLayout_11)
        leftLayout.addSpacing(10)
        leftLayout_1 = QGridLayout()
        leftLayout_1.addWidget(self.pBstart,0,0,1,1)
        leftLayout_1.addWidget(self.pBstop,0,1,1,1)
        leftLayout.addLayout(leftLayout_1)
        leftLayout.addSpacing(10)
        leftLayout_2 = QGridLayout()
        leftLayout_2.addWidget(self.cBprijem,0,0,1,1)
        leftLayout_2.addWidget(self.cBvysilani,0,1,1,1)
        leftLayout_2.setColumnStretch(2,1)
        leftLayout_2.addWidget(self.rBzobrazeni1,0,4,1,1)
        leftLayout_2.addWidget(self.rBzobrazeni2,0,5,1,1)
        leftLayout.addLayout(leftLayout_2)
        leftLayout.addSpacing(20)
        leftLayout_3 = QGridLayout()
        leftLayout_3.addWidget(self.cBmodulaceVysilani,0,0,1,1)
        leftLayout_3.addWidget(self.cBnbitmodulaceVysilani,0,1,1,1)
        leftLayout_3.addWidget(self.pBjakModulace,0,2,1,1)
        leftLayout_3.setColumnStretch(3,1)
        leftLayout.addLayout(leftLayout_3)
        leftLayout.addSpacing(10)
        leftLayout.addWidget(self.rBgenSekv)
        leftLayout.addWidget(self.rBrostSekv)
        leftLayout.addWidget(self.rBvlSekv)
        leftLayout.addSpacing(5)
        leftLayout.addWidget(self.label1)
        leftLayout.addWidget(self.lEvlastniSekvence)
        leftLayout.addSpacing(5)
        leftLayout_4 = QGridLayout()
        leftLayout_4.addWidget(self.sBzesileniManualVysilani,0,0,1,1)
        leftLayout_4.addWidget(self.lVysilaniManual,0,1,1,1)
        leftLayout_4.setColumnStretch(2,1)
        leftLayout.addLayout(leftLayout_4)
        leftLayout.addSpacing(5)
        leftLayout.addWidget(self.tWvlastniSignal)
        leftLayout.addSpacing(5)
        leftLayout_5 = QGridLayout()
        leftLayout_5.addWidget(self.pBstartVysilani,0,0,1,1)
        leftLayout_5.addWidget(self.pBstopVysilani,0,1,1,1)
        leftLayout.addLayout(leftLayout_5)
        #leftLayout.addSpacing(50)
        leftLayout.addStretch(3)
        leftLayout_6 = QGridLayout()
        leftLayout_6.addWidget(self.cBmodulacePrijem,0,0,1,1)
        leftLayout_6.addWidget(self.cBnbitmodulacePrijem,0,1,1,1)
        leftLayout_6.addWidget(self.pBjakModulace1,0,2,1,1)
        leftLayout_6.setColumnStretch(3,1)
        leftLayout.addLayout(leftLayout_6)
        leftLayout.addWidget(self.label2)
        leftLayout.addWidget(self.lEzachycenaSekv)
        leftLayout_7 = QGridLayout()
        leftLayout_7.addWidget(self.pBstartPrijem,0,0,1,1)
        leftLayout_7.addWidget(self.pBstopPrijem,0,1,1,1)
        leftLayout.addLayout(leftLayout_7)
        
        #leftLayout.addSpacing(150)
        leftLayout.addStretch()


        rightLayout.addWidget(self.graphWidget)
        rightLayout.addWidget(self.graphWidget2)
        rightLayout.addWidget(self.graphWidget3)

        outerLayout.addLayout(leftLayout,1)
        outerLayout.addLayout(rightLayout,4)

        self.centralwidget.setLayout(outerLayout)

        """
        Inicializace
        """
        self.retranslateUi(MainWindow) # Dojde k nahrání textů a tool tipů
        self.ZmenaDemodulacePrijem()
        self.ZmenaModulaceVysilani()
        self.ZmenaRaduDemodulace()
        self.ZmenaRaduModulace()
        self.ZmenaVlastniSignal()
        self.ZmenaZesileniVysilani()
        self.Prevod()
        self.ZmenaVlastniSignal()
        self.Zamek() # Inicialitace toho, co má být vidět, a co ne
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
  

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PySDR"))
        self.pBstart.setToolTip(_translate("MainWindow", "<html><head/><body><p>Spustí příjem</p></body></html>"))
        self.pBstart.setText(_translate("MainWindow", "Start"))
        self.sBGHz.setToolTip(_translate("MainWindow", "<html><head/><body><p>Jednotky GHz; Přijímaná frekvence</p></body></html>"))
        self.label_GHz.setText(_translate("MainWindow", "GHz"))
        self.sBMHz3.setToolTip(_translate("MainWindow", "<html><head/><body><p>Stovky MHz; Přijímaná frekvence</p></body></html>"))
        self.sBMHz2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Desítky MHz; Přijímaná frekvence</p></body></html>"))
        self.sBMHz1.setToolTip(_translate("MainWindow", "<html><head/><body><p>Jednotky MHz; Přijímaná frekvence</p></body></html>"))
        self.label_MHz.setText(_translate("MainWindow", "MHz"))
        self.sBkHz3.setToolTip(_translate("MainWindow", "<html><head/><body><p>Stovky kHz; Přijímaná frekvence</p></body></html>"))
        self.sBkHz2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Desítky kHz; Přijímaná frekvence</p></body></html>"))
        self.sBkHz1.setToolTip(_translate("MainWindow", "<html><head/><body><p>Desítky kHz; Přijímaná frekvence</p></body></html>"))
        self.label_kHz.setText(_translate("MainWindow", "kHz"))
        self.pBstop.setToolTip(_translate("MainWindow", "<html><head/><body><p>Zastaví příjem</p></body></html>"))
        self.pBstop.setText(_translate("MainWindow", "Stop"))
        self.lPrijemManual.setText(_translate("MainWindow", "dB"))
        self.pBjakModulace.setToolTip(_translate("MainWindow", "<html><head/><body><p>Vysvětlí jak fungují všechny modulace.</p></body></html>"))
        self.pBjakModulace.setText(_translate("MainWindow", "Popis modulace"))
        self.tWvlastniSignal.setToolTip(_translate("MainWindow", "<html><head/><body><p>Tabulka, kam se zadávají parametry pro tvorbu vlastníhi modulačního signálu.</p></body></html>"))
        self.rBzobrazeni1.setToolTip(_translate("MainWindow", "<html><head/><body><p>Dolní zobrazení bude ukazovat waterfall</p></body></html>"))
        self.rBzobrazeni1.setToolTip(_translate("MainWindow", "<html><head/><body><p>Dolní zobrazení bude ukazovat výsledek návrhu vlastního modulačního signálu</p></body></html>"))
        self.pBjakModulace1.setToolTip(_translate("MainWindow", "<html><head/><body><p>Vysvětlí jak fungují všechny modulace.</p></body></html>"))
        self.pBjakModulace1.setText(_translate("MainWindow", "Popis modulace"))
        self.lVysilaniManual.setText(_translate("MainWindow", "dB"))
        self.cBprijem.setToolTip(_translate("MainWindow", "<html><head/><body><p>Po zaškrtnutí zobrazí nastavení příjmu signálu pro demodulaci.</p></body></html>"))
        self.cBprijem.setText(_translate("MainWindow", "Demod"))
        self.cBvysilani.setToolTip(_translate("MainWindow", "<html><head/><body><p>Po zaškrtnutí zobrazí nastavení vysílání a modulace.</p></body></html>"))
        self.cBvysilani.setText(_translate("MainWindow", "Vysílání"))
        self.label1.setText(_translate("MainWindow", "Zadej vysílanou sekvenci:"))
        self.rBgenSekv.setText(_translate("MainWindow", "Vygenerovat sekvenci"))
        self.rBgenSekv.setToolTip(_translate("MainWindow", "<html><head/><body><p>Umožní vygenerovat náhodnou sekvenci čísel</p></body></html>"))
        self.rBvlSekv.setToolTip(_translate("MainWindow", "<html><head/><body><p>Lze zadat vlastní číselnou sekvenci (čísla musí být z rozsahu modulace)</p></body></html>"))
        self.rBvlSekv.setText(_translate("MainWindow", "Vlastní sekvence"))
        self.rBrostSekv.setToolTip(_translate("MainWindow", "<html><head/><body><p>Všechny hodnoty, které aktuální verze modulace zvládne</p></body></html>"))
        self.rBrostSekv.setText(_translate("MainWindow", "Roustoucí sekvence"))      
        self.pBstartVysilani.setToolTip(_translate("MainWindow", "<html><head/><body><p>Spustí vysílání</p></body></html>"))
        self.pBstartVysilani.setText(_translate("MainWindow", "Start"))
        self.pBstopVysilani.setToolTip(_translate("MainWindow", "<html><head/><body><p>Zastaví vysílání</p></body></html>"))
        self.pBstopVysilani.setText(_translate("MainWindow", "Stop"))
        self.label2.setText(_translate("MainWindow", "Příjatá sekvence:"))
        self.pBstartPrijem.setToolTip(_translate("MainWindow", "<html><head/><body><p>Spustí demodulaci přijímaného signálu</p></body></html>"))
        self.pBstartPrijem.setText(_translate("MainWindow", "Start"))
        self.pBstopPrijem.setToolTip(_translate("MainWindow", "<html><head/><body><p>Zastaví demodulaci</p></body></html>"))
        self.pBstopPrijem.setText(_translate("MainWindow", "Stop"))
        self.cBmodulacePrijem.setToolTip(_translate("MainWindow", "<html><head/><body><p>Výběr demodulace</p></body></html>"))
        self.cBmodulaceVysilani.setToolTip(_translate("MainWindow", "<html><head/><body><p>Výměr modulace</p></body></html>"))
        self.cBnbitmodulacePrijem.setToolTip(_translate("MainWindow", "<html><head/><body><p>Řád demodulace</p></body></html>"))
        self.cBnbitmodulaceVysilani.setToolTip(_translate("MainWindow", "<html><head/><body><p>Řád modulace</p></body></html>"))
        self.cBmzesileniPrijem.setToolTip(_translate("MainWindow", "<html><head/><body><p>Varianty zesílení příjmu</p></body></html>"))
        self.sBzesileniManualPrijem.setToolTip(_translate("MainWindow", "<html><head/><body><p>Ruční nastavení zesílení příjmu</p></body></html>"))
        self.sBzesileniManualVysilani.setToolTip(_translate("MainWindow", "<html><head/><body><p>Nastavení zeslabení vysílání</p></body></html>"))
        self.lEvlastniSekvence.setToolTip(_translate("MainWindow", "<html><head/><body><p>Ukazuje aktuální sekvenci. Při tvorbě vlastní sekvence se píše sem.</p></body></html>"))
        self.lEzachycenaSekv.setToolTip(_translate("MainWindow", "<html><head/><body><p>Zobrazuje přijatou sekvenci v ASCII</p></body></html>"))



if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()
    width =  size.width()
    height = size.height()

    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())