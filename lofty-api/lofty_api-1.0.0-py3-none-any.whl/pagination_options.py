class PaginationOptions:
    def __init__(
            self,
            next: str = None,
            # unix time in milliseconds
            start: int = None,
            # unix time in milliseconds
            end: int = None,
            # BE will default this to 2000 items, limited by the max items returned by dynamo
            page_size: int = 2000,
            # 'asc' or 'desc'
            # default desc - asc only used when start/end are not provided e.g. downloading the txn list for export.
            sort: str = 'desc',
    ):
        self.next = next
        self.start = start
        self.end = end
        self.page_size = page_size
        self.sort = sort

    def to_params(self) -> dict:
        params = {}
        if self.next:
            params['next'] = self.next
        if self.start:
            params['start'] = self.start
        if self.end:
            params['end'] = self.end
        if self.page_size:
            params['pageSize'] = self.page_size
        if self.sort:
            params['sort'] = self.sort

        return params