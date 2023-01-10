'''
This file contains the stuff you need to express your model
'''

from typing import Generator

from google.protobuf.json_format import ParseDict
import sys
from typing import Any
from protmo.name_to_protobuf import *
from protmo.provide import use_provided


def request_user():
    USER_KEY = 2
    return use_provided(USER_KEY)


def db():
    from protmo.db import DB_KEY
    return use_provided(DB_KEY)


class Message:
    '''
    To define your model, create classes which extend this class. Then
    create class-level attributes where different FieldTypes are assigned,
    like StringField or Int32Field.
    You can mark all methods that you want to call from your client with
    the @rpc annotation (see the rpc-function in this file for details).

    Example:

    ```python
    class Employee(Message):
        id = StringField(1)
        firstName = StringField(2, default=lambda self: f'no name {self.age}')
        age = Int32Field(3)
        roles = StringField(4, repeated=True)
        address = EmbeddedField(5, Address)
        dresses = EmbeddedField(6, Dress, repeated=True)
        createdAt = Int64Field(7, onCreate=currentTimestamp)
        lastUpdatedAt = Int64Field(8, onUpdate=currentTimestamp)

        @rpc
        def summarizeModel(self) -> str:
            return f'{self.id} | {self.firstName} {self.age}, {self.roles}'

        @rpc
        def sayHello(self, name : Name) -> str:
            msg = self.messageBulider(name.firstName)
            return msg
    ```
    '''

    def __init__(self, *arg, **kwargs):
        '''
        Prepares the kwargs for protobuf, creates a probouf message and sets the
        data passed via kwargs to it. Message is a wrapper around a protobuf message
        using __getattribute__ and __setattribute__ and the protobuf-message is
        responsible of holding the data, while this class can add "extension-methods"
        to it.
        Beside that this constructor does house-keeping like setting the names of its
        fields and sets up lazy-loading.
        '''

        # Set the names to the fields
        #  ===========================
        # We define the fields like: `address = EmbeddedField(5, Address)`
        # where the EmbeddedField is a field. But now, the field-name is external
        # to the constructor call - on the left hand side of the equal sign (address)
        # Thus we have to set it here from external, where we have both access to the
        # field and the name of the message-field-attribute
        # self.__class__ -- the same as self.__class__, but go around
        # __getattribute__
        cls = object.__getattribute__(self, '__class__')
        for fieldName in [f for f in dir(cls) if not f.startswith('_')]:
            field = _getattr_or_none(cls, fieldName)
            if not field:
                continue
            if isinstance(field, Field):
                field.name = fieldName

        # Replace ReferenceField-values with ID-strings pointing to the references object
        #  ===============================================================================
        # In the end of the day, we want to construct the kwargs and pass it to the
        # proto-model which we wrap. This proto model contains all the data and we
        # wrap it via the __getattribute__-method.
        # But when there is a ReferenceField, we don't want to give the real reference
        # to the protobuf-model, but only the id. Protobuf is always serializable and
        # in this world, references are IDs to other messages, not python-object-refs.
        # Therefore, we loop over the kwargs, get the field of this message to get the
        # type of it. Now we can check if it is a Reference field and if so, extract
        # the ID and replace the entry in the kwargs with it.
        # The same idea, but within a list applies when the field is also
        # repeated.
        referenceIdFields = {}
        for name in kwargs.keys():
            field = _getattr_or_none(self, name)
            if not field:
                continue
            if isinstance(field, ReferenceField):
                if field.repeated:
                    referenceIdFields[field.name] = [
                        o.id for o in kwargs[name]]
                else:
                    referenceIdFields[field.name] = kwargs[name].id
        # because referenceIdFields come second, they override
        kwargs = {**kwargs, **referenceIdFields}

        # Initialized the wrapped Proto-Message
        #  =====================================
        # Create a protobuf-instance as data-container and initalize it with the data we got
        # via kwargs. In this way to user can use the Message class as if it would be a
        # proto-message and we can extend our functionality around it.
        name = cls.__name__
        proto = name_to_grpc_message_or_method(name)()
        proto = ParseDict(kwargs, proto, ignore_unknown_fields=True)
        # We use the Message class to wrap the proto-message-class which holds the actual data.
        # thus we set the data into the proto-attribute and whenever someone asks us for data
        # we take it from there
        # required to do it with __setattr__, as __setattr__ already needs
        # self.proto
        super().__setattr__('proto', proto)

        # Initalize Lazy Loading
        #  ======================
        # self._loaded indicates, if the data is loaded from the database. We often only transfer
        # the ID of the model over the wire. In this case, the have to take this ID and ask the
        # database for the data belongin to this ID and set it to the fields. But we want to do this
        # lazy. Thus we initialize the class with only the ID, set the _loaded=False (which is done
        # by the web layer) and as soon as the DB set the data, it sets it back
        # to _loaded=False
        self._loaded = True  # per default, the ORM- or Web-Layer should set it to False, if not

    # TODO: isn't __getattr__ more suitable?

    def __getattribute__(self, name):
        '''
        As Message is in the runtime only a wrapper around protobuf, return the data from the
        self.proto
        But there is additional functionality we want like lazy loading or ReferenceFields which
        have to be resolved on the fly
        '''

        def attr(n: str) -> Any:
            '''
            A little helper to access fields of the Message-Object and not run into
            recursion as self.n would call __getattribute__(self, n) and so on.
            '''
            return object.__getattribute__(self, n)

        def take_value_from_proto_and_maybe_lazy_load():
            # do not lazy load, if
            #   - the requested attribute is id, as is is has to be already present, thus no need for lazy loading
            #   - we not already have done so. The DB- and Web-Layer set _loaded to false when creating an instance
            #   - the ID is not set, lazy loading converts the ID to the data
            if not name == 'id' and not attr('_loaded') and attr('id'):
                db_result = self.db.query(
                    attr('proto').__class__, {
                        '_id': attr('_id')})
                if db_result:
                    loaded_doc_from_db = db_result[0]
                    setattr(self, 'proto', loaded_doc_from_db)
                    # when using only setattr, the getattr outide the if gets still
                    # the old message. It works, when doing it a second time, but this
                    # is too hacky. I don't know why. If we return the value of the
                    # freshly loaded object it works on the first try.
                    # DO NOT DELETE !! read the comment above!
                    return getattr(loaded_doc_from_db, name)

            # lazy loading not required / has no effect. Return the value already in the proto-message
            # This should be the normal case
            return getattr(proto, name)

        # normal case, if values are present and lazy-loading
        #  ===================================================
        # If the proto-message has the given field we can return it
        # directoly or load it on the fly
        proto = attr('proto')
        if hasattr(proto, name):
            return take_value_from_proto_and_maybe_lazy_load()

        # ReferenceFields (Foreign Keys) Lazy Loading
        #  ==============================================
        # If the proto-message does not have the requested field, check if it
        # is an reference field.
        # References of Reference-Fields only contain the ID to the referenced
        # objects, thus are always lazy. This means, that we have to load them
        # on the fly.
        # More complexity is added because we alsow allow repeated ReferenceFields
        # to allow unidirectoral Many-To-Many definition
        attribute_value = attr(name)
        if isinstance(attribute_value, ReferenceField):  # lazy load first!

            if attribute_value.repeated:
                foreign_objects_ids = list(
                    getattr(attr('proto'), attribute_value.name))
                db_res = self.db.query(
                    attribute_value.otherClass, {
                        '_id': {
                            '$in': foreign_objects_ids}})
                if not db_res:
                    return []
                setattr(self, name, db_res)
                return db_res

            else:  # not repeatet
                foreign_object_id = getattr(
                    attr('proto'), attribute_value.name)
                if foreign_object_id:
                    db_res = self.db.query(
                        attribute_value.otherClass, {
                            '_id': foreign_object_id})
                    if not db_res:
                        return None  # Or create an empty instance ??
                    attribute_value = db_res[0]
                    # cache for the next time (getattr will pick it up)
                    setattr(self, name, attribute_value)
                    return attribute_value

                # in this case, there is no id assigned yet. Initalize an empty container, so that the user still
                # can set attributes this is only relevant, if not repeated. In the latter case it would just be
                # an empty list and we can expect that the user adds new
                # instances to the list.
                else:
                    attribute_value = attribute_value.otherClass()
                    setattr(self, name, attribute_value)
                    return attribute_value

        # Return attribute of extended class
        #  ==================================
        # If it not a reference-field and not part of the proto-message, it has to be defined
        # in the extended Message-Class by the user, e.g. by self.abc = 'value'
        # In this case, we can just return the value, we obtained via attr(name) which is like
        # calling self.`name`

        return attribute_value

    def __setattr__(self, name, value):
        '''
        If the proto-message has the attribute, set the value there
        else set it to this class.
        '''
        if hasattr(self.proto, name):
            return setattr(self.proto, name, value)
        return super().__setattr__(name, value)

    def __str__(self):
        return str(self.proto)

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.proto == other.proto

    def set_defaults(self, creating=False):
        '''
        Called by the database-layer on store (either on create or update)
        Gives a hook to set the right defaults at the right time.
        Itererates through the fields and calls their set_defaults. Thus
        it distributes the work down. See the subclasses of Field for
        details.
        '''
        c = object.__getattribute__(self, '__class__')
        for fieldName in [f for f in dir(c) if not f.startswith('_')]:
            field = object.__getattribute__(self, fieldName)
            if isinstance(field, Field):
                field.name = fieldName
                field.set_defaults(self, creating)

    @property
    def db(self):
        '''
        When the user defines the model, this class is extended. Within the
        methods, he wants to use self.db -> This becomes possible with this.
        It is set by the server, which connects to the correct database for
        every request.

        Also used for lazy-loading resolve in the __getattribute__ part.
        '''
        return db()

    # @property
    # def user(self):
    # pass # TODO -> Already set by GenericServer->__getattribute__->handler


def _getattr_or_none(obj, name):
    '''
    As Message implements __getattribute__, it captures a lot. This helper goes around this
    and looks the attribute up and returns it. If it does not exist, it returns None.
    '''
    try:
        # the same as self.name, but go around __getattribute__
        return object.__getattribute__(obj, name)
    except AttributeError:
        return None


class Field:
    '''
    This is the abstract representation of the field in the models.py.
    A message has multiple fields and you create them by adding them to
    your class, which inherits from Message.
    Give it a name and specify the field type. For example:

    class MyMessage(Message):
        id = StringField(1)
        age = Int32Field(3)
        address = EmbeddedField(5, Address)
        something = 'abc'

    Here, id, age and address are fields, but something is not as a string
    is assigned, which does not inherit from Field.

    Fields always have
    - a tag to make them unique, even if you change the
      name, as it is done in probuf.
    - repeated, as in protobuf
    - default, to set a value automatically via a callback if it is empy
    - onCreate and onUpdate which are callbacks that are triggered when
      these events happen
    '''

    def __init__(
            self,
            tag,
            repeated=False,
            default=None,
            onCreate=None,
            onUpdate=None):
        # The name is not known at the constructor-call, as we have the assignment
        # `age = Int32Field(3)` where the name is left of the `=` and thus not part of
        # the parameter list. It will be set externally by the constructor of
        # Message
        self._name = None
        self.tag = tag  # like protobuf tags (the numbers)
        self.repeated = repeated
        self.default = default
        self.onCreate = onCreate
        self.onUpdate = onUpdate

    def __str__(self):
        t = self.protoType
        if self.repeated:
            t = 'repeated ' + str(t)
        return f'{t} {self.name} = {self.tag};'

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def set_defaults(self, target, creating: bool = False):
        '''
        This is called by Message.set_defaults for all its fields. The set_defaults of the
        message is called by the database on store, which means either on create or on update.
        '''

        if self.default and not getattr(target, self.name):
            setattr(target, self._name, self.default(target))
        if creating and self.onCreate:
            setattr(target, self._name, self.onCreate(target))
        if self.onUpdate:
            setattr(target, self._name, self.onUpdate(target))


class DoubleField(Field):
    protoType = 'double'


class FloatField(Field):
    protoType = 'int32'


class Int32Field(Field):
    protoType = 'int32'


class Int64Field(Field):
    protoType = 'int64'


class UInt32Field(Field):
    protoType = 'uint32'


class UInt64Field(Field):
    protoType = 'uint64'


class SInt32Field(Field):
    protoType = 'sint32'


class SInt64Field(Field):
    protoType = 'sint64'


class Fixed32Field(Field):
    protoType = 'fixed32'


class Fixed64Field(Field):
    protoType = 'fixed64'


class SFixed32Field(Field):
    protoType = 'sfixed32'


class SFixed64Field(Field):
    protoType = 'sfixed64'


class BoolField(Field):
    protoType = 'bool'


class StringField(Field):
    protoType = 'string'


class BytesField(Field):
    protoType = 'bytes'


class EmbeddedField(Field):
    '''
    Other messages can either be referenced (ReferenceField) or embedded (EmbeddedField).
    When embedded, the complete message is part of its parent.
    '''

    def __init__(self, tag, other, repeated=False):
        if isinstance(other, Late):
            other = other()  # for cyclic refs, wrap in lambda
        self.other = other
        self.protoType = other.__name__ if hasattr(
            other, '__name__') else str(other)
        super().__init__(tag, repeated=repeated)


class ReferenceField(Field):
    '''
    Other messages can either be referenced (ReferenceField) or embedded (EmbeddedField).
    When referenced, only the ID of the other message becomes part of this message and
    becomes lazy, which means that it only loaded/resolved if needed.
    '''

    def __init__(self, tag, other, repeated=False):
        if isinstance(other, Late):
            other = other()  # for cyclic refs, wrap in lambda
        self.other = other
        self.protoType = 'string'  # IDs are always strings, and we only store IDs
        super().__init__(tag, repeated=repeated)

    @property
    def name(self) -> str:
        if self._name is None:
            return self._name
        suffix = 'Id'
        if self.repeated:
            suffix = 'Ids'
        return self._name + suffix

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def otherClass(self) -> type:
        return self.other


_rpc_methods = {}


def rpc(*args, **kwargs):
    '''
    Adds the function annotated with @rpc to the dict _rpc_methods,
    optionally with parameters @rpc(param1='val1')


    There are two big different cases, when using the @rpc annotation:
    - @rpc
    - @rpc(key=value)

    If you look closely, you see, that the second is actually a function
    call.

    We have to detect and handle both cases. When it its a function call
    it "peels off" one layer, thus we have to return a result with one
    layer more.

    To detecht, if @rpc or @rpc(...) was used we use
    ```
    len(args) == 1 and callable(args[0]):
    ```
    In this case, there are no arguments, thus we just add the method to
    the methods to remember and are finished

    Otherwise, we use inner_gen to wrap the result in another layer and
    pass the arguments to make them accessible to inner (within inner_gen).
    `inner` is called then with the method as argument. Now we have the
    function-pointer AND the parameters in the body of inner. Now we can
    add the parameters to the _rpcs_methods
    '''

    def unpack(method):
        '''
        Staticmethods are wrapped. To get the real function-pointer,
        we have to use the __func__ methos. This helper returns the
        function pointer to the given method while handling this.
        '''
        if isinstance(method, staticmethod):
            return method.__func__  # static is wrapped, so unwrap
        return method

    def inner_gen(**kwargs):
        def inner(method):
            _rpc_methods[unpack(method)] = kwargs
            return method
        return inner

    # if @rpc without parantheses is used:
    if len(args) == 1 and callable(args[0]):
        method = args[0]
        _rpc_methods[unpack(method)] = {}
        return method

    return inner_gen(**kwargs)


def stream(T: type) -> Generator:
    '''
    This is a helper method to express in the model, that you either
    expect a stream or result one. Example:

    @rpc
    def greetInDifferentWays(self, requests : stream(str)) -> str:
        ...

    or

    @rpc
    def userInfoStream(self) -> stream(str):
        ...

    It is kind of syntactical sugar, as we only want to carry along
    the type T and the information that it is a generator. But we don't
    need the second and third argument. Thus this method, which makes
    them invisible.
    Also, it adjusts the wording, as we don't have Generators with gRPC
    but streams.
    '''
    return Generator[T, None, None]


class Late:
    '''
    Sometimes, you have cyclic references, like:

    class Employee:
        patient = ReferenceField(Patient)

    class Patient:
        last_emplyee = ReferenceField(Employee)

    This does not work, as Patient is not defined when Employee
    is defined. Changing order does not help.

    To solve this, you can wrap the reference with this class:

    class Employee:
        patient = ReferenceField(Late('Patient'))

    class Patient:
        last_emplyee = ReferenceField(Employee)
    '''

    # TODO: create a test-case using this feature

    def __init__(self, ResultClassStr, package):
        self.ResultClassStr = ResultClassStr
        self.package = package

    def __call__(self):
        return getattr(sys.modules[self.package], self.ResultClassStr)()
