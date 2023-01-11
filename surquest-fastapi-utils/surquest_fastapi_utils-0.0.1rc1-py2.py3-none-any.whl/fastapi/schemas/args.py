import datetime as dt
from fastapi import Query, Path


class QueryConfig(object):

    def __init__(self, type_, query):

        self.type_ = type_
        self.query = query

    @property
    def type(self):

        return self.type_


class PathConfig(object):

    def __init__(self, type_, path):

        self.type_ = type_
        self.path = path

    @property
    def type(self):

        return self.type_


class Args(object):

    start_date = QueryConfig(
        type_=dt.date,
        query=Query(
            default=dt.datetime.strptime("2022-10-01", "%Y-%m-%d").date(),
            alias="startDate",
            description="Start date (YYYY-MM-DD)",
            example=dt.datetime.strptime("2022-10-01", "%Y-%m-%d").date()
        )
    )
    end_date = QueryConfig(
        type_=dt.date,
        query=Query(
            default=dt.date.today(),
            alias="endDate",
            description="End date (YYYY-MM-DD)",
            example=dt.date.today()
        )
    )

    offset = QueryConfig(
        type_=int,
        query=Query(
            default=0,
            alias="offset",
            description="Offset for pagination",
            example=0
        )
    )

    limit = QueryConfig(
        type_=int,
        query=Query(
            default=1000,
            alias="limit",
            description="Limit for pagination",
            example=1000
        )
    )
