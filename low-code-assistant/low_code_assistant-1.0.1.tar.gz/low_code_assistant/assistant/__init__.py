from IPython.display import display


def init():
    from .assistant import Assistant

    element = Assistant()
    display(element)
