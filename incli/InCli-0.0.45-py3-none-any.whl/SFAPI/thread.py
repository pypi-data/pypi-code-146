import logging
import threading,time
import math
import sys


_counter = 0
#---------------------------------
def getCounter():
  global _counter
  return _counter
#---------------------------------
def count():
  return _counter
  
def printCounter():
  global _counter

  print(_counter)
#---------------------------------
def _testMultiple(func,iterations,processNumber,**funcArg):
  global _counter
  for a in range(iterations):
    func(processNumber=processNumber+a)
    with threadLock:
      _counter += 1
#---------------------------------
threadLock = threading.Lock()
def run(func,iterations,processStartNumber=0,threads=50,onFinished=None):
  global _counter
  _counter = 0

  try:
    for _itera in range(threads):
      processNumber = processStartNumber+ (_itera*threads)
      threading.Thread(target=_testMultiple,args=(func,iterations,processNumber), daemon=True).start()

  except:
    print ("Error: unable to start thread")
  while _counter < iterations * threads :
    logging.info(f'Iteration {_counter}  from {iterations * threads}')
    time.sleep(30)

  if onFinished!=None:
    onFinished()
    
  print("Done")

#---------------------------------
_processed = 0
_totalToProcess = 0

def processList(func,theList,threads):
  global _processed,_totalToProcess

  _processed = 0
  _totalToProcess = len(theList)
  itemsPerTh = math.ceil(_totalToProcess/threads)


  total = 0
  while total < _totalToProcess:
    end = total+itemsPerTh
    if end>_totalToProcess:
      end = _totalToProcess
    data = {
      "list" : theList[total:end]
    }

    threading.Thread(target=_processList,args=(func,theList[total:end],)).start()
    total = total + itemsPerTh

 # print()

  while (_totalToProcess>_processed):
   # print(_processed)
 #   sys.stdout.write("\r%d%%" % int(100*_processed/_totalToProcess))
 #   sys.stdout.flush()
    time.sleep(1)

def progress():
    global _processed,_totalToProcess

    sys.stdout.write("\r%d%%" % int(100*_processed/_totalToProcess))
    sys.stdout.flush() 
    if (_processed==_totalToProcess):
      print()


def _processList(func,ls):
  global _processed
  for l in ls:
    func(l)
   # print('one done')
    with threadLock:
      _processed += 1
      progress()
 # print('X done')


