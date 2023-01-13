"""
Factory adapter module. Contains the main class that provides factory related
interaction with the qalx API: QalxFactory
"""

import json

from ...factories.mixins import FactoryValidateMixin
from ..entities.factory import Factory
from .adapter import QalxFileAdapter
from ..errors import QalxFactoryValidationError, QalxAPIResponseError


class QalxFactory(QalxFileAdapter):
    """
    Provides an interface for accessing the API for
    :class:`~pyqalx.core.entities.factory.Factory` entities
    """

    _entity_class = Factory
    _file_key = "plan"
    # The `status` key should be saved for this adapter
    _keys_to_exclude = {"guid", "info"}

    def validate(self, plan_path):
        """
        Reads a .yaml file that contains the definition of the factory plan and
        then runs the factory validation endpoint in the API

        :param plan_path:   A local path to the .yaml file that contains the
                            factory plan definition
        :type plan_path: str

        :raises QalxFactoryValidationError:     If the .yaml file does not
                                                exist, if there are any errors
                                                parsing the yaml file to a
                                                dict, or if the yaml plan
                                                structure is invalid
        """
        plan = FactoryValidateMixin.read_plan(plan_path)
        plan_json = json.dumps(FactoryValidateMixin.load_plan(plan))
        try:
            self._process_api_request(
                "post", "factory/validate", plan=plan_json
            )
        except QalxAPIResponseError as exc:
            raise QalxFactoryValidationError(
                f"There was an error validating the factory plan:\n\n{exc}"
            )

    def add(
        self, name, source=None, file_name="", meta=None, upload=True, **kwargs
    ):
        """
        Adds a `Factory` instance

        :param name:        The name of the factory
        :type  name:        str
        :param source:  file path to the factory plan or instance of
                            StringIO or BytesIO
                            (https://docs.python.org/3/library/io.html)
        :type  source:  str or `io` object
        :param file_name:   Name for the factory plan input file. Optional if a
                            file path is given for source parameter.
                            Required if an `io` object
        :type  file_name:   str
        :param meta:        A dictionary of metadata to store
        :type  meta:        dict
        :param upload: Whether the file should be automatically uploaded or not
        :type upload: bool

        :return: A newly created `Factory` instance
        """

        return super(QalxFactory, self).add(
            name=name,
            source=source,
            file_name=file_name,
            meta=meta,
            file_key=self.entity_class._file_key,
            as_file=False,
            upload=upload,
            encrypt=False,
            **kwargs,
        )

    def save(
        self, entity, source=None, file_name="", upload=True, *args, **kwargs
    ):
        """
        Saves an updated existing `Factory` instance.

        :param entity: The entity that we are saving
        :type  entity: An instance of `Factory`
        :param source:  file path to the factory plan or instance of
                            StringIO or BytesIO
                            (https://docs.python.org/3/library/io.html)
        :type  source:  str or `io` object
        :param file_name:   Name for the factory plan input file. Optional if a
                            file path is given for source parameter.
                            Required if an `io` object
        :type  file_name:   str
        :param upload: Whether the file should be automatically uploaded or not
        :type upload: bool
        :return: An updated `Factory` instance
        """
        return super(QalxFactory, self).save(
            entity=entity,
            source=source,
            file_name=file_name,
            as_file=False,
            upload=upload,
            encrypt=False,
            *args,
            **kwargs,
        )

    def get(self, guid, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxFactory, self).get(guid, *args, **kwargs)

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
        # extended to create better autodocs
        return super(QalxFactory, self).find(
            query=query,
            sort=sort,
            skip=skip,
            limit=limit,
            many=many,
            include_session_tags=include_session_tags,
            **kwargs,
        )

    def find_one(self, query, **kwargs):
        # extended to create better autodocs
        return super(QalxFactory, self).find_one(query=query, **kwargs)

    def reload(self, entity, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxFactory, self).reload(entity=entity, **kwargs)

    def aggregate(self, aggregate, **kwargs):
        # extended to create better autodocs
        return super(QalxFactory, self).aggregate(aggregate=aggregate, **kwargs)
