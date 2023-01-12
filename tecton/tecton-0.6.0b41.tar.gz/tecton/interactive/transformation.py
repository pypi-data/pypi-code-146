from typing import Optional
from typing import Union

import pandas as pd
import pyspark

from tecton import conf
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton._internals.sdk_decorators import sdk_public_method
from tecton.fco import Fco
from tecton.interactive import spark_api
from tecton.interactive.data_frame import TectonDataFrame
from tecton.unified.transformation import Transformation as UnifiedTransformation
from tecton_core import specs
from tecton_core.fco_container import FcoContainer
from tecton_core.logger import get_logger
from tecton_core.materialization_context import BaseMaterializationContext
from tecton_proto.args.transformation_pb2 import TransformationMode
from tecton_proto.data.transformation_pb2 import Transformation as TransformationProto
from tecton_proto.metadataservice.metadata_service_pb2 import GetTransformationRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetTransformationSummaryRequest

logger = get_logger("Transformation")


class Transformation(Fco):
    """
    Transformation Class.

    A Transformation is a Tecton Object that contains logic for creating a feature.

    To get a Transformation instance, call :py:func:`tecton.get_transformation`.
    """

    _transformation_proto: TransformationProto
    _fco_container: FcoContainer
    _transformation_spec: specs.TransformationSpec

    def __init__(self):
        """Do not call this directly. Use :py:func:`tecton.get_transformation`"""

    @classmethod
    def _fco_type_name_singular_snake_case(cls) -> str:
        return "transformation"

    @classmethod
    def _fco_type_name_plural_snake_case(cls) -> str:
        return "transformations"

    @property
    def _fco_metadata(self):
        return self._transformation_proto.fco_metadata

    @property
    def transformer(self):
        """
        Returns the raw transformation function encapsulated by this Transformation.
        """
        return self._transformation_spec.user_function

    @classmethod
    def _from_proto(cls, transformation: TransformationProto, fco_container: FcoContainer):
        """
        Returns a Transformation instance.

        :param transformations: Transformation proto object.
        """
        obj = Transformation.__new__(cls)
        obj._transformation_proto = transformation
        obj._fco_container = fco_container
        obj._transformation_spec = specs.TransformationSpec.from_data_proto(transformation)
        return obj

    @sdk_public_method
    def run(
        self,
        *inputs: Union["pd.DataFrame", "pd.Series", "TectonDataFrame", "pyspark.sql.DataFrame", spark_api.CONST_TYPE],
        context: BaseMaterializationContext = None,
    ) -> TectonDataFrame:
        """Run the transformation against inputs.

        :param inputs: positional arguments to the transformation function. For PySpark and SQL transformations,
                       these are either ``pandas.DataFrame`` or ``pyspark.sql.DataFrame`` objects.
                       For on-demand transformations, these are ``pandas.Dataframe`` objects.
        :param context: An optional materialization context object.
        """

        if self._transformation_spec.transformation_mode == TransformationMode.TRANSFORMATION_MODE_SPARK_SQL:
            return spark_api.run_transformation_mode_spark_sql(
                *inputs,
                transformer=self.transformer,
                context=context,
                transformation_name=self._transformation_spec.name,
            )
        elif self._transformation_spec.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYSPARK:
            return spark_api.run_transformation_mode_pyspark(*inputs, transformer=self.transformer, context=context)
        elif self._transformation_spec.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            return self._on_demand_run(*inputs)
        raise RuntimeError(f"{self._transformation_spec.transformation_mode} does not support `run(...)`")

    def _on_demand_run(self, *inputs) -> TectonDataFrame:
        for df in inputs:
            if not isinstance(df, pd.DataFrame):
                raise TypeError(f"Input must be of type pandas.DataFrame, but was {type(df)}.")

        return TectonDataFrame._create(self.transformer(*inputs))

    def summary(self):
        """
        Displays a human readable summary of this Transformation.
        """
        request = GetTransformationSummaryRequest()
        request.fco_locator.id.CopyFrom(self._transformation_proto.transformation_id)
        request.fco_locator.workspace = self.workspace

        response = metadata_service.instance().GetTransformationSummary(request)
        return Displayable.from_fco_summary(response.fco_summary)


@sdk_public_method
def get_transformation(name, workspace_name: Optional[str] = None) -> Transformation:
    """
    Fetch an existing :class:`tecton.interactive.Transformation` by name.

    :param name: An unique name of the registered Transformation.

    :return: A :class:`tecton.interactive.Transformation` class instance.

    :raises TectonValidationError: if a Transformation with the passed name is not found.
    """
    if workspace_name == None:
        logger.warning(
            "`tecton.get_transformation('<name>')` is deprecated. Please use `tecton.get_workspace('<workspace_name>').get_transformation('<name>')` instead."
        )

    request = GetTransformationRequest()
    request.name = name
    request.workspace = workspace_name or conf.get_or_none("TECTON_WORKSPACE")

    response = metadata_service.instance().GetTransformation(request)
    fco_container = FcoContainer.from_proto(response.fco_container)
    transformation_spec = fco_container.get_single_root()

    if transformation_spec is None:
        raise errors.FCO_NOT_FOUND(Transformation, name)

    assert isinstance(transformation_spec, specs.TransformationSpec)
    if conf.get_bool("UNIFIED_TECTON_OBJECTS_ENABLED"):
        return UnifiedTransformation._from_spec(transformation_spec)

    return Transformation._from_proto(transformation_spec.data_proto, fco_container)
