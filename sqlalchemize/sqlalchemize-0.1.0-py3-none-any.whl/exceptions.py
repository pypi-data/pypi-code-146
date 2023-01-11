class ForceFail(Exception):
    pass


class MissingPrimaryKey(Exception):
    pass


class SliceError(IndexError):
    pass


def rollback_on_exception(method):
    def inner_method(self, *args, **kwargs):
        try:
            method(self, *args, **kwargs)
        except Exception as e:
            self.rollback()
            raise e
    return inner_method


def check_for_engine(sa_table, engine):
    if engine is None:
        engine = sa_table.bind
    if engine is None:
        raise ValueError('sa_table must be bound to engine or pass engine parameter.')
    return engine