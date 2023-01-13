from pyqalx.core.entities.entity import QalxFileEntity


class Factory(QalxFileEntity):
    """
    A factory is an entity that allows for the interaction of bots that can
    execute code from different locations

    Class attributes
        entity_type:    The qalx type is factory
    """

    entity_type = "factory"
    _file_key = "plan"
