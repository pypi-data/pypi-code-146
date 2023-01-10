from kfsdutils.apps.endpoints.handlers.core.utils import DictUtils

from django.db.models import Q


class BaseHandler():
    ARG_NAME_IDENTIFIER = "identifier"
    ARG_NAME_SERIALIZER = "serializer"
    ARG_NAME_MODELCLASS = "modelClass"
    ARG_NAME_ISDBFETCH = "isDBFetch"

    def __init__(self, **kwargs):
        self.__modelSerializer = DictUtils.getDictValue(kwargs, self.ARG_NAME_SERIALIZER)
        self.__modelClass = DictUtils.getDictValue(kwargs, self.ARG_NAME_MODELCLASS)
        self.__identifier = DictUtils.getDictValue(kwargs, self.ARG_NAME_IDENTIFIER)
        isDBFetch = DictUtils.getDictValue(kwargs, self.ARG_NAME_ISDBFETCH)
        self.__modelQS = self.getQS(self.__identifier) if isDBFetch else None
        self.__modelQSData = self.getModelQSDataFromDB(self.__identifier) if isDBFetch else None

    def dbFetch(self):
        self.__modelQS = self.getQS(self.__identifier)
        self.__modelQSData = self.getModelQSDataFromDB(self.__identifier)

    def getModelClass(self):
        return self.__modelClass

    def getQS(self, objIdentifier):
        return self.getModelClass().objects.get(identifier=objIdentifier)

    def exists(self):
        if self.getModelClass().objects.filter(identifier=self.__identifier).exists():
            return True
        return False

    def create(self, **kwargs):
        return self.getModelClass().objects.create(**kwargs)

    def update(self, **kwargs):
        return self.getModelClass().objects.update(**kwargs)

    def delete(self):
        if self.exists():
            self.getModelQS().delete()

    def getModelQSData(self):
        return self.__modelQSData

    def setModelQSData(self, data):
        self.__modelQSData = data

    def getModelQS(self, refresh=False):
        if refresh:
            self.__modelQS = self.getQS(self.__identifier)
        return self.__modelQS

    def refreshModelQSData(self):
        self.__modelQSData = self.getModelQSDataFromDB(self.__identifier)

    def getModelSerializer(self):
        return self.__modelSerializer

    def getIdentifier(self):
        return self.__identifier

    def getModelQSDataFromDB(self, objIdentifier):
        serializedData = self.getModelSerializer()(self.getQS(objIdentifier))
        return serializedData.data

    def getQStoSerializerMany(self, qs):
        serializedData = self.getModelSerializer()(qs, many=True)
        return serializedData

    def getIdentifiersQS(self, identifiers):
        query = Q(identifier__in=identifiers)
        return self.getModelClass().objects.distinct().filter(query)

    def getFilterQS(self, queries):
        return self.getModelClass().objects.distinct().filter(queries)

    def search(self, modelClass, queries):
        return modelClass.objects.distinct().filter(queries)
