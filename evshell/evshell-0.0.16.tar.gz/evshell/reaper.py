from threading import Thread
import os
from here import here

class PipeThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def background(self):

    def run(self):
        self.result = self.p.communicate()
        self.returncode = self.p.returncode
        if "stdout" in self.kwargs and type(self.kwargs["stdout"]) == int:
            fd = self.kwargs["stdout"]
            if fd > 2:
                os.close(self.kwargs["stdout"])
    def getpid(self):
        return self.pid
    def communicate(self):
        self.join()
        if self.pid in running:
            del running[self.pid]
        return self.result

if __name__ == "__main__":
    pipe = os.pipe()
    env = os.environ
    p1 = PipeThread(["echo","hello"], universal_newlines=True, stdout=pipe[1], env=env)
    p1.setDaemon(True)
    p1.start()
    p2 = PipeThread(["sed","s/h/H/"], universal_newlines=True, stdin=pipe[0], stdout=PIPE, env=env)
    p2.start();
    o, e = p2.communicate()
    print("out:",o,end='')

