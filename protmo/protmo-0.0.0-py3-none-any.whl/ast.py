'''
This file contains everything for the AST-representation of the models
which are defined with the help of pm.py

- The user of the library defines multiple messages, that are defined by extending the
  Message super-type (from pm.py) and assign some Fields, like StringField or Int32Field
- The Message then is convertet to a MessageInfo (Info to not cause a name-conflict). This
  is the root of the AST. A message constists of multiple Fields and Methods
- A method has multiple Params and a ReturnType.
    - These are reflected for example in the gRPC definition:
    - `rpc collectLive (stream EmployeeCollectLiveParam) returns (stream EmployeeCollectLiveResult);`
    - collectLive is the Method, EmployeeCollectLiveParam are the parameters where the parameters are
      grouped into an Parameter object as protbuf allows only one parameter
    - EmployeeCollectLiveResult, which contains the ReturnType


'''
from __future__ import annotations
import types
import re
from protmo.pm import *
from protmo.pm import _rpc_methods
from protmo.utils import *
from typing import Callable
from typing import List
from typing import Tuple


class MessageInfo:
    '''
    This is an abstract representation of the message defined by a
    model-class. It contains:
    - fields: The attributes, which assigned using the Field-Superclass,
        like StringField, Int32Field, etc.
    - rpc_methods: These are the methods, which are callable through
        the gRPC middleware and are annotated via @rpc in the models.py

    There are models and messages. We regard everything a model, which
    has the first field with the name id.
    '''

    def __init__(self, modelClass: type) -> None:
        self.name = modelClass.__name__
        self.modelClass = modelClass

        self.fields: list[Field] = self._extract_fields(modelClass)
        self.rpc_methods: list[Method] = self._extract_rpc_methods(modelClass)

        self.is_model = bool(len(self.fields) and self.fields[0].name == 'id')

    def _extract_fields(self, modelClass: type) -> List[Field]:
        '''
        Given a modelClass (a class that inherits from Message), it searches
        for attributes, whose type inherit from the Field-Supertype. For example
        StringField or Int32Field.
        '''

        fields = []
        for fieldName in dir(modelClass):
            if not fieldName.startswith('_'):
                field = getattr(modelClass, fieldName)
                if isinstance(field, Field):
                    field.name = fieldName
                    fields.append(field)
        fields.sort(key=lambda f: f.tag)
        return fields

    def _extract_rpc_methods(self, modelClass: type) -> List[Method]:
        '''
        A model class is a class the user of the library implements by extending the
        message-super type. It consits of attributes which can have a type which is a
        subtype of Field (like Int32Field) or it can have methods that are flagged
        with the annotation @rpc. This method takes such a model-class and extract all
        the methods that have such a flag. For Example:

        ```python
        class Employee(Message):
            @rpc
            def sayHello(self, name : Name) -> str:
                msg = self.messageBulider(name.firstName)
                return msg
        ```

        This method would return an AST-Representation of type Method of the rpc-method
        `sayHello`, including the return type, parameter list and addtitional metadata,
        which you can find in the class Method.
        '''

        res = []
        instance = modelClass()
        for fieldName in [f for f in dir(modelClass) if not f.startswith('_')]:
            field = getattr(modelClass, fieldName)
            instance_field = getattr(instance, fieldName)

            if field in _rpc_methods.keys():
                params = self._extract_params(field)
                client_side_streaming = any(
                    param.is_generator for param in params)
                returnTypeName, repeated, server_side_streaming = self._extract_return_type(
                    field)
                is_static = isinstance(instance_field, types.FunctionType)
                method = Method(
                    fieldName, params,
                    ReturnType(returnTypeName, repeated=repeated),
                    ref=field,
                    is_static=is_static,
                    clientSideStreaming=client_side_streaming,
                    serverSideStreaming=server_side_streaming
                )
                res.append(method)
        return res

    def _extract_params(self, field: Callable) -> List[Param]:
        '''
        This is part of the _extract_rpc_methods and extracts the parameter-
        list of a found method.
        '''
        annotations = field.__annotations__
        vars = field.__code__.co_varnames

        paramNames = [a for a in annotations.keys() if a in vars]
        paramNames.sort(key=lambda n: vars.index(n))

        params = []
        for p in paramNames:
            type_name, repeated, is_generator = self._extract_type_name(
                annotations[p])
            if type_name == 'Generator':
                print(annotations[p], self._extract_type_name(annotations[p]))
            params.append(
                Param(
                    type_name,
                    p,
                    annotations[p],
                    repeated=repeated,
                    is_generator=is_generator))

        return params

    def _extract_type_name(self, python_type: type) -> Tuple[str, bool, bool]:
        '''
        Used by _extract_params and _extract_return_type, it takes a python type and returns
        a type name. This is kind of complex, as:
        - a type could be a list[str] where it is a list of strings. In protobuf this is represented
          as repeated. Here, a simple type mapping like int->int32 is not possible as every type could
          be wrapped as list.
        - another complexity is that there can be client-side or server-side streaming or both. To achive
          that, we wrap the actual type T with a Generator[T, None, None] (see the stream()-helper method)
          Here we have to extract the actual type and mark that it is streaming.

        return-tuple:
        1. type-name: str
        2. repeated: bool
        3. is_generator: bool

        Thus an example usage is:
        `type_name, repeated, is_generator = self._extract_type_name(annotation)`
        '''

        python_type_str = str(python_type)
        is_generator = False

        # check if it is agenerator, by looking if its type-string starts with
        # Generator
        inner = re.search('^typing\\.Generator\\[(.*)\\]$', python_type_str)
        if inner:
            # if so, mark the 3. return value and extract the actual type name
            is_generator = True
            # generator consits of 3 types, keep only first, e.g.
            # Generator[str,NoneType,NoneType]
            python_type_str = inner.group(1).split(',')[0].strip()
            # we can't return immediatly, as the inner type of the Generator could be a list, which
            # we need to unpack first

        # now check, if the type is a list, wrapping the actual type. E.G.
        # list[str] should become str
        inner = re.search('^list\\[(.*)\\]$', python_type_str)
        if inner:  # it is actually a list
            # extract the the inner type
            is_list = True
            fully_qualified_name = inner.group(1)
            name = fully_qualified_name.split('.')[-1]
            # here we can return immediatly, as we already have extracted and marked the inner type
            # of a potential generator
            return name, is_list, is_generator

        # if generator, return the wrapped type which is stored in
        # python_type_str
        is_list = False
        if hasattr(python_type, '__name__') and not is_generator:
            return python_type.__name__, is_list, is_generator
        else:
            return python_type_str, is_list, is_generator

    def _extract_return_type(self, field: Callable) -> Tuple[str, bool, bool]:
        '''
        The return type is specified after the signature, like def abc() -> returnType
        We get it via the python annotations and extract the type-name of it the same
        way we do with the parameters (_extract_type_name)

        Returns a tuple (like _extract_type_name) with:
        - typeName: str
        - repeated: bool
        - is_generator: bool
        '''
        returnType = field.__annotations__.get('return')
        if not returnType:
            return 'Void', False, False
        name, repeated, is_generator = self._extract_type_name(returnType)
        return name, repeated, is_generator

    def __str__(self):
        '''
        This does not generate valid code in any language, but includes everything
        stored in the abstract model in a nice pseudo-code style.
        '''
        res = f'modelMessage {self.name} {{\n'
        for field in self.fields:
            res += f' {field}\n'

        for method in self.rpc_methods.keys():
            res += f' rpc {method};\n'
        res += '}'
        return res


class Method:
    '''
    A method has a name, parameter-list (List[Param]) and a return-type (ReturnType). It is part
    of the MessageInfo and will become an gRPC GrpcProcedure. There are these different types as
    described in gRPC:
    - Unary Call Method
    - Client Side Streaming
    - Server Side Streaming
    - Bidirectional Streaming (=Client+Server Side Streaming)

    Beside that, there are object-methods, which get a reference to an object as first parameter
    (and an ID to that object is transferred via RPCs) and static-methods which are part of the
    MessageInfo, but have to reference to it - like normal static methods.

    Sometimes it is useful to get a reference to the python-definition of the method, which was
    annotated with @rpc in a message-class that extended Message. This is stored in ref.

    '''

    def __init__(self,
                 name: str,
                 parameters: List[Param],
                 returnType: ReturnType,
                 ref: Callable = None,
                 is_static: bool = False,
                 clientSideStreaming: bool = False,
                 serverSideStreaming: bool = False) -> None:

        self.name = name
        self.parameters = parameters
        self.returnType = returnType
        self.ref = ref  # the method-reference to the original python-method
        self.is_static = is_static
        self.clientSideStreaming = clientSideStreaming
        self.serverSideStreaming = serverSideStreaming

    @property
    def has_params(self) -> bool:
        return bool(len(self.parameters))

    def __str__(self) -> str:
        '''
        Returns pseudo-code with everything we have stored about this
        the method.
        '''
        parmeterList = ', '.join([str(p) for p in self.parameters])
        staticFlag = 'static ' if self.is_static else ''

        params = parmeterList
        if self.clientSideStreaming:
            params = 'stream ' + params

        ret = str(self.returnType)
        if self.serverSideStreaming:
            ret = 'stream ' + ret

        return f'{staticFlag}{self.name} ({params}) -> {ret}'


class Param:

    '''
    Part of the Method-ast-class. One method has multiple parameters.
    repeated indicates that the the type if a list of the given pythonType.
    ref gives you a python-reference to the python-Type of the parameter.
    is_generator hints, if you have client-side-streaming for this parameters.
    '''

    def __init__(
            self,
            pythonType: str,
            name: str,
            ref: type = None,
            repeated: bool = False,
            is_generator: bool = False):
        self.pythonType = pythonType
        self.name = name
        self.ref = ref
        self.repeated = repeated
        self.is_generator = is_generator

    def __str__(self) -> str:
        return f'{self.name} : {self.pythonType}'


class ReturnType:
    '''
    Part of the Method-ast-class. One method has a single ReturnType.
    '''

    def __init__(self, python_type: str, repeated: bool = False):
        self.python_type = python_type
        self.repeated = repeated

    @property
    def is_void(self) -> bool:
        return self.python_type == 'Void'

    def __str__(self) -> str:
        res = str(self.python_type)
        if self.repeated:
            res = 'repeated ' + res
        return res
