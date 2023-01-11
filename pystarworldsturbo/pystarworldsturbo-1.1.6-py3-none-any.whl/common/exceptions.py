class ActionException(Exception):
    def __init__(self, message):
        super(ActionException, self).__init__(message)


class ActorException(Exception):
    def __init__(self, message):
        super(ActorException, self).__init__(message)


class IdentityException(ActorException):
    def __init__(self, message):
        super(IdentityException, self).__init__(message)


class EnvironmentException(Exception):
    def __init__(self, message):
        super(EnvironmentException, self).__init__(message)


class PhysicsException(EnvironmentException):
    def __init__(self, message):
        super(PhysicsException, self).__init__(message)


class PerceptionException(Exception):
    def __init__(self, message):
        super(PerceptionException, self).__init__(message)


class CommunicationException(Exception):
    def __init__(self, message):
        super(CommunicationException, self).__init__(message)


class MessageException(CommunicationException):
    def __init__(self, message):
        super(MessageException, self).__init__(message)
