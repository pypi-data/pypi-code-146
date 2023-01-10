from sqlalchemy.orm import DeclarativeBase, MappedColumn


class Relation:
    def __init__(self, model: type[DeclarativeBase], **join_on):
        self.model = model
        if len(join_on):
            self.join_on = {}
            for foreign_col, local_col in join_on.items():
                if not isinstance(local_col, MappedColumn):
                    raise Exception("Local column has to be instance of MappedColumn")
                self.join_on[foreign_col] = local_col
        else:
            self.join_on = None
