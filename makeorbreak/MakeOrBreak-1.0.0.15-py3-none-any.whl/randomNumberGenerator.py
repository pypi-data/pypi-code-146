from random import randint

## Take note that [start, end]
def generateRdmNumber(start, end):
   return randint(start, end)


if __name__ == "__main__":
   print(generateRdmNumber(0, 10))