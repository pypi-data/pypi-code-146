from chalk.features import DataFrame
from chalk.utils.missing_dependency import missing_dependency_exception


def assert_frame_equal(a: DataFrame, b: DataFrame):
    try:
        import polars.testing
    except ImportError:
        raise missing_dependency_exception("chalkpy[polars]")
    return polars.testing.assert_frame_equal(a.to_polars().collect(), b.to_polars().collect())


def assert_frame_equal_ignore_order(a: DataFrame, b: DataFrame):
    try:
        import polars.testing
    except ImportError:
        raise missing_dependency_exception("chalkpy[polars]")
    a_polars = a.to_polars().collect()
    b_polars = b.to_polars().collect()
    return polars.testing.assert_frame_equal(
        a_polars.select(sorted(a_polars.columns)), b_polars.select(sorted(b_polars.columns))
    )
