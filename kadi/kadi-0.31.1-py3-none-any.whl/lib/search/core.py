# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from elasticsearch.exceptions import ConnectionError as ElasticsearchConnectionError
from elasticsearch.exceptions import ElasticsearchException
from elasticsearch.exceptions import NotFoundError
from elasticsearch.exceptions import RequestError
from elasticsearch_dsl import analyzer
from elasticsearch_dsl import Search
from elasticsearch_dsl import tokenizer
from flask import current_app

import kadi.lib.constants as const
from .elasticsearch import es
from kadi.ext.db import db
from kadi.lib.format import timestamp
from kadi.lib.utils import as_list
from kadi.lib.utils import get_class_by_name


class MappingMixin:
    """Mixin for custom search mappings."""

    class Analyzers:
        """Container to store common analyzers."""

        trigram = analyzer(
            "trigram_analyzer",
            tokenizer=tokenizer("trigram", "ngram", min_gram=3, max_gram=3),
            filter=["lowercase"],
        )

    @classmethod
    def get_attributes(cls):
        """Get a list of all attributes from a mapping class."""
        properties = cls._doc_type.mapping.properties
        return list(properties._params["properties"].keys())

    @classmethod
    def create_document(cls, obj):
        """Create a new document to be indexed in ElasticSearch

        :param obj: The object to be indexed.
        :return: The created document.
        """
        document = cls()
        document.meta.id = obj.id

        for attr in cls.get_attributes():
            if hasattr(obj, attr):
                setattr(document, attr, getattr(obj, attr))

        return document


class SearchableMixin:
    """Mixin for SQLALchemy models to add support for searching.

    The columns to index have to be specified in a mapping class, which has to be
    configured with its fully qualified name using ``Meta.search_mapping``.

    **Example:**

    .. code-block:: python3

        class Foo:
            class Meta:
                search_mapping = "kadi.modules.record.mapping.RecordMapping"

    After calling :meth:`register_search_listeners`, the search index will automatically
    get updated whenever an object is created or deleted or if any of the indexed
    columns (or the ``state`` column, if present) are updated using :func:`add_to_index`
    and :func:`remove_from_index`.
    """

    @classmethod
    def get_mapping_class(cls):
        """Convenience method to get the mapping class of a model."""
        return get_class_by_name(cls.Meta.search_mapping)

    @classmethod
    def search(cls, query=None, sort="_score", filter_ids=None, start=0, end=10):
        """Query the search index corresponding to this model.

        Uses :func:`search_index`, but returns the actual results instead of the raw
        search response.

        :param query: (optional) See :func:`search_index`.
        :param sort: (optional) See :func:`search_index`.
        :param filter_ids: (optional) See :func:`search_index`.
        :param start: (optional) See :func:`search_index`.
        :param end: (optional) See :func:`search_index`.
        :return: A tuple containing a list of the search results and the total amount of
            hits.
        :raises elasticsearch.exceptions.ConnectionError: If no connection could be
            established to Elasticsearch.
        """
        response = search_index(
            cls.__tablename__,
            query=query,
            sort=sort,
            filter_ids=filter_ids,
            start=start,
            end=end,
        )

        if response is None or not response.hits:
            return [], 0

        ids = [int(hit.meta.id) for hit in response.hits]
        when = []

        for index, id in enumerate(ids):
            when.append((id, index))

        results = (
            cls.query.filter(cls.id.in_(ids))
            .order_by(db.case(when, value=cls.id))
            .all()
        )

        return results, response.hits.total.value

    @classmethod
    def _before_flush_search(cls, session, flush_context, instances):
        if not hasattr(session, "_changes"):
            session._changes = {"add": set(), "remove": set()}

        for obj in session.new:
            if isinstance(obj, cls):
                session._changes["add"].add(obj)

        for obj in session.deleted:
            if isinstance(obj, cls):
                session._changes["remove"].add(obj)

        for obj in session.dirty:
            if isinstance(obj, cls) and session.is_modified(obj):
                if (
                    getattr(obj, "state", const.MODEL_STATE_ACTIVE)
                    == const.MODEL_STATE_ACTIVE
                ):
                    session._changes["add"].add(obj)
                    session._changes["remove"].discard(obj)
                else:
                    session._changes["remove"].add(obj)
                    session._changes["add"].discard(obj)

    @classmethod
    def _after_commit_search(cls, session):
        if hasattr(session, "_changes"):
            for obj in session._changes["add"]:
                add_to_index(obj)

            for obj in session._changes["remove"]:
                remove_from_index(obj)

            del session._changes

    @classmethod
    def _after_rollback_search(cls, session):
        if hasattr(session, "_changes"):
            del session._changes

    @classmethod
    def register_search_listeners(cls):
        """Register listeners to automatically update the search index.

        Uses SQLAlchemy's ``before_flush``, ``after_commit`` and ``after_rollback``
        events and propagates to all inheriting models.
        """
        db.event.listen(
            db.session, "before_flush", cls._before_flush_search, propagate=True
        )
        db.event.listen(
            db.session, "after_commit", cls._after_commit_search, propagate=True
        )
        db.event.listen(
            db.session, "after_rollback", cls._after_rollback_search, propagate=True
        )


def create_index(model, force=False):
    """Create a new search index if it does not exist yet.

    The name of the index will be in the form of ``"<tablename>_<timestamp>"``, where
    ``<tablename>`` depends on the given model. An alias ``<tablename>`` pointing to the
    actual index will also be created automatically if it does not exist yet.

    :param model: The model to create the index of. See also :class:`.SearchableMixin`.
    :param force: (optional) Flag indicating whether a new index should be created even
        if one already exists. Note that if an alias already exists it will not be
        updated automatically to point to the new index.
    :return: The name of the newly created or existing index or ``None`` if no new index
        could be created.
    """
    alias = model.__tablename__

    try:
        alias_exists = es.indices.exists(alias)

        if alias_exists and not force:
            return list(es.indices.get_alias(alias).keys())[0]

        index = f"{alias}_{timestamp(include_micro=True)}"

        mapping_class = model.get_mapping_class()
        mapping_class.init(using=es, index=index)

        if not alias_exists:
            es.indices.put_alias(index=index, name=alias)

        return index

    except ElasticsearchException as e:
        current_app.logger.exception(e)

    return None


def add_to_index(obj, index=None):
    """Add an object to its corresponding search index.

    :param obj: The object to index. See also :class:`.SearchableMixin`.
    :param index: (optional) The name of an index that should be used instead of the
        alias corresponding to the given object. See also :func:`create_index`.
    :return: ``True`` if the object was indexed successfully, ``False`` otherwise.
    """
    index = index if index is not None else obj.__tablename__

    try:
        # Check if the index actually exists, as it will be created dynamically
        # otherwise (even if dynamic mapping is turned off for newly added fields).
        if not es.indices.exists(index):
            return False

        document = obj.get_mapping_class().create_document(obj)
        document.save(using=es, index=index)
    except ElasticsearchConnectionError as e:
        if not current_app.config["ELASTICSEARCH_ENABLE_FALLBACK"]:
            current_app.logger.exception(e)

        return False
    except ElasticsearchException as e:
        current_app.logger.exception(e)
        return False

    return True


def remove_from_index(obj, index=None):
    """Remove an object from its corresponding search index.

    :param obj: The object to remove from the index. See also :class:`.SearchableMixin`.
    :param index: (optional) The name of an index that should be used instead of the
        alias corresponding to the given object. See also :func:`create_index`.
    :return: ``True`` if the object was removed successfully, ``False`` otherwise.
    """
    index = index if index is not None else obj.__tablename__
    mapping_class = obj.get_mapping_class()

    try:
        document = mapping_class.get(using=es, index=index, id=obj.id)
        document.delete(using=es)
    except NotFoundError:
        pass
    except ElasticsearchConnectionError as e:
        if not current_app.config["ELASTICSEARCH_ENABLE_FALLBACK"]:
            current_app.logger.exception(e)

        return False
    except ElasticsearchException as e:
        current_app.logger.exception(e)
        return False

    return True


def search_index(index, query=None, sort="_score", filter_ids=None, start=0, end=10):
    """Query a specific search index.

    :param index: The name of the search index.
    :param query: (optional) The search query in form of an Elasticsearch DSL query
        object.
    :param sort: (optional) The name of a field or a list of multiple fields to sort on.
    :param filter_ids: (optional) A list of IDs to restrict the search results to.
    :param start: (optional) The start index of the results to return.
    :param end: (optional) The end index of the results to return.
    :return: A response object as returned by the Elasticsearch DSL or ``None`` if the
        request returned an error. Note that only the metadata will be returned as part
        of the search results, without any field data.
    :raises elasticsearch.exceptions.ConnectionError: If no connection could be
        established to Elasticsearch.
    """
    search = Search(using=es, index=index)

    if query:
        search = search.query(query)

    if filter_ids is not None:
        search = search.filter("ids", values=filter_ids)

    search = (
        search.sort(*as_list(sort))
        .extra(track_total_hits=True)
        .source(False)[start:end]
    )

    try:
        response = search.execute()
    except RequestError:
        # Ignore malformed requests.
        return None
    except ElasticsearchConnectionError as e:
        if not current_app.config["ELASTICSEARCH_ENABLE_FALLBACK"]:
            current_app.logger.exception(e)

        raise
    except ElasticsearchException as e:
        current_app.logger.exception(e)
        return None

    return response
