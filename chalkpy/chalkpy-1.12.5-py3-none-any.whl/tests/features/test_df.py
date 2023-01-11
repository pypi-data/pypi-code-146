import math
import pathlib
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import pandas as pd
import pyarrow as pa
import pydantic
import pytest
from pydantic import BaseModel

from chalk.features import DataFrame, Filter, after, feature, feature_time, features, has_many, has_one, unwrap_feature
from chalk.utils.annotation_parsing import ResolverAnnotationParser

try:
    import zoneinfo
except ImportError:
    # Zoneinfo was introduced in python 3.9
    from backports import zoneinfo

try:
    import polars as pl
except ImportError:
    pl = None


@dataclass(frozen=True)
class Foo:
    bar: int


class PydanticFoo(pydantic.BaseModel):
    bar: Optional[int]


@features
class ToppingPrice:
    id: str
    topping_id: str
    wow: str
    ts: datetime = feature_time()


@features
class Nickname:
    id: str


@features
class Taco:
    id: str
    user_id: str
    price: int
    maybe_price: Optional[int]
    maybe_str: Optional[str]
    hat: str
    topping_id: str
    ts: datetime = feature_time()
    unzoned_ts: datetime = feature(dtype=pa.timestamp("us", None))
    nicknames: DataFrame[Nickname] = has_many(lambda: Nickname.id == Taco.id)
    topping: "Topping" = has_one(lambda: Topping.id == Taco.topping_id)
    foo: Foo
    pydantic_foo: PydanticFoo
    foos: List[Foo]
    float_list: List[float]


@features
class Topping:
    id: str
    value: int
    ts: datetime = feature_time()
    nicknames: DataFrame[Nickname] = has_many(lambda: Nickname.id == Topping.id)
    price: ToppingPrice = has_one(lambda: ToppingPrice.topping_id == Topping.id)


class Thing(BaseModel):
    id: str
    wow: str


@features
class Silly:
    id: str
    name: str


@pytest.mark.skipif(pl is None, reason="Polars is not installed")
class TestDF:
    def test_read_csv(self, tmp_path: pathlib.Path):
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, "w") as file:
            file.write("2,joshua\n3,samantha")

        values = DataFrame.read_csv(
            tmp.name,
            columns={0: Silly.id, 1: Silly.name},
            has_header=False,
        )
        assert values[Silly.id].max() == "3"

    def test_dataframe_with_pydantic(self):
        assert pl is not None
        df_type = DataFrame[Thing]
        assert df_type.columns == ()
        assert df_type.__pydantic_model__ == Thing
        x = DataFrame(
            pl.DataFrame(
                {
                    "id": ["hello", "there"],
                    "wow": ["hello", "there"],
                }
            ),
            pydantic_model=Thing,
        )
        assert x["wow"].max() == "there"
        x.to_polars()
        x.to_pandas()

    def test_indexing(self):
        import polars.testing

        f = DataFrame({Taco.id: [1, 2, 3], Taco.price: [5, 6, 7]})
        polars.testing.assert_frame_equal(
            f.to_polars().collect()[-1],
            DataFrame(
                {
                    Taco.id: [3],
                    Taco.price: [7],
                }
            )
            .to_polars()
            .collect(),
        )

    def test_range(self):
        f = DataFrame({Taco.id: [1, 2, 3]})
        assert len(f[0:]) == len(f) == 3
        assert len(f[1:]) == 2
        assert len(f[0:1]) == 1

    def test_eq(self):
        assert (DataFrame.from_dict({Taco.id: [1, 1, 3]}) == DataFrame.from_dict({Taco.id: [1, 1, 3]})).all()
        assert not (DataFrame.from_dict({Taco.id: [1, 1, 2]}) == DataFrame.from_dict({Taco.id: [1, 1, 3]})).all()

    def test_eq_ignore_column_order(self):
        assert (
            DataFrame.from_dict({Taco.id: [1, 3], Taco.hat: ["foo", "bar"]})
            == DataFrame.from_dict({Taco.hat: ["foo", "bar"], Taco.id: [1, 3]})
        ).all()

    def test_from_pandas(self):
        df = pd.DataFrame({Taco.id: ["1", "2", "3"], Taco.price: [5, 6, 7]})
        chalk_df = DataFrame(df)
        is_eq = chalk_df.to_pandas() == df
        is_all_eq = is_eq.all().all()
        assert is_all_eq

    def test_empty(self):
        empty_df = DataFrame()
        assert empty_df.references_feature_set is None

    def test_datetimes_timezone(self):
        now_ts = datetime.now(timezone.utc)
        df = DataFrame(
            {
                Taco.ts: [now_ts],
                Taco.id: [1],
            }
        )
        item = df[Taco.ts].item()
        assert isinstance(item, datetime)
        assert item == now_ts

    def test_timezoned_datetime_str(self):
        df = DataFrame(
            {
                Taco.ts: [
                    # with a timezone, it should be converted
                    "2022-04-21T19:36:02.767566-07:00",
                    # without a timezone, it should be interpreted as the timezone of the column
                    "2022-04-21T19:36:02.767566",
                ],
                Taco.id: [1, 1],
            }
        )
        # The ts column is utc, so this should be converted
        assert df[Taco.ts].to_polars().collect().rows() == [
            (datetime(2022, 4, 22, 2, 36, 2, 767566, zoneinfo.ZoneInfo("UTC")),),
            (datetime(2022, 4, 21, 19, 36, 2, 767566, zoneinfo.ZoneInfo("UTC")),),
        ]

    def test_unzoned_datetime_str(self):
        df = DataFrame(
            {
                Taco.unzoned_ts: [
                    # with a timezone, it should be dropped
                    "2022-04-21T19:36:02.767566-07:00",
                    # without a timezone should also work
                    "2022-04-21T19:36:02.767566",
                ],
                Taco.id: [1, 1],
            }
        )
        # The ts column is utc, so this should be converted
        assert df[Taco.unzoned_ts].to_polars().collect().rows() == [
            (datetime(2022, 4, 21, 19, 36, 2, 767566),),
            (datetime(2022, 4, 21, 19, 36, 2, 767566),),
        ]

    def test_in(self):
        chalk_df = DataFrame(
            {
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.price: [1, 2, 10],
            }
        )
        one_two_three_tacos = chalk_df[Taco.price in (1, 2, 3)]
        assert isinstance(one_two_three_tacos, DataFrame)
        assert len(one_two_three_tacos) == 2
        assert one_two_three_tacos[Taco.price].max() == 2
        assert one_two_three_tacos[Taco.price].min() == 1
        in_tacos_1 = chalk_df[Taco.price in []]
        assert len(in_tacos_1) == 0
        in_tacos_2 = chalk_df[Taco.price in [444]]
        assert len(in_tacos_2) == 0
        in_tacos_3 = chalk_df[Taco.price not in [1, 4]]
        assert len(in_tacos_3) == 2
        in_tacos_4 = chalk_df[not Taco.price in [1]]
        assert len(in_tacos_4) == 2

    def test_struct(self):
        df = DataFrame(
            {
                Taco.foo: [Foo(1), Foo(2), Foo(3)],
                Taco.id: [1, 2, 3],
            }
        )
        ans_1 = df[Taco.foo == Foo(1), Taco.id]
        assert (ans_1 == DataFrame({Taco.id: ["1"]})).all()
        ans_2 = df[Taco.foo != Foo(1), Taco.id]
        assert (ans_2 == DataFrame({Taco.id: [2, 3]})).all()
        ans_3 = df[Taco.foo in [Foo(1)], Taco.id]
        assert (ans_3 == DataFrame({Taco.id: [1]})).all()
        ans_4 = df[Taco.foo not in [Foo(1)], Taco.id]
        assert (ans_4 == DataFrame({Taco.id: [2, 3]})).all()

    def test_empty_struct(self):
        assert pl is not None
        df = DataFrame({Taco.foo: []})
        assert df.to_polars().schema == {"taco.foo": pl.Struct([pl.Field("bar", pl.Int64)])}

    def test_null_struct(self):
        assert pl is not None
        df = DataFrame({Taco.foo: [None]})
        assert df.to_polars().schema == {"taco.foo": pl.Struct([pl.Field("bar", pl.Int64)])}
        # Polars does not distinguish between a null entry for a struct and a struct containing all null values
        assert df.to_polars().collect().rows() == [({"bar": None},)]

    def test_valid_and_null_struct(self):
        # Test a null value after the first value
        df = DataFrame({Taco.foo: [Foo(bar=1), Foo(bar=None)]})
        assert df.to_polars().schema == {"taco.foo": pl.Struct([pl.Field("bar", pl.Int64)])}
        assert df.to_polars().collect().rows() == [({"bar": 1},), ({"bar": None},)]

    def test_null_and_valid_struct(self):
        # Test a null value before the first value
        df = DataFrame(
            {
                Taco.foo: [
                    Foo(bar=None),
                    Foo(bar=1),
                ]
            }
        )
        assert df.to_polars().schema == {"taco.foo": pl.Struct([pl.Field("bar", pl.Int64)])}
        assert df.to_polars().collect().rows() == [({"bar": None},), ({"bar": 1},)]

    def test_null_and_valid_pydantic_struct(self):
        # Test a null value before the first value
        df = DataFrame(
            {
                Taco.pydantic_foo: [
                    PydanticFoo(bar=None),
                    PydanticFoo(bar=1),
                ]
            }
        )
        assert df.to_polars().schema == {"taco.pydantic_foo": pl.Struct([pl.Field("bar", pl.Int64)])}
        assert df.to_polars().collect().rows() == [({"bar": None},), ({"bar": 1},)]

    @pytest.mark.xfail(reason="Lists of structs are not fully supported")
    def test_null_list_struct(self):
        assert pl is not None
        df = DataFrame({Taco.foos: [None]})
        assert df.to_polars().schema == {"taco.foos": pl.List(pl.Struct([pl.Field("bar", pl.Int64)]))}
        assert df.to_polars().collect().rows() == [(None,)]

    def test_empty_list_struct(self):
        assert pl is not None
        df = DataFrame({Taco.foos: [[]]})
        assert df.to_polars().schema == {"taco.foos": pl.List(pl.Struct([pl.Field("bar", pl.Int64)]))}
        assert df.to_polars().collect().rows() == [([],)]

    def test_null_list_float(self):
        assert pl is not None
        df = DataFrame({Taco.float_list: [None]})
        assert df.to_polars().schema == {"taco.float_list": pl.List(pl.Float64)}
        assert df.to_polars().collect().rows() == [(None,)]

    def test_empty_list_float(self):
        assert pl is not None
        df = DataFrame({Taco.float_list: [[]]})
        assert df.to_polars().schema == {"taco.float_list": pl.List(pl.Float64)}
        assert df.to_polars().collect().rows() == [([],)]

    @pytest.mark.xfail(reason="Lists of structs are not fully supported")
    def test_list_of_null_struct(self):
        assert pl is not None
        # None for the struct element should be a list of one empty struct
        df = DataFrame({Taco.foos: [[None]]})
        assert df.to_polars().schema == {"taco.foos": pl.List(pl.Struct([pl.Field("bar", pl.Int64)]))}
        assert df.to_polars().collect().rows() == [
            ([{"bar": None}],),
        ]

    @pytest.mark.xfail(reason="Lists of structs are not fully supported")
    def test_list_of_not_null_struct(self):
        assert pl is not None
        df = DataFrame({Taco.foos: [[Foo(bar=1)]]})
        assert df.to_polars().schema == {"taco.foos": pl.List(pl.Struct([pl.Field("bar", pl.Int64)]))}
        assert df.to_polars().collect().rows() == [
            ([{"bar": 1}],),
        ]

    @pytest.mark.xfail(reason="Lists of structs are not fully supported")
    def test_list_of_null_and_not_null_struct(self):
        assert pl is not None
        # Test a null value before the first value
        df = DataFrame({Taco.foos: [[None, Foo(bar=1)]]})
        assert df.to_polars().schema == {"taco.foos": pl.List(pl.Struct([pl.Field("bar", pl.Int64)]))}
        assert df.to_polars().collect().rows() == [
            ([{"bar": None}, {"bar": 1}],),
        ]

    def test_missing_and_struct(self):
        assert pl is not None
        # Test a null value before the first value
        df = DataFrame(
            {
                Taco.foo: [
                    None,
                    Foo(bar=1),
                ]
            }
        )
        assert df.to_polars().schema == {"taco.foo": pl.Struct([pl.Field("bar", pl.Int64)])}
        assert df.to_polars().collect().rows() == [({"bar": None},), ({"bar": 1},)]

    def test_is_none(self):
        chalk_df = DataFrame(
            {
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.maybe_price: [20, None, 10],
            }
        )
        is_none = chalk_df[Taco.maybe_price is None]
        assert len(is_none) == 1
        equals_none = chalk_df[Taco.maybe_price == None]
        assert len(equals_none) == 1
        is_not_none = chalk_df[Taco.maybe_price is not None]
        assert len(is_not_none) == 2
        ne_none = chalk_df[Taco.maybe_price != None]
        assert len(ne_none) == 2

    def test_bool_op(self):
        chalk_df = DataFrame(
            {
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.maybe_price: [20, None, 10],
                Taco.price: [1, 2, 3],
            }
        )
        tacos = chalk_df[Taco.maybe_price is None or Taco.id == "t_1"]
        assert len(tacos) == 2
        tacos = chalk_df[Taco.maybe_price is None and Taco.id == "t_2"]
        assert len(tacos) == 1
        tacos = chalk_df[not (Taco.maybe_price is not None or not Taco.id == "t_2")]
        assert len(tacos) == 1

        tacos = chalk_df[Taco.maybe_price is None and Taco.id == "t_1"]
        assert len(tacos) == 0
        tacos = chalk_df[Taco.maybe_price is not None and (Taco.id == "t_1" or Taco.price == 3)]
        assert len(tacos) == 2
        tacos = chalk_df[Taco.maybe_price is not None and (Taco.id == "t_1" or Taco.price in [8, 4, 99])]
        assert len(tacos) == 1

    def test_after(self):
        assert pl is not None
        now = datetime.now()
        data = [now - timedelta(days=10), now]
        series = pl.Series(values=data, dtype=pl.Datetime)
        chalk_df = DataFrame(
            {
                Taco.ts: series,
                Taco.price: [5, 10],
            }
        )
        new_price = chalk_df[after(days_ago=5), Taco.price].sum()
        assert new_price == 10

    def test_filtering(self):
        chalk_df = DataFrame(
            {
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.price: [1, 5, 10],
            }
        )
        expensive_tacos = chalk_df[Taco.price > 1]
        assert isinstance(expensive_tacos, DataFrame)
        assert len(expensive_tacos) == 2
        assert expensive_tacos[Taco.price].max() == 10
        assert expensive_tacos[Taco.price].min() == 5

    def test_filter_and_project(self):
        chalk_df = DataFrame(
            {
                Taco.user_id: ["u_1", "u_1", "u_2"],
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.price: [1, 5, 10],
            }
        )
        expensive_tacos = chalk_df[Taco.price, Taco.price > 1, Taco.user_id == "u_1"]
        assert len(expensive_tacos) == 1
        assert expensive_tacos.max() == 5
        assert expensive_tacos.min() == 5

    def test_filter_many(self):
        chalk_df = DataFrame(
            {
                Taco.user_id: ["u_1", "u_1", "u_2"],
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.price: [1, 5, 10],
            }
        )
        expensive_tacos = chalk_df[Taco.price > 1, Taco.user_id == "u_1"]
        assert len(expensive_tacos) == 1
        assert expensive_tacos[Taco.price].max() == 5
        assert expensive_tacos[Taco.price].min() == 5

    def test_filtering_with_datetime(self):
        chalk_df = DataFrame(
            {
                Taco.user_id: ["u_1", "u_1", "u_2"],
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.price: [1, 5, 10],
                Taco.ts: [
                    datetime.now(tz=timezone.utc) - timedelta(days=3),
                    datetime.now(tz=timezone.utc) - timedelta(days=1),
                    datetime.now(tz=timezone.utc),
                ],
            }
        )
        recent_tacos = chalk_df[Taco.ts >= datetime.now(tz=timezone.utc) - timedelta(hours=3)]
        assert isinstance(recent_tacos, DataFrame)
        assert len(recent_tacos) == 1
        assert recent_tacos[Taco.price].max() == 10

    def test_indexing_one(self):
        chalk_df = DataFrame(
            {
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.price: [100, 200, 300],
            }
        )
        assert chalk_df[Taco.price].mean() == 200
        assert len(chalk_df[Taco.price]) == 3
        assert chalk_df[Taco.price].max() == 300
        assert chalk_df[Taco.price].min() == 100

    def test_indexing_many(self):
        import polars.testing

        chalk_df = DataFrame(
            {
                Taco.id: ["t_1", "t_2", "t_3"],
                Taco.price: [100, 200, 300],
                Taco.hat: ["green", "red", "blue"],
            }
        )
        actual = chalk_df[Taco.price, Taco.id]
        expected = DataFrame(
            {
                Taco.price: [100, 200, 300],
                Taco.id: ["t_1", "t_2", "t_3"],
            }
        )
        polars.testing.assert_frame_equal(actual.to_polars(), expected.to_polars())

    def test_input_feature_types(self):
        df = DataFrame({Taco.topping.id: ["1"]})
        assert df[Taco.topping.id].item() == "1"

    def test_from_dict(self):
        df = DataFrame(
            {
                Taco.topping.value: [100, 200],
            }
        )
        assert 300 == df[Taco.topping.value].sum()

    def test_from_list(self):
        assert 0 == len(DataFrame.from_list([]))
        assert len(DataFrame.from_list(Taco(price=123, user_id="33"))) == 1
        assert len(DataFrame.from_list([Taco(price=123, user_id="33")])) == 1
        assert len(DataFrame.from_list(Taco(price=123, user_id="33"), Taco(price=3, user_id="33"))) == 2
        assert len(DataFrame.from_list([Taco(price=123, user_id="33"), Taco(price=3, user_id="33")])) == 2
        with pytest.raises(ValueError):
            DataFrame.from_list(Taco(price=123, user_id="33"), Taco(price=3))

        with pytest.raises(ValueError):
            DataFrame.from_list(Taco(), Taco(price=3, user_id="33"))

    def test_ast_parsing(self):
        container = {1, 2, 3}

        def my_resolver(
            my_arg: DataFrame[
                Taco.price,
                Taco.user_id > "33",
                Taco.maybe_price is not None,
                Taco.maybe_price is None,
                Taco.price not in container,
                Taco.price in container or (Taco.topping.price == -3 and (Taco.hat == "cool" or Taco.price == 4)),
            ]
        ):
            ...

        fancy_index = ResolverAnnotationParser(my_resolver, globals(), locals()).parse_annotation("my_arg")
        assert issubclass(fancy_index, DataFrame)

        assert ">" == fancy_index.filters[0].operation
        assert "taco.user_id" == str(fancy_index.filters[0].lhs)
        assert "33" == fancy_index.filters[0].rhs

        assert "!=" == fancy_index.filters[1].operation
        assert "taco.maybe_price" == str(fancy_index.filters[1].lhs)
        assert None == fancy_index.filters[1].rhs

        assert "==" == fancy_index.filters[2].operation
        assert "taco.maybe_price" == str(fancy_index.filters[2].lhs)
        assert None == fancy_index.filters[2].rhs

        assert "not in" == fancy_index.filters[3].operation
        assert "taco.price" == str(fancy_index.filters[3].lhs)
        assert container == fancy_index.filters[3].rhs

        fancy_clause = fancy_index.filters[4]
        assert isinstance(fancy_clause, Filter)
        first_fancy = fancy_clause.lhs
        assert isinstance(first_fancy, Filter)
        assert "in" == first_fancy.operation
        assert "taco.price" == str(first_fancy.lhs)
        assert container == first_fancy.rhs

        assert "or" == fancy_clause.operation

    def test_to_pandas(self):
        df = DataFrame({ToppingPrice.id: ["hi"]})
        pandas_df = df.to_pandas()
        assert isinstance(pandas_df, pd.DataFrame)
        assert pandas_df.dtypes.tolist() == [pd.StringDtype()]
        assert pandas_df.columns.tolist() == [unwrap_feature(ToppingPrice.id)]
        assert pandas_df.values.tolist() == [["hi"]]

    def test_wrong_dtype(self):
        assert pl is not None
        with pytest.raises(
            TypeError,
            match="Feature `topping.value` at index 0 with value 'not_an_int' could not be converted to dtype `i64`",
        ):
            # Should raise if constructing via a dict
            DataFrame({Topping.value: ["not_an_int"]})

        with pytest.raises(TypeError, match="Values for feature `topping.value` could not be converted to dtype `i64`"):
            # Should also raise if passing in another dataframe
            DataFrame(pl.DataFrame({"topping.value": ["not_an_int"]}))
        with pytest.raises(TypeError, match="Values for feature `topping.value` could not be converted to dtype `i64`"):
            # If there is a type mismatch when passing in a lazyframe, we should materialize it and convert it immediately
            DataFrame(pl.DataFrame({"topping.value": ["not_an_int"]}).lazy())

    def test_item(self):
        df = DataFrame({Topping.value: [2]})
        assert df.item() == 2

    def test_float(self):
        df = DataFrame({Topping.value: [2]})
        assert float(df) == 2.0

    def test_int(self):
        df = DataFrame({Topping.value: [2]})
        assert int(df) == 2

    def test_aggregation(self):
        df = DataFrame({Topping.value: [2, 3]})
        assert df.mean() == 2.5
        assert df.sum() == 5
        assert df.min() == 2
        assert df.max() == 3
        assert df.median() == 2.5
        assert df.var() == 0.5
        assert df.std() == math.sqrt(0.5)

    def test_csv(self, tmp_path: pathlib.Path):
        df = DataFrame({Topping.value: [2, 3]})
        pl_df = df.to_polars().collect()
        pl_df = pl_df.rename({"topping.value": "my_col_name"})
        csv_filepath = tmp_path / "my_file.csv"
        pl_df.write_csv(csv_filepath, has_header=True)
        new_df = DataFrame.read_csv(csv_filepath, has_header=True, columns={"my_col_name": "topping.value"})
        assert (df == new_df).all()

    def test_parquet(self, tmp_path: pathlib.Path):
        df = DataFrame({Topping.value: [2, 3]})
        pl_df = df.to_polars().collect()
        pl_df = pl_df.rename({"topping.value": "my_col_name"})
        filepath = tmp_path / "my_file.csv"
        pl_df.write_parquet(filepath)
        new_df = DataFrame.read_parquet(filepath, columns={"my_col_name": "topping.value"})
        assert (df == new_df).all()

    def test_slice(self):
        df = DataFrame({Topping.value: [2, 3, 4]})
        assert (df.slice() == df).all()
        assert (df.slice(1) == DataFrame({Topping.value: [3, 4]})).all()
        assert (df.slice(3) == DataFrame({Topping.value: []})).all()
        # Out-of-range slices should be fine
        assert (df.slice(4) == DataFrame({Topping.value: []})).all()
        # Negative slicing should work, too
        assert (df.slice(-1) == DataFrame({Topping.value: [4]})).all()
        # Check that length is respected
        assert (df.slice(0, 2) == DataFrame({Topping.value: [2, 3]})).all()
        # If length is too big, then it should be equivalent to not specifying it
        assert (df.slice(0, 4) == DataFrame({Topping.value: [2, 3, 4]})).all()

    def test_to_features_no_hasone(self):
        """Test that to_features() works without a has-one relationship"""
        dt = datetime.now(timezone.utc)
        assert DataFrame({Topping.value: [1, 2], Topping.ts: [dt, dt]}).to_features() == [
            Topping(value=1, ts=dt),
            Topping(value=2, ts=dt),
        ]

    def test_to_features_with_hasone(self):
        df = DataFrame(
            {
                Topping.price.id: [2],
                Topping.id: [1],
                Topping.price.topping_id: [1],
                Topping.value: [5],
            }
        )

        assert df.to_features() == [Topping(id="1", value=5, price=ToppingPrice(id="2", topping_id="1"))]

    def test_eq_null(self):
        # Test that the Chalk DataFrame works around https://github.com/pola-rs/polars/issues/5870
        df1 = DataFrame({Taco.maybe_str: [None], Taco.maybe_price: [None]})
        df2 = DataFrame({Taco.maybe_str: [None], Taco.maybe_price: [None]})

        assert (df1 == df2).all()

    def test_all_empty(self):
        assert DataFrame().all()
        assert DataFrame({Taco.maybe_str: []}).all()

    def test_any_empty(self):
        assert not DataFrame().any()
        assert not DataFrame({Taco.maybe_str: []}).any()
