from subprocess import Popen
from random import randint
from sys import argv, executable

def runAsBackgroundProcess(choice, interval):
   print(executable)
   Popen([executable, 'python3', 'controller.py', str(choice), str(interval)])

def generateRdmNumber(start, end):
   return randint(start, end)

def getSysArgs():
   return argv


if __name__ == "__main__":
   runAsBackgroundProcess()
   print(generateRdmNumber(0, 10))
