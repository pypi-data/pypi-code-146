from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attrs
from typeguard import typechecked

from tecton._internals import display
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton.declarative import base as declarative_base
from tecton.unified import common as unified_common
from tecton.unified import utils as unified_utils
from tecton.unified import validations_api
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_core import specs
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import entity_pb2 as entity__args_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.common import id_pb2
from tecton_proto.metadataservice import metadata_service_pb2


@attrs.define
class Entity(unified_common.BaseTectonObject, declarative_base.BaseEntity):
    """Tecton class for entities.

    Attributes:
        _spec:  A transformation spec, i.e. a dataclass representation of the Tecton object that is used in most functional
            use cases, e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e.
            applied objects fetched from the backend, are assumed valid.
        _args: A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
            and fetched from the Tecton backend.


    """

    _spec: Optional[specs.EntitySpec] = attrs.field(repr=False)
    _args: Optional[entity__args_pb2.EntityArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        join_keys: Optional[Union[str, List[str]]] = None,
    ):
        """
        Declare a new Entity.

        :param name: Unique name for the new entity.
        :param description: Short description of the new entity.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param join_keys: Names of columns that uniquely identify the entity in FeatureView's SQL statement
            for which features should be aggregated. Defaults to using ``name`` as the entity's join key.

        :raises TectonValidationError: if the input non-parameters are invalid.
        """
        from tecton.cli import common as cli_common

        if not join_keys:
            resolved_join_keys = [name]
        elif isinstance(join_keys, str):
            resolved_join_keys = [join_keys]
        else:
            resolved_join_keys = join_keys

        args = entity__args_pb2.EntityArgs(
            entity_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            join_keys=resolved_join_keys,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
        )
        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.entity_id)
        source_info = cli_common.get_fco_source_info()
        self.__attrs_init__(info=info, spec=None, args=args, source_info=source_info)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.EntitySpec) -> "Entity":
        """Create an Entity from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = unified_common.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None)
        return obj

    def _build_args(self) -> fco_args_pb2.FcoArgs:
        if self._args is None:
            raise errors.BUILD_ARGS_INTERNAL_ERROR

        return fco_args_pb2.FcoArgs(entity=self._args)

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    @property
    def join_keys(self) -> List[str]:
        """Join keys of the entity."""
        if self._spec is None:
            return list(self._args.join_keys)
        return list(self._spec.join_keys)

    @sdk_decorators.sdk_public_method
    def validate(self):
        """Validate a local Entity object.

        If this object has already been applied (i.e. not a locally defined object), validate() does not need to be called.
        """
        if self._is_valid:
            print("This object has already been validated.")
            return

        validation_passed = validations_api.run_backend_validation([self])
        if validation_passed:
            self._spec = specs.EntitySpec.from_args_proto(self._args)

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this Feature View."""
        request = metadata_service_pb2.GetEntitySummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetFeatureViewSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @property
    # TODO(jake): Remove this base data source property after deleting declarative code.
    def name(self) -> str:
        return self.info.name

    @property
    # TODO(jake): Remove this base data source property after deleting declarative code.
    def _id(self) -> id_pb2.Id:
        return self.info._id_proto
