from jija_orm import models


class ModelSerializer:
    class Empty:
        pass

    def __init__(self, model: 'models.Model'):
        self.__model = model
        self.__fields = self.get_fields()

    def get_fields(self):
        return self.__model.get_fields()

    def serialize(self, record):
        data = {}
        for field in self.__fields:
            attr = record.get(field, self.Empty)
            if attr is self.Empty:
                continue

            data[field] = attr

        return models.SerializedModel(**data)
