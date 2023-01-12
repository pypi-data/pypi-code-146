import pyttsx3
def say(contents):
    engine = pyttsx3.init()
    engine.say(contents)
    print(contents)
    engine.runAndWait()

if __name__ == '__main__':
    say('欢迎进入Python世界！！欢迎使用 Python Education Tools')
