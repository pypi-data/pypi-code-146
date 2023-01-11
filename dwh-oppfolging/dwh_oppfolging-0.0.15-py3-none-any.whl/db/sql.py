

def build_left_join_to_dimension_sql(
    dim_schema: str,
    dim_table: str,
    src_dim_equal_columns: list[tuple[str, str]],
    src_date_column: str,
    dim_date_valid_from_column: str,
    dim_date_valid_to_column: str,
    truncate_src_date: bool = True,
    truncate_dim_date: bool = False,
    half_open_valid_range: bool = False,
):
    """builds a left join from source table aliased as 'src' to dimension
    >>> build_left_join_to_dimension_sql("dims", "dim_emps", [("name_id", "name", "dept_id", "department")], "timestamp", "valid_from", "valid_to")
    'left join dims.dim_emps dim_emps on src.name_id = dim_emps.name and trunc(src.timestamp) between dim_emps.valid_from and dim_emps.valid_to'
    """
    def truncit(col: str):
        return col.join(("trunc(", ")"))
    equal_sql_fmt = "src.{} = " + dim_table + ".{}"
    src_date_sql = f"src.{src_date_column}"
    if truncate_src_date:
        src_date_sql = truncit(src_date_sql)
    dim_date_from_sql = f"{dim_table}.{dim_date_valid_from_column}"
    dim_date_to_sql = f"{dim_table}.{dim_date_valid_to_column}"
    if truncate_dim_date:
        dim_date_from_sql = truncit(dim_date_from_sql)
        dim_date_to_sql = truncit(dim_date_to_sql)
    if not half_open_valid_range:
        date_sql = f"{src_date_sql} between {dim_date_from_sql} and {dim_date_to_sql}"
    else:
        date_sql = f"{src_date_sql} >= {dim_date_from_sql} and {src_date_sql} < {dim_date_to_sql}"
    join_sql = (
        f"left join {dim_schema}.{dim_table} {dim_table} on "
        + " and ".join(
            equal_sql_fmt.format(pair[0], pair[1]) for pair in src_dim_equal_columns
        )
        + f" and {date_sql}"
    )
    return join_sql


def build_scd2_insert_sql(
    schema: str,
    table: str,
    source_select: str,
):
    """constructs the sql for an scd2 insert
    params:
        schema: target schema name
        table: target table name
        source_select: source table select statement
    """
    raise NotImplementedError
