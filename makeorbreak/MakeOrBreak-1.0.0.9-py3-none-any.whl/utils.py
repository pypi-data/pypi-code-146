from subprocess import Popen, run
from random import randint

def runAsBackgroundProcess(choice, interval):
   p = run(['python3', 'app.py', str(choice), str(interval)])

def generateRdmNumber(start, end):
   return randint(start, end)


if __name__ == "__main__":
   runAsBackgroundProcess()
   print(generateRdmNumber(0, 10))
