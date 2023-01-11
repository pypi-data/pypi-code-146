from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.dropdown_dependency import DropdownDependency
from ..models.entity_schema_dependency import EntitySchemaDependency
from ..models.manifest_array_config_type import ManifestArrayConfigType
from ..models.manifest_scalar_config import ManifestScalarConfig
from ..models.resource_dependency import ResourceDependency
from ..models.schema_dependency import SchemaDependency
from ..models.workflow_task_schema_dependency import WorkflowTaskSchemaDependency
from ..types import UNSET, Unset

T = TypeVar("T", bound="ManifestArrayConfig")


@attr.s(auto_attribs=True, repr=False)
class ManifestArrayConfig:
    """  """

    _element_definition: List[
        Union[
            SchemaDependency,
            EntitySchemaDependency,
            WorkflowTaskSchemaDependency,
            DropdownDependency,
            ResourceDependency,
            ManifestScalarConfig,
            UnknownType,
        ]
    ]
    _type: ManifestArrayConfigType
    _name: str
    _default_element_name: Union[Unset, str] = UNSET
    _description: Union[Unset, None, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("element_definition={}".format(repr(self._element_definition)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("default_element_name={}".format(repr(self._default_element_name)))
        fields.append("description={}".format(repr(self._description)))
        return "ManifestArrayConfig({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        element_definition = []
        for element_definition_item_data in self._element_definition:
            if isinstance(element_definition_item_data, UnknownType):
                element_definition_item = element_definition_item_data.value
            elif isinstance(element_definition_item_data, SchemaDependency):
                element_definition_item = element_definition_item_data.to_dict()

            elif isinstance(element_definition_item_data, EntitySchemaDependency):
                element_definition_item = element_definition_item_data.to_dict()

            elif isinstance(element_definition_item_data, WorkflowTaskSchemaDependency):
                element_definition_item = element_definition_item_data.to_dict()

            elif isinstance(element_definition_item_data, DropdownDependency):
                element_definition_item = element_definition_item_data.to_dict()

            elif isinstance(element_definition_item_data, ResourceDependency):
                element_definition_item = element_definition_item_data.to_dict()

            else:
                element_definition_item = element_definition_item_data.to_dict()

            element_definition.append(element_definition_item)

        type = self._type.value

        name = self._name
        default_element_name = self._default_element_name
        description = self._description

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if element_definition is not UNSET:
            field_dict["elementDefinition"] = element_definition
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name
        if default_element_name is not UNSET:
            field_dict["defaultElementName"] = default_element_name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_element_definition() -> List[
            Union[
                SchemaDependency,
                EntitySchemaDependency,
                WorkflowTaskSchemaDependency,
                DropdownDependency,
                ResourceDependency,
                ManifestScalarConfig,
                UnknownType,
            ]
        ]:
            element_definition = []
            _element_definition = d.pop("elementDefinition")
            for element_definition_item_data in _element_definition:

                def _parse_element_definition_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    SchemaDependency,
                    EntitySchemaDependency,
                    WorkflowTaskSchemaDependency,
                    DropdownDependency,
                    ResourceDependency,
                    ManifestScalarConfig,
                    UnknownType,
                ]:
                    element_definition_item: Union[
                        SchemaDependency,
                        EntitySchemaDependency,
                        WorkflowTaskSchemaDependency,
                        DropdownDependency,
                        ResourceDependency,
                        ManifestScalarConfig,
                        UnknownType,
                    ]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        element_definition_item = SchemaDependency.from_dict(data, strict=True)

                        return element_definition_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        element_definition_item = EntitySchemaDependency.from_dict(data, strict=True)

                        return element_definition_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        element_definition_item = WorkflowTaskSchemaDependency.from_dict(data, strict=True)

                        return element_definition_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        element_definition_item = DropdownDependency.from_dict(data, strict=True)

                        return element_definition_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        element_definition_item = ResourceDependency.from_dict(data, strict=True)

                        return element_definition_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        element_definition_item = ManifestScalarConfig.from_dict(data, strict=True)

                        return element_definition_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                element_definition_item = _parse_element_definition_item(element_definition_item_data)

                element_definition.append(element_definition_item)

            return element_definition

        try:
            element_definition = get_element_definition()
        except KeyError:
            if strict:
                raise
            element_definition = cast(
                List[
                    Union[
                        SchemaDependency,
                        EntitySchemaDependency,
                        WorkflowTaskSchemaDependency,
                        DropdownDependency,
                        ResourceDependency,
                        ManifestScalarConfig,
                        UnknownType,
                    ]
                ],
                UNSET,
            )

        def get_type() -> ManifestArrayConfigType:
            _type = d.pop("type")
            try:
                type = ManifestArrayConfigType(_type)
            except ValueError:
                type = ManifestArrayConfigType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(ManifestArrayConfigType, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_default_element_name() -> Union[Unset, str]:
            default_element_name = d.pop("defaultElementName")
            return default_element_name

        try:
            default_element_name = get_default_element_name()
        except KeyError:
            if strict:
                raise
            default_element_name = cast(Union[Unset, str], UNSET)

        def get_description() -> Union[Unset, None, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, None, str], UNSET)

        manifest_array_config = cls(
            element_definition=element_definition,
            type=type,
            name=name,
            default_element_name=default_element_name,
            description=description,
        )

        return manifest_array_config

    @property
    def element_definition(
        self,
    ) -> List[
        Union[
            SchemaDependency,
            EntitySchemaDependency,
            WorkflowTaskSchemaDependency,
            DropdownDependency,
            ResourceDependency,
            ManifestScalarConfig,
            UnknownType,
        ]
    ]:
        if isinstance(self._element_definition, Unset):
            raise NotPresentError(self, "element_definition")
        return self._element_definition

    @element_definition.setter
    def element_definition(
        self,
        value: List[
            Union[
                SchemaDependency,
                EntitySchemaDependency,
                WorkflowTaskSchemaDependency,
                DropdownDependency,
                ResourceDependency,
                ManifestScalarConfig,
                UnknownType,
            ]
        ],
    ) -> None:
        self._element_definition = value

    @property
    def type(self) -> ManifestArrayConfigType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: ManifestArrayConfigType) -> None:
        self._type = value

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def default_element_name(self) -> str:
        if isinstance(self._default_element_name, Unset):
            raise NotPresentError(self, "default_element_name")
        return self._default_element_name

    @default_element_name.setter
    def default_element_name(self, value: str) -> None:
        self._default_element_name = value

    @default_element_name.deleter
    def default_element_name(self) -> None:
        self._default_element_name = UNSET

    @property
    def description(self) -> Optional[str]:
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET
