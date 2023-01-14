from http.server import executable
from subprocess import Popen
from random import randint
from sys import argv, executable

import MakeOrBreak

def runAsBackgroundProcess(choice, interval):
   controllerFileLocation = MakeOrBreak.__path__[0] + "/controller.py" 
   print(controllerFileLocation)
   # Popen(['python3', 'controller.py', str(choice), str(interval)])

def generateRdmNumber(start, end):
   return randint(start, end)

def getSysArgs():
   return argv


if __name__ == "__main__":
   runAsBackgroundProcess()
   print(generateRdmNumber(0, 10))
