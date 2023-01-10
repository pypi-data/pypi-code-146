import time


def run(name, **kwargs):
    time.sleep(1)
    reply = None
    if name is not None:
        reply = "Hello " + name + "!"
    return {"reply": reply}
