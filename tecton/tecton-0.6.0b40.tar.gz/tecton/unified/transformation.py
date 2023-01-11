from enum import Enum
from inspect import signature
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

import attrs
import pandas as pd
import pyspark
from google.protobuf.empty_pb2 import Empty
from typeguard import typechecked

from tecton._internals import display
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals.repo import function_serialization
from tecton.cli import common as cli_common
from tecton.declarative.transformation import Constant
from tecton.interactive import data_frame
from tecton.interactive import spark_api
from tecton.unified import common as unified_common
from tecton.unified import utils as unified_utils
from tecton.unified import validations_api
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_core import materialization_context
from tecton_core import specs
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import pipeline_pb2
from tecton_proto.args import transformation_pb2 as transformation__args_proto
from tecton_proto.common import fco_locator_pb2
from tecton_proto.metadataservice import metadata_service_pb2


class TransformationModeName(str, Enum):
    SPARK_SQL_MODE = "spark_sql"
    PYSPARK_MODE = "pyspark"
    SNOWFLAKE_SQL_MODE = "snowflake_sql"
    SNOWPARK_MODE = "snowpark"
    ATHENA_MODE = "athena"
    PANDAS_MODE = "pandas"
    PYTHON_MODE = "python"


@attrs.define
class Transformation(unified_common.BaseTectonObject):
    """Tecton class for Transformations.

    Attributes:
        _spec:  A transformation spec, i.e. a dataclass representation of the Tecton object that is used in most functional
            use cases, e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e.
            applied objects fetched from the backend, are assumed valid.
        _args: A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
            and fetched from the Tecton backend.
        _user_function: The user function for this transformation. Only set if this object was defined locally.
            It is needed to create the Transformation spec from args.
    """

    _args: transformation__args_proto.TransformationArgs = attrs.field(repr=False, on_setattr=attrs.setters.frozen)
    _spec: Optional[specs.TransformationSpec] = attrs.field(repr=False)
    _user_function: Optional[Callable] = attrs.field(repr=False)

    @typechecked
    def __init__(
        self,
        name: str,
        mode: str,
        user_function: Callable[..., Union[str, "pyspark.sql.DataFrame"]],
        description: Optional[str],
        owner: Optional[str],
        tags: Optional[Dict[str, str]],
    ):
        args = transformation__args_proto.TransformationArgs(
            transformation_id=id_helper.IdHelper.generate_id(),
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            info=basic_info_pb2.BasicInfo(name=name, description=description, owner=owner, family=None, tags=tags),
            transformation_mode=_get_transformation_mode_enum(mode, name),
            user_function=function_serialization.to_proto(user_function),
        )

        source_info = cli_common.get_fco_source_info()
        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.transformation_id)

        self.__attrs_init__(info=info, spec=None, args=args, source_info=source_info, user_function=user_function)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.TransformationSpec) -> "Transformation":
        """Create a Transformation from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = unified_common.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None, user_function=None)
        return obj

    def _build_args(self) -> fco_args_pb2.FcoArgs:
        if self._args is None:
            raise errors.BUILD_ARGS_INTERNAL_ERROR

        return fco_args_pb2.FcoArgs(transformation=self._args)

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    def __call__(self, *args, **kwargs) -> pipeline_pb2.PipelineNode:
        """Override the user defined transformation function.

        Returns a PipelineNode for this transformation which is used to construct the pipelines for feature views."""
        wrapper = pipeline_pb2.PipelineNode()
        node = wrapper.transformation_node
        node.transformation_id.CopyFrom(self.info._id_proto)
        user_function = self._spec.user_function if self._spec is not None else self._user_function

        try:
            bound_user_function = signature(user_function).bind(*args, **kwargs)
        except TypeError as e:
            raise TypeError(f"while binding inputs to function {self.info.name}, TypeError: {e}")

        materialization_context_count = 0
        # Construct input nodes from args for the user function
        for i, arg in enumerate(args):
            input_ = pipeline_pb2.Input()
            input_.arg_index = i
            input_.node.CopyFrom(self._value_to_node(arg))
            node.inputs.append(input_)
            if isinstance(arg, materialization_context.UnboundMaterializationContext):
                materialization_context_count += 1
        # Construct input nodes from kwargs for the user function
        for name, arg in kwargs.items():
            input_ = pipeline_pb2.Input()
            input_.arg_name = name
            input_.node.CopyFrom(self._value_to_node(arg))
            node.inputs.append(input_)
            if isinstance(arg, materialization_context.UnboundMaterializationContext):
                materialization_context_count += 1
        # Construct input nodes for default params for the user function
        for param in signature(user_function).parameters.values():
            if isinstance(param.default, materialization_context.UnboundMaterializationContext):
                if param.name in bound_user_function.arguments:
                    # the user passed in context explicitly, so no need to double register
                    continue
                input_ = pipeline_pb2.Input()
                input_.arg_name = param.name
                input_.node.CopyFrom(self._value_to_node(param.default))
                node.inputs.append(input_)
                if isinstance(param.default, materialization_context.UnboundMaterializationContext):
                    materialization_context_count += 1
            elif param.default is materialization_context:
                raise Exception(
                    "It seems you passed in tecton.materialization_context. Did you mean tecton.materialization_context()?"
                )

        if materialization_context_count > 1:
            raise Exception(f"Only 1 materialization_context can be passed into transformation {self.info.name}")

        return wrapper

    def _value_to_node(
        self,
        arg: Union[pipeline_pb2.PipelineNode, Constant, materialization_context.UnboundMaterializationContext],
    ) -> pipeline_pb2.PipelineNode:
        if isinstance(arg, pipeline_pb2.PipelineNode):
            return arg
        elif isinstance(arg, Constant):
            wrapper = pipeline_pb2.PipelineNode()
            node = wrapper.constant_node
            if arg.value is None:
                node.null_const.CopyFrom(Empty())
            elif arg.value_type == str:
                node.string_const = arg.value
            elif arg.value_type == int:
                node.int_const = repr(arg.value)
            elif arg.value_type == float:
                node.float_const = repr(arg.value)
            elif arg.value_type == bool:
                node.bool_const = arg.value
            return wrapper
        elif isinstance(arg, materialization_context.UnboundMaterializationContext):
            wrapper = pipeline_pb2.PipelineNode()
            wrapper.materialization_context_node.CopyFrom(pipeline_pb2.MaterializationContextNode())
            assert wrapper.HasField("materialization_context_node")
            return wrapper
        else:
            raise errors.InvalidTransformInvocation(self.info.name, arg)

    @property
    def transformer(self):
        """The user function for this transformation."""
        if self._spec is None:
            return self._user_function
        return self._spec.user_function

    @sdk_decorators.sdk_public_method
    def validate(self) -> None:
        if self._is_valid:
            print("Object has already been validated!")
            return

        validation_passed = validations_api.run_backend_validation([self])
        if validation_passed:
            self._spec = specs.TransformationSpec.from_args_proto(self._args, self._user_function)

    def _on_demand_run(self, *inputs: pd.DataFrame) -> data_frame.TectonDataFrame:
        for df in inputs:
            if not isinstance(df, pd.DataFrame):
                raise TypeError(f"Input must be of type pandas.DataFrame, but was {type(df)}.")

        return data_frame.TectonDataFrame._create(self.transformer(*inputs))

    @sdk_decorators.sdk_public_method
    @typechecked
    def run(
        self,
        *inputs: Union[
            "pd.DataFrame", "pd.Series", "data_frame.TectonDataFrame", "pyspark.sql.DataFrame", spark_api.CONST_TYPE
        ],
        context: materialization_context.BaseMaterializationContext = None,
    ) -> data_frame.TectonDataFrame:
        """Run the transformation against inputs.
        Currently, this method only supports spark_sql, pyspark, and pandas modes.

        :param inputs: positional arguments to the transformation function. For PySpark and SQL transformations,
                       these are either ``pandas.DataFrame`` or ``pyspark.sql.DataFrame`` objects.
                       For on-demand transformations, these are ``pandas.Dataframe`` objects.
        :param context: An optional materialization context object.
        """
        # TODO(TEC-11512): add support for other modes
        transformation_mode = (
            self._spec.transformation_mode if self._spec is not None else self._args.transformation_mode
        )
        if transformation_mode == transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SPARK_SQL:
            return spark_api.run_transformation_mode_spark_sql(
                *inputs, transformer=self.transformer, context=context, transformation_name=self.info.name
            )
        elif transformation_mode == transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYSPARK:
            return spark_api.run_transformation_mode_pyspark(*inputs, transformer=self.transformer, context=context)
        elif transformation_mode == transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PANDAS:
            return self._on_demand_run(*inputs)
        raise RuntimeError(f"{self._spec.transformation_mode} does not support `run(...)`")

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_remote_object
    def summary(self):
        """Displays a human readable summary of this Transformation."""
        request = metadata_service_pb2.GetTransformationSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetTransformationSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)


def _get_transformation_mode_enum(mode: str, name: str) -> transformation__args_proto.TransformationMode:
    if mode == TransformationModeName.SPARK_SQL_MODE:
        transform_mode = transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SPARK_SQL
    elif mode == TransformationModeName.PYSPARK_MODE:
        transform_mode = transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYSPARK
    elif mode == TransformationModeName.SNOWFLAKE_SQL_MODE:
        transform_mode = transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SNOWFLAKE_SQL
    elif mode == TransformationModeName.SNOWPARK_MODE:
        transform_mode = transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SNOWPARK
    elif mode == TransformationModeName.ATHENA_MODE:
        transform_mode = transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_ATHENA
    elif mode == TransformationModeName.PANDAS_MODE:
        transform_mode = transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PANDAS
    elif mode == TransformationModeName.PYTHON_MODE:
        transform_mode = transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYTHON
    else:
        raise errors.InvalidTransformationMode(
            name,
            mode,
            TransformationModeName,
        )
    return transform_mode


@typechecked
def transformation(
    mode: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
):
    """
    Declares a Transformation that wraps a user function. Transformations are assembled in a pipeline function of a Feature View.

    :param mode: The mode for this transformation must be one of "spark_sql", "pyspark", "snowflake_sql", "snowpark", "athena", "pandas" or "python".
    :param name: Unique, human friendly name that identifies the Transformation. Defaults to the function name.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :return: A wrapped transformation

    Examples of Spark SQL, PySpark, Pandas, and Python transformation declarations:

        .. code-block:: python

            from tecton import transformation
            from pyspark.sql import DataFrame
            import pandas as pd

            # Create a Spark SQL transformation.
            @transformation(mode="spark_sql",
                            description="Create new column by splitting the string in an existing column")
            def str_split(input_data, column_to_split, new_column_name, delimiter):
                return f'''
                    SELECT
                        *,
                        split({column_to_split}, {delimiter}) AS {new_column_name}
                    FROM {input_data}
                '''

             # Create an Athena transformation.
             @transformation(mode="athena",
                             description="Create new column by splitting the string in an existing column")
             def str_split(input_data, column_to_split, new_column_name, delimiter):
                 return f'''
                     SELECT
                         *,
                         split({column_to_split}, '{delimiter}') AS {new_column_name}
                     FROM {input_data}
                 '''

            # Create a PySpark transformation.
            @transformation(mode="pyspark",
                            description="Add a new column 'user_has_good_credit' if score is > 670")
            def user_has_good_credit_transformation(credit_scores):
                from pyspark.sql import functions as F

                (df = credit_scores.withColumn("user_has_good_credit",
                    F.when(credit_scores["credit_score"] > 670, 1).otherwise(0))
                return df.select("user_id", df["date"].alias("timestamp"), "user_has_good_credit") )

            # Create a Pandas transformation.
            @transformation(mode="pandas",
                            description="Whether the transaction amount is considered high (over $10000)")
            def transaction_amount_is_high(transaction_request):
                import pandas as pd

                df = pd.DataFrame()
                df['amount_is_high'] = (request['amount'] >= 10000).astype('int64')
                return df

            @transformation(mode="python",
                            description="Whether the transaction amount is considered high (over $10000)")
            # Create a Python transformation.
            def transaction_amount_is_high(transaction_request):

                result = {}
                result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
                return result
    """

    def decorator(user_function):
        transform_name = name or user_function.__name__
        transform = Transformation(transform_name, mode, user_function, description, owner, tags=tags)
        # TODO (samantha): check updating the wrapper is not neccessary, else add the line back and set slots=False
        # functools.update_wrapper(wrapper=transform, wrapped=user_function)

        return transform

    return decorator
