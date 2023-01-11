import json

def Singleton(theClass):
    classInstances = {}

    def getInstance(*args, **kwargs):
        key = (theClass, args, json.dumps(kwargs))
        if key not in classInstances:
           classInstances[key] = theClass(*args, **kwargs)
        return classInstances[key]
    return getInstance
