import string
import numpy as np
from scipy import signal

sample_rate = 600e3

"""
Různé funkce
"""
def ProZobrazeniFFT(Signal, N, Fs) -> float: # Vypočítá FFT a vrátí i osu f
    FFT = np.fft.fftshift(np.fft.fft(Signal,N))**2
    FFT_Mag = 10*np.log10(np.abs((FFT))**2 + 10**(-100))
    f = np.arange(Fs / -2, Fs / 2, Fs / N)
    
    kladneFrek = np.arange(1,np.floor(N/2),dtype='int')

    return FFT_Mag, f, kladneFrek

def StejnyZacatekKonec(samples, opakovani) -> complex: # začátek a konce signálu budou stejný
    # zacatekLen = int(opakovani/2) # Přidá na začátek
    # konceLen = opakovani - zacatekLen # Přidá na konce
    # samples = np.concatenate((np.repeat(samples[0],zacatekLen), samples))
    # samples = np.concatenate((samples, np.repeat(samples[0],konceLen)))
    samples = np.concatenate((samples, np.repeat(samples[0], opakovani)))
    return samples

def KvalitniDecimace(samples, opakovani): # Vybere vzorek
    dSamples = np.diff(np.real(samples))

    start = np.argmin(np.abs(dSamples[0:opakovani+5]-0))

    out = np.zeros(int(np.floor(len(samples)/opakovani)),dtype=complex)
    for i in np.arange(int(np.floor(len(samples)/opakovani))):
        if i*opakovani+start > len(samples):
            break
        
        if i == 0 and start < 4:
            start2 = np.argmin(np.abs(dSamples[i*opakovani+start:i*opakovani+start+4]))
        else:
            start2 = np.argmin(np.abs(dSamples[i*opakovani+start-4:i*opakovani+start+4]))
        if start == start2+4:
            out = samples[i*opakovani+start]
            pass
        else:
            out[i] = np.array(samples[i*opakovani+start2])
            start += int(((start + start2 - 4) - start)/2)

    out = Normovani(out)
    posunReal = (np.max(np.real(out)) + np.min(np.real(out))) / 2
    posunImag = (np.max(np.imag(out)) + np.min(np.imag(out))) / 2
    out += - posunReal - 1j * posunImag
    return out

def VyberVzorkuFSK(samples, opakovani): # Podle kritéria vybere jeden vzorek za jeden pulz
    delkaBloku = len(samples) / opakovani # Určení délky bloku na základě počtu opakování symbolu

    """
    Určení nejvhodnějšího místa pro odebrání vzorků - hledá se nejmenší rozdíl mezi 2 pokusnými vzorky
    """
    delta1 = np.abs(samples[10] - samples[20])
    delta2 = np.abs(samples[20] - samples[40])
    if delta1 <= delta2:
        a = 10
        b = 20
    elif delta2 < delta1:
        a = 20
        b = 40

    """
    Extrakce vzorků ze signálu
    """
    bit = np.zeros(int(delkaBloku), dtype=int)
    for i in np.arange(delkaBloku-1, dtype=int):
        if b+(opakovani*i) <= len(samples):
            bit[i] = (samples[a+(opakovani*i)] + samples[b+(opakovani*i)]) / 2
        else: break

    return bit

def NormovaniReal(signal): # Normuje pouze real část komplexního čísla
    if np.abs(min(np.real(signal))) > max(np.real(signal)):
         signal = signal / np.abs(min(np.real(signal)))
    elif np.abs(min(np.real(signal))) <= max(np.real(signal)):
        signal = signal/max(np.real(signal))
    
    return signal

def Normovani(signal): # Vzdálenost od středu budu max 1
    absMax = max(abs(signal))
    signal = signal / absMax
    
    return signal

def NormovaniAbs(signal): # Normování vzdálenosti od počátku souřadného systému
    return signal/np.max(np.abs(signal))

def StartStopSymbol(n): # Výběr start a stop symbolu podle počtu úrovní
    if n < 8:
        startSymbol = "##"
        stopSymbol = '~~'
    if n == 8:
        startSymbol = "~"
        stopSymbol = '/'
    return startSymbol, stopSymbol

def PrevodStartStopSymbolu(n): # Převede Start a stop symboly do vhodné soustavy
    # Vytvoření proměnné pro převod do soustav
    if n >= 4: startSymbolPrevedeny = np.zeros(4, dtype=int)
    if n == 2: startSymbolPrevedeny = np.zeros(8, dtype=int)
    if n >= 4: stopSymbolPrevedeny = np.zeros(4, dtype=int)
    if n == 2: stopSymbolPrevedeny = np.zeros(8, dtype=int)

    if n == 8: 
        startSymbolPrevedeny = DecimalTo8(ord('~'), 4*(0+1)-1, startSymbolPrevedeny)
        stopSymbolPrevedeny = DecimalTo8(ord('/'), 4*(0+1)-1, stopSymbolPrevedeny)
    if n == 4: 
        startSymbolPrevedeny = DecimalTo4(ord('#'), 4*(0+1)-1, startSymbolPrevedeny)
        stopSymbolPrevedeny = DecimalTo4(ord('~'), 4*(0+1)-1, stopSymbolPrevedeny)
    if n == 2: 
        startSymbolPrevedeny = DecimalToBinary(ord('#'), 8*(0+1)-1, startSymbolPrevedeny)
        stopSymbolPrevedeny = DecimalToBinary(ord('~'), 8*(0+1)-1, stopSymbolPrevedeny)

    return startSymbolPrevedeny, stopSymbolPrevedeny

def UpravaProVysilani(signal): # Upravý signál do rozsahu pro Pluto (+-2^14)
    # Vybere, která ze ložek je větší a tou udělá normalizaci signálu
    if np.real(max(signal)) >= np.imag(max(signal)): signal = signal/np.real(max(signal)) 
    if np.real(max(signal)) <= np.imag(max(signal)): signal = signal/np.imag(max(signal)) 
    signal *= 2**14
    return signal

def DecimalToBinary(num, i, out): # Převod do dvodjkové soustavy
    if num >= 1:
        out = DecimalToBinary(num // 2, i-1, out)
    out[i] = num % 2
    return out

def DecimalTo4(num, i, out): # Převod do čtyřkové soustavy
    if num >= 3:
        out = DecimalTo4(num // 4, i-1, out)
    out[i] = num % 4
    return out    

def DecimalTo8(num, i, out): # Převod do osmičkové soustavy
    if num >= 7:
        out = DecimalTo8(num // 8, i-1, out)
    out[i] = num % 8
    return out 

def NalezeniStartSymbolu(n, bit, startSymbol, stopSymbol): # Nalezne start symbol (šlo by to předělat na univerzální vyhledávání symbolů)
    # Vytvoření proměnné pro převod do soustav
    startSymbol_ascii = np.zeros(len(startSymbol), dtype=int)
    if n == 2: startSymbol_bin = np.zeros(8*len(startSymbol), dtype=int)
    if n == 4: startSymbol_bin = np.zeros(4*len(startSymbol), dtype=int)
    if n == 8: startSymbol_bin = np.zeros(4*len(startSymbol), dtype=int)

    i = 0
    for pismeno in startSymbol: #Převedení do používané soustavy, ale jen start byte
        startSymbol_ascii[i] = ord(pismeno)
        if n == 2: text_bin = DecimalToBinary(startSymbol_ascii[i], 8*(i+1)-1, startSymbol_bin)
        if n == 4: text_bin = DecimalTo4(startSymbol_ascii[i], 4*(i+1)-1, startSymbol_bin)
        if n == 8: text_bin = DecimalTo8(startSymbol_ascii[i], 4*(i+1)-1, startSymbol_bin)
        i += 1

    """
    Samotné hledání StartByte v signálu
    """
    korelace = signal.correlate(startSymbol_bin,bit)
    korelace = np.flip(korelace) # Pro správné použití je třeba otočit

    # Naleznou se 3 největší shody
    nalezeno = np.zeros(3, dtype=int)
    nalezeno[0] = np.argmax(korelace)
    korelace[nalezeno[0]] = -korelace[nalezeno[0]]
    nalezeno[1] = np.argmax(korelace)
    korelace[nalezeno[1]] = -korelace[nalezeno[1]]
    nalezeno[2] = np.argmax(korelace)
    korelace[nalezeno[2]] = -korelace[nalezeno[2]]

    return bit, startSymbol_bin, nalezeno

def opravaKorelace(bit, pozice, startSymbolPrevedeny): # Opravý korelaci, aby jsem přesně věděl, kde začíná věta
    start =  - 20
    stop =  20
    if pozice < 20: # Aby jsem nešahal mimo pole
        start = - pozice
    
    poradi = np.concatenate((np.arange(0,stop), np.arange(start,0))) # Upřednostnění nalezení začátku dále než zpětně

    for i in poradi: # Hledání StartByte v rozsahu kolem korelace
        ramec = bit[pozice+i:pozice+i+len(startSymbolPrevedeny)]
        if np.array_equal(ramec,startSymbolPrevedeny):
            return pozice+i-1
    return pozice

def VyhodnoceniZprav(veta): # Vyhodnotí převedené pakety na text
    if veta[0] == veta[1]:
        out = veta[0]
        kolik = 2
        if veta[0] == veta[2]:
            kolik = 3
    elif veta[1] == veta[2]:
        out = veta[1]
        kolik = 2
        if veta[0] == veta[2]:
            kolik = 3
    elif veta[0] == veta[2]:
        out = veta[2]
        kolik = 2
        if veta[0] == veta[1]:
            kolik = 3
    elif veta[0] == '' and veta[1] == '':
        out = veta[2]
        kolik = 1
    elif veta[1] == '' and veta[2] == '':
        out = veta[0]
        kolik = 1
    elif veta[0] == '' and veta[2] == '':
        out = veta[1]
        kolik = 1
    else:
        out = ''
        kolik = 1
    print(veta)
    return out, kolik

def VysilanaVeta2(bit, startSymbol_bin, nalezeno, n): # Mezi start symboly převede bity na symboly
    necelaVeta = True
    dalsiByte = -8
    veta = ['','','']
    zacatek = False # Značí nalezení StartByte
    l = 0 # Značí počet průchodů
    print(nalezeno)
    nalezeno[0] = opravaKorelace(bit,nalezeno[0], startSymbol_bin) # Dojde k opravě korelace, protože ukazuje o kus vedle
    
    for i in np.arange(3):
        if nalezeno[i] <= 6:
            nalezeno[i] = 7

    while necelaVeta:
        nalezenyByte = bit[nalezeno[l]+1+dalsiByte:nalezeno[l]+1+len(startSymbol_bin)+dalsiByte] # Vybrání jedno rámce
        
        """
        Převod na decimální hodnotu
        """
        dec = 0
        k = 7
        for i in np.arange(8):
            dec = dec + nalezenyByte[i] * n**k
            k -= 1
        
        """
        Vyhodnocení rámce
        """
        if chr(dec) != "#" and chr(dec) != "~": # Je to písmeno
            if zacatek: veta[l] = veta[l] + chr(dec)
        elif chr(dec) == "#": # Je to StartByte
            zacatek = True
        elif chr(dec) == "~" and  dalsiByte!= 0 and dalsiByte!= -8: # Je to StopByte
            l += 1
            if l == 3: break # Ukončí se převod, pokud už to proběhlo 3x
            
            nalezeno[l] = opravaKorelace(bit,nalezeno[l-1]+dalsiByte, startSymbol_bin) # Podívám se za vetu, jestli je tam další
            dalsiByte = -8
            zacatek = False            

        if dalsiByte >= 512 or nalezeno[l]+1+len(startSymbol_bin)+dalsiByte+8 > len(bit): # Nenašel jsem StopByte nebo jsem mimo signál
            print(veta[l])
            veta[l] = ''
            print(dalsiByte)           
            l += 1
            if l == 3: break # Ukončí se převod, pokud už to proběhlo 3x
            nalezeno[l] = opravaKorelace(bit,nalezeno[l], startSymbol_bin) # Oprava další hodnoty z korelace pro další pokus
            dalsiByte = -8
            zacatek = False
        dalsiByte += 8

    """
    Vyhodnocení přijmuté zprávy
    """
    out, kolik = VyhodnoceniZprav(veta)
   
    return out, kolik

def VysilanaVeta4(bit, startSymbol_bin, nalezeno, n): # Mezi start symboly převede bity na symboly
    necelaVeta = True
    dalsiByte = 0
    veta = ['','','']
    zacatek = False # Značí nalezení StartByte
    l = 0 # Značí počet průchodů
    print(nalezeno)
    nalezeno[0] = opravaKorelace(bit,nalezeno[0], startSymbol_bin) # Dojde k opravě korelace, protože ukazuje o kus vedle

    while necelaVeta:
        nalezenyByte = bit[nalezeno[l]+1+dalsiByte:nalezeno[l]+1+len(startSymbol_bin)+dalsiByte] # Vyslaný bit nalezený bez lagu
        
        """
        Převod na decimální hodnotu
        """
        dec = 0
        k = 3
        for i in np.arange(4):
            dec = dec + nalezenyByte[i] * n**k
            k -= 1

        """
        Vyhodnocení rámce
        """
        if chr(dec) != "#" and chr(dec) != "~": # Je to písmeno
            if zacatek: veta[l] = veta[l] + chr(dec)
        elif chr(dec) == "#": # Je to StartByte
            zacatek = True
        elif chr(dec) == "~" and  dalsiByte!= 0 and dalsiByte!= -4: # Je to StopByte
            l += 1
            if l == 3: break # Ukončí se převod, pokud už to proběhlo 3x

            nalezeno[l] = opravaKorelace(bit,nalezeno[l-1]+dalsiByte, startSymbol_bin) # Podívám se za vetu, jestli je tam další
            dalsiByte = -4
            zacatek = False
                    
        if dalsiByte >= 512 or nalezeno[l]+1+len(startSymbol_bin)+dalsiByte+4 > len(bit): # Nenašel jsem StopByte nebo jsem mimo signál
            veta[l] = ''
            print(dalsiByte)
            l += 1
            if l == 3: break

            nalezeno[l] = opravaKorelace(bit,nalezeno[l], startSymbol_bin) # Oprava další hodnoty z korelace pro další pokus
            dalsiByte = -4
            zacatek = False
        dalsiByte += 4

    """
    Vyhodnocení přijmuté zprávy
    """
    out, kolik = VyhodnoceniZprav(veta)

    return out, kolik

def VysilanaVeta8(bit, startSymbol_bin, nalezeno, n): # Mezi start symboly převede bity na symboly
    necelaVeta = True
    dalsiByte = -4
    veta = ['','','']
    zacatek = False # Značí nalezení StartByte
    l = 0 # Značí počet průchodů
    print(nalezeno)
    nalezeno[0] = opravaKorelace(bit,nalezeno[0], startSymbol_bin) # Dojde k opravě korelace, protože ukazuje o kus vedle
    
    for i in np.arange(3):
        if nalezeno[i] <= 2:
            nalezeno[i] = 3

    while necelaVeta:
        nalezenyByte = bit[nalezeno[l]+1+dalsiByte:nalezeno[l]+1+len(startSymbol_bin)+dalsiByte] # Vyslaný bit nalezený bez lagu
        
        """
        Převod na decimální hodnotu
        """
        dec = 0
        k = 3
        for i in np.arange(4):
            dec = dec + nalezenyByte[i] * n**k
            k -= 1

        """
        Vyhodnocení rámce
        """
        if chr(dec) != "~" and chr(dec) != "/": # Je to písmeno
           if zacatek: veta[l] = veta[l] + chr(dec)
        elif chr(dec) == "~": # Je to StartByte             
            zacatek = True
        elif chr(dec) == "/" and  dalsiByte!= 0 and dalsiByte!= -4: # Je to StopByte
            l += 1
            if l == 3: break # Ukončí se převod, pokud už to proběhlo 3x
            
            nalezeno[l] = opravaKorelace(bit,nalezeno[l-1]+dalsiByte, startSymbol_bin) # Podívám se za vetu, jestli je tam další
            dalsiByte = -4
            zacatek = False
        
        if dalsiByte >= 512 or nalezeno[l]+1+len(startSymbol_bin)+dalsiByte+4 > len(bit): # Nenašel jsem StopByte nebo jsem mimo signál
            veta[l] = ''
            print(dalsiByte)
            l += 1
            if l == 3: break # Ukončí se převod, pokud už to proběhlo 3x

            nalezeno[l] = opravaKorelace(bit,nalezeno[l], startSymbol_bin) # Oprava další hodnoty z korelace pro další pokus
            dalsiByte = -4
            zacatek = False
        dalsiByte += 4
    
    """
    Vyhodnocení přijmuté zprávy
    """
    out, kolik = VyhodnoceniZprav(veta)

    return out, kolik


"""
Modulace
"""
def PokracovaniASK(x,n,k): #Vypočítává hodnoty zesílení pro 4-ASK a větší
    x = x-2 # Snížení na rozsah 0 - 1
    if x <= 1:
        y = (x - 0.5) * (k+2)
    else:
        k = k+2
        y = PokracovaniASK(x,n,k)                    
    return y

def ASK(n, text) -> complex:
    startSymbol, stopSymbol = StartStopSymbol(n)
    opakovani = 30
    # Přidání start a stop symbolu k vysílanému textu
    if n < 8: textKomplet = startSymbol + text + stopSymbol
    if n == 8: textKomplet = startSymbol + text + stopSymbol
    
    """
    Převod na ASCII
    """
    text_ascii = np.zeros(len(textKomplet), dtype=int)
    if n == 4: text_bin = np.zeros(4*len(textKomplet), dtype=int)
    if n == 2: text_bin = np.zeros(8*len(textKomplet), dtype=int)
    if n == 8: text_bin = np.zeros(4*len(textKomplet), dtype=int)

    i = 0
    for pismeno in textKomplet:
        text_ascii[i] = ord(pismeno)
        if n == 2: text_bin = DecimalToBinary(text_ascii[i], 8*(i+1)-1, text_bin)
        if n == 4: text_bin = DecimalTo4(text_ascii[i], 4*(i+1)-1, text_bin)
        if n == 8: text_bin = DecimalTo8(text_ascii[i], 4*(i+1)-1, text_bin)
        i += 1
    
    """
    Samotná modulace
    """
    xInt = text_bin

    xAmp = xInt / (n - 1) + 0.5 # Posun do pravé poloroviny

    xSymbols = xAmp * (np.cos(0) + 1j * np.sin(0))  # Vytvoří complexní symbol
    samples = np.repeat(xSymbols, opakovani)
    samples = StejnyZacatekKonec(samples, opakovani)

    """
    Pulse shaping
    """
    # t = np.arange(0, len(samples)/sample_rate,1/sample_rate)
    # samples1 = np.real(samples)*np.cos(2*np.pi*100000.0*t) + 1.0j*np.imag(samples)*np.sin(2*np.pi*100000.0*t)

    b, a = signal.butter(15, 80000/sample_rate)
    x_shaped = signal.filtfilt(b, a, samples)
    
    samples = x_shaped

    # samples = UpravaProVysilani(samples1)

    # print(xInt)
    return UpravaProVysilani(samples)

def PSK(n, text) -> complex:    
    startSymbol, stopSymbol = StartStopSymbol(n)
    opakovani = 25
    # Přidání start a stop symbolu k vysílanému textu
    if n < 8: textKomplet = startSymbol + text + stopSymbol
    if n == 8: textKomplet = startSymbol + text + stopSymbol

    """
    Převod na ASCII
    """
    text_ascii = np.zeros(len(textKomplet), dtype=int)
    if n == 4: text_bin = np.zeros(4*len(textKomplet), dtype=int)
    if n == 2: text_bin = np.zeros(8*len(textKomplet), dtype=int)
    if n == 8: text_bin = np.zeros(4*len(textKomplet), dtype=int)

    i = 0
    for pismeno in textKomplet:
        text_ascii[i] = ord(pismeno)
        if n == 2: text_bin = DecimalToBinary(text_ascii[i], 8*(i+1)-1, text_bin)
        if n == 4: text_bin = DecimalTo4(text_ascii[i], 4*(i+1)-1, text_bin)
        if n == 8: text_bin = DecimalTo8(text_ascii[i], 4*(i+1)-1, text_bin)
        i += 1

    """
    Samotná modulace
    """
    xInt = text_bin

    if n == 4:
        xDegrees = xInt * 360 / 4.0 + 45  # 45, 135, 225, 315 stupňů
    else:
        xDegrees = xInt * 360 / n
    xRadians = xDegrees * np.pi / 180.0
    
    if n == 2:
        xSymbols = np.cos(xRadians) + 1j * np.floor(np.sin(xRadians))
    else:
        xSymbols = np.cos(xRadians) + 1j * np.sin(xRadians) 
    samples = np.repeat(xSymbols, opakovani)
    samples = StejnyZacatekKonec(samples, opakovani)

    """
    Pulse shaping
    """
    b, a = signal.butter(15, 50000/sample_rate)
    x_shaped = signal.filtfilt(b, a, samples)

    samples = UpravaProVysilani(x_shaped)

    return samples

def FSK(n, text) -> complex:
    startSymbol, stopSymbol = StartStopSymbol(n)
    opakovani = 50
    # Přidání start a stop symbolu k vysílanému textu
    if n < 8: textKomplet = startSymbol + text + stopSymbol
    if n == 8: textKomplet = startSymbol + text + stopSymbol
    
    """
    Převod na ASCII
    """
    text_ascii = np.zeros(len(textKomplet), dtype=int)
    if n == 4: text_bin = np.zeros(4*len(textKomplet), dtype=int)
    if n == 2: text_bin = np.zeros(8*len(textKomplet), dtype=int)
    if n == 8: text_bin = np.zeros(4*len(textKomplet), dtype=int)

    i = 0
    for pismeno in textKomplet:
        text_ascii[i] = ord(pismeno)
        if n == 2: text_bin = DecimalToBinary(text_ascii[i], 8*(i+1)-1, text_bin)
        if n == 4: text_bin = DecimalTo4(text_ascii[i], 4*(i+1)-1, text_bin)
        if n == 8: text_bin = DecimalTo8(text_ascii[i], 4*(i+1)-1, text_bin)
        i += 1

    """
    Samotná modulace
    """
    xInt_n = text_bin
    carrierFreq = 80000
    Delta_f = 3000
       
    xInt = np.repeat(xInt_n, opakovani)

    f = (carrierFreq + Delta_f * xInt - (n * Delta_f)/2) + Delta_f/2
    delta_phi = f * np.pi / (sample_rate / 2.0)
    phi = np.cumsum(delta_phi)
    samples = np.cos(phi) + 1j*np.sin(phi)

    return UpravaProVysilani(samples)

def QAM(n, text) -> complex:
    startSymbol, stopSymbol = StartStopSymbol(n)
    opakovani = 25
    # Přidání start a stop symbolu k vysílanému textu
    if n < 8: textKomplet = startSymbol + text + stopSymbol
    if n == 8: textKomplet = startSymbol + text + stopSymbol
    
    """
    Převod na ASCII
    """
    text_ascii = np.zeros(len(textKomplet), dtype=int)
    if n == 4: text_bin = np.zeros(4*len(textKomplet), dtype=int)
    if n == 2: text_bin = np.zeros(8*len(textKomplet), dtype=int)
    if n == 8: text_bin = np.zeros(4*len(textKomplet), dtype=int)

    i = 0
    for pismeno in textKomplet:
        text_ascii[i] = ord(pismeno)
        if n == 2: text_bin = DecimalToBinary(text_ascii[i], 8*(i+1)-1, text_bin)
        if n == 4: text_bin = DecimalTo4(text_ascii[i], 4*(i+1)-1, text_bin)
        if n == 8: text_bin = DecimalTo8(text_ascii[i], 4*(i+1)-1, text_bin)
        i += 1

    """
    Samotná modulace
    """
    xInt = text_bin

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

    samples = np.repeat(xSymbols, opakovani)
    samples = StejnyZacatekKonec(samples, opakovani)

    """
    Pulse shaping
    """
    b, a = signal.butter(15, 50000/sample_rate)
    x_shaped = signal.filtfilt(b, a, samples)

    samples = UpravaProVysilani(x_shaped)
    return samples

def AM(carrierFreq, frekvenceMin, modulation_index, signal) -> complex:
    t = np.arange(0,2/frekvenceMin,1/sample_rate)
    signal = signal + 0j

    xRadians = 2 * np.pi * t
    cosCarrier = np.cos(carrierFreq * xRadians) + 1j * np.sin(carrierFreq * xRadians)
    # samples = A_c * (1 + modulation_index * (signal)) * cosCarrier
    samples = modulation_index * signal * cosCarrier + cosCarrier # Modulace
  
    samples = UpravaProVysilani(samples)
    return samples

def FM(carrierFreq, frekvenceMin, D_f, signal) -> complex:
    # t = np.arange(0,2/frekvenceMin,1/sample_rate)
    
    # samples = np.cos(2*np.pi*carrierFreq*t + D_f*signal) + 1j * np.sin(2*np.pi*carrierFreq*t + D_f*signal)

    f = carrierFreq + 1000 * (signal)
    delta_phi = f * np.pi / (sample_rate / 2.0)
    phi = np.cumsum(delta_phi) # Kumulativní suma
    samples = 1*np.cos(phi) + 1j * np.sin(phi)

    return UpravaProVysilani(samples)


"""
Demodulace
"""
def dASK(samples, n) -> string: 
    startSymbol, stopSymbol = StartStopSymbol(n)
    startSymbolPrevedeny, stopSymbolPrevedeny = PrevodStartStopSymbolu(n)
    opakovani = 30

    # Filtrace
    b, a = signal.butter(15, 80000/sample_rate)
    samples = signal.filtfilt(b, a, samples)

    # Vyber vzorků
    vytazek = []
    for i in np.arange(len(samples)/opakovani):
        vytazek.append(np.real(samples[int(i*opakovani+5)]))
    vytazek = - NormovaniReal(np.array(vytazek))

    posunReal = (np.max(np.real(vytazek)) + np.min(np.real(vytazek))) / 2
    vytazek += - posunReal
    samples = NormovaniReal(np.array(vytazek))

    """
    Vyhodnocení
    """
    i = 0
    bit = []

    if n == 2:
        for s in samples:
            if s > 0.5 and s < 1.1: bit.append(1)
            elif s < 0 and s > -1.1: bit.append(0)
            i += 1 
    if n == 4:
        for s in samples:
            if s > 0 and s <= 0.5: bit.append(2)
            elif s >= 0.5 and s < 1.1: bit.append(3)
            elif s > -0.5 and s < 0: bit.append(1)
            elif s > -1.1 and s < -0.5: bit.append(0)
            i += 1 
    if n == 8:
        for s in samples:
            if s > -0.72 and s <= -0.4: bit.append(1)
            elif s >= -1.1 and s < -0.72: bit.append(0)
            elif s > -0.25 and s < 0: bit.append(3)
            elif s > -0.4 and s < -0.25: bit.append(2)
            elif s > 0.25 and s < 0.45: bit.append(5)
            elif s > 0 and s < 0.25: bit.append(4)
            elif s > 0.75 and s < 1.1: bit.append(7)
            elif s > 0.45 and s < 0.75: bit.append(6)
            i += 1     

    """
    Nalezení startu a vyhodnocení, co je mezi startem a StopBytem
    """
    bit, startSymbol_bin, nalezeno = NalezeniStartSymbolu(n, bit, startSymbol, stopSymbol)
    if n == 2: out, kolik = VysilanaVeta2(bit, startSymbol_bin, nalezeno, n)
    if n == 4: out, kolik = VysilanaVeta4(bit, startSymbol_bin, nalezeno, n)
    if n == 8: out, kolik = VysilanaVeta8(bit, startSymbol_bin, nalezeno, n)

    return out, kolik

def dPSK(samples, n) -> string:
    opakovani = 25
    startSymbol, stopSymbol = StartStopSymbol(n)

    # Filtrace
    b, a = signal.butter(15, 80000/sample_rate)
    samples = signal.filtfilt(b, a, samples)

    # Výběr vzorku
    # samples = KvalitniDecimace(samples, opakovani)

    vytazek = []
    for i in np.arange(len(samples)/opakovani):
        vytazek.append(samples[int(i*opakovani+5)])
    vytazek = Normovani(np.array(vytazek))

    posunReal = (np.max(np.real(vytazek)) + np.min(np.real(vytazek))) / 2
    posunImag = (np.max(np.imag(vytazek)) + np.min(np.imag(vytazek))) / 2
    vytazek += - posunReal - 1j * posunImag
    samples = vytazek

    # Příprava na vyhodnocení
    kdeNula = np.where(samples == 0) # Najde všechny nuly v poly
    samples = np.delete(samples, kdeNula) # Odebere všechny 0 v poli

    otoc = np.repeat(np.exp(1j*(np.pi/2+np.pi/14)), len(samples)) # OPrava konstelace
    samples = samples*otoc

    uhel = np.angle(samples)

    """
    Vyhodnocení
    """
    bit = np.zeros(len(uhel), dtype=int)
    if n == 2:
        for i in np.arange(len(uhel)):
            if uhel[i] < 0: uhel[i] += 2*np.pi

            if uhel[i] >= 3/2*np.pi and uhel[i] <= np.pi/2: bit[i] = 0
            if uhel[i] >= np.pi/2 and uhel[i] <= 3/2*np.pi: bit[i] = 1
    a = 0
    if n == 4:
        for i in np.arange(len(uhel)):
            if uhel[i] < 0: uhel[i] += 2*np.pi
            if np.abs(samples[i]) > 0.3:
                if uhel[i] >= 0 and uhel[i] <= np.pi/2: bit[a] = 0
                elif uhel[i] >= np.pi/2 and uhel[i] <= np.pi: bit[a] = 1
                elif uhel[i] >= np.pi and uhel[i] <= 1.5*np.pi: bit[a] = 2
                elif uhel[i] >= 1.5*np.pi and uhel[i] <= 2*np.pi: bit[a] = 3
                a += 1      
    if n == 8:
        for i in np.arange(len(uhel)):
            if uhel[i] < 0: uhel[i] += 2*np.pi

            if uhel[i] >= 0 and uhel[i] <= np.pi/8 or uhel[i] >= 15/8*np.pi and uhel[i] <= 2*np.pi: bit[i] = 0
            elif uhel[i] >= np.pi/8 and uhel[i] <= 3/8*np.pi+0.09: bit[i] = 1
            elif uhel[i] >= 3/8*np.pi+0.09 and uhel[i] <= 5/8*np.pi: bit[i] = 2
            elif uhel[i] >= 5/8*np.pi and uhel[i] <= 7/8*np.pi: bit[i] = 3
            elif uhel[i] >= 7/8*np.pi and uhel[i] <= 9/8*np.pi: bit[i] = 4
            elif uhel[i] >= 9/8*np.pi and uhel[i] <= 11/8*np.pi: bit[i] = 5
            elif uhel[i] >= 11/8*np.pi and uhel[i] <= 13/8*np.pi: bit[i] = 6
            elif uhel[i] >= 13/8*np.pi and uhel[i] <= 15/8*np.pi: bit[i] = 7   

    """
    Nalezení startu a vyhodnocení, co je mezi startem a StopBytem
    """
    bit, startSymbol_bin, nalezeno = NalezeniStartSymbolu(n, bit, startSymbol, stopSymbol)
    if n == 2: out, kolik = VysilanaVeta2(bit, startSymbol_bin, nalezeno, n)
    if n == 4: out, kolik = VysilanaVeta4(bit, startSymbol_bin, nalezeno, n)
    if n == 8: out, kolik = VysilanaVeta8(bit, startSymbol_bin, nalezeno, n)

    return str(out), kolik

def dFSK(samples, n) -> string:
    samples = np.real(samples)
    opakovani = 50

    # b, a = signal.butter(7, [50000/sample_rate, 150000/sample_rate], 'bandpass')
    # samples = signal.filtfilt(b, a, samples)

    """
    Hilbertova transformace
    """
    analytic_signal = signal.hilbert(samples)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0*np.pi) * sample_rate)

    # Výběr vzorku
    vzorek = VyberVzorkuFSK(instantaneous_frequency[100:len(instantaneous_frequency)], opakovani)
    samples = vzorek - np.min(vzorek) # Nejnižší hodnota je nově považována za 0
    samples = Normovani(np.abs(samples))

    """
    Vyhodnocení
    """
    startSymbol, stopSymbol = StartStopSymbol(n)
    bit = []
    if n == 2:
        for i in samples:
            if i < 0.5 and i > 0:
                bit.append(0)
            elif i < 1.0 and i > 0.5:
                bit.append(1)
    if n == 4:
        for i in samples:
            if i < 0.13 and i > 0:
                bit.append(0)
            elif i < 0.38 and i > 0.13:
                bit.append(1)
            elif i < 0.7 and i > 0.38:
                bit.append(2)
            elif i < 1.0 and i > 0.7:
                bit.append(3)
    if n == 8:
        for i in samples:
            if i < 0.12 and i > 0:
                bit.append(0)
            elif i < 0.22 and i > 0.12:
                bit.append(1)
            elif i < 0.35 and i > 0.22:
                bit.append(2)
            elif i < 0.52 and i > 0.35:
                bit.append(3)
            elif i < 0.66 and i > 0.52:
                bit.append(4)
            elif i < 0.79 and i > 0.66:
                bit.append(5)
            elif i < 0.91 and i > 0.79:
                bit.append(6)
            elif i < 1.0 and i > 0.91:
                bit.append(7)
    
    """
    Nalezení startu a vyhodnocení, co je mezi startem a StopBytem
    """
    bit, startSymbol_bin, nalezeno = NalezeniStartSymbolu(n, bit, startSymbol, stopSymbol)
    if n == 2: out, kolik = VysilanaVeta2(bit, startSymbol_bin, nalezeno, n)
    if n == 4: out, kolik = VysilanaVeta4(bit, startSymbol_bin, nalezeno, n)
    if n == 8: out, kolik = VysilanaVeta8(bit, startSymbol_bin, nalezeno, n)
    return out, kolik

def dQAM(samples, n):
    opakovani = 25
    startSymbol, stopSymbol = StartStopSymbol(n)

    # Filtrace
    b, a = signal.butter(4, 70000/sample_rate)
    samples = signal.filtfilt(b, a, samples)

    # Vybrání vzorku
    vytazek = []
    for i in np.arange(len(samples)/opakovani):
        vytazek.append(samples[int(i*opakovani+5)])
    vytazek = Normovani(np.array(vytazek))

    posunReal = (np.max(np.real(vytazek)) + np.min(np.real(vytazek))) / 2
    posunImag = (np.max(np.imag(vytazek)) + np.min(np.imag(vytazek))) / 2
    vytazek += - posunReal - 1j * posunImag
    samples =  vytazek

    # Příprava před vyhodnocením
    kdeNula = np.where(samples == 0) # Najde všechny nuly v poly
    samples = np.delete(samples, kdeNula) # Odebere všechny 0 v poli

    otoc = np.repeat(np.exp(1j*(np.pi/2+np.pi/14)), len(samples)) #/16 pro n=4
    samples = samples*otoc
    uhel = np.angle(samples)

    """
    Vyhodnocení
    """
    bit = np.zeros(len(uhel), dtype=int)
    a = 0
    if n == 4:
        for i in np.arange(len(uhel)):
            if uhel[i] < 0: uhel[i] += 2*np.pi
            if np.abs(samples[i]) > 0.3:
                if uhel[i] >= 0 and uhel[i] <= np.pi/2: bit[a] = 0
                elif uhel[i] >= np.pi/2 and uhel[i] <= np.pi: bit[a] = 1
                elif uhel[i] >= np.pi and uhel[i] <= 1.5*np.pi: bit[a] = 2
                elif uhel[i] >= 1.5*np.pi and uhel[i] <= 2*np.pi: bit[a] = 3
                a += 1
            
    if n == 8:
        for i in np.arange(len(uhel)):
            if uhel[i] < 0: uhel[i] += 2*np.pi
            if np.abs(samples[i]) > 0.0:
                if uhel[i] >= 0 and uhel[i] <= np.pi/2: 
                    if np.abs(samples[i]) < 0.5: bit[a] = 0
                    else: bit[a] = 4
                elif uhel[i] >= np.pi/2 and uhel[i] <= np.pi:
                    if np.abs(samples[i]) < 0.5: bit[a] = 1
                    else: bit[a] = 5
                elif uhel[i] >= np.pi and uhel[i] <= 1.5*np.pi:
                    if np.abs(samples[i]) < 0.5: bit[a] = 2
                    else: bit[a] = 6
                elif uhel[i] >= 1.5*np.pi and uhel[i] <= 2*np.pi: 
                    if np.abs(samples[i]) < 0.5: bit[a] = 3
                    else: bit[a] = 7
                a += 1  

    """
    Nalezení startu a vyhodnocení, co je mezi startem a StopBytem
    """
    bit, startSymbol_bin, nalezeno = NalezeniStartSymbolu(n, bit, startSymbol, stopSymbol)
    if n == 4: out, kolik = VysilanaVeta4(bit, startSymbol_bin, nalezeno, n)
    if n == 8: out, kolik = VysilanaVeta8(bit, startSymbol_bin, nalezeno, n)

    return out, kolik

def dAM(samples) -> float:
    samples = np.real(samples)

    # b, a = signal.butter(7, [60000/sample_rate, 140000/sample_rate], 'bandpass')
    # samples = signal.filtfilt(b, a, samples)

    """
    Hilbertova transformace
    """
    analytic_signal = signal.hilbert(samples)
    amplitude_envelope = np.abs(analytic_signal)
    amplitude_envelope -= np.mean(amplitude_envelope)

    # Filtrace demodulovaného signálu
    b, a = signal.butter(7, 35000/sample_rate)
    amplitude_envelope = signal.filtfilt(b, a, amplitude_envelope)
    out = NormovaniAbs(amplitude_envelope)
    samples = signal.filtfilt(b, a, out)
    return samples[100:len(samples)-50]    

def dFM(samples, carrierFreq) -> float:
    # samples = signal.filtfilt(b, a, samples)
    
    """
    Hilbertova transformace
    """
    samples = np.real(samples)
    analytic_signal = signal.hilbert(samples)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0*np.pi) * sample_rate) - carrierFreq
    
    # Filtrace demodulovaného signálu
    b, a = signal.butter(7, 35000/sample_rate)
    instantaneous_frequency = signal.filtfilt(b, a, instantaneous_frequency)

    out = NormovaniAbs(instantaneous_frequency[100:len(instantaneous_frequency)-100])

    return out