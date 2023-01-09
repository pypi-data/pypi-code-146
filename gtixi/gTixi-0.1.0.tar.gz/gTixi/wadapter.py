#! /usr/bin/env python3

"""
wadapter
=======================
Created by Cerulany 2022 <www.zhihu.com/people/cerulany>
    with lrm

Adapts numpy etc. commonly used python modules, so that same code can run on fullfledged python, as well as in a reduced python environment (e.g. micropython, qpython)

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
221202 by Spectre Lee
    把加法器的驱动转移到单独的文件中，
    该文件专注适配器。
    给每个适配类添加了name属性，可以直接调用name判断当前的设备类型。
221115 by Spectre Lee
    楠哥的继承写的有问题，
    class newClass(fClass):
        def __init__(self):
            fClass.__init__(self)
            pass
    必须这样写newClass才会继承fClass的init，否则是覆盖（重载）
221109 by Spectre Lee
    在SpXxx中添加了DrawStdLine.
    添加了Spwin的模式，一方面可以再win下调试，另一方面避免修改Shipei父类带来的bug。
    修改了checkKey的逻辑，现在会运行到检测到输入才停止，是一种等待操作。
221027 SpEsp32, 将SpZkb, SpWlb归为其子类
    复用代码，1030 lines
221018
    modified YsKey of Zkb, add timedelta display
    1041 lines
221012 by Spectre Lee
    Shipei类里添加self.i2c=none,不然win下不能运行
    为SvgScreen添加了DrawStdLines,将带有\n的几行数据格式化输出为四行的形式。
    对SvgScreen的位置和字号进行了比例缩放，适配不同尺寸的显示屏。
221009 改self.ai2c为self.i2c，增加通用性
    SvgScreen类,SpSmp和SpBdz增加SvgScreen
    1015 lines
220929 SpBdz fallback
    SIp fallback
220927 增加aenv.fPyL, LoopShowBme等
    Zkb上验证可用
220906 MCPioeb的程doのq283 加入debug选项
    修复Shipei.Sleep
    added 0x5a MLX90614 temperature sensor
    Zkb ad rwd but may have some problems
220905 button_a.value, button_b.value
    烫74283的程getのcheckLogic
    MCPioeb的程doのq283
    MCPioeb的程loopの74283speed 改为 LoopShow283
220902 repaired microPython I2C writeto_mem compatibility
    passed test on wlb
220831 repaired button a b simulation
    unified wlb DrawText, 626 lines
220829 add waFile, waText import as common fascade
    initDisplay for SpSmp
    add
220825 deal with i2c compatibility
    alib dict
    wa.LsScanI2c
220824 add SMbus, SpBdz
220823 增加Wa, SpZkb
    zkb demo成功了！
    Key Demo and CheckKey
    aI2c
220818 change sMac to shMac
    add SIp
    alib has some problems in microPython
220812 增加a支持的平台和a支持的设备,
    AWaEnv, Hello, Draw的框架，116 lines
220331 numpy, smbus for qpython

"""
aWaEnv={'sWal':'WalArtmin'}

a支持的平台='''[Python3|3.6+在电脑和GT0上运行的]
[QPython3|在安卓平台上运行的]
[microPython|在ESP32等微控制器上运行的]'''

a支持的设备='''[oDraw|[#|小屏幕控制]
[SSD1306|Pioneer600上的黄青屏等]
[mPython|掌控板上的黑白屏]
[Wlb|未来板上的彩屏]]

[I2C设备|
[LTR390|可见光、紫外传感器]
[mcp23017|IO扩展]
[MLX90614|红外传感]]

[组合设备|
[Pioneer600|Waveshare, 能插到GT0上的扩展板，包含SSD1306]
[UPS HAT|Waveshare, 不间断电源]
[GTmcp|包含mcp23017和LTR390的扩展板]
[GTamp|PKU RCCE, 可测转移曲线的扩展板]]'''
#以上模块可在GTixi的任何主机上使用

def AWaEnv():
    '''收集当前系统信息'''
    import os
    try:
        un=os.uname()
        aWaEnv['sSysname']=un.sysname
        aWaEnv['sNodename']=un.nodename
        aWaEnv['sRelease']=un.release
        aWaEnv['sVersion']=un.version
        aWaEnv['sMachine']=un.machine
    except AttributeError:
        #那估计是windows系统
        import platform
        un=platform.uname()
        aWaEnv['sNodename']=un.node
        aWaEnv['sSysname']=un.system
        aWaEnv['sRelease']=un.release
        aWaEnv['sVersion']=un.version
        aWaEnv['sMachine']=un.machine #architecture
        aWaEnv['sProcessor']=un.processor
    try:
        import uuid
        aWaEnv['iMac']=uuid.getnode()
        aWaEnv['shMac']=hex(aWaEnv['iMac'])[2:]
    except ImportError:
        try:
            import network
            #microPython here
            wlan=network.WLAN()
            bMac=wlan.config('mac')
            iMac=0
            for b in bMac:
                #print(b)
                iMac=iMac<<8
                iMac+=b
            aWaEnv['iMac']=iMac
            aWaEnv['shMac']=hex(aWaEnv['iMac'])[2:]
        except ImportError:
            #no network
            aWaEnv['iMac']=0
            aWaEnv['shMac']='none'
    except:
        pass
    return aWaEnv

def Hello():
    aWaEnv=AWaEnv()

aWaEnv['fPyL']=0
'''fPyL: Python环境评级
1.0 microPython 可用库：sys, os, random, math, time
2.0 bdz QPython 可用库：
3.0 Python36 可用库：numpy, PIL, scipy
3.5 smp Python：qcodes, graphviz, latex
'''
class SvgScreen(): #svg虚拟屏幕
    def __init__(self,size=(128,64)):
        self.tSize=size
        self.lContent=[]
        self.sSvg=''
    def Generate(self): #
        sSvg='<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg" version="1.1" style="background:#000">\n'.format(self.tSize[0],self.tSize[1])
        sSvg+='\n'.join(self.lContent)
        sSvg+='\n</svg>'
        #print(sSvg)
        #sSvg.replace('\n','')
        return sSvg.replace('\n','') # 加上\n的话在传送门里显示会有点问题
    def DispShow(self):
        self.sSvg=self.Generate()
        return self.sSvg
    def DispClear(self):
        self.lContent=[]
    def DrawText(self,tPos,sTxt,c=None):
        if c is None:
            if tPos[1]<0.1:
                c="#ee0"
            else:
                c='#0ee'
        fontsize = self.tSize[1] * 3 // 16#起点不一样, svg是左下，zkb等是左上
        self.lContent.append('<text x="{}" y="{}" font-size="{}" font-family="monospace" style="fill:{}" xml:space="preserve">{}</text>'.format(int(self.tSize[0]*tPos[0]),int(self.tSize[1]*tPos[1])+fontsize,fontsize,c,sTxt))
    def DrawStdLines(self,input):
        self.DispClear()
        if input:
            lines = input.split("\n")
            for i in range(len(lines)):
                if i<4:
                    self.DrawText((0,0.04+0.2375*i),lines[i])
        return self.Generate()


class Shipei(): #统一Fascade
    def __init__(self,aenv):
        self.aenv=aenv # aWaEnv
        self.i2c = None
        self.name = "default"
        self.tag = []
    def ctag(self,str):
        return str in self.tag
    def gpio(self,pin,value= None):
        return None
    def DispChar(self,txt):
        if isinstance(txt,str):
            lines=txt.split('\n')
        else:
            lines=txt
        self.DispClear()
        try:
            self.DrawText((0,0),lines[0],c=(200,200,0))
            self.DrawText((0,15),lines[1],c=(0,200,200))
            self.DrawText((0,30),lines[2],c=(0,200,200))
            self.DrawText((0,45),lines[3],c=(0,200,200))
        except IndexError:
            pass
        self.DispShow()
    def YsDisp(self): #demonstrate display function
        txt=str(self.aenv)
        self.LoopText(txt)
        self.DispClear()

    def Sleep(self,fDurS):
        import time
        time.sleep(fDurS)
    def YsKey(self):
        import time
        iStart=time.time()
        while True:
            try:
                self.DispChar('KeyDemo  {}\n CurKey: '.format(waText.STimeDiffS(time.time()-iStart))+self.cKey)
                self.Sleep(.5)
            except KeyboardInterrupt:
                import _thread
                _thread.exit()
    def LoopText(self,sText,sTitle='文本查看'):

        lines=sText.splitlines()
        nl=len(lines)
        i=0
        k=self.CheckKey()
        while k!='L':
            if i==0:
                l1=''
            else:
                l1=lines[i-1]
            l2=lines[i]
            if i==nl-1:
                l3=''
            else:
                l3=lines[i+1]
            self.DispChar([sTitle,l1,l2,l3])

            k=self.CheckKey()

            if k=='U':
                i-=1
            elif k=='D':
                i+=1

            if i>nl-1:
                i=nl-1
            elif i<0:
                i=0
            self.Sleep(.2)
        #self.DispClear()
        self.DispShow()
    def LsScanI2c(self):
        #default scan, rp seems does not have i2c scan function
        i2c=self.oi2c
        lsI2c=[]
        for h in range(255):
            try:
                r=i2c.read_byte(h)
                print('Found I2C 0x{:x}({}): {:0x}'.format(h,h,r))
                lsI2c.append('0x{:x}'.format(h))
            except OSError:
                pass
        print('Done scan I2C')
        return lsI2c
class SpEsp32(Shipei): #Esp32, includes Zkb, Wlb etc.
    def __init__(self,aenv):
        Shipei.__init__(self,aenv)
        self.tag.extend(['board'])
    def ASetupI2c(self):
        # 使用self.oi2c
        def wbd(address,pos,dat,i2c=self.oi2c):
            return i2c.writeto_mem(address,pos,chr(dat).encode())
        def rbd(address,pos,i2c=self.oi2c):
            return ord(i2c.readfrom_mem(address,pos,1))
        def rwd(address,pos,i2c=self.oi2c):
            r=i2c.readfrom_mem(address,pos,2)
            print(r)
            return ord(r[0])<<8+ord(r[1]) #maybe problems here
        def ribd(address,pos,iLen,i2c=self.oi2c):
            r=i2c.readfrom_mem(address,pos,iLen)
            return r
        def wtm(address,pos,dat,i2c=self.oi2c):
            return i2c.writeto_mem(address,pos,(bytearray(dat)))
        class AI2C():
            def __init__(self,write_byte_data,read_byte_data,read_word_data,read_i2c_block_data,write_to_mem):
                self.read_word_data = read_word_data
                self.write_byte_data = write_byte_data
                self.read_byte_data = read_byte_data
                self.read_i2c_block_data = read_i2c_block_data
                self.write_to_mem = write_to_mem
        return AI2C(write_byte_data=wbd, read_byte_data=rbd, read_word_data=rwd,read_i2c_block_data=ribd,write_to_mem=wtm)

    def CheckKey(self):
        return self.cKey
    def LsScanI2c(self):
        liI2c=self.oi2c.scan()
        lsI2c=['0x{:x}'.format(h) for h in liI2c]
        return lsI2c
    def YsKey(self): #demo key
        from wadapter import waText
        import time
        iStart=time.time()
        while True:
            try:
                self.DispChar('KeyDemo  {}\nCurKey: {}\n    iLastA: {}\n    iLastB: {}'.format(waText.STimeDiffS(time.time()-iStart),self.cKey,self.iLastA,self.iLastB))
                self.Sleep(.5)
            except KeyboardInterrupt:
                import _thread
                _thread.exit()

class SpZkb(SpEsp32): #掌控板适配
    def __init__(self,aenv):
        SpEsp32.__init__(self,aenv)
        self.name="zkb"
        self.aenv=aenv
        from mpython import oled
        self.DispShow=oled.show
        from mpython import i2c
        self.oi2c=i2c
        self.i2c=self.ASetupI2c()
        self.DrawStdLine = self.DispChar
        self.oSvg = SvgScreen()
    def CheckKey(self):
        from mpython import sleep_ms,button_a,button_b,touchPad_P,touchPad_Y,touchPad_T,touchPad_H,touchPad_O,touchPad_N
        while True:
            sleep_ms(100)           
    def gpio(self,pin,value=None):
        from machine import Pin
        pinmap={0:Pin.P0,1:Pin.P1,2:Pin.P2,3:Pin.P3}
        if value:
            return Pin(pinmap[pin],Pin.OUT).value(value)
        else:
            return Pin(pinmap[pin],Pin.IN).value()        
    def DrawText(self,tPos,sTxt,c=None):
        from mpython import oled
        oled.DispChar(sTxt,tPos[0],tPos[1])
    def DispClear(self):
        from mpython import oled
        oled.fill(0)
        #oled.show()
    def Sleep(self,fDurS):
        from mpython import sleep_ms
        sleep_ms(int(fDurS*1000))
    def DrawStdLines(self,input):
        from mpython import oled
        oled.fill(0)
        if input:
            lines = input.split("\n")
            for i in range(len(lines)):
                if i<4:
                    oled.DispChar(lines[i],0,1+15*i)
            oled.show()

class SpSmp(Shipei): #树莓派适配
    def __init__(self,aenv):
        Shipei.__init__(self,aenv)
        self.name="smp"
        self.tag.extend(['web','smbus','gpiorpi','pinmap'])
        self.aenv=aenv
        self.cSoftKey=''
        import math
        import time

        import spidev as SPI
        import SSD1306

        import smbus
        self.oi2c=smbus.SMBus(1)
        i2c=self.oi2c
        class AI2C():
            def __init__(self,write_byte_data,read_byte_data,read_i2c_block_data):
                self.write_byte_data = write_byte_data
                self.read_byte_data = read_byte_data
                self.read_i2c_block_data = read_i2c_block_data
        self.i2c=AI2C(write_byte_data=i2c.write_byte_data, read_byte_data=i2c.read_byte_data, read_i2c_block_data=i2c.read_i2c_block_data)
        self.hasSsd=None
        self.oSvg=None
        self.InitDisplay()

    def InitDisplay(self):
        try:
            import spidev as SPI
            import SSD1306
            from PIL import Image
            from PIL import ImageFont
            from PIL import ImageDraw

            # Raspberry Pi pin configuration:
            RST = 19
            DC = 16
            bus = 0
            device = 0

            # 128x32 display with hardware SPI:
            disp = SSD1306.SSD1306(rst=RST,dc=DC,spi=SPI.SpiDev(bus,device))

            # Initialize library.
            disp.begin()

            # Get display width and height.
            width = disp.width
            height = disp.height
            self.width=width
            self.height=height

            # Clear display.
            disp.clear()
            disp.display()

            # Create image buffer.
            # Make sure to create image with mode '1' for 1-bit color.
            self.image = Image.new('1', (width, height))

            # Get drawing object to draw on image.
            self.draw = ImageDraw.Draw(self.image)
            self.disp=disp
            # Draw a black filled box to clear the image.
            #draw.rectangle((0,0,width,height), outline=0, fill=0)

            fontpath='simsun.ttf'
            self.font=ImageFont.truetype(fontpath,15)
            self.hasSsd=True
        except Exception as e:
            print('SSD初始化出错:',e)
            self.hasSsd=False
        self.oSvg=SvgScreen()

    def CheckKey(self):
        import RPi.GPIO as GPIO
        import smbus
        import time
        address = 0x20
        bus = smbus.SMBus(1)
        ans=''
        while True:
            time.sleep(0.15)
            bus.write_byte(address,0x0F|bus.read_byte(address))
            value = bus.read_byte(address) | 0xF0
            if value != 0xFF:
                if (value | 0xFE) != 0xFF:
                    ans='L'
                elif (value | 0xFD) != 0xFF:
                    ans='U'
                elif (value | 0xFB) != 0xFF:
                    ans='D'
                else :
                    ans='R'
                return ans
            elif self.cSoftKey:
                ans=self.cSoftKey
                self.cSoftKey=''
                return ans   
    def DrawText(self,tPos,sTxt,c=None):
        if self.hasSsd:
            self.draw.text(tPos,sTxt,font=self.font,fill=1)
        self.oSvg.DrawText(tPos,sTxt)
    def DispClear(self):
        if self.hasSsd:
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.oSvg.DispClear()
    def DispShow(self):
        if self.hasSsd:
            self.disp.image(self.image)
            self.disp.display()
        return self.oSvg.DispShow()
    
    def DrawStdLines(self,input):
        if self.hasSsd:
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        else:
            return
        if input:
            lines = input.split("\n")
            for i in range(len(lines)):
                if i<4:
                    if self.hasSsd:
                        self.draw.text((0,1+15*i),lines[i],font=self.font,fill=1)
            self.disp.image(self.image)
            self.disp.display()

    def Sleep(self,fDur):
        import time
        time.sleep(fDur)

class SpBdz(Shipei): #GT1 adapter
    def __init__(self,aenv):
        Shipei.__init__(self,aenv)
        self.name="bdz"
        self.tag.extend(['web','gpio4','smbus'])
        self.aenv=aenv
        self.cSoftKey=''
        try:
            from smbus2 import SMBus
            self.oi2c=SMBus(6)
            i2c=self.oi2c
            class AI2C():
                def __init__(self,write_byte_data,read_byte_data,read_i2c_block_data):
                    self.write_byte_data = write_byte_data
                    self.read_byte_data = read_byte_data
                    self.read_i2c_block_data = read_i2c_block_data
            self.i2c=AI2C(write_byte_data=i2c.write_byte_data, read_byte_data=i2c.read_byte_data, read_i2c_block_data=i2c.read_i2c_block_data)
        except:
            print('SMbus2 not available, install it to use it')
            self.oi2c=None
            self.i2c=None
        self.oSvg=SvgScreen()
    def CheckKey(self):
        while True:
            import time
            time.sleep(100) #by Spectre Lee, 预留给bdz实体键可以使用时

    def DrawText(self,tPos,sTxt,c=None):
        self.oSvg.DrawText(tPos,sTxt,c)
    def DispClear(self):
        self.oSvg.DispClear()
    def DispShow(self):
        return self.oSvg.DispShow()
    def DrawStdLines(self,input):
        return self.oSvg.DrawStdLines(input)

class SpWlb(SpEsp32):
    def __init__(self,aenv):
        SpEsp32.__init__(self,aenv)
        self.name="wlb"
        self.aenv=aenv

        self.iLastA=0
        self.iLastB=0
        self.cKey=''
        self.needClear=True

        from future import i2c
        self.oi2c=i2c
        self.i2c=self.ASetupI2c()
        from future import sleep
        self.Sleep=sleep
    def gpio(self,pin,value):
        from future import MeowPin
        pinmap={0:'P0',1:'P1',2:'P2',3:'P3'}
        if value:
            MeowPin(pinmap[pin],'OUT').setDigital(value)
        else:
            MeowPin(pinmap[pin],'IN').getDigital()
    def str2unicode(self,a):
        b = ''.join(map(lambda x:('' if len(hex(x))>=4 else '/x0')+hex(x)[2:],a.encode()))
        i=0
        splitLen=2
        chars=[]
        while b[i*splitLen:]:
            c = b[i*splitLen:i*splitLen+splitLen]
            c = int(c,16)
            chars.append(c)
            i += 1
        return chars
    def DrawText(self,tPos,sTxt,c=(255,255,255)):
        from future import screen
        ipos=0
        iLenTxt=len(sTxt)
        IsCh=lambda x:ord(x)>128
        isCh=IsCh(sTxt[ipos])
        iPosX=tPos[0]+16
        iPosY=tPos[1]+32
        while ipos<iLenTxt:
            iLen=0
            while ipos+iLen<iLenTxt and isCh==IsCh(sTxt[ipos+iLen]):
                iLen+=1
            if isCh:
                screen.textCh(sTxt[ipos:ipos+iLen],iPosX,iPosY,1,c)
                iPosX+=iLen*16
            else:
                screen.text(sTxt[ipos:ipos+iLen],iPosX,iPosY,1,c)
                iPosX+=iLen*8
            ipos+=iLen
            isCh=not isCh
    def DispClear(self):
        from future import screen
        #screen.fill(0)
        screen.clear()
    def DispShow(self):
        from future import screen
        screen.refresh()
    def DrawStdLines(self,input):
        return self.oSvg.DrawStdLines(input)
    def DrawStdLines(self,input):
        from future import screen
        screen.sync = 0
        screen.clear()
        if input:
            lines = input.split("\n")
            for i in range(len(lines)):
                if i<4:
                    screen.textCh(self.str2unicode(lines[i]),0,25+20*i,1,(238,238,0) if i==0 else (0,238,238))
            screen.refresh()

class SpWin(Shipei):
    def __init__(self,aenv):
        Shipei.__init__(self,aenv)
        self.name = "win"
        self.oSvg = SvgScreen()
        self.tag.extend(['web','debug'])
    def CheckKey(self):
        while True:
            import time
            time.sleep(100) #by Spectre Lee, 
    def DrawText(self,tPos,sTxt,c=None):
        self.oSvg.DrawText(tPos,sTxt,c)
    def DispClear(self):
        self.oSvg.DispClear()
    def DispShow(self):
        return self.oSvg.DispShow()
    def DrawStdLines(self,input):
        return self.oSvg.DrawStdLines(input)

def SIp():
    #get Ip address
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip='no network'
    aWaEnv['sIp']=ip
    return ip
def Wa(aenv=aWaEnv):
    if aenv == 'debug':
        return SpSmp(aenv)
    elif 'mpython' in aenv['sMachine']:
        return SpZkb(aenv)
    elif 'Future' in aenv['sMachine']:
        return SpWlb(aenv)
    elif 'v7l' in aenv['sMachine']:
        if 'localhost' in aenv['sNodename']:
            return SpBdz(aenv)
        else:
            return SpSmp(aenv)
    else:
        #print(aenv.sMachine)
        return SpWin(aenv)
SIp()
Hello()
wa=Wa()
print(wa.name)
##################################################
DEBUG=False
aI2c='''[#comment|此体系中器件有统一i2c地址]
[0x20|PCF8574IO扩展（Pioneer600）]
[0x26|GTmcp的mcp23017]
[0x39|APDS9960光线颜色传感器]
[0x42|UPS HAT]
[0x48|PCF8591ADDA（Pioneer600）]
[0x53|LTR390紫外光光感]
[0x5a|MLX90614红外传感]
[0x68|DS3231时钟模块（Pioneer600）]
[0x76|BMP280温度压力传感（Pioneer600）]
[0x77|BME280温湿度压力传感器]'''
strWaEnv = str(aWaEnv).replace("{","[").replace("}","]").replace(": ","|").replace("'","").replace(", ","][")
print(strWaEnv)

if __name__ == "__main__":
    pass
