
#基础模块类，作为各种功能模块的基础，推荐直接继承baseMod，然后重载show和InputKey的部分
#menuSelect属性用于记录进入这个模块的菜单索引，在backToMenu函数中调用
#show和InputKey可以重载为需要的功能
class baseMod():
    def __init__(self,menuInfo):
        self.menuInfo = menuInfo
        self.msgr = menuInfo['sm']
        self.dev = self.msgr.shipei.name
        self.tag = self.msgr.shipei.tag

        ##初始化保存数据的路径
        self.path = ""
        import os
        if self.dev == "smp":
            if os.path.isdir('../Sandbox/'):
                self.path = '../Sandbox/'
            elif os.path.isdir('../../Sandbox/'):
                self.path = '../../Sandbox'
        elif self.dev == "win":
            if os.path.isdir('../DAKu/testdata/'):
                self.path = '../DAKu/testdata/'
            elif os.path.isdir('../../DAKu/testdata/'):
                self.path = '../../DAKu/testdata/'
        if not self.ctag('board'):
            import os
            if not os.path.isdir(self.path):
                if self.path:
                    os.mkdir(self.path)
    def ctag(self,str):
        return str in self.tag

    def start(self):
        self.show()
    def backToMenu(self):
        self.msgr.workModule = menu(**self.menuInfo)
        self.msgr.workModule.show()
    def show(self):
        self.output("默认模块：\n该模块尚未开发，\n按任意键返回。")
    def InputKey(self,key):
        self.backToMenu()
    def output(self,str):
        self.msgr.output(str)
    def saveCSV(self,slist,backstr):
        if self.ctag('board'):
            return     
        import pandas as pd
        df = pd.DataFrame(slist)
        from datetime import datetime
        fn = self.path + datetime.now().strftime('%y%m%d-%H%M%S')+backstr
        df.to_csv(fn,index=False)
    def saveTXT(self,textstr,backstr):
        from datetime import datetime
        sfn = self.path + datetime.now().strftime('%y%m%d-%H%M%S')+backstr
        with open(sfn,'w') as f:
            f.write(textstr)        

#基础的循环采集模式
#只需要重载loopUnit函数即可
class loopMod(baseMod):
    def __init__(self,mi):
        baseMod.__init__(self,mi)
        self.pause = False
        self.stop = False
        self.pauseWait = 0.5
        self.loopDelay = 0.5
    def loopUnit(self):
        self.output("Looping...")
    def loop(self,_=None):
        while not self.stop:
            while self.pause and not self.stop:
                pass
                time.sleep(self.pauseWait)
            self.loopUnit()
            import time
            time.sleep(self.loopDelay)
        self.backToMenu()
        self.msgr.workModule.show()
    def show(self):
        if self.ctag('board'):
            import _thread as th
            th.start_new_thread(self.loop,(None,))
        else:
            import threading
            t = threading.Thread(target=self.loop)
            t.start()

    def InputKey(self,key):
        if not key:
            return
        if key in "UAPHDT":
            self.pause = not self.pause
        elif key in "LRBNOY":
            self.stop = True

#高级循环
class loopPro(baseMod):
    def __init__(self,mi):
        baseMod.__init__(self,mi)
        self.pause = False
        self.stop = False
        self.isRunning = False
    def loop(self):
        pass

    def running(self,_=None):
        self.isRunning = True
        self.loop()
        self.isRunning = False

    def show(self):
        if self.ctag('board'):
            import _thread as th
            th.start_new_thread(self.running,(None,))
        else:
            import threading
            t = threading.Thread(target=self.running)
            t.start()

    def InputKey(self,key):
        if not key:
            return
        if self.isRunning:
            if key in "UAPHDT":
                self.pause = not self.pause
            elif key in "LRBNOY":
                self.stop = True
        else:
            if key in "UAPHDT":
                self.show()
            elif key in "LRBNOY":
                self.backToMenu()

#关机面板：内容为纯黑屏        
#暂时退出，关闭屏幕，按下任意键重新启动
class offStatus(baseMod):
    def __init__(self,mi):
        baseMod.__init__(self,mi)
    def show(self):
        self.output(" ")

class menu():
    def __init__(self,sm,initData,select=([],0),):
        self.data = initData
        self.submenu = select[0] #第一个数字代表哪个子目录，列表代表根目录；第二个为当前选中元素的下标
        self.pointer = select[1]
        self.msgr = sm
    def selectedSub(self):
        menuItem = self.data
        for i in self.submenu:
            keys = list(menuItem.keys())
            keys.sort()
            menuItem = menuItem[keys[i]]
        return menuItem        
    def show(self):
        menuItem = list(self.selectedSub().keys())
        menuItem.sort()
        output = ''
        if len(menuItem)<3:
            for _ in range(3-len(menuItem)):
                menuItem.append('\n')
        if self.pointer == 0:
            displayList = [0,1,2]
        elif self.pointer == len(menuItem)-1:
            displayList = [len(menuItem)-3,len(menuItem)-2,len(menuItem)-1]
        else:
            displayList = [self.pointer-1,self.pointer,self.pointer+1]
        for (i,item) in enumerate(menuItem):
            if i in displayList:
                output += "|* " + item + '\n' if(i == self.pointer) else "|  " + item + '\n'

        mtitle = ""
        if self.submenu:
            menuItem = self.data
            for i in self.submenu:
                keys = list(menuItem.keys())
                keys.sort()
                mtitle = keys[i]
                menuItem = menuItem[keys[i]]
            mtitle += '\n'
        else:
            mtitle = '主菜单\n'
        if self.msgr.shipei.name == 'zkb':
            output += " A    ←    ↓    ↑    →    B"
        else:
            output = mtitle + output
        self.msgr.output(output)
    def subLength(self):
        return len(self.selectedSub())
    def movePointer(self,shift):
        self.pointer = (self.pointer + shift) % self.subLength()
    def enterSub(self):
        keys = list(self.selectedSub().keys())
        keys.sort()
        sSub = self.selectedSub()[keys[self.pointer]]
        if isinstance(sSub,dict):
            self.submenu.append(self.pointer)
            self.pointer = 0
            return False
        elif sSub == 0:
            self.exitSub()
        else:
            menuInfo = {"sm":self.msgr,"initData":self.data,"select":(self.submenu,self.pointer)}
            self.msgr.workModule = sSub(menuInfo)
            self.msgr.workModule.start()
            return True#返回值代表是否进入了新的Mod
    def exitSub(self):
        if len(self.submenu):
            self.pointer = self.submenu.pop()
    def InputKey(self,key):
        if not key:
            return
        self.msgr.msg=""
        if key in "UH":
            self.movePointer(-1)
        elif key in "DTAP":
            self.movePointer(1)
        elif key in "ROBN":
            if self.enterSub():
                return
        elif key in "LY":
            self.exitSub()
        self.show()