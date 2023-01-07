from cakework import App
import time

def say_hello(name):
    time.sleep(10)
    return { "status": "ok", "greeting": "hi " + name }

if __name__ == "__main__":
    # app = App("app", local=True)
    app = App("app")

    app.register_task(say_hello)
