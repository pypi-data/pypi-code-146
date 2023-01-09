class Context(object):
    def __int__(self):
        return

    def __str__(self):
        return


# FUNC_CONTEXT={"name":"faas.http","version":"v1.0.1","port":"8080","runtime":"Knative","prePlugins":["plugin-signature"],"postPlugins":["plugin-signature"]}
class FunctionContext(object):
    def __init__(self, name, version, port, runtime, inputs=None, outputs=None, prePlugins=None, postPlugins=None,pluginsTracing=None,out=None):
        self.name = name
        self.version = version
        self.port = port
        self.runtime = runtime
        self.inputs = inputs
        self.outputs = outputs
        self.prePlugins = prePlugins
        self.postPlugins = postPlugins
        self.pluginsTracing = pluginsTracing
        self.out = out
        if self.inputs is not None and type(inputs) == dict :
            for key,input in  dict(inputs).items():
                self.inputs[key] = Input(**input)
        if self.outputs is not None and type(outputs) == dict :
            for key,output in  dict(outputs).items():
                self.outputs[key] = Output(**output)
    # def __int__(self, _obj):
    #     self.__dict__.update(_obj)

    # def __str__(self):
    #     return "todo"


class Input(object):
    def __init__(self,uri,componentName,componentType,metadata=None):
        self.uri = uri
        self.componentName = componentName
        self.componentType = componentType
        self.metadata =metadata

class Output(object):
    def __init__(self,uri,componentName,componentType,operation,metadata=None):
        self.uri = uri
        self.componentName = componentName
        self.componentType = componentType
        self.operation = operation
        self.metadata = metadata
