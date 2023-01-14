import json

FILENAME = "data.json"

def readDataFromFile(contentType):
   file = open(FILENAME)
   return json.load(file)['data'][contentType]


if __name__ == "__main__":
   print(readDataFromFile("compliments"))
   print(readDataFromFile("insults"))