class RestServiceMixin:
    def get(self, id_record):
        return self.repository.fetch_pk(id_record)

    def delete(self, id_record):
        return self.repository.delete_pk(id_record)

    def insert(self, record):
        return self.repository.insert_pk(record)

    def update(self, id_record, record):
        return self.repository.update(record, id_record)

    def exists(self, id_record):
        pass

    def list(
        self,
        search_fields: list,
        search_text: str = None,
        match_fields: dict = None,
        limit: int = None,
        offset: int = None,
        sort_fields: dict = None,
    ):
        pass
