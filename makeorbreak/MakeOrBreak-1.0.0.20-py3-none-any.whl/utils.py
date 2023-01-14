from http.server import executable
from subprocess import Popen
from random import randint
from sys import argv

def runAsBackgroundProcess(choice, interval):
   controllerFileLocation = f"{executable}/controller.py"
   print(controllerFileLocation)
   # Popen(['python3', 'controller.py', str(choice), str(interval)])

def generateRdmNumber(start, end):
   return randint(start, end)

def getSysArgs():
   return argv


if __name__ == "__main__":
   runAsBackgroundProcess()
   print(generateRdmNumber(0, 10))
