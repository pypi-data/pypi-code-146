
from . import wadapter as wad
wa = wad.wa

DEBUG = wad.DEBUG
#===========BEGIN MODULE FUNCTIONS================#
MCP23017_ADDRESS=0x26
#   Addr(BIN)      Addr(hex)
#XXX X  A2 A1 A0
# short is high
#010 0  1  1  1      0x27
#010 0  1  1  0      0x26
#010 0  1  0  1      0x25
#010 0  1  0  0      0x24
#010 0  0  1  1      0x23
#010 0  0  1  0      0x22
#010 0  0  0  1      0x21
#010 0  0  0  0      0x20
MCP23017_IODIRA = 0x00
MCP23017_IPOLA  = 0x02
MCP23017_GPINTENA = 0x04
MCP23017_DEFVALA = 0x06
MCP23017_INTCONA = 0x08
MCP23017_IOCONA = 0x0A
MCP23017_GPPUA = 0x0C
MCP23017_INTFA = 0x0E
MCP23017_INTCAPA = 0x10
MCP23017_GPIOA = 0x12
MCP23017_OLATA = 0x14

MCP23017_IODIRB = 0x01
MCP23017_IPOLB = 0x03
MCP23017_GPINTENB = 0x05
MCP23017_DEFVALB = 0x07
MCP23017_INTCONB = 0x09
MCP23017_IOCONB = 0x0B
MCP23017_GPPUB = 0x0D
MCP23017_INTFB = 0x0F
MCP23017_INTCAPB = 0x11
MCP23017_GPIOB = 0x13
MCP23017_OLATB = 0x15

def LgetGTmcp(lPins,debug=False):
    #Configue the register to default value
    bus=wa.i2c
    for addr in range(22):
        if (addr == 0) or (addr == 1):
            bus.write_byte_data(MCP23017_ADDRESS, addr, 0xFF)
        else:
            bus.write_byte_data(MCP23017_ADDRESS, addr, 0x00)

    # pb0 is pin1 pa0 is pin16
    pins=lPins
    iodira=0
    iodirb=0 # 0 is in, 1 is out
    pua=0
    pub=0 # 1 is pull up, 0 is no
    gpioa=0
    gpiob=0 # output

    isOut=lambda s: True if s=='H' or s=='L' else False
    asb=[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]
    asa=asb
    for i in range(8):
        if isOut(pins[i]):
            gpiob|=asb[i] if pins[i]=='H' else 0
        else:
            iodirb|=asb[i]
            if pins[i]=='U':
                pub|=asb[i]
        if isOut(pins[i+8]):
            gpioa|=asa[i] if pins[i+8]=='H' else 0
        else:
            iodira|=asa[i]
            if pins[i+8]=='U':
                pua|=asa[i]
    #set io direction and pull up
    bus.write_byte_data(MCP23017_ADDRESS,MCP23017_IODIRB,iodirb)
    bus.write_byte_data(MCP23017_ADDRESS,MCP23017_IODIRA,iodira)
    bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPPUA,pua)
    bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPPUB,pub)

    if debug:
        pua=bus.read_byte_data(MCP23017_ADDRESS,MCP23017_GPPUA)
        pub=bus.read_byte_data(MCP23017_ADDRESS,MCP23017_GPPUB)
        print('pull up: {}, {}'.format(pub,pua))
    if wa.ctag('board'):
        bus.write_to_mem(MCP23017_ADDRESS,MCP23017_GPIOA,(bytearray([gpioa,gpiob])))
    else:
        bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,gpiob)
        bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOA,gpioa)

    if DEBUG:
        wa.Sleep(0.5)
    else:
        wa.Sleep(0.005)
    

    ioa=bus.read_byte_data(MCP23017_ADDRESS,MCP23017_GPIOA)
    iob=bus.read_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB)

    res=list('{:0>8b}'.format(iob))[::-1]+list('{:0>8b}'.format(ioa))[::-1]
    res=''.join(res)

    for i,v in enumerate(pins):
        if not isOut(v):
            pins[i]=res[i]

    ans=pins
    if DEBUG:
        print('Receive:{}'.format(res))
        print('Result:{}'.format(ans))
    return ans
################ Adder ###############
def 烫74283的程getのcheckLogic(args):
    # check if the logic is correct for any p and q string input
    # return a bitwise string representation

    p,q=args

    cout=''
    for a,b in zip(p,q):
        cout+='O' if a==b else 'X'

    if all([i=='O' for i in cout]):
        cout='  OK! '
    ans=cout
    return ans

def AdderQ283(args,debug=False):
    # test 283 logic once
    import random
    if isinstance(args,tuple):
        i=0
        a,b,cin=args
    else:
        i=args # result counter
        a=random.randint(0,15)
        b=random.randint(0,15)
        cin=random.randint(0,1)
    def moniRes():
        l1='{}+{}+{}'.format(a,b,cin)
        rout = a + b + cin if random.randint(0,50) else a + b + cin + random.randint(-5,5)
        l2='→{:>3} '.format(rout)
        l3= 'OK' if rout == a+b+cin else 'Err!'
        sf='*模拟加法器*测试\n入：{}  \n出：{}↑暂停\n   {} ←退出 '.format(l1,l2,l3)
        return sf,(a,b,cin),rout
    if wa.ctag('debug'):
        return moniRes()

    sf='74283加法器测试\n入：{}  \n出：{}↑暂停\n   {} ←退出 '
    #
    l1='{}+{}+{}'.format(a,b,cin)

    sA='{:0>4b}'.format(a)
    sB='{:0>4b}'.format(b)
    
    lA=[11,10,9,8]#[4,2,13,11][::-1]
    lB=[15,14,13,12]#[5,1,14,10][::-1]
    pC=7#6
    lOut=[4,3,2,1,0]#[3,0,12,9,8][::-1]
    vcc=6#15 #
    gnd =5#7
    parg=['-']*16 #initialize pin arg
    #if wa.name == 'zkb':
    #    lB=[12,13,14,15]

    for i,v in enumerate(sA):
        parg[lA[i]]='H' if v=='1' else 'L'
    for i,v in enumerate(sB):
        parg[lB[i]]='H' if v=='1' else 'L'
    parg[pC]='H' if cin==1 else 'L'
    parg[vcc]='H'
    parg[gnd]='L'
    #try:
    #    r=LgetGTmcp(parg)
    #except:
    #    return moniRes()                                                                                                                                                                                                         
    r=LgetGTmcp(parg)
    rout=''
    for p in lOut:
        rout+=r[p]
    if debug:
        print('{sA}+{sB}+{cin}->{rout}'.format(**locals()))
    #print(rout)
    rout=int(rout,2) #

    l2='→{:>3} '.format(rout)

    p='{:0>5b}'.format(a+b+cin)
    q='{:0>5b}'.format(rout)
    if debug:
        print('[{i}] a={a},b={b},cin={cin}: {p} vs {q}'.format(**locals()))
    l3=烫74283的程getのcheckLogic((p,q))

    qin=(a,b,cin)

    ans=sf.format(l1,l2,l3),qin,rout
    return ans
def LoopShow283():
    # test yx logic gates on GTC platform
    # save every hour

    CheckKey=wa.CheckKey
    DispChar=wa.DispChar
    Q=AdderQ283
    ftSave=3600

    k=CheckKey()
    count=0
    pause = False
    idx=1
    lSave=[]
    add=[' ',' .',' ..',' ...']
    #fStart=time.time()
    while k!='L':
        if count%20 == 0 and not pause:
            sf, sIn, sOut=Q(None)
            DispChar(sf)
            idx+=1
        #time.sleep(0.05)
        count+=1
        k=CheckKey()
        if k=='U':
            pause=True
        elif k=='D':
            pause=False
    wa.DispClear()

################ BME280 #######################
class ct():
    def getShort(self,data, index):
    # return two bytes from data as a signed 16-bit value
    #from ctypes import c_short
    #return c_short((data[index+1] << 8) + data[index]).value
        return (data[index+1] << 8) + data[index]

    def getUShort(self,data, index):
    # return two bytes from data as an unsigned 16-bit value
        return (data[index+1] << 8) + data[index]

    def getChar(self,data,index):
    # return one byte from data as a signed char
        result = data[index]
        if result > 127:
            result -= 256
        return result

    def getUChar(self,data,index):
    # return one byte from data as an unsigned char
        result =  data[index] & 0xFF
        return result

cct=ct()

def readBME280ID(addr=0x76,bus=wa.i2c):
  # Chip ID Register Address
  REG_ID     = 0xD0
  (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
  return (chip_id, chip_version)

def readBME280All(addr=0x76, bus=wa.i2c, ct=cct):
  # Register Addresses
  REG_DATA = 0xF7
  REG_CONTROL = 0xF4
  REG_CONFIG  = 0xF5

  REG_CONTROL_HUM = 0xF2
  REG_HUM_MSB = 0xFD
  REG_HUM_LSB = 0xFE

  # Oversample setting - page 27
  OVERSAMPLE_TEMP = 2
  OVERSAMPLE_PRES = 2
  MODE = 1

  # Oversample setting for humidity register - page 26
  OVERSAMPLE_HUM = 2
  bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

  control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
  bus.write_byte_data(addr, REG_CONTROL, control)

  # Read blocks of calibration data from EEPROM
  # See Page 22 data sheet
  cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
  cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
  cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

  # Convert byte data to word values
  dig_T1 = ct.getUShort(cal1, 0)
  dig_T2 = ct.getShort(cal1, 2)
  dig_T3 = ct.getShort(cal1, 4)

  dig_P1 = ct.getUShort(cal1, 6)
  dig_P2 = ct.getShort(cal1, 8)
  dig_P3 = ct.getShort(cal1, 10)
  dig_P4 = ct.getShort(cal1, 12)
  dig_P5 = ct.getShort(cal1, 14)
  dig_P6 = ct.getShort(cal1, 16)
  dig_P7 = ct.getShort(cal1, 18)
  dig_P8 = ct.getShort(cal1, 20)
  dig_P9 = ct.getShort(cal1, 22)

  dig_H1 = ct.getUChar(cal2, 0)
  dig_H2 = ct.getShort(cal3, 0)
  dig_H3 = ct.getUChar(cal3, 2)

  dig_H4 = ct.getChar(cal3, 3)
  dig_H4 = (dig_H4 << 24) >> 20
  dig_H4 = dig_H4 | (ct.getChar(cal3, 4) & 0x0F)

  dig_H5 = ct.getChar(cal3, 5)
  dig_H5 = (dig_H5 << 24) >> 20
  dig_H5 = dig_H5 | (ct.getUChar(cal3, 4) >> 4 & 0x0F)

  dig_H6 = ct.getChar(cal3, 6)

  # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
  wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
  wa.Sleep(wait_time/1000)  # Wait the required time

  # Read temperature/pressure/humidity
  data = bus.read_i2c_block_data(addr, REG_DATA, 8)
  pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
  temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
  hum_raw = (data[6] << 8) | data[7]

  #Refine temperature
  var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
  var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
  t_fine = var1+var2
  temperature = float(((t_fine * 5) + 128) >> 8);

  # Refine pressure and adjust for temperature
  var1 = t_fine / 2.0 - 64000.0
  var2 = var1 * var1 * dig_P6 / 32768.0
  var2 = var2 + var1 * dig_P5 * 2.0
  var2 = var2 / 4.0 + dig_P4 * 65536.0
  var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
  var1 = (1.0 + var1 / 32768.0) * dig_P1
  if var1 == 0:
    pressure=0
  else:
    pressure = 1048576.0 - pres_raw
    pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
    var1 = dig_P9 * pressure * pressure / 2147483648.0
    var2 = pressure * dig_P8 / 32768.0
    pressure = pressure + (var1 + var2 + dig_P7) / 16.0

  # Refine humidity
  humidity = t_fine - 76800.0
  humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
  humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
  if humidity > 100:
    humidity = 100
  elif humidity < 0:
    humidity = 0

  return temperature/100.0,pressure/100.0,humidity

def AReadBme280():
    try:
        #chipId, chipVersion=readBME280ID()
        T,P,H=readBME280All()
    except:
        T,P,H = -1.0,-1.0,-1.0
    class tempData():
        def __init__(self):
            self.temperature=T
            self.humidity=H
            self.pressure=P/10
    return tempData()
    
def LoopShowBme():
    Q=AReadBme280
    sf='Bme280测试\n{}  \n{}↑暂停\n{} ←退出 '
    al=Q()
    return sf.format('{:.3g}℃ {:.3}%'.format(al.temperature,al.humidity),
                        '{:.5g}kPa'.format(al.pressure),' ')


########蜂鸣器##########
def beam(dur=0.5):
    address = 0x20
    if wa.name == "smp":
        import smbus
        import time
        
        bus = smbus.SMBus(1)
        bus.write_byte(address,0x7F&bus.read_byte(address))
        wa.Sleep(dur)
        bus.write_byte(address,0x80|bus.read_byte(address))
    elif wa.name == "zkb":
        try:
            from mpython import i2c
            i2c.writeto(address,(bytearray([0x7F])),True)
            wa.Sleep(dur)
            i2c.writeto(address,(bytearray([0x80])),True)
        except:                    
            import music
            music.pitch(400,int(dur*1000))
    elif wa.name == 'wlb':
        try:
            from future import i2c
            i2c.writeto(address,(bytearray([0x7F])),True)
            wa.Sleep(dur)
            i2c.writeto(address,(bytearray([0x80])),True)
        except:
            from future import buzzer
            buzzer.tone(440,dur)
    else:
        print('Beam'+str(dur))

##########ADDA##########
class addaServ():
    def __init__(self):
        import smbus
        import time
        if wa.name == 'smp':
            self.bus = smbus.SMBus(1)
        elif wa.name == 'bdz':
            self.bus = smbus.SMBus(6)
        else:
            self.bus = None

        self.address = 0x48
        self.cmd = 0x40
        self.A = [0x40,0x41,0x42,0x43]
    def Ad(self,add):
        self.bus.write_byte(self.address,self.A[add])
        v=self.bus.read_byte(self.address)
        return v*3.3/255

    def Da(self,v):
        self.bus.write_byte_data(self.address,self.cmd,v)
        return v*3.3/255

def addaspd(v):
    if wa.name in ['win','zkb','bdz','wlb']:
        return '*模拟ADDA*\n {:.2f} sps\nD{:.2f}V A0{:.2f}V\nLeft to exit'.format(10,v/100,v)


    sf='soft ADDA speed\n {:.2f} sps\nD{:.2f}V A0{:.2f}V\nLeft to exit'

    v=128
    Ad=addaServ().Ad
    Da=addaServ().Da
    import time
    dur=0.1
    tic=time.time()
    v = v % 256
    a=Ad(0)
    d=Da(v)
    dur=time.time()-tic    
    if dur == 0:
        dur = 0.0001
    return sf.format(1/dur,d,a)

 

###########IR############
def getIR():
    #check IR signal
    if wa.name in ["win","zkb","bdz"]:
        return "Not support!"
    import RPi.GPIO as GPIO
    import time
    PIN = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN,GPIO.IN,GPIO.PUD_UP)

    ans=None
    if GPIO.input(PIN) == 0:
        count = 0
        while GPIO.input(PIN) == 0 and count < 200:  #9ms
            count += 1
            time.sleep(0.00006)

        count = 0
        while GPIO.input(PIN) == 1 and count < 80:  #4.5ms
            count += 1
            time.sleep(0.00006)

        idx = 0
        cnt = 0
        data = [0,0,0,0]
        for i in range(0,32):
            count = 0
            while GPIO.input(PIN) == 0 and count < 15:    #0.56ms
                count += 1
                time.sleep(0.00006)

            count = 0
            while GPIO.input(PIN) == 1 and count < 40:   #0: 0.56mx
                count += 1                               #1: 1.69ms
                time.sleep(0.00006)

            if count > 8:
                data[idx] |= 1<<cnt
            if cnt == 7:
                cnt = 0
                idx += 1
            else:
                cnt += 1
        print('caught {}'.format(data))
        if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
            print("Get the key: 0x%02x" %data[2])
        ans='{0:02x} {1:02x} {2:02x} {3:02x}'.format(*data)
    return ans   






