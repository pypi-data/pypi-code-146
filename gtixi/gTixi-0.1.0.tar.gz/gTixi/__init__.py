
__all__ = ['alib','waText','waFile','wa','wad','SvgScreen',
    'starMessager',
    'baseMod','loopMod','menu','loopPro',
    'bme280','lightSensor','getIR','adder74283','adda',
    'beam','inverter','invqe','pins15','logicTest','led','gpiopin']
#init alib
from .alib import alib
from .wadapter import Wa,SvgScreen
from . import wadapter as wad
from . import waText
from . import waFile
wa = Wa()

#init baseMod
from .starMod import baseMod,loopMod,menu,loopPro

if wa.name in ['win','smp','bdz']:
    __all__.extend(['wsServer','httpServer','wsCtrl','webConf'])
    #init messager and servers
    from .starServer import wsServer,httpServer,wsCtrl,webConf
from .starServer import sm
starMessager = sm

#Drivers
from . import waDrivers
bme280 = waDrivers.LoopShowBme
getIR = waDrivers.getIR
adder74283 = waDrivers.AdderQ283
beam = waDrivers.beam
adda = waDrivers.addaspd
from . import wLTR390
lightSensor = wLTR390.getOnce
from .gpioPins import InverterOnce,invQeRate,cnt15pin,logicTest,led,gpioPin
inverter = InverterOnce
invqe = invQeRate
pins15 = cnt15pin
gpiopin = gpioPin
