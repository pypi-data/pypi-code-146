"""
Copyright 2021 Objectiv B.V.
"""
from typing import Tuple, Dict

import numpy
import pandas
from sqlalchemy.engine import Engine, Dialect

from bach import DataFrame, get_series_type_from_dtype
from bach.types import value_to_dtype, DtypeOrAlias, Dtype
from bach.expression import Expression, join_expressions
from bach.utils import get_sql_column_name, get_name_to_column_mapping
from sql_models.model import CustomSqlModelBuilder
from sql_models.util import quote_identifier, DatabaseNotSupportedException, is_postgres, is_bigquery, \
    is_athena


def from_pandas(engine: Engine,
                df: pandas.DataFrame,
                convert_objects: bool,
                name: str,
                materialization: str,
                if_exists: str = 'fail') -> DataFrame:
    """
    See DataFrame.from_pandas() for docstring.
    """
    if materialization == 'cte':
        return from_pandas_ephemeral(engine=engine, df=df, convert_objects=convert_objects, name=name)
    if materialization == 'table':
        return from_pandas_store_table(
            engine=engine,
            df=df,
            convert_objects=convert_objects,
            table_name=name,
            if_exists=if_exists
        )
    raise ValueError(f'Materialization should either be "cte" or "table", value: {materialization}')


def from_pandas_store_table(engine: Engine,
                            df: pandas.DataFrame,
                            convert_objects: bool,
                            table_name: str,
                            if_exists: str = 'fail') -> DataFrame:
    """
    Instantiate a new DataFrame based on the content of a Pandas DataFrame. This will first write the
    data to a database table using pandas' df.to_sql() method.
    Supported dtypes are 'int64', 'float64', 'string', 'datetime64[ns]', 'bool'


    :param engine: db connection
    :param df: Pandas DataFrame to instantiate as DataFrame
    :param convert_objects: If True, columns of type 'object' are converted to 'string' using the
        pd.convert_dtypes() method where possible.
    :param table_name: name of the sql table the Pandas DataFrame will be written to
    :param if_exists: {'fail', 'replace', 'append'}, default 'fail'
        How to behave if the table already exists:
        * fail: Raise a ValueError.
        * replace: Drop the table before inserting new values.
        * append: Insert new values to the existing table.
    """
    # todo add dtypes argument that explicitly let's you set the supported dtypes for pandas columns
    df_copy, index_dtypes, all_dtypes, name_to_column_mapping = _from_pd_shared(
        dialect=engine.dialect,
        df=df,
        convert_objects=convert_objects,
        cte=False
    )

    df_copy = df_copy.rename(columns=name_to_column_mapping)

    if is_athena(engine):
        _athena_pandas_to_sql(
            engine=engine,
            df=df_copy,
            table_name=table_name,
            if_exists=if_exists,
        )
    else:
        conn = engine.connect()
        df_copy.to_sql(name=table_name, con=conn, if_exists=if_exists, index=False)
        conn.close()

    index = list(index_dtypes.keys())
    return DataFrame.from_table(
        engine=engine,
        table_name=table_name,
        index=index,
        all_dtypes=all_dtypes,
        name_to_column_mapping=name_to_column_mapping
    )


def _athena_pandas_to_sql(df: pandas.DataFrame, table_name: str, engine: Engine, if_exists: str) -> None:
    """
    Helper function for writing records from a pandas DataFrame to Amazon Athena.
    Currently, pandas.DataFrame.to_sql is broken for Athena, as an alternative
    we use `pyathena.panda.util.to_sql`, which stores the records into the specified `location` parameter
    in the engine's url. In case the location is not specified, s3_staging_dir parameter will be used instead.
    """
    from pyathena.pandas.util import to_sql
    from pyathena.sqlalchemy_athena import AthenaDialect
    from pyathena.connection import Connection

    connection_args = AthenaDialect().create_connect_args(engine.url)[1]

    # The location of the Amazon S3 table is specified by the location parameter in the connection string.
    # If location is not specified, s3_staging_dir parameter will be used
    # s3://{location or s3_staging_dir}/{schema}/{table}/
    location = connection_args.get('location') or connection_args["s3_staging_dir"]
    location += "/" if not location.endswith("/") else ""
    location += f'{table_name}/'

    # Pandas.to_sql is not used as pyAthena's SQLAlchemy DDL Compiler replaces BIGINT columns
    # with INT db type, most likely a bug from pyathena as it raises a ParseException when trying
    # to execute the CREATE statement.
    # Fortunately, pyathena's to_sql function creates the correct DDL statement but requires a
    # pyathena Connection instead

    # For more information: https://pypi.org/project/pyathena/#pandas
    with Connection(**connection_args) as conn:
        to_sql(
            df,
            name=table_name,
            schema=connection_args['schema_name'],
            conn=conn,
            if_exists=if_exists,
            index=False,
            location=location
        )


def from_pandas_ephemeral(
        engine: Engine,
        df: pandas.DataFrame,
        convert_objects: bool,
        name: str
) -> DataFrame:
    """
    Instantiate a new DataFrame based on the content of a Pandas DataFrame. The data will be represented
    using a `select * from values()` query, or something similar depending on the database dialect.

    Warning: This method is only suited for small quantities of data.
    For anything over a dozen kilobytes of data it is recommended to store the data in a table in
    the database, e.g. by using the from_pd_store_table() function.

    Supported dtypes are 'int64', 'float64', 'string', 'datetime64[ns]', 'bool'

    :param engine: db connection
    :param df: Pandas DataFrame to instantiate as DataFrame
    :param convert_objects: If True, columns of type 'object' are converted to 'string' using the
        pd.convert_dtypes() method where possible.
    """
    # todo add dtypes argument that explicitly let's you set the supported dtypes for pandas columns
    df_copy, index_dtypes, all_dtypes, name_to_column_mapping = _from_pd_shared(
        dialect=engine.dialect,
        df=df,
        convert_objects=convert_objects,
        cte=True
    )

    column_series_type = [get_series_type_from_dtype(dtype) for dtype in all_dtypes.values()]

    per_row_expr = []
    for row in df_copy.itertuples():
        per_column_expr = []
        # Access the columns in `row` by index rather than by name. Because if a name starts with an
        # underscore (e.g. _index_skating_order) it will not be available as attribute.
        # so we use `row[i]` instead of getattr(row, column_name).
        # start=1 is to account for the automatic index that pandas adds
        for i, series_type in enumerate(column_series_type, start=1):
            val = row[i]
            per_column_expr.append(
                series_type.value_to_expression(dialect=engine.dialect, value=val, dtype=series_type.dtype)
            )
        row_expr = Expression.construct('({})', join_expressions(per_column_expr))
        per_row_expr.append(row_expr)
    all_values_str = join_expressions(per_row_expr, join_str=',\n').to_sql(engine.dialect)

    dialect = engine.dialect
    if is_postgres(engine) or is_athena(engine):
        # We are building sql of the form:
        #     select * from (values
        #         ('row 1', cast(1234 as bigint), cast(-13.37 as double precision)),
        #         ('row 2', cast(1337 as bigint), cast(31.337 as double precision))
        #     ) as t("a", "b", "c")
        column_names_expressions = []
        for series_name in all_dtypes.keys():
            sql_column_name = name_to_column_mapping.get(series_name, series_name)
            column_names_expressions.append(Expression.raw(quote_identifier(dialect, sql_column_name)))
        column_names_expr = join_expressions(column_names_expressions)
        column_names_str = column_names_expr.to_sql(engine.dialect)
        sql = f'select * from (values \n{all_values_str}\n) as t({column_names_str})\n'
    elif is_bigquery(engine):
        # We are building sql of the form:
        #     select * from UNNEST([
        #         STRUCT<`a` STRING, `b` INT64, `c` FLOAT64>
        #         ('row 1', 1234, cast(-13.37 as FLOAT64))
        #         ('row 2', 1337, cast(31.337 as FLOAT64))
        #     ])
        sql_column_name_types = []
        for series_name, dtype in all_dtypes.items():
            sql_column_name = name_to_column_mapping.get(series_name, series_name)
            db_col_name = quote_identifier(dialect=engine.dialect, name=sql_column_name)
            db_dtype = get_series_type_from_dtype(dtype).get_db_dtype(dialect=engine.dialect)
            sql_column_name_types.append(f'{db_col_name} {db_dtype}')
        sql_struct = f'STRUCT<{", ".join(sql_column_name_types)}>'
        sql = f'select * from UNNEST([{sql_struct} \n{all_values_str}\n])\n'
    else:
        raise DatabaseNotSupportedException(engine)

    model_builder = CustomSqlModelBuilder(sql=sql, name=name)
    sql_model = model_builder()

    index = list(index_dtypes.keys())
    return DataFrame.from_model(
        engine=engine,
        model=sql_model,
        index=index,
        all_dtypes=all_dtypes,
        name_to_column_mapping=name_to_column_mapping
    )


def _assert_column_names_valid(dialect: Dialect, df: pandas.DataFrame):
    """
    Performs three checks on the columns (not on the indices) of the DataFrame:
    1) All Series must have a string as name
    2) No duplicated Series names
    3) All Series names either are a valid column name or can be mapped to a valid column name in the given
        sql dialect.
    Will raise a ValueError if any of the checks fails
    """
    names = list(df.columns)
    not_strings = [name for name in names if not isinstance(name, str)]
    if not_strings:
        raise ValueError(f'Not all columns names are strings. Non-string names: {not_strings}')
    if len(set(names)) != len(names):
        raise ValueError(f'Duplicate column names in: {names}')

    for name in names:
        # Will raise an exception if this cannot be turned into a legal column_name
        get_sql_column_name(dialect=dialect, name=name)


def _from_pd_shared(
        dialect: Dialect,
        df: pandas.DataFrame,
        convert_objects: bool,
        cte: bool
) -> Tuple[pandas.DataFrame, Dict[str, Dtype], Dict[str, Dtype], Dict[str, str]]:
    """
    Pre-processes the given Pandas DataFrame, and do some checks. This results in a new DataFrame and three
    dictionaries with meta data. The returned DataFrame contains all processed data in the data columns, this
    includes any columns that were originally indices. The index_dtypes dict will indicate which of the data
    columns should be indexes. The name_to_column_mapping dict defines what column name should be used for
    each series; depending on the dialect certain names are not allowed as column names so we cannot just use
    the series names.

    Pre-processing/checks:
    1)  Add index if missing
    2a) Convert string columns to string dtype (if convert_objects)
    2b) Set content of columns of dtype other than `supported_pandas_dtypes` to supported types
        (if convert_objects & cte)
    3)  Check that the dtypes are supported
    4)  extract index_dtypes and dtypes dictionaries
    5) Check: all column names (after previous steps) are set, unique, and can be mapped to valid column
        names for the given dialect.

    :return: Tuple:
        * Modified copy of Pandas DataFrame. No index columns, the original index columns are regular
            columns in this copy.
        * index_dtypes dict. Mapping of index names to the dtype.
        * all_dtypes dict. Mapping of all series names to dtypes, includes data and index columns.
        * name_to_column_mapping: mapping of series name, to sql column name
    """
    index = []

    for idx, name in enumerate(df.index.names):
        if name is None:
            name = f'_index_{idx}'
        else:
            name = f'_index_{name}'

        index.append(name)

    df_copy = df.copy()
    df_copy.index.set_names(index, inplace=True)
    # set the index as normal columns, this makes it easier to convert the dtype
    df_copy.reset_index(inplace=True)

    supported_pandas_dtypes = ['int64', 'float64', 'string', 'datetime64[ns]', 'bool', 'int32']
    all_dtypes_or_alias: Dict[str, DtypeOrAlias] = {}
    for series_name in df_copy.columns:
        series_name = str(series_name)
        dtype = df_copy[series_name].dtype.name

        if dtype in supported_pandas_dtypes:
            all_dtypes_or_alias[series_name] = dtype
            continue

        if df_copy[series_name].dropna().empty:
            raise ValueError(f'{series_name} column has no non-nullable values, cannot infer type.')

        if convert_objects:
            df_copy[series_name] = df_copy[series_name].convert_dtypes(
                convert_integer=False, convert_boolean=False, convert_floating=False,
            )
            dtype = df_copy[series_name].dtype.name

        if dtype not in supported_pandas_dtypes and not(cte and convert_objects):
            raise TypeError(f'unsupported dtype for {series_name}: {dtype}')

        if cte and convert_objects:
            non_nullables = df_copy[series_name].dropna()
            types = non_nullables.apply(type).unique()
            if len(types) != 1:
                raise TypeError(f'multiple types found in column {series_name}: {types}')
            dtype = value_to_dtype(non_nullables.iloc[0])

        all_dtypes_or_alias[series_name] = dtype

    _assert_column_names_valid(dialect=dialect, df=df_copy)

    all_dtypes = {name: get_series_type_from_dtype(dtype_or_alias).dtype
                  for name, dtype_or_alias in all_dtypes_or_alias.items()}
    index_dtypes = {index_name: all_dtypes[index_name] for index_name in index}

    name_to_column_mapping = get_name_to_column_mapping(dialect=dialect, names=all_dtypes.keys())

    df_copy = df_copy.replace({numpy.nan: None})
    return df_copy, index_dtypes, all_dtypes, name_to_column_mapping
