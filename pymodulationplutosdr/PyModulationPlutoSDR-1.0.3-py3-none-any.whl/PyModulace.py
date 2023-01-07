import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QVBoxLayout, QWidget, QMessageBox, QGridLayout, QHBoxLayout
from PyQt5.QtCore import QObject, QThread, pyqtSignal

import TxRxModul


matplotlib.use('QT5Agg')

class Worker(QObject):
    finished = pyqtSignal() # Signál pro signalizaci skončení vláklna

    def AM(self, carrier_freq, modulater_freq, modulation_index, n, sample_rate):
        global N
        modulation_index = modulation_index/100
        N = n*5
        t = np.arange(N) / sample_rate

        """
        Komlexní zápis
        """
        # cosModulacni = np.cos(modulater_freq * xRadians) + 1j * np.sin(modulater_freq * xRadians)
        # cosNosna = np.cos(carrier_freq * xRadians) + 1j * np.sin(carrier_freq * xRadians)
        # samples = A_c * (1 + modulation_index * cosModulacni) * cosNosna
        """
        Normální zápis
        """
        global samples, cosNosna, cosModulacni
        cosModulacni = np.cos(modulater_freq * 2 * np.pi * t)
        cosNosna = np.cos(carrier_freq * 2 * np.pi * t)
        # samples = A_c * (1 + modulation_index * cosModulacni) * cosNosna
        samples = modulation_index * cosModulacni * cosNosna + cosNosna
        
        samples = TxRxModul.NormovaniAbs(samples)
        cosModulacni = TxRxModul.NormovaniAbs(cosModulacni)
        cosNosna = TxRxModul.NormovaniAbs(cosNosna)

        self.finished.emit() # Vyslání signálu o skončení vlákna

    def FM(self, carrier_freq, modulater_freq, D_f, n, sample_rate):
        global N
        D_f = D_f/10
        N = n*5
        t = np.arange(N) / sample_rate  # Diskrétní čas

        global samples, cosNosna, cosModulacni

        cosNosna = np.cos(2*np.pi*carrier_freq*t)
        cosModulacni = np.cos(2*np.pi*modulater_freq*t)  # Vysílaná zpráva
        samples = np.cos(2*np.pi*carrier_freq*t + D_f*np.sin(2*np.pi*modulater_freq*t))
        
        self.finished.emit() # Vyslání signálu o skončení vlákna

    def NahodSymboly(self, n, pocet) -> int: # Vygeneruje nahodný symboly
        symboly = np.random.randint(0, n, pocet)  # 0 to n-1
        return symboly

    def IQnaReal(self, samples, N, t, f): # Z IQ složek vytvoří reálný signál
        ampl = np.sqrt(np.real(samples)**2 + np.imag(samples)**2)
        I = np.real(samples)
        Q = np.imag(samples)
        
        if len(t) == len(ampl): 
            out = I*np.cos(2*np.pi*f*t) + Q*np.sin(2*np.pi*f*t)
            return out
        pass

    def PokracovaniASK(self,x,n,k): #Vypočítává hodnoty zesílení pro 4-ASK a větší
        x = x-2 # Snížení na rozsah 0 - 1
        if x <= 1:
            y = (x - 0.5) * (k+2)
        else:
            k = k+2
            y = self.PokracovaniASK(x,n,k)                    
        return y

    def ASK(self, n, opakovani, polorovina, sekvence, carrier_freq, sample_rate, x):
        global samples, out, xIntText

        """
        Výběr tvorby sekvence
        """
        if sekvence == 0: 
            xInt = self.NahodSymboly(n,2*n) # Počet čísel 2x větší než je řád, aby se zabezpečil dostatečný rozsah hodnot
            delka = 2 * n * opakovani # Délka generovaného signálu
        if sekvence == 1:
            xInt = np.arange(0,n)
            delka = n * opakovani # Délka generovaného signálu  
        if sekvence == 2:                 
            xInt = x
            delka = len(xInt) * opakovani # Délka generovaného signálu

        """
        Výběr poloroviny
        """
        if polorovina == "Celá rovina": polorovina = 0
        if polorovina == "Pravá polorovina": polorovina = 1
        if polorovina == "Levá polorovina": polorovina = 2

        """
        Generování amplitud
        """
        xAmp = np.zeros(len(xInt), dtype=np.float64)
        if polorovina == 0: # Podle toho jaká se používá polorovina se vypočítají apmlitudy pro symboly
            for i in np.arange(len(xInt)):
                if xInt[i] <= 1: # Vypočte aplitudu pro čísla 0 a 1
                    xAmp[i] = (xInt[i] - 0.5) * 2
                else: # Vypočte aplitudu pro čísla 2 a více
                    k = 2
                    xAmp[i] = self.PokracovaniASK(xInt[i],n,k) # Rekurzivní výpočet aplitud pro symboly
        elif polorovina == 1:
            xAmp = xInt / (n - 1) + 0.5
        elif polorovina == 2:
            xAmp = xInt / (n - 1) - 1.5
        xSymbols = xAmp * (np.cos(0) + 1j * np.sin(0))  # Vytvočení komplexních čísel
        samples = np.repeat(xSymbols, opakovani)
        out = self.IQnaReal(samples,len(samples), np.arange(delka) / sample_rate, carrier_freq)

        xIntText = str(xInt)
        xIntText = xIntText.replace("[", "")
        xIntText = xIntText.replace("]", "")
        self.finished.emit() # Vyslání signálu o skončení vlákna

    def PSK(self, n, opakovani, sekvence, carrier_freq, sample_rate, x):
        global samples, out, xIntText

        """
        Výběr tvorby sekvence
        """
        if sekvence == 0: 
            xInt = self.NahodSymboly(n,2*n) # Počet čísel 2x větší než je řád, aby se zabezpečil dostatečný rozsah hodnot
            delka = 2 * n * opakovani # Délka generovaného signálu
        if sekvence == 1:
            xInt = np.arange(0,n)
            delka = n * opakovani # Délka generovaného signálu  
        if sekvence == 2:                 
            xInt = x
            delka = len(xInt) * opakovani # Délka generovaného signálu
        
        if n == 4:
            xDegrees = xInt * 360 / 4.0 + 45  # 45, 135, 225, 315 stupňů
        else:
            xDegrees = xInt * 360 / n
        xRadians = xDegrees * np.pi / 180.0  # převod na radiany
        if n == 2:
            xSymbols = np.cos(xRadians) + 1j * np.floor(np.sin(xRadians))  # vytvoří komplexní symbol
        else:
            xSymbols = np.cos(xRadians) + 1j * np.sin(xRadians)  # Vytvoří komplexní symbol
        samples = np.repeat(xSymbols, opakovani) 
        out = self.IQnaReal(samples,len(samples), np.arange(delka) / sample_rate, carrier_freq)

        xIntText = str(xInt)
        xIntText = xIntText.replace("[", "")
        xIntText = xIntText.replace("]", "")
        self.finished.emit() # Vyslání signálu o skončení vlákna

    def QAM(self, n, opakovani, sekvence, carrier_freq, sample_rate, x):  # jen do 32b
        global samples, out, xIntText
        
        """
        Výběr tvorby sekvence
        """
        if sekvence == 0: 
            xInt = self.NahodSymboly(n,2*n) # Počet čísel 2x větší než je řád, aby se zabezpečil dostatečný rozsah hodnot
            delka = 2 * n * opakovani # Délka generovaného signálu
        if sekvence == 1:
            xInt = np.arange(0,n)
            delka = n * opakovani # Délka generovaného signálu  
        if sekvence == 2:                 
            xInt = x
            delka = len(xInt) * opakovani # Délka generovaného signálu
        
        xSymbols = np.zeros(len(xInt), dtype=complex)                
        match n:
            case 4:
                i = 0
                for a in xInt:
                    match a:
                        case 0:
                            xSymbols[i] = 1 + 1j
                        case 1:
                            xSymbols[i] = -1 + 1j
                        case 2:
                            xSymbols[i] = -1 - 1j
                        case 3:
                            xSymbols[i] = 1 - 1j
                    i += 1
            case 8:
                i = 0
                for a in xInt:
                    match a:
                        case 0:
                            xSymbols[i] = 1 + 1j
                        case 1:
                            xSymbols[i] = -1 + 1j
                        case 2:
                            xSymbols[i] = -1 - 1j
                        case 3:
                            xSymbols[i] = 1 - 1j
                        case 4:
                            xSymbols[i] = 3 + 3j
                        case 5:
                            xSymbols[i] = -3 + 3j
                        case 6:
                            xSymbols[i] = -3 - 3j
                        case 7:
                            xSymbols[i] = 3 - 3j
                    i += 1
            case 16:
                i = 0
                for a in xInt:
                    match a:
                        case 0:
                            xSymbols[i] = 1 + 1j
                        case 1:
                            xSymbols[i] = -1 + 1j
                        case 2:
                            xSymbols[i] = -1 - 1j
                        case 3:
                            xSymbols[i] = 1 - 1j
                        case 4:
                            xSymbols[i] = 3 + 1j
                        case 5:
                            xSymbols[i] = 3 + 3j
                        case 6:
                            xSymbols[i] = 1 + 3j
                        case 7:
                            xSymbols[i] = -1 + 3j
                        case 8:
                            xSymbols[i] = -3 + 3j
                        case 9:
                            xSymbols[i] = -3 + 1j
                        case 10:
                            xSymbols[i] = -3 - 1j
                        case 11:
                            xSymbols[i] = -3 - 3j
                        case 12:
                            xSymbols[i] = -1 - 3j
                        case 13:
                            xSymbols[i] = 1 - 3j
                        case 14:
                            xSymbols[i] = 3 - 3j
                        case 15:
                            xSymbols[i] = 3 - 1j
                    i += 1
            case 32:
                i = 0
                for a in xInt:
                    match a:
                        case 0:
                            xSymbols[i] = 1 + 1j
                        case 1:
                            xSymbols[i] = -1 + 1j
                        case 2:
                            xSymbols[i] = -1 - 1j
                        case 3:
                            xSymbols[i] = 1 - 1j
                        case 4:
                            xSymbols[i] = 3 + 1j
                        case 5:
                            xSymbols[i] = 3 + 3j
                        case 6:
                            xSymbols[i] = 1 + 3j
                        case 7:
                            xSymbols[i] = -1 + 3j
                        case 8:
                            xSymbols[i] = -3 + 3j
                        case 9:
                            xSymbols[i] = -3 + 1j
                        case 10:
                            xSymbols[i] = -3 - 1j
                        case 11:
                            xSymbols[i] = -3 - 3j
                        case 12:
                            xSymbols[i] = -1 - 3j
                        case 13:
                            xSymbols[i] = 1 - 3j
                        case 14:
                            xSymbols[i] = 3 - 3j
                        case 15:
                            xSymbols[i] = 3 - 1j
                        case 16:
                            xSymbols[i] = 5 + 1j
                        case 17:
                            xSymbols[i] = 5 + 3j
                        case 18:
                            xSymbols[i] = 3 + 5j
                        case 19:
                            xSymbols[i] = 1 + 5j
                        case 20:
                            xSymbols[i] = -1 + 5j
                        case 21:
                            xSymbols[i] = -3 + 5j
                        case 22:
                            xSymbols[i] = -5 + 3j
                        case 23:
                            xSymbols[i] = -5 + 1j
                        case 24:
                            xSymbols[i] = -5 - 1j
                        case 25:
                            xSymbols[i] = -5 - 3j
                        case 26:
                            xSymbols[i] = -3 - 5j
                        case 27:
                            xSymbols[i] = -1 - 1j
                        case 28:
                            xSymbols[i] = 1 - 5j
                        case 29:
                            xSymbols[i] = 3 - 5j
                        case 30:
                            xSymbols[i] = 5 - 3j
                        case 31:
                            xSymbols[i] = 5 - 1j
                    i += 1

        samples = np.repeat(xSymbols, opakovani)  # Z impulzu na pulz o délce opakování
        out = self.IQnaReal(samples,len(samples), np.arange(delka) / sample_rate, carrier_freq)

        xIntText = str(xInt)
        xIntText = xIntText.replace("[", "")
        xIntText = xIntText.replace("]", "")
        self.finished.emit() # Vyslání signálu o skončení vlákna

    def FSK(self, n, opakovani, sekvence, carrier_freq, sample_rate, x, Delta_f): # Podívat se i na předlohu - podle mě to uplně nefunguje
        global samples, out, xIntText, N         
        
        """
        Výběr tvorby sekvence
        """
        if sekvence == 0: 
            xInt_n = self.NahodSymboly(n,2*n) # Počet čísel 2x větší než je řád, aby se zabezpečil dostatečný rozsah hodnot
            delka = 2 * n * opakovani # Délka generovaného signálu
        if sekvence == 1:
            xInt_n = np.arange(0,n)
            delka = n * opakovani # Délka generovaného signálu  
        if sekvence == 2:                 
            xInt_n = x
            delka = len(xInt_n) * opakovani # Délka generovaného signálu
        t = np.arange(delka) / sample_rate  # Diskrétní čas

        xInt = np.repeat(xInt_n, opakovani)

        f = (carrier_freq + Delta_f * xInt - (n * Delta_f)/2) + Delta_f/2
        #f = carrier_freq + D_f * carrier_freq * xInt / 2 # Frekvence pro každý symbol
        # xSymbols = np.cos(2 * np.pi * f * t) + 1j*np.sin(2 * np.pi * f * t)
        #samples = np.repeat(xSymbols, opakovani)
        #samples = xSymbols
        delta_phi = f * np.pi / (sample_rate / 2.0)
        phi = np.cumsum(delta_phi)
        samples = np.cos(2*np.pi*carrier_freq*t + phi) + 1j * np.sin(2*np.pi*carrier_freq*t + phi)
        out = self.IQnaReal(samples,len(samples), np.arange(delka) / sample_rate, carrier_freq)

        N = len(samples)
        xIntText = str(xInt_n)
        xIntText = xIntText.replace("[", "")
        xIntText = xIntText.replace("]", "")
        self.finished.emit() # Vyslání signálu o skončení vlákna

class Ui_ModulaceWindow(object):
    """
    Inicializace
    """
    # Proměnné
    opakovani = 200
    sample_rate = 15000  # Hz

    # Objekty
    thread = QThread()

    def ZmenaPoctuVzorkuNaSymbol(self): # Změní počet vzorků na symbol
        if self.cBmodulace.currentText() != "FM" and self.cBmodulace.currentText() != "AM": # Neplatí to pro AM a FM
            self.opakovani = self.sBOpakovani.value()

    def NahodSymboly(self, n, pocet) -> int: # Vygeneruje nahodný symboly
        symboly = np.random.randint(0, n, pocet)  # 0 to n-1
        return symboly

    def IQnaReal(self, samples, N, t): # Převede IQ složky na reálný signál
        ampl = np.sqrt(np.real(samples)**2 + np.imag(samples)**2)
        f = self.hSfrekNosne.value()
        I = np.real(samples)
        Q = np.imag(samples)
        
        if len(t) == len(ampl): 
            out = I*np.cos(2*np.pi*f*t) + Q*np.sin(2*np.pi*f*t)
            return out
        pass

    def Zamek(self): # Rozhoduje o tom jaký prvek lze používat
        if self.cBmodulace.currentText() == "AM":
            self.hSfrekNosne.setEnabled(True) 
            self.hSfrekSign.setEnabled(True)
            self.sBfrekNosne.setEnabled(True)
            self.sBfrekSign.setEnabled(True)
            self.rBgenSekv.setEnabled(False)
            self.rBvlSekv.setEnabled(False)
            self.rBrostSekv.setEnabled(False)
            self.lEvlastniSekvence.setEnabled(False)
            self.cBnbitmodulace.setEnabled(False)
            self.cBpolorovina.setEnabled(False)
            self.sBpromodulovanost.setEnabled(True)
            self.sBpromodulovanost.setMaximum(200)
            self.sBpromodulovanost.setValue(80)
            self.rBzobrazeni1.setEnabled(False)
            self.rBzobrazeni2.setEnabled(False)
            self.label6.setText("Promodulovanost [%]:")
            self.lOpakovani.setText("Počet vzorků")
            self.sBOpakovani.setMinimum(100)
            self.sBOpakovani.setMaximum(2000)
            self.sBOpakovani.setValue(1000)
            self.sBOpakovani.setSingleStep(10)
        if self.cBmodulace.currentText() == "FM":
            self.hSfrekNosne.setEnabled(True) 
            self.hSfrekSign.setEnabled(True)
            self.sBfrekNosne.setEnabled(True)
            self.sBfrekSign.setEnabled(True)
            self.rBgenSekv.setEnabled(False)
            self.rBvlSekv.setEnabled(False)
            self.rBrostSekv.setEnabled(False)
            self.lEvlastniSekvence.setEnabled(False)
            self.cBnbitmodulace.setEnabled(False)
            self.cBpolorovina.setEnabled(False)
            self.sBpromodulovanost.setEnabled(True)
            self.sBpromodulovanost.setMaximum(20)
            self.sBpromodulovanost.setValue(1)
            self.rBzobrazeni1.setEnabled(False)
            self.rBzobrazeni2.setEnabled(False)
            self.label6.setText("Index modulace: [/10]")
            self.lOpakovani.setText("Počet vzorků")
            self.sBOpakovani.setMinimum(100)
            self.sBOpakovani.setMaximum(2000)
            self.sBOpakovani.setValue(1000)
            self.sBOpakovani.setSingleStep(10)
        if self.cBmodulace.currentText() == "ASK":
            self.hSfrekNosne.setEnabled(True) 
            self.hSfrekSign.setEnabled(False)
            self.sBfrekNosne.setEnabled(True)
            self.sBfrekSign.setEnabled(False)
            self.rBgenSekv.setEnabled(True)
            self.rBvlSekv.setEnabled(True)
            self.rBrostSekv.setEnabled(True)
            if self.rBgenSekv.isChecked(): self.lEvlastniSekvence.setEnabled(False)
            if self.rBvlSekv.isChecked(): self.lEvlastniSekvence.setEnabled(True)
            if self.rBrostSekv.isChecked(): self.lEvlastniSekvence.setEnabled(False)
            self.cBnbitmodulace.setEnabled(True)
            self.cBpolorovina.setEnabled(True)
            self.sBpromodulovanost.setEnabled(False)
            self.rBzobrazeni1.setEnabled(True)
            self.rBzobrazeni2.setEnabled(True)
            self.lOpakovani.setText("Počet vzorků na symbol")
            self.sBOpakovani.setMinimum(1)
            self.sBOpakovani.setMaximum(500)
            self.sBOpakovani.setValue(self.opakovani)
            self.sBOpakovani.setSingleStep(10)
        if self.cBmodulace.currentText() == "FSK":
            self.hSfrekNosne.setEnabled(True) 
            self.hSfrekSign.setEnabled(False)
            self.sBfrekNosne.setEnabled(True)
            self.sBfrekSign.setEnabled(False)
            self.rBgenSekv.setEnabled(True)
            self.rBvlSekv.setEnabled(True)
            self.rBrostSekv.setEnabled(True)
            if self.rBgenSekv.isChecked(): self.lEvlastniSekvence.setEnabled(False)
            if self.rBvlSekv.isChecked(): self.lEvlastniSekvence.setEnabled(True)
            if self.rBrostSekv.isChecked(): self.lEvlastniSekvence.setEnabled(False)
            self.cBnbitmodulace.setEnabled(True)
            self.cBpolorovina.setEnabled(False)
            self.sBpromodulovanost.setMaximum(2000)
            self.sBpromodulovanost.setValue(200)
            self.rBzobrazeni1.setEnabled(True)
            self.rBzobrazeni2.setEnabled(True)
            self.label6.setText("Rozdíl frekvencí [Hz]:")
            self.sBpromodulovanost.setEnabled(True)
            self.lOpakovani.setText("Počet vzorků na symbol")
            self.sBOpakovani.setMinimum(1)
            self.sBOpakovani.setMaximum(500)
            self.sBOpakovani.setValue(self.opakovani)
            self.sBOpakovani.setSingleStep(10)
        if self.cBmodulace.currentText() == "PSK":
            self.hSfrekNosne.setEnabled(True) 
            self.hSfrekSign.setEnabled(False)
            self.sBfrekNosne.setEnabled(True)
            self.sBfrekSign.setEnabled(False)
            self.rBgenSekv.setEnabled(True)
            self.rBvlSekv.setEnabled(True)
            self.rBrostSekv.setEnabled(True)
            if self.rBgenSekv.isChecked(): self.lEvlastniSekvence.setEnabled(False)
            if self.rBvlSekv.isChecked(): self.lEvlastniSekvence.setEnabled(True)
            if self.rBrostSekv.isChecked(): self.lEvlastniSekvence.setEnabled(False)
            self.cBnbitmodulace.setEnabled(True)
            self.cBpolorovina.setEnabled(False)
            self.sBpromodulovanost.setEnabled(False)
            self.lOpakovani.setText("Počet vzorků na symbol")
            self.rBzobrazeni1.setEnabled(True)
            self.rBzobrazeni2.setEnabled(True)
            self.sBOpakovani.setMinimum(1)
            self.sBOpakovani.setMaximum(500)
            self.sBOpakovani.setValue(self.opakovani)
            self.sBOpakovani.setSingleStep(10)
        if self.cBmodulace.currentText() == "QAM":
            self.hSfrekNosne.setEnabled(True) 
            self.hSfrekSign.setEnabled(False)
            self.sBfrekNosne.setEnabled(True)
            self.sBfrekSign.setEnabled(False)
            self.rBgenSekv.setEnabled(True)
            self.rBvlSekv.setEnabled(True)
            self.rBrostSekv.setEnabled(True)
            if self.rBgenSekv.isChecked(): self.lEvlastniSekvence.setEnabled(False)
            if self.rBvlSekv.isChecked(): self.lEvlastniSekvence.setEnabled(True)
            if self.rBrostSekv.isChecked(): self.lEvlastniSekvence.setEnabled(False)
            self.cBnbitmodulace.setEnabled(True)
            self.cBpolorovina.setEnabled(False)
            self.sBpromodulovanost.setEnabled(False)
            self.lOpakovani.setText("Počet vzorků na symbol")
            self.rBzobrazeni1.setEnabled(True)
            self.rBzobrazeni2.setEnabled(True)
            self.sBOpakovani.setMinimum(1)
            self.sBOpakovani.setMaximum(500)
            self.sBOpakovani.setValue(self.opakovani)
            self.sBOpakovani.setSingleStep(10)

    def Obnoveni(self): # Propojení SpinBoxů a Sliderů
        sender = self.sBfrekNosne.sender()
        name = sender.objectName()
        if name == "hSfrekSign": self.sBfrekSign.setValue(self.hSfrekSign.value())
        if name == "sBfrekSign": self.hSfrekSign.setValue(self.sBfrekSign.value())
        if name == "hSfrekNosne": self.sBfrekNosne.setValue(self.hSfrekNosne.value())
        if name == "sBfrekNosne": self.hSfrekNosne.setValue(self.sBfrekNosne.value())
        if name == "hSfrekVzork": self.sBfrekVzork.setValue(self.hSfrekVzork.value())
        if name == "sBfrekVzork": self.hSfrekVzork.setValue(self.sBfrekVzork.value())

        self.sample_rate = self.hSfrekVzork.value()

    # def Zobrazeni(self, samples, out, xIntText):
    def Zobrazeni(self): # Zobrazení signálů pro digitální modulace s vyjímkou FSK
        plt.ioff()
        """
        IQ složky
        """
        if self.rBzobrazeni1.isChecked():
            self.matplotwidget.axis.clear()
            self.matplotwidget.axis.plot(np.real(samples),'.-')
            self.matplotwidget.axis.plot(np.imag(samples),'.-')
            self.matplotwidget.axis.grid(True)
            self.matplotwidget.axis.legend(["I","Q"])
            self.matplotwidget.axis.set_xlabel('Vzorky')
            self.matplotwidget.axis.set_ylabel('Amplituda')
            self.matplotwidget.canvas.draw()
            self.matplotwidget.canvas.flush_events()

        """
        Reálný signál
        """
        if self.rBzobrazeni2.isChecked(): 
            self.matplotwidget.axis.clear()
            self.matplotwidget.axis.plot(out,'.-')
            self.matplotwidget.axis.grid(True)
            self.matplotwidget.axis.set_xlabel('Vzorky')
            self.matplotwidget.axis.set_ylabel('Amplituda')
            self.matplotwidget.canvas.draw()
            self.matplotwidget.canvas.flush_events()

        """
        Konstelační diagram
        """
        self.matplotwidget.axis2.clear()
        self.matplotwidget.axis2.plot(np.real(samples), np.imag(samples), '.') # Zobrazení konstelačního diagramu
        self.matplotwidget.axis2.grid(True)
        self.matplotwidget.axis2.set_xlabel('I')
        self.matplotwidget.axis2.set_ylabel('Q')
        # self.matplotwidget2.axis.set_xlim([-1.1,1.1])
        # self.matplotwidget2.axis.set_ylim([-1.1,1.1])
        self.matplotwidget.canvas.draw()
        self.matplotwidget.canvas.flush_events()

        self.lEvlastniSekvence.setText(xIntText)

    # def ZobrazeniAnal(self, samples,cosModulacni,cosNosna,N):
    def ZobrazeniAnal(self): # Zobrazení pro analogové modulace
        plt.ioff()
        """
        Signály
        """
        self.matplotwidget.axis.clear()
        # self.matplotwidget.axis.plot(np.real(samples)) 
        # self.matplotwidget.axis.plot(samples) 
        # self.matplotwidget.axis.plot(np.imag(samples)) 
        self.matplotwidget.axis.plot(np.real(cosModulacni[0:int(N/5)]))
        self.matplotwidget.axis.plot(np.real(cosNosna[0:int(N/5)]))
        self.matplotwidget.axis.plot(np.real(samples[0:int(N/5)])+np.imag(samples[0:int(N/5)]), linewidth=3) 
        self.matplotwidget.axis.grid(True)
        self.matplotwidget.axis.legend(["Modulační signál","Nosná","Modulovaný signál"])
        self.matplotwidget.axis.set_xlabel('Vzorky')
        self.matplotwidget.axis.set_ylabel('Amplituda')
        self.matplotwidget.canvas.draw()
        self.matplotwidget.canvas.flush_events()

        """
        Frekvenční spektrum
        """
        # Výpočet FFT
        mag_samples, f1, L1 = TxRxModul.ProZobrazeniFFT(samples, N, self.sample_rate)
        mag_modulater, f2, L2 = TxRxModul.ProZobrazeniFFT(cosModulacni, N, self.sample_rate)
        mag_carrier, f3, L3 = TxRxModul.ProZobrazeniFFT(cosNosna, N, self.sample_rate)

        # Zobrazení FFT
        self.matplotwidget.axis2.clear()
        #self.matplotwidget2.axis.plot(f1[L1],mag_samples[L1],'.-')
        #self.matplotwidget2.axis.plot(f2[L2],mag_modulater[L2],'.-')
        #self.matplotwidget2.axis.plot(f3[L3],mag_carrier[L3],'.-')
        self.matplotwidget.axis2.plot(f2,np.real(mag_modulater),'.-')
        self.matplotwidget.axis2.plot(f3,np.real(mag_carrier),'.-')
        self.matplotwidget.axis2.plot(f1,np.real(mag_samples),'.-', linewidth=3)
        self.matplotwidget.axis2.grid(True)
        self.matplotwidget.axis2.legend(["Modulační signál","Nosná","Modulovaný signál"])
        self.matplotwidget.axis2.set_xlabel('Frekvence [Hz]')
        self.matplotwidget.axis2.set_ylabel('Výkon [dB]')
        #self.matplotwidget2.axis.set_xlim([0,2500])
        self.matplotwidget.canvas.draw()
        self.matplotwidget.canvas.flush_events()

    # def ZobrazeniFSK(self, out, N, xIntText)
    def ZobrazeniFSK(self): # Pro zobrazení signálů FSK
        plt.ioff()
        
        """
        IQ složky
        """
        if self.rBzobrazeni1.isChecked():
            self.matplotwidget.axis.clear()
            self.matplotwidget.axis.plot(np.real(samples),'.-') # Zobrazení I a Q složky
            self.matplotwidget.axis.plot(np.imag(samples),'.-')
            self.matplotwidget.axis.grid(True)
            self.matplotwidget.axis.legend(["I","Q"])
            self.matplotwidget.axis.set_xlabel('Vzorky')
            self.matplotwidget.axis.set_ylabel('Amplituda')
            self.matplotwidget.canvas.draw()
            self.matplotwidget.canvas.flush_events()

        """
        Reálný sgnál
        """
        if self.rBzobrazeni2.isChecked():
            self.matplotwidget.axis.clear()
            self.matplotwidget.axis.plot(out,'.-')
            self.matplotwidget.axis.grid(True)
            self.matplotwidget.axis.set_xlabel('Vzorky')
            self.matplotwidget.axis.set_ylabel('Amplituda')
            self.matplotwidget.canvas.draw()
            self.matplotwidget.canvas.flush_events()
        
        """
        Frekvenční spektrum
        """
        # Výpočet FFT
        mag_samples, f1, L1 = TxRxModul.ProZobrazeniFFT(out, N, self.sample_rate)

        # Zobrazení FFT
        self.matplotwidget.axis2.clear()
        self.matplotwidget.axis2.plot(f1,np.real(mag_samples),'.-')
        self.matplotwidget.axis2.grid(True)
        self.matplotwidget.axis2.legend(["Výsledek"])
        self.matplotwidget.axis2.set_xlabel('Frekvence [Hz]')
        self.matplotwidget.axis2.set_ylabel('Amplituda [dB]')
        #self.matplotwidget2.axis.set_xlim([0,2500])
        self.matplotwidget.canvas.draw()
        self.matplotwidget.canvas.flush_events()

        self.lEvlastniSekvence.setText(xIntText)

    def JeToCislo(self, znak): # Zjistí, jestli char je číslo 0 - 9
        jeToCislo = znak == '0' or znak == '1' or znak == '2' or znak == '3' or znak == '4' or znak == '5' or znak == '6' or znak == '7' or znak == '8' or znak == '9'
        return jeToCislo

    def SpravneCislo(self, cislo, n): # Zjistí, jestli číslo patří do řádu modulace
        if cislo < n: return True
        else: return False

    def SpravnyFormat(self, text): # Zjistí, jestli byl použitý správný formát v řádku
        allowed_characters=['1','2','3','4','5','6','7','8','9','0',' ']
        if any(x not in allowed_characters for x in text):
            return False
        return True

    def NaCislo(self, n): # Převede text na čísla a oveří správnost formátu
        if not self.SpravnyFormat(list(self.lEvlastniSekvence.text())):
            text = ['0', ' ', '1'] # Aby byl to i dále fungovalo = opravý formát

            # Oznámení o špatném formátu
            self.dlg = QMessageBox(self.centralwidget)
            self.dlg.setIcon(QMessageBox.Critical)
            self.dlg.setWindowTitle("Chyba")
            # self.dlg.setText("Špatný formát. Správný: [0 1 2 10]")
            self.dlg.setText("Pouze čísla!")
            self.dlg.exec() 
        else:
            text = list(self.lEvlastniSekvence.text())
        
        i = 0
        x_prevod = []
        for znak in text: # Převod z listu charů na čísla
            if self.JeToCislo(znak):
                if i == len(text) - 1:
                    if self.SpravneCislo(int(znak),n):
                        x_prevod.append(int(znak))
                elif text[i+1] == ' ' or text[i+1] == '': # Je to jednomístný číslo
                    if self.SpravneCislo(int(znak),n):
                        x_prevod.append(int(znak))
                elif text[i+1] != ' ' and text[i+1] != '': # Je to dvoumístný číslo
                    if self.SpravneCislo(int(znak + text[i+1]),n):
                        x_prevod.append(int(znak + text[i+1]))
            i += 1

        i = 0
        xInt = np.zeros(len(x_prevod),dtype=int)
        for cislo in x_prevod: # Do xInt se předají čísla
            xInt[i] = int(cislo)
            i += 1
        return xInt

    def Modulace(self): # Vybere žádanou modulaci
        if self.cBmodulace.currentText() == "AM":
            """
            Přes jinou knihovnu na threading
            """
            # t1 = threading.Thread(target=self.AM()) # Vytvoření vlákna
            # t1.start()

            """
            Bez paralelizace
            """
            # AM()

            """
            Tato varianta threadingu umožňuje signalizovat konec práce vlákna
            """
            try:
                if not self.thread.isRunning(): # Pokud vlákno není aktivní může se provést
                    self.thread = QThread() # Vytvoreni QThread objektu                   
                    self.worker = Worker() # Vytvoření worker objektu
                    # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                    # Spojení signálů a slotů
                    self.thread.started.connect(lambda: self.worker.AM(self.hSfrekNosne.value(), self.hSfrekSign.value(), self.sBpromodulovanost.value(), self.sBOpakovani.value(), self.sample_rate))
                    self.worker.finished.connect(self.ZobrazeniAnal) # Po skončení vlákna se volá tato funkce
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.start() # Start
            except: # Pokud vlákno není vytvořeno
                self.thread = QThread() # Vytvoreni QThread objektu                   
                self.worker = Worker() # Vytvoření worker objektu
                # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                # Spojení signálů a slotů
                self.thread.started.connect(lambda: self.worker.AM(self.hSfrekNosne.value(), self.hSfrekSign.value(), self.sBpromodulovanost.value(), self.sBOpakovani.value(), self.sample_rate))
                self.worker.finished.connect(self.ZobrazeniAnal) # Po skončení vlákna se volá tato funkce
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start() # Start 
        if self.cBmodulace.currentText() == "FM":
            """
            Přes jinou knihovnu na threading
            """
            # t2 = threading.Thread(target=self.FM()) # Vytvoření vlákna
            # t2.start()

            """
            Bez paralelizace
            """
            # FM()

            """
            Tato varianta threadingu umožňuje signalizovat konec práce vlákna
            """
            try:
                if not self.thread.isRunning(): # Pokud vlákno není aktivní může se provést
                    self.thread = QThread() # Vytvoreni QThread objektu                   
                    self.worker = Worker() # Vytvoření worker objektu
                    # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                    # Spojení signálů a slotů
                    self.thread.started.connect(lambda: self.worker.FM(self.hSfrekNosne.value(), self.hSfrekSign.value(), self.sBpromodulovanost.value(), self.sBOpakovani.value(), self.sample_rate))
                    self.worker.finished.connect(self.ZobrazeniAnal) # Po skončení vlákna se volá tato funkce
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.start() # Start
            except:
                # Vytvoreni QThread objektu
                self.thread = QThread() # Vytvoreni QThread objektu                   
                self.worker = Worker() # Vytvoření worker objektu
                # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                # Spojení signálů a slotů
                self.thread.started.connect(lambda: self.worker.FM(self.hSfrekNosne.value(), self.hSfrekSign.value(), self.sBpromodulovanost.value(), self.sBOpakovani.value(), self.sample_rate))
                self.worker.finished.connect(self.ZobrazeniAnal) # Po skončení vlákna se volá tato funkce
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start() # Start
        if self.cBmodulace.currentText() == "ASK":
            """
            Přes jinou knihovnu na threading
            """
            # t3 = threading.Thread(target=self.ASK()) # Vytvoření vlákna
            # t3.start()

            """
            Bez paralelizace
            """
            # ASK()

            """
            Tato varianta threadingu umožňuje signalizovat konec práce vlákna
            """
            if self.rBgenSekv.isChecked(): 
                sekvence = 0
                x = 0
            if self.rBrostSekv.isChecked():
                sekvence = 1
                x = 0
            if self.rBvlSekv.isChecked():                 
                sekvence = 2
                x = self.NaCislo(int(self.cBnbitmodulace.currentText()))

            try:
                if not self.thread.isRunning(): # Pokud vlákno není aktivní může se provést
                    self.thread = QThread() # Vytvoreni QThread objektu                   
                    self.worker = Worker() # Vytvoření worker objektu
                    # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                    # Spojení signálů a slotů
                    self.thread.started.connect(lambda: self.worker.ASK(int(self.cBnbitmodulace.currentText()), self.opakovani, self.cBpolorovina.currentText(), sekvence, self.hSfrekNosne.value(), self.sample_rate, x))
                    self.worker.finished.connect(self.Zobrazeni)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.start() # Start
            except:
                self.thread = QThread() # Vytvoreni QThread objektu                   
                self.worker = Worker() # Vytvoření worker objektu
                # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                # Spojení signálů a slotů
                self.thread.started.connect(lambda: self.worker.ASK(int(self.cBnbitmodulace.currentText()), self.opakovani, self.cBpolorovina.currentText(), sekvence, self.hSfrekNosne.value(), self.sample_rate, x))
                self.worker.finished.connect(self.Zobrazeni)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start() # Start
        if self.cBmodulace.currentText() == "FSK":
            # Před zpracování typu sekvence
            if self.rBgenSekv.isChecked(): 
                sekvence = 0
                x = 0
            if self.rBrostSekv.isChecked():
                sekvence = 1
                x = 0
            if self.rBvlSekv.isChecked():                 
                sekvence = 2
                x = self.NaCislo(int(self.cBnbitmodulace.currentText()))

            """
            Přes jinou knihovnu na threading
            """
            # t4 = threading.Thread(target=self.FSK()) # Vytvoření vlákna
            # t4.start()

            """
            Bez paralelizace
            """
            # FSK()

            """
            Tato varianta threadingu umožňuje signalizovat konec práce vlákna
            """
            try:
                if not self.thread.isRunning(): # Pokud vlákno není aktivní může se provést
                    self.thread = QThread() # Vytvoreni QThread objektu                   
                    self.worker = Worker() # Vytvoření worker objektu
                    # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                    # Spojení signálů a slotů
                    self.thread.started.connect(lambda: self.worker.FSK(int(self.cBnbitmodulace.currentText()), self.opakovani, sekvence, self.hSfrekNosne.value(), self.sample_rate, x, self.sBpromodulovanost.value()))
                    self.worker.finished.connect(self.ZobrazeniFSK)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.start() # Start
            except:
                self.thread = QThread() # Vytvoreni QThread objektu                   
                self.worker = Worker() # Vytvoření worker objektu
                # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                # Spojení signálů a slotů
                self.thread.started.connect(lambda: self.worker.FSK(int(self.cBnbitmodulace.currentText()), self.opakovani, sekvence, self.hSfrekNosne.value(), self.sample_rate, x, self.sBpromodulovanost.value()))
                self.worker.finished.connect(self.ZobrazeniFSK)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start() # Start
        if self.cBmodulace.currentText() == "PSK":
            # Předzpracování sekvence
            if self.rBgenSekv.isChecked(): 
                sekvence = 0
                x = 0
            if self.rBrostSekv.isChecked():
                sekvence = 1
                x = 0
            if self.rBvlSekv.isChecked():                 
                sekvence = 2
                x = self.NaCislo(int(self.cBnbitmodulace.currentText()))

            """
            Přes jinou knihovnu na threading
            """
            # t5 = threading.Thread(target=self.PSK()) # Vytvoření vlákna
            # t5.start()

            """
            Bez paralelizace
            """
            # PSK()

            """
            Tato varianta threadingu umožňuje signalizovat konec práce vlákna
            """
            try:
                if not self.thread.isRunning(): # Pokud vlákno není aktivní může se provést
                    self.thread = QThread() # Vytvoreni QThread objektu                   
                    self.worker = Worker() # Vytvoření worker objektu
                    # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                    # Spojení signálů a slotů
                    self.thread.started.connect(lambda: self.worker.PSK(int(self.cBnbitmodulace.currentText()), self.opakovani, sekvence, self.hSfrekNosne.value(), self.sample_rate, x))
                    self.worker.finished.connect(self.Zobrazeni)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.start() # Start
            except:
                self.thread = QThread() # Vytvoreni QThread objektu                   
                self.worker = Worker() # Vytvoření worker objektu
                # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                # Spojení signálů a slotů
                self.thread.started.connect(lambda: self.worker.PSK(int(self.cBnbitmodulace.currentText()), self.opakovani, sekvence, self.hSfrekNosne.value(), self.sample_rate, x))
                self.worker.finished.connect(self.Zobrazeni)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start() # Start
        if self.cBmodulace.currentText() == "QAM":
            # Předzpracování sekvence
            if self.rBgenSekv.isChecked(): 
                sekvence = 0
                x = 0
            if self.rBrostSekv.isChecked():
                sekvence = 1
                x = 0
            if self.rBvlSekv.isChecked():                 
                sekvence = 2
                x = self.NaCislo(int(self.cBnbitmodulace.currentText()))

            if int(self.cBnbitmodulace.currentText()) == 2: # QAM není def pro n=2
                self.dlg = QMessageBox(self.centralwidget)
                self.dlg.setIcon(QMessageBox.Critical)
                self.dlg.setWindowTitle("Chyba")
                self.dlg.setText("QAM může být pouze 4, 8, 16 nebo 32")
                self.dlg.exec() 
                return

            """
            Přes jinou knihovnu na threading
            """
            # t6 = threading.Thread(target=self.QAM()) # Vytvoření vlákna
            # t6.start()

            """
            Bez paralelizace
            """
            # QAM()

            """
            Tato varianta threadingu umožňuje signalizovat konec práce vlákna
            """
            try:
                if not self.thread.isRunning(): # Pokud vlákno není aktivní může se provést
                    self.thread = QThread() # Vytvoreni QThread objektu                   
                    self.worker = Worker() # Vytvoření worker objektu
                    # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                    # Spojení signálů a slotů
                    self.thread.started.connect(lambda: self.worker.QAM(int(self.cBnbitmodulace.currentText()), self.opakovani, sekvence, self.hSfrekNosne.value(), self.sample_rate, x))
                    self.worker.finished.connect(self.Zobrazeni)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.start() # Start
            except:
                self.thread = QThread() # Vytvoreni QThread objektu                   
                self.worker = Worker() # Vytvoření worker objektu
                # self.worker.moveToThread(self.thread) # Přesunutí worker do thread
                # Spojení signálů a slotů
                self.thread.started.connect(lambda: self.worker.QAM(int(self.cBnbitmodulace.currentText()), self.opakovani, sekvence, self.hSfrekNosne.value(), self.sample_rate, x))
                self.worker.finished.connect(self.Zobrazeni)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start() # Start
            # QAM()

    def PokracovaniASK(self,x,n,k): #Vypočítává hodnoty zesílení pro 4-ASK a větší
        x = x-2 # Snížení na rozsah 0 - 1
        if x <= 1:
            y = (x - 0.5) * (k+2)
        else:
            k = k+2
            y = self.PokracovaniASK(x,n,k)                    
        return y

    def ASK(self):
        n = int(self.cBnbitmodulace.currentText())

        """
        Výběr tvorby sekvence
        """
        if self.rBgenSekv.isChecked(): 
            xInt = self.NahodSymboly(n,2*n) # Počet čísel 2x větší než je řád, aby se zabezpečil dostatečný rozsah hodnot
            delka = 2 * n * self.opakovani # Délka generovaného signálu
        if self.rBrostSekv.isChecked():
            xInt = np.arange(0,n)
            delka = n * self.opakovani # Délka generovaného signálu  
        if self.rBvlSekv.isChecked():                 
            xInt = self.NaCislo(n)
            delka = len(xInt) * self.opakovani # Délka generovaného signálu

        """
        Výběr poloroviny
        """
        if self.cBpolorovina.currentText() == "Celá rovina": polorovina = 0
        if self.cBpolorovina.currentText() == "Pravá polorovina": polorovina = 1
        if self.cBpolorovina.currentText() == "Levá polorovina": polorovina = 2

        """
        Generování amplitud
        """
        xAmp = np.zeros(len(xInt), dtype=np.float64)
        if polorovina == 0: # Podle toho jaká se používá polorovina se vypočítají apmlitudy pro symboly
            for i in np.arange(len(xInt)):
                if xInt[i] <= 1: # Vypočte aplitudu pro čísla 0 a 1
                    xAmp[i] = (xInt[i] - 0.5) * 2
                else: # Vypočte aplitudu pro čísla 2 a více
                    k = 2
                    xAmp[i] = self.PokracovaniASK(xInt[i],n,k) # Rekurzivní výpočet aplitud pro symboly
        elif polorovina == 1:
            xAmp = xInt / (n - 1) + 0.5
        elif polorovina == 2:
            xAmp = xInt / (n - 1) - 1.5
        xSymbols = xAmp * (np.cos(0) + 1j * np.sin(0))  # Vytvočení komplexních čísel
        samples = np.repeat(xSymbols, self.opakovani)
        out = self.IQnaReal(samples,len(samples), np.arange(delka) / self.sample_rate)

        xIntText = str(xInt)
        xIntText = xIntText.replace("[", "")
        xIntText = xIntText.replace("]", "")
        self.Zobrazeni(samples, out)

    def QAM(self):  # jen do 32b
        n = int(self.cBnbitmodulace.currentText())
        if n == 2: # QAM není definovaná pro n=2
            self.dlg = QMessageBox(self.centralwidget)
            self.dlg.setIcon(QMessageBox.Critical)
            self.dlg.setWindowTitle("Chyba")
            self.dlg.setText("QAM může být pouze 4, 8, 16 nebo 32")
            self.dlg.exec() 
            return
        
        """
        Výběr tvorby sekvence
        """
        if self.rBgenSekv.isChecked(): 
            xInt = self.NahodSymboly(n,2*n) # Počet čísel 2x větší než je řád, aby se zabezpečil dostatečný rozsah hodnot
            delka = 2 * n * self.opakovani # Délka generovaného signálu
        if self.rBrostSekv.isChecked():
            xInt = np.arange(0,n)
            delka = n * self.opakovani # Délka generovaného signálu  
        if self.rBvlSekv.isChecked():                 
            xInt = self.NaCislo(n)
            delka = len(xInt) * self.opakovani # Délka generovaného signálu
        xSymbols = np.zeros(n, dtype=complex)                
        
        """
        Vytváření symbolů
        """
        match n:
            case 4:
                i = 0
                for a in xInt:
                    match a:
                        case 0:
                            xSymbols[i] = 1 + 1j
                        case 1:
                            xSymbols[i] = -1 + 1j
                        case 2:
                            xSymbols[i] = -1 - 1j
                        case 3:
                            xSymbols[i] = 1 - 1j
                    i += 1
            case 8:
                i = 0
                for a in xInt:
                    match a:
                        case 0:
                            xSymbols[i] = 1 + 1j
                        case 1:
                            xSymbols[i] = -1 + 1j
                        case 2:
                            xSymbols[i] = -1 - 1j
                        case 3:
                            xSymbols[i] = 1 - 1j
                        case 4:
                            xSymbols[i] = 3 + 3j
                        case 5:
                            xSymbols[i] = -3 + 3j
                        case 6:
                            xSymbols[i] = -3 - 3j
                        case 7:
                            xSymbols[i] = 3 - 3j
                    i += 1
            case 16:
                i = 0
                for a in xInt:
                    match a:
                        case 0:
                            xSymbols[i] = 1 + 1j
                        case 1:
                            xSymbols[i] = -1 + 1j
                        case 2:
                            xSymbols[i] = -1 - 1j
                        case 3:
                            xSymbols[i] = 1 - 1j
                        case 4:
                            xSymbols[i] = 3 + 1j
                        case 5:
                            xSymbols[i] = 3 + 3j
                        case 6:
                            xSymbols[i] = 1 + 3j
                        case 7:
                            xSymbols[i] = -1 + 3j
                        case 8:
                            xSymbols[i] = -3 + 3j
                        case 9:
                            xSymbols[i] = -3 + 1j
                        case 10:
                            xSymbols[i] = -3 - 1j
                        case 11:
                            xSymbols[i] = -3 - 3j
                        case 12:
                            xSymbols[i] = -1 - 3j
                        case 13:
                            xSymbols[i] = 1 - 3j
                        case 14:
                            xSymbols[i] = 3 - 3j
                        case 15:
                            xSymbols[i] = 3 - 1j
                    i += 1
            case 32:
                i = 0
                for a in xInt:
                    match a:
                        case 0:
                            xSymbols[i] = 1 + 1j
                        case 1:
                            xSymbols[i] = -1 + 1j
                        case 2:
                            xSymbols[i] = -1 - 1j
                        case 3:
                            xSymbols[i] = 1 - 1j
                        case 4:
                            xSymbols[i] = 3 + 1j
                        case 5:
                            xSymbols[i] = 3 + 3j
                        case 6:
                            xSymbols[i] = 1 + 3j
                        case 7:
                            xSymbols[i] = -1 + 3j
                        case 8:
                            xSymbols[i] = -3 + 3j
                        case 9:
                            xSymbols[i] = -3 + 1j
                        case 10:
                            xSymbols[i] = -3 - 1j
                        case 11:
                            xSymbols[i] = -3 - 3j
                        case 12:
                            xSymbols[i] = -1 - 3j
                        case 13:
                            xSymbols[i] = 1 - 3j
                        case 14:
                            xSymbols[i] = 3 - 3j
                        case 15:
                            xSymbols[i] = 3 - 1j
                        case 16:
                            xSymbols[i] = 5 + 1j
                        case 17:
                            xSymbols[i] = 5 + 3j
                        case 18:
                            xSymbols[i] = 3 + 5j
                        case 19:
                            xSymbols[i] = 1 + 5j
                        case 20:
                            xSymbols[i] = -1 + 5j
                        case 21:
                            xSymbols[i] = -3 + 5j
                        case 22:
                            xSymbols[i] = -5 + 3j
                        case 23:
                            xSymbols[i] = -5 + 1j
                        case 24:
                            xSymbols[i] = -5 - 1j
                        case 25:
                            xSymbols[i] = -5 - 3j
                        case 26:
                            xSymbols[i] = -3 - 5j
                        case 27:
                            xSymbols[i] = -1 - 1j
                        case 28:
                            xSymbols[i] = 1 - 5j
                        case 29:
                            xSymbols[i] = 3 - 5j
                        case 30:
                            xSymbols[i] = 5 - 3j
                        case 31:
                            xSymbols[i] = 5 - 1j
                    i += 1

        samples = np.repeat(xSymbols, self.opakovani)  # Z impulzu na pulz o délce opakování
        # samples = Normovani(samples)
        out = self.IQnaReal(samples,delka,np.arange(delka) / self.sample_rate)

        xIntText = str(xInt)
        xIntText = xIntText.replace("[", "")
        xIntText = xIntText.replace("]", "")
        # Zobrazeni(samples)
        self.Zobrazeni(samples, out)
        # self.lEvlastniSekvence.setText(str(xInt))

    def PSK(self):
        n = int(self.cBnbitmodulace.currentText())
        
        """
        Výběr tvorby sekvence
        """
        if self.rBgenSekv.isChecked(): 
            xInt = self.NahodSymboly(n,2*n) # Počet čísel 2x větší než je řád, aby se zabezpečil dostatečný rozsah hodnot
            delka = 2 * n * self.opakovani # Délka generovaného signálu
        if self.rBrostSekv.isChecked():
            xInt = np.arange(0,n)
            delka = n * self.opakovani # Délka generovaného signálu  
        if self.rBvlSekv.isChecked():                 
            xInt = self.NaCislo(n)
            delka = len(xInt) * self.opakovani # Délka generovaného signálu 
        
        if n == 4:
            xDegrees = xInt * 360 / 4.0 + 45  # 45, 135, 225, 315 stupňů
        else:
            xDegrees = xInt * 360 / n
        xRadians = xDegrees * np.pi / 180.0  # převod na radiany
        if n == 2:
            xSymbols = np.cos(xRadians) + 1j * np.floor(np.sin(xRadians))  # vytvoří komplexní symbol
        else:
            xSymbols = np.cos(xRadians) + 1j * np.sin(xRadians)  # Vytvoří komplexní symbol
        samples = np.repeat(xSymbols, self.opakovani) 
        out = self.IQnaReal(samples,delka,np.arange(delka) / self.sample_rate)

        xIntText = str(xInt)
        xIntText = xIntText.replace("[", "")
        xIntText = xIntText.replace("]", "")
        # Zobrazeni(samples)
        self.Zobrazeni(samples, out)
        # self.lEvlastniSekvence.setText(str(xInt))

    def FSK(self):
        carrier_freq = self.hSfrekNosne.value()
        # D_f = self.sBpromodulovanost.value()/100
        Delta_f = self.sBpromodulovanost.value()          
        n = int(self.cBnbitmodulace.currentText())
        
        """
        Výběr tvorby sekvence
        """
        if self.rBgenSekv.isChecked(): 
            xInt_n = self.NahodSymboly(n,2*n) # Počet čísel 2x větší než je řád, aby se zabezpečil dostatečný rozsah hodnot
            delka = 2 * n * self.opakovani # Délka generovaného signálu
        if self.rBrostSekv.isChecked():
            xInt_n = np.arange(0,n)
            delka = n * self.opakovani # Délka generovaného signálu  
        if self.rBvlSekv.isChecked():                 
            xInt_n = self.NaCislo(n)
            delka = len(xInt_n) * self.opakovani # Délka generovaného signálu
        t = np.arange(delka) / self.sample_rate  # Diskrétní čas


        """
        Modulace
        """
        xInt = np.repeat(xInt_n, self.opakovani)

        f = (carrier_freq + Delta_f * xInt - (n * Delta_f)/2) + Delta_f/2 # průběh frekvence v čase
        #f = carrier_freq + D_f * carrier_freq * xInt / 2 # Frekvence pro každý symbol
        # xSymbols = np.cos(2 * np.pi * f * t) + 1j*np.sin(2 * np.pi * f * t)
        #samples = np.repeat(xSymbols, opakovani)
        #samples = xSymbols
        delta_phi = f * np.pi / (self.sample_rate / 2.0)
        phi = np.cumsum(delta_phi)
        samples = np.cos(2*np.pi*carrier_freq*t + phi) + 1j * np.sin(2*np.pi*carrier_freq*t + phi)
        out = self.IQnaReal(samples,delka, t)

        xIntText = str(xInt_n)
        xIntText = xIntText.replace("[", "")
        xIntText = xIntText.replace("]", "")
        self.ZobrazeniFSK(samples, out, len(samples))
        # self.lEvlastniSekvence.setText(str(xInt_n))

    def AM(self):
        # Inicializace
        carrier_freq = self.hSfrekNosne.value()
        modulater_freq = self.hSfrekSign.value()
        modulation_index = self.sBpromodulovanost.value()/100
        N = self.sBOpakovani.value()*5
        t = np.arange(N) / self.sample_rate

        """
        Komlexní zápis
        """
        # cosModulacni = np.cos(modulater_freq * xRadians) + 1j * np.sin(modulater_freq * xRadians)
        # cosNosna = np.cos(carrier_freq * xRadians) + 1j * np.sin(carrier_freq * xRadians)
        # samples = A_c * (1 + modulation_index * cosModulacni) * cosNosna
        
        """
        Normální zápis
        """
        cosModulacni = np.cos(modulater_freq * 2 * np.pi * t)
        cosNosna = np.cos(carrier_freq * 2 * np.pi * t)
        # samples = A_c * (1 + modulation_index * cosModulacni) * cosNosna
        samples = modulation_index * cosModulacni * cosNosna + cosNosna
        
        samples = TxRxModul.NormovaniAbs(samples)
        cosModulacni = TxRxModul.NormovaniAbs(cosModulacni)
        cosNosna = TxRxModul.NormovaniAbs(cosNosna)

        self.ZobrazeniAnal(samples,cosModulacni,cosNosna,N)

    def FM(self):
        # Inicializace
        carrier_freq = self.hSfrekNosne.value()
        modulater_freq = self.hSfrekSign.value()
        D_f = self.sBpromodulovanost.value()/10
        N = self.sBOpakovani.value()*5
        t = np.arange(N) / self.sample_rate

        # f = carrier_freq + D_f * np.cos(2*np.pi*modulater_freq*t)
        cosNosna = np.cos(2*np.pi*carrier_freq*t)
        cosModulacni = np.cos(2*np.pi*modulater_freq*t)  # Vysílaná zpráva
        # soucet_modulater = np.real(cosModulacni) + np.imag(cosModulacni)
        # samples = A_c*np.cos(2*np.pi*carrier_freq*t + D_f*np.sin(2*np.pi*modulater_freq*t)) + 1j * np.sin(2*np.pi*carrier_freq*t + D_f*np.sin(2*np.pi*modulater_freq*t)) # Vysílaný výsledek
        # Pěkný pokud by se to považovalo za real a ne IQ
        # phi = carrier_freq * t + D_f * cosModulacni
        # samples = np.cos(2*np.pi * phi) + 1j*np.sin(2*np.pi * phi)
        samples = np.cos(2*np.pi*carrier_freq*t + D_f*np.sin(2*np.pi*modulater_freq*t))
        
        # samples = Normovani(samples)

        # samples = IQnaReal(samples, len(samples), t)

        # deltaF = D_f
        # h = deltaF/modulater_freq
        self.ZobrazeniAnal(samples,cosModulacni,cosNosna,N)

    def setupUi(self, ModulaceWindow, width, height):
        ModulaceWindow.setObjectName("ModulaceWindow")
        ModulaceWindow.resize(width, height)
        ModulaceWindow.showMaximized() # Okno mám maxilmální velikost (obrazovky)
        self.centralwidget = QtWidgets.QWidget(ModulaceWindow)
        self.centralwidget.setObjectName("centralwidget")
        """"""
        self.zobrazeniModulace = QtWidgets.QWidget(self.centralwidget)
        # self.zobrazeniModulace.setGeometry(QtCore.QRect(240, -20, width-260, int(height/2)))
        self.zobrazeniModulace.setGeometry(QtCore.QRect(240, -20, width-260, height))
        self.zobrazeniModulace.setObjectName("zobrazeniModulace")
        """Label Modulace"""
        self.lModulace = QtWidgets.QLabel(self.centralwidget)
        self.lModulace.setGeometry(QtCore.QRect(235, 150, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lModulace.setFont(font)
        self.lModulace.setObjectName("lModulace")
        """Font"""
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        """ComboBox na výběr modulace"""
        self.cBmodulace = QtWidgets.QComboBox(self.centralwidget)
        self.cBmodulace.setGeometry(QtCore.QRect(10, 10, 191, 31))
        self.cBmodulace.setFont(font)
        self.cBmodulace.setObjectName("cBmodulace")
        self.cBmodulace.addItems(["AM","FM","ASK","PSK","FSK","QAM"])
        self.cBmodulace.currentIndexChanged.connect(self.Modulace)
        self.cBmodulace.currentIndexChanged.connect(self.Zamek)
        """Slider frekvence modulačního signálu"""
        self.hSfrekSign = QtWidgets.QSlider(self.centralwidget)
        self.hSfrekSign.setGeometry(QtCore.QRect(10, 80, 160, 22))
        self.hSfrekSign.setOrientation(QtCore.Qt.Horizontal)
        self.hSfrekSign.setObjectName("hSfrekSign")
        self.hSfrekSign.setMinimum(10)
        self.hSfrekSign.setMaximum(5000)
        self.hSfrekSign.setValue(300)
        # self.hSfrekSign.valueChanged.connect(self.Modulace)
        self.hSfrekSign.valueChanged.connect(self.Obnoveni)
        """SpinBox frekvence modulačního signálu"""
        self.sBfrekSign = QtWidgets.QSpinBox(self.centralwidget)
        self.sBfrekSign.setGeometry(QtCore.QRect(170, 80, 61, 22))
        # self.sBfrekSign.setFont(font)
        self.sBfrekSign.setObjectName("sBfrekSign")
        self.sBfrekSign.setMinimum(10)
        self.sBfrekSign.setMaximum(5000)
        self.sBfrekSign.setValue(300)
        self.sBfrekSign.valueChanged.connect(self.Modulace)
        self.sBfrekSign.valueChanged.connect(self.Obnoveni)
        """Label Hz"""
        self.lFrekSig = QtWidgets.QLabel(self.centralwidget)
        self.lFrekSig.setGeometry(QtCore.QRect(235, 80, 80, 21))
        self.lFrekSig.setFont(font)
        self.lFrekSig.setObjectName("lFrekSig")
        """Slider frekvence nosné"""
        self.hSfrekNosne = QtWidgets.QSlider(self.centralwidget)
        self.hSfrekNosne.setGeometry(QtCore.QRect(10, 150, 160, 22))
        self.hSfrekNosne.setOrientation(QtCore.Qt.Horizontal)
        self.hSfrekNosne.setObjectName("hSfrekNosne")
        self.hSfrekNosne.setMinimum(100)
        self.hSfrekNosne.setMaximum(25000)
        self.hSfrekNosne.setValue(1000)
        # self.hSfrekNosne.valueChanged.connect(self.Modulace)
        self.hSfrekNosne.valueChanged.connect(self.Obnoveni)
        """SpinBox frekvence nosné"""
        self.sBfrekNosne = QtWidgets.QSpinBox(self.centralwidget)
        self.sBfrekNosne.setGeometry(QtCore.QRect(170, 150, 61, 22))
        self.sBfrekNosne.setObjectName("sBfrekNosne")
        self.sBfrekNosne.setMinimum(100)
        self.sBfrekNosne.setMaximum(25000)
        self.sBfrekNosne.setValue(1000)
        self.sBfrekNosne.valueChanged.connect(self.Modulace)
        self.sBfrekNosne.valueChanged.connect(self.Obnoveni)
        """Label Hz"""
        self.lFrekNos = QtWidgets.QLabel(self.centralwidget)
        self.lFrekNos.setGeometry(QtCore.QRect(235, 150, 80, 21))
        self.lFrekNos.setFont(font)
        self.lFrekNos.setObjectName("lFrekNos")
        """Label Frekvence signálu"""
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(10, 50, 181, 21))
        self.label1.setFont(font)
        self.label1.setMouseTracking(False)
        self.label1.setObjectName("label1")
        """Label Frekvence nosné"""
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(10, 120, 181, 21))
        self.label3.setFont(font)
        self.label3.setMouseTracking(False)
        self.label3.setObjectName("label3")
        """lineEdit zobrazení sekvence a zadání vlastní"""
        self.lEvlastniSekvence = QtWidgets.QLineEdit(self.centralwidget)
        self.lEvlastniSekvence.setGeometry(QtCore.QRect(10, 300, 211, 22))
        self.lEvlastniSekvence.setFont(font)
        self.lEvlastniSekvence.setObjectName("lEvlastniSekvence")
        self.lEvlastniSekvence.returnPressed.connect(self.Modulace)
        """Label Zadej vysílanou sekvenci"""
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(10, 280, 240, 21))
        self.label2.setFont(font)
        self.label2.setMouseTracking(False)
        self.label2.setObjectName("label2")
        """ButtonGroup pro výběr generování sekvence"""
        self.sekvence_Group = QButtonGroup()
        """RadioButton vlastní sekvence"""
        self.rBvlSekv = QtWidgets.QRadioButton(self.centralwidget)
        self.rBvlSekv.setGeometry(QtCore.QRect(10, 220, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBvlSekv.setFont(font)
        self.rBvlSekv.setObjectName("rBvlSekv")
        self.sekvence_Group.addButton(self.rBvlSekv)
        self.rBvlSekv.clicked.connect(self.Modulace)
        self.rBvlSekv.clicked.connect(self.Zamek)
        # self.rBvlSekv.clicked.connect(plot_widget)
        """RadioButton generování náhodné sekvence"""
        self.rBgenSekv = QtWidgets.QRadioButton(self.centralwidget)
        self.rBgenSekv.setGeometry(QtCore.QRect(10, 190, 240, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBgenSekv.setFont(font)
        self.rBgenSekv.setObjectName("rBgenSekv")
        #self.rBgenSekv.setChecked(True)
        self.sekvence_Group.addButton(self.rBgenSekv)
        self.rBgenSekv.clicked.connect(self.Modulace)
        self.rBgenSekv.clicked.connect(self.Zamek)
        """RadioButton rostoucí sekvence"""
        self.rBrostSekv = QtWidgets.QRadioButton(self.centralwidget)
        self.rBrostSekv.setGeometry(QtCore.QRect(10, 250, 240, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBrostSekv.setFont(font)
        self.rBrostSekv.setObjectName("rBrostSekv")
        self.rBrostSekv.setChecked(True)
        self.sekvence_Group.addButton(self.rBrostSekv)
        self.rBrostSekv.clicked.connect(self.Modulace)
        self.rBrostSekv.clicked.connect(self.Zamek)
        """Label Kolik stavová modualce"""
        self.label4 = QtWidgets.QLabel(self.centralwidget)
        self.label4.setGeometry(QtCore.QRect(10, 340, 230, 21))
        self.label4.setFont(font)
        self.label4.setMouseTracking(False)
        self.label4.setObjectName("label4")
        """ComboBox n-úrovňová modulace"""
        self.cBnbitmodulace = QtWidgets.QComboBox(self.centralwidget)
        self.cBnbitmodulace.setGeometry(QtCore.QRect(10, 360, 191, 31))
        self.cBnbitmodulace.setFont(font)
        self.cBnbitmodulace.setObjectName("cBnbitmodulace")
        self.cBnbitmodulace.addItems(["2","4","8","16","32"])
        self.cBnbitmodulace.currentIndexChanged.connect(self.Modulace)
        self.cBnbitmodulace.currentIndexChanged.connect(self.Zamek)
        """ComboBox jaká polorovina"""
        self.cBpolorovina = QtWidgets.QComboBox(self.centralwidget)
        self.cBpolorovina.setGeometry(QtCore.QRect(10, 430, 191, 31))
        self.cBpolorovina.setFont(font)
        self.cBpolorovina.setObjectName("cBpolorovina")
        self.cBpolorovina.addItems(["Celá rovina","Pravá polorovina","Levá polorovina"])
        self.cBpolorovina.currentIndexChanged.connect(self.Modulace)
        self.cBpolorovina.currentIndexChanged.connect(self.Zamek)
        """Label Polorovina"""
        self.label5 = QtWidgets.QLabel(self.centralwidget)
        self.label5.setGeometry(QtCore.QRect(10, 410, 120, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label5.setFont(font)
        self.label5.setMouseTracking(False)
        self.label5.setObjectName("label5")
        """SpinBox promodulovanost"""
        self.sBpromodulovanost = QtWidgets.QSpinBox(self.centralwidget)
        self.sBpromodulovanost.setGeometry(QtCore.QRect(10, 510, 61, 22))
        self.sBpromodulovanost.setFont(font)
        self.sBpromodulovanost.setObjectName("sBpromodulovanost")
        self.sBpromodulovanost.setMinimum(0)
        self.sBpromodulovanost.setMaximum(200)
        self.sBpromodulovanost.setValue(80)
        self.sBpromodulovanost.valueChanged.connect(self.Modulace)
        """Label Promodulovanost"""
        self.label6 = QtWidgets.QLabel(self.centralwidget)
        self.label6.setGeometry(QtCore.QRect(10, 480, 250, 35))
        self.label6.setFont(font)
        self.label6.setMouseTracking(False)
        self.label6.setObjectName("label6")
        """Slider frekvence vzorkování"""
        self.hSfrekVzork = QtWidgets.QSlider(self.centralwidget)
        self.hSfrekVzork.setGeometry(QtCore.QRect(10, 590, 160, 22))
        self.hSfrekVzork.setOrientation(QtCore.Qt.Horizontal)
        self.hSfrekVzork.setObjectName("hSfrekVzork")       
        self.hSfrekVzork.setMinimum(1000)
        self.hSfrekVzork.setMaximum(100000)
        self.hSfrekVzork.setValue(15000)
        self.hSfrekVzork.setTickInterval(100)
        self.hSfrekVzork.setSingleStep(500)        
        # self.hSfrekVzork.sliderReleased.connect(self.Modulace)
        self.hSfrekVzork.sliderReleased.connect(self.Obnoveni)
        """SpinBox frekvence vzorkování"""
        self.sBfrekVzork = QtWidgets.QSpinBox(self.centralwidget)
        self.sBfrekVzork.setGeometry(QtCore.QRect(170, 590, 61, 22))
        self.sBfrekVzork.setObjectName("sBfrekVzork")  
        self.sBfrekVzork.setMinimum(1000)
        self.sBfrekVzork.setMaximum(100000)
        self.sBfrekVzork.setValue(15000)
        self.sBfrekVzork.setSingleStep(100)
        self.sBfrekVzork.valueChanged.connect(self.Modulace)
        self.sBfrekVzork.valueChanged.connect(self.Obnoveni)
        """Label Hz"""
        self.lFrekVzork = QtWidgets.QLabel(self.centralwidget)
        self.lFrekVzork.setGeometry(QtCore.QRect(235, 590, 80, 21))
        self.lFrekVzork.setFont(font)
        self.lFrekVzork.setObjectName("lFrekVzork")
        """Label Vzorkovací frekvence"""
        self.label7 = QtWidgets.QLabel(self.centralwidget)
        self.label7.setGeometry(QtCore.QRect(10, 560, 200, 21))
        self.label7.setFont(font)
        self.label7.setMouseTracking(False)
        self.label7.setObjectName("label7")
        """ButtonGroup pro varianty zobrazení"""
        self.zobrazeni_Group = QButtonGroup()
        """RadioButton zobrazení 1"""
        self.rBzobrazeni1 = QtWidgets.QRadioButton(self.centralwidget)
        self.rBzobrazeni1.setGeometry(QtCore.QRect(10, 630, 240, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBzobrazeni1.setFont(font)
        self.rBzobrazeni1.setObjectName("rBzobrazeni1")
        self.rBzobrazeni1.setChecked(True)
        self.zobrazeni_Group.addButton(self.rBzobrazeni1)
        self.rBzobrazeni1.clicked.connect(self.Modulace)
        """RadioButton zobrazení 2"""
        self.rBzobrazeni2 = QtWidgets.QRadioButton(self.centralwidget)
        self.rBzobrazeni2.setGeometry(QtCore.QRect(10, 660, 240, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rBzobrazeni2.setFont(font)
        self.rBzobrazeni2.setObjectName("rBzobrazeni2")
        self.zobrazeni_Group.addButton(self.rBzobrazeni2)
        self.rBzobrazeni2.clicked.connect(self.Modulace)
        """Label Počet vzorků"""
        self.lOpakovani = QtWidgets.QLabel(self.centralwidget)
        self.lOpakovani.setGeometry(QtCore.QRect(10, 560, 200, 21))
        self.lOpakovani.setFont(font)
        self.lOpakovani.setMouseTracking(False)
        self.lOpakovani.setObjectName("lOpakovani")
        """SpinBox počet opakování/počet vzorků na symbol"""
        self.sBOpakovani = QtWidgets.QSpinBox(self.centralwidget)
        self.sBOpakovani.setGeometry(QtCore.QRect(170, 590, 61, 22))
        self.sBOpakovani.setFont(font)
        self.sBOpakovani.setObjectName("sBOpakovani")  
        self.sBOpakovani.setMinimum(5)
        self.sBOpakovani.setMaximum(2000)
        self.sBOpakovani.setValue(1000)
        self.sBOpakovani.setSingleStep(10)
        self.sBOpakovani.valueChanged.connect(self.Obnoveni)
        self.sBOpakovani.valueChanged.connect(self.Modulace)
        self.sBOpakovani.valueChanged.connect(self.ZmenaPoctuVzorkuNaSymbol)
        """"""
        ModulaceWindow.setCentralWidget(self.centralwidget)

        """Layout"""
        outerLayout = QHBoxLayout() 
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # leftLayout.addWidget(self.cBmodulace)
        leftLayout.addWidget(self.lModulace)
        leftLayout_0 = QGridLayout()
        leftLayout_0.addWidget(self.cBmodulace,0,0)
        leftLayout_0.setColumnStretch(1,50)
        leftLayout.addLayout(leftLayout_0)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.label1)
        leftLayout_1 = QGridLayout()
        leftLayout_1.addWidget(self.hSfrekSign,0,0,1,1)
        leftLayout_1.addWidget(self.sBfrekSign,0,1,1,1)
        leftLayout_1.addWidget(self.lFrekSig,0,2,1,1)
        leftLayout.addLayout(leftLayout_1)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.label3)
        leftLayout_2 = QGridLayout()
        leftLayout_2.addWidget(self.hSfrekNosne,0,0,1,1)
        leftLayout_2.addWidget(self.sBfrekNosne,0,1,1,1)
        leftLayout_2.addWidget(self.lFrekNos,0,2,1,1)
        leftLayout.addLayout(leftLayout_2)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.rBgenSekv)
        leftLayout.addWidget(self.rBvlSekv)
        leftLayout.addWidget(self.rBrostSekv)
        leftLayout.addSpacing(10)
        leftLayout.addWidget(self.label2)
        leftLayout.addWidget(self.lEvlastniSekvence)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.label4)
        leftLayout_3 = QGridLayout()
        leftLayout_3.addWidget(self.cBnbitmodulace,0,0)
        leftLayout_3.setColumnStretch(1,50)
        leftLayout.addLayout(leftLayout_3)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.label5)
        leftLayout_4 = QGridLayout()
        leftLayout_4.addWidget(self.cBpolorovina,0,0)
        leftLayout_4.setColumnStretch(1,50)
        leftLayout.addLayout(leftLayout_4)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.label6)
        leftLayout_5 = QGridLayout()
        leftLayout_5.addWidget(self.sBpromodulovanost,0,0)
        leftLayout_5.setColumnStretch(1,50)
        leftLayout.addLayout(leftLayout_5)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.label7)
        leftLayout_6 = QGridLayout()
        leftLayout_6.addWidget(self.hSfrekVzork,0,0,1,1)
        leftLayout_6.addWidget(self.sBfrekVzork,0,1,1,1)
        leftLayout_6.addWidget(self.lFrekVzork,0,2,1,1)
        leftLayout.addLayout(leftLayout_6)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.rBzobrazeni1)
        leftLayout.addWidget(self.rBzobrazeni2)
        leftLayout.addSpacing(20)
        leftLayout.addWidget(self.lOpakovani)
        leftLayout_7 = QGridLayout()
        leftLayout_7.addWidget(self.sBOpakovani,0,0,1,1)
        leftLayout_7.setColumnStretch(1,50)
        leftLayout.addLayout(leftLayout_7)

        leftLayout.addStretch()

        rightLayout.addWidget(self.zobrazeniModulace,1000)
        # rightLayout.addStretch(1)

        outerLayout.addLayout(leftLayout,1)
        outerLayout.addLayout(rightLayout,5)

        self.centralwidget.setLayout(outerLayout)

        class MatplotlibWidget(QWidget): # Vytvoří 2 grafy
            def __init__(self, parent=None):
                super(MatplotlibWidget, self).__init__(parent)
                self.figure = Figure()
                self.figure.set_tight_layout([50, 500, 100])
                self.canvas = Canvas(self.figure)

                # self.axis = self.figure.add_subplot(111)
                self.axis = self.figure.add_subplot(211) # subplot 1
                self.axis2 = self.figure.add_subplot(212) # subplot 2
                toolbar = NavigationToolbar(self.canvas, self)

                # spojí graf a toolbar
                self.layoutvertical = QVBoxLayout(self)
                self.layoutvertical.addWidget(toolbar) 
                self.layoutvertical.addWidget(self.canvas)

        def init_widget(self): # Inicializace zobrazení
            self.matplotwidget = MatplotlibWidget()
            self.layoutvertical = QVBoxLayout(self.zobrazeniModulace)
            self.layoutvertical.addWidget(self.matplotwidget)
            
            # Pro verzi, kde jsou 2 grafy a ne 2 subploty
            # self.matplotwidget2 = MatplotlibWidget()
            # self.layoutvertical = QVBoxLayout(self.zobrazeniModulace_2)
            # self.layoutvertical.addWidget(self.matplotwidget2)

        """
        Inicializace
        """
        self.retranslateUi(ModulaceWindow)
        init_widget(self)
        self.Zamek()
        self.lEvlastniSekvence.setText("0 1")
        QtCore.QMetaObject.connectSlotsByName(ModulaceWindow)

    def retranslateUi(self, ModulaceWindow):
        _translate = QtCore.QCoreApplication.translate
        ModulaceWindow.setWindowTitle(_translate("ModulaceWindow", "PyModulace"))
        self.lModulace.setText(_translate("ModulaceWindow", "Modulace:"))
        self.label1.setText(_translate("ModulaceWindow", "Frekvence signálu"))
        self.label3.setText(_translate("ModulaceWindow", "Frekvence nosné"))
        self.label2.setText(_translate("ModulaceWindow", "Zadej vysílanou sekvenci:"))
        self.rBvlSekv.setToolTip(_translate("MainWindow", "<html><head/><body><p>Lze zadat vlastní číselnou sekvenci (čísla musí být z rozsahu modulace)</p></body></html>"))
        self.rBvlSekv.setText(_translate("ModulaceWindow", "Vlastní sekvence"))
        self.rBgenSekv.setToolTip(_translate("ModulaceWindow", "<html><head/><body><p>Umožní vygenerovat náhodnou sekvenci čísel</p></body></html>"))
        self.rBgenSekv.setText(_translate("ModulaceWindow", "Vygenerovat sekvenci"))
        self.rBrostSekv.setToolTip(_translate("MainWindow", "<html><head/><body><p>Všechny hodnoty, které aktuální verze modulace zvládne</p></body></html>"))
        self.rBrostSekv.setText(_translate("ModulaceWindow", "Rostoucí sekvence"))
        self.rBzobrazeni1.setText(_translate("ModulaceWindow", "Zobrazení 1"))
        self.rBzobrazeni2.setText(_translate("ModulaceWindow", "Zobrazení 2"))
        self.label4.setText(_translate("ModulaceWindow", "Kolika stavová modulace:"))
        self.label5.setText(_translate("ModulaceWindow", "Polorovina:"))
        self.label6.setText(_translate("ModulaceWindow", "Promodulovanost [%]:"))
        self.label7.setText(_translate("ModulaceWindow", "Vzorkovací frekvence:"))
        self.lEvlastniSekvence.setToolTip(_translate("MainWindow", "<html><head/><body><p>Ukazuje aktuální sekvenci. Při tvorbě vlastní sekvence se píše sem.</p></body></html>"))
        self.cBnbitmodulace.setToolTip(_translate("MainWindow", "<html><head/><body><p>Počet úrovní modulace</p></body></html>"))
        self.lFrekSig.setText(_translate("ModulaceWindow", "Hz"))
        self.lFrekNos.setText(_translate("ModulaceWindow", "Hz"))
        self.lFrekVzork.setText(_translate("ModulaceWindow", "Hz"))
        self.lOpakovani.setText(_translate("ModulaceWindow", "Počet vzorků:"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()
    width =  size.width()
    height = size.height()

    ModulaceWindow = QtWidgets.QMainWindow()
    ui = Ui_ModulaceWindow()
    ui.setupUi(ModulaceWindow, width, height)
    ModulaceWindow.show()
    sys.exit(app.exec_())
