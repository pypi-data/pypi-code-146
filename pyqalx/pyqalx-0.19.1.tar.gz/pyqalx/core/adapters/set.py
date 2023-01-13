from pyqalx.core.adapters.adapter import (
    QalxUnpackableAdapter,
    QalxValidateBlueprintAdapter,
)
from pyqalx.core.entities import Set


class QalxSet(QalxValidateBlueprintAdapter, QalxUnpackableAdapter):
    """
    Provides an interface for accessing the API for
    :class:`~pyqalx.core.entities.set.Set` entities
    """

    _entity_class = Set
    child_entity_class = Set.child_entity_class

    def add(self, items, meta=None, blueprint_name=None, **kwargs):
        """
        When adding a `Set` ensure that the items posted to the api are in the
        format {<key>: :class:`~pyqalx.core.entities.item.Item`}

        :param items: A dictionary of Items to create on the set
        :type items: dict
        :param meta: A dictionary of metadata to store on this set
        :type meta: dict
        :param blueprint_name: An optional blueprint
         name to use if you want to validate this set against an existing Blueprint
        :type blueprint_name: str
        :return: :class:`~pyqalx.core.entities.set.Set`

        """
        return super(QalxSet, self).add(
            items=items, blueprint_name=blueprint_name, meta=meta, **kwargs
        )

    def get(self, guid, child_fields=None, unpack=True, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxSet, self).get(
            guid, child_fields, unpack, *args, **kwargs
        )

    def save(self, entity, blueprint_name=None, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxSet, self).save(
            entity, blueprint_name, *args, **kwargs
        )

    def find(
        self,
        query=None,
        sort=None,
        skip=0,
        limit=25,
        many=True,
        include_session_tags=True,
        **kwargs
    ):
        """
        Return multiple packed entities from the API

        :param query: The optional Mongo query to find entities
        :type query: dict
        :param sort: The keys to sort by
        :type sort: list
        :param skip: The number of results to skip (offset) by
        :type skip: int
        :param limit: How many results should the response be limited to
        :type limit: int
        :param many: Should many entities be returned or just a single one
        :type many: bool
        :param include_session_tags:    Should the tags for the session be
                                        included in the query. Default is True
        :type include_session_tags: bool
        :param child_fields: A list of fields that should be returned from
                             child entities
        :type child_fields: list
        :return: A list of entities
        """
        return super(QalxSet, self).find(
            query=query,
            sort=sort,
            skip=skip,
            limit=limit,
            many=many,
            include_session_tags=include_session_tags,
            **kwargs
        )

    def find_one(self, query, unpack=True, **kwargs):
        """
        Method for returning a unique entity. Will return the entity that
        matches the query

        :param query: The mongoDB query
        :type query: dict
        :param unpack: Should any child entities be automatically unpacked?
        :type unpack: bool
        :return: an instance of `self.entity_class`
        :raises QalxMultipleEntityReturned:
        :raises QalxEntityNotFound:
        """
        return super(QalxSet, self).find_one(
            query=query, unpack=unpack, **kwargs
        )

    def reload(self, entity, unpack=True, *args, **kwargs):
        """
        Reloads the current entity from the API.

        :param entity: An instance of Set
        :type entity: pyqalx.core.entities.set.Set
        :param unpack: Should the child entities by unpacked?  Defaults to False
        :type unpack: bool
        :return: :class:`~pyqalx.core.entities.set.Set`
        """
        return super(QalxSet, self).reload(
            entity=entity, unpack=unpack, **kwargs
        )

    def aggregate(self, aggregate, **kwargs):
        # extended to create better autodocs
        return super(QalxSet, self).aggregate(aggregate=aggregate, **kwargs)
