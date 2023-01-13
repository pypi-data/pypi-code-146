import concurrent
import copy
import io
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from http import HTTPStatus

from types import MethodType

import requests
from bson_extra import bson_extra

from pyqalx.config import UserConfig, BotConfig
from pyqalx.core.entities import QalxListEntity
from pyqalx.core.entities.entity import AggregationResult
from pyqalx.core.enums import ValidStates
from pyqalx.core.errors import (
    QalxError,
    QalxNoGUIDError,
    QalxAPIResponseError,
    QalxMultipleEntityReturned,
    QalxEntityNotFound,
    QalxConfigError,
    QalxInvalidSession,
    QalxFileError,
)


class QalxAdapter(object):
    """
    The base class for a QalxAdapter. An adapter is the interface for the
    entity to the rest api.  This allows us to have a consistent interface
    across all entity types.
    """

    # Certain keys shouldn't be attemped to be saved
    _keys_to_exclude = {"info", "guid", "status"}

    def __init__(self, session, *args, **kwargs):
        QalxSession = __import__("pyqalx").QalxSession
        if not isinstance(session, QalxSession):
            raise QalxInvalidSession(
                f"`qalx_session` should be an instance of"
                f" `{QalxSession}`.  "
                f"Got `{type(session)}`"
            )
        self.session = session
        super(QalxAdapter, self).__init__(*args, **kwargs)

    def __getattribute__(self, item):
        """
        Certain methods can only be called by sessions with a UserConfig or a
        BotConfig.  The API will return a 403 Permission Denied
        but this method handles showing the user a more useful error message
        """
        attr = super(QalxAdapter, self).__getattribute__(item)
        if callable(attr) and isinstance(attr, MethodType):
            # This is a method on `QalxBot`.  Check the config
            # is correct for the method we are calling
            def _msg(expected_class, actual_class):
                return (
                    f"Method `{item}` on `{self.__class__}` "
                    f"must be called via a session with a `{expected_class}`"
                    f"instance.  Got `{actual_class}`"
                )

            is_user_config = isinstance(self.session.config, UserConfig)
            is_bot_config = isinstance(self.session.config, BotConfig)

            if (
                item in getattr(self, "_user_only_methods", [])
                and not is_user_config
            ):
                raise QalxConfigError(_msg(UserConfig, BotConfig))
            if (
                item in getattr(self, "_bot_only_methods", [])
                and not is_bot_config
            ):
                raise QalxConfigError(_msg(BotConfig, UserConfig))
        return attr

    @property
    def entity_class(self):
        return self.session._registry["entities"][
            self._entity_class.entity_type
        ]

    @staticmethod
    def raise_api_response_error(data_dict):
        message = (
            "API request error, message:\n\n-vvv-\n\n"
            + "\n".join([f"{k}: {v}" for k, v in data_dict.items()])
            + "\n\n-^^^-"
        )
        raise QalxAPIResponseError(message)

    def _process_api_request(self, method, *args, **kwargs):
        """calls to transport layer

        :param method: http method required
        :param args: args to be passed to endpoint method
        :param kwargs: kwargs to be passed to endpoint method
        :returns: `dict` containing API resource data
        """
        headers = kwargs.pop("headers", {})

        try:
            bson_extra.dumps(kwargs)
        except (TypeError, ValueError, OverflowError):
            raise QalxError(
                "One of the keyword arguments is not JSON serializable"
            )

        try:
            endpoint = getattr(self.session.rest_api, method.lower())
            self.session.log.debug(f"{self.__class__.__name__}#{method}")
        except AttributeError:
            raise QalxError(f"`{method}` not recognised.")

        success, data = endpoint(*args, data=kwargs, headers=headers)

        if success:
            return data
        self.raise_api_response_error(data)

    def detail_endpoint(self, guid, *args, **kwargs):
        """
        The endpoint for interfacing with a single
        instance of `self.entity_class`
        """
        return f"{self.entity_class.entity_type}/{guid}"

    def list_endpoint(self, *args, **kwargs):
        """
        The endpoint for interfacing with multiple instances of
        `self.entity_class`
        """
        return self.entity_class.entity_type

    @classmethod
    def get_keys_to_save(cls, entity):
        """
        When saving an entity not every key should be saved
        """
        # info & guid are both read only
        # status should only be saved via `update_status` (if available)
        return {k: entity[k] for k in entity if k not in cls._keys_to_exclude}

    @staticmethod
    def _validate(**kwargs):
        """
        Hook for specifying adapter level validation.  Returns kwargs
        so that if we need to mutate any of the kwargs (i.e. ensuring that
        a key not provided by the user has a specific value) then we can
        """
        if kwargs.get("meta", None) is None:
            # meta is optional but must always be sent through as a dict
            kwargs["meta"] = {}
        if not isinstance(kwargs["meta"], dict):
            raise QalxError("`meta` kwarg must be a `dict`")
        return kwargs

    def _process_api_response(
        self, response, entity_class=None, *args, **kwargs
    ):
        """
        Hook for processing the response from the API.  By default
        returns an instance of self.entity_class.  kwargs can be provided
        which will be passed through to entity_class
        :param response: The response dict from the API
        :param entity_class:The entity class that should be instantiated.
        :return: An instance of `entity_class`
        """
        if entity_class is None:
            entity_class = self.entity_class
        return entity_class(
            response, _region=self.session.config.get("REGION"), **kwargs
        )

    def _add_tags(self, entity):
        """
        Helper for applying tags to the entity before adding.  The tags
        need to be added to the individual entity, but can only be applied
        from the session - i.e. the user shouldn't add them manually.
        :param entity: The entity data that is being added
        :return: The entity data.
        """
        if "tags" in entity.keys():
            # Ensures users don't get confused if they try to do
            # `.add(tags={'my': 'tag'}).  We cannot do this in `_validate`
            # because we only want this validation to occur on `add`
            raise QalxError(
                "Tags can only be added to entities via the "
                "session.  Do `session.tags.add(name=<tag_name>, "
                "value=<tag value>)` rather than passing a `tags` "
                "argument to `add`"
            )
        entity["tags"] = self.session.tags
        return entity

    def add(self, **kwargs):
        """
        Adds a new instance of `self.entity_class` or a parent class that is
        provided in `kwargs`.  Provide valid `kwargs` for the object you are
        trying to create

        :return:    An instance of `self.entity_class` or an instance of
                    `parent_class` if this is provided in `kwargs`
        """
        # If parent_class is provided, we return an instance of the parent class
        parent_class = kwargs.pop("parent_class", None)
        if kwargs.pop("_is_validated", False) is False:
            # We may have already validated at this point if we are
            # doing a bulk insert.  This kwarg should be set on the adapter
            # that has done the validation
            kwargs = self._validate(**kwargs)

        self._add_tags(kwargs)

        response = self._process_api_request(
            "post", self.list_endpoint(**kwargs), **kwargs
        )
        if parent_class:
            return self._process_api_response(
                entity_class=parent_class,
                child=self.entity_class,
                response=response,
            )
        return self._process_api_response(response)

    def get(self, guid, *args, **kwargs):
        """
        Gets an instance of `self.entity_class` by the given guid.

        :param guid: The guid of the entity to get
        :return: An instance of `self.entity_class`
        """
        endpoint = self.detail_endpoint(guid=guid, *args, **kwargs)
        resp = self._process_api_request("get", endpoint, *args, **kwargs)
        self.session.log.debug(
            f"get `{self.entity_class.entity_type}` with "
            f"guid `{guid}` with `/{endpoint}`"
        )
        return self._process_api_response(resp)

    def find_one(self, query, **kwargs):
        """
        Method for returning a unique entity. Will return the entity that
        matches the query

        :param query: The mongoDB query
        :type query: dict
        :return: an instance of `self.entity_class`
        :raises QalxMultipleEntityReturned:
        :raises QalxEntityNotFound:
        """
        return self.find(many=False, limit=2, query=query, **kwargs)

    def find(
        self,
        query=None,
        sort=None,
        skip=0,
        limit=25,
        many=True,
        include_session_tags=True,
        **kwargs,
    ):
        """
        Method for listing entities.

        :param query: The optional Mongo query to find entities
        :param sort: The keys to sort by
        :param skip: The number of results to skip (offset) by
        :param limit: How many results should the response be limited to
        :param many: Should many entities be returned or just a single one
        :param include_session_tags:    Should the tags for the session be
                                        included in the query. Default is True
        :param kwargs: kwargs to query by
        :return:
        """
        list_endpoint = self.list_endpoint(**kwargs)

        self.session.log.debug(
            f"find `{self.entity_class.entity_type}` with `/{list_endpoint}`"
        )
        if include_session_tags and self.session.tags:
            # There are tags on this session, modify the query given (if
            # necessary) to include a filter that applies those tags.
            empty_and = {"$and": []}
            if query is None:
                query = empty_and
            elif "$and" not in query:
                query.update(empty_and)
            query["$and"] += self.session.tags._query()

        if query:
            # We need to dump the query to JSON as there could be
            # complex lookups which would get lost when the request is made
            try:
                query = bson_extra.dumps(query)
            except (TypeError, ValueError, OverflowError):
                raise QalxError(
                    "One of the keyword arguments is not JSON serializable"
                )

        resp = self._process_api_request(
            "get",
            list_endpoint,
            sort=sort,
            skip=skip,
            limit=limit,
            query=query,
            **kwargs,
        )
        entities = self._process_api_response(
            resp, entity_class=QalxListEntity, child=self.entity_class
        )

        if many is False:

            # We are expecting only a single entity.
            entities = entities.data
            if len(entities) > 1:
                entities_str = "\n".join([str(q) for q in entities])
                raise QalxMultipleEntityReturned(
                    "Expected one but got "
                    "{}:\n{}".format(len(entities), entities_str)
                )
            elif entities:
                return entities[0]
            else:
                raise QalxEntityNotFound(
                    self.entity_class.entity_type + " not found."
                )
        return entities

    def aggregate(self, aggregate, **kwargs):
        """
        Method for performing an aggregation on data.
        See https://docs.mongodb.com/manual/core/aggregation-pipeline/.  If
        a subset of the data is required then provide the query within the
        aggregation pipeline

        :param aggregate: The aggregation pipeline
        :type aggregate: list
        :return: :class:`~pyqalx.core.entities.entity.AggregationResult`
        """
        try:
            aggregate = bson_extra.dumps(aggregate)
        except (TypeError, ValueError, OverflowError):
            raise QalxError(
                "One of the keyword arguments is not JSON serializable"
            )

        list_endpoint = self.list_endpoint(**kwargs)
        list_endpoint += "/aggregate"
        resp = self._process_api_request(
            "post", list_endpoint, aggregate=aggregate, **kwargs
        )
        return self._process_api_response(
            resp, entity_class=AggregationResult, child=self.entity_class
        )

    def reload(self, entity, *args, **kwargs):
        """
        Reloads the current entity from the API

        :param entity: An instance of `self.entity_class`
        :return: A refreshed instance of `self.entity_class`
        """
        return self.get(entity.guid, *args, **kwargs)

    def save(self, entity, *args, **kwargs):
        """
        Saves `entity` to the database.

        :return: The updated instance of `entity`
        """
        if not entity.get("guid"):
            raise QalxNoGUIDError("No guid.")
        # kwargs is also passed through as it could contain data required
        # for validation by any subclasses (blueprints/files etc)
        entity = self._validate(**entity, **kwargs)
        guid = entity["guid"]

        # If there are tags on the session then use them. Otherwise, fallback
        # to using the tags on the entity. This prevents a session without
        # tags from accidentally removing tags previously set on an entity.
        # If there are no tags on the entity (because they weren't returned via
        # `fields` then we don't update the tags - unless tags have been
        # specified on the session)
        tags_to_save = self.session.tags or entity.get("tags", None)
        if tags_to_save:
            entity["tags"] = tags_to_save

        endpoint = self.detail_endpoint(guid=guid, *args, **kwargs)
        keys_to_save = self.get_keys_to_save(entity=entity)
        self.session.log.debug(
            f"save `{self.entity_class.entity_type}` with "
            f"guid `{guid}` with `/{endpoint}`"
        )

        resp = self._process_api_request("patch", endpoint, **keys_to_save)
        return self._process_api_response(resp)

    def archive(self, entity, *args, **kwargs):
        """
        Archives `entity`

        :param entity: An instance of `self.entity_class`
        :return: The archived instance of `entity`
        """
        guid = entity["guid"]
        detail_endpoint = self.detail_endpoint(guid=guid, *args, **kwargs)
        endpoint = f"{detail_endpoint}/archive"
        self.session.log.debug(
            f"archive `{self.entity_class.entity_type}` with "
            f"guid `{guid}` with `/{endpoint}`"
        )

        resp = self._process_api_request("patch", endpoint)
        return self._process_api_response(resp)

    def delete(self, entity, *args, **kwargs):
        """
        Deletes the given entity from the API

        :param entity: An instance of QalxEntity
        """
        detail_endpoint = self.detail_endpoint(
            guid=entity["guid"], *args, **kwargs
        )
        return self._process_api_request("delete", detail_endpoint)


class QalxUnpackableAdapter(QalxAdapter):
    """
    A qalx adapter for unpackable entities (Set, Group)
    """

    @property
    def kids(self):
        """
        The key that the child entities live in
        """
        return self.child_entity_class.pluralise()

    @staticmethod
    def _child_list_response(child_adapter, query, **kwargs):
        return child_adapter.find(
            query=query, include_session_tags=False, **kwargs
        )

    def _child_list_request(
        self, entity, kids, child_adapter, query_key="guid", child_fields=None
    ):
        """
        Builds the list request for getting any unpackable children. Handles
        chunking of the query and also pagination of the response
        :param entity: The entity that has the children
        :param kids: The details of the kids entities we want to lookup
        :param child_adapter: The child adapter to use
        :param query_key: The query key (defaults to `guid`)
        :return: A list of unpacked child_adapter.entity_class entities
        """
        unpacked_entities = []
        page_size = 100
        _futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for _page in entity._chunks(kids, chunk_size=page_size):
                # Chunk to avoid hitting maximum request size
                values = list(filter(None, _page))
                query = {query_key: {"$in": values}}
                _futures.append(
                    executor.submit(
                        self._child_list_response,
                        child_adapter=child_adapter,
                        query=query,
                        fields=child_fields,
                        limit=page_size,
                    )
                )
            for future in concurrent.futures.as_completed(_futures):
                try:
                    unpacked_entities += future.result().data
                except QalxAPIResponseError as exc:
                    self.raise_api_response_error(exc)
        return unpacked_entities

    def _kids_for_lookup(self, entity):
        """
        For the given entity, will get the child keys so that an API request
        can be made to obtain them
        :param entity: The entity that has child
        :return: The child keys to send to the API, as a list of values
        """
        return list(entity[self.kids].values())

    def _get_child_entities(self, entity, **kwargs):
        """
        Gets all the child entities for the given entity.  Handles chunking
        the children up into blocks to guard against sending a request that is
        too large.  Also handles the paginated result coming back from the
        `list` endpoint.  Does a `list` lookup for self.child_entity_class
        filtering on `guid` of the children to reduce the amount of queries

        :param entity: The entity to be unpacked
        :return: The child entities as a list
        """
        kids = self._kids_for_lookup(entity)

        child_adapter = getattr(
            self.session, self.child_entity_class.entity_type
        )
        unpacked_entities = self._child_list_request(
            entity=entity, kids=kids, child_adapter=child_adapter, **kwargs
        )
        return unpacked_entities

    def _unpacked_entities_to_valid_children(
        self, entity, unpacked_entities, **kwargs
    ):
        """
        Converts a list of `unpacked_entities` into valid child entities
        for the given entity.  Handles getting any nested children (i.e. items
        on sets when we are unpacking a group).  A two stage process to keep
        queries down in the instance where the same set is on a group multiple
        times

        :param entity: The entity that has kids that should be unpacked
        :param unpacked_entities: The unpacked child entities that need to be
                                  stitched into the entity
        :return: The unpacked entities in the correct format to be assigned to
                 `entity[self.kids]`
        """
        to_return = {}
        fully_unpacked_entities = []
        for child_entity in unpacked_entities:
            # iterate through all the unpacked_entities, getting any further
            # nested children as required
            child_entity_adapter = getattr(
                self.session, child_entity.entity_type
            )
            if hasattr(child_entity_adapter, "child_entity_class"):
                # The child entity has a child adapter of it's own.
                # Attempt unpack. This can occur if we are unpacking
                # a Group as we may need to unpack the Sets on the
                # Group
                child_entity_with_nested = child_entity_adapter._attempt_unpack(
                    child_entity, **kwargs
                )
                # At this point this given `child_entity` will have all
                # the nested children within fully unpacked.
                fully_unpacked_entities.append(child_entity_with_nested)
            else:
                # This is the bottom of the unpacking hierarchy.
                fully_unpacked_entities.append(child_entity)

        for key, child_guid in entity[self.kids].items():
            # Iterate through the key/values on the children of this entity
            # and update the appropriate key from the fully_unpacked_entities.
            for child_entity in fully_unpacked_entities:
                if child_guid == child_entity.guid:
                    to_return[key] = child_entity
        return to_return

    def _attempt_unpack(self, entity, **kwargs):
        """
        For the given entity will attempt
        to unpack the child_entity data that it contains

        :entity: The entity to be unpack
        :return: The entity instance with the child_entity objects unpacked
        """

        if self.kids in entity:
            # `self.kid` might not be there if we have specified a subset
            # of fields
            unpacked_entities = self._get_child_entities(entity, **kwargs)
            entity[self.kids] = self._unpacked_entities_to_valid_children(
                entity=entity, unpacked_entities=unpacked_entities, **kwargs
            )
        return entity

    def _pack_kids_for_request(self, kwargs):
        """
        Packs the kids into a format that they need to be in
        for sending to the API
        :param kwargs: The kwargs sent to the `add` method
        :return: kwargs with packed kids
        """
        kids = {key: str(kid.guid) for key, kid in kwargs[self.kids].items()}
        kwargs[self.kids] = kids
        return kwargs

    def get_keys_to_save(self, entity):
        """
        Unpackable entities will have unpacked data stored on them that have
        to be submitted as packed data
        """
        keys_to_save = super(QalxUnpackableAdapter, self).get_keys_to_save(
            entity=entity
        )
        if self.kids in keys_to_save.keys():
            keys_to_save[self.kids] = self.get_kids_keys_to_save(
                keys_to_save[self.kids]
            )
        return keys_to_save

    @staticmethod
    def get_kids_keys_to_save(kids_to_save):
        """
        Gets the keys of the kids that we want to save.  Ensures that if the
        keys are in an packed state we don't attempt to unpack them.
        :param kids_to_save: A dict of the kids we want to save
        :type kids_to_save: dict
        :return: A dict of {key:guid} of the kids we want to save
        """
        return {
            k: str(i["guid"]) if isinstance(i, dict) else i
            for k, i in kids_to_save.items()
        }

    @staticmethod
    def cache_original_kids(kids):
        """
        When saving the API only wants to know about the guids of the kids so
        we need to cache the originals
        until after the save
        :param kids: The kids on this entity
        :type kids: dict
        :return: A dictionary of the kids
        """
        return {k: v for k, v in kids.items()}

    def get(self, guid, child_fields=None, unpack=True, *args, **kwargs):
        """
        Gets the entity for the given `guid` and unpacks it if specified.
        Provide `child_fields` to restrict the fields returned on unpacked
        children

        :param guid: The `guid` of the entity to get
        :type guid: str
        :param child_fields: A list of fields that should be returned from
                             child entities
        :type child_fields: list
        :param unpack: Should the child entities be unpacked. Defaults to True
        :type unpack: bool
        :return: An unpacked entity
        """
        entity = super(QalxUnpackableAdapter, self).get(
            guid=guid, *args, **kwargs
        )
        if unpack is True:
            entity = self._attempt_unpack(entity, child_fields=child_fields)
        return entity

    def reload(self, entity, unpack=True, *args, **kwargs):
        entity = super(QalxUnpackableAdapter, self).reload(
            entity, unpack=unpack, *args, **kwargs
        )
        return entity

    def find_one(self, query, unpack=True, **kwargs):
        entity = super(QalxUnpackableAdapter, self).find_one(
            query, unpack=unpack, **kwargs
        )
        return entity

    def find(self, many=True, child_fields=None, *args, **kwargs):
        """
        Return multiple packed entities from the API

        :param many: Are many results expected or just one?
        :type many: bool
        :param child_fields: A list of fields that should be returned from
                             child entities
        :type child_fields: list
        :return: A list of entities
        """
        entities = super(QalxUnpackableAdapter, self).find(
            many=many, *args, **kwargs
        )
        unpack = kwargs.get("unpack", True)
        if unpack is True and many is False:
            # Only unpack a list view if we have a single entity
            entities = self._attempt_unpack(entities, child_fields=child_fields)
        return entities

    def save(self, entity, *args, **kwargs):
        """
        When saving an unpacked entity the kids need to be packed. To save
        having to unpack them again just save the original kids and replace
        them with the packed values after saving

        :param entity: An instance of `self.entity_class`
        :return: An updated instance of `self.entity_class`
        """
        has_kids_key = self.kids in entity.keys()
        if has_kids_key:
            original_kids = self.cache_original_kids(entity[self.kids])

        entity = super(QalxUnpackableAdapter, self).save(
            entity=entity, *args, **kwargs
        )
        if has_kids_key:
            entity[self.kids] = original_kids
        else:
            entity = self._attempt_unpack(entity=entity)
        return entity

    def cache_kids(self, kwargs):
        """
        Gets the kids from the given kwargs

        :param kwargs:a dict with a `self.kids` key
        :type kwargs: dict
        :return:The value of the `self.kids` key or None
        """
        return kwargs.get(self.kids, None)

    def save_kids_on_entity(self, entity, kids):
        """
        Updates the given `self.kids` key on the entity with the given kids

        :param entity: An entity to be updated
        :param kids: The kids to update the entity with
        """
        entity[self.kids] = kids

    def add(self, **kwargs):
        # Need to validate before we pack the kids up
        kwargs = self._validate(**kwargs)
        # Cache the kids to reassign them to the newly created entity

        cached_kids = self.cache_kids(kwargs)
        kwargs = self._pack_kids_for_request(kwargs)
        entity = super(QalxUnpackableAdapter, self).add(
            _is_validated=True, **kwargs
        )
        if cached_kids is not None:
            self.save_kids_on_entity(entity, cached_kids)
        return entity


class QalxSignalAdapter(QalxAdapter):
    """
    Bots and Workers have signals that are used to determine when to stop
    processing data.  This class provides that shared functionality
    """

    def get_signal(self, entity, *args, **kwargs):
        """
        Gets just the `signal` field from the entity and then parses that
        into the `signal_class`
        """
        entity = self.get(guid=entity["guid"], fields="signal", *args, **kwargs)
        signal = self.signal_class(entity)
        return signal

    def terminate(self, entity, *args, **kwargs):
        """
        Updates the entity with a terminate signal
        """
        guid = entity["guid"]
        endpoint = self.detail_endpoint(guid=guid, **kwargs)
        self.session.log.debug(
            f"terminate `{self.entity_class.entity_type}` with guid `{guid}` with `/{endpoint}`"  # noqa
        )
        signal = self.signal_class._terminate_signal(*args, **kwargs)

        self._process_api_request("patch", endpoint, signal=signal)

    def _stop_or_resume(self, entity, stop, **kwargs):
        guid = entity["guid"]
        endpoint = self.detail_endpoint(guid=guid, **kwargs)
        signal = self.signal_class._stop_signal(stop)
        self.session.log.debug(
            f"signal `{signal}` on `{self.entity_class.entity_type}` with guid `{guid}` with `/{endpoint}`"  # noqa
        )
        self._process_api_request("patch", endpoint, signal=signal)

    def stop(self, entity, **kwargs):
        """
        Updates the entity with a stop signal
        """
        self._stop_or_resume(entity, stop=True, **kwargs)

    def resume(self, entity, **kwargs):
        """
        Updates the entity with a resume signal
        """
        self._stop_or_resume(entity, stop=False, **kwargs)


class QalxNamedEntityAdapter(QalxAdapter):
    """
    Certain QalxEntities have a `name` field that can be used to look up the
    entity.
    """

    def get_by_name(self, name, **kwargs):
        """gets a single entity by name

        :param name: name of entity
        :type name: str
        :param kwargs: Keyword arguments to be used in the find method
        :return: instance of `self.entity_class`
        :raises QalxMultipleEntityReturned:
        :raises QalxEntityNotFound:
        """
        return self.find_one(query={"name": name}, **kwargs)

    def get_or_create(self, name, meta=None, **kwargs):
        """
        Gets an entity by the given name or creates it if it doesn't exist

        :param name: The `name` that to use to get or create the entity by
        :type name: str
        :param meta: metadata about the entity
        :param kwargs: Other kwargs on the entity to use when creating
        :return: instance of `self.entity_class`
        """
        try:
            return self.get_by_name(name=name)
        except QalxEntityNotFound:
            return self.add(name=name, meta=meta, **kwargs)


class QalxValidateBlueprintAdapter(QalxAdapter):
    """
    Certain entity types can be validated against a preexisting Blueprint
    when they are created.
    """

    def _validate(self, blueprint_name=None, **kwargs):
        """
        When adding entities that inherit from this class, pyqalx will get
        the blueprint based on the `blueprint_name` and then ensure that
        the schema validates correctly against the data that you are creating
        the entity with

        :param blueprint_name: the name of the blueprint
        :type blueprint_name: str, None
        :param get_blueprint: Should this method retrieve the blueprint?
        :type get_blueprint: bool, False
        :return: A valid `self.entity_class` instance
        :raises: jsonschema.ValidationError
        """
        validated_data = super(QalxValidateBlueprintAdapter, self)._validate(
            **kwargs
        )
        if blueprint_name is not None:
            blueprint = validated_data.pop("blueprint", None)
            if blueprint is None:
                blueprint = self._get_blueprint(name=blueprint_name)
            blueprint.validate(validated_data)
        return validated_data

    def _get_blueprint(self, name):
        """
        Helper method for getting the blueprint instance
        :param name: The name of the blueprint
        :type name: str
        :return: A `~entities.blueprint.Blueprint` instance
        """
        blueprint = self.session.blueprint.get_by_name(name=name)
        return blueprint

    def add(self, blueprint_name, **kwargs):
        """
        When adding entities that inherit from this class, pyqalx will get
        the blueprint based on the `blueprint_name` and then ensure that
        the schema validates correctly against the data that you are creating
        the entity with

        :param blueprint_name: the name of the blueprint
        :type blueprint_name: str, None
        :return: A valid `self.entity_class` instance
        :raises: jsonschema.ValidationError
        """
        return super(QalxValidateBlueprintAdapter, self).add(
            blueprint_name=blueprint_name, **kwargs
        )

    def save(self, entity, blueprint_name=None, *args, **kwargs):
        """
        When saving entities that inherit from this class, pyqalx will get
        the blueprint based on the `blueprint_name` and then ensure that
        the schema validates correctly against the data that you are updating
        the entity with

        :param entity: The entity instance that you are saving
        :param blueprint_name: the name of the blueprint
        :type blueprint_name: str, None
        :return: A valid `self.entity_class` instance
        :raises: jsonschema.ValidationError
        """
        return super(QalxValidateBlueprintAdapter, self).save(
            entity, blueprint_name=blueprint_name, **kwargs
        )


class QalxFileAdapter(QalxAdapter):
    """
    Adapter that allows files to be uploaded to an entity
    """

    def __init__(self, *args, **kwargs):
        self._cached_data = None
        super().__init__(*args, **kwargs)

    def _process_api_response(self, *args, **kwargs):
        """
        Ensures that if there is a KEYFILE configured that this is present
        on all instances of `self.entity_class` to provide seamless decryption
        of files when downloading
        :param response: The response dict from the API
        :return: An instance of `self.entity_class`
        """
        kwargs["keyfile"] = self.session.config.get("KEYFILE")

        # Handle `data` dict manipulation if stored as file
        try:
            if args[0]["file"]["as_file"]:
                if self._cached_data:
                    # POST or PATCH/PUT
                    args[0]["data"] = self._cached_data
                else:
                    args[0]["data"] = self._retrieve_data_file(args[0]["file"])
        except KeyError:
            try:
                if args[0]["query"]:
                    # Handle response of LIST (find)
                    with ThreadPoolExecutor(max_workers=30) as pool:
                        futures = {
                            pool.submit(
                                self._retrieve_data_file, item["file"]
                            ): item["guid"]
                            for item in args[0]["data"]
                        }
                        for i, obj in enumerate(as_completed(futures)):
                            if obj.result():
                                # Will only assign to `data` if the item is a
                                # data file item
                                args[0]["data"][i]["data"] = obj.result()
            except (IndexError, KeyError):
                pass
        except IndexError:
            pass
        return super(QalxFileAdapter, self)._process_api_response(
            *args, **kwargs
        )

    @staticmethod
    def _retrieve_data_file(file_dict):
        if file_dict["as_file"]:
            # Only return content if the item is a data is stored as file
            url = file_dict["url"]
            file_retrieved = False
            sleep_time = 3
            while not file_retrieved:
                resp = requests.get(url)
                if resp.status_code == HTTPStatus.NOT_FOUND:
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                        sleep_time -= 1
                    else:
                        break
                else:
                    file_retrieved = True
                    break
            if file_retrieved:
                return bson_extra.loads(resp.content.decode())
            else:
                # TODO: Improve error message
                raise QalxFileError("Could not retrieve file data from S3.")

    def _validate(self, source, file_name, as_file=False, **kwargs):
        """
        Ensures that the `source` and/or `file_name` and `as_file are present
        and correct
        :param source: The path to the file or the file stream
        :param file_name: The name of the file
        :param as_file: Whether the `data` dict should be stored in S3 rather
        than in Mongo
        :return: kwargs
        """
        if source is not None:
            # Only validate the file if it's specified in the
            # implementing adapter
            file = {}
            if as_file:
                # Handle `data` saved as file
                if kwargs.get(self.entity_class._file_key):
                    # Saving an existing item
                    file = kwargs.get(self.entity_class._file_key)
                else:
                    # Adding a new item
                    file = {
                        "name": f"item_data_{uuid.uuid4()}.bson",
                        "as_file": True,
                    }
            else:
                is_filestream = self.session.rest_api.is_filestream(source)
                if is_filestream:
                    if not file_name:
                        raise QalxFileError(
                            "You must supply a file name when supplying"
                            " a file stream"
                        )
                    file["name"] = file_name
                else:
                    if os.path.isfile(source):
                        file_path = os.path.abspath(source)
                        filename = (
                            file_name
                            if file_name
                            else os.path.basename(file_path)
                        )
                        file["name"] = filename
                    else:
                        raise QalxFileError(f"Invalid file `{source}`")
            key_file = self.session.config.get("KEYFILE")
            if key_file is not None:
                # The user can suppress encryption on a per-case basis, by
                # passing `encrypt=False`
                if kwargs["encrypt"]:
                    file["keyfile"] = os.path.basename(key_file)
            kwargs[self.entity_class._file_key] = file
        return super(QalxFileAdapter, self)._validate(**kwargs)

    def add(
        self,
        source,
        file_name,
        data=None,
        as_file=False,
        upload=True,
        encrypt=True,
        **kwargs,
    ):
        """
        When a user creates an entity with a file pyqalx will upload the file
        automatically for you after the entity itself has been created.  Pass
        `upload=False` through to stop this from happening and upload the file
        yourself

        :param source: The input file path or stream
        :param file_name: The optional file name
        :param data: Data to store on this item
        :param as_file: Whether the `data` dict should be stored in S3 rather
        than in Mongo
        :param upload: Whether the file should be automatically uploaded or not
        :type upload: bool
        :param encrypt: Whether the file should be automatically encrypted if
         the KEYFILE is present
        :type encrypt: bool
        :param as_file: Whether the `data` dict should be stored in S3 rather
        than in Mongo
        :return: A valid entity
        """
        if data is None:
            data = {}
        source = self._handle_data_as_file(data, source, as_file)
        entity = super(QalxFileAdapter, self).add(
            data=data,
            source=source,
            file_name=file_name,
            encrypt=encrypt,
            as_file=as_file,
            **kwargs,
        )
        if upload and source is not None:
            entity = self._upload_file(entity=entity, source=source)
        return entity

    def save(
        self,
        entity,
        source,
        file_name,
        upload=True,
        encrypt=True,
        as_file=False,
        *args,
        **kwargs,
    ):  # noqa
        """
        Saves an entity - optionally updating any file data.

        :param entity: The entity that is being saved
        :param source: The input file path or stream
        :param file_name: The optional file name
        :type file_name: str
        :param upload: Whether the file should be automatically uploaded or not
        :type upload: bool
        :param encrypt: Whether the file should be automatically encrypted if
         the KEYFILE is present
        :type encrypt: bool
        :param as_file: Whether the `data` dict should be stored in S3 rather
        than in Mongo
        :return: A valid entity
        """
        # If item data is already saved as file, then keep it that way
        as_file = as_file or (
            entity.file.get("as_file") if entity.get("file") else False
        )
        source = self._handle_data_as_file(
            entity.get("data", {}), source, as_file
        )
        entity = super(QalxFileAdapter, self).save(
            entity=entity,
            source=source,
            file_name=file_name,
            encrypt=encrypt,
            as_file=as_file,
            **kwargs,
        )
        if source is not None:
            if upload:
                entity = self._upload_file(entity=entity, source=source)  # noqa
            else:
                # Entity is returned with the put_url so that the user can
                # upload the file manually
                return entity
        # Ensure "put_url" is removed even if we are not changing the file
        entity[self.entity_class._file_key].pop("put_url", None)
        return entity

    def _upload_file(self, entity, source):
        # Only upload if everything was OK with the item creation
        # and the user wants to upload the file automatically.

        s3_resp_ok, s3_data = self.session.rest_api._upload_to_s3(
            entity, source, self.entity_class._file_key
        )
        if s3_resp_ok is False:
            # The S3 upload failed, return the failed S3 response in place
            # of the response from the api.  Any implementing client will
            # have to handle tidying up any incorrect data.
            self.raise_api_response_error(s3_data)
        else:
            # Always pop the `put_url` off if it's a success
            entity[self.entity_class._file_key].pop("put_url")
        return entity

    def _handle_data_as_file(self, data, source, as_file):
        if as_file:
            # Need to raise error here if required
            if source is not None:
                raise QalxFileError(
                    "Cannot specify a file `source` and have `as_file` = True"
                    "together"
                )
            source = io.BytesIO()
            source.write(bson_extra.dumps(data).encode())
            source.seek(0)

            # 'Cache' the data dict in memory so that it can be returned to the
            # user without saving it to Mongo or having to retrieve it from S3
            self._cached_data = copy.deepcopy(data)
            data.clear()
        return source


class QalxUpdateStatusAdapter(QalxAdapter):
    def update_status(self, entity, status, **kwargs):
        """
        Updates the status of an entity

        :param entity: The entity that is being updated
        :param status: The status to update to
        :type status: str
        """
        guid = entity["guid"]
        endpoint = self.detail_endpoint(guid=guid, **kwargs)
        self.session.log.debug(
            f"update status `{self.entity_class.entity_type}` with guid `{guid}` with `/{endpoint}`"  # noqa
        )
        status_dict = {"message": status}
        self._process_api_request("patch", endpoint, status=status_dict)


class QalxUpdateStateAdapter(QalxAdapter):
    def update_state(self, entity, state: ValidStates, **kwargs):
        """
        Helper to update the state of a bot or worker. The API handles
        validation of the `state` arg.

        :param entity: The entity that is being updated
        :param state: The state to update to
        """
        endpoint = self.detail_endpoint(guid=entity["guid"], **kwargs)
        self._process_api_request("patch", endpoint, state=state.value)
