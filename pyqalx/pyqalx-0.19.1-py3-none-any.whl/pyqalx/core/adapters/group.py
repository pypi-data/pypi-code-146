from pyqalx.core.adapters.adapter import QalxUnpackableAdapter
from pyqalx.core.entities import Group


class QalxGroup(QalxUnpackableAdapter):
    """
    Provides an interface for accessing the API for
    :class:`~pyqalx.core.entities.group.Group` entities
    """

    _entity_class = Group
    child_entity_class = Group.child_entity_class

    def add(self, sets, meta=None, **kwargs):
        """
        When adding a `Group` ensure that the sets posted to the api are in
        the format {<key>: :class:`~pyqalx.core.entities.set.Set`}

        :param sets: A dictionary of Sets to create on the group
        :type sets: dict
        :param meta: A dictionary of metadata to store
        :type meta: dict
        :return: A newly created `Group` instance
        """
        return super(QalxGroup, self).add(sets=sets, meta=meta, **kwargs)

    def get(self, guid, child_fields=None, unpack=False, *args, **kwargs):
        """
        Gets the entity for the given `guid` and unpacks it if specified.
        Provide `child_fields` to restrict the fields returned on unpacked
        children


        :param guid: The `guid` of the entity to get
        :type guid: str
        :param child_fields: A list of fields that should be returned from
                             child entities
        :type child_fields: list
        :param unpack: Should the child entities be unpacked. Defaults to False
        :type unpack: bool
        :return: An unpacked entity
        """
        return super(QalxGroup, self).get(
            guid, child_fields=child_fields, unpack=unpack, *args, **kwargs
        )

    def reload(self, entity, unpack=False, *args, **kwargs):
        """
        Reloads the current entity from the API.

        :param entity: An instance of `self.entity_class`
        :param unpack: Should the child entities by unpacked?  Defaults to False
        :type unpack: bool
        :return: A refreshed instance of `self.entity_class`
        """
        return super(QalxGroup, self).reload(
            entity, unpack=unpack, *args, **kwargs
        )

    def find(
        self,
        query=None,
        sort=None,
        skip=0,
        limit=25,
        many=True,
        child_fields=None,
        include_session_tags=True,
        *args,
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
        # extended to create better autodocs
        return super(QalxGroup, self).find(
            query=query,
            sort=sort,
            skip=skip,
            limit=limit,
            many=many,
            include_session_tags=include_session_tags,
            child_fields=child_fields,
            *args,
            **kwargs
        )

    def find_one(self, query, unpack=False, **kwargs):
        """
        Method for returning a unique entity. Will return the entity that
        matches the query

        :param query: The mongoDB query
        :type query: dict
        :param unpack: Should any child entities be automatically unpacked?
        :type unpack: bool
        :return: :class:`~pyqalx.core.entities.group.Group`
        :raises QalxMultipleEntityReturned:
        :raises QalxEntityNotFound:
        """
        return super(QalxGroup, self).find_one(query, unpack=unpack, **kwargs)

    def aggregate(self, aggregate, **kwargs):
        # extended to create better autodocs
        return super(QalxGroup, self).aggregate(aggregate=aggregate, **kwargs)

    def save(self, entity, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxGroup, self).save(entity=entity, *args, **kwargs)
