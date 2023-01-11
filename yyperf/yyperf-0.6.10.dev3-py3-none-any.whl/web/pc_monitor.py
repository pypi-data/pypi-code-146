# -*- coding: utf-8 -*-
import argparse
import os
import re
import shutil
import threading
import time
import psutil
import logging
from pynvml import *

DATA_TITLE = "TimeStamp,app CPU Load(%),Total CPU(%),Memory(MB),Native(MB),Dalvik(MB),totalTraffic(Kb/s)," \
             "trafficUp,trafficDown,GPU Load [%],Threads,virtual Mem(MB),Activities,FPS,wakeups," \
             "batteryLevel,temperature,HandleCount"

logging = logging.getLogger("client_log")

current_path = os.path.abspath(__file__)
current_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")

class BaseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.bStop = False

    def stop(self):
        self.bStop = True

class AllGPUThread(BaseThread):
    def __init__(self,timeInterval=1,testTime=1800):
        super(AllGPUThread,self).__init__()
        self.timeInterval = timeInterval#采集时间间隔
        self.timeOut = testTime
        self.gpu_memory = -1
        self.gpu_temperature = -1

    def get_data(self):
        return self.gpu_memory,self.gpu_temperature

    def run(self):
        try:
            nvmlInit()
            count = nvmlDeviceGetCount()
            if count<1:
                logging.error("没有找到Nvidia显卡，目前只支持Nvidia显卡的GPU采集")
                return False
            gpuHandle = nvmlDeviceGetHandleByIndex(0)
            # name = nvmlDeviceGetName(gpuHandle)
            # mem = nvmlDeviceGetMemoryInfo(gpuHandle)
            logging.info(u"启动线程，开始采集GPU数据")
            while self.timeOut > 0 and self.bStop is False:
                try:
                    self.gpu_memory = nvmlDeviceGetMemoryInfo(gpuHandle).used/1024/1024
                    self.gpu_temperature = nvmlDeviceGetTemperature(gpuHandle,NVML_TEMPERATURE_GPU)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    logging.error(str(e))
                time.sleep(self.timeInterval)
                self.timeOut = self.timeOut - self.timeInterval
                # if self.timeOut % 60 == 0:
                #     logging.info(u"正在采集GPU数据，还剩 %d s"%self.timeOut)
        except Exception as e:
            logging.error(str(e))
        finally:
            nvmlShutdown()
            logging.info(u"采集线程已退出")

class GPUThread(BaseThread):
    def __init__(self,process_name,pid_list, timeInterval=1,testTime=1800):
        super(GPUThread,self).__init__()
        self.process_name = process_name
        self.pid_list = pid_list
        self.timeInterval = timeInterval#采集时间间隔
        self.timeOut = testTime
        self.gpu_load = {}
        self.gpu_memory = -1
        self.gpu_temperature = -1
        self.read_offset_dict = {}
        for pid in self.pid_list:
            self.read_offset_dict.setdefault(pid,(None,0))
            self.gpu_load.setdefault(pid,0)

    def get_gpu_data(self,pid):
        return self.gpu_load.get(pid,0)

    def run(self):
        try:
            logging.info(u"启动线程，开始采集GPU数据")
            while self.timeOut > 0 and self.bStop is False:
                try:
                    for pid in self.pid_list:
                        fd,offset = self.read_offset_dict.get(pid,(None,0))
                        csv_name = os.path.join(current_path,r"ProcessHacker\plugins\psmonlog\%s_%d.csv"%(self.process_name,pid))
                        if fd is None and os.path.exists(csv_name) :
                            fd = open(csv_name,mode='r')
                            self.read_offset_dict[pid] = (fd,0)
                        if not fd:
                            continue
                        fd.seek(offset)
                        data = fd.read()
                        data_lines = data.splitlines()
                        last_line = data_lines[-1] if len(data_lines)>0 else ""
                        if len(last_line.split(','))>=10 and not last_line.startswith("time"):
                            self.gpu_load[pid] = float(last_line.split(',')[2])
                        offset += len(data)
                        self.read_offset_dict[pid] = (fd, offset)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    logging.error(str(e))
                time.sleep(self.timeInterval)
                self.timeOut = self.timeOut - self.timeInterval
                # if self.timeOut % 60 == 0:
                #     logging.info(u"正在采集GPU数据，还剩 %d s"%self.timeOut)
        except Exception as e:
            logging.error(str(e))
        finally:
            for pid in self.pid_list:
                fd, offset = self.read_offset_dict.get(pid, (None, 0))
                if fd:
                    fd.close()
            logging.info(u"采集线程已退出")

class NetworkThread(BaseThread):
    def __init__(self, timeInterval=1,testTime=1800):
        super(NetworkThread,self).__init__()
        self.timeInterval = timeInterval#采集时间间隔
        self.timeOut = testTime
        self.networkIn = -1
        self.networkOut = -1
        self.oldRecv = {}
        self.oldSent = {}

    def get_network(self):
        return self.networkIn,self.networkOut

    def getNetworkData(self):
        # 获取网卡流量信息
        recv = {}
        sent = {}
        data = psutil.net_io_counters(pernic=True)
        interfaces = data.keys()
        for interface in interfaces:
            recv.setdefault(interface, data.get(interface).bytes_recv)
            sent.setdefault(interface, data.get(interface).bytes_sent)
        return interfaces, recv, sent

    def getNetworkRate(self):
        # 计算网卡流量速率
        interfaces, newRecv, newSent = self.getNetworkData()
        if not self.oldRecv:
            self.oldRecv = newRecv
            self.oldSent = newSent
            return -1,-1
        networkIn = 0.0
        networkOut = 0.0
        for interface in interfaces:
            networkIn = networkIn + float("%.3f" % (newRecv.get(interface) - self.oldRecv.get(interface)))
            networkOut = networkOut + float("%.3f" % (newSent.get(interface) - self.oldSent.get(interface)))

        self.oldRecv = newRecv
        self.oldSent = newSent

        return networkIn/1024.0, networkOut/1024.0

    def run(self):
        while self.bStop is False and self.timeOut>0:
            try:
                self.networkIn,self.networkOut = self.getNetworkRate()
            except Exception as e:
                logging.error(f"获取流量数据异常：{str(e)}")
            time.sleep(self.timeInterval)
            self.timeOut = self.timeOut-self.timeInterval

class CaptureThread(BaseThread):
    def __init__(self, process_name,gpu_thread,timeInterval=1, testTime=1800, filename=None,pcinfo=None):
        super(CaptureThread,self).__init__()
        self.process_name = process_name
        self.timeInterval = timeInterval  # 采集时间间隔
        self.timeOut = testTime
        self.filename = filename
        self.pcinfo = pcinfo
        self.all_gpu_thread = gpu_thread

    def get_pids(self):
        if not self.process_name.endswith(".exe"):
            self.process_name = self.process_name+".exe"
        pid_list = []
        all_pids = psutil.pids()
        for pid in all_pids:
            try:
                p = psutil.Process(pid)
                pName = p.name()
                # 过滤出YY进程
                if pName == self.process_name:
                    logging.info(f'process name={self.process_name} ,pid={pid}, cmdline = {p.cmdline()}')
                    pid_list.append(pid)
            except:
                print('进程无法访问 pid=', pid)
        return pid_list

    def run(self) -> None:
        pid_list = self.get_pids()
        if len(pid_list)==0:
            logging.info(f"没有获取到进程名为{self.process_name}的pid")
            return
        logging.info(f"获取到进程名为{self.process_name}的pid：{pid_list}")
        file_list = {}
        proutil_list = []
        perf_file = open(self.filename,mode='w+',encoding='gbk')
        for pid in pid_list:
            filename = self.filename.replace(".csv",f"_{pid}.csv")
            fd = open(filename,mode='w+',encoding='gbk')
            file_list.setdefault(pid,fd)
            fd.write(f"机器信息：{self.pcinfo.replace(',',' ')}\n")
            pro = psutil.Process(pid)
            proutil_list.append(pro)
            fd.write(f"进程信息： pid：{pid} cmdline:{' '.join(pro.cmdline())}\n")
            fd.write("\n\n\n")
            fd.write(f"{DATA_TITLE}\n")
            fd.flush()
        perf_file.write(f"{DATA_TITLE}\n")
        perf_file.flush()
        logging.info(f"{self.process_name}--启动线程获取GPU和网络数据")
        gputhread = GPUThread(self.process_name,pid_list,self.timeInterval,self.timeOut)
        gputhread.setDaemon(True)
        gputhread.start()
        netthread = NetworkThread(self.timeInterval,self.timeOut)
        netthread.setDaemon(True)
        netthread.start()
        num_cpus = psutil.cpu_count()
        while self.bStop is False and self.timeOut>0:
            try:
                all_cpu_percent = all_thread_num = all_handle_num = all_memory = all_vss = all_rss = 0
                networkin, networkout = netthread.get_network()
                all_gpu_load = 0
                if networkin==-1 :#or gpu_load==-1:
                    continue
                gpu_mem, gpu_temp = self.all_gpu_thread.get_data()
                str_now_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
                for putil in proutil_list:
                    cpu_percent = putil.cpu_percent()/num_cpus
                    mem_percent = putil.memory_percent()
                    thread_num = putil.num_threads()
                    handle_num = putil.num_handles()
                    memory_info = putil.memory_info()
                    memory = memory_info.wset
                    vss = memory_info.vms
                    rss = memory_info.rss
                    gpu_load = gputhread.get_gpu_data(putil.pid)
                    all_gpu_load += gpu_load
                    all_cpu_percent += cpu_percent
                    all_thread_num += thread_num
                    all_handle_num += handle_num
                    all_memory += memory
                    all_vss += vss
                    all_rss += rss
                    datastr = f"{str_now_time},{cpu_percent:.2f},-1,{memory/1024.0/1024.0:.2f},{rss/1024.0/1024.0:.2f},{gpu_mem},{networkin+networkout:.2f}," \
                              f"{networkout:.2f},{networkin:.2f},{gpu_load},{thread_num},{vss/1024.0/1024.0:.2f},-1,-1,-1,-1,{gpu_temp},{handle_num}\n"
                    file_list[putil.pid].write(datastr)
                    file_list[putil.pid].flush()
                datastr = f"{str_now_time},{all_cpu_percent:.2f},-1,{all_memory / 1024.0/1024.0:.2f},{all_rss/1024.0/1024.0:.2f},{gpu_mem},{networkin + networkout:.2f}," \
                          f"{networkout:.2f},{networkin:.2f},{all_gpu_load},{all_thread_num},{all_vss/1024.0/1024.0:.2f},-1,-1,-1,-1,{gpu_temp},{all_handle_num}\n"
                perf_file.write(datastr)
                perf_file.flush()
            except Exception as e:
                logging.error(f"{self.process_name}--获取数据异常：{str(e)}")
            time.sleep(self.timeInterval)
            self.timeOut = self.timeOut - self.timeInterval
            if self.timeOut % 60 == 0:
                logging.info(f"{self.process_name}--正在采集数据，还剩 {self.timeOut} s" )
        gputhread.stop()
        netthread.stop()
        perf_file.close()
        for pid,fd in file_list.items():
            fd.close()
        logging.info(f"{self.process_name}--数据采集完成")

class PCMonitorThread(BaseThread):
    def __init__(self, process_name,timeInterval=1, testTime=1800, filename=None,pcinfo=None):
        super(PCMonitorThread,self).__init__()
        self.process_name = process_name
        self.timeInterval = timeInterval  # 采集时间间隔
        self.timeOut = testTime
        self.filename = filename
        self.pcinfo = pcinfo
        self.thread_list = []

    def init_process_hacker(self):
        try:
            processname_list = re.split('[;,]', self.process_name)
            name_list = []
            for name in processname_list:
                if not name.endswith(".exe"):
                    name = name + ".exe"
                name_list.append(name)
            content = f"[ps]\nids=\nexes={','.join(name_list)}\nautotimeout={self.timeOut}\n"
            fd = open(os.path.join(current_path,r"ProcessHacker\plugins\psmon.ini"),mode="w+")
            fd.write(content)
            fd.close()
            shutil.rmtree(os.path.join(current_path,r"ProcessHacker\plugins\psmonlog"),ignore_errors=True)
            os.makedirs(os.path.join(current_path,r"ProcessHacker\plugins\psmonlog"),exist_ok=True)
        except Exception as e:
            logging.error(str(e))

    def run(self):
        try:
            self.init_process_hacker()
            os.popen(f'start /min {os.path.join(current_path,"ProcessHacker/ProcessHacker.exe")}')
            processname_list = re.split('[;,]',self.process_name)
            self.thread_list = []
            all_gpu_thread = AllGPUThread(self.timeInterval,self.timeOut)
            all_gpu_thread.setDaemon(True)
            all_gpu_thread.start()
            self.thread_list.append(all_gpu_thread)
            time.sleep(3)
            for processname in processname_list:
                th = CaptureThread(processname,all_gpu_thread,self.timeInterval,self.timeOut,self.filename.replace(".csv",f"_{processname}.csv"),self.pcinfo)
                th.setDaemon(True)
                th.start()
                self.thread_list.append(th)
            for th in self.thread_list:
                th.join(timeout=self.timeOut+180)
        except Exception as e:
            logging.error(str(e))
            os.popen("taskkill /F /IM ProcessHacker.exe").read()

    def stop(self):
        try:
            os.popen("taskkill /F /IM ProcessHacker.exe").read()
            for th in self.thread_list:
                th.stop()
            time.sleep(2)
            shutil.move(os.path.join(current_path,r"ProcessHacker\plugins\psmonlog"), os.path.dirname(self.filename))
        except Exception as e:
            logging.error(str(e))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="ios perf data monitor")
    parser.add_argument('-filename', type=str, default='73_YY.csv',
                        help='csv file name (end with .csv)')
    parser.add_argument('-time', type=float, default=300.0, help='trace time (second)')
    parser.add_argument('-process', type=str, default="YY,yyexternal", help='process name')
    args = parser.parse_args()
    from winUtil import pcinfo
    th = PCMonitorThread(args.process,timeInterval=1,testTime= args.time,filename=args.filename,pcinfo=pcinfo)
    th.start()
    th.join(args.time+30)