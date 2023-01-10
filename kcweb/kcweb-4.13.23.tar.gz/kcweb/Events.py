# -*- coding: utf-8 -*- 
import os, sys, time, subprocess,signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
eventgtimexz=0
class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if '.py' in event.src_path and event.src_path.endswith('.py'):
            global eventgtimexz
            if time.time()-eventgtimexz > 3:
                eventgtimexz=time.time()
                # print('* 更新文件：%s' % event.src_path)
                # time.sleep(10)
                time.sleep(0.2)
                self.restart()
class Events:
    command = ['echo', 'ok']
    process = None
    def __init__(self,argv):
        if '--server' not in argv and 'python' not in argv[0] or 'kcw.py' in argv:
            argv.insert(0, 'python')
        self.command = argv
        paths = os.path.abspath('.')
        self.start_watch(paths, None)

    def kill_process(self):
        "关闭"
        if self.process:
            self.process.kill()
            self.process.wait()
            self.process = None

    def start_process(self):
        "启动"
        self.process = subprocess.Popen(self.command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    def restart_process(self):
        "重启"
        self.kill_process()
        time.sleep(0.1)
        self.start_process()

    def start_watch(self,path, callback):
        "执行"
        observer = Observer()
        observer.schedule(MyFileSystemEventHander(self.restart_process), path, recursive=True)
        observer.start()
        self.start_process()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.kill_process()
            # observer.stop()
        # observer.join()
    
# Events(['server.py'])  #执行server.py文件