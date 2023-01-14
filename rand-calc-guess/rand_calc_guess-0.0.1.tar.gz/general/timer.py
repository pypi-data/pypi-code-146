import time

def countdown(setTime):
  Insec = setTime * 60
  while Insec:
    min = Insec//60
    sec = Insec%60
    timer = '{:02d}:{:02d}'.format(min,sec)
    print('\r',timer, end='')
    time.sleep(1)
    Insec-=1
  print("Times up!")
