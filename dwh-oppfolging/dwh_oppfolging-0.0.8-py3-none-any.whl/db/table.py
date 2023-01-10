

class JoinRule:
    """Rule for joining with table"""
    def __init__(self, joining_columns: list[str], fetchable_columns: list[str]) -> None:
        self.joining_columns = joining_columns
        self.fetchable_columns = fetchable_columns
        raise NotImplementedError

class OracleTable:
    """Oracle DB Table"""
    def __init__(self, schema: str, name: str) -> None:
        self.schema = schema
        self.name = name
        self.fullname = schema + "." + name
        raise NotImplementedError