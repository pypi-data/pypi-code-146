from platform import system
import os

import MakeOrBreak.utils as utils
import MakeOrBreak.dataReader as dataReader
# from MakeOrBreak.utils import generateRdmNumber
# from MakeOrBreak.dataReader import readDataFromFile

CONTENT_TYPE_MAPPING = {
   0: "compliments",
   1: "insults"
}

def getNotificationContent():
   contentType = CONTENT_TYPE_MAPPING.get(utils.generateRdmNumber(0, len(CONTENT_TYPE_MAPPING) - 1))
   contentData = dataReader.readDataFromFile(contentType)

   return contentData[utils.generateRdmNumber(0, len(contentData) - 1)]

def createNotification():
   content = getNotificationContent()
   os_system = system()
   command = None

   if os_system == "Darwin":
      command = f'''
      osascript -e 'display notification "{content}" with title "MakeOrBreak"'
      '''
   elif os_system == "Linux":
      command = f'''
      notify-send "MakeOrBreak" "{content}"
      '''
   else:
      raise Exception("Unknown OS detected..")

   os.system(command)


if __name__ == "__main__":
   for i in range(10):
      createNotification()