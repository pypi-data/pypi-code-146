from copy import deepcopy

from pyqalx.core.adapters.adapter import (
    QalxNamedEntityAdapter,
    QalxUnpackableAdapter,
)
from pyqalx.core.entities.blueprint import Blueprint
from pyqalx.core.errors import QalxInvalidBlueprintError


class QalxBlueprint(QalxUnpackableAdapter, QalxNamedEntityAdapter):
    """
    Provides an interface for accessing the API for
    :class:`~pyqalx.core.entities.blueprint.Blueprint` entities
    """

    _entity_class = Blueprint
    child_entity_class = Blueprint

    def _validate(self, **kwargs):
        """
        Validates that the blueprint is in the correct format, handling
        potential issues if it is a nested schema
        """
        # The _kids_for_lookup method does everything we need in order to
        # determine the nested kids, so just call that with validate=True
        self._kids_for_lookup(entity=kwargs)
        return super(QalxBlueprint, self)._validate(**kwargs)

    def _check_schema(self, schema):
        self._entity_class({}).check_schema(schema)

    def add(self, name, schema, meta=None, **kwargs):
        """
        Adds a :class:`~pyqalx.core.entities.blueprint.Blueprint` with a
        valid `jsonschema` `schema`.
        If the `schema` is invalid then a `jsonschema.SchemaError` is raised

        :param name: The name of this blueprint
        :type name: str
        :param schema: The schema that you want to set on the Blueprint.
        :type schema: dict
        :param meta: A dictionary of metadata to store
        :type meta: dict

        :return: :class:`~pyqalx.core.entities.blueprint.Blueprint`
        :raises: jsonschema.SchemaError
        """
        self._check_schema(schema)
        entity_type = schema.get("entity_type", None)
        if entity_type is None:
            raise QalxInvalidBlueprintError(
                "schema must specify "
                "`entity_type` top level key which "
                "has a valid `entity_type` as the "
                "value"
            )
        return super(QalxBlueprint, self).add(
            name=name,
            schema=schema,
            entity_type=entity_type,
            meta=meta,
            **kwargs,
        )

    def save(self, entity, **kwargs):
        """
        Saves any updates to the given
        :class:`~pyqalx.core.entities.blueprint.Blueprint`.  Validates that
        the `schema` on the entity is a valid `jsonschema` schema

        :param entity: A valid Blueprint instance
        :type entity: ~pyqalx.core.entities.blueprint.Blueprint
        :param kwargs: Any kwargs you want to save against this `Blueprint`
        :return: :class:`~pyqalx.core.entities.blueprint.Blueprint`
        :raises: jsonschema.SchemaError
        """
        if "schema" in entity.keys():
            self._check_schema(entity["schema"])
        return super(QalxBlueprint, self).save(entity=entity, **kwargs)

    def get(self, guid, child_fields=None, unpack=True, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxBlueprint, self).get(
            guid=guid, child_fields=child_fields, unpack=unpack, *args, **kwargs
        )

    def get_by_name(self, name, **kwargs):
        # extended to create better autodocs
        return super(QalxBlueprint, self).get_by_name(name=name, **kwargs)

    def get_or_create(self, name, meta=None, **kwargs):
        # extended to create better autodocs
        return super(QalxBlueprint, self).get_or_create(
            name=name, meta=meta, **kwargs
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
        **kwargs,
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
        return super(QalxBlueprint, self).find(
            query=query,
            sort=sort,
            skip=skip,
            limit=limit,
            many=many,
            include_session_tags=include_session_tags,
            child_fields=child_fields,
            *args,
            **kwargs,
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
        # extended to create better autodocs
        return super(QalxBlueprint, self).find_one(
            query, unpack=unpack, **kwargs
        )

    def reload(self, entity, unpack=True, *args, **kwargs):
        """
        Reloads the current entity from the API

        :param entity: An instance of Blueprint
        :type entity: ~pyqalx.core.entities.blueprint.Blueprint
        :param unpack: Should any child entities be automatically unpacked?
        :type unpack: bool
        :return: A refreshed instance of `self._entity_class`
        """
        # extended to create better autodocs
        return super(QalxBlueprint, self).reload(
            entity=entity, unpack=unpack, *args, **kwargs
        )

    def aggregate(self, aggregate, **kwargs):
        # extended to create better autodocs
        return super(QalxBlueprint, self).aggregate(
            aggregate=aggregate, **kwargs
        )

    @staticmethod
    def _kids_properties(entity):
        """
        A Blueprint may not be nested (i.e. if it's an Item Blueprint).
        Therefore, check get the kids properties by checking if the "schema"
        key is there (may not be if "schema" wasn't returned from the API,
        and check that `kids` is there (may not be if not nested blueprint)
        :param entity: An instance of Blueprint
        :return: Boolean determining if this Blueprint is nested
        """
        schema = entity.get("schema", {}).get("properties", {})
        # currently the only nested blueprint can be Sets. Which
        # will have the kids nested using the `items` key
        kids = schema.get("items", {}).get("properties")
        return kids

    def _kids_for_lookup(self, entity):
        """
        The blueprint kids will be nested deeply in the schema as enums.
        We should iterate through them (checking to make sure each nested
        key only has a single enum) and return them
        :param entity: The blueprint entity
        :type entity: instance of Blueprint
        :return:The child blueprint names as list
        """
        blueprint_names = []
        if self._kids_properties(entity):
            # Build the blueprint names to lookup - handling either no
            # blueprint name or too many blueprint names
            for key, value in self._kids_properties(entity).items():
                child_blueprint_name = value.get("enum")
                if child_blueprint_name:
                    if len(child_blueprint_name) > 1:
                        # Can only happen if a user builds a schema themselves
                        raise QalxInvalidBlueprintError(
                            f"Multiple `enum` values "
                            f"found for `{key}`. "
                            f"Ensure only one "
                            f"is specified`"
                        )
                    blueprint_names.append(child_blueprint_name[0])
        return blueprint_names

    def _child_list_request(
        self, entity, kids, child_adapter, query_key="name", **kwargs
    ):
        """
        We lookup a blueprints kids using the "name" query key rather than
        the guid as default as the kids are stored as names on the API
        :param entity: Instance of Blueprint
        :type entity: ~entities.blueprint.Blueprint
        :param kids: A list of blueprint names
        :type kids: list
        :param child_adapter: The child adapter
        :type child_adapter: Instance of QalxBlueprint
        :param query_key: The query key
        :type query_key: str
        :return: The unpacked child blueprint entities
        """
        return super(QalxBlueprint, self)._child_list_request(
            entity=entity,
            kids=kids,
            child_adapter=child_adapter,
            query_key=query_key,
            **kwargs,
        )

    def _pack_kids_for_request(self, kwargs):
        """
        If the Blueprint is a nested blueprint, will pack the kids to be
        enums rather than the fully inflated kids schema that would have come
        from the Blueprint entity
        """
        if self._kids_properties(kwargs):
            for key, value in self._kids_properties(kwargs).items():
                if "name" in value:
                    kwargs["schema"]["properties"]["items"]["properties"][
                        key
                    ] = {"type": "string", "enum": [value["name"]]}
                else:
                    if value != {"type": "object"}:
                        # A name wasn't specified and the nested entity
                        # has been defined.  This can only happen if a user
                        # builds the schema manually.  We require the `name`
                        # field in order to build the `enum` list to enable
                        # packing/unpacking to work.
                        raise QalxInvalidBlueprintError(
                            f"{key} key must specify `name` key which should "
                            f"be the name of the specific child blueprint. "
                            f"This is required for packing/unpacking to work."
                        )
        return kwargs

    def _attempt_unpack(self, entity, **kwargs):
        """
        Have to override _attempt_unpack because the `self.kids` key is not
        actually where we need to get the children from.
        """
        if self._kids_properties(entity):
            unpacked_entities = self._get_child_entities(entity, **kwargs)
            self._unpacked_entities_to_valid_children(
                entity=entity, unpacked_entities=unpacked_entities
            )
        return entity

    def cache_kids(self, kwargs):
        """
        Override `cache_kids` because the `self.kids` key is not where
        we need to get the children from. Using deepcopy because schema is a
        mutable object(dict)
        """
        return deepcopy(kwargs["schema"])

    def save_kids_on_entity(self, entity, kids):
        """
        Override `save_kids_on_entity` because the `self.kids` key is
        not where the children should be saved.
        """
        entity["schema"] = kids

    def _unpacked_entities_to_valid_children(self, entity, unpacked_entities):
        """
        Iterates the enum values of the child blueprints and replaces them
        with the full item schema
        """
        kids_properties = self._kids_properties(entity)
        for key, value in kids_properties.items():
            for child_entity in unpacked_entities:
                if (
                    value.get("enum")
                    and value.get("enum")[0] == child_entity.name
                ):
                    kids_properties[key] = child_entity.schema
        return kids_properties
