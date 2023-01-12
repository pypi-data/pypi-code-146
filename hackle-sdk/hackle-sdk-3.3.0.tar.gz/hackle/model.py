import abc

from six import add_metaclass


class User(object):
    def __init__(self, id, properties):
        self.id = id
        self.properties = properties

    def __str__(self):
        return 'User(id={}, properties={})'.format(self.id, self.properties)


class HackleUser(object):
    def __init__(self, id=None, user_id=None, device_id=None, identifiers=None, properties=None):
        self.id = id
        self.user_id = user_id
        self.device_id = device_id
        self.identifiers = identifiers
        self.properties = properties

    def __str__(self):
        return 'HackleUser(id={}, user_id={}, device_id={}, identifiers={}, properties={})'.format(self.id,
                                                                                                   self.user_id,
                                                                                                   self.device_id,
                                                                                                   self.identifiers,
                                                                                                   self.properties)

    @staticmethod
    def builder():
        return HackleUserBuilder()

    @staticmethod
    def of(user):
        return HackleUser.builder().id(user.id).properties(user.properties).build()


class HackleUserBuilder:

    def __init__(self):
        self.__id = None
        self.__user_id = None
        self.__device_id = None
        self.__identifiers = {}
        self.__properties = {}

    def id(self, id):
        self.__id = id
        return self

    def user_id(self, user_id):
        self.__user_id = user_id
        return self

    def device_id(self, device_id):
        self.__device_id = device_id
        return self

    def session_id(self, session_id):
        return self.identifier("$sessionId", session_id)

    def identifier(self, identifier_type, identifier_value):
        self.__identifiers[identifier_type] = identifier_value
        return self

    def identifiers(self, identifiers):
        if identifiers is None:
            return self

        if not isinstance(identifiers, dict):
            return self

        for identifier_type in identifiers:
            self.identifier(identifier_type, identifiers[identifier_type])

        return self

    def property(self, property_key, property_value):
        self.__properties[property_key] = property_value
        return self

    def properties(self, properties):
        if properties is None:
            return self

        if not isinstance(properties, dict):
            return self

        for property_key in properties:
            self.property(property_key, properties[property_key])

        return self

    def build(self):
        return HackleUser(
            self.__id,
            self.__user_id,
            self.__device_id,
            self.__identifiers,
            self.__properties,
        )


class Event(object):
    def __init__(self, key, value, properties):
        self.key = key
        self.value = value
        self.properties = properties


class Hackle:
    @staticmethod
    def user(id, **kwargs):
        return User(id, kwargs)

    @staticmethod
    def event(key, value=None, **kwargs):
        return Event(key, value, kwargs)


@add_metaclass(abc.ABCMeta)
class HackleRemoteConfig(object):
    @abc.abstractmethod
    def get(self, key, default=None):
        pass
