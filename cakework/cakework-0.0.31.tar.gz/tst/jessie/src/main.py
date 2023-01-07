from cakework import App
from os.path import exists
import os

counter = 0

def say_hello():
    counter = 0
    counter += 1
    print("counter is: " + str(counter))
    return(counter)

if __name__ == "__main__":
    app = App("jessie")
    app.register_task(say_hello)
