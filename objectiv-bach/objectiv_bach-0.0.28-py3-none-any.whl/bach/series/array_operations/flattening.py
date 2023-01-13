from abc import ABC, abstractmethod
from typing import TypeVar, Dict, Tuple, cast

from bach.expression import Expression, join_expressions
from bach.sql_model import BachSqlModel, construct_references
from sql_models.model import CustomSqlModelBuilder, Materialization

from bach.series import SeriesJson, SeriesInt64
from bach.utils import get_name_to_column_mapping

TSeriesJson = TypeVar('TSeriesJson', bound='SeriesJson')

_ITEM_IDENTIFIER_EXPR = Expression.identifier(name='__unnest_item')
_OFFSET_IDENTIFIER_EXPR = Expression.identifier(name='__unnest_item_offset')


class ArrayFlattening(ABC):
    """
    Abstract class that expands an array-type column into a set of rows.

    Child classes are in charge of
    1) specifying the correct expressions for unnesting arrays, by overriding `_get_cross_join_expression`.
    2) giving the correct offset for each item, by setting `_db_offset_is_one_based`.

    .. note::
        Final result will always have different base node than provided Series object.

    returns Tuple with:
        - SeriesJson: Representing the element of the array.
        - SeriesInt64: Offset of the element in the array
    """

    """
    _db_offset_is_one_based can be overridden by child classes to indicate that the offsets from the database
    are 1-based offsets instead of 0-based offsets.
    """
    _db_offset_is_one_based = False

    def __init__(self, series_object: 'TSeriesJson'):
        self._series_object = series_object.copy()

        if not self._series_object.is_materialized:
            self._series_object = cast(
                TSeriesJson, self._series_object.materialize(node_name='array_flatten')
            )

    def __call__(self, *args, **kwargs) -> Tuple['TSeriesJson', 'SeriesInt64']:
        from bach import DataFrame, SeriesInt64

        dialect = self._series_object.engine.dialect
        name_to_column_mapping = get_name_to_column_mapping(dialect=dialect, names=self.all_dtypes.keys())

        unnested_array_df = DataFrame.from_model(
            engine=self._series_object.engine,
            model=self._get_unnest_model(),
            index=list(self._series_object.index.keys()),
            all_dtypes=self.all_dtypes,
            name_to_column_mapping=name_to_column_mapping
        )
        item_series = unnested_array_df[self.item_series_name]
        offset_series = unnested_array_df[self.item_offset_series_name]
        return (
            cast(TSeriesJson, item_series),
            offset_series.copy_override_type(SeriesInt64),
        )

    @property
    def item_series_name(self) -> str:
        """
        Final name of the series containing the array elements.
        """
        return self._series_object.name

    @property
    def item_offset_series_name(self) -> str:
        """
        Final name of the series containing the offset of the element in the array.
        """
        return f'{self._series_object.name}_offset'

    @property
    def all_dtypes(self) -> Dict[str, str]:
        """
        Mapping of all dtypes of all referenced columns in generated model
        """
        return {
            **{idx.name: idx.dtype for idx in self._series_object.index.values()},
            self.item_series_name: self._series_object.dtype,
            self.item_offset_series_name: 'int64'
        }

    def _get_unnest_model(self) -> BachSqlModel:
        """
        Creates a BachSqlModel in charge of expanding the array column.
        """
        column_expressions = self._get_column_expressions()
        select_column_expr = join_expressions(list(column_expressions.values()))
        from_model_expr = Expression.model_reference(self._series_object.base_node)
        cross_join_expr = self._get_cross_join_expression()

        sql_exprs = [select_column_expr, from_model_expr, cross_join_expr]
        dialect = self._series_object.engine.dialect
        sql = Expression.construct('SELECT {} FROM {} CROSS JOIN {}', *sql_exprs).to_sql(dialect)

        return BachSqlModel(
            model_spec=CustomSqlModelBuilder(sql=sql, name='unnest_array'),
            placeholders={},
            references=construct_references(base_references={}, expressions=sql_exprs),
            materialization=Materialization.CTE,
            materialization_name=None,
            column_expressions=column_expressions,
        )

    def _get_column_expressions(self) -> Dict[str, Expression]:
        """
        Final column expressions for the generated model
        """
        dialect = self._series_object.engine.dialect

        offset_expr = _OFFSET_IDENTIFIER_EXPR
        if self._db_offset_is_one_based:
            offset_expr = Expression.construct('{} - 1', offset_expr)  # Normalize to 0-based offset

        return {
            **{
                idx.name: idx.expression for idx in self._series_object.index.values()
            },
            self.item_series_name: Expression.construct_expr_as_sql_name(
                dialect=dialect, expr=_ITEM_IDENTIFIER_EXPR, name=self.item_series_name
            ),
            self.item_offset_series_name: Expression.construct_expr_as_sql_name(
                dialect=dialect, expr=offset_expr, name=self.item_offset_series_name,
            ),
        }

    @abstractmethod
    def _get_cross_join_expression(self) -> Expression:
        """
        Expression that unnest/extract elements and offsets from array column. Later used
        in a cross join operation for joining the new set of rows back to the source.
        """
        raise NotImplementedError()


class BigQueryArrayFlattening(ArrayFlattening):

    # BigQuery uses 0-based offsets.
    _db_offset_is_one_based = False

    def _get_cross_join_expression(self) -> Expression:
        """ For documentation, see implementation in class :class:`ArrayFlattening` """
        return Expression.construct(
            'UNNEST(JSON_QUERY_ARRAY({}.{})) AS {} WITH OFFSET AS {}',
            Expression.model_reference(self._series_object.base_node),
            self._series_object,
            _ITEM_IDENTIFIER_EXPR,
            _OFFSET_IDENTIFIER_EXPR,
        )


class PostgresArrayFlattening(ArrayFlattening):

    # Postgres uses 1-based ordinality instead of 0-based offsets.
    _db_offset_is_one_based = True

    def _get_cross_join_expression(self) -> Expression:
        """ For documentation, see implementation in class :class:`ArrayFlattening` """
        return Expression.construct(
            'JSONB_ARRAY_ELEMENTS({}.{}) WITH ORDINALITY AS _unnested({}, {})',
            Expression.model_reference(self._series_object.base_node),
            self._series_object,
            _ITEM_IDENTIFIER_EXPR,
            _OFFSET_IDENTIFIER_EXPR,
        )


class AthenaArrayFlattening(ArrayFlattening):

    # Athena uses 1-based ordinality instead of 0-based offsets.
    _db_offset_is_one_based = True

    def _get_cross_join_expression(self) -> Expression:
        """ For documentation, see implementation in class :class:`ArrayFlattening` """
        return Expression.construct(
            'unnest(cast({}.{} as array(json))) with ordinality as _unnested({}, {})',
            Expression.model_reference(self._series_object.base_node),
            self._series_object,
            _ITEM_IDENTIFIER_EXPR,
            _OFFSET_IDENTIFIER_EXPR,
        )
