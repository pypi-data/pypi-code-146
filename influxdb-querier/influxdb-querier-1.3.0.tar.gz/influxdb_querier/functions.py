
class QueryFunction(str):
    def __new__(cls, func, **kwargs):
        obj = super().__new__(cls, func)
        obj.func = func
        return obj

    def __str__(self):
        return str(self.func)

    @staticmethod
    def mean():
        return QueryFunction("mean")

    @staticmethod
    def max():
        return QueryFunction("max")

    @staticmethod
    def min():
        return QueryFunction("min")

    @staticmethod
    def count():
        return QueryFunction("count")

    @staticmethod
    def last():
        return QueryFunction("last")

    @staticmethod
    def sum():
        return QueryFunction("sum")

    def wrapkey(self, key):
        """
        Wraps a key with the given function to use for the SELECT clause in the query towards InfluxDB.
        Args:
            key: The key to wrap with the function.

        Returns:
            `key` wrapped with the function.
            e.g. max("key")
        """
        return f"{self.func}(\"{key}\")"


if __name__ == '__main__':
    print(QueryFunction.mean())
    print(QueryFunction.max())
    print(QueryFunction.min())
    print(QueryFunction.count())
    print(QueryFunction.last())

