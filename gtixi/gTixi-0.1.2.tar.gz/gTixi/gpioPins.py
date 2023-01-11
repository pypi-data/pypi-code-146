def ssd15pin(args):
    # get 15 pin state
    # this is compatible with SSD1306
    # set pin8 to Gnd
    # same interface with 16pin, omit #8

    s=args # 16  str 01HLUD-
    debug=0
    dPin={1:7,2:17,3:27,4:22,5:5,6:6,7:13,9:26,10:21,11:20,12:9,13:12,14:25,15:24,16:23}

    import RPi.GPIO as gpio

    try:
        gpio.setmode(gpio.BCM)
    except ValueError:
        gpio.cleanup()
        print('Cleaned up old mode')
        gpio.setmode(gpio.BCM)

    res=[' ']*16
    #configure
    for i,c in enumerate(s):
        if i==7:
            continue
        if c=='-':
            gpio.setup(dPin[i+1],gpio.IN)
        elif c=='D':
            gpio.setup(dPin[i+1],gpio.IN,pull_up_down=gpio.PUD_DOWN)
        elif c=='U':
            gpio.setup(dPin[i+1],gpio.IN,pull_up_down=gpio.PUD_UP)
        elif c=='H':
            gpio.setup(dPin[i+1],gpio.OUT,initial=gpio.HIGH)
            res[i]='H'
        elif c=='L':
            gpio.setup(dPin[i+1],gpio.OUT,initial=gpio.LOW)
            res[i]='L'

    #time.sleep(.03)

    for i,c in enumerate(s):
        if i==7:
            continue
        if c=='-' or c=='U' or c=='D':
            r=gpio.input(dPin[i+1])
            res[i]=str(r)
    if debug:
        print(res)
    #gpio.cleanup()

    return res

#################inverter###############
def inverter7404(args):
    #query 7404 through GTC RpGPIO interface

    qin=args # 6-str of 0 or 1

    #translate to 15 pin in

    if len(qin)<6:
        qin='0'*(6-len(qin))+qin

    lIn=[1,3,5,9,11,13]
    lOut=[2,4,6,8,10,12]
    vcc=14 #Gnd is 7
    parg=['-']*16 #initialize pin arg

    for i,v in enumerate(qin):
        parg[lIn[i]]='H' if v=='1' else 'L'
    parg[vcc]='H'

    r=ssd15pin(parg)

    rout=''
    for p in lOut:
        rout+=r[p]

    return qin, rout #return the full input also
def inveterChecklogic(args):
    # check if the logic is correct for hex inverter
    # return a bitwise string representation

    qin,rout=args

    cout=''
    for a,b in zip(qin,rout):
        cout+='O' if a!=b else 'X'

    if all([i=='O' for i in cout]):
        cout='  OK! '
    return cout

def InverterOnce(right=0,all=0):
    import random
    from .wadapter import wa
    if wa.name in ['win','zkb','wlb']:
        num = ""
        for i in range(6):
            num += str(random.randint(0,1))
        out = ""
        for i in range(6):
            if random.randint(0,99)>97:#模拟反相器，正确率97%
                out += '0' if num[i] == '0' else '1'
            else:
                out += '1' if num[i] == '0' else '0'
                right += 1
        all += 6
        return '*模拟反相器*\n入：{}\n出：{}↑暂停\n{}/{}←退出'.format(num,out,right,all),right,all,(num,inveterChecklogic((num,out)))
        
    # test 7404 hex inverter on GTC platform
    Q7404=inverter7404
    
    num = random.randint(0,63)
    qr = Q7404('{:b}'.format(num))
    for i in range(6):
        if qr[0][i] != qr[1][i]:
            right+=1
    all += 6
    sf='7404反相器测试\n入：{}\n出：{}↑暂停\n{}/{}←退出'.format(qr[0],qr[1],right,all)
    return sf,right,all,(num,inveterChecklogic(qr))

def invQeRate():
    # check and calculate error rate
    from .wadapter import wa
    if wa.name in ['win','zkb','wlb']:
        ans = []
        import random
        for i in range(6):
            ans.append(random.randint(0,100)/100)
        return ans
    
    Q=inverter7404
    Check=inveterChecklogic

    gc = [0] * 6

    for i in range(100):
        import random
        num = random.randint(0,63)
        qr=Q('{:b}'.format(num))
        sOK=Check(qr)
        if sOK=='  OK! ':
            for p,c in enumerate(gc):
                gc[p]=c+1
        else:
            for p,c in enumerate(sOK):
                if c=='O':
                    gc[p]+=1
    for p,c in enumerate(gc):
        gc[p]=c/100
    return gc

#管脚连通性
def cnt15pin(isBeeps = False):
    sAskCnt='15pin测试\n  请用0V\n接触管脚↑暂停\n不要接触8号←退出 '
    sShowNum='15pin测试\n  有响应的管脚：\n{}↑暂停\n  ←退出 '
    if isBeeps:
        from .waDrivers import beam
        Beeps=beam
    else:
        Beeps=lambda x:x
    
    from .wadapter import wa
    if wa.name in ['win','zkb','wlb']:
        import random
        lr = []
        for i in range(16):
            if random.randint(1,10)>9:
                lr.append(i+1)
        if len(lr)==0:
            return sAskCnt,lr
        elif len(lr)==1:
            Beeps(0.8)
            return sShowNum.format(lr[0]),lr
        else:
            Beeps(0.5)
            wa.Sleep(0.1)
            Beeps(0.5)
            return sShowNum.format(lr),lr     

    # test connectivity of the 15 pins
    CheckPin=ssd15pin


    lq=['U']*16

    r=CheckPin(lq)
    lr=[]
    for i,v in enumerate(r):
        if v=='0':
            lr.append(i+1)
    if len(lr)==0:
        ans = sAskCnt
    elif len(lr)==1:
        ans = sShowNum.format(lr[0])
        Beeps(0.8)
    else:
        ans = sShowNum.format(lr)
        Beeps(0.5)
        wa.Sleep(0.1)
        Beeps(0.5)
    return ans,lr 

#逻辑门
def logicQuery():
    Q=ssd15pin

    q1='--LL---L-------H'
    q2='--LH---L-------H'
    q3='--HL---L-------H'
    q4='--HH---L-------H'

    res=Q(q1)
    out=res[12]
    out+=Q(q2)[12]
    out+=Q(q3)[12]
    out+=Q(q4)[12]
    Q('--LL---L-------H')

    sIn='0123'

    if out=='1100':
        sR='反相器'
    elif out=='1110':
        sR='与非门'
    elif out=='0110':
        sR='异或门'
    elif out=='0011':
        sR='D锁存器'
    else:
        sR='...'

    return sIn,out,sR
def logicTest():
    # test yx logic gates on GTC platform
    # save every hour
    sf='YX逻辑门测试\n入：{}  \n出：{}↑暂停\n   {} ←退出 '
    from .wadapter import wa
    if wa.name != 'smp':
        import random
        out = [['1100','反相器'],['1110','与非门'],['0110','异或门'],['0011','D锁存器']][random.randint(0,3)]
        return sf.format('0123',out[0],out[1]),'0123',out[0]
    Yxq=logicQuery
    

    sIn, sOut, sR=Yxq()
    return sf.format(sIn,sOut,sR),sIn,sOut

   
def led(r=True,g=True,b=True):
    r = 'H' if r else 'L'
    g = 'H' if g else 'L'
    b = 'H' if b else 'L'
    from .wadapter import wa
    if wa.name == 'smp':
        inputStr = '--{}{}--------{}---'.format(b,r,g)
        ssd15pin(''.join(inputStr))
    elif wa.name == 'zkb':
        from mpython import rgb
        on = [255 if g=='H' else 0,255 if r=='H' else 0,255 if b=='H' else 0]
        for i,c in enumerate(on):
            rgb[i] = (int(c),int(c),int(c))
        rgb.write()
    elif wa.name == 'wlb':
        from future import NeoPixel
        np = NeoPixel('P7',3)
        on = [255 if g=='H' else 0,255 if r=='H' else 0,255 if b=='H' else 0]
        for i,c in enumerate(on):
            np.setColor(i,(int(c),int(c),int(c)))
        np.update()
        
    elif wa.ctag('gpio4'):
        from .gpio4 import SysfsGPIO
        pin_num = [20,3,2]
        on = [1 if g=='H' else 0,1 if r=='H' else 0,1 if b=='H' else 0]
        for i,p in enumerate(pin_num):
            pin = SysfsGPIO(p)
            pin.export = True                   # register pin through sysfs
            pin.direction = 'out'               # same like pinMode()
            pin.value = on[i]                   # same like digitalWrite()
            pin.export = False                  # unregister from sysfs
    sf = "LED Control\nR  G  B\n{}  {}  {}\n↑A切换←B退出".format(r,g,b)
    return sf

def gpioPin(p0,p1):
    from .wadapter import wa
    sf = "GPIO调试\nP0:{}\nP1:{}\n↑A切换←B退出".format("H" if p0 else "L", "H" if p1 else "L")
    if wa.ctag('board'):
        wa.gpio(0,1 if p0 else 0)
        wa.gpio(1,1 if p1 else 0)
        return sf
    
    return "GPIO模拟\nP0: {}\nP1: {}\n↑A切换←B退出".format("H" if p0 else "L", "H" if p1 else "L")

