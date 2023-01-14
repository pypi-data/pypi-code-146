def print(text = "", delay = 0.005):
  import time
  import sys
  import string
  chars = string.printable
  generated = ""
  for i in range(len(text)):
    current = generated+''
    for c in chars:
      sys.stdout.write("\r"+current+c)
      sys.stdout.flush()
      if text.startswith(current+c):
        generated = current+c+''
        break
      time.sleep(delay)
  sys.stdout.write("\n")
  sys.stdout.flush()
