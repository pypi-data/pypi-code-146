import pyttsx3

class Pyttsx:
    tts_obj = pyttsx3.init("espeak")
    tts_obj.setProperty("voice","zh")
    tts_obj.setProperty("volume",0.5)
    tts_obj.setProperty("rate",170)
    def __init__(self):
        pass
    def my_say(self,word):
        self.tts_obj.say(word)
        self.tts_obj.runAndWait()
    def my_make(self,str1,str2,str3):
        word = str1 + str2 + str3
        self.tts_obj.say(word)
        self.tts_obj.runAndWait()
    def say_price(self,str1,price,str2):
        if price < 10:
            word = str1+str(price)+str2
            self.tts_obj.say(word)
            self.tts_obj.runAndWait()
        if price >9 and price < 100:
            shi = str(int(price / 10))
            ge = str(price % 10)
            word = str1 + shi + '十' + ge + str2
            if ge == '0':
                word = str1 + shi + '十' + str2
          
            self.tts_obj.say(word)
            self.tts_obj.runAndWait()
        if price >99 and price < 1000:
            bai = str(int(price / 100))
            shi = str(int((price % 100)/10))
            ge = str(price % 10)
            word = str1 + bai + '百' + shi +'十'+ ge + str2
            if shi == '0':
                word = str1 + bai + '百' + '零' + ge + str2
                if ge == '0':
                    word = str1 + bai + '百' + str2
            else:
                if ge == '0':
                    word = str1 + bai + '百' + shi +'十'+ str2
            self.tts_obj.say(word)
            self.tts_obj.runAndWait()
    
    def my_voice(self,volume,rate):
        self.tts_obj.setProperty("volume",volume)
        self.tts_obj.setProperty("rate",rate)


