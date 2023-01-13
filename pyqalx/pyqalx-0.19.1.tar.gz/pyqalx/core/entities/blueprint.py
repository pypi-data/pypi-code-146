from jsonschema import validate, validators

from pyqalx.core.entities import QalxEntity, Item, Set
from pyqalx.core.errors import QalxInvalidBlueprintError


class Blueprint(QalxEntity):
    """
    Provides an interface for creating blueprints.  Blueprints allow a user to
    create items or sets in a consistent fashion
    """

    entity_type = "blueprint"

    def _update_property(self, property_key, key, schema_value, required=False):
        self["properties"][property_key]["properties"][key] = self.__class__(
            schema_value
        )
        if (required is True) and (
            key not in self["properties"][property_key]["required"]
        ):
            self["properties"][property_key]["required"].append(key)
        self.check_schema()
        return self

    @classmethod
    def _base_blueprint(cls):
        return cls(
            {
                "type": "object",
                "properties": {
                    "meta": {"type": "object", "properties": {}, "required": []}
                },
            }
        )

    @classmethod
    def item(cls):
        """
        A blueprint that gives the default blueprint structure for an
        :class:`~pyqalx.core.entities.item.Item` entity
        """
        blueprint = cls._base_blueprint()
        blueprint.entity_type = Item.entity_type
        blueprint.properties.data = cls(
            {"type": "object", "properties": {}, "required": []}
        )
        blueprint.required = ["data"]
        return blueprint

    @classmethod
    def set(cls):
        """
        A blueprint that gives the default blueprint structure for an
        :class:`~pyqalx.core.entities.set.Set` entity
        """
        blueprint = cls._base_blueprint()
        blueprint.entity_type = Set.entity_type
        blueprint.properties["items"] = cls(
            {"type": "object", "properties": {}, "required": []}
        )
        blueprint.required = ["items"]
        return blueprint

    def check_schema(self, schema=None):
        """
        Checks that the given schema is structure correctly

        :param schema: The schema to validate.  Uses `self` if None
        :type schema: None or ~pyqalx.core.entities.blueprint.Blueprint

        :raises: jsonschema.SchemaError
        """
        if schema is None:
            schema = self
        validators._LATEST_VERSION.check_schema(schema=schema)

    def validate(self, entity):
        """
        Validate an entity against the blueprint schema locally.

        :param entity: A full schema for an entity that can have a Blueprint
        """
        validate(instance=entity, schema=self["schema"])

    def add_schema(self, schema_value):
        """
        Update the entire Blueprint schema at once.  Will
        completely overwrite all `properties` that are already on this Blueprint
        instance

        :param schema_value: A full schema for an entity that can have a
                             Blueprint
        :return: An updated instance of the blueprint
        """
        # addict will update keys when merging - not replace.  But
        # we want to replace the properties with the new schema
        # https://github.com/mewwts/addict#update
        self.properties = self.__class__(schema_value)
        self.check_schema()
        return self

    def add_data(self, key, schema_value, required=False):
        """
        Adds data to this item blueprint instance.

        :param key: The key in the data you want to add
        :type key: str
        :param schema_value: The schema value you want to add
        :type schema_value: str
        :param required: Is this key required?
        :type required: bool
        :return: An updated instance of the item blueprint
        """
        return self._update_property(
            property_key="data",
            key=key,
            schema_value=schema_value,
            required=required,
        )

    def add_meta(self, key, schema_value, required=False):
        """
        Adds meta to this item blueprint instance.

        :param key: The key in the meta you want to add
        :type key: str
        :param schema_value: The schema value you want to add
        :type schema_value: str
        :param required: Is this key required?
        :type required: bool
        :return: An updated instance of the item blueprint
        """
        return self._update_property(
            property_key="meta",
            key=key,
            schema_value=schema_value,
            required=required,
        )

    def add_item(self, key, item_blueprint=None, required=False):
        """
        Adds an item to this set blueprint instance.  If `item_blueprint` is
        provided then the set schema will always require that specific
        item blueprint for `key`.  If `item_blueprint` is not provided then
        the set blueprint will accept any data for `key` when being used

        :param key: The `key` of the item you want the blueprint to validate
        :type key: str
        :param item_blueprint: If provided will save the `name` from the
                               blueprint against the `key`.
                               This means that whenever the set is
                               created you must use the same blueprint.
        :type item_blueprint: str
        :param required: Is this key required?
        :type required: bool
        :return: An updated instance of the set blueprint
        """
        if item_blueprint is None:
            # the data stored against `key` can be anything when the set is
            # created
            schema_value = {"type": "object"}
        else:
            # the data stored against `key` must match the item blueprint
            if not isinstance(item_blueprint, self.__class__):
                raise QalxInvalidBlueprintError(
                    f"`{item_blueprint}` is not an"
                    f" instance of `{self.__class__}`"
                )
            # The "name" is required in order to pack the Blueprint
            # in QalxBlueprint for saving.
            item_blueprint.schema.name = item_blueprint["name"]
            schema_value = item_blueprint["schema"]
        return self._update_property(
            property_key="items",
            key=key,
            schema_value=schema_value,
            required=required,
        )
