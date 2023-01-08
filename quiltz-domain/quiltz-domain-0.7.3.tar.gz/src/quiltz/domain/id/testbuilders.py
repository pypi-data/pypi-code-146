from quiltz.domain.id import ID 
import uuid


def aValidUUID(simpleIdValue):
    return uuid.UUID("{:>32}".format(simpleIdValue).replace(' ', '1'))


def aValidID(simpleIdValue):
    return ID(aValidUUID(simpleIdValue))
