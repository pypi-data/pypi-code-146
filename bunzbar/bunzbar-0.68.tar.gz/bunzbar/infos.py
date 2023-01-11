import time
import psutil


class infos:
    def __init__(self):
        pass

    def clck(self):
        return (time.strftime("%H:%M:%S", time.localtime()))

    def battery(self):
        try:
            percent = psutil.sensors_battery().percent
            return (str(percent))
        except:
            return None

    def cpu(self):
        return (str(psutil.cpu_percent)+"%")
