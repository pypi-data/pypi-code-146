class EventBus:
    eventMap = {}

    def __init__(self):
        self.eventMap = {}

    def on(self, eventName, function):

        if eventName not in self.eventMap:
            self.eventMap[eventName] = []
        self.eventMap[eventName].append(function)

    def once(self, eventName, function):

        if eventName not in self.eventMap:
            self.eventMap[eventName] = []

        add = True
        for cb in self.eventMap[eventName]:
            if cb.__qualname__ == function.__qualname__:
                add = False
        if add:
            self.eventMap[eventName].append(function)

    def trigger(self, eventName, *args):
        if eventName not in self.eventMap:
            return
        for f in self.eventMap[eventName]:
            f(*args)
